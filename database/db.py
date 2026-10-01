import sqlite3
from werkzeug.security import generate_password_hash  # type: ignore[import-not-found]

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

def seed_db():
    """
    Inserts demo data if the users table is empty.
    Prevents duplicate inserts on repeated runs.
    """
    with get_db() as conn:
        # Check if users table already contains data
        user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
        if user:
            return

        # Insert demo user
        demo_user_data = {
            "name": "Demo User",
            "email": "demo@spendly.com",
            "password_hash": generate_password_hash("demo123", method='pbkdf2:sha256')
        }

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (demo_user_data["name"], demo_user_data["email"], demo_user_data["password_hash"])
        )
        user_id = cursor.lastrowid

        # Define sample expenses covering all categories
        categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]
        sample_expenses = [
            (user_id, 12.50, "Food", "2026-09-25", "Lunch at Cafe"),
            (user_id, 45.00, "Transport", "2026-09-26", "Gas refill"),
            (user_id, 120.00, "Bills", "2026-09-27", "Internet bill"),
            (user_id, 30.00, "Health", "2026-09-28", "Pharmacy"),
            (user_id, 15.00, "Entertainment", "2026-09-29", "Movie ticket"),
            (user_id, 65.20, "Shopping", "2026-09-30", "New shirt"),
            (user_id, 10.00, "Other", "2026-10-01", "Misc"),
            (user_id, 22.00, "Food", "2026-10-01", "Dinner"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
        conn.commit()
