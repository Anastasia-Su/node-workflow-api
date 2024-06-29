#!/bin/sh


#if [ ! -d "alembic" ]; then
#    alembic init alembic
#    alembic revision --autogenerate -m "initial_migration"
#else
#    echo "Alembic directory already exists. Skipping initialization."
#
#fi

#python docker/generate_alembic_ini.py

#if [ ! -f "/app/alembic.ini" ]; then
#    cp alembic.ini ./alembic.ini
#fi

alembic upgrade head
python -m uvicorn main:app --host 0.0.0.0 --port 8000
