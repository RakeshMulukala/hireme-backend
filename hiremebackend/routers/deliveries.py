from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hiremebackend import models, schemas, database_module
from hiremebackend.auth import get_current_user
from typing import List

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

@router.post("/", response_model=schemas.DeliveryRead)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(database_module.get_db), current_user: models.User = Depends(get_current_user)):
    db_delivery = models.Delivery(
        item_name=delivery.item_name,
        quantity=delivery.quantity,
        pickup_address=delivery.pickup_address,
        dropoff_address=delivery.dropoff_address,
        instructions=delivery.instructions,
        user_id=current_user.id
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.get("/", response_model=List[schemas.DeliveryRead])
def get_deliveries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database_module.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Delivery)
        .filter(models.Delivery.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
