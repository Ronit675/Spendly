import sqlite3
from werkzeug.security import generate_password_hash  

DB_PATH = "spendly.db"

def get_db():
    """
    Opens a connection to the SQLite database.
    Sets row_factory to sqlite3.Row for dictionary-like access
    and enables foreign key constraints.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates the users and expenses tables if they do not already exist.
    """
    with get_db() as conn:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create expenses table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

def create_user(name, email, password_hash):
    """
    Creates a new user in the users table.
    Returns the ID of the new user.
    """
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        return cursor.lastrowid

def get_user_by_email(email):
    """
    Fetches a user from the users table by their email.
    Returns the user row if found, otherwise None.
    """
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

