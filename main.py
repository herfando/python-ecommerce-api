from fastapi import FastAPI
from api import 
from code.logging_config import configure_logging

setup_logging()
app = FastAPI(title="Acumen Backend")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Backend running"}