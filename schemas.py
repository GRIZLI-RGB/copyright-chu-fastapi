from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class OperationSchema(BaseModel):
    status: bool
    details: Optional[str] = None


class PaymentMethodSchema(BaseModel):
    tag: str
    name: str
    img: str
    recipient: str
    requisites: str


class TariffSchema(BaseModel):
    icon: str
    name: str
    price: int = Field(ge=1)
    access_level: int = Field(ge=0, le=3)
    advantages: list[str]


class SettingsSchema(BaseModel):
    id: int
    tariffs: Optional[list[TariffSchema]] = None
    payments: Optional[list[PaymentMethodSchema]] = None
    updated_at: Any


class SettingsUpdateSchema(BaseModel):
    tariffs: Optional[list[TariffSchema]] = None
    payments: Optional[list[PaymentMethodSchema]] = None
    updated_at: Any


class PaymentSchema(BaseModel):
    id: int
    status: str
    sum: int
    created_at: datetime
    user_id: int
    # user: UserSchema - тут выкидывает ошибку рекурсии какую-то


class PaymentUpdateSchema(BaseModel):
    status: str


class UserSchema(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    education_level: str = Field(default="beginner")
    created_at: Any
    email: str
    phone: Optional[str] = None
    access_level: int = Field(ge=0, le=3, default=0)
    password: Optional[str] = None
    role: str = Field(default="user")
    payments: Optional[list[PaymentSchema]] = Field(default=[])


class UserCreateSchema(BaseModel):
    email: str
    access_level: int = Field(gе=0, le=3)


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    education_level: Optional[str] = Field(default="beginner")
    email: Optional[str] = None
    phone: Optional[str] = None
    access_level: Optional[int] = Field(ge=0, le=3, default=0)
    password: Optional[str] = None
    role: Optional[str] = Field(default="user")
