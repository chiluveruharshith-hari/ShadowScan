from fastapi import FastAPI
from .modules.url_module.route import router as url_router
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="ShadowScan URL Analysis")

# Register the URL analysis router
app.include_router(url_router)

@app.get("/")
def read_root():
    return {"message": "ShadowScan URL Analysis API is active"}
