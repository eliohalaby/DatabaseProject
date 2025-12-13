import os
from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)

    # Use environment variables for security
    app.secret_key = os.getenv("SECRET_KEY", "DBCOURSEPROJECT") 
    username = os.getenv('DB_USER', 'dbproject')
    password = os.getenv('DB_PASS', 'ElioFarahJean')
    host = os.getenv('DB_HOST', 'localhost')
    database = os.getenv('DB_NAME', 'mydatabase')

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://dbproject:ElioFarahJean@localhost:3306/mydatabase"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import models and blueprints
    from .models import Items, Ingredient, CustomIngredients
    from .auth import auth
    from .items import items_bp
    from .admin import admin_bp 
    from .user_home_page import userhp_bp 
    from .order import order_bp 

    # Create tables safely
    try:
        createdatabase(app)
    except Exception as e:
        print(f"Error creating database tables: {e}")
    app.register_blueprint(auth, url_prefix='/login')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(admin_bp,url_prefix='/admin') 
    app.register_blueprint(userhp_bp, url_prefix='/') 
    app.register_blueprint(order_bp, url_prefix = '/order')

    @app.route('/')
    def index():
        return redirect(url_for("auth.login")) 
    return app

def createdatabase(app):
    with app.app_context():
        db.create_all()
        print("Database tables created")