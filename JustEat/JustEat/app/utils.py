from slugify import slugify

from .models import UserRole


def get_dashboard_for_role(role: UserRole) -> str:
    """
    Get the dashboard URL for a given user role.

    Args:
        role (UserRole): The role of the user.

    Returns:
        str: The URL of the dashboard for the given role.
    """
    dashboards = {
        UserRole.OWNER: "restaurant.dashboard",
        UserRole.CUSTOMER: "customer.home",
    }

    return dashboards.get(role, "auth.login")


def generate_restaurant_slug(name: str, id: int) -> str:
    """
    Generate a unique slug for a restaurant.

    Args:
        name (str): The name of the restaurant.
        id (int): The ID of the restaurant.

    Returns:
        str: A unique slug for the restaurant.
    """
    return f"{slugify(name)}-{id}"
