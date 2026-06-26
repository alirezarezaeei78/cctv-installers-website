\# NasabDoorbin



NasabDoorbin is a Persian CCTV installation marketplace built with a Django backend and React frontend.



The platform helps customers submit CCTV installation requests, compare installer profiles, and manage service requests through a trust-focused marketplace structure.



\## Features



\- Persian RTL user interface

\- React frontend

\- Django backend

\- Django REST Framework API

\- Django admin panel

\- Customer and installer registration

\- Installer profile listing

\- Multi-step CCTV installation request form

\- Service request management

\- Quote model and API structure

\- SEO-focused homepage structure

\- Custom CSS and UI animations



\## Tech Stack



\### Backend



\- Python

\- Django

\- Django REST Framework

\- SQLite

\- Django Admin



\### Frontend



\- React

\- React Router

\- Axios

\- Bootstrap

\- Custom CSS

\- RTL Persian layout



\## Project Structure



cctv\_marketplace/

\- backend/

\- frontend/

\- README.md



\## Backend Setup



Go to the backend folder:



cd C:\\Users\\Rezaei\\Desktop\\cctv\_marketplace\\backend



Install dependencies:



C:\\Users\\Rezaei\\Desktop\\relbench\\.conda\\python.exe -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers



Run migrations:



C:\\Users\\Rezaei\\Desktop\\relbench\\.conda\\python.exe manage.py makemigrations

C:\\Users\\Rezaei\\Desktop\\relbench\\.conda\\python.exe manage.py migrate



Run backend:



C:\\Users\\Rezaei\\Desktop\\relbench\\.conda\\python.exe manage.py runserver



Backend URLs:



http://127.0.0.1:8000/admin/

http://127.0.0.1:8000/api/



\## Frontend Setup



Open another PowerShell window:



cd C:\\Users\\Rezaei\\Desktop\\cctv\_marketplace\\frontend



Install packages:



npm install

npm install react-scripts@5.0.1 --save



Run frontend:



npm start



Frontend URL:



http://localhost:3000



\## Main Pages



\- / : Homepage

\- /installers : Installer directory

\- /request : Multi-step CCTV installation request form

\- /register : Customer / installer registration

\- /login : User login



\## GitHub



To push changes:



git add .

git commit -m "Update project"

git push



\## License



This project is private and currently has no public license.

