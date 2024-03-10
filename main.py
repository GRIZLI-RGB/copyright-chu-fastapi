from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="КОПИРАЙЧУ",
    docs_url="/api/swagger",
    redoc_url=None
)

app.include_router(router)
