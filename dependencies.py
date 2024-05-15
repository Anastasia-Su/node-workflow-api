from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import SessionLocal


async def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def common_db(db: Session = Depends(get_db)):
    return db


CommonDB = Annotated[Session, Depends(common_db)]
