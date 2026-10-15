from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)


def register_user(db: Session, name: str, email: str, password: str):
    normalized_email = email.strip().lower()

    if get_user_by_email(db, normalized_email):
        return None

    user = create_user(
        db=db,
        name=name.strip(),
        email=normalized_email,
        hashed_password=hash_password(password),
        role="Viewer",
    )

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email.strip().lower())

    if not user or not verify_password(password, user.hashed_password):
        return None

    token = create_access_token(user_id=user.id, role=user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }