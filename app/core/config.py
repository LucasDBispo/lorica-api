from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@postgres:5432/lorica_dev"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AdminSettings(BaseSettings):
    admin_email: str = "admin@lorica.app"
    admin_password: str = "lorica12345"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class JWTSettings(BaseSettings):
    jwt_secret_key: str = "supersecretkey"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: float = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
