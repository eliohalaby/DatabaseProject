from flask import Blueprint, request, render_template, redirect, url_for

userhp_bp = Blueprint('user_hp', __name__) 

@userhp_bp.route('/<int:user_id>', methods = ["GET", "POST"]) 
def homepage(user_id): 
    if request.method == "POST": 
        return redirect(url_for('item.items')) 
    return render_template('home_page.html', user_id = user_id) 