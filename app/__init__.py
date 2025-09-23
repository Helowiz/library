import os

from flask import Flask

from .config import Config
from .extensions import db, migrate
from .models import Book


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")

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
