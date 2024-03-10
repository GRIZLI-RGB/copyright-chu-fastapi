from fastapi_mail import ConnectionConfig

config = ConnectionConfig(
    MAIL_USERNAME="support@copyright-chu.ru",
    MAIL_PASSWORD="/fQd.b55yG2uF(",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.timeweb.ru",
    MAIL_FROM_NAME="Desired Name",
    MAIL_FROM="support@copyright-chu.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)
