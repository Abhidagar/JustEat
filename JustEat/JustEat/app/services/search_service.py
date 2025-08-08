from typing import List, Tuple

from flask import current_app
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import Category, Cuisine, MenuItem, Restaurant


def get_search_results(query: str) -> Tuple[List[Restaurant], List[MenuItem]]:
    """
    Search for restaurants and menu items matching the query.

    Args:
        query: Search term to match against restaurant and menu item attributes

    Returns:
        Tuple containing:
        - List of matching Restaurant objects
        - List of matching MenuItem objects (with eager-loaded relationships)

    Raises:
        DatabaseError: If there's an issue executing the queries
    """
    try:
        query = query or ""
        query = query.strip().lower()
        if not query:
            current_app.logger.debug("Empty search query received")
            return [], []

        current_app.logger.info(f"Processing search for: {query}")

        # Search restaurants by name or location
        restaurants = search_restaurants(query)
        current_app.logger.debug(f"Found {len(restaurants)} matching restaurants")

        # Search menu items by name, cuisine, or category
        menu_items = search_menu_items(query)
        current_app.logger.debug(f"Found {len(menu_items)} matching menu items")

        return restaurants, menu_items

    except Exception as e:
        current_app.logger.error(
            f"Search failed for query '{query}': {str(e)}", exc_info=True
        )
        raise


def search_restaurants(query: str) -> List[Restaurant]:
    """Search restaurants by name or location."""
    return (
        Restaurant.query.filter(
            or_(
                Restaurant.name.ilike(f"%{query}%"),
                Restaurant.location.ilike(f"%{query}%"),
            ),
            Restaurant.is_active == True,  # Only active restaurants
        )
        .order_by(Restaurant.name.asc())
        .all()
    )


def search_menu_items(query: str) -> List[MenuItem]:
    """Search menu items by name, cuisine, or category."""
    return (
        MenuItem.query.options(
            joinedload(MenuItem.cuisine),
            joinedload(MenuItem.category),
            joinedload(MenuItem.restaurant),
        )
        .join(Cuisine)
        .join(Category)
        .filter(
            or_(
                MenuItem.name.ilike(f"%{query}%"),
                Cuisine.name.ilike(f"%{query}%"),
                Category.name.ilike(f"%{query}%"),
            ),
            MenuItem.is_active == True,  # Only active menu items
        )
        .order_by(MenuItem.name.asc())
        .all()
    )


def get_filtered_search_results(
    query: str = None,
    cuisine_ids: List[str] = None,
    restaurant_ids: List[str] = None,
    price_min: float = None,
    price_max: float = None
) -> Tuple[List[Restaurant], List[MenuItem]]:
    """
    Search for restaurants and menu items with filters applied.

    Args:
        query: Search term to match against restaurant and menu item attributes
        cuisine_ids: List of cuisine IDs to filter by
        restaurant_ids: List of restaurant IDs to filter by
        price_min: Minimum price filter
        price_max: Maximum price filter

    Returns:
        Tuple containing:
        - List of matching Restaurant objects
        - List of matching MenuItem objects (with eager-loaded relationships)
    """
    try:
        current_app.logger.info(f"Processing filtered search for: {query} with filters")

        # Convert string IDs to integers
        cuisine_ids = [int(id) for id in cuisine_ids if id.isdigit()] if cuisine_ids else []
        restaurant_ids = [int(id) for id in restaurant_ids if id.isdigit()] if restaurant_ids else []

        # Search restaurants with filters
        restaurants = search_restaurants_filtered(query, cuisine_ids, restaurant_ids)
        current_app.logger.debug(f"Found {len(restaurants)} matching restaurants")

        # Search menu items with filters
        menu_items = search_menu_items_filtered(query, cuisine_ids, restaurant_ids, price_min, price_max)
        current_app.logger.debug(f"Found {len(menu_items)} matching menu items")

        return restaurants, menu_items

    except Exception as e:
        current_app.logger.error(
            f"Filtered search failed for query '{query}': {str(e)}", exc_info=True
        )
        # Fallback to regular search if filtering fails
        return get_search_results(query) if query else ([], [])


def search_restaurants_filtered(
    query: str = None,
    cuisine_ids: List[int] = None,
    restaurant_ids: List[int] = None
) -> List[Restaurant]:
    """Search restaurants with filters applied."""
    query_builder = db.session.query(Restaurant).filter(Restaurant.is_active == True)
    
    # Apply text search if query provided
    if query:
        query = query.strip().lower()
        query_builder = query_builder.filter(
            or_(
                Restaurant.name.ilike(f"%{query}%"),
                Restaurant.location.ilike(f"%{query}%"),
            )
        )
    
    # Apply cuisine filter
    if cuisine_ids:
        query_builder = query_builder.join(Restaurant.cuisines).filter(
            Cuisine.id.in_(cuisine_ids)
        )
    
    # Apply restaurant filter (for specific restaurant selection)
    if restaurant_ids:
        query_builder = query_builder.filter(Restaurant.id.in_(restaurant_ids))
    
    return query_builder.order_by(Restaurant.name.asc()).all()


def search_menu_items_filtered(
    query: str = None,
    cuisine_ids: List[int] = None,
    restaurant_ids: List[int] = None,
    price_min: float = None,
    price_max: float = None
) -> List[MenuItem]:
    """Search menu items with filters applied."""
    query_builder = (
        db.session.query(MenuItem)
        .options(
            joinedload(MenuItem.restaurant),
            joinedload(MenuItem.cuisine),
            joinedload(MenuItem.category),
        )
        .filter(MenuItem.is_active == True)
    )
    
    # Track if we need to join tables
    cuisine_joined = False
    category_joined = False
    
    # Apply text search if query provided
    if query:
        query = query.strip().lower()
        query_builder = query_builder.join(Cuisine).join(Category)
        cuisine_joined = True
        category_joined = True
        query_builder = query_builder.filter(
            or_(
                MenuItem.name.ilike(f"%{query}%"),
                MenuItem.description.ilike(f"%{query}%"),
                Cuisine.name.ilike(f"%{query}%"),
                Category.name.ilike(f"%{query}%"),
            )
        )
    
    # Apply cuisine filter
    if cuisine_ids:
        if not cuisine_joined:
            query_builder = query_builder.join(Cuisine)
        query_builder = query_builder.filter(Cuisine.id.in_(cuisine_ids))
    
    # Apply price filters
    if price_min is not None:
        query_builder = query_builder.filter(MenuItem.price >= price_min)
    if price_max is not None:
        query_builder = query_builder.filter(MenuItem.price <= price_max)
    
    # Apply restaurant filter
    if restaurant_ids:
        query_builder = query_builder.filter(MenuItem.restaurant_id.in_(restaurant_ids))
    
    return query_builder.order_by(MenuItem.name.asc()).all()
