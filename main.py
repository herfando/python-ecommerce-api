from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.users import router
from core.logging_config import configure_logging
import logging

# setup logging
configure_logging()
logger = logging.getLogger(__name__)

# lifespan handler (REPLACEMENT on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("🚀 Backend is starting...")

    yield  # app jalan di sini

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