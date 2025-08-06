from datetime import time
import random
import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Cuisine, Restaurant, User, UserRole, MenuItem, Category


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def customer_a():
    user = User(
        email="test@example.com",
        phone="9999999999",
        name="Test Customer",
        role=UserRole.CUSTOMER,
    )
    user.password = "password"

    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def owner_a():
    owner = User(
        name="Test Owner 1",
        phone="8888888888",
        email="owner_1@example.com",
        role=UserRole.OWNER,
    )
    owner.password = "password"

    db.session.add(owner)
    db.session.commit()

    return owner


@pytest.fixture
def owner_b():
    owner = User(
        name="Test Owner 2",
        phone="8888888889",
        email="owner_2@example.com",
        role=UserRole.OWNER,
    )
    owner.password = "password"

    db.session.add(owner)
    db.session.commit()

    return owner


@pytest.fixture
def cuisines():
    items = [Cuisine(name=f"Cuisine {i}") for i in range(1, 4)]
    db.session.add_all(items)
    db.session.commit()
    return items


@pytest.fixture
def categories():
    items = [Category(name=f"Category {i}") for i in range(1, 4)]
    db.session.add_all(items)
    db.session.commit()
    return items


@pytest.fixture
def restaurant_a(owner_a, cuisines):
    restaurant = Restaurant(
        name="Testaurant",
        location="Testville",
        slug="testaurant-1",
        opening_time=time(10, 0),
        closing_time=time(22, 0),
        owner_id=owner_a.id,
        cuisines=cuisines[:2],  # Assign first 2 cuisines
    )
    db.session.add(restaurant)
    db.session.commit()
    return restaurant


@pytest.fixture
def menu_a(restaurant_a, cuisines, categories):
    menu = [
        MenuItem(
            name="Pizza",
            description="Delicious cheese pizza",
            price=10.99,
            cuisine_id=random.choice(cuisines).id,
            category_id=random.choice(categories).id,
            restaurant_id=restaurant_a.id,
        ),
        MenuItem(
            name="Burger",
            description="Juicy beef burger",
            price=8.99,
            cuisine_id=random.choice(cuisines).id,
            category_id=random.choice(categories).id,
            restaurant_id=restaurant_a.id,
        ),
    ]
    db.session.add_all(menu)
    db.session.commit()
    return menu


@pytest.fixture
def login_user(client):
    def _login(user):
        with client.session_transaction() as session:
            session["_user_id"] = str(user.id)
        return user

    return _login
