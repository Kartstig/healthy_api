import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .fastapi import FastApiApplication
    from .flask import FlaskApplication

from ..git import git_stats, GitReturn
from ..version import read_version_file

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

SupportedApplication = Union["FlaskApplication", "FastApiApplication"]
FuncList = List[Callable]

ResponseJson = Dict[
    Union[Literal["uptime"], Literal["app"], Literal["status"], Literal["git"], str],
    Union[str, Literal["OK"], Literal["DOWN"], GitReturn],
]


class BaseAdapter(ABC):
    DEFAULT_ENABLE = True
    DEFAULT_ENABLE_GIT = True
    DEFAULT_ENABLE_VERSION = True
    DEFAULT_ENDPOINT = "/_health"

    def __init__(
        self,
        app: Optional[SupportedApplication] = None,
        extra_checks: Optional[FuncList] = None,
    ) -> None:
        if app is not None:
            check_fns = extra_checks if extra_checks is not None else []
            self.init_app(app, check_fns)

    def init_app(
        self,
        app: Optional[SupportedApplication],
        extra_checks: Optional[FuncList] = None,
    ) -> None:
        if app is None:
            raise ValueError("None is not a valid application")

        self.app = app
        self.extra_checks = extra_checks if extra_checks is not None else []
        self.start_time = datetime.now()
        self.config = self.load_config()
        self.logger = self.get_logger()

        if self.config["HAPI_ENABLE"]:
            self.load_router()

    def health(self):
        data: ResponseJson = {
            "uptime": str(datetime.now() - self.start_time),
            "app": self.app_name(),
        }

        raw_results: List[bool] = []
        if self.extra_checks:
            results = {}
            for func in self.extra_checks:
                try:
                    res: bool = func()
                    raw_results.append(res)
                except Exception as e:
                    self.logger.error(f"Error in healthcheck: {str(e)}")
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
