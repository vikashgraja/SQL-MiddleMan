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

## Create New Table

    python manage.py create_table Ingestion sample_table

Generates: - model - service - API - serializer

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
