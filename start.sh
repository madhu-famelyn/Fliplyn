#!/bin/bash

# Run alembic migrations
alembic upgrade head

# Start the FastAPI app
uvicorn main:app --host 0.0.0.0 --port=$PORT
