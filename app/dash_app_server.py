import os
import yaml
from waitress import serve

# import app
from dash_app import flask_app as app

# custom import(s)
from helpers.app_config import app_config_cls

app_config = app_config_cls()

# serve app
serve(
    app,
    host=app_config.dash_config.host,
    threads=app_config.dash_config.threads,
    port=app_config.dash_config.port
)
