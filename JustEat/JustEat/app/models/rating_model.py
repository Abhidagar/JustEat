from app.extensions import db
from datetime import datetime as dt
from .auth_model import User


class RestaurantRating(db.Model):
    """Stores customer ratings and reviews for restaurants.

    Attributes:
        id: Primary key
        user_id: Reference to reviewing user
        restaurant_id: Reference to rated restaurant
        rating: Numeric rating (1-5)
        comment: Optional review text
        order_id: Reference to associated order
        created_at: When review was submitted
        user: Relationship to User model
        restaurant: Relationship to Restaurant model
    """

    __tablename__ = "restaurant_ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurants.id"), nullable=False
    )
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=dt.now)

    # Relationships
    user = db.relationship("User", backref="restaurant_ratings")
    restaurant = db.relationship("Restaurant", back_populates="ratings")


class MenuItemRating(db.Model):
    """Stores customer ratings for individual menu items.

    Attributes:
        id: Primary key
        user_id: Reference to reviewing user
        menu_item_id: Reference to rated item
        rating: Numeric rating (typically 1-5)
        user: Relationship to User model
        menu_item: Relationship to MenuItem model
    """

    __tablename__ = "menu_item_ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Relationships
    user = db.relationship("User", backref="menu_item_ratings")
    menu_item = db.relationship("MenuItem", back_populates="ratings")
