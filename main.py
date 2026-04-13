from fastapi import FastAPI, File, UploadFile
from contextlib import asynccontextmanager
from api.users import router
from core.logging_config import configure_logging
import logging

# ✅ TAMBAHAN
import cloudinary
import cloudinary.uploader

# setup logging
configure_logging()
logger = logging.getLogger(__name__)

# ✅ CONFIG CLOUDINARY (ISI PUNYA LO)
cloudinary.config(
    cloud_name="ISI_CLOUD_NAME",
    api_key="ISI_API_KEY",
    api_secret="ISI_API_SECRET"
)

# lifespan handler (REPLACEMENT on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("🚀 Backend is starting...")
    yield
    # SHUTDOWN
    logger.info("🛑 Backend is shutting down...")

# create app pakai lifespan
app = FastAPI(
    title="Python Backend",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Backend running"}

# =========================================
# ✅ TAMBAHAN ENDPOINT UPLOAD
# =========================================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Uploading file: {file.filename}")

    result = cloudinary.uploader.upload(file.file)

    return {
        "filename": file.filename,
        "url": result["secure_url"]
    }