from sqlalchemy.orm import Session
from db import SessionLocal
from models import Payment

def save_payment(data: dict, db: Session = None):
    if db is None:
        db = SessionLocal()
        manual_commit = True
    else:
        manual_commit = False
    
    try:
        new_payment = Payment(
            name=data.get("name", "Unknown"),
            amount=data.get("amount", 0),
            method=data.get("method", "Not specified")
        )
        db.add(new_payment)
        db.commit()
        print(f"[DB] Payment saved to Supabase: {data.get('name')} - ₱{data.get('amount')} via {data.get('method')}")
        
    except Exception as e:
        if not manual_commit:
            db.rollback()
        raise Exception(f"Payment save failed: {str(e)}")
    finally:
        if manual_commit:
            db.close()
