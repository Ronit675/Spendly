import sqlite3
import random
from datetime import datetime, timedelta
from database.db import get_db

def seed_expenses(user_id, count, months):
    categories_data = {
        "Food": {"range": (50, 800), "weight": 30, "desc": ["Lunch at local dhaba", "Dinner with family", "Groceries from Blinkit", "Street food", "Cafe coffee", "Vegetable market"]},
        "Transport": {"range": (20, 500), "weight": 20, "desc": ["Auto rickshaw", "Uber ride", "Petrol refill", "Metro recharge", "Bus fare"]},
        "Bills": {"range": (200, 3000), "weight": 15, "desc": ["Electricity bill", "Water bill", "Mobile recharge", "Broadband bill", "Gas cylinder"]},
        "Health": {"range": (100, 2000), "weight": 10, "desc": ["Pharmacy medicines", "Doctor consultation", "Lab test", "Health supplement"]},
        "Entertainment": {"range": (100, 1500), "weight": 10, "desc": ["Movie ticket", "OTT subscription", "Gaming zone", "Bowling"]},
        "Shopping": {"range": (200, 5000), "weight": 10, "desc": ["Amazon order", "New clothes", "Electronics", "Footwear", "Gift for friend"]},
        "Other": {"range": (50, 1000), "weight": 5, "desc": ["Miscellaneous", "Donation", "Courier charges", "Parking fee"]}
    }

    categories = list(categories_data.keys())
    weights = [categories_data[cat]["weight"] for cat in categories]

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)

    expenses_to_insert = []

    for _ in range(count):
        category = random.choices(categories, weights=weights)[0]
        cat_info = categories_data[category]

        amount = round(random.uniform(*cat_info["range"]), 2)
        description = random.choice(cat_info["desc"])

        # Random date within the range
        days_diff = (end_date - start_date).days
        random_days = random.randint(0, days_diff)
        date_val = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

        expenses_to_insert.append((user_id, amount, category, date_val, description))

    try:
        conn = get_db()
        with conn: # Transaction
            conn.executemany(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                expenses_to_insert
            )

        # Determine actual date range of inserted data
        dates = [e[3] for e in expenses_to_insert]
        print(f"Successfully inserted {len(expenses_to_insert)} expenses.")
        print(f"Date range: {min(dates)} to {max(dates)}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        exit(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python seed_expenses.py <user_id> <count> <months>")
        sys.exit(1)

    try:
        u_id = int(sys.argv[1])
        cnt = int(sys.argv[2])
        mths = int(sys.argv[3])
        seed_expenses(u_id, cnt, mths)
    except ValueError:
        print("All arguments must be integers.")
        sys.exit(1)
