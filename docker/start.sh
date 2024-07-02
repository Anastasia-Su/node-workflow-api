#!/bin/sh

alembic revision --autogenerate -m "initial_migration"
alembic upgrade head
python -m uvicorn main:app --host 0.0.0.0 --port 8000
