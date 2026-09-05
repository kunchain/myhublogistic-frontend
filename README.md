# Myhublogistic Frontend

Simple static frontend for a logistics management app (shipments, invoices, admin controls).

## Pages

- `index.html` – Landing page
- `login.html` – Login (redirects to admin or client dashboard by role)
- `admin-users.html` – Admin user management (create/edit/delete users)
- `admin-shipments.html` – Admin shipment management (list/create/edit)
- `admin-invoices.html` – Admin invoice management (list/create/edit)
- `admin-db-view.html` – Admin database viewer (inspect tables)
- `client-dashboard.html` – Client dashboard (shipments, invoices, profile)
- `client-create-shipment.html` – Client page to create a new shipment

## API integration

Configure `API_BASE_URL` in `assets/app.js` to point to your backend, e.g.:

```js
const API_BASE_URL = "https://api.myhublogistic.com";
```

Expected endpoints (non-exhaustive):

- Auth
  - `POST /auth/login`
- Admin
  - `GET /admin/users`, `POST /admin/users`, `PUT /admin/users/:id`, `DELETE /admin/users/:id`
  - `GET /admin/shipments`, `POST /admin/shipments`, `PUT /admin/shipments/:id`
  - `GET /admin/invoices`, `POST /admin/invoices`, `PUT /admin/invoices/:id`
  - `GET /admin/db/:table`
- Client
  - `GET /client/shipments`
  - `POST /client/shipments` (for client-create-shipment.html)
  - `GET /client/invoices`
  - `PUT /client/profile`

## Local development

1. Clone the repo:
   ```bash
   git clone https://github.com/kunchain/myhublogistic-frontend.git
   cd myhublogistic-frontend
   ```

2. Set `API_BASE_URL` in `assets/app.js` to your local or staging backend.

3. Serve the static files, e.g.:
   ```bash
   python -m http.server 8080
   ```
   Then open `http://localhost:8080`.

## Deploy

This is a static site; you can deploy it as-is.

### Netlify

1. Create a new site in Netlify and connect this GitHub repo.
2. Build settings:
   - Build command: (leave empty)
   - Publish directory: `.` (root)
3. Add environment variables if needed (e.g. via a small config file or build script).

### Vercel

1. Import this repo into Vercel.
2. Framework preset: "Other".
3. Root directory: `.`
4. Deploy.

### GitHub Pages

1. Go to repo Settings → Pages.
2. Source: deploy from `main` branch, folder: `/ (root)`.
3. Save and wait for the site to publish at `https://<user>.github.io/myhublogistic-frontend/`.

After deploying, make sure `API_BASE_URL` in `assets/app.js` points to your production backend and that CORS is configured appropriately.

## Usage

- **Admin**
  - Log in with an admin account (e.g. `admin@myhublogistic.com` / `Admin@1234` if using the default seed).
  - Manage users, shipments, invoices, and inspect DB tables via the admin nav.

- **Client**
  - Log in with a client account.
  - View shipments and invoices, edit profile, and create new shipments from the client dashboard.

## License

MIT
