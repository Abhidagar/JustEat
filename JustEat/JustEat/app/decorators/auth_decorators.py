from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from app.models import UserRole
from app.utils import get_dashboard_for_role


def role_required(role: UserRole):
    """Decorator factory to restrict access by user role.

    Args:
        role (UserRole): Required role to access the endpoint

    Returns:
        function: Decorator function that enforces role requirements
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Authentication check
            if not current_user.is_authenticated:
                flash("Please log in to access this page", "warning")
                return redirect(url_for("auth.login"))

            # Authorization check
            if current_user.role != role:
                role_name = role.name.lower()
                flash(f"This section is for {role_name}s only", "danger")
                return redirect(url_for(get_dashboard_for_role(current_user.role)))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def owner_required(f):
    """Shortcut decorator requiring OWNER role."""
    return role_required(UserRole.OWNER)(f)


def customer_required(f):
    """Shortcut decorator requiring CUSTOMER role."""
    return role_required(UserRole.CUSTOMER)(f)
