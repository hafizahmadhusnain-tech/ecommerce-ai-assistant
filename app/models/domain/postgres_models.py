from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.postgres import Base

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, index=True, default="General")
    rating = Column(Float, default=4.5)

class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    status = Column(String, default="Pending") # Pending, Processing, Shipped, In Transit, Delivered
    total_amount = Column(Float, nullable=False)
    items_summary = Column(String, default="")
    courier = Column(String, default="Standard Express")
    estimated_delivery = Column(String, default="2-3 Business Days")
    created_at = Column(DateTime, default=datetime.utcnow)