from fastapi import APIRouter

from . import auth_router, user_router, form_router

router = APIRouter()

router.include_router(auth_router.router)
router.include_router(user_router.router)
router.include_router(form_router.router)
