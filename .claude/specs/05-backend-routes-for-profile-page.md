# Spec: Backend Routes for Profile Page

## Overview
This feature replaces the hardcoded mock data in the `/profile` route with real data fetched from the SQLite database. It ensures that the logged-in user sees their actual profile information, spending statistics, and transaction history.

## Depends on
- Step 1: Database Setup (Users and Expenses tables)
- Step 2: Registration
- Step 3: Login and Logout

## Routes
- `GET /profile` — Fetches and displays the logged-in user's profile data, summary statistics, and expense history — access level (logged-in)

## Database changes
No database changes.

## Templates
- **Create:** No new templates.
- **Modify:** `templates/profile.html` — update to ensure it handles the dynamic data structure coming from the backend.

## Files to change
- `app.py` — update the `/profile` route to call DB helper functions.
- `database/db.py` — add helper functions to fetch user profile, total spending, category breakdowns, and transactions.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic must reside in `database/db.py`, not in `app.py`

## Definition of done
- [ ] User can log in and see their actual name and email on the profile page.
- [ ] Total spent and transaction count are calculated correctly based on the user's expenses in the DB.
- [ ] The transaction list shows only the expenses belonging to the logged-in user.
- [ ] Category-wise spending breakdown is accurately calculated from the database.
- [ ] Accessing `/profile` without being logged in redirects to the login page.
