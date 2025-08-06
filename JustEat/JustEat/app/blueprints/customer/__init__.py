from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user

from app.models import UserRole
from app.utils import get_dashboard_for_role

# Initialize customer blueprint
customer_bp = Blueprint("customer", __name__)


@customer_bp.before_request
def restrict_to_customers():
    """
    Restrict access to customer routes only for authenticated customers.

    This before_request handler ensures:
    1. User is authenticated
    2. User has CUSTOMER role

    """
    # Authentication check
    if not current_user.is_authenticated:
        flash("Please login to access this page", "danger")
        return redirect(url_for("auth.login"))

    # Role authorization check
    if current_user.role != UserRole.CUSTOMER:
        flash("This section is only available for customers", "danger")
        return redirect(url_for(get_dashboard_for_role(current_user.role)))


# Import routes after blueprint initialization to avoid circular imports
from . import routes
