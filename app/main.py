from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.services.sqlite_service import ensure_schema

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
def initialize_database() -> None:
    ensure_schema()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.APP_NAME} is running", "env": settings.ENV}
