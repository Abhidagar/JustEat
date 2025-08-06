from flask import Flask
from flask_login import current_user

from app.blueprints import auth_bp, customer_bp, restaurant_bp
from app.config import configs
from app.extensions import csrf, db, login_manager, migrate, moment
from app.logging_config import setup_logging

# Import services to register decorators
from app.services import auth_service  # This registers the user_loader


def create_app(config: str = "development") -> Flask:
    app = Flask(__name__)

    # use development config as default
    app.config.from_object(configs.get(config))

    # Initialize extensions
    initialize_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Setup logging
    setup_logging(app)

    return app


def initialize_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions.

    Args:
        app (Flask): The Flask application instance.
    """
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)


def register_blueprints(app: Flask) -> None:
    """
    Register Flask blueprints.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
