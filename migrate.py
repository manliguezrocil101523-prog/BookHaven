import os
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from db import SessionLocal, Base, engine
from models import Book, Order, OrderItem, Payment
import random

# Book generation data from app.py
categories = {
    'Fantasy': 'fantasy',
    "Children's Books": "children'sfiction",
    'Mystery': 'mystery',
    'Romance': 'romance',
    'Wattpad': 'wattpad',
    'History': 'history',
    'Autobiography': 'autobiography',
    'Drama': 'drama',
    'SciFi': 'scifi',
    'Action': 'action'
}
price_ranges = {
    'Fantasy': (250, 450),
    "Children's Books": (180, 320),
    'Mystery': (220, 380),
    'Romance': (240, 380),
    'Wattpad': (180, 300),
    'History': (260, 420),
    'Autobiography': (280, 460),
    'Drama': (230, 390),
    'SciFi': (260, 440),
    'Action': (250, 430)
}
category_titles = {
    'Fantasy': [
        'Realm of Ruins', 'Age of Shadows', 'The Folly Magic', 'The Prince and the Witch', 'A Storm of Shadows and Pearls', 'Alice in Neverland', 'The Fall of The Fairy Queen', 'Return of the Dragons', 'Last of Fae', 'Gift of Earth'
    ],
    "Children's Books": [
        'The Secret Garden', 'The Secret Life of Birds', 'Mermaid to Rescue', 'Little Polar Bear', 'Story Thieves', 'Princess Snarl', 'Dinasaurs Loves Underpants', 'Jack and the Beanstalk', 'SIGFRED Goes to Hollywood', 'In your own Backyard'
    ],
    'Mystery': [
        'Whispering Key', 'The Forest of Damned Souls', 'The Silo', 'Dont Go There', 'Murder n the GreenHouse', 'Cut To the Bone', 'A Date with Murder', 'A Spoonful of Murder', 'A Scenery of Loss', 'Notebook Mysteries'
    ],
    'Romance': [
        'Love of My Life', 'The Love Hyphotesis', 'Love & other Words', 'Say Youll be Mine', 'Best Beloved', 'Yours Forever', 'Love More than Ever', 'Wilde in Love', 'The Art of Taking Second Chances', 'Dinner for Two'
    ],
    'Wattpad': [
        'Once Upon a Crime', 'The Darkest Night', 'Entwined Obsession', 'Fire and Light', 'Frozen Hearts', 'Digital Heartstrings', 'Our Love Memories', 'How to Burn the Bad Boy', 'Baby Steps', 'Half Blood'
    ],
    'History': [
        'Empires of Dawn', 'The Forgotten Revolution', 'Secrets of the Silk Road', 'Chronicles of the Monarchs', 'Battlefield of the Ages', 'Legacy of the Founders', 'Portraits of Power', 'The Great Migration', 'Voices from the Dust', 'Treaty of the Crossroads'
    ],
    'Autobiography': [
        'Steps to Sunrise', 'My Story, My Voice', 'Becoming in the City', 'The Road I Chose', 'A Life Unscripted', 'Lessons from the Climb', 'Against the Current', 'Finding Home Again', 'Notes from the Journey', 'The Years Between'
    ],
    'Drama': [
        'Curtain Call Confessions', 'Broken Mirrors', 'The Last Encore', 'Behind the Velvet Rope', 'Stage of Secrets', 'Echoes in the Lobby', 'Distant Applause', 'Fractured Spotlight', 'Act Two Betrayal', 'Scenes from the Edge'
    ],
    'SciFi': [
        'Orbit of the Lost', 'Neon Sky Exodus', 'Quantum Ghosts', 'The Binary Frontier', 'Colony in the Stars', 'Singularity Drift', 'Androids of Avalon', 'Planetfall Protocol', 'Celestial Rebellion', 'Timewave Paradox'
    ],
    'Action': [
        'Sabotage Run', 'Crossfire Gamble', 'Breakpoint Zero', 'Shadow Strike Unit', 'Deadlock Chase', 'Rogue Mission', 'Terminal Velocity', 'Code Red Rescue', 'Apex Assault', 'Final Countdown'
    ]
}

def seed_books(db: Session):
    db.query(Book).delete()
    count = 0
    for category, prefix in categories.items():
        titles = category_titles.get(category, [])
        for index in range(1, 11):
            title = titles[index - 1] if index <= len(titles) else f'{category} Book #{index}'
            book = Book(
                title=title,
                category=category,
                price=random.randint(*price_ranges[category]),
                image=f'images/{prefix}{index}.jpg',
                stock=50
            )
            db.add(book)
            count += 1
    db.commit()
    print(f"Seeded {count} books")

def migrate_orders(db: Session):
    orders_file = 'data/order.xml'
    if os.path.exists(orders_file):
        tree = ET.parse(orders_file)
        root = tree.getroot()
        for xml_order in root.findall('order'):
            order_id = xml_order.get('id')
            total = float(xml_order.get('total'))
            items_count = int(xml_order.get('items_count', 0))
            
            # Skip if already migrated
            existing = db.query(Order).filter(Order.order_id == order_id).first()
            if existing:
                print(f"Order {order_id} already exists, skipping")
                continue
            
            new_order = Order(order_id=order_id, total=total, items_count=items_count)
            db.add(new_order)
            db.flush()
            
            for item in xml_order.find('items').findall('item'):
                title = item.get('title')
                qty = int(item.get('qty'))
                db.add(OrderItem(order_id=order_id, title=title, qty=qty))
            
            print(f"Migrated order {order_id}")
        db.commit()

def migrate_payments(db: Session):
    payments_file = 'data/payment.xml'
    if os.path.exists(payments_file):
        tree = ET.parse(payments_file)
        root = tree.getroot()
        for xml_payment in root.findall('payment'):
            name = xml_payment.find('name').text if xml_payment.find('name') is not None else 'Unknown'
            amount_str = xml_payment.find('amount').text if xml_payment.find('amount') is not None else '0'
            method = xml_payment.find('method').text if xml_payment.find('method') is not None else 'Not specified'
            
            new_payment = Payment(name=name, amount=float(amount_str), method=method)
            db.add(new_payment)
        db.commit()
        print("Migrated payments")

if __name__ == '__main__':
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_books(db)
        migrate_orders(db)
        migrate_payments(db)
        print("Migration complete! Data now in Supabase.")
    finally:
        db.close()
