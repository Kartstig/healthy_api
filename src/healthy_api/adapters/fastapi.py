import logging
import os
from typing import Type, cast

from fastapi import FastAPI, Response

from .base_adapter import BaseAdapter

FastApiApplication = Type[FastAPI]


class FastapiAdapter(BaseAdapter):
    def app_name(self) -> str:
        app = cast(FastAPI, self.app)
        return app.title

    def get_logger(self):
        return logging.getLogger()

    def json_response(self, data: dict) -> dict:
        # FastAPI will handle the json headers
        return data

    def load_config(self) -> dict:
        return {
            "HAPI_ENABLE": bool(int(os.environ.get("HAPI_ENABLE", self.DEFAULT_ENABLE))),
            "HAPI_ENABLE_GIT": bool(
                int(os.environ.get("HAPI_ENABLE_GIT", self.DEFAULT_ENABLE_GIT))
            ),
            "HAPI_ENABLE_VERSION": bool(
                int(os.environ.get("HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION))
            ),
            "HAPI_ENDPOINT": os.environ.get("HAPI_ENDPOINT", self.DEFAULT_ENDPOINT),
        }

    def load_router(self) -> None:
        app = cast(FastAPI, self.app)
        endpoint = cast(str, self.config["HAPI_ENDPOINT"])

        @app.get(path=endpoint)
        def _health():
            return self.health()

        @app.options(path=endpoint)
        def _health_options():
            return Response(status_code=200)
