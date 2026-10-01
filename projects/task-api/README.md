# Task Management API

A small independent REST API built with FastAPI as part of the AI Engineer 2026 Month 1 portfolio.

The purpose of this project was to independently design and implement a complete CRUD API while applying REST principles, request validation, service-layer separation, HTTP status codes, and automated testing.

## Features

* Create tasks
* List all tasks
* Retrieve a task by ID
* Update a task
* Delete a task
* Request validation with Pydantic
* Proper HTTP status codes
* 404 handling for missing tasks
* Service-layer separation
* Automated API tests
* Test data isolation between tests

## API Endpoints

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| POST   | `/tasks`           | Create a task      |
| GET    | `/tasks`           | Retrieve all tasks |
| GET    | `/tasks/{task_id}` | Retrieve a task    |
| PUT    | `/tasks/{task_id}` | Update a task      |
| DELETE | `/tasks/{task_id}` | Delete a task      |

## Project Structure

```text
task-api/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       └── task_service.py
│
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
│
├── pyproject.toml
└── README.md
```

## Architecture

The project separates responsibilities into simple layers:

### API layer

`app/api.py`

Defines the HTTP endpoints, request handling, response models, and HTTP status codes.

### Schema layer

`app/schemas.py`

Defines Pydantic models for validating incoming requests and outgoing responses.

### Service layer

`app/services/task_service.py`

Contains the task storage and business operations separately from the HTTP layer.

### Tests

`tests/test_tasks.py`

Contains automated tests covering successful CRUD operations and expected 404 responses.

`tests/conftest.py`` resets the in-memory task storage between tests so individual tests remain isolated.

## Data Storage

This project intentionally uses an **in-memory Python dictionary** rather than a database.

The goal was to focus on REST API design and application architecture rather than database configuration.

The project can later be extended with SQLAlchemy and a relational database.

## Running the Tests

From the `projects/task-api` directory:

```bash
python -m pytest
```

The project currently contains **8 automated tests** covering:

* Task creation
* Task listing
* Task retrieval
* Missing task handling
* Task updates
* Task deletion

## Code Quality

Ruff is used for code-quality checks.

```bash
ruff check .
```

```bash
ruff format --check .
```

## Technologies

* Python
* FastAPI
* Pydantic
* pytest
* Ruff

## Learning Outcome

This project demonstrates the ability to independently build a small REST API from scratch and apply concepts learned throughout Month 1 of the AI Engineer 2026 roadmap.

The project serves as a focused example of:

* REST API design
* CRUD operations
* Pydantic validation
* Service-layer architecture
* HTTP status codes
* Error handling
* Automated testing
* Code quality practices
