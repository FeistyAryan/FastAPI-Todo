# Production-Grade Microservice & Worker Architecture with FastAPI

This repository is a showcase of a robust, scalable, and observable backend system engineered for high performance and resilience. It moves beyond a simple CRUD application to demonstrate a complete, production-ready architecture featuring decoupled services, asynchronous task processing, and a comprehensive observability stack.

<br />


*A high-level overview of the service architecture, showcasing the flow of requests from the user to the API, and the decoupled communication with the worker via the message broker.*

---

## Core Features & Technical Highlights

This system is built with a focus on best practices for modern web services.

### Security
- **Robust Authentication**: Implements a secure JWT-based authentication system featuring **`HttpOnly` Refresh Token Rotation** to mitigate XSS attacks and provide secure, long-lived user sessions.
- **Secure Logout**: Utilizes a **Redis-based JWT Denylist** to immediately invalidate tokens upon logout, ensuring they cannot be reused even if they haven't expired.
- **Resilient Password Reset**: A secure, asynchronous password reset workflow that invalidates previous tokens upon new requests to minimize the attack surface.

### Architecture & Design
- **Decoupled Service Architecture**: The system is split into two primary services: a synchronous **API service** for handling user requests and an asynchronous **Worker service** for processing background tasks, ensuring the API remains fast and responsive.
- **Message-Driven Communication**: Leverages **RabbitMQ** as a message broker to facilitate reliable, asynchronous communication between the API and the worker, implementing the **Producer-Consumer** pattern for background job processing.
- **Layered (N-Tier) Architecture**: Enforces a strict separation of concerns through a well-defined layered architecture (**API Layer**, **Service Layer**, **Repository Layer**), making the codebase modular, testable, and maintainable.
- **Repository Design Pattern**: Abstracts data access logic, isolating the business layer from the database implementation and ensuring a consistent data access API.

### Observability
- **Structured Logging**: Implements `structlog` to produce machine-readable **JSON logs**, enabling powerful querying and analysis in centralized logging platforms.
- **End-to-End Request Tracing**: Utilizes **Correlation IDs** to trace a single user request across the entire system—from the initial API call, through the message queue, to the final processing in the worker—simplifying debugging in a distributed environment.
- **Real-time Monitoring**: Integrated with **Prometheus** for metrics collection and **Grafana** for real-time performance monitoring dashboards, providing crucial insights into API latency, error rates, and system health.

---

## Tech Stack

| Category              | Technology                                                                                                  |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Backend Framework** | FastAPI                                                                                                     |
| **Database** | PostgreSQL                                                                                                  |
| **ORM & Validation** | SQLModel (Pydantic + SQLAlchemy)                                                                            |
| **Migrations** | Alembic                                                                                                     |
| **Message Broker** | RabbitMQ                                                                                                    |
| **In-Memory Cache** | Redis                                                                                                       |
| **Observability** | Prometheus, Grafana                                                                                         |
| **Containerization** | Docker, Docker Compose                                                                                      |
| **Async Driver** | `asyncpg`                                                                                                   |
| **Logging** | `structlog`                                                                                                 |

---

## Local Development

### Prerequisites
- Docker and Docker Compose must be installed on your system.

### Running the Application
1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd <repository-folder>
    ```

2.  **Configure Environment Variables**
    Create a `.env` file from the example template and populate it with your own secret keys and configuration values.
    ```bash
    cp .env.example .env
    ```

3.  **Launch the System**
    Build and run the entire stack using Docker Compose. The `--build` flag is only necessary on the first run or after changing dependencies.
    ```bash
    docker compose up --build
    ```

---

## Exploring the Running System

Once the `docker compose up` command completes, the following services will be available:

| Service                   | URL                                     | Credentials      |
| ------------------------- | --------------------------------------- | ---------------- |
| **API Docs (Swagger UI)** | http://localhost:8000/docs              | -                |
| **Grafana Dashboard** | http://localhost:3000                   | `admin` / `admin` |
| **Prometheus Metrics** | http://localhost:9090                   | -                |
| **RabbitMQ Management** | http://localhost:15672                  | `guest` / `guest` |