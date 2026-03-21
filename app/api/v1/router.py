from fastapi import APIRouter

from app.controllers.v1 import health, imagine

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(imagine.router, tags=["imagine"])
