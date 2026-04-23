import random
import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from order import save_order
from payment import save_payment

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'homestyle-secret-key-2024')

BOOKS = []
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
        'Realm of Ruins',
        'Age of Shadows',
        'The Folly Magic',
        'The Prince and the Witch',
        'A Storm of Shadows and Pearls',
        'Alice in Neverland',
        'The Fall of The Fairy Queen',
        'Return of the Dragons',
        'Last of Fae',
        'Gift of Earth'
    ],
    "Children's Books": [
        'The Secret Garden',
        'The Secret Life of Birds',
        'Mermaid to Rescue',
        'Little Polar Bear',
        'Story Thieves',
        'Princess Snarl',
        'Dinasaurs Loves Underpants',
        'Jack and the Beanstalk',
        'SIGFRED Goes to Hollywood',
        'In your own Backyard'
    ],
    'Mystery': [
        'Whispering Key',
        'The Forest of Damned Souls',
        'The Silo',
        'Dont Go There',
        'Murder n the GreenHouse',
        'Cut To the Bone',
        'A Date with Murder',
        'A Spoonful of Murder',
        'A Scenery of Loss',
        'Notebook Mysteries'
    ],
    'Romance': [
        'Love of My Life',
        'The Love Hyphotesis',
        'Love & other Words',
        'Say Youll be Mine',
        'Best Beloved',
        'Yours Forever',
        'Love More than Ever',
        'Wilde in Love',
        'The Art of Taking Second Chances',
        'Dinner for Two'
    ],
    'Wattpad': [
        'Once Upon a Crime',
        'The Darkest Night',
        'Entwined Obsession',
        'Fire and Light',
        'Frozen Hearts',
        'Digital Heartstrings',
        'Our Love Memories',
        'How to Burn the Bad Boy',
        'Baby Steps',
        'Half Blood'
    ],
    'History': [
        'Empires of Dawn',
        'The Forgotten Revolution',
        'Secrets of the Silk Road',
        'Chronicles of the Monarchs',
        'Battlefield of the Ages',
        'Legacy of the Founders',
        'Portraits of Power',
        'The Great Migration',
        'Voices from the Dust',
        'Treaty of the Crossroads'
    ],
    'Autobiography': [
        'Steps to Sunrise',
        'My Story, My Voice',
        'Becoming in the City',
        'The Road I Chose',
        'A Life Unscripted',
        'Lessons from the Climb',
        'Against the Current',
        'Finding Home Again',
        'Notes from the Journey',
        'The Years Between'
    ],
    'Drama': [
        'Curtain Call Confessions',
        'Broken Mirrors',
        'The Last Encore',
        'Behind the Velvet Rope',
        'Stage of Secrets',
        'Echoes in the Lobby',
        'Distant Applause',
        'Fractured Spotlight',
        'Act Two Betrayal',
        'Scenes from the Edge'
    ],
    'SciFi': [
        'Orbit of the Lost',
        'Neon Sky Exodus',
        'Quantum Ghosts',
        'The Binary Frontier',
        'Colony in the Stars',
        'Singularity Drift',
        'Androids of Avalon',
        'Planetfall Protocol',
        'Celestial Rebellion',
        'Timewave Paradox'
    ],
    'Action': [
        'Sabotage Run',
        'Crossfire Gamble',
        'Breakpoint Zero',
        'Shadow Strike Unit',
        'Deadlock Chase',
        'Rogue Mission',
        'Terminal Velocity',
        'Code Red Rescue',
        'Apex Assault',
        'Final Countdown'
    ]
}
for category, prefix in categories.items():
    titles = category_titles.get(category, [])
    for index in range(1, 11):
        title = titles[index - 1] if index <= len(titles) else f'{category} Book #{index}'
        BOOKS.append({
            'id': f'{prefix}{index}',
            'title': title,
            'category': category,
            'price': random.randint(*price_ranges[category]),
            'image': f'images/{prefix}{index}.jpg'
        })
print(f"Loaded {len(BOOKS)} books")  # Debug

def get_items(query='', category=''):
    q = query.lower().strip()
    c = category.lower().strip()
    filtered = [
        book for book in BOOKS
        if (not q or q in book['title'].lower() or q in book['category'].lower())
        and (not c or c == book['category'].lower())
    ]
    return [
        {
            'id': book['id'],
            'title': book['title'],
            'category': book['category'],
            'price': book['price'],
            'image': book['image']
        }
        for book in filtered
    ]

@app.route('/')
def home():
    return render_template('index.html', items=get_items(), categories=list(categories.keys()))

@app.route('/search')
def search():
    return jsonify(get_items(request.args.get('query', ''), request.args.get('category', '')))

@app.route('/checkout')
def checkout():
    temp_cart_str = request.args.get('cart', '{}')
    try:
        temp_cart = json.loads(temp_cart_str)
    except:
        temp_cart = {}
    
    session['cart'] = temp_cart
    return render_template('checkout.html', cart=temp_cart)

@app.route('/place-order', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        cart = data.get('cart', {})
        customer = data.get('customer', {})
        total = data.get('total', 0)
        
        # Debug logging
        print(f"\n=== PLACE ORDER DEBUG ===")
        print(f"Cart type: {type(cart)}")
        print(f"Cart content: {cart}")
        print(f"Cart is empty: {not cart}")
        print(f"Customer: {customer}")
        print(f"Total: {total}")
        print(f"========================\n")
        
        if not cart:
            return jsonify({'success': False, 'error': 'No cart items'})
        
        # Convert cart to simple format if needed
        simple_cart = {}
        for title, qty_data in cart.items():
            if isinstance(qty_data, dict):
                simple_cart[title] = qty_data.get('qty', 1)
            else:
                simple_cart[title] = int(qty_data) if qty_data else 1
        
        # Save order
        try:
            print("Attempting to save order...")
            order_id = save_order(simple_cart, customer, total)
            print(f"Order saved successfully: {order_id}")
        except Exception as order_error:
            print(f"ERROR in save_order: {str(order_error)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': f'Failed to save order: {str(order_error)}'})
        
        # Save payment method
        try:
            print("Attempting to save payment...")
            payment_data = {
                'name': customer.get('name', 'Unknown'),
                'amount': total,
                'method': customer.get('payment', 'Not specified')
            }
            save_payment(payment_data)
            print("Payment saved successfully")
        except Exception as payment_error:
            print(f"ERROR in save_payment: {str(payment_error)}")
            import traceback
            traceback.print_exc()
        
        session.pop('cart', None)
        
        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Error in place_order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

port = int(os.getenv('PORT', 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
