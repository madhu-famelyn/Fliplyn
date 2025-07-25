#!/bin/bash
# run alembic migrations
alembic upgrade head

# start the app
uvicorn app.main:app --host 0.0.0.0 --port 10000