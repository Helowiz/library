import os

from flask import Flask

from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.book import bp as book_bp

    app.register_blueprint(book_bp, url_prefix="/book")

    @app.route("/routes")
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule}")
        return "<br>".join(routes)

    return app


app = create_app()
