from flask import flash, redirect, render_template, url_for

from app.decorators import (
    order_exists,
    owns_restaurant,
    restaurant_exists,
    order_for_restaurant,
)
from app.services import order_service as order_svc
from app.services import restaurant_service as restaurant_svc

from . import restaurant_bp


@restaurant_bp.route("/<string:slug>/orders", methods=["GET"])
@restaurant_exists
@owns_restaurant
def view_orders(slug, restaurant):
    """Display all orders for a restaurant.

    Args:
        slug: Restaurant URL identifier
        restaurant: Restaurant object from decorator

    Returns:
        Rendered template with orders list
    """
    orders = order_svc.get_restaurant_orders(restaurant.id)

    return render_template(
        "restaurants/view_orders.html",
        restaurant=restaurant,
        orders=orders,
        page="orders",
    )


@restaurant_bp.route(
    "/<string:slug>/orders/<int:order_id>/<string:status>", methods=["POST"]
)
@restaurant_exists
@owns_restaurant
@order_exists
@order_for_restaurant
def update_order_status(order_id, status, order, **kwargs):
    """Update order status (e.g., preparing, ready, completed).

    Args:
        order_id: ID of order to update
        status: New status to set
        order: Order object from decorator
        **kwargs: Additional route parameters

    Returns:
        Redirect back to orders list with flash message
    """
    slug = kwargs.get("slug")

    if not order_svc.update_order_status(order, status):
        flash("Failed to update order status", "danger")
    else:
        flash("Order status updated successfully", "success")

    return redirect(url_for("restaurant.view_orders", slug=slug))
