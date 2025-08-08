from app.extensions import db
from sqlalchemy.sql import func


__all__ = ['Favorite', 'FavoriteMenuItem']


class Favorite(db.Model):
    """Model representing a user's favorite restaurant."""
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    
    # Relationships
    user = db.relationship("User", back_populates="favorites")
    restaurant = db.relationship("Restaurant", back_populates="favorites")
    
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (db.UniqueConstraint("user_id", "restaurant_id", name="unique_user_restaurant_favorite"),)
    
    def __repr__(self):
        return f"<Favorite user_id={self.user_id} restaurant_id={self.restaurant_id}>"


class FavoriteMenuItem(db.Model):
    """Model representing a user's favorite menu item."""
    
    __tablename__ = "favorite_menu_items"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    
    # Relationships
    user = db.relationship("User", back_populates="favorite_menu_items")
    menu_item = db.relationship("MenuItem", back_populates="favorited_by")
    
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (db.UniqueConstraint("user_id", "menu_item_id", name="unique_user_menu_item_favorite"),)
    
    def __repr__(self):
        return f"<FavoriteMenuItem user_id={self.user_id} menu_item_id={self.menu_item_id}>"