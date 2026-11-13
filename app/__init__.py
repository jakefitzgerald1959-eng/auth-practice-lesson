from pathlib import Path

from flask import Flask
from .db import close_db, init_db
from .auth import bp as auth_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.teardown_appcontext
    def _close_db(exception):
        close_db(exception)

    # Initialize DB inside app context
    with app.app_context():
        init_db()

    # Register auth routes (including /register)
    app.register_blueprint(auth_bp)

    return app