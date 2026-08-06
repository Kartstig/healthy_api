from __future__ import annotations

from typing import Any, Type, cast

import flask

from .base_adapter import BaseAdapter

FlaskApplication = Type[flask.Flask]


class FlaskAdapter(BaseAdapter):
    def app_name(self) -> str:
        app = cast(flask.Flask, self.app)
        return app.name

    def get_logger(self) -> Any:
        app = cast(flask.Flask, self.app)
        return app.logger

    def json_response(self, data: dict) -> flask.Response:
        return flask.jsonify(data)

    def load_config(self) -> dict[str, Any]:
        app = cast(flask.Flask, self.app)
        config = {
            "HAPI_ENABLE": bool(int(app.config.get("HAPI_ENABLE", self.DEFAULT_ENABLE))),
            "HAPI_ENABLE_GIT": bool(
                int(app.config.get("HAPI_ENABLE_GIT", self.DEFAULT_ENABLE_GIT))
            ),
            "HAPI_ENABLE_VERSION": bool(
                int(app.config.get("HAPI_ENABLE_VERSION", self.DEFAULT_ENABLE_VERSION))
            ),
            "HAPI_ENDPOINT": app.config.get("HAPI_ENDPOINT", self.DEFAULT_ENDPOINT),
        }
        app.config.update(config)
        return config

    def load_router(self) -> None:
        app = cast(flask.Flask, self.app)
        endpoint = cast(str, self.config["HAPI_ENDPOINT"])

        def _health_options():
            return flask.Response(status=200)

        app.add_url_rule(
            rule=endpoint, endpoint="hapi_health", view_func=self.health, methods=["GET"]
        )
        app.add_url_rule(
            rule=endpoint,
            endpoint="hapi_health_options",
            view_func=_health_options,
            methods=["OPTIONS"],
        )
