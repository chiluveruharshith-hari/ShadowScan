from fastapi import FastAPI
from .modules.url_module.route import router as url_router
from .modules.phone_module.route import router as phone_router   # ✅ ADD THIS
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ShadowScan API")

# Register routers
app.include_router(url_router)
app.include_router(phone_router)  

@app.get("/")
def read_root():
    return {"message": "ShadowScan API is active"}