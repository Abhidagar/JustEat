from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.decorators.restaurant_decorators import owns_restaurant, restaurant_exists
from app.services import restaurant_service as restaurant_svc
from app.services import order_service as order_svc

from . import restaurant_bp
from .forms import CuisineForm, RestaurantForm


@restaurant_bp.route("/dashboard")
def dashboard():
    """Display all restaurants owned by the current user."""
    restaurants = restaurant_svc.get_user_restaurants(current_user)
    return render_template(
        "restaurants/dashboard.html",
        restaurants=restaurants,
        dashboard=True,
        page="dashboard",
    )


@restaurant_bp.route("/new", methods=["GET", "POST"])
def create():
    """Handle new restaurant creation."""
    form = RestaurantForm()

    if form.validate_on_submit():
        restaurant = restaurant_svc.create_new_restaurant(
            owner_id=current_user.id,
            name=form.name.data,
            location=form.location.data,
            opening_time=form.opening_time.data,
            closing_time=form.closing_time.data,
        )

        if restaurant:
            flash("Restaurant created successfully", "success")
            return redirect(url_for("restaurant.cuisines", slug=restaurant.slug))
        flash("Failed to create restaurant", "danger")

    return render_template(
        "restaurants/add_restaurant.html",
        form=form,
        dashboard=True,
        page="create",
    )


@restaurant_bp.route("/<string:slug>")
@restaurant_exists
@owns_restaurant
def home(slug, restaurant):
    """Redirect to restaurant orders page (dashboard removed)."""
    return redirect(url_for("restaurant.view_orders", slug=slug))


@restaurant_bp.route("/<string:slug>/cuisines", methods=["GET", "POST"])
@restaurant_exists
@owns_restaurant
def cuisines(slug, restaurant):
    """Manage restaurant cuisine types."""
    form = CuisineForm()
    all_cuisines = restaurant_svc.get_all_cuisines()
    form.cuisines.choices = [(c.id, c.name, c.image) for c in all_cuisines]

    if form.validate_on_submit():
        if restaurant_svc.update_restaurant_cuisines(restaurant, form.cuisines.data):
            flash("Cuisines updated successfully", "success")
            return redirect(url_for("restaurant.cuisines", slug=restaurant.slug))
        flash("Failed to update cuisines", "danger")

    form.cuisines.data = [c.id for c in restaurant.cuisines]

    return render_template(
        "restaurants/cuisines.html", form=form, restaurant=restaurant, page="cuisine"
    )


@restaurant_bp.route("/<string:slug>/status/<int:status>", methods=["POST"])
@restaurant_exists
@owns_restaurant
def update_status(slug, status, restaurant):
    """Toggle restaurant active/inactive status."""
    if restaurant_svc.update_restaurant_status(restaurant, status):
        status_text = "activated" if status else "deactivated"
        flash(f"Restaurant {status_text} successfully", "success")
    else:
        flash("Failed to update status", "danger")

    return redirect(url_for("restaurant.edit_details", slug=restaurant.slug))


@restaurant_bp.route("/<string:slug>/delete", methods=["POST"])
@restaurant_exists
@owns_restaurant
def delete(slug, restaurant):
    """Delete restaurant permanently."""
    if restaurant_svc.delete_restaurant(restaurant):
        flash("Restaurant deleted successfully", "success")
    else:
        flash("Failed to delete restaurant", "danger")

    return redirect(url_for("restaurant.dashboard"))


@restaurant_bp.route("/<string:slug>/settings", methods=["GET", "POST"])
@restaurant_exists
@owns_restaurant
def edit_details(slug, restaurant):
    """Update restaurant details."""
    form = RestaurantForm(obj=restaurant)

    if form.validate_on_submit():
        if restaurant_svc.update_restaurant_details(
            slug=restaurant.slug,
            name=form.name.data,
            location=form.location.data,
            opening_time=form.opening_time.data,
            closing_time=form.closing_time.data,
        ):
            flash("Restaurant details updated successfully", "success")
            return redirect(url_for("restaurant.view_menu", slug=restaurant.slug))
        flash("Failed to update details", "danger")

    return render_template(
        "restaurants/edit_details.html",
        restaurant=restaurant,
        page="settings",
        form=form,
    )


@restaurant_bp.route("/<string:slug>/reviews")
@restaurant_exists
@owns_restaurant
def view_reviews(restaurant, **kwargs):
    """Display all restaurant reviews."""
    reviews = order_svc.get_reviews(restaurant.id)
    return render_template(
        "restaurants/reviews.html",
        restaurant=restaurant,
        reviews=reviews,
        page="reviews",
    )
