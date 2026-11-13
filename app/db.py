import sqlite3
from pathlib import Path

from flask import g, current_app


def get_db():
    if "db" not in g:
        # Use instance_path from the current app *inside* the request/app context
        db_path = Path(current_app.instance_path) / "app.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)

        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
    )
    db.commit()