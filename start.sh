#!/bin/sh

#if [ ! -d "alembic" ]; then
#    alembic init alembic
#    alembic revision --autogenerate -m "initial_migration"
#fi
#
#python generate_alembic_ini.py

alembic upgrade head
python -m uvicorn main:app --host 0.0.0.0 --port 8000
