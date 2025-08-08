from datetime import datetime as dt

from app.extensions import db

# Association table for many-to-many between Restaurant and Cuisine
restaurant_cuisine = db.Table(
    "restaurant_cuisine",
    db.Column(
        "restaurant_id", db.Integer, db.ForeignKey("restaurants.id"), primary_key=True
    ),
    db.Column("cuisine_id", db.Integer, db.ForeignKey("cuisines.id"), primary_key=True),
)

# Only restaurant-related attributes (Single Responsibility Principle)
class Restaurant(db.Model):
    """Represents a restaurant business in the system.

    Attributes:
        id: Primary key
        owner_id: Reference to owner user
        name: Restaurant name
        location: Physical address
        opening_time: Daily opening time
        closing_time: Daily closing time
        slug: URL-friendly identifier
        avg_rating: Calculated average rating
        rating_count: Number of ratings received
        created_at: When restaurant was registered
        is_active: Business status flag
        image: Logo/cover image URL
    """

    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)

    slug = db.Column(db.String(255), unique=True)

    avg_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=dt.now)
    is_active = db.Column(db.Boolean, default=False)

    image = db.Column(
        db.String(255),
        default="https://cwdaust.com.au/wpress/wp-content/uploads/2015/04/placeholder-restaurant.png",
    )

    # Relationships
    carts = db.relationship("Cart", back_populates="restaurant")
    cuisines = db.relationship(
        "Cuisine", secondary=restaurant_cuisine, back_populates="restaurants"
    )
    menu_items = db.relationship(
        "MenuItem", back_populates="restaurant", cascade="all, delete-orphan"
    )
    orders = db.relationship("Order", back_populates="restaurant")
    ratings = db.relationship(
        "RestaurantRating", back_populates="restaurant", cascade="all, delete-orphan"
    )
    favorites = db.relationship("Favorite", back_populates="restaurant", cascade="all, delete-orphan")


class MenuItem(db.Model):
    """Represents a single menu item offered by a restaurant.

    Attributes:
        id: Primary key
        name: Item name
        description: Item description
        price: Current price
        restaurant_id: Owning restaurant reference
        avg_rating: Calculated average rating
        rating_count: Number of ratings received
        cuisine_id: Cuisine type reference
        category_id: Menu category reference
        is_active: Availability status
        is_non_veg: Dietary classification
        is_special: Special item flag
        image: Item photo URL
    """

    __tablename__ = "menu_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)

    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurants.id"), nullable=False
    )

    avg_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)

    cuisine_id = db.Column(db.Integer, db.ForeignKey("cuisines.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    is_non_veg = db.Column(db.Boolean, default=False)

    is_special = db.Column(db.Boolean, default=False)

    image = db.Column(
        db.String(255),
        default="https://theme-assets.getbento.com/sensei/4f4ca77.sensei/assets/images/catering-item-placeholder-704x520.png",
    )

    restaurant = db.relationship("Restaurant", back_populates="menu_items")
    cuisine = db.relationship("Cuisine", back_populates="menu_items")
    category = db.relationship("Category", back_populates="menu_items")
    ratings = db.relationship(
        "MenuItemRating", back_populates="menu_item", cascade="all, delete-orphan"
    )
    favorited_by = db.relationship("FavoriteMenuItem", back_populates="menu_item", cascade="all, delete-orphan")


class Cuisine(db.Model):
    """Represents a type of cuisine (e.g., Italian, Mexican)."""

    __tablename__ = "cuisines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(
        db.String(255),
        default="https://tse3.mm.bing.net/th?id=OIP.k7zYh0xnwGj3NH0uY6ZQFwHaE8&pid=Api",
    )

    # Relationships
    restaurants = db.relationship(
        "Restaurant", secondary=restaurant_cuisine, back_populates="cuisines"
    )
    menu_items = db.relationship("MenuItem", back_populates="cuisine")


class Category(db.Model):
    """Represents a menu category (e.g., Appetizers, Desserts)."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    menu_items = db.relationship("MenuItem", back_populates="category")
