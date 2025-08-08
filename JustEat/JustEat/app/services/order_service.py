from decimal import Decimal
from typing import Optional

from flask import current_app

from app.extensions import db
from app.models import MenuItemRating, Order, OrderItem, OrderStatus, RestaurantRating
from app.services import menu_item_service as menu_item_svc
from app.services import restaurant_service as restaurant_svc


def get_order_status(status: str) -> Optional[OrderStatus]:
    """Validate and convert string to OrderStatus enum."""
    try:
        return OrderStatus(status) if status else None
    except ValueError:
        current_app.logger.warning(f"Invalid order status: {status}")
        return None


def get_orders(user, status: Optional[str] = None) -> list[Order]:
    """Retrieve user's orders with optional status filter."""
    try:
        query = Order.query.filter_by(customer_id=user.id)
        if status_enum := get_order_status(status):
            query = query.filter_by(status=status_enum)
        return query.order_by(Order.created_at.desc()).all()
    except Exception as e:
        current_app.logger.error(f"Failed to fetch orders for user {user.id}: {str(e)}")
        return []


def place_order(user, cart) -> Optional[Order]:
    """Convert cart to completed order with transaction."""
    try:
        total = Decimal(0)
        order = Order(
            customer_id=user.id,
            restaurant_id=cart.restaurant_id,
            total=0,
            status=OrderStatus.PENDING,
        )
        db.session.add(order)
        db.session.flush()

        for item in cart.items:
            item_total = item.menu_item.price * item.quantity
            total += item_total

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item.menu_item.id,
                quantity=item.quantity,
                price_at_order=item.menu_item.price,
                name=item.menu_item.name,
            )
            db.session.add(order_item)

        order.total = total
        db.session.delete(cart)
        db.session.commit()

        current_app.logger.info(
            f"Order {order.id} placed for user {user.id}, total: {total}"
        )
        return order

    except Exception as e:
        current_app.logger.error(
            f"Failed to place order for user {user.id}: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return None


def get_restaurant_orders(restaurant_id: int) -> list[Order]:
    """Retrieve all orders for a restaurant."""
    try:
        return (
            Order.query.filter_by(restaurant_id=restaurant_id)
            .order_by(Order.created_at.desc())
            .all()
        )
    except Exception as e:
        current_app.logger.error(
            f"Failed to fetch orders for restaurant {restaurant_id}: {str(e)}"
        )
        return []


def get_order_by_id(order_id: int) -> Optional[Order]:
    """Retrieve single order by ID."""
    try:
        return Order.query.get(order_id)
    except Exception as e:
        current_app.logger.error(f"Failed to fetch order {order_id}: {str(e)}")
        return None


def update_order_status(order: Order, status: str) -> Optional[Order]:
    """Safely update order status with validation."""
    try:
        if order.status != OrderStatus.PENDING:
            current_app.logger.warning(
                f"Attempt to modify non-pending order {order.id} status"
            )
            return None

        status_enum = OrderStatus(status)
        order.status = status_enum
        db.session.commit()

        current_app.logger.info(
            f"Updated order {order.id} status to {status_enum.value}"
        )
        return order

    except ValueError as e:
        current_app.logger.error(
            f"Invalid status '{status}' for order {order.id}: {str(e)}"
        )
        db.session.rollback()
        return None
    except Exception as e:
        current_app.logger.error(
            f"Failed to update order {order.id} status: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return None


def add_ratings(
    user_id: int, order_id: int, item_ratings: list[dict], restaurant_rating: dict
) -> bool:
    """Add ratings for both restaurant and menu items."""
    try:
        # Add restaurant rating
        rest_rating = RestaurantRating(
            user_id=user_id,
            restaurant_id=restaurant_rating["restaurant_id"],
            order_id=order_id,
            rating=restaurant_rating["rating"],
            comment=restaurant_rating.get("comment", ""),
        )
        db.session.add(rest_rating)

        # Add menu item ratings
        for item in item_ratings:
            item_rating = MenuItemRating(
                user_id=user_id,
                menu_item_id=item["item_id"],
                rating=item["rating"],
            )
            db.session.add(item_rating)
            menu_item_svc.update_item_rating(item["item_id"], item["rating"])

        # Update restaurant aggregate rating
        restaurant_svc.update_restaurant_rating(
            restaurant_rating["restaurant_id"], restaurant_rating["rating"]
        )

        db.session.commit()
        current_app.logger.info(
            f"Added {len(item_ratings)} item ratings and "
            f"restaurant rating for order {order_id}"
        )
        return True

    except Exception as e:
        current_app.logger.error(
            f"Failed to add ratings for order {order_id}: {str(e)}", exc_info=True
        )
        db.session.rollback()
        return False


def get_reviews(restaurant_id: int) -> list[RestaurantRating]:
    """Retrieve reviews for a restaurant."""
    try:
        return (
            RestaurantRating.query.filter_by(restaurant_id=restaurant_id)
            .order_by(RestaurantRating.created_at.desc())
            .all()
        )
    except Exception as e:
        current_app.logger.error(
            f"Failed to fetch reviews for restaurant {restaurant_id}: {str(e)}"
        )
        return []
