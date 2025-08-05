from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str 
    database_port: int
    database_db_name: str 
    database_user: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()