from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserOut
from core.database import get_db
from services.user_service import create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user