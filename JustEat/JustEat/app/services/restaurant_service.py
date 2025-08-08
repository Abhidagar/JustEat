from datetime import time
from typing import List, Optional

from flask import current_app

from app.extensions import db
from app.models import Category, Cuisine, Restaurant, User
from app.utils import generate_restaurant_slug

# only handles restaurant-related operations (Single Responsibility Principle)
def get_all_restaurants() -> List[Restaurant]:
    """Retrieve all active restaurants sorted by creation date."""
    try:
        return (
            Restaurant.query
            .filter(Restaurant.is_active == True)
            .order_by(Restaurant.created_at.desc())
            .all()
        )
    except Exception as e:
        current_app.logger.error(f"Failed to fetch all restaurants: {str(e)}")
        return []


def get_user_restaurants(user: User) -> List[Restaurant]:
    """Retrieve restaurants owned by a specific user."""
    try:
        return (
            Restaurant.query
            .filter_by(owner_id=user.id)
            .order_by(Restaurant.created_at.desc())
            .all()
        )
    except Exception as e:
        current_app.logger.error(
            f"Failed to fetch restaurants for user {user.id}: {str(e)}"
        )
        return []


def get_restaurant_by_slug(slug: str) -> Optional[Restaurant]:
    """Retrieve restaurant by its unique slug."""
    try:
        return Restaurant.query.filter_by(slug=slug).first()
    except Exception as e:
        current_app.logger.error(f"Failed to fetch restaurant by slug {slug}: {str(e)}")
        return None

#Dependency inversion principle(DIP): high-level modules should not depend on low-level modules
def create_new_restaurant(
    owner_id: int,
    name: str,
    location: str,
    opening_time: time,
    closing_time: time
) -> Optional[Restaurant]:
    """Create a new restaurant with generated slug."""
    try:
        restaurant = Restaurant(
            owner_id=owner_id,
            name=name.strip(),
            location=location.strip(),
            opening_time=opening_time,
            closing_time=closing_time,
            is_active=False  # New restaurants inactive by default
        )

        db.session.add(restaurant)
        db.session.flush()  # Get ID before slug generation
        restaurant.slug = generate_restaurant_slug(restaurant.name, restaurant.id)
        db.session.commit()

        current_app.logger.info(f"Created new restaurant {restaurant.id}")
        return restaurant

    except Exception as e:
        current_app.logger.error(
            f"Failed to create restaurant for owner {owner_id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return None


def update_restaurant_details(
    slug: str,
    name: str,
    location: str,
    opening_time: time,
    closing_time: time
) -> Optional[Restaurant]:
    """Update restaurant details and regenerate slug if name changed."""
    try:
        restaurant = get_restaurant_by_slug(slug)
        if not restaurant:
            current_app.logger.warning(f"Restaurant not found for slug {slug}")
            return None

        name_changed = restaurant.name != name
        restaurant.name = name.strip()
        restaurant.location = location.strip()
        restaurant.opening_time = opening_time
        restaurant.closing_time = closing_time

        if name_changed:
            restaurant.slug = generate_restaurant_slug(restaurant.name, restaurant.id)

        db.session.commit()
        current_app.logger.info(f"Updated details for restaurant {restaurant.id}")
        return restaurant

    except Exception as e:
        current_app.logger.error(
            f"Failed to update restaurant {slug}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return None


def update_restaurant_status(restaurant: Restaurant, status: bool) -> bool:
    """Toggle restaurant active/inactive status."""
    try:
        restaurant.is_active = status
        db.session.commit()
        current_app.logger.info(
            f"Set status to {'active' if status else 'inactive'} "
            f"for restaurant {restaurant.id}"
        )
        return True
    except Exception as e:
        current_app.logger.error(
            f"Failed to update status for restaurant {restaurant.id}: {str(e)}"
        )
        db.session.rollback()
        return False


def update_restaurant_cuisines(
    restaurant: Restaurant,
    cuisine_ids: List[int]
) -> Optional[Restaurant]:
    """Update restaurant's cuisine associations."""
    try:
        cuisines = Cuisine.query.filter(Cuisine.id.in_(cuisine_ids)).all()
        restaurant.cuisines = cuisines
        db.session.commit()
        current_app.logger.info(
            f"Updated {len(cuisines)} cuisines for restaurant {restaurant.id}"
        )
        return restaurant
    except Exception as e:
        current_app.logger.error(
            f"Failed to update cuisines for restaurant {restaurant.id}: {str(e)}"
        )
        db.session.rollback()
        return None


def get_all_cuisines() -> List[Cuisine]:
    """Retrieve all available cuisine types."""
    try:
        return Cuisine.query.all()
    except Exception as e:
        current_app.logger.error(f"Failed to fetch cuisines: {str(e)}")
        return []


def get_all_categories() -> List[Category]:
    """Retrieve all menu categories."""
    try:
        return Category.query.all()
    except Exception as e:
        current_app.logger.error(f"Failed to fetch categories: {str(e)}")
        return []


def delete_restaurant(restaurant: Restaurant) -> bool:
    """Permanently delete a restaurant."""
    try:
        db.session.delete(restaurant)
        db.session.commit()
        current_app.logger.warning(f"Deleted restaurant {restaurant.id}")
        return True
    except Exception as e:
        current_app.logger.error(
            f"Failed to delete restaurant {restaurant.id}: {str(e)}",
            exc_info=True
        )
        db.session.rollback()
        return False


def update_restaurant_rating(restaurant_id: int, new_rating: float) -> bool:
    """Update restaurant's average rating with new review."""
    try:
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            current_app.logger.warning(f"Restaurant {restaurant_id} not found")
            return False

        if restaurant.rating_count == 0:
            restaurant.avg_rating = new_rating
            restaurant.rating_count = 1
        else:
            total = restaurant.avg_rating * restaurant.rating_count
            total += new_rating
            restaurant.rating_count += 1
            restaurant.avg_rating = total / restaurant.rating_count

        db.session.commit()
        current_app.logger.debug(
            f"Updated rating for restaurant {restaurant_id} to {restaurant.avg_rating}"
        )
        return True
    except Exception as e:
        current_app.logger.error(
            f"Failed to update rating for restaurant {restaurant_id}: {str(e)}"
        )
        db.session.rollback()
        return False