import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./edabip_reports.db",
    )
    TEST_DATABASE_URL: str = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///./test_edabip_reports.db",
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )


settings = Settings()

if not settings.JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY is missing. Add it to your .env file."
    )