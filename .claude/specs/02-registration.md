---
# Spec: Registration

## Overview
This feature implements the user registration flow, allowing new users to create an account with their name, email, and password. This is a foundational step in the Spendly roadmap, enabling personalized expense tracking by associating data with specific user accounts.

## Depends on
- Step 1: Database Setup

## Routes
- `GET /register` — Displays the registration form — public
- `POST /register` — Processes the registration form and creates a new user — public

## Database changes
No database changes. The `users` table already contains the necessary fields: `name`, `email`, and `password_hash`.

## Templates
- **Modify:** `templates/register.html` — Update the stub template to be a functional HTML form that posts to `/register`.

## Files to change
- `app.py` — Implement the `POST /register` route handler.
- `database/db.py` — Add a helper function to create a new user.
- `templates/register.html` — Implement the registration form.

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
- Validate that the email is not already registered before inserting.
- Redirect to `/login` with a success message upon successful registration.

## Definition of done
- [ ] A user can fill out the registration form and successfully create an account.
- [ ] Passwords are stored as hashes in the database, not plain text.
- [ ] Attempting to register with an existing email results in an appropriate error message.
- [ ] Successful registration redirects the user to the login page.
- [ ] The registration form validates for required fields (name, email, password).
---
