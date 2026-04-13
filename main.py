from fastapi import FastAPI, File, UploadFile
from contextlib import asynccontextmanager
from api.users import router
from core.logging_config import configure_logging
import logging

# =========================
# ENV CONFIG
# =========================
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CLOUDINARY SETUP
# =========================
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# =========================
# AWS S3 SETUP
# =========================
import boto3
import uuid

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# =========================
# LOGGING
# =========================
configure_logging()
logger = logging.getLogger(__name__)

# =========================
# LIFESPAN (START/STOP APP)
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Backend is starting...")
    yield
    logger.info("🛑 Backend is shutting down...")

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Python Backend",
    lifespan=lifespan
)

app.include_router(router)

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def root():
    return {"message": "Backend running"}

# =========================
# CLOUDINARY UPLOAD
# =========================
@app.post("/upload-cloudinary")
async def upload_cloudinary(file: UploadFile = File(...)):
    logger.info(f"Uploading to Cloudinary: {file.filename}")

    result = cloudinary.uploader.upload(file.file)

    return {
        "filename": file.filename,
        "url": result["secure_url"]
    }

# =========================
# AWS S3 UPLOAD (FIXED + PRO)
# =========================
@app.post("/upload-s3")
async def upload_s3(file: UploadFile = File(...)):
    logger.info(f"Uploading to S3: {file.filename}")

    try:
        # bikin nama file unik biar tidak ketimpa
        file_key = f"uploads/{uuid.uuid4()}-{file.filename}"

        # upload ke S3
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file_key,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # URL hasil upload
        url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_key}"

        return {
            "filename": file.filename,
            "url": url
        }

    except Exception as e:
        logger.error(f"S3 upload failed: {str(e)}")
        return {"error": str(e)}