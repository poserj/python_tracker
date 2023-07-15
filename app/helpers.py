import yaml
from fastapi import FastAPI

from .routers.users import router


def get_app_config() -> dict:
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data['APP']
        except yaml.YAMLError as exc:
            raise yaml.YAMLError


def init_app() -> FastAPI:
    config: dict = get_app_config()
    app = FastAPI()
    app.include_router(router)
    return app
