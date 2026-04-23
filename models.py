from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    image = Column(String(255))
    stock = Column(Integer, default=50)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(20), unique=True, nullable=False, index=True)
    total = Column(DECIMAL(10,2), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    items_count = Column(Integer)

    order_items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(String(20), ForeignKey('orders.order_id'), nullable=False)
    title = Column(String(255))
    qty = Column(Integer)

    order = relationship('Order', back_populates='order_items')

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    name = Column(String(255))
    amount = Column(DECIMAL(10,2))
    method = Column(String(100))

