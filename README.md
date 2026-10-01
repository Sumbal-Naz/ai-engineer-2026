# AI Engineer 2026

My six-month transition into modern AI/ML engineering.

This repository documents my hands-on journey from Python/backend engineering fundamentals toward production-oriented AI/ML engineering.

The focus is on building real projects, writing tests, understanding software architecture, using Git professionally, and gradually progressing into modern AI systems.

## Current Focus

* Python
* SQL
* PostgreSQL
* FastAPI
* REST APIs
* Docker
* LLMs
* RAG
* AI Agents
* LLM Evaluation
* Fine-tuning
* Cloud
* CI/CD

---

# Month 1 — Python & Backend Engineering

Month 1 focused on building a strong software engineering foundation for AI engineering.

Topics covered include:

* Python fundamentals and typing
* Dataclasses and data structures
* File handling
* JSON and CSV processing
* FastAPI
* REST API design
* Pydantic validation
* Dependency injection
* SQLAlchemy
* SQLite
* Alembic migrations
* Authentication and authorization
* Password hashing and verification
* JWT authentication
* Role-based access control
* API testing with pytest
* Test database isolation
* Mocking and dependency overrides
* OpenAPI / Swagger
* Ruff linting and formatting
* Git branches and pull requests
* Building an independent REST API

---

# Main Project — AI Engineer 2026 API

The main project is a FastAPI-based backend demonstrating the software engineering concepts learned throughout Month 1.

The API provides functionality for:

* User registration
* User login
* JWT authentication
* Protected endpoints
* Admin authorization
* AI model management
* AI model CRUD operations
* Pagination
* Provider filtering
* Sorting
* Structured API errors
* Database persistence
* AI service integration

## Authentication

The API implements authentication using:

* Password verification
* OAuth2 password flow
* JWT access tokens
* Protected routes
* Active-user validation
* Role-based admin authorization

## AI Model Management

Authenticated users can manage AI model records through REST endpoints.

Supported operations include:

* Create an AI model
* Retrieve all models
* Retrieve a model by ID
* Update a model
* Delete a model

The model listing endpoint supports:

* Pagination with `skip` and `limit`
* Provider filtering
* Sorting by ID, name, or provider
* Ascending or descending order

## Database

The project uses:

* SQLAlchemy
* SQLite for local development
* Alembic for database migrations

The database layer is separated from API and business logic through dependency injection and service functions.

## Error Handling

The API includes custom exception handling for application-level errors such as:

* Model not found
* Duplicate model

These are converted into structured HTTP responses rather than exposing internal exceptions to API users.

---

# Independent Project — Task Management API

Month 1 also included an independently built Task Management REST API.

Location:

```text
projects/task-api/
```

The project demonstrates the ability to design and implement a smaller REST API independently without relying on the architecture of the main application.

Features include:

* Create tasks
* List tasks
* Retrieve a task
* Update a task
* Delete a task
* Validation
* HTTP status codes
* 404 error handling
* Automated API tests
* Service-layer separation

The project uses an in-memory data store intentionally to keep the focus on REST API design and implementation.

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* SQLite

## Authentication

* OAuth2
* JWT
* Password hashing and verification
* Role-based authorization

## Testing & Quality

* pytest
* Ruff
* FastAPI TestClient
* Mocking
* Dependency overrides

## Development

* Git
* GitHub
* VS Code
* Jupyter

---

# Repository Structure

```text
AI-Engineer-2026/
│
├── alembic/
│   ├── env.py
│   └── versions/
│
├── data/
│   ├── example.txt
│   ├── models.csv
│   └── models.json
│
├── docs/
│   └── git-workflow.md
│
├── notebooks/
│
├── projects/
│   └── task-api/
│       ├── app/
│       ├── tests/
│       ├── pyproject.toml
│       └── README.md
│
├── src/
│   └── app/
│       ├── api.py
│       ├── auth.py
│       ├── config.py
│       ├── database.py
│       ├── exceptions.py
│       ├── file_utils.py
│       ├── models.py
│       ├── relationship_models.py
│       ├── schemas.py
│       └── services.py
│
├── tests/
│
├── .gitignore
├── pyproject.toml
└── README.md
```

---

# Testing

The repository currently contains automated tests for both the main application and the independent Task API.

Run the complete test suite from the repository root:

```bash
python -m pytest
```

Current Day 30 baseline:

```text
65 passed
1 warning
```

The tests cover:

* API endpoints
* Authentication
* Authorization
* Validation
* Services
* Models
* Database-related behavior
* Configuration
* File utilities
* Task API CRUD operations
* Error handling
* Mocking and dependency overrides

---

# Code Quality

Ruff is used for linting and formatting.

Run linting:

```bash
ruff check .
```

Run formatting verification:

```bash
ruff format --check .
```

Current Day 30 status:

```text
Ruff: all checks passed
Formatting: 42 files already formatted
```

---

# API Documentation

The main API is built with FastAPI and provides automatically generated OpenAPI documentation.

When the API server is running, FastAPI provides interactive API documentation through its Swagger UI and OpenAPI endpoints.

Authentication-protected endpoints require a valid JWT access token.

---

# Month 1 Portfolio Checkpoint

By the end of Month 1, this repository demonstrates practical experience with:

* Designing REST APIs
* Separating API, service, schema, model, and database responsibilities
* Building authentication systems
* Implementing JWT-based authorization
* Working with relational databases
* Managing database schema changes with migrations
* Writing automated tests
* Testing authenticated and unauthorized behavior
* Mocking external behavior
* Using dependency injection
* Handling application errors cleanly
* Applying automated code-quality checks
* Working with Git branches and pull requests
* Building an independent API from scratch

---

# Month 2 — Data & Analytics Engineering

The next phase focuses on the data foundations required for modern AI/ML engineering.

Planned topics include:

* NumPy
* Pandas
* SQL
* Data cleaning
* Exploratory data analysis
* Data transformation
* Analytics engineering
* Data pipelines
* Working with structured datasets

The longer-term roadmap will progress toward:

```text
Python
   ↓
Backend & APIs
   ↓
Data & SQL
   ↓
Machine Learning
   ↓
Deep Learning
   ↓
LLMs
   ↓
RAG
   ↓
AI Agents
   ↓
Evaluation
   ↓
Deployment & MLOps
   ↓
Production AI Engineering
```

# Goal

Build and deploy production-grade AI applications and become job-ready for:

* AI/ML Engineer
* Applied AI Engineer
* LLM Engineer
* Python AI Engineer

This repository is a record of that progression through practical projects and progressively more production-oriented engineering work.
