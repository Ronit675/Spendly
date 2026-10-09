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

def get_user_profile(user_id):
    """
    Fetches basic profile information for a user.
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        if row:
            return {
                "name": row["name"],
                "email": row["email"],
                "member_since": row["created_at"][:7] + " " + row["created_at"][8:11] # Simplified date
            }
        return None

def get_user_stats(user_id):
    """
    Calculates total spending and identifies the top category.
    """
    with get_db() as conn:
        totals = conn.execute(
            "SELECT SUM(amount) as total, COUNT(id) as count FROM expenses WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        top_cat = conn.execute(
            "SELECT category FROM expenses WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            (user_id,)
        ).fetchone()

        return {
            "total_spent": totals["total"] if totals["total"] else 0,
            "transaction_count": totals["count"] if totals["count"] else 0,
            "top_category": top_cat["category"] if top_cat else "N/A"
        }

def get_user_transactions(user_id):
    """
    Fetches the most recent expenses for a user.
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT date, description, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 10",
            (user_id,)
        ).fetchall()

        return [
            {
                "date": row["date"],
                "description": row["description"],
                "category": row["category"],
                "amount": f"-₹{row['amount']:.2f}"
            }
            for row in rows
        ]

def get_category_breakdown(user_id):
    """
    Aggregates spending per category and calculates percentages.
    """
    with get_db() as conn:
        total_row = conn.execute(
            "SELECT SUM(amount) as total FROM expenses WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        total_sum = total_row["total"] if total_row["total"] else 0

        categories = conn.execute(
            "SELECT category, SUM(amount) as amount FROM expenses WHERE user_id = ? GROUP BY category",
            (user_id,)
        ).fetchall()

        breakdown = []
        for row in categories:
            percentage = (row["amount"] / total_sum * 100) if total_sum > 0 else 0
            breakdown.append({
                "name": row["category"],
                "amount": f"₹{row['amount']:.2f}",
                "percentage": round(percentage, 2)
            })
        return breakdown
