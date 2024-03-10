import ssl
from email.mime.text import MIMEText
from fastapi_mail import FastMail, MessageSchema, MessageType
import models
import smtplib
from datetime import datetime
from fastapi import APIRouter, HTTPException
from mail import config
from schemas import SettingsSchema, SettingsUpdateSchema, UserSchema, UserCreateSchema, UserUpdateSchema
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

db_depends = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/api"
)

default_settings = {"tariffs": [
    {"icon": "clock", "name": "Быстрый старт", "price": 589, "access_level": 1, "advantages": ["Преимущество 1"]}
],
    "payments": [
        {"tag": "Банковские карты", "name": "Сбер", "recipient": "Козлов Е.И.", "img": "sber",
         "requisites": "+7(982)783-04-18"}
    ],
    "updated_at": datetime.utcnow()}


@router.get("/settings", tags=["Настройки"], summary="Получить настройки", response_model=SettingsSchema)
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


@router.patch("/settings", tags=["Настройки"], summary="Обновить настройки", response_model=SettingsSchema)
async def update_settings(db: db_depends, body: SettingsUpdateSchema):
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


@router.get("/users", tags=["Пользователи"], summary="Получить всех пользователей", response_model=list[UserSchema])
async def get_users(db: db_depends):
    return db.query(models.UserModel).all()


@router.get("/user/{id}", tags=["Пользователи"], summary="Получить пользователя по ID", response_model=UserSchema)
async def get_user_by_id(id: int, db: db_depends):
    query_user = db.query(models.UserModel).get(id)
    if query_user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с ID {id} не найден")
    else:
        return query_user


@router.post("/user", tags=["Пользователи"], summary="Первоначальное создание пользователя", response_model=UserSchema)
async def create_user(body: UserCreateSchema, db: db_depends):
    new_user = models.UserModel(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.patch("/user/{id}", tags=["Пользователи"], summary="Обновить пользователя", response_model=UserSchema)
async def update_user(id: int, body: UserUpdateSchema, db: db_depends):
    pass


@router.delete("/user/{id}", tags=["Пользователи"], summary="Удалить пользователя", response_model=dict[str, bool])
async def delete_user(id: int, db: db_depends):
    pass


@router.post('/test/send-mail/fast-api-mail', tags=['Почта'])
async def send_mail_fast_api_mail():
    try:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=["ek916569@gmail.com"],
            body="Hi this test mail, thanks for using Fastapi-mail",
            subtype=MessageType.html)
        fm = FastMail(config)
        await fm.send_message(message)
        return {"message": "success"}
    except Exception as e:
        raise (HTTPException(status_code=500, detail="Неизвестная ошибка при отправке почты"))


@ router.post('/test/send-mail/smtplib', tags=['Почта'])
async def send_mail_smtplib():
    try:
        msg = MIMEText('This is test mail')

        msg['Subject'] = 'Test mail'
        msg['From'] = 'support@copyright-chu.ru'
        msg['To'] = 'ek916569@gmail.com'

        with smtplib.SMTP('smtp.timeweb.ru', 25) as server:
            server.login('support@copyright-chu.ru', '/fQd.b55yG2uF(')
            server.sendmail('support@copyright-chu.ru', ['ek916569@gmail.com'], msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Неизвестная ошибка при отправке почты")
