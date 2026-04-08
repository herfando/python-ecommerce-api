from fastapi import FastAPI
from api import users

app = FastAPI(title="Acumen Backend")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Backend running"}