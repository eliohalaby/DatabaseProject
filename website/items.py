from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Items, Ingredient, CustomIngredients, Custom_OrderLine, OrderLine

items_bp = Blueprint('item', __name__) #__name__ indicates where the blueprint lives 

@items_bp.route('/', methods=['GET', 'POST'])
def items():
    new_item = []
    if request.method == 'GET': 
        new_item = Items.query.all() 

    return render_template('items_view.html', new_item=new_item) 


@items_bp.route('/customize/<int:item_id>', methods=['GET', 'POST'])
def customize(item_id):
    item = Items.query.get_or_404(item_id)  
    ingredients = item.ingredients 
    custom_ingredients = CustomIngredients.query.filter_by(item_id=item_id).all() 
    added_ingredients = [c.ingredient for c in custom_ingredients] 

    if request.method == 'POST':
        selected_ingredient_ids = list(map(int, request.form.getlist("ingredients")))
        quantity = int(request.form.get('quantity', 1))

        order_line = OrderLine(
            # orderId=current_order_id, 
            quantity=quantity
        )
        db.session.add(order_line)
        db.session.flush()  # ensures orderLine_id is set

        for ing_id in selected_ingredient_ids:
            order_line_ingredient = Custom_OrderLine(
                orderLine_id=order_line.orderLine_id,
                added_ingredients=ing_id
            )
            db.session.add(order_line_ingredient)

        db.session.commit()
        return redirect(url_for("item.items"))

    return render_template(
        'customize_item.html',
        item=item,
        ingredients=ingredients,
        added_ingredients=added_ingredients
    )
