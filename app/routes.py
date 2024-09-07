
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, abort
from app.models import User, Product, Order, Review, Category
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import (
    generate_new_password, send_reset_email, compare_product_features, get_product_questions
)

bp = Blueprint('api', __name__)

# User Routes

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if request.method == 'GET':
        return jsonify({"username": user.username, "email": user.email})
    if request.method == 'PUT':
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({"message": "Profile updated"})

@bp.route('/profile/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url  # Assuming you have an avatar_url field
    })

@bp.route('/profile/avatar', methods=['PUT'])
@jwt_required()
def update_avatar():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.avatar_url = data.get('avatar_url')
    db.session.commit()
    return jsonify({"message": "Avatar updated"})

@bp.route('/password-reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    new_password = generate_new_password()
    user.set_password(new_password)
    db.session.commit()
    send_reset_email(user.email, new_password)
    return jsonify({"message": "Password reset email sent"})

# Product Management

@bp.route('/products', methods=['GET'])
def product_listing():
    products = Product.query.all()
    return jsonify([product.name for product in products])

@bp.route('/products/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({"name": product.name, "description": product.description, "price": product.price})

@bp.route('/products/search', methods=['GET'])
def product_search():
    query = request.args.get('q')
    products = Product.query.filter(Product.name.contains(query)).all()
    return jsonify([product.name for product in products])

@bp.route('/products/categories', methods=['GET'])
def product_categories():
    categories = Category.query.all()
    return jsonify([category.name for category in categories])

@bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(product_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    new_review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=data['rating'],
        comment=data.get('comment')
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added"}), 201

@bp.route('/products/<int:product_id>/compare', methods=['GET'])
def compare_products(product_id):
    other_product_id = request.args.get('other_product_id')
    if not other_product_id:
        return jsonify({"message": "Other product ID is required"}), 400
    
    comparison = compare_product_features(product_id, int(other_product_id))
    return jsonify(comparison)

@bp.route('/products/<int:product_id>/questions', methods=['GET'])
def product_questions(product_id):
    questions = get_product_questions(product_id)
    return jsonify(questions)

@bp.route('/products/advanced-search', methods=['GET'])
def advanced_product_search():
    # Implement your advanced search logic here
    return jsonify({"message": "Advanced search endpoint"})

@bp.route('/products/<int:product_id>/qa', methods=['GET'])
def get_product_qa(product_id):
    # Implement your logic to get questions and answers for a product here
    return jsonify({"message": "Product QA endpoint"})

@bp.route('/products/<int:product_id>/qa', methods=['POST'])
@jwt_required()
def submit_product_qa(product_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    # Implement your logic to submit a question for a product here
    return jsonify({"message": "Question submitted"})

@bp.route('/products/recommendations', methods=['GET'])
def product_recommendations():
    # Implement your logic to get personalized recommendations here
    return jsonify({"message": "Product recommendations endpoint"})

@bp.route('/products/<int:product_id>/notify', methods=['POST'])
def notify_back_in_stock(product_id):
    data = request.get_json()
    # Implement your logic to add a notification request for a product here
    return jsonify({"message": "Notification request added"})

# Wishlist

@bp.route('/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    user_id = get_jwt_identity()
    # Implement your logic to retrieve the user's wishlist here
    return jsonify({"message": "Wishlist retrieved"})

@bp.route('/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    data = request.get_json()
    user_id = get_jwt_identity()
    # Implement your logic to add a product to the user's wishlist here
    return jsonify({"message": "Product added to wishlist"})

# Cart and Checkout

@bp.route('/cart', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def cart():
    user_id = get_jwt_identity()
    
    if request.method == 'GET':
        cart_items = get_cart_items(user_id)  # Implement this function
        return jsonify(cart_items)

    if request.method == 'POST':
        data = request.get_json()
        add_to_cart(user_id, data['product_id'], data['quantity'])  # Implement this
        return jsonify({"message": "Added to cart"})

    if request.method == 'DELETE':
        data = request.get_json()
        remove_from_cart(user_id, data['product_id'])  # Implement this
        return jsonify({"message": "Removed from cart"})

@bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    # Implement your checkout logic
    order_id = process_checkout(user_id)  # You should implement this function
    return jsonify({"message": "Checkout successful", "order_id": order_id})

@bp.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    # Process payment using the provided data
    payment_status = process_payment(data)  # Implement this function
    if payment_status:
        return jsonify({"message": "Payment successful"})
    else:
        return jsonify({"message": "Payment failed"}), 400

# Order Management

@bp.route('/orders', methods=['GET'])
@jwt_required()
def order_history():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": order.id, "total_amount": order.total_amount} for order in orders])

@bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def order_tracking(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    return jsonify({"status": order.status})  # Assuming an order status field exists

@bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def order_cancellation(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    if cancel_order(order):  # Implement this function
        return jsonify({"message": "Order cancelled"})
    else:
        return jsonify({"message": "Unable to cancel order"}), 400

# Admin Panel

@bp.route('/admin/products', methods=['POST'])
@jwt_required()
def admin_add_product():
    data = request.get_json()
    if not check_admin(get_jwt_identity()):  # Implement this function
        return jsonify({"message": "Access forbidden"}), 403
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added"}), 201

@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def admin_view_users():
    if not check_admin(get_jwt_identity()):  # Implement this function
        return jsonify({"message": "Access forbidden"}), 403
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def admin_view_orders():
    if not check_admin(get_jwt_identity()):  # Implement this function
        return jsonify({"message": "Access forbidden"}), 403
    orders = Order.query.all()
    return jsonify([{"id": order.id, "total_amount": order.total_amount, "status": order.status} for order in orders])

# Promo and Support

@bp.route('/promo-code/validate', methods=['POST'])
def validate_promo_code():
    data = request.get_json()
    # Implement your logic to validate a promo code here
    return jsonify({"message": "Promo code validated"})

@bp.route('/support/chat', methods=['POST'])
def start_support_chat():
    data = request.get_json()
    # Implement your logic to start a support chat here
    return jsonify({"message": "Support chat started"})

@bp.route('/faq', methods=['GET'])
def faq():
    faqs = [
        {"question": "How do I reset my password?", "answer": "You can reset your password by going to the password reset page and following the instructions."},
        {"question": "How do I contact support?", "answer": "You can contact support via the contact page or email us at support@example.com."}
    ]
    return jsonify(faqs)
