from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_username: str
    auth_password: str
    beatsaber_dir: str

    class Config:
        env_file = ".env"
