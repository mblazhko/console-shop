from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from database import SessionLocal
from user.models import OAuthAccount, User


async def get_db() -> AsyncSession:
    db = SessionLocal()

    try:
        yield db
    finally:
        await db.close()


async def get_user_db(session: AsyncSession = Depends(SessionLocal)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
