__version__ = "0.1.0"

import os

from typing import Union

from .adapters.fastapi import FastapiAdapter
from .adapters.flask import FlaskAdapter


def load_adapter() -> Union[FlaskAdapter, FastapiAdapter]:
    framework = os.getenv("HAPI_WEB_FRAMEWORK")

    if framework == "flask":
        return FlaskAdapter
    elif framework == "fastapi":
        return FastapiAdapter
    else:
        raise ValueError("You must specify a web framework (flask/fastapi)")
