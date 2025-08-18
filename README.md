# Multi-Device To-Do App Backend

A robust, production-grade backend for a To-Do application, featuring a secure, multi-device authentication system using FastAPI. This project demonstrates a clean, layered architecture and modern development best practices.

## Features

* **Secure User Authentication:** JWT-based authentication with `HttpOnly` Refresh Token Rotation for enhanced security.
* **Multi-Device Session Management:** Users can be logged in on multiple devices, with the ability to log out from a specific session.
* **Layered Architecture:** A clean separation of concerns between the API, business logic, and data access layers.
* **Asynchronous from the Ground Up:** Built with `async` and `await` using `asyncpg` for high performance.
* **Database Migrations:** Alembic for safe and version-controlled schema management.
* **Containerized:** Fully containerized with Docker and Docker Compose for easy setup and deployment.

---
## Architecture & Design Patterns

This project is built using a **Layered (N-Tier) Architecture** to ensure a clean separation of concerns, making the application scalable, maintainable, and easy to test.



* **1. API Layer (`/api`)**: The outermost layer, responsible for handling HTTP requests and responses. It defines the API endpoints and handles request validation using FastAPI's Pydantic integration. It knows nothing about business logic or the database.

* **2. Service Layer (`/services`)**: The "brains" of the application. This layer contains all the business logic and orchestrates the application's use cases (e.g., "registering a new user" involves checking for duplicates, hashing a password, and creating a user record). It is completely independent of the web framework.

* **3. Repository Layer (`/repositories`)**: This layer implements the **Repository Pattern**, abstracting the data source. Its only job is to perform direct database operations (CRUD - Create, Read, Update, Delete). This isolates our business logic from the specifics of the database, making it easy to change or mock for testing.

We also leverage **Dependency Injection** by creating singleton instances of our service and repository classes, which are then used throughout the application. This promotes loose coupling and makes the codebase easier to manage.

---
## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (with Alembic for migrations)
- **ORM / Data Validation:** SQLModel (built on Pydantic & SQLAlchemy)
- **Authentication:** JWT with `HttpOnly` Refresh Token Rotation
- **Async Driver:** `asyncpg`
- **Infrastructure:** Docker & Docker Compose
- **Dependency Management:** `pip-tools` (or Poetry)

---


## Getting Started

### Prerequisites
- Docker and Docker Compose must be installed on your system.

1.  **Clone the repository**
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

4.  **API Documentation**

    Once the application is running, the interactive API documentation (provided by Swagger UI) is available at:

    [**http://localhost:8000/docs**](http://localhost:8000/docs)