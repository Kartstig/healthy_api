from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, Union

if TYPE_CHECKING:
    from .fastapi import FastApiApplication
    from .flask import FlaskApplication

from ..git import GitReturn, git_stats
from ..version import read_version_file

SupportedApplication = Union["FlaskApplication", "FastApiApplication"]
FuncList = List[Callable]

ResponseJson = Dict[
    Union[Literal["uptime", "app", "status", "git"], str],
    Union[Literal["OK", "DOWN"], str, GitReturn],
]


class BaseAdapter(ABC):
    DEFAULT_ENABLE = True
    DEFAULT_ENABLE_GIT = True
    DEFAULT_ENABLE_VERSION = True
    DEFAULT_ENDPOINT = "/_health"

    def __init__(
        self,
        app: SupportedApplication | None = None,
        extra_checks: FuncList | None = None,
    ) -> None:
        if app is not None:
            check_fns = extra_checks if extra_checks is not None else []
            self.init_app(app, check_fns)

    def init_app(
        self,
        app: SupportedApplication | None,
        extra_checks: FuncList | None = None,
    ) -> None:
        if app is None:
            raise ValueError("None is not a valid application")

        self.app = app
        self.extra_checks = extra_checks if extra_checks is not None else []
        self.start_time = datetime.now(timezone.utc)
        self.config = self.load_config()
        self.logger = self.get_logger()

        if self.config["HAPI_ENABLE"]:
            self.load_router()

    def health(self):
        data: ResponseJson = {
            "uptime": str(datetime.now(timezone.utc) - self.start_time),
            "app": self.app_name(),
        }

        raw_results: list[bool] = []
        if self.extra_checks:
            results = {}
            for func in self.extra_checks:
                try:
                    res: bool = func()
                    raw_results.append(res)
                except Exception as e:  # noqa: BLE001 - user checks may raise anything
                    self.logger.error(f"Error in healthcheck: {e!s}")
                    res = False

                results[func.__doc__] = "OK" if res else "DOWN"
            data.update(results)

        data["status"] = "OK" if all(raw_results) else "DOWN"

        if self.config["HAPI_ENABLE_GIT"]:
            data.update({"git": git_stats()})

        if self.config["HAPI_ENABLE_VERSION"]:
            data.update({"version": read_version_file()})

        return self.json_response(data)

    @abstractmethod
    def get_logger(self) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def json_response(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def load_config(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def load_router(self) -> None:
        raise NotImplementedError
