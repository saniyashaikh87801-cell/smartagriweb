import sqlite3
import os
from flask import g, current_app

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Create tables if they don't exist."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "smartagri.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    sql_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
    conn = sqlite3.connect(db_path)
    with open(sql_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("[OK] Database initialized.")

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid
