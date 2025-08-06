import os

# Base configuration class with common settings
class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "not so secure key")
    # Disable SQLAlchemy event system for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Configuration for development environment
class DevelopmentConfig(Config):
    DEBUG = True  # Enable debug mode for development
    # Use environment variable or fallback to local SQLite DB
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI") or "sqlite:///just_eat.dev.db"
    )


# Configuration for production environment
class ProductionConfig(Config):
    DEBUG = False  # Disable debug mode in production
    # Use production database URI or fallback to production SQLite DB
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///just_eat.prod.db"
    )


# Configuration for testing environment
class TestingConfig(Config):
    TESTING = True  # Enable testing mode (affects behavior of some Flask extensions)
    # Use in-memory SQLite DB for fast, isolated test runs
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URI") or "sqlite:///:memory:"
    )
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing forms easily


# Dictionary to map config names to config classes
configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
