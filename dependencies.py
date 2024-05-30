from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def common_db(db: Session = Depends(get_db)) -> Session:
    return db


CommonDB = Annotated[Session, Depends(common_db)]
