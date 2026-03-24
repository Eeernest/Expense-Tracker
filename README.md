# Expense-Tracker

Simple REST API for tracking expenses, accessible via Swagger UI.

## Features

### User Management

#### General User
- Register a new account

#### Admin
- View all users (with pagination and filtering through roles)
- Change user role
- Activate or deactivate user account
- Delete user

### Authentication & Authorization
- Secure login with JWT authentication
- Role based access control (user / admin)

### Expense Management

#### General User
- Add a new expense
- Edit an existing expense
- Delete an existing expense
- View all expenses
- Filter expenses by category and date range
- Calculate sum of expenses within a selected period

#### Admin
- View all user expenses
- View selected user expenses
- Pagination and filtering support

## Installation
1. Clone the repository

```bash
git clone https://github.com/Eeernest/expense-tracker.git
cd expense-tracker
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


4. Start PostgreSQL with Docker:

```bash
docker run --name expense-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=expense_db \
  -p 5432:5432 \
  -d postgres
```

5. Create an .env file in the project root:

```env
# Database configuration
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# FastAPI / JWT configuration
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin credentials (for initial setup)
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password
```

> Do not commit real credentials. Replace all values with your own before running the application.


6. Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

7. Testing
Run tests with:

```bash
pytest
```

## Docs
- API docs available at http://127.0.0.1:8000/docs

## Tech Stack
- Python 3.14.2
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Docker

## Project Structure
- app/
  - routers/ API endpoints
  - dependencies/ dependency injections
  - services/ business logic
  - repositories/ database operations
  - schemas/ Pydantic schemas
  - models/ database models
  - db/ database setup
  - core/ config, security and middleware

- tests/
  - services/ unit tests
  - repositories/ integration tests
  - fixtures/ fixtures for all of the tests