import flask
from typing import Any, Dict, Type

from .base_adapter import BaseAdapter

FlaskApplication = Type[flask.Flask]


class FlaskAdapter(BaseAdapter):
    def app_name(self) -> str:
        return self.app.name

    def get_logger(self) -> Any:
        return self.app.logger

    def json_response(self, data: dict) -> flask.Response:
        return flask.jsonify(data)

    def load_config(self) -> Dict[str, Any]:
        config = {
            "HAPI_ENABLE": bool(
                int(self.app.config.get("HAPI_ENABLE", self.DEFAULT_ENABLE))
            ),
            "HAPI_ENABLE_GIT": bool(
                int(self.app.config.get("HAPI_ENABLE_GIT", self.DEFAULT_ENABLE_GIT))
            ),
            "HAPI_ENABLE_VERSION": bool(
                int(
                    self.app.config.get(
                        "HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION
                    )
                )
            ),
            "HAPI_ENDPOINT": self.app.config.get(
                "HAPI_ENDPOINT", self.DEFAULT_ENDPOINT
            ),
            "HAPI_ENABLE_VERSION": bool(
                int(
                    self.app.config.get(
                        "HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION
                    )
                )
            ),
        }
        self.app.config.update(config)
        return config

    def load_router(self) -> None:
        self.app.add_url_rule(self.config["HAPI_ENDPOINT"], view_func=self.health)
