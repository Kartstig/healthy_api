__version__ = "0.1.0"

import os

from typing import Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .adapters.fastapi import FastapiAdapter
    from .adapters.flask import FlaskAdapter

    T_FlaskAdapter = Type[FlaskAdapter]
    T_FastApiAdapter = Type[FastapiAdapter]


def load_adapter() -> Union["T_FlaskAdapter", "T_FastApiAdapter"]:
    framework = os.getenv("HAPI_WEB_FRAMEWORK")

    if framework == "flask":
        from .adapters.flask import FlaskAdapter

        return FlaskAdapter
    elif framework == "fastapi":
        from .adapters.fastapi import FastapiAdapter

        return FastapiAdapter
    else:
        raise ValueError("You must specify a web framework (flask/fastapi)")
