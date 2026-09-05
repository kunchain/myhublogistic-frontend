# Myhublogistic Frontend

Simple static frontend for a logistics management app (shipments, invoices, admin controls).

## Pages

- `index.html` – Landing page
- `login.html` – Login (redirects to admin or client dashboard by role)
- `admin-users.html` – Admin user management (create/edit/delete users)
- `admin-db-view.html` – Admin database viewer (inspect tables)
- `client-dashboard.html` – Client dashboard (shipments, invoices, profile)

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/kunchain/myhublogistic-frontend.git
   cd myhublogistic-frontend
   ```

2. Configure the API base URL in `assets/app.js`:
   - Set `API_BASE_URL` to your backend (e.g. `https://api.myhublogistic.com`).
   - Ensure the backend implements the expected endpoints:
     - `POST /auth/login`
     - `GET /admin/users`, `POST /admin/users`, `PUT /admin/users/:id`, `DELETE /admin/users/:id`
     - `GET /admin/db/:table`
     - `GET /client/shipments`, `GET /client/invoices`, `PUT /client/profile`

3. Serve the static files (any static server, e.g.):
   ```bash
   # Using Python
   python -m http.server 8080
   ```
   Then open `http://localhost:8080` in your browser.

## Usage

- **Admin**
  - Log in with an admin account (e.g. `admin@myhublogistic.com` / `Admin@1234` if using the default seed).
  - Manage users at `admin-users.html`.
  - Inspect database tables at `admin-db-view.html`.

- **Client**
  - Log in with a client account.
  - View shipments and invoices, and edit profile at `client-dashboard.html`.

## License

MIT
