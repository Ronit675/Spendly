---
# Spec: Login and Logout

## Overview
This feature implements the authentication mechanism for Spendly. It allows registered users to authenticate via their email and password, establishing a secure session that grants access to protected routes (like the profile page). It also provides a way to terminate this session securely.

## Depends on
- 01-database-setup
- 02-registration

## Routes
- `GET /login` — Renders the login form — public
- `POST /login` — Authenticates user and starts session — public
- `GET /logout` — Terminates session and redirects to landing — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `login.html` — Ensure form uses POST method and correct field names.
- **Modify:** `base.html` — Add conditional navigation links (e.g., show "Login/Register" when logged out, "Logout/Profile" when logged in).

## Files to change
- `app.py` — Implementation of login/logout logic and session management.
- `database/db.py` — Addition of a helper function to fetch user by email.
- `templates/base.html` — Navigation updates.
- `templates/login.html` — Form updates.

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
- Use `flask.session` for session management

## Definition of done
- [ ] User can log in with valid email and password.
- [ ] User is redirected to a protected page (e.g., `/profile`) after successful login.
- [ ] User receives an error message upon providing incorrect credentials.
- [ ] User is prevented from accessing `/profile` if not logged in.
- [ ] User is successfully logged out via `/logout` and cannot access protected routes thereafter.
- [ ] Navigation bar correctly reflects the user's authentication state.
---
