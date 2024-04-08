from sqlalchemy import Column, Integer, String, ARRAY, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# created_at = Column(DateTime, default=func.now())
# updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SettingsModel(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    tariffs = Column(ARRAY(JSON))
    payments = Column(ARRAY(JSON))
    updated_at = Column(String)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    education_level = Column(String, default="beginner")
    created_at = Column(DateTime, default=func.now())
    email = Column(String)
    phone = Column(String)
    access_level = Column(Integer, default=0)
    password = Column(String)
    role = Column(String, default="user")

    payments = relationship("PaymentModel", back_populates="user")


class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")  # pending <-> success <-> failure
    sum = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="payments")
