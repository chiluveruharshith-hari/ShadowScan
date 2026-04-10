from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .modules.url_module.route import router as url_router
from .modules.phone_module.route import router as phone_router
from .modules.sms_module.route import router as sms_router
from .routes.fusion_route import router as fusion_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="ShadowScan API")

# CORS — allow frontend (file://, localhost, any origin for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router)
app.include_router(phone_router)
app.include_router(sms_router)
app.include_router(fusion_router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/")
def read_root():
    return {"message": "ShadowScan API is active"}