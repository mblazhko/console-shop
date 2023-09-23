from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from database import Base


class DBUser(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
