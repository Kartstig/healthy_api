=====
Usage
=====

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
