import os
import logging
from flask import Flask

from .config import Config
from .extensions import db, migrate
from .models import Book


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "developpment")
    
    print(f"Current Environment: {env}")
    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
        logging.basicConfig(level=logging.INFO)
    else:
        app.config.from_object("app.config.DevelopmentConfig")
        logging.basicConfig(level=logging.DEBUG)


    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    from .book import bp as book_bp

    app.register_blueprint(book_bp, url_prefix="/books")

    return app


app = create_app()
