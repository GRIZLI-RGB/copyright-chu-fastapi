from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routes import router
from sqladmin import Admin, ModelView
import models

app = FastAPI(
    title="КОПИРАЙЧУ",
    docs_url="/api/swagger",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

admin = Admin(app, engine)


class UsersAdmin(ModelView, model=models.UserModel):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-sharp fa-solid fa-user"
    column_list = "__all__"


class PaymentsAdmin(ModelView, model=models.PaymentModel):
    name = "Платёж"
    name_plural = "Платежи"
    icon = "fa-sharp fa-solid fa-credit-card-alt"
    column_list = "__all__"


admin.add_view(UsersAdmin)
admin.add_view(PaymentsAdmin)

app.include_router(router)
