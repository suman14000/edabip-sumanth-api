# EDABIP - Reports Backend API

## Tech Stack

- Python
- FastAPI
- SQL
- MySQL


### Day 1 - Database Design

- Created the `edabip-sumanth-api` GitHub repository.
- Cloned the repository and set up the project in VS Code.
- Designed the database structure for the Reports module.
- Created the SQL schema and required tables.
- Added realistic seed data with 30+ sample reports.
- Added report types: Scheduled and On Demand.
- Added report statuses: Completed, Failed and Scheduled.

### Day 2 - FastAPI APIs

- Set up the FastAPI backend.
- Created APIs for the Reports module.
- Implemented Reports Summary API.
- Implemented Report Type Distribution API.
- Implemented Reports by Status API.
- Implemented Recent Reports API.
- Implemented Top Report Templates API.
- Implemented Recent Activity API.
- Added search, status filtering and pagination for Recent Activity.
- Added report re-run/status update functionality.
- Added input validation and basic error handling.
- Tested the APIs using Swagger UI.


Task 2

# EDABIP Reports Management API

## Project Description
EDABIP Reports Management API is a backend application developed using
Python, FastAPI, SQLAlchemy, and MySQL.

It manages reports, report templates, report activity, users, and
report schedules.

## Technologies Used
- Python
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Bcrypt Password Hashing
- Pydantic
- Pytest

## Features
- User registration and login
- JWT-based authentication
- Admin and Viewer roles
- Report management
- Report templates
- Report activity tracking
- Daily, Weekly, and Monthly schedules
- CSV export of recent activity
- Search, sorting, and date filters
- Report summary and status distribution
- Automated API testing

## Database Tables
1. users
2. reports
3. report_templates
4. report_activity
5. report_schedules

## Authentication
1. Register using the registration API.
2. Log in to receive a JWT access token.
3. Use the token to access protected endpoints.
4. Viewers can read reports.
5. Admins can create, update, rerun, and delete reports.

## Run the Project

Install dependencies:

    pip install -r requirements.txt

Start the server:

    uvicorn app.main:app --reload

Open Swagger documentation:

    http://127.0.0.1:8000/docs

## Run Tests

    pytest -v

## ER Diagram

See the database relationships below.

- One report template can have many reports.
- One report can have many activity records.
- One report can have many schedules.
- Users authenticate to access the API.
## ER Diagram

```text
+---------------------------+
|      REPORT_TEMPLATES     |
+---------------------------+
| PK  id                    |
|     template_name         |
|     module                |
|     created_by            |
|     created_at            |
+---------------------------+
              |
              | 1
              |
              |------< Many
              |
+---------------------------+
|          REPORTS          |
+---------------------------+
| PK  id                    |
| FK  template_id           |
|     report_name           |
|     module                |
|     report_type           |
|     owner                 |
|     status                |
|     created_at            |
|     last_run              |
|     run_time              |
+---------------------------+
        |              |
        | 1            | 1
        |              |
        v              v
+------------------+  +----------------------+
| REPORT_ACTIVITY  |  |   REPORT_SCHEDULES   |
+------------------+  +----------------------+
| PK  id           |  | PK  id               |
| FK  report_id    |  | FK  report_id        |
|     activity_type|  |     frequency        |
|     message      |  |     next_run         |
|     status       |  |     active           |
|     created_at   |  |     created_at       |
+------------------+  +----------------------+

+---------------------------+
|           USERS           |
+---------------------------+
| PK  id                    |
|     name                  |
| UK  email                 |
|     hashed_password       |
|     role                  |
|     created_at            |
+---------------------------+