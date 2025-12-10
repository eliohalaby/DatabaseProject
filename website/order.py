from flask import Blueprint, request, render_template 

order_bp = Blueprint('order', __name__) 

@order_bp.route('/') 
def order(): 
    return '<h1>Hello</h1>' 