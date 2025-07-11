from typing import Any

from sqlalchemy import UUID, Column, String
from sqlalchemy.sql.schema import Column

from ..utils.db_util import Base


class User(Base):
    __tablename__: str = "users"
    id: Column[Any] = Column(UUID, primary_key=True)
    name: Column[str] = Column(String)
    email: Column[str] = Column(String)
    password: Column[str] = Column(String)
