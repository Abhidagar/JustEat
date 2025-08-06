from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user

from app.models import UserRole
from app.utils import get_dashboard_for_role

# Initialize restaurant blueprint with URL prefix
restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurants")


@restaurant_bp.before_request
def restrict_to_owners():
    """Restrict access to restaurant routes to authenticated owners only.

    Checks:
    - User is authenticated (else redirect to login)
    - User has OWNER role (else redirect to role-appropriate dashboard)
    """
    # Authentication check
    if not current_user.is_authenticated:
        flash("Please login to access this page", "danger")
        return redirect(url_for("auth.login"))

    # Authorization check
    if current_user.role != UserRole.OWNER:
        flash("Access restricted to restaurant owners", "danger")
        return redirect(url_for(get_dashboard_for_role(current_user.role)))


# Import route modules after blueprint to avoid circular imports
from . import menu_item_routes, order_routes, restaurant_routes
