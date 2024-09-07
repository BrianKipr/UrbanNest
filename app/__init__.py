# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager

# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()

# def create_app():
#     app = Flask(__name__)
    
#     # Load configuration from config.py
#     app.config.from_object('app.config.Config')
    
#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
    
#     # Register blueprints
#     from app.routes import bp as routes_bp
#     app.register_blueprint(routes_bp, url_prefix='/api')
    
#     return app





from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Update with your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Import models here to ensure they are registered
        from app.models import User, Product, Category, Order, Review, PromoCode, SupportChat, ProductQuestion
        
        # Create database tables
        db.create_all()

    return app
