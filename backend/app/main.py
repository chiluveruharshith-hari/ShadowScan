from fastapi import FastAPI
from .modules.url_module.route import router as url_router
from .modules.phone_module.route import router as phone_router
from .modules.sms_module.route import router as sms_router
from .routes.fusion_route import router as fusion_router  # ✅ ADD THIS
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ShadowScan API")

app.include_router(url_router)
app.include_router(phone_router)
app.include_router(sms_router)
app.include_router(fusion_router)  

@app.get("/")
def read_root():
    return {"message": "ShadowScan API is active"}