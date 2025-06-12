from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hiremebackend import models, schemas, database_module
from hiremebackend.auth import get_password_hash, get_current_user
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(database_module.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserRead])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(database_module.get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()
