from sqlalchemy.orm import Session
from db import get_db
from models import Book

def get_inventory(db: Session = None):
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
    try:
        books = db.query(Book).all()
        return [
            {
                'id': str(book.id),
                'title': book.title,
                'category': book.category,
                'price': float(book.price),
                'image': book.image,
                'stock': book.stock
            }
            for book in books
        ]
    finally:
        if db is not None:
            db.close()

def update_stock(db: Session, title: str, quantity: int):
    book = db.query(Book).filter(Book.title == title).first()
    if book and book.stock >= quantity:
        book.stock -= quantity
        db.commit()
        print(f"Stock updated for '{title}': {quantity} deducted (remaining: {book.stock})")
        return True
    else:
        print(f"Insufficient stock for '{title}' or book not found")
        return False

