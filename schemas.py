from typing import Any, Optional, Union
from pydantic import BaseModel, Field


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


class UserCreateSchema(BaseModel):
    email: str


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    education_level: Optional[str] = Field(default="beginner")
    email: Optional[str] = None
    phone: Optional[str] = None
    access_level: Optional[int] = Field(ge=0, le=3, default=0)
    password: Optional[str] = None
    role: Optional[str] = Field(default="user")
