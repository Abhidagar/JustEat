from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required

from app.decorators import (
    item_exists,
    order_exists,
    order_from_customer,
    restaurant_exists,
    validate_cart_before_order,
)
from app.services import (
    cart_service as cart_svc,
    favorite_service as favorite_svc,
    menu_item_service as menu_item_svc,
    order_service as order_svc,
    restaurant_service as restaurant_svc,
    search_service as search_svc,
)

from . import customer_bp
from .forms import FullReviewForm, ItemReviewForm


@customer_bp.route("/home")
def home():
    """Render customer homepage with restaurant listings and cuisine categories."""
    # Get filter parameters if any
    cuisine_ids = request.args.getlist("cuisine")
    restaurant_ids = request.args.getlist("restaurant") 
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)
    
    # Get filtered restaurants if filters are applied
    if cuisine_ids or restaurant_ids or price_min or price_max:
        restaurants, _ = search_svc.get_filtered_search_results(
            query=None,
            cuisine_ids=cuisine_ids,
            restaurant_ids=restaurant_ids,
            price_min=price_min,
            price_max=price_max
        )
    else:
        restaurants = restaurant_svc.get_all_restaurants()
    
    cuisines = [(c.id, c.name, c.image) for c in restaurant_svc.get_all_cuisines()]
    
    # Get all cuisines and restaurants for filter options
    all_cuisines = restaurant_svc.get_all_cuisines()
    all_restaurants = restaurant_svc.get_all_restaurants()

    # Cart data for header display
    cart_summary = cart_svc.get_cart_summary(current_user)
    cart = cart_svc.get_user_cart(current_user)
    
    # Get user's favorites for showing heart icons
    user_favorites = []
    if current_user.is_authenticated:
        user_favorites = [r.id for r in favorite_svc.get_user_favorites(current_user)]

    return render_template(
        "customer/home.html",
        restaurants=restaurants,
        cuisines=cuisines,
        all_cuisines=all_cuisines,
        all_restaurants=all_restaurants,
        cart=cart,
        cart_summary=cart_summary,
        user_favorites=user_favorites,
        page="home",
        # Pass current filter values back to template
        selected_cuisines=cuisine_ids,
        selected_restaurants=restaurant_ids,
        price_min=price_min,
        price_max=price_max,
    )


@customer_bp.route("/<string:slug>/menu")
@restaurant_exists
def restaurant_info(restaurant, **kwargs):
    """
    Display restaurant menu and information.

    Args:
        restaurant (Restaurant): Restaurant object from decorator
        **kwargs: Additional route parameters
    """
    cart_summary = cart_svc.get_cart_summary(current_user)
    cart = cart_svc.get_user_cart(current_user)

    # Get popular items to highlight
    popular_item_ids = menu_item_svc.get_popular_item_ids(restaurant)
    
    # Check if restaurant is favorited by current user
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = favorite_svc.is_favorited(current_user, restaurant.id)

    return render_template(
        "customer/restaurant.html",
        restaurant=restaurant,
        cart=cart,
        cart_summary=cart_summary,
        popular_item_ids=popular_item_ids,
        is_favorited=is_favorited,
        homepage=True,
    )


@customer_bp.route("/<string:slug>/reviews")
@restaurant_exists
def restaurant_reviews(restaurant, **kwargs):
    """
    Display reviews for a specific restaurant.

    Args:
        restaurant (Restaurant): Restaurant object from decorator
        **kwargs: Additional route parameters
    """
    cart_summary = cart_svc.get_cart_summary(current_user)
    cart = cart_svc.get_user_cart(current_user)

    reviews = order_svc.get_reviews(restaurant.id)
    
    # Check if restaurant is favorited by current user
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = favorite_svc.is_favorited(current_user, restaurant.id)

    return render_template(
        "customer/restaurant_reviews.html",
        restaurant=restaurant,
        reviews=reviews,
        cart=cart,
        cart_summary=cart_summary,
        is_favorited=is_favorited,
    )


@customer_bp.route("/<string:slug>/cart/add/<int:item_id>", methods=["POST"])
@restaurant_exists
@item_exists
def add_to_cart(slug, restaurant, item, **kwargs):
    """Add menu item to customer's cart.

    Args:
        slug (str): Restaurant slug
        restaurant (Restaurant): Restaurant object from decorator
        item (MenuItem): Menu item object from decorator
        **kwargs: Additional route parameters
    """
    message = cart_svc.add_to_cart(current_user, item.id, restaurant.id)

    if message:
        flash(message, "danger")

    return redirect(url_for("customer.restaurant_info", slug=slug))


@customer_bp.route("/<string:slug>/cart/remove/<int:item_id>", methods=["POST"])
@restaurant_exists
@item_exists
def remove_from_cart(slug, item, **kwargs):
    """
    Remove item from customer's cart.

    Args:
        slug (str): Restaurant slug
        item (MenuItem): Menu item object from decorator
        **kwargs: Additional route parameters
    """
    cart = cart_svc.remove_from_cart(current_user, item.id)

    if not cart:
        flash("An error occurred", "danger")

    return redirect(url_for("customer.restaurant_info", slug=slug))


