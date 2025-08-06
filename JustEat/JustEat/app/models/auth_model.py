from enum import Enum

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class UserRole(Enum):
    CUSTOMER = "customer"
    OWNER = "owner"


class User(db.Model, UserMixin):
    """User model representing all system users.

    Attributes:
        id: Primary key
        name: User's full name
        phone: Unique phone number
        email: Unique email address
        password_hash: Hashed password storage
        role: User role (customer or owner)
        cart: Associated shopping cart (1:1 relationship)
        orders: List of user's orders (1:many relationship)
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)

    cart = db.relationship("Cart", back_populates="user", uselist=False)
    orders = db.relationship("Order", back_populates="user")
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    favorite_menu_items = db.relationship("FavoriteMenuItem", back_populates="user", cascade="all, delete-orphan")

    @property
    def password(self):
        """Prevent direct password access (security measure)."""
        raise AttributeError("Inaccessible")

    @password.setter
    def password(self, text_password):
        """Generate password hash when setting password.

        Args:
            password: Plain text password to hash and store
        """
        self.password_hash = generate_password_hash(text_password)

    def verify_password(self, text_password):
        """Check if provided password matches stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, text_password)

    def __repr__(self):
        """Official string representation of User."""
        return f"<User {self.name} ({self.role.value})>"
