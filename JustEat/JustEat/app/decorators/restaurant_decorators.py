from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from app.services.menu_item_service import get_item_by_id
from app.services.restaurant_service import get_restaurant_by_slug
from app.utils import get_dashboard_for_role

# Only checks restaurant existence(Single Responsibility Principle)
def restaurant_exists(f):
    """Verify restaurant exists before processing route.

    Args:
        f: Route function to decorate

    Returns:
        Decorated function with restaurant validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        slug = kwargs.get("slug")
        restaurant = get_restaurant_by_slug(slug)

        if not restaurant:
            flash("Restaurant not found. Please check the URL.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, restaurant=restaurant, **kwargs)

    return decorated_function


def owns_restaurant(f):
    """Verify current user owns the restaurant.

    Args:
        f: Route function to decorate

    Returns:
        Decorated function with ownership validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        restaurant = kwargs.get("restaurant")

        if not restaurant or restaurant.owner_id != current_user.id:
            flash("Restaurant not found. Please check the URL.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, **kwargs)

    return decorated_function


def item_exists(f):
    """Verify menu item exists before processing route.

    Args:
        f: Route function to decorate

    Returns:
        Decorated function with item validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        item_id = kwargs.get("item_id")
        item = get_item_by_id(item_id)

        if not item:
            flash("Menu item not found. It may have been removed.", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, item=item, **kwargs)

    return decorated_function


def owns_item(f):
    """Verify restaurant owns the menu item.

    Args:
        f: Route function to decorate

    Returns:
        Decorated function with item ownership validation
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        restaurant = kwargs.get("restaurant")
        item = kwargs.get("item")

        if not item or item.restaurant_id != restaurant.id:
            flash("Item not found", "danger")
            return redirect(url_for(get_dashboard_for_role(current_user.role)))

        return f(*args, **kwargs)

    return decorated_function
