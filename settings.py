import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_username: str
    auth_password: str
    beatsaber_dir: str
    app_host: str
    app_port: int

    class Config:
        env_file = os.path.join(os.path.expanduser("~"), ".spicetify", ".beatsaber.env")
