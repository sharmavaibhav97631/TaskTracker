# Mini Project & Task Tracker (Django)

This project is a Django-based application for tracking projects and tasks for multiple users.  
It follows Django best practices, uses PostgreSQL, and implements all requirements specified in the assignment.

---

## Tech Stack
- Python 3
- Django (LTS / Django 6)
- PostgreSQL
- Django ORM (no raw SQL)
- Session-based authentication

---

## How to Run the Project

1. Activate Virtual Environment
```bash
source venv/bin/activate

1.2 Install all requirements
pip install -m requirements.txt

2. Run Migrations
python manage.py makemigrations
python manage.py migrate

3. Start the Development Server
python manage.py runserver

Open the application in browser:
http://127.0.0.1:8000/

How to Create a Test User
user registration is not required, users are created via Django admin.

Create Superuser
python manage.py createsuperuser

Then log in at:
http://127.0.0.1:8000/admin/login/

Use this account to access:
/projects/
/dashboard/
/tasks/

Data Modeling (High Level)

Project
    Each project belongs to a single user (owner).
    Project names are unique per user using a database constraint.
Task
    Each task belongs to a project.
    Tasks support priority, status, due date, and optional assignee.
    Business rules are enforced at the model level (validation).    

Authentication & Access Protection

Uses Django’s built-in session authentication.
All views are protected with @login_required.
Users can only:
    View their own projects
    View tasks from their own projects or tasks assigned to them
Task creation inside a project is restricted to the project owner.

Dashboard Implementation
The dashboard is implemented using Django ORM aggregation functions.
Uses annotate() and Count() to calculate:
    Total projects
    Total tasks
    Task count grouped by status
Upcoming tasks are fetched using filtered and ordered ORM queries.
NOTE: I have implemented the dashboard using ORM aggregation, not manual Python loops.

Tests
Run unit tests using:
python manage.py test tracker

The test suite verifies:
    Duplicate project name restriction per user
    Task validation rules (done task cannot have future due date)
    Task visibility and access control