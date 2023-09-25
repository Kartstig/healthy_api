import logging
import os

from .base_adapter import BaseAdapter


class FastapiAdapter(BaseAdapter):
    def app_name(self) -> str:
        return self.app.title

    def get_logger(self):
        return logging.getLogger()

    def json_response(self, data: dict):
        # FastAPI will handle the json headers
        return data

    def load_config(self) -> dict:
        return {
            "HAPI_ENABLE": bool(
                int(os.environ.get("HAPI_ENABLE", self.DEFAULT_ENABLE))
            ),
            "HAPI_ENABLE_GIT": bool(
                int(os.environ.get("HAPI_ENABLE_GIT", self.DEFAULT_ENABLE_GIT))
            ),
            "HAPI_ENABLE_VERSION": bool(
                int(os.environ.get("HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION))
            ),
            "HAPI_ENDPOINT": os.environ.get("HAPI_ENDPOINT", self.DEFAULT_ENDPOINT),
            "HAPI_ENABLE_VERSION": bool(
                int(os.environ.get("HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION))
            ),
        }

    def load_router(self) -> None:
        @self.app.get(self.config["HAPI_ENDPOINT"])
        def _health():
            return self.health()
