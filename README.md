# 🛒 Mini E-Commerce Backend (FastAPI + PostgreSQL)

A simple backend for an e-commerce application built with **FastAPI**,
**SQLAlchemy**, and **PostgreSQL**.\
Includes authentication (JWT), user management, product management, cart
system, and order workflow.

------------------------------------------------------------------------

## 🚀 Features

-   User registration & login (JWT-based authentication)
-   Product CRUD (create, list, stock management)
-   Shopping cart with quantity increment/decrement
-   Order creation with stock checks
-   Alembic migrations for database schema
-   Unit tests with pytest & SQLite in-memory DB

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   [FastAPI](https://fastapi.tiangolo.com/)\
-   [SQLAlchemy](https://www.sqlalchemy.org/) ORM\
-   [PostgreSQL](https://www.postgresql.org/)\
-   [Alembic](https://alembic.sqlalchemy.org/) for migrations\
-   [Pydantic](https://docs.pydantic.dev/) for schema validation\
-   [Pytest](https://docs.pytest.org/) for testing

------------------------------------------------------------------------

## ⚙️ Setup & Installation

### 1. Clone the repo

``` bash
git clone https://github.com/TTanoz/mini-e-commerce.git
cd mini-e-commerce
```

### 2. Create virtual environment

``` bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the project root:

    DATABASE_URL=postgresql+psycopg2://postgres:<password>@localhost:5432/miniecom
    JWT_SECRET=your_secret_key_here
    JWT_ALG=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

### 5. Run migrations

``` bash
alembic upgrade head
```

### 6. Start the app

``` bash
uvicorn app.main:app --reload
```

Server runs at:\
👉 http://127.0.0.1:8000\
👉 API docs: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 🧪 Running Tests

``` bash
pytest -vv
```

------------------------------------------------------------------------

## 📂 Project Structure

    mini-e-commerce/
    │── app/
    │   ├── core/          # Config & security
    │   ├── routers/       # API endpoints
    │   ├── models.py      # SQLAlchemy models
    │   ├── schemas.py     # Pydantic schemas
    │   ├── deps.py        # Dependencies
    │   ├── database.py    # DB setup
    │   └── main.py        # App entrypoint
    │
    │── tests/             # Unit tests
    │── alembic/           # Migrations
    │── requirements.txt
    │── README.md
    │── .env (ignored)

------------------------------------------------------------------------

## ✨ Author

👤 **Fırat Özgür Erişek (TTanoz)**\
🔗 [GitHub Profile](https://github.com/TTanoz)

------------------------------------------------------------------------

## 📜 License

This project is licensed under the MIT License.
