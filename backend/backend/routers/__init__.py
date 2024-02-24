from fastapi import APIRouter
from backend.routers import api

router = APIRouter()
router.include_router(api.router)
