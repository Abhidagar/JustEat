from typing import Optional

from flask import current_app
from werkzeug.security import check_password_hash

from app.extensions import db, login_manager
from app.models import User


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Load user by ID for Flask-Login session management.

    Args:
        user_id: String representation of user ID

    Returns:
        User object if found, None otherwise
    """
    return db.session.get(User, int(user_id))

# Only handles authentication operations (Single Responsibility Principle)
def login_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password.

    Args:
        email: User's email address
        password: Plain text password to verify

    Returns:
        Authenticated User object if successful, None otherwise
    """
    user = User.query.filter_by(email=email).first()

    if user is None:
        current_app.logger.debug(f"Login attempt for unknown email: {email}")
        return None

    if not user.verify_password(password):
        current_app.logger.debug(f"Failed login attempt for user: {user.id}")
        return None

    current_app.logger.info(f"Successful login for user: {user.id}")
    return user


def update_profile(user: User, name: str, phone: str) -> Optional[User]:
    """Update user profile information.

    Args:
        user: User object to update
        name: New full name
        phone: New phone number

    Returns:
        Updated User object if successful, None otherwise

    Raises:
        ValueError: If phone number format is invalid
    """
    # Validate phone number format (basic check)
    if not phone.isdigit() or len(phone) < 10:
        raise ValueError("Invalid phone number format")

    try:
        user.name = name.strip()
        user.phone = phone

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f"Updated profile for user: {user.id}")
        return user

    except Exception as e:
        current_app.logger.error(f"Error updating profile for user {user.id}: {str(e)}")
        db.session.rollback()
        return None


def update_password(user: User, current_password: str, new_password: str) -> bool:
    """Update user password after verifying current password.

    Args:
        user: User object to update
        current_password: Current password for verification
        new_password: New password to set

    Returns:
        True if password was updated successfully, False otherwise
    """
    # Verify current password
    if not user.verify_password(current_password):
        current_app.logger.debug(f"Invalid current password for user: {user.id}")
        return False

    try:
        # Set new password using the property setter (this will automatically hash it)
        user.password = new_password
        
        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f"Password updated for user: {user.id}")
        return True

    except Exception as e:
        current_app.logger.error(f"Error updating password for user {user.id}: {str(e)}")
        db.session.rollback()
        return False
