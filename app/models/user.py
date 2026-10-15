from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        Enum("Admin", "Viewer", name="user_role"),
        nullable=False,
        default="Viewer",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )