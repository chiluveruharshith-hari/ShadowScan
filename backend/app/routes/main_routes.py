from fastapi import APIRouter
from app.modules.phone_module.route import router as phone_router
from app.modules.sms_module.route import router as sms_router

main_router = APIRouter()

main_router.include_router(phone_router, prefix="/analyze", tags=["Phone"])
main_router.include_router(sms_router, prefix="/analyze", tags=["SMS"])