===============================
Healthy-API
===============================

        Healthchecks for Any Framework (FastAPI/Flask)

.. _FastAPI: https://github.com/tiangolo/fastapi/

.. _Flask: https://github.com/pallets/flask/

.. image:: https://img.shields.io/pypi/v/Healthy-API.svg
        :target: https://pypi.python.org/pypi/Healthy-API
        :alt: PyPI

.. image:: https://github.com/Kartstig/healthy_api/actions/workflows/pytest.yml/badge.svg?branch=master
        :target: https://github.com/Kartstig/healthy_api/actions/workflows/pytest.yml
        :alt: GitHub Actions

.. image:: https://readthedocs.org/projects/healthy_api/badge/?version=latest
        :target: https://healthy_api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/Kartstig/healthy_api/graph/badge.svg?token=mTG6WudJwK
        :target: https://codecov.io/gh/Kartstig/healthy_api
        :alt: Codecov

.. image:: https://img.shields.io/pypi/dm/Healthy-API
        :alt: PyPI - Downloads

Healthy-API is designed to work with both Flask and FastAPI. Healthy-API is really simple
to set up. Healthy-API will provide an enpoint at `/_health` where you will get a JSON response
of the system's uptime, current git revision, version, and function you want.

You can also add in extra checks by passing in a list of checks to the
constructor.

Installing
----------

Install and update using `pip`\:

.. code-block:: text

        pip install -U healthy_api

FastAPI Configuration
---------------------

.. code-block:: python

  from fastapi import FastAPI
  from healthy_api.adapters.fastapi import FlaskAdapter as HealthyApi

  app = FastAPI(__name__)

  def db_check():
    """Database"""
    try:
        with get_session_ctx() as session:
            (res,) = session.execute(text("SELECT 1")).fetchone()
            return bool(res == 1)
    except Exception as e:
        logger.error(f"Unable to connect to database: {e}")
        return False

  HealthyApi(app, extra_checks=[db_check])


Flask Configuration
-------------------

.. code-block:: python

  from Flask import Flask
  from healthy_api.adapters.flask import Flask as HealthyApi

  app = Flask(__name__)

  HealthyApi(app)

Or if you can use the `init_app` function:

.. code-block:: python

    from Flask import Flask
    from healthy_api.adapters.flask import Flask as HealthyApi

    app = Flask(__name__)

    healthy_api = HealthyApi()
    healthy_api.init_app(app)

* Free software: MIT license
* Documentation: https://healthy_api.readthedocs.io.


Features
--------

* Current Git Commit
* Current Version
* Accepts custom functions


Configuration
-------------

+---------------------+---------------------------------+------+------------+
| Config Key          | Description                     | Type | Default    |
+=====================+=================================+======+============+
| HAPI_ENABLE         | Enable/Disable Healthy-API      | bool | True       |
+---------------------+---------------------------------+------+------------+
| HAPI_ENABLE_GIT     | Enable/Disable Git Stats        | bool | True       |
+---------------------+---------------------------------+------+------------+
| HAPI_ENABLE_VERSION | Enable/Disable Version Stats    | bool | True       |
+---------------------+---------------------------------+------+------------+
| HAPI_ENDPOINT       | Custom Route                    | str  | /_health   |
+---------------------+---------------------------------+------+------------+


Sponsorship
-----------

Put your logo here! `Become a sponsor`_ and support this project!

.. _Become a sponsor: https://github.com/sponsors/Kartstig



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

