import sys
import os
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Product, Category, Order, OrderProduct, Review, PromoCode, SupportChat, ProductQuestion

app = create_app()

def generate_products():
    base_products = [
        {"name": "Electric Kettle", "description": "Stainless steel electric kettle with temperature control.", "price": 89.99, "category_id": 1},
        {"name": "Fitness Tracker", "description": "Wearable fitness tracker with heart rate monitor and step counter.", "price": 59.99, "category_id": 1},
        {"name": "LED Desk Lamp", "description": "Adjustable LED desk lamp with touch control and dimming feature.", "price": 34.99, "category_id": 2},
        {"name": "Memory Foam Pillow", "description": "Contoured memory foam pillow with cooling gel.", "price": 49.99, "category_id": 2},
        {"name": "Camping Tent", "description": "2-person camping tent with waterproof and breathable fabric.", "price": 119.99, "category_id": 5},
        {"name": "Bluetooth Headphones", "description": "Over-ear Bluetooth headphones with noise cancellation.", "price": 99.99, "category_id": 1},
        {"name": "Wall-mounted Wine Rack", "description": "Elegant wall-mounted wine rack for up to 8 bottles.", "price": 59.99, "category_id": 3},
        {"name": "Electric Grill", "description": "Indoor electric grill with adjustable temperature control.", "price": 89.99, "category_id": 2},
        {"name": "Outdoor Lounge Chair", "description": "Adjustable outdoor lounge chair with reclining feature.", "price": 149.99, "category_id": 5},
        {"name": "Cordless Vacuum Cleaner", "description": "Powerful cordless vacuum cleaner with multiple attachments.", "price": 229.99, "category_id": 2},
        {"name": "Smart Light Bulbs", "description": "Set of 4 smart light bulbs with color-changing and dimming features.", "price": 49.99, "category_id": 1},
        {"name": "Multifunctional Blender", "description": "High-speed blender with multiple blending and chopping functions.", "price": 139.99, "category_id": 6},
        {"name": "Electric Blanket", "description": "Electric blanket with adjustable heat settings and automatic shut-off.", "price": 99.99, "category_id": 2},
        {"name": "Portable Grill", "description": "Compact and portable grill for outdoor cooking.", "price": 79.99, "category_id": 5},
        {"name": "Digital Camera", "description": "High-resolution digital camera with interchangeable lenses.", "price": 799.99, "category_id": 1},
        {"name": "KitchenAid Stand Mixer", "description": "Professional stand mixer with various speed settings and attachments.", "price": 349.99, "category_id": 6},
        {"name": "Men's Leather Wallet", "description": "Genuine leather wallet with multiple card slots and compartments.", "price": 39.99, "category_id": 3},
        {"name": "Adjustable Dumbbell Set", "description": "Set of adjustable dumbbells for various workout routines.", "price": 159.99, "category_id": 4},
        {"name": "Electric Wine Opener", "description": "Battery-operated wine opener with foil cutter and charging base.", "price": 34.99, "category_id": 3},
        {"name": "Portable Power Bank", "description": "High-capacity power bank for charging devices on the go.", "price": 29.99, "category_id": 1},
        {"name": "Cookware Set", "description": "Complete cookware set including pots, pans, and utensils.", "price": 249.99, "category_id": 6},
        {"name": "Electric Scooter", "description": "Foldable electric scooter with long battery life.", "price": 399.99, "category_id": 1}
    ]
    
    products = []
    for product in base_products:
        product["stock_quantity"] = random.randint(10, 100)
        products.append(product)
    return products

def seed_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create some categories
        categories = [
            {"name": "Electronics"},
            {"name": "Home Appliances"},
            {"name": "Furniture"},
            {"name": "Sports"},
            {"name": "Outdoor"},
            {"name": "Kitchen"}
        ]
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        db.session.commit()

        # Create users
        users = [
            {"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": True},
            {"username": "user1", "email": "user1@example.com", "password": "password123", "is_admin": False},
            {"username": "user2", "email": "user2@example.com", "password": "password456", "is_admin": False}
        ]
        for user_data in users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                is_admin=user_data['is_admin']
            )
            db.session.add(user)
        db.session.commit()

        # Create products
        products = generate_products()
        for prod_data in products:
            product = Product(**prod_data)
            db.session.add(product)
        db.session.commit()

        # Create orders
        orders = [
            {"user_id": 1, "total_amount": 299.97, "status": "Shipped"},
            {"user_id": 2, "total_amount": 89.99, "status": "Delivered"},
            {"user_id": 3, "total_amount": 199.98, "status": "Processing"}
        ]
        for order_data in orders:
            order = Order(**order_data)
            db.session.add(order)
        db.session.commit()

        # Create order products
        order_products = [
            {"order_id": 1, "product_id": 1, "quantity": 2, "price": 89.99},
            {"order_id": 1, "product_id": 2, "quantity": 1, "price": 59.99},
            {"order_id": 2, "product_id": 3, "quantity": 1, "price": 34.99},
            {"order_id": 3, "product_id": 4, "quantity": 4, "price": 49.99},
        ]
        for op_data in order_products:
            order_product = OrderProduct(**op_data)
            db.session.add(order_product)
        db.session.commit()

        # Create reviews
        reviews = [
            {"product_id": 1, "user_id": 1, "rating": 5, "comment": "Excellent kettle with precise temperature control!"},
            {"product_id": 2, "user_id": 2, "rating": 4, "comment": "Good fitness tracker, but the battery life could be better."},
            {"product_id": 4, "user_id": 3, "rating": 5, "comment": "The memory foam pillow is extremely comfortable!"}
        ]
        for review_data in reviews:
            review = Review(**review_data)
            db.session.add(review)
        db.session.commit()

        # Create promo codes
        promo_codes = [
            {"code": "SUMMER20", "discount_percentage": 20, "expiration_date": datetime(2024, 9, 30)},
            {"code": "WELCOME10", "discount_percentage": 10, "expiration_date": datetime(2024, 12, 31)},
            {"code": "BLACKFRIDAY50", "discount_percentage": 50, "expiration_date": datetime(2023, 11, 29)}
        ]
        for promo_data in promo_codes:
            promo_code = PromoCode(**promo_data)
            db.session.add(promo_code)
        db.session.commit()

        # Create support chats
        support_chats = [
            {"user_id": 1, "message": "Problem with order delivery"},
            {"user_id": 2, "message": "Account login issue"},
            {"user_id": 3, "message": "Product not as described"}
        ]
        for chat_data in support_chats:
            support_chat = SupportChat(**chat_data)
            db.session.add(support_chat)
        db.session.commit()

        # Create product questions
        product_questions = [
            {"product_id": 1, "user_id": 2, "question": "Does this kettle have a keep-warm function?", "answer": "Yes, it does.", "created_at": datetime.utcnow()},
            {"product_id": 2, "user_id": 3, "question": "What is the battery life of this fitness tracker?", "answer": "The battery lasts up to 7 days.", "created_at": datetime.utcnow()},
            {"product_id": 3, "user_id": 1, "question": "Is this desk lamp adjustable in terms of brightness?", "answer": "Yes, it has multiple brightness settings.", "created_at": datetime.utcnow()}
        ]
        for question_data in product_questions:
            question = ProductQuestion(**question_data)
            db.session.add(question)
        db.session.commit()

if __name__ == '__main__':
    seed_db()





