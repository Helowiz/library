import os
from flask import Flask, request
from config import Config
from app.extensions import db
import json

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.book import bp as book_bp
    app.register_blueprint(book_bp, url_prefix='/book')

    @app.route('/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule}")
        return "<br>".join(routes)
    
    @app.route('/plus_one')
    def plus_one():
        x = int(request.args.get('x', 1))
        return json.dumps({'x': x + 1})

    return app

if __name__ == '__main__':
    create_app.run()