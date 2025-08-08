from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from app.services import order_service as order_svc
from app.utils import get_dashboard_for_role


def order_exists(f):
    """Verify an order exists before proceeding.

    Args:
        f: The route function to decorate

    Returns:
        function: Decorated route with order validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        order_id = kwargs.get("order_id")
        order = order_svc.get_order_by_id(order_id)

        if not order:
            flash("Order not found. Please check the order ID.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, order=order, **kwargs)

    return decorated_function


def order_from_customer(f):
    """Verify the order belongs to the current customer.

    Args:
        f: The route function to decorate

    Returns:
        function: Decorated route with ownership validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        order = kwargs.get("order")

        if not order or order.customer_id != current_user.id:
            flash("You don't have permission to access this order.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, **kwargs)

    return decorated_function


def order_for_restaurant(f):
    """Verify the order belongs to the current restaurant.

    Args:
        f: The route function to decorate

    Returns:
        function: Decorated route with restaurant validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        order = kwargs.get("order")
        restaurant = kwargs.get("restaurant")

        if not order or order.restaurant_id != restaurant.id:
            flash("This order doesn't belong to your restaurant.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, **kwargs)

    return decorated_function
