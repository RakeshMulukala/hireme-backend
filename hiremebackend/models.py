from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from hiremebackend.database_module import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Fix here — must match Coupon's relationship
    deliveries = relationship("Delivery", back_populates="user")
    coupons = relationship("Coupon", back_populates="owner")



class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)  # THIS IS CRUCIAL
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    pickup_address = Column(String, nullable=False)
    dropoff_address = Column(String, nullable=False)
    instructions = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="deliveries")


# models.py
class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    expiry = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    discount = Column(Float, nullable=True)  # or Integer, depending on your needs
    description = Column(String, nullable=True)
    owner = relationship("User", back_populates="coupons")


