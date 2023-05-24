# Bullpen API

The Bullpen API is the application that powers Bullpen AI.

The stack:
 - Nginx
 - FastAPI (python 3.11)
 - Vue 3
 - Postgres

## Setup

On development, you can launch the application with Docker.

1. Copy .env.example to .env and populate all values with the necessary values.
2. Update your hosts file:
  - `sudo nano /etc/hosts`
  - Add the line: `127.0.0.1   bullpen.local`
  - Add the line: `127.0.0.1   api.bullpen.local`
3. Launch the application: `docker-compose up -d`

After it launches, you can access the Vue site at http://bullpen.local/. The API can be referenced at http://bullpen.local/api/v1/

## Deployment

For now we do a manual deployment.

On staging/prod, run the following command: `docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d`

## Database Migrations

To create a new database migration, log into the fastapi container and run: `alembic revision -m "description of my migration"`

To execute outstanding migrations, run: `alembic upgrade head`

To roll back the most recent migration, run: `alembic downgrade -1`. More info here: https://alembic.sqlalchemy.org/en/latest/tutorial.html#downgrading