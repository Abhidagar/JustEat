import random
from datetime import time

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import (
    Cart,
    CartItem,
    Category,
    Cuisine,
    MenuItem,
    MenuItemRating,
    Order,
    OrderItem,
    OrderStatus,
    Restaurant,
    RestaurantRating,
    User,
    UserRole,
)
from app.utils import generate_restaurant_slug


def seed():
    # Create the Flask application
    app = create_app()

    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # USERS
        customer1 = User(
            name="john doe",
            email="john@example.com",
            role=UserRole.CUSTOMER,
            phone="1234567890",
            password_hash=generate_password_hash("password"),
        )
        customer2 = User(
            name="jane smith",
            email="jane@example.com",
            role=UserRole.CUSTOMER,
            phone="1234567891",
            password_hash=generate_password_hash("password"),
        )
        owner1 = User(
            name="chef mario",
            email="mario@example.com",
            role=UserRole.OWNER,
            phone="1234567892",
            password_hash=generate_password_hash("password"),
        )
        owner2 = User(
            name="chef luigi",
            email="luigi@example.com",
            role=UserRole.OWNER,
            phone="1234567893",
            password_hash=generate_password_hash("password"),
        )
        db.session.add_all([customer1, customer2, owner1, owner2])
        db.session.commit()

        print("Users created successfully.")

        # CUISINES
        cuisines = [
            Cuisine(name="Italian", image="https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?auto=compress&cs=tinysrgb&w=400"),
            Cuisine(name="Chinese", image="https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg?auto=compress&cs=tinysrgb&w=400"),
            Cuisine(name="Indian", image="https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=400"),
            Cuisine(name="Mexican", image="https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg?auto=compress&cs=tinysrgb&w=400"),
            Cuisine(name="Thai", image="https://images.pexels.com/photos/162993/food-thai-spicy-asian-162993.jpeg?auto=compress&cs=tinysrgb&w=400"),
        ]
        db.session.add_all(cuisines)
        db.session.commit()

        print("Cuisines created successfully.")

        # CATEGORIES
        categorie_names = ["Appetizer", "Main Course", "Dessert", "Beverage", "Side"]
        categories = [Category(name=name) for name in categorie_names]
        db.session.add_all(categories)
        db.session.commit()

        print("Categories created successfully.")

        restaurants = []
        all_menu_items = []

        r_names = [
            "Pasta Palace",
            "Sushi Spot",
            "Curry Corner",
            "Taco Town",
            "Thai Delight",
        ]

        r_locs = [
            "New Delhi",
            "Mumbai",
            "Bangalore",
            "Chennai",
            "Hyderabad",
        ]

        r_images = [
            "/static/images/restaurants/pasta-palace.jpg",
            "/static/images/restaurants/sushi-spot.jpg",
            "/static/images/restaurants/curry-corner.jpg",
            "/static/images/restaurants/taco-town.jpg",
            "/static/images/restaurants/thai-delight.jpg",
        ]

        for i in range(5):
            restaurant = Restaurant(
                name=r_names[i],
                is_active=True,
                location=r_locs[i],
                image=r_images[i],
                owner_id=random.choice([owner1.id, owner2.id]),  # Randomly assign owner
                slug=generate_restaurant_slug(r_names[i], i + 1),  # Generate slug
                opening_time=time(10, 0),
                closing_time=time(23, 0),
            )
            db.session.add(restaurant)
            db.session.flush()  # To get restaurant.id

            # Add cuisines
            restaurant.cuisines = random.sample(cuisines, k=3)

            i_names = [
                "Spaghetti",
                "Sushi",
                "Biryani",
                "Tacos",
                "Pad Thai",
                "Pizza",
                "Noodles",
                "Curry",
                "Chili",
                "Spring Rolls",
                "Ice Cream",
                "Margarita",
                "Lassi",
                "Soda",
                "Tea",
                "Coffee",
                "Salad",
                "Fries",
                "Nachos",
                "Dim Sum",
                "Dumplings",
                "Pancakes",
                "Waffles",
                "Cheesecake",
                "Brownies",
            ]

            # MENU ITEMS
            menu_items_data = [
                {"name": "Spaghetti", "image": "https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg"},
                {"name": "Sushi", "image": "https://images.pexels.com/photos/248444/pexels-photo-248444.jpeg"},
                {"name": "Biryani", "image": "https://images.pexels.com/photos/7469289/pexels-photo-7469289.jpeg"},
                {"name": "Tacos", "image": "https://images.pexels.com/photos/2338015/pexels-photo-2338015.jpeg"},
                {"name": "Pad Thai", "image": "https://images.pexels.com/photos/162993/food-thai-spicy-asian-162993.jpeg"},
                {"name": "Pizza", "image": "https://images.pexels.com/photos/845811/pexels-photo-845811.jpeg"},
                {"name": "Noodles", "image": "https://images.pexels.com/photos/2347311/pexels-photo-2347311.jpeg"},
                {"name": "Curry", "image": "https://images.pexels.com/photos/674574/pexels-photo-674574.jpeg"},
                {"name": "Chili", "image": "https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg"},
                {"name": "Spring Rolls", "image": "https://images.pexels.com/photos/3569706/pexels-photo-3569706.jpeg"},
                {"name": "Ice Cream", "image": "https://images.pexels.com/photos/1362534/pexels-photo-1362534.jpeg"},
                {"name": "Margarita", "image": "https://images.pexels.com/photos/10836977/pexels-photo-10836977.jpeg"},
                {"name": "Margarita Dessert", "image": "https://images.pexels.com/photos/2109099/pexels-photo-2109099.jpeg"},
                {"name": "Lassi", "image": "https://images.pexels.com/photos/6808666/pexels-photo-6808666.jpeg"},
                {"name": "Soda", "image": "https://images.pexels.com/photos/2775860/pexels-photo-2775860.jpeg"},
                {"name": "Tea", "image": "https://images.pexels.com/photos/1362534/pexels-photo-1362534.jpeg"},
                {"name": "Coffee", "image": "https://images.pexels.com/photos/851555/pexels-photo-851555.jpeg"},
                {"name": "Salad", "image": "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg"},
                {"name": "Fries", "image": "https://images.pexels.com/photos/115740/pexels-photo-115740.jpeg"},
                {"name": "Nachos", "image": "https://images.pexels.com/photos/3904035/pexels-photo-3904035.jpeg"},
                {"name": "Dim Sum", "image": "https://images.pexels.com/photos/3911229/pexels-photo-3911229.jpeg"},
                {"name": "Dumplings", "image": "https://images.pexels.com/photos/3911229/pexels-photo-3911229.jpeg"},
                {"name": "Pancakes", "image": "https://images.pexels.com/photos/2516025/pexels-photo-2516025.jpeg"},
                {"name": "Waffles", "image": "https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg"},
                {"name": "Cheesecake", "image": "https://images.pexels.com/photos/3185509/pexels-photo-3185509.png"},
                {"name": "Brownies", "image": "https://images.pexels.com/photos/2067396/pexels-photo-2067396.jpeg"},
            ]

            for j in range(5):
                selected_item = random.choice(menu_items_data)
                item = MenuItem(
                    name=selected_item["name"],
                    description=f"Tasty {selected_item['name'].lower()} from restaurant {i + 1}",
                    price=round(random.uniform(5, 25), 2),
                    category=random.choice(categories),
                    cuisine=random.choice(cuisines),
                    restaurant_id=restaurant.id,
                    is_active=random.randint(1, 100) < 80,  # Randomly set active status
                    is_non_veg=random.randint(1, 100)
                    < 60,  # Randomly set non-veg status
                    image=selected_item["image"]  # Add the image URL
                )
                all_menu_items.append(item)
                db.session.add(item)

            restaurants.append(restaurant)

        db.session.commit()

        print("Restaurants and menu items created successfully.")

        # CART for customer1
        cart = Cart(user_id=customer1.id, restaurant_id=restaurants[0].id)
        db.session.add(cart)
        db.session.flush()

        # Add 2 items from first restaurant to cart
        cart_items = [
            CartItem(cart_id=cart.id, menu_item_id=all_menu_items[0].id, quantity=2),
            CartItem(cart_id=cart.id, menu_item_id=all_menu_items[1].id, quantity=1),
        ]
        db.session.add_all(cart_items)
        db.session.commit()

        # ORDERS
        for i in range(2):
            order = Order(
                customer_id=customer2.id,
                restaurant_id=restaurants[i].id,
                total=0,
                status=OrderStatus.DELIVERED,
            )
            db.session.add(order)
            db.session.flush()

            if i == 0:
                # Add rating for the first order
                rating = random.randint(1, 5)
                restaurant_rating = RestaurantRating(
                    restaurant_id=restaurants[i].id,
                    user_id=customer2.id,
                    rating=rating,
                    comment="Great food!",
                    order_id=order.id,
                )
                db.session.add(restaurant_rating)
                restaurants[i].avg_rating = rating
                restaurants[i].rating_count = 1

            # Add 2 items from that restaurant
            items = [
                item
                for item in all_menu_items
                if item.restaurant_id == restaurants[i].id
            ][:2]
            total = 0
            for item in items:
                qty = random.randint(1, 3)
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=item.id,
                    name=item.name,
                    quantity=qty,
                    price_at_order=item.price,
                )
                total += item.price * qty
                db.session.add(order_item)

                if i == 0:
                    # Add rating for the menu item
                    rating = random.randint(1, 5)
                    order_item_rating = MenuItemRating(
                        menu_item_id=item.id,
                        user_id=customer2.id,
                        rating=rating,
                    )
                    db.session.add(order_item_rating)
                    item.avg_rating = rating
                    item.rating_count = 1

            order.total = round(total, 2)

            db.session.commit()

        print("Orders created successfully.")


if __name__ == "__main__":
    seed()
