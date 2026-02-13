from fastapi import APIRouter

from app.api.v1.endpoints.compteurs import router as compteurs_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.pistes import router as pistes_router
from app.api.v1.endpoints.pointsdinteret import router as pointsdinteret_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(compteurs_router)
api_v1_router.include_router(pistes_router)
api_v1_router.include_router(pointsdinteret_router)
