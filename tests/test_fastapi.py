#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_healthy_api
----------------------------------

Tests for `healthy_api` module.
"""

import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.healthy_api import load_adapter
from src.healthy_api.adapters.fastapi import FastapiAdapter as FA_REF


@pytest.fixture(scope="function")
def fastapi_app():
    app = FastAPI(title="TEST_APP")
    app.debug = True
    os.environ["HAPI_WEB_FRAMEWORK"] = "fastapi"
    return app


def test_constructor(fastapi_app):
    FastapiAdapter = load_adapter()
    fm = FastapiAdapter(fastapi_app)
    assert isinstance(fm, FA_REF)
    assert fm.app.title == "TEST_APP"
    assert fm.config["HAPI_ENABLE_GIT"] is True


def test_init_app(fastapi_app):
    FastapiAdapter = load_adapter()
    fm = FastapiAdapter()
    fm.init_app(fastapi_app)
    assert isinstance(fm, FA_REF)
    assert fm.app.title == "TEST_APP"


def test_response(fastapi_app):
    import subprocess

    commit = "lfbd90b2kn2knpds0iboslkmb2kl2g90sg09sbjl"
    author = "He-Man with an R <he-man@gmail.com>"
    date = "Tue Apr 20 01:04:20 2017 -0500"

    def mock_subprocess(*args, **kwargs):
        lines = [
            "commit:\t{}".format(commit),
            "Author:\t{}".format(author),
            "Date:\t{}".format(date),
        ]
        return "\n".join(lines).encode("utf-8")

    subprocess.check_output = mock_subprocess
    FastapiAdapter = load_adapter()
    fm = FastapiAdapter(fastapi_app)
    client = TestClient(fastapi_app)

    rv = client.get("/_health")
    data = rv.json()
    assert rv.status_code == 200
    assert data["status"] == "OK"
    assert data["app"] == fm.app.title
    assert data["git"] != {}
    assert data["git"]["author"] == author
    assert data["git"]["commit"] == commit
    assert data["git"]["date"] == date


def test_disable(fastapi_app):
    os.environ["HAPI_ENABLE"] = "0"
    FastapiAdapter = load_adapter()
    fm = FastapiAdapter()
    fm.init_app(fastapi_app)

    client = TestClient(fastapi_app)
    rv = client.get("/_health")

    os.environ["HAPI_ENABLE"] = "1"

    assert rv.status_code == 404


def test_extra_ok(fastapi_app):
    def fake_function():
        """TestingFunc"""
        return True

    FastapiAdapter = load_adapter()
    FastapiAdapter(fastapi_app, extra_checks=[fake_function])

    client = TestClient(fastapi_app)
    rv = client.get("/_health")

    assert rv.status_code == 200
    data = rv.json()
    assert data["TestingFunc"] == "OK"


def test_extra_exception(fastapi_app):
    def fake_function():
        """FailFunc"""
        raise Exception("This function raised an exception")

    FastapiAdapter = load_adapter()
    fm = FastapiAdapter()
    fm.init_app(fastapi_app, extra_checks=[fake_function])

    client = TestClient(fastapi_app)
    rv = client.get("/_health")

    assert rv.status_code == 200
    data = rv.json()
    assert data["FailFunc"] == "DOWN"
