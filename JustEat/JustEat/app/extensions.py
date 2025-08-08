from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()

# Setup LoginManager
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"
