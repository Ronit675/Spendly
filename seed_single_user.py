import random
from datetime import datetime
from werkzeug.security import generate_password_hash
from database.db import get_db

def generate_indian_user():
    first_names = [
        "Aarav", "Vihaan", "Aditya", "Arjun", "Sai", "Ishaan", "Rahul", "Ananya",
        "Diya", "Myra", "Saanvi", "Priya", "Kavya", "Zara", "Ishani", "Rohan",
        "Amit", "Sneha", "Vikram", "Deepika"
    ]
    last_names = [
        "Sharma", "Verma", "Gupta", "Malhotra", "Kapoor", "Singh", "Iyer",
        "Reddy", "Patel", "Chatterjee", "Nair", "Kulkarni", "Joshi", "Mehta", "Das"
    ]

    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"

    # Generate email: first.last[2-3 digits]@gmail.com
    email_suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{email_suffix}@gmail.com"

    return {
        "name": full_name,
        "email": email,
        "password_hash": generate_password_hash("password123", method='pbkdf2:sha256')
    }

def seed_user():
    while True:
        user_data = generate_indian_user()

        with get_db() as conn:
            # Check if email exists
            exists = conn.execute("SELECT id FROM users WHERE email = ?", (user_data["email"],)).fetchone()
            if not exists:
                # Insert user
                cursor = conn.execute(
                    "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (user_data["name"], user_data["email"], user_data["password_hash"], datetime.now().isoformat())
                )
                conn.commit()

                user_id = cursor.lastrowid
                print(f"Successfully seeded user:")
                print(f"ID: {user_id}")
                print(f"Name: {user_data['name']}")
                print(f"Email: {user_data['email']}")
                return

if __name__ == "__main__":
    seed_user()
