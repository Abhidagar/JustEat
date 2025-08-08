from datetime import datetime as dt
from enum import Enum

from app.extensions import db


class OrderStatus(Enum):
    """Defines possible states of an order."""

    PENDING = "pending"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


class Order(db.Model):
    """Represents a customer's food order.

    Attributes:
        id: Primary key
        customer_id: Reference to ordering user
        restaurant_id: Reference to restaurant
        created_at: Order creation timestamp
        updated_at: Last status update timestamp
        total: Order total amount
        status: Current order state
        user: Relationship to User model
        restaurant: Relationship to Restaurant model
        items: List of ordered items
        restaurant_rating: Associated rating (if exists)
    """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurants.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, default=dt.now, onupdate=dt.now)

    total = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)

    # Relationships
    user = db.relationship("User", back_populates="orders")
    restaurant = db.relationship("Restaurant", back_populates="orders")
    items = db.relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    restaurant_rating = db.relationship(
        "RestaurantRating", backref="order", uselist=False
    )


class OrderItem(db.Model):
    """Represents an individual item within an order.

    Attributes:
        id: Primary key
        order_id: Parent order reference
        name: Item name at time of order
        menu_item_id: Original menu item reference
        quantity: Ordered quantity
        price_at_order: Price snapshot when ordered
        created_at: When item was added to order
    """

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=dt.now)

    order = db.relationship("Order", back_populates="items")
