import random
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Order, OrderItem

import random
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Order, OrderItem, Book
from inventory import update_stock

def save_order(cart: dict, customer: dict, total: float, db: Session = None):
    if db is None:
        db = SessionLocal()
        manual_commit = True
    else:
        manual_commit = False
    
    try:
        # Validate and update stock first
        for title, qty in cart.items():
            if not update_stock(db, title, qty):
                raise Exception(f"Insufficient stock for '{title}'")
        
        # Generate unique order_id (6 digits)
        order_id = str(random.randint(100000, 999999))
        
        # Create main order record
        new_order = Order(
            order_id=order_id,
            total=total,
            items_count=sum(cart.values())
        )
        db.add(new_order)
        db.flush()
        
        # Create order_items for each cart item
        for title, qty in cart.items():
            item = OrderItem(
                order_id=order_id,
                title=title,
                qty=qty
            )
            db.add(item)
        
        db.commit()
        print(f"[DB] Order {order_id} saved to Supabase: {len(cart)} items, total ₱{total}")
        return order_id
        
    except Exception as e:
        if not manual_commit:
            db.rollback()
        else:
            db.rollback()
        raise Exception(f"Database save failed: {str(e)}")
    finally:
        if manual_commit:
            db.close()
