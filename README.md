# SQL-MiddleMan

> Django-based **API Middleware for SQL Databases**\
> Built for **ETL pipelines, and analytics workflows**

------------------------------------------------------------------------

## Overview

SQL-MiddleMan acts as a **structured data control layer** between:

    - Data Sources (ETL jobs)
    - SQL Database
    - Analytics / Reporting Systems

------------------------------------------------------------------------

## Architecture

    SAP / ETL → Ingestion API → Service Layer → SQL DB → Fetch API → Analytics

------------------------------------------------------------------------

## Project Structure

    SQL-MiddleMan/
    ├── Ingestion/        # ETL → DB
    ├── Analytics/        # Analysis → DB
    ├── SQLMiddleMan/     # Core config & auth
    ├── tools/            # CLI generators
    ├── manage.py
    └── pyproject.toml

------------------------------------------------------------------------

## Setup

### 1. Install dependencies

    uv sync

### 2. Migrate DB

    python manage.py makemigrations
    python manage.py migrate

### 3. Run server

    python manage.py runserver

------------------------------------------------------------------------

## Create New Table (Step-by-Step Implementation)

When you need to add a new table to the project, follow these steps to hook it up correctly from end-to-end:

### 1. Run the Generator
Use the custom `create_table` management command to scaffold the base files:
```bash
uv run manage.py create_table <AppName> <table_name>
# Example: uv run manage.py create_table Ingestion customer_data
```
*(This automatically generates the Model, Serializer, Service, API, and a Test stub in `<AppName>/tests/test_<table_name>.py`)*

### 2. Update the Serializer
Open `<AppName>/serializers/<table_name>_serializer.py` and define the validation fields that match your intended payload (the incoming `rows`):
```python
from rest_framework import serializers

class CustomerDataSerializer(serializers.Serializer):
    run_id = serializers.CharField(max_length=50, required=False)
    # Define your specific row fields here
    customer_name = serializers.CharField()
```

### 3. Implement the Service Logic
Open `<AppName>/services/<table_name>_service.py` and define the behavior for storing and retrieving records:
- **`insert_<name>`**: Iterate over the `rows` to create new database records via your Model.
- **`fetch_<name>`**: Query the Model (e.g. filtered by `run_id`) and return a list of dictionaries.

### 4. Wire up the URL Routes
Open `<AppName>/urls.py` and map your new endpoints. Import the API views and route them appropriately:
```python
from .api.customer_data_api import insert_customer_data_api, fetch_customer_data_api

urlpatterns += [
    path("customer_data/insert/", insert_customer_data_api),
    path("customer_data/fetch/", fetch_customer_data_api),
]
```

### 5. Migrate the Database
Finally, generate and apply migrations to register the new Model in your database schema:
```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

------------------------------------------------------------------------

## API Design

### Insert

    POST /ingestion/<name>/insert/

Body:

    ```json
    {
    "run_id": "run_001",
    "rows": []
    }
    ```

------------------------------------------------------------------------

### Fetch

    GET /ingestion/<name>/fetch/?run_id=run_001

------------------------------------------------------------------------

## Data Flow

    API → Serializer → Service → Model → Database

------------------------------------------------------------------------

## Coding Rules

### DO

> [!IMPORTANT]
> One module per table\
> Use service layer to access database\
> Validate using serializers

### DON'T

> [!WARNING]
> No business logic in API\
> No cross-module edits

------------------------------------------------------------------------

## Authentication

Located in:

    SQLMiddleMan/authentication.py

------------------------------------------------------------------------

## Use Cases

- SAP T-code ingestion
- Audit pipelines
- Internal analytics APIs
- Data governance layer

------------------------------------------------------------------------

## Future Scope

- Pagination
- Admin‑managed endpoint groups with scoped access tokens for granular API control
- Monitoring

------------------------------------------------------------------------

## Testing with Sample Tables

Since `create_table` automatically generates the base components (API, serializer, service, and model), testing the components end-to-end requires explicitly defining your logic layers and mapping the generic URL routes.

### 1. Configure the API Key 
The system relies on a central API Key for authentication via the `APIKeyAuthentication` class. Create a `.env` file in the project directory:
```env
API_KEY=testkey123
```

### 2. Prepare the Database Models
Run Django's migration commands to formalize the generated tables into your local `db.sqlite3`:
```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

### 3. Curl Test Examples
Spin up your local server (`uv run manage.py runserver`). You can then insert and fetch data from the tables using the `Authorization: API-Key <key>` header format.

**Test Ingestion (Insert Data)**:
```bash
curl -s -X POST http://127.0.0.1:8000/ingestion/sample_data/insert/ \
  -H "Authorization: API-Key testkey123" \
  -H "Content-Type: application/json" \
  -d '{"run_id": "test_ingestion_1", "rows": [{"example_column": "example_value"}]}'
```

**Test Ingestion (Fetch Data)**:
```bash
curl -s -X GET "http://127.0.0.1:8000/ingestion/sample_data/fetch/?run_id=test_ingestion_1" \
  -H "Authorization: API-Key testkey123"
```

**Test Analytics Example**: 
The endpoints seamlessly mirror the data behavior in the Analytics side using the same URL convention:
`POST http://127.0.0.1:8000/analytics/sample_result/insert/`
`GET http://127.0.0.1:8000/analytics/sample_result/fetch/?run_id=test_1`
