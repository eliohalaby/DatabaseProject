from . import db 
from flask_login import UserMixin #instead of writing my own authentication system I can use the one provided by flask login 
from sqlalchemy.sql import func 
import enum 

class PaymentMethod(enum.Enum): 
    cash = 'Cash' 
    card = 'Card' 

class PaymentStatus(enum.Enum): 
    start = 'start' 
    pending = 'pending' 
    complete = 'completed'


class Customer(db.Model, UserMixin): 
    __tablename__ = 'customers' 
    user_id = db.Column(db.Integer, primary_key = True) 
    first_name = db.Column(db.String(150)) 
    last_name = db.Column(db.String(150)) 
    email = db.Column(db.String(150), unique = True) 
    phone_number = db.Column(db.String(8), unique = True) 


class Items(db.Model): 
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True) 
    itemName = db.Column(db.String(150), nullable=False)  
    description = db.Column(db.String(150)) 
    price = db.Column(db.Float) 
    image = db.Column(db.String(255)) 
    #Adding a many2many relationship with ingredients. 
    ingredients = db.relationship(
        'Ingredient',
        secondary='item_ingredients',
        backref='items'
    )


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100))
    extra_price = db.Column(db.Float) 

class ItemIngredient(db.Model):
    __tablename__ = 'item_ingredients'
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True) 

class CustomIngredients(db.Model): 
    __tablename__ = 'custom_ingredients' 
    added_ingredients = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key = True) 
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), primary_key = True) 
    ingredient = db.relationship("Ingredient", backref="custom_added") 

class Custom_OrderLine(db.Model): 
    __tablename__ =  "custom_orderline" 
    added_ingredients = db.Column(db.Integer, db.ForeignKey('custom_ingredients.added_ingredients'), primary_key = True) 
    orderLine_id = db.Column(db.Integer, db.ForeignKey('orderline.orderLine_id'), primary_key = True)


class Category(db.Model): 
    __tablename__ = 'category'
    categoryId = db.Column(db.Integer, primary_key =True) 
    category_type = db.Column(db.String(150), nullable=False) 
    itemId = db.Column(db.Integer, db.ForeignKey('items.item_id')) 

class Order(db.Model): 
    __tablename__ = 'order' 
    order_id = db.Column(db.Integer, primary_key = True) 
    orderStatus = db.Column(db.String(150)) 
    totalAmount = db.Column(db.Float) 
    dateTimeOrdered = db.Column(db.DateTime(timezone = True), default = func.now()) 
    dateTimeReviewed = db.Column(db.DateTime(timezone = True), default = func.now()) 
    userId = db.Column(db.Integer, db.ForeignKey('customers.user_id')) 

class OrderLine(db.Model): 
    __tablename__ = 'orderline' 
    orderLine_id = db.Column(db.Integer, primary_key = True) 
    quantity = db.Column(db.Integer, default=1) 
    orderId = db.Column(db.Integer, db.ForeignKey('order.order_id')) 


class Payment(db.Model): 
    __tablename__ = 'payment' 
    payment_id = db.Column(db.Integer, primary_key=True) 
    payment_method = db.Column(db.Enum(PaymentMethod), default = PaymentMethod.cash) 
    payment_date = db.Column(db.DateTime(timezone=True), default = func.now()) 
    payment_status = db.Column(db.Enum(PaymentMethod), default = PaymentStatus.pending) 
    discount = db.Column(db.Integer) 
    totalAmount = db.Column(db.Integer) 
    cardId = db.Column(db.Integer, db.ForeignKey('loyaltycard.card_id'))  
    order = db.Column(db.Integer, db.ForeignKey('order.order_id')) 
    userid = db.Column(db.Integer, db.ForeignKey('customers.user_id')) 



class LoyaltyCard(db.Model): 
    __tablename__ = 'loyaltycard' 
    card_id = db.Column(db.Integer, primary_key=True) 
    loyalty_amount = db.Column(db.Integer, nullable = False) 
    promocode = db.Column(db.Integer) 
    userid = db.Column(db.Integer, db.ForeignKey('customers.user_id')) 