from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str = "ES256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def private_key_bytes(self) -> bytes:
        return self.JWT_PRIVATE_KEY.replace("\\n", "\n").encode("utf-8")

    @property
    def public_key_bytes(self) -> bytes:
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n").encode("utf-8")

    class Config:
        env_file = ".env"


settings = Settings()
