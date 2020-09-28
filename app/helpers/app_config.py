import os
import yaml
import pyodbc

# retrieve a class attributes without having to instantiate an assignment variable
# ***not used***
def get_cls_attributes(cls_obj):
    return (lambda obj_cls: obj_cls.__dict__, cls_obj())[1].__dict__

# read yml file contents
def read_yml_file(config_file_path, config_file_name):
    with open(os.path.join(config_file_path, config_file_name), "r") as yml_file:
        app_config = yaml.load(stream=yml_file, Loader=yaml.FullLoader)
    return app_config

# variables
dash_config_str = 'dash_config'
db_config_str = 'db_config'
config_file_name = 'config.yml'
relative_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
app_config = read_yml_file(relative_path, config_file_name)

# classes
class dash_config_cls():
    def __init__(self,
                 routes_pathname_prefix: str = app_config[dash_config_str]['routes_pathname_prefix'],
                 requests_pathname_prefix: str = app_config[dash_config_str]['requests_pathname_prefix'],
                 host: str = app_config[dash_config_str]['host'],
                 threads: int = app_config[dash_config_str]['threads'],
                 port: int = app_config[dash_config_str]['port']
                 ):
        self.routes_pathname_prefix = routes_pathname_prefix
        self.requests_pathname_prefix = requests_pathname_prefix
        self.host = host
        self.threads = threads
        self.port = port

class db_config_cls():
    def __init__(self,
                 username: str = app_config[db_config_str]['username'],
                 password: str = app_config[db_config_str]['password'],
                 port: str = app_config[db_config_str]['port'],
                 server: str = app_config[db_config_str]['server'],
                 driver: str = app_config[db_config_str]['driver'],
                 database: str = app_config[db_config_str]['database'],
                 tbl_slider_data: str = app_config[db_config_str]['tbl_slider_data'],
                 tbl_slider_marks: str = app_config[db_config_str]['tbl_slider_marks']
                 ):
        self.username = username
        self.password = password
        self.port = port
        self.server = server
        self.driver = driver
        self.database = database
        self.tbl_slider_data = tbl_slider_data
        self.tbl_slider_marks = tbl_slider_marks

class app_config_cls():
    def __init__(self, config_file_name: str = config_file_name, config_file_dir_path: str = relative_path):
        self.config_file_name = config_file_name
        self.config_file_dir_path = config_file_dir_path
        self.config = read_yml_file(
            config_file_name=self.config_file_name, 
            config_file_path=self.config_file_dir_path
        )

        self.dash_config = dash_config_cls()
        self.db_config = db_config_cls()
        
class dynamic_attr_class(object):
    def __init__(self, **kwargs):
        for attr_name, value in kwargs.items():
            self.__dict__[attr_name] = value

if __name__ == '__main__':
    pass