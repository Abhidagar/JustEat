from typing import List, Optional

from app.extensions import db
from app.models import Favorite, Restaurant, User


def toggle_favorite(user: User, restaurant_id: int) -> bool:
    """
    Toggle a restaurant as favorite for a user.
    
    Args:
        user: The user object
        restaurant_id: ID of the restaurant to favorite/unfavorite
        
    Returns:
        bool: True if restaurant is now favorited, False if unfavorited
    """
    try:
        # Check if already favorited
        existing_favorite = Favorite.query.filter_by(
            user_id=user.id, 
            restaurant_id=restaurant_id
        ).first()
        
        if existing_favorite:
            # Remove from favorites
            db.session.delete(existing_favorite)
            db.session.commit()
            return False
        else:
            # Add to favorites
            new_favorite = Favorite(user_id=user.id, restaurant_id=restaurant_id)
            db.session.add(new_favorite)
            db.session.commit()
            return True
            
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling favorite: {e}")
        return False


def is_favorited(user: User, restaurant_id: int) -> bool:
    """
    Check if a restaurant is favorited by a user.
    
    Args:
        user: The user object
        restaurant_id: ID of the restaurant to check
        
    Returns:
        bool: True if favorited, False otherwise
    """
    if not user.is_authenticated:
        return False
        
    return Favorite.query.filter_by(
        user_id=user.id, 
        restaurant_id=restaurant_id
    ).first() is not None


def get_user_favorites(user: User) -> List[Restaurant]:
    """
    Get all favorite restaurants for a user.
    
    Args:
        user: The user object
        
    Returns:
        List[Restaurant]: List of favorite restaurants
    """
    if not user.is_authenticated:
        return []
        
    favorites = (
        db.session.query(Restaurant)
        .join(Favorite, Restaurant.id == Favorite.restaurant_id)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    
    return favorites


def get_favorites_with_info(user: User) -> List[dict]:
    """
    Get favorite restaurants with additional info like when favorited.
    
    Args:
        user: The user object
        
    Returns:
        List[dict]: List of dicts containing restaurant and favorite info
    """
    if not user.is_authenticated:
        return []
        
    favorites = (
        db.session.query(Restaurant, Favorite)
        .join(Favorite, Restaurant.id == Favorite.restaurant_id)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    
    return [
        {
            'restaurant': restaurant,
            'favorited_at': favorite.created_at
        }
        for restaurant, favorite in favorites
    ]


def get_favorite_menu_items_with_info(user: User) -> List[dict]:
    """
    Get favorite menu items with additional info like when favorited.
    This is a placeholder since menu item favorites are not implemented yet.
    
    Args:
        user: The user object
        
    Returns:
        List[dict]: Empty list for now
    """
    return []