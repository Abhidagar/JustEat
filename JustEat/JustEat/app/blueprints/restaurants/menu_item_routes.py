from flask import flash, redirect, render_template, url_for

from app.decorators import item_exists, owns_item, owns_restaurant, restaurant_exists
from app.services import menu_item_service as menu_item_svc
from app.services import restaurant_service as restaurant_svc

from . import restaurant_bp
from .forms import ItemForm


@restaurant_bp.route("/<string:slug>/menu", methods=["GET", "POST"])
@restaurant_exists
@owns_restaurant
def view_menu(slug, restaurant):
    """Display restaurant menu with popular items highlighted.

    Args:
        slug: Restaurant URL identifier
        restaurant: Restaurant object from decorator
    """
    restaurant = restaurant or restaurant_svc.get_restaurant_by_slug(slug)
    popular_item_ids = menu_item_svc.get_popular_item_ids(restaurant)

    return render_template(
        "restaurants/menu_items.html",
        restaurant=restaurant,
        popular_item_ids=popular_item_ids,
        page="menu",
    )


@restaurant_bp.route("/<string:slug>/menu/<int:item_id>/edit", methods=["GET", "POST"])
@restaurant_exists
@owns_restaurant
@item_exists
@owns_item
def edit_menu_item(slug, item_id, restaurant, item):
    """Edit existing menu item details.

    Args:
        slug: Restaurant URL identifier
        item_id: ID of item being edited
        restaurant: Restaurant object from decorator
        item: MenuItem object from decorator
    """
    restaurant = restaurant or restaurant_svc.get_restaurant_by_slug(slug)
    item = item or restaurant_svc.get_item_by_id(item_id)

    # Get dropdown options
    all_cuisines = restaurant_svc.get_all_cuisines()
    all_categories = restaurant_svc.get_all_categories()

    # Initialize form with current values
    form = ItemForm(obj=item)
    form.cuisine_id.choices = [(c.id, c.name) for c in all_cuisines]
    form.category_id.choices = [(c.id, c.name) for c in all_categories]

    if form.validate_on_submit():
        updated = menu_item_svc.update_menu_item(
            item_id=item_id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            cuisine_id=form.cuisine_id.data,
            category_id=form.category_id.data,
            is_non_veg=form.is_non_veg.data,
        )

        if updated:
            flash("Item updated successfully", "success")
            return redirect(url_for("restaurant.view_menu", slug=slug))
        flash("Failed to update item", "danger")

    return render_template(
        "restaurants/edit_menu_item.html",
        restaurant=restaurant,
        form=form,
        page="menu",
    )


@restaurant_bp.route("/<string:slug>/menu/add", methods=["GET", "POST"])
@restaurant_exists
@owns_restaurant
def add_menu_item(slug, restaurant):
    """Add new item to restaurant menu.

    Args:
        slug: Restaurant URL identifier
        restaurant: Restaurant object from decorator
    """
    restaurant = restaurant or restaurant_svc.get_restaurant_by_slug(slug)

    # Get dropdown options
    all_cuisines = restaurant_svc.get_all_cuisines()
    all_categories = restaurant_svc.get_all_categories()

    form = ItemForm()
    form.cuisine_id.choices = [(c.id, c.name) for c in all_cuisines]
    form.category_id.choices = [(c.id, c.name) for c in all_categories]

    if form.validate_on_submit():
        menu_item = menu_item_svc.create_menu_item(
            restaurant_id=restaurant.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            cuisine_id=form.cuisine_id.data,
            category_id=form.category_id.data,
        )

        if menu_item:
            flash("Item added successfully", "success")
            return redirect(url_for("restaurant.view_menu", slug=slug))
        flash("Failed to add item", "danger")

    return render_template(
        "restaurants/add_menu_item.html", restaurant=restaurant, form=form, page="menu"
    )


@restaurant_bp.route("/<string:slug>/menu/<int:item_id>/delete", methods=["POST"])
@restaurant_exists
@owns_restaurant
@item_exists
@owns_item
def delete_menu_item(slug, item_id, **kwargs):
    """Delete menu item from restaurant.

    Args:
        slug: Restaurant URL identifier
        item_id: ID of item to delete
    """
    success = menu_item_svc.delete_menu_item(item_id)

    if success:
        flash("Item deleted successfully", "success")
    else:
        flash("Failed to delete item", "danger")

    return redirect(url_for("restaurant.view_menu", slug=slug))


@restaurant_bp.route(
    "/<string:slug>/menu/<int:item_id>/<int:special>", methods=["POST"]
)
@restaurant_exists
@owns_restaurant
@item_exists
@owns_item
def update_special_status(slug, special, item, **kwargs):
    """Toggle special status for menu item.

    Args:
        slug: Restaurant URL identifier
        special: New special status (0/1)
        item: MenuItem object from decorator
    """
    menu_item_svc.update_item_special_status(item, special)
    return redirect(url_for("restaurant.view_menu", slug=slug))


@restaurant_bp.route(
    "/<string:slug>/menu/<int:item_id>/active/<int:active>", methods=["POST"]
)
@restaurant_exists
@owns_restaurant
@item_exists
@owns_item
def update_active_status(slug, active, item, **kwargs):
    """Toggle active/availability status for menu item.

    Args:
        slug: Restaurant URL identifier
        active: New active status (0/1)
        item: MenuItem object from decorator
    """
    menu_item_svc.update_item_active_status(item, active)
    return redirect(url_for("restaurant.view_menu", slug=slug))