@customer_bp.route("/cart/place-order", methods=["POST"])
@validate_cart_before_order
def place_order(cart):
    """
    Process order placement from cart contents.

    Args:
        cart (Cart): Validated cart object from decorator
    """
    order_svc.place_order(current_user, cart)
    flash("Order placed successfully!", "success")
    return redirect(url_for("customer.home"))


@customer_bp.route("/orders")
def view_orders():
    """Display customer's order history with optional status filtering."""
    cart = cart_svc.get_user_cart(current_user)
    cart_summary = cart_svc.get_cart_summary(current_user)

    status = request.args.get("status")
    orders = order_svc.get_orders(current_user, status)

    return render_template(
        "customer/view_orders.html",
        orders=orders,
        cart=cart,
        cart_summary=cart_summary,
    )


@customer_bp.route("/search")
def search():
    """Handle restaurant and menu item searches."""
    query = request.args.get("q")
    
    if not query:
        return redirect(url_for("customer.home"))

    cart_summary = cart_svc.get_cart_summary(current_user)
    cart = cart_svc.get_user_cart(current_user)

    # Get search results
    restaurants, menu_items = search_svc.get_filtered_search_results(query=query)
    
    # Get popular item IDs for search results
    popular_item_ids = set()
    if menu_items:
        popular_item_ids = menu_item_svc.get_popular_item_ids_for_search(menu_items)
    
    # Get user's favorites for showing heart icons
    user_favorites = []
    if current_user.is_authenticated:
        user_favorites = [r.id for r in favorite_svc.get_user_favorites(current_user)]

    return render_template(
        "customer/search_results.html",
        cart=cart,
        cart_summary=cart_summary,
        restaurants=restaurants,
        menu_items=menu_items,
        popular_item_ids=popular_item_ids,
        user_favorites=user_favorites,
        query=query
    )


@customer_bp.route("/orders/<int:order_id>/review", methods=["GET", "POST"])
@order_exists
@order_from_customer
def add_review(order_id, order, **kwargs):
    """
    Handle order review submission.

    Args:
        order_id (int): ID of order being reviewed
        order (Order): Order object from decorator
        **kwargs: Additional route parameters
    """
    if order.restaurant_rating:
        flash("You have already reviewed this order", "warning")
        return redirect(url_for("customer.view_orders"))

    form = FullReviewForm()
    cart = cart_svc.get_user_cart(current_user)
    cart_summary = cart_svc.get_cart_summary(current_user)

    # Initialize form with order items
    if request.method == "GET":
        form.item_reviews.entries.clear()
        for item in order.items:
            item_form = ItemReviewForm()
            item_form.item_id.data = item.menu_item_id
            item_form.rating.data = 5  # Default to 5 stars
            item_form.process()
            form.item_reviews.append_entry(item_form)

    # Process form submission
    if form.validate_on_submit():
        item_ratings = [
            {
                "item_id": entry.item_id.data,
                "rating": entry.rating.data,
            }
            for entry in form.item_reviews.entries
        ]

        restaurant_rating = {
            "restaurant_id": order.restaurant_id,
            "rating": form.restaurant_review.rating.data,
            "comment": form.restaurant_review.review.data,
        }

        success = order_svc.add_ratings(
            user_id=current_user.id,
            order_id=order_id,
            item_ratings=item_ratings,
            restaurant_rating=restaurant_rating,
        )

        if success:
            flash("Thank you for your review!", "success")
            return redirect(url_for("customer.view_orders"))
        else:
            flash("An error occurred", "error")

    return render_template(
        "customer/rate_order.html",
        form=form,
        order=order,
        cart=cart,
        cart_summary=cart_summary,
    )


@customer_bp.route("/favorites")
@login_required
def view_favorites():
    """Display user's favorite restaurants and menu items."""
    cart = cart_svc.get_user_cart(current_user)
    cart_summary = cart_svc.get_cart_summary(current_user)
    
    restaurant_favorites = favorite_svc.get_favorites_with_info(current_user)
    menu_item_favorites = favorite_svc.get_favorite_menu_items_with_info(current_user)
    
    return render_template(
        "customer/favorites.html",
        restaurant_favorites=restaurant_favorites,
        menu_item_favorites=menu_item_favorites,
        cart=cart,
        cart_summary=cart_summary,
    )


@customer_bp.route("/restaurant/<int:restaurant_id>/toggle-favorite", methods=["POST"])
@login_required
def toggle_favorite(restaurant_id):
    """Toggle a restaurant as favorite."""
    is_favorited = favorite_svc.toggle_favorite(current_user, restaurant_id)
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({
            'success': True,
            'is_favorited': is_favorited
        })
    else:
        if is_favorited:
            flash("Restaurant added to favorites!", "success")
        else:
            flash("Restaurant removed from favorites!", "info")
        
        # Redirect back to the previous page
        return redirect(request.referrer or url_for('customer.home'))



