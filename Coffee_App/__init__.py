from flask import Flask, redirect, url_for

from Coffee_App.config import Config
from Coffee_App.database import get_db, init_app
from Coffee_App.routes.auth import auth_bp
from Coffee_App.routes.posts import posts_bp
from Coffee_App.routes.users import users_bp
from Coffee_App.routes.search import search_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(search_bp)

    @app.route("/")
    def index():
        return redirect(url_for("posts.timeline"))

    @app.route("/db-test")
    def db_test():
        try:
            connection = get_db()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return "Database connection successful!"
        except Exception as e:
            return f"Database connection failed: {e}", 500

    return app
