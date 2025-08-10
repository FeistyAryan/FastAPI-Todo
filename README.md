# Multi-Device To-Do App Backend

A robust, production-grade backend for a To-Do application, featuring a secure, multi-device authentication system using FastAPI.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with Alembic for migrations)
- **ORM / Data Validation:** SQLModel (built on Pydantic & SQLAlchemy)
- **Authentication:** JWT with `HttpOnly` Refresh Token Rotation
- **Async Driver:** `asyncpg`
- **Infrastructure:** Docker & Docker Compose
- **Dependency Management:** `pip-tools`

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd fastapi-app
    ```

2.  **Create the environment file:**
    Copy the example file and fill in your own secret values.
    ```bash
    cp .env.example .env
    ```

3.  **Build and run the application:**
    ```bash
    docker compose up --build
    ```

4.  **The API will be available at:** `http://localhost:8000`