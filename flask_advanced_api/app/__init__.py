from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Flask-Limiter can help rate-limit API requests to protect against abuse.
limiter = Limiter(
    get_remote_address,
    app=None,
    default_limits=["200 per day", "50 per hour"]
)



# Create the database object
db = SQLAlchemy()

# Create the migration object
migrate = Migrate()

# Create the CSRF object
csrf  = CSRFProtect()


# Create the JWT object
jwt = JWTManager()


# Create the mail object
mail = Mail()


# Create the app factory function and initialize the app with the configuration that we have defined in the Config class.
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    # Initialize the database object
    db.init_app(app)

    # Initialize the migration object
    migrate.init_app(app, db)

    # Initialize the CSRF object
    # This will automatically protect all forms and requests in your application. Make sure your forms include the CSRF token.
    csrf.init_app(app)

    # Initialize the JWT object
    jwt.init_app(app)

    # Initialize the mail object
    mail.init_app(app)

    # Initialize the limiter object
    limiter.init_app(app)


    # Import the blueprints
    from app import routes
    csrf.exempt(routes.bp) 
    app.register_blueprint(routes.bp)


    return app