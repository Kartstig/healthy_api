#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_healthy_api
----------------------------------

Tests for `healthy_api` module.
"""

import json
import os
import pytest

from src.healthy_api import load_adapter


@pytest.fixture
def flask_app():
    from flask import Flask

    app = Flask("TEST_APP")
    app.config["TESTING"] = True
    os.environ["HAPI_WEB_FRAMEWORK"] = "flask"
    return app


def test_constructor(flask_app):
    FlaskAdapter = load_adapter()
    fm = FlaskAdapter(flask_app)
    assert isinstance(fm, load_adapter())
    assert fm.app.name == "TEST_APP"
    assert fm.app.config["HAPI_ENABLE_GIT"] is True


def test_init_app(flask_app):
    FlaskAdapter = load_adapter()
    fm = FlaskAdapter()
    fm.init_app(flask_app)
    assert isinstance(fm, load_adapter())
    assert fm.app.name == "TEST_APP"


def test_response(flask_app):
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
    FlaskAdapter = load_adapter()
    fm = FlaskAdapter(flask_app)
    client = fm.app.test_client()
    rv = client.get("/_health")
    data = json.loads(rv.data.decode("utf-8"))
    assert rv.status_code == 200
    assert data["status"] == "OK"
    assert data["app"] == fm.app.name
    assert data["git"] != {}
    assert data["git"]["author"] == author
    assert data["git"]["commit"] == commit
    assert data["git"]["date"] == date


def test_disable(flask_app):
    flask_app.config["HAPI_ENABLE"] = False
    FlaskAdapter = load_adapter()
    fm = FlaskAdapter()
    fm.init_app(flask_app)
    client = fm.app.test_client()
    rv = client.get("/_health")

    assert rv.status_code == 404


def test_extra_ok(flask_app):
    def fake_function():
        """TestingFunc"""
        return True

    FlaskAdapter = load_adapter()
    fm = FlaskAdapter()
    fm.init_app(flask_app, extra_checks=[fake_function])

    client = fm.app.test_client()
    rv = client.get("/_health")

    assert rv.status_code == 200
    data = json.loads(rv.data.decode("utf-8"))
    assert data["TestingFunc"] == "OK"


def test_extra_exception(flask_app):
    def fake_function():
        """FailFunc"""
        raise Exception("This function raised an exception")

    FlaskAdapter = load_adapter()
    fm = FlaskAdapter()
    fm.init_app(flask_app, extra_checks=[fake_function])

    client = fm.app.test_client()
    rv = client.get("/_health")

    assert rv.status_code == 200
    data = json.loads(rv.data.decode("utf-8"))
    assert data["FailFunc"] == "DOWN"
