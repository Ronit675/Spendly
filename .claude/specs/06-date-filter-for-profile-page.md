# Spec: Date Filter for Profile Page

## Overview
This feature introduces a date range filter to the user's profile page, allowing users to filter their transaction history and summary statistics by a specific time period. This enhances the utility of the profile page from a static overview to a functional reporting tool.

## Depends on
- 04-profile-page (The profile page must be implemented)

## Routes
- `GET /profile` — Modify existing route to handle optional `start_date` and `end_date` query parameters. Access level: logged-in.

## Database changes
No database changes. The filter will be applied to queries against the existing `expenses` table.

## Templates
- **Modify:** `templates/profile.html` — Add a date filter form (start date and end date inputs) and ensure the filtered results are displayed.

## Files to change
- `app.py` — Update the `/profile` route to process query parameters and call the appropriate DB helper.
- `database/db.py` — Add a new helper function `get_expenses_by_user_and_date(user_id, start_date, end_date)` to fetch filtered transactions.
- `templates/profile.html` — Add the filter UI.

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
- Date parameters should be validated to ensure they are in a correct ISO format (YYYY-MM-DD) before being passed to the database.

## Definition of done
- [ ] The profile page displays a date range filter (Start Date and End Date).
- [ ] Submitting the filter updates the transaction list to show only expenses within that range.
- [ ] The summary statistics (Total Spent, Transaction Count) update to reflect the filtered range.
- [ ] If no dates are provided, the page defaults to showing all transactions for the user.
- [ ] The application does not crash when invalid date formats are provided in the URL.
