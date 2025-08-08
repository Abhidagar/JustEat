from datetime import datetime, timedelta
from typing import Optional, Set

from flask import current_app
from sqlalchemy import func

from app.extensions import db
from app.models import MenuItem, Order, OrderItem


def get_item_by_id(id: int) -> Optional[MenuItem]:
    """Retrieve menu item by ID with caching consideration."""
    try:
        return MenuItem.query.get(id)
    except Exception as e:
        current_app.logger.error(f"Failed to fetch item {id}: {str(e)}")
        return None


def get_popular_item_ids(restaurant, criteria_count: int = 1) -> Set[int]:
    """Get frequently ordered item IDs within last 24 hours."""
    try:
        popular_items = (
            OrderItem.query.join(Order)
            .filter(
                Order.restaurant_id == restaurant.id,
                OrderItem.created_at >= datetime.now() - timedelta(hours=24),
            )
            .group_by(OrderItem.menu_item_id)
            .having(func.sum(OrderItem.quantity) > criteria_count)
            .all()
        )
        current_app.logger.debug(
            f"Found {len(popular_items)} popular items for restaurant {restaurant.id}"
        )
        return {item.menu_item_id for item in popular_items}
    except Exception as e:
        current_app.logger.error(
            f"Error calculating popular items for restaurant {restaurant.id}: {str(e)}"
        )
        return set()


def get_popular_item_ids_for_search(menu_items, criteria_count: int = 1) -> Set[int]:
    """Get popular item IDs from a list of menu items for search results."""
    try:
        if not menu_items:
            return set()
        
        # Get all menu item IDs from the search results
        menu_item_ids = [item.id for item in menu_items]
        
        # Find popular items among the search results
        popular_items = (
            OrderItem.query.join(Order)
            .filter(
                OrderItem.menu_item_id.in_(menu_item_ids),
                OrderItem.created_at >= datetime.now() - timedelta(hours=24),
            )
            .group_by(OrderItem.menu_item_id)
            .having(func.sum(OrderItem.quantity) > criteria_count)
            .all()
        )
        
        current_app.logger.debug(
            f"Found {len(popular_items)} popular items in search results"
        )
        return {item.menu_item_id for item in popular_items}
    except Exception as e:
        current_app.logger.error(
            f"Error calculating popular items for search results: {str(e)}"
        )
        return set()


def create_menu_item(
    restaurant_id: int,
    name: str,
    description: str,
    price: float,
    cuisine_id: int,
    category_id: int,
) -> Optional[MenuItem]:
    """Create new menu item with validation."""
    try:
        menu_item = MenuItem(
            restaurant_id=restaurant_id,
            name=name.strip(),
            description=description.strip(),
            price=price,
            cuisine_id=cuisine_id,
            category_id=category_id,
        )
        
        db.session.add(menu_item)
        db.session.commit()
        current_app.logger.info(f"Created menu item {menu_item.id}")
        return menu_item
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to create menu item: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return None


def update_menu_item(
    item_id: int,
    name: str,
    description: str,
    price: float,
    cuisine_id: int,
    category_id: int,
    is_non_veg: bool,
) -> Optional[MenuItem]:
    """Update existing menu item details."""
    try:
        item = get_item_by_id(item_id)
        if not item:
            current_app.logger.warning(f"Menu item {item_id} not found for update")
            return None
            
        item.name = name.strip()
        item.description = description.strip()
        item.price = price
        item.cuisine_id = cuisine_id
        item.category_id = category_id
        item.is_non_veg = is_non_veg
        
        db.session.commit()
        current_app.logger.info(f"Updated menu item {item_id}")
        return item
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to update menu item {item_id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return None


def update_item_special_status(item: MenuItem, status: bool) -> Optional[MenuItem]:
    """Toggle special status flag for menu item."""
    try:
        item.is_special = status
        db.session.commit()
        current_app.logger.info(
            f"Set special status to {status} for item {item.id}"
        )
        return item
    except Exception as e:
        current_app.logger.error(
            f"Failed to update special status for item {item.id}: {str(e)}"
        )
        db.session.rollback()
        return None


def update_item_active_status(item: MenuItem, status: bool) -> Optional[MenuItem]:
    """Toggle active/availability status flag for menu item."""
    try:
        item.is_active = status
        db.session.commit()
        current_app.logger.info(
            f"Set active status to {status} for item {item.id}"
        )
        return item
    except Exception as e:
        current_app.logger.error(
            f"Failed to update active status for item {item.id}: {str(e)}"
        )
        db.session.rollback()
        return None


def delete_menu_item(item_id: int) -> bool:
    """Permanently remove menu item from system."""
    try:
        item = get_item_by_id(item_id)
        if not item:
            current_app.logger.warning(f"Item {item_id} not found for deletion")
            return False
            
        db.session.delete(item)
        db.session.commit()
        current_app.logger.info(f"Deleted menu item {item_id}")
        return True
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to delete menu item {item_id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return False


def update_item_rating(menu_item_id: int, new_rating: float) -> bool:
    """Update item's average rating with new review."""
    try:
        menu_item = get_item_by_id(menu_item_id)
        if not menu_item:
            current_app.logger.warning(f"Item {menu_item_id} not found for rating update")
            return False
            
        if menu_item.rating_count == 0:
            menu_item.avg_rating = new_rating
            menu_item.rating_count = 1
        else:
            total = menu_item.avg_rating * menu_item.rating_count
            total += new_rating
            menu_item.rating_count += 1
            menu_item.avg_rating = total / menu_item.rating_count
            
        db.session.commit()
        current_app.logger.debug(
            f"Updated rating for item {menu_item_id} to {menu_item.avg_rating}"
        )
        return True
        
    except Exception as e:
        current_app.logger.error(
            f"Failed to update rating for item {menu_item_id}: {str(e)}"
        )
        db.session.rollback()
        return False