from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from app.services import cart_service as cs


def validate_cart_before_order(f):
    """Decorator to validate cart contents before order processing.
    
    Ensures:
    - Cart exists and is not empty
    - All items in cart are currently active
    
    Returns:
        function: Original route function if valid, otherwise redirect with flash message
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cart = cs.get_user_cart(current_user)

        # Validate cart existence and contents
        if not cart or not cart.items:
            flash("Your cart is empty. Please add items before ordering.", "warning")
            return redirect(url_for("customer.home"))

        # Check item availability
        if not all(item.menu_item.is_active for item in cart.items):
            unavailable_items = [
                item.menu_item.name 
                for item in cart.items 
                if not item.menu_item.is_active
            ]
            flash(
                f"These items are no longer available: {', '.join(unavailable_items)}", 
                "danger"
            )
            return redirect(url_for("customer.home"))

        return f(*args, cart=cart, **kwargs)

    return decorated_function