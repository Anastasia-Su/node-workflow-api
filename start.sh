if [ ! -d "alembic" ]; then
    alembic init alembic
    alembic revision --autogenerate -m "initial_migration"
    alembic upgrade head
fi

python -m uvicorn main:app --host 0.0.0.0 --port 8000
