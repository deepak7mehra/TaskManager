# Task Manager API

A RESTful API built with **Django** and **Django REST Framework** for managing tasks.

## Features
* **User Authentication:** JWT-based login and registration.
* **CRUD Operations:** Create, Read, Update, and Delete tasks.
* **Role-Based Access:** Admins can see all tasks; regular users see only their own.
* **Filtering:** Filter tasks by `completed` status.
* **Pagination:** Dynamic page sizes supported via `?page_size=X`.
* **API Documentation:** Interactive Swagger UI available.

## Setup Instructions
1. **Clone the repo:** `git clone https://github.com/deepak7mehra/TaskManager.git`
2. **Create Virtual Env:** `python -m venv venv`
3. **Activate Env:** `source venv/bin/activate`
4. **Install Deps:** `pip install -r requirements.txt`
5. **Migrate DB:** `python manage.py migrate`
6. **Run Server:** `python manage.py runserver`

## API Documentation
Once the server is running, visit:
* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`

## Testing
Run the automated test suite:
`python manage.py test`