import os
import yaml
from waitress import serve
from dash_app import flask_app as app

# retrieve app params from yml file
## grab same path as py script
relative_path = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
with open(os.path.join(relative_path, "config.yml"), "r") as yml_file:
    app_config = yaml.load(stream=yml_file, Loader=yaml.FullLoader)

# serve app
serve(
    app, 
    host=app_config['dash_config']['host'],
    threads=app_config['dash_config']['threads'],
    port=app_config['dash_config']['port']
)
