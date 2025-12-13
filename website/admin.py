from flask import Blueprint, request, render_template, redirect, url_for 
from .models import db, Items, Customer
admin_bp = Blueprint('admin', __name__) 

@admin_bp.route('/add_item', methods=['GET', 'POST']) 
def admin_add_item(): 
    if request.method == "POST": 
        item_name = request.form['item_name'] 
        description = request.form['description'] 
        price = request.form['price'] 
        new_item = Items(
            itemName=item_name, 
            description=description, 
            price=price
        ) 
        db.session.add(new_item) 
        db.session.commit() 
        return redirect(url_for('admin.admin_add_item'))
    return render_template('admin_add_item.html') 

@admin_bp.route('/list') 
def list_items(): 
    items = Items.query.all() 
    return render_template('list_items.html', items=items) 

@admin_bp.route('/create_user', methods = ['POST', 'GET']) 
def create_user(): 
    if request.method == 'POST': 
        first_name = request.form['username'] 
        last_name = request.form['userlastname'] 
        email = request.form['email'] 
        phone = request.form['phone'] 
        password = request.form['password']
        new_user = Customer(first_name = first_name, 
                            last_name = last_name, 
                            email = email, 
                            phone_number = phone
                            , password_hash = password
                            ) 
        db.session.add(new_user) 
        db.session.commit() 
    return render_template('create_user.html') 