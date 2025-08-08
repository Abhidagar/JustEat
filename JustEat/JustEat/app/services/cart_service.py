from typing import Optional

from flask import current_app

from app.extensions import db
from app.models import Cart, CartItem, User


def get_user_cart(user: User) -> Optional[Cart]:
    """Retrieve a user's active cart."""
    return Cart.query.filter_by(user_id=user.id).first()

# Only handles shopping cart operations (Single Responsibility Principle)
def get_cart_summary(user: User) -> dict:
    """Generate summary of cart contents and total."""
    cart = get_user_cart(user)
    item_qty = {}
    total = 0
    
    if cart:
        for item in cart.items:
            item_qty[item.menu_item.id] = item.quantity
            total += item.menu_item.price * item.quantity
            
    return {"item_qty": item_qty, "total": total}


def create_user_cart(user: User, restaurant_id: int) -> Cart:
    """Initialize a new cart for user."""
    cart = Cart(user_id=user.id, restaurant_id=restaurant_id)
    db.session.add(cart)
    db.session.commit()
    current_app.logger.info(f"Created new cart {cart.id} for user {user.id}")
    return cart


def add_to_cart(user: User, item_id: int, restaurant_id: int) -> Optional[str]:
    """Add item to user's cart with validation."""
    cart = get_user_cart(user)

    if not cart:
        cart = create_user_cart(user, restaurant_id)

    if cart.restaurant_id != restaurant_id:
        current_app.logger.warning(
            f"Cart restaurant mismatch for user {user.id}. "
            f"Expected {restaurant_id}, found {cart.restaurant_id}"
        )
        return "Please checkout or clear cart"

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id, 
        menu_item_id=item_id
    ).first()

    if cart_item and not cart_item.menu_item.is_active:
        current_app.logger.warning(
            f"Attempt to add inactive item {item_id} to cart {cart.id}"
        )
        return "Cannot add inactive item"

    try:
        if cart_item:
            cart_item.quantity += 1
            current_app.logger.debug(
                f"Incremented item {item_id} in cart {cart.id}"
            )
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                menu_item_id=item_id,
                quantity=1
            )
            db.session.add(cart_item)
            current_app.logger.info(
                f"Added new item {item_id} to cart {cart.id}"
            )
        
        db.session.commit()
        return None
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to update cart {cart.id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return "Error updating cart"


def remove_from_cart(user: User, item_id: int) -> Optional[Cart]:
    """Remove item from cart or decrement quantity."""
    cart = get_user_cart(user)

    if not cart:
        current_app.logger.debug(f"No cart found for user {user.id}")
        return None

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        menu_item_id=item_id
    ).first()

    if not cart_item:
        current_app.logger.debug(
            f"Item {item_id} not found in cart {cart.id}"
        )
        return None

    try:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            current_app.logger.debug(
                f"Decremented item {item_id} in cart {cart.id}"
            )
        else:
            db.session.delete(cart_item)
            current_app.logger.info(
                f"Removed item {item_id} from cart {cart.id}"
            )
            if not cart.items:
                db.session.delete(cart)
                current_app.logger.info(f"Deleted empty cart {cart.id}")

        db.session.commit()
        return cart
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to modify cart {cart.id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return None