from datetime import datetime as dt

from app.extensions import db

from .auth_model import User
from .restaurant_model import MenuItem, Restaurant


class Cart(db.Model):
    """Represents a user's shopping cart.

    Attributes:
        id: Primary key
        user_id: Reference to owner user (1:1)
        restaurant_id: Reference to restaurant
        created_at: Cart creation timestamp
        updated_at: Last modification timestamp
        user: Relationship to User model
        restaurant: Relationship to Restaurant model
        items: List of cart items
    """

    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurants.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=dt.now)
    updated_at = db.Column(db.DateTime, default=dt.now, onupdate=dt.now)

    # Relationships
    user = db.relationship("User", back_populates="cart", uselist=False)
    restaurant = db.relationship("Restaurant", back_populates="carts")
    items = db.relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItem(db.Model):
    """Represents an item in a shopping cart.

    Attributes:
        id: Primary key
        cart_id: Reference to parent cart
        menu_item_id: Reference to menu item
        quantity: Item quantity (default 1)
        cart: Relationship to Cart model
        menu_item: Relationship to MenuItem model
    """

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    # Relationships
    cart = db.relationship("Cart", back_populates="items")
    menu_item = db.relationship("MenuItem")
