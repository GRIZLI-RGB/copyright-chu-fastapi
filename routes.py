import schemas
import models
from fastapi_mail import FastMail, MessageSchema, MessageType
from datetime import datetime
from fastapi import APIRouter, HTTPException
from mail import config
from sqlalchemy.orm import Session
from typing import Annotated, Any
from fastapi import Depends
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

db_depends = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/api"
)

default_settings = {"tariffs": [
    {"icon": "clock", "name": "Быстрый старт", "price": 589, "access_level": 1,
     "advantages": ["Стандартные уроки", "Интерактивных тренажеры (24 ч)", "Поддержка 24/7"]},
    {"icon": "path", "name": "Серьёзный настрой", "price": 1490, "access_level": 2,
     "advantages": ["Стандартные уроки", "База знаний", "Партнерство", "Поддержка 24/7"]},
    {"icon": "crown", "name": "Всё включено!", "price": 4379, "access_level": 3,
     "advantages": ["Стандартные и продвинутые уроки", "База знаний", "Интерактивные тренажеры", "VIP-партнерство",
                    "VIP-поддержка 24/7"]},
],
    "payments": [
        {"tag": "Банковские карты", "name": "Сбер", "recipient": "Козлов Е.И.", "img": "sber",
         "requisites": "+7(982)783-04-18"},
         {"tag": "Банковские карты", "name": "Тинькофф", "recipient": "Козлов Е.И.", "img": "tinkoff",
         "requisites": "+7(982)783-04-18"},
    ],
    "updated_at": datetime.utcnow()}


@router.get("/settings", tags=["Настройки"], summary="Получить настройки", response_model=schemas.SettingsSchema)
async def get_settings(db: db_depends):
    settings = db.query(models.SettingsModel).all()
    if len(settings) > 0:
        return settings[0]
    else:
        new_settings = models.SettingsModel(**default_settings)
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings


@router.patch("/settings", tags=["Настройки"], summary="Обновить настройки", response_model=schemas.SettingsSchema)
async def update_settings(db: db_depends, body: schemas.SettingsUpdateSchema):
    settings = db.query(models.SettingsModel).all()
    if len(settings) > 0:
        db.query(models.SettingsModel).update(body.dict(), synchronize_session="fetch")
        db.commit()
        last_settings = db.query(models.SettingsModel).get(1)
        return last_settings
    else:
        settings_enters = {**body.dict(), **default_settings}
        new_settings = models.SettingsModel(**settings_enters)
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings


@router.get("/users", tags=["Пользователи"], summary="Получить всех пользователей",
            response_model=list[schemas.UserSchema])
async def get_users(db: db_depends):
    return db.query(models.UserModel).all()


@router.get("/user/{id}", tags=["Пользователи"], summary="Получить пользователя по ID",
            response_model=schemas.UserSchema)
async def get_user_by_id(id: int, db: db_depends):
    query_user = db.query(models.UserModel).get(id)
    if query_user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с ID {id} не найден")
    else:
        return query_user


@router.post("/user", tags=["Пользователи"], summary="Первоначальное создание пользователя",
             response_model=schemas.UserSchema)
async def create_user(body: schemas.UserCreateSchema, db: db_depends):
    try:
        settings = db.query(models.SettingsModel).first()
        for tariff in settings.tariffs:
            if body.access_level == tariff['access_level']:
                new_user = models.UserModel(email=body.email)
                new_payment = models.PaymentModel(sum=tariff['price'])
                new_user.payments = [new_payment]
                db.add_all([new_user, new_payment])
                db.commit()
                print(f"https://copyright-chu.ru/payment/{new_payment.id}")
                # message = MessageSchema(
                #     subject="Оплата по платёжному документу номер 39",
                #     recipients=[body.email],
                #     body=f"<h1>Заказ №{new_payment.id}</h1><br/><br/><p>Для оплаты тарифа «Быстрый старт» перейдите по ссылке: <a href='https://copyright-chu.ru/payment/{new_payment.id}'>https://copyright-chu.ru/payment/{new_payment.id}</a></p>",
                #     subtype=MessageType.html)
                # fm = FastMail(config)
                # await fm.send_message(message)

        return new_user
    except Exception as e:
        raise (HTTPException(status_code=500, detail="Ошибка при создании пользователя"))


@router.patch("/user/{id}", tags=["Пользователи"], summary="Обновить пользователя по ID",
              response_model=schemas.UserSchema)
async def update_user(id: int, body: schemas.UserUpdateSchema, db: db_depends):
    query_user = db.query(models.UserModel).filter(models.UserModel.id == id)
    db_user = query_user.first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Нет пользователя c ID {id}')

    update_data = body.dict(exclude_unset=True)
    query_user.filter(models.UserModel.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/user/{id}", tags=["Пользователи"], summary="Удалить пользователя по ID",
               response_model=schemas.OperationSchema)
async def delete_user(id: int, db: db_depends):
    query_user = db.query(models.UserModel).get(id)
    db.delete(query_user)
    db.commit()
    return {"status": True}


@router.get("/payments", tags=["Финансы"], summary="Получить все платежи", response_model=list[schemas.PaymentSchema])
async def get_payments(db: db_depends):
    return db.query(models.PaymentModel).all()


@router.get("/payment/{id}", tags=["Финансы"], summary="Получить платёж по ID", response_model=schemas.PaymentSchema)
async def get_payment_by_id(id: int, db: db_depends):
    query_payment = db.query(models.PaymentModel).get(id)
    if query_payment is None:
        raise HTTPException(status_code=404, detail=f"Платёж с ID {id} не найден")
    else:
        return query_payment


@router.patch("/payment/{id}", tags=["Финансы"], summary="Обновить платёж по ID", response_model=schemas.PaymentSchema)
async def update_payment(id: int, body: schemas.PaymentUpdateSchema, db: db_depends):
    db.query(models.PaymentModel).update(body.dict())
    db.commit()
    query_payment = db.query(models.PaymentModel).get(id)
    return query_payment
