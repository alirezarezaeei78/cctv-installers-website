# NasabDoorbin

A Persian CCTV installation marketplace with a **Django REST Framework backend** and **React frontend**.

The application supports customer installation requests, installer profiles, registration, and service-request management through a Persian RTL interface.

## Application structure

| Path | Purpose |
| --- | --- |
| `backend/config/` | Django project configuration |
| `backend/core/` | Application models, API, and service logic |
| `backend/manage.py` | Django management entry point |
| `frontend/src/` | React pages, components, and styling |
| `frontend/public/` | Frontend static assets |

## Development setup

Use Python, Node.js, and npm. Create and activate a Python virtual environment before installing backend packages.

From `backend/`:

```sh
python -m pip install -r requirements.txt
python manage.py test
python manage.py migrate
python manage.py runserver
```

The requirements specify compatible minor-version ranges. Django administration is available at `http://127.0.0.1:8000/admin/` and the API at `http://127.0.0.1:8000/api/`.

Session-based forms obtain a CSRF cookie from `GET /api/csrf/` and send `X-CSRFToken` on writes. The frontend configures Axios for this automatically. See [Django's AJAX CSRF documentation](https://docs.djangoproject.com/en/5.2/howto/csrf/).

Customers create and view their own requests. Signed-in installers can browse requests and submit positive-price quotes for open jobs. Quotes are visible to the customer and their quoting installer; clients cannot mark a quote accepted during creation. Registration validates roles, passwords, and unique usernames.

For deployment, set `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ALLOWED_ORIGINS`, and `DJANGO_CSRF_TRUSTED_ORIGINS` in the process environment. Secure cookies are enabled when debug is off. Configure HTTPS and protected media storage before serving customer uploads.

In a second terminal, from `frontend/`:

```sh
npm ci
npm start
```

The development frontend runs at `http://localhost:3000` and proxies API requests to `http://localhost:8000`.

Use Node.js 20 or newer for the frontend. Axios and React Router have been updated, and the npm lockfile includes compatible dependency fixes. The frontend still uses Create React App 5; its dependency audit retains findings in the legacy build/test toolchain. Plan a build-system migration and deployment review before a production release. `npm run build` has been checked, but it does not establish production security.

## Main routes

- `/` — homepage
- `/installers` — installer directory
- `/request` — installation-request form
- `/register` — customer and installer registration
- `/login` — account login

## Development scope

This is a private development repository. Validate authentication, service workflows, database configuration, and deployment settings before using it in production. Keep local credentials and customer information outside source control.
