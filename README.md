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
python -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
python manage.py migrate
python manage.py runserver
```

The backend currently has no dependency lockfile. Review its configuration and dependency compatibility for your environment. Django administration is available at `http://127.0.0.1:8000/admin/` and the API at `http://127.0.0.1:8000/api/`.

In a second terminal, from `frontend/`:

```sh
npm ci
npm start
```

The development frontend runs at `http://localhost:3000` and proxies API requests to `http://localhost:8000`.

## Main routes

- `/` — homepage
- `/installers` — installer directory
- `/request` — installation-request form
- `/register` — customer and installer registration
- `/login` — account login

## Development scope

This is a private development repository. Validate authentication, service workflows, database configuration, and deployment settings before using it in production. Keep local credentials and customer information outside source control.
