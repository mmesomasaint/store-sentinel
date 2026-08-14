# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import router as store_router

api_router = APIRouter()
api_router.include_router(store_router, prefix="/stores", tags=["Store Inspection"])
