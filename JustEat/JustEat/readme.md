# JustEat - Food Ordering Application

The web application aims to provide a platform to order food, focused on delivering a seamless and
efficient user experience, empowering customers to effortlessly and swiftly place food orders. The
application aims to revolutionize the ordering process by offering an intuitive interface, streamlining
the ordering journey for users. Through swift and reliable service, personalized recommendations, and
dietary restrictions, our goal is to exceed customer expectations, making food ordering quick,
convenient, and enjoyable.

## Features

- Restaurant Management

  - Create and manage restaurant profiles

  - Menu item management with categories and cuisines

  - Operating hours configuration

  - Restaurant status (open/closed)

- Order System

  - Cart functionality

  - Order placement and tracking

  - Order status updates (Pending, Preparing, Delivered)

  - Order history for customers, with status filters

- Rating and Reviews

  - Restaurant ratings and reviews

  - Menu item ratings

  - Average rating calculations

- Search Functionality

  - Search restaurants by name/location

  - Search menu items by name/cuisine/category

## Setup

### Prerequisites

- Python 3.9+

- pip

- virtualenv (recommended)

### Installation

1. Create and activate virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` in the root directory:

```ini
SECRET_KEY=your-secure-secret-key
DATABASE_URI=sqlite:///app.db
TEST_DATABASE_URI=sqlite:///:memory:  # (for testing)
```

### Database Setup

1. Initialize the database:

```bash
flask db upgrade
```

2. Seed sample data

```bash
python seed.py
```

### Running the Application

Start the development server:

```bash
flask run
```

The application will be available at http://localhost:5000

## Project Structure

```
justeat/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Extensions: login, migrate etc
│   ├── loggin_config.py     # Logging configurations
│   │
│   ├── blueprints/          # App blueprints
│   │   ├── auth/            # Authentication Forms & Routes
│   │   ├── customer/        # Customer Forms & Routes
│   │   └── restaurants/     # Restaurant Forms & Routes
│   |
│   ├── decorators/          # Decorators for routes
│   ├── models/              # Database models
│   ├── services/            # Business logic services
│   ├── templates/           # Jinja2 templates
│   └── static/              # Static files (CSS, JS, images)
│
├── migrations/              # Database migration scripts
├── tests/                   # Test cases
├── .env.sample              # Sample env
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## Credentials
Restaurant Owner:
- Email: `mario@example.com`  Password: `password`
- Email: `luigi@example.com`  Password: `password`

Customer:
- Email: `john@example.com`  Password: `password`
- Email: `jane@example.com`  Password: `password`


## Testing

To run the suite:

```bash
pytest -v
```
