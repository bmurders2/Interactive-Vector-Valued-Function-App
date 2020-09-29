import os
import sys
import yaml
import pyodbc
import numpy as np
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html

def get_env_var_value(env_var: str):
    return os.environ[env_var]

if __name__ == '__main__':
    sys.path.insert(0,get_env_var_value('app_working_dir'))

# custom module(s)
from helpers.app_config import app_config_cls

app_config = app_config_cls()

def get_db_value(env_var: str, app_config: app_config_cls = app_config):
    return get_env_var_value(
        env_var=app_config.db_config.__getattribute__(env_var)
    )

def dcc_slider_values(tab_label: str, div_id: str, slider_id: str, slider_min, slider_max, slider_marks, slider_value, slider_step,
                      slider_updatemode: str, div_style={'margin-top': 20}, make_slider_vertical: bool = False):
    return dcc.Tab(label=tab_label, children=[
        html.Div(id=div_id, style=div_style),
        dcc.Slider(
            id=slider_id,
            min=slider_min,
            max=slider_max,
            marks=slider_marks,
            value=slider_value,
            step=slider_step,
            updatemode=slider_updatemode,
            vertical=make_slider_vertical
        )
    ])

class gui_comp_other_params_cls():
    def __init__(self, param_name: str, value_str: str = None, comp_id_str: str = None, additional_value_str: str = 'NULL'):
        self.param_name = param_name
        self.comp_id_str = '{comp_id_str}_other_params_obj_id'.format(
            comp_id_str=param_name) if comp_id_str == None else comp_id_str
        self.value_str = param_name if value_str == None else value_str
        self.additional_value_str = additional_value_str


class gui_comp_slider_cls():
    def __init__(self, comp_name_str: str,
                 slider_min=None,
                 slider_max=None,
                 slider_marks=None,
                 slider_value=None,
                 slider_step=None,
                 slider_updatemode: str = 'mouseup',
                 tab_name_override_str: str = None
    ):
        self.comp_name = comp_name_str
        self.tab_title = '{comp_type_str}'.format(
            comp_type_str=comp_name_str if tab_name_override_str == None else tab_name_override_str
        )
        self.container_id_str = '{comp_type_str}_slider_label_key'.format(comp_type_str=comp_name_str)
        self.slider_id_str = '{comp_type_str}_slider_key'.format(comp_type_str=comp_name_str)
        self.slider_min = slider_min
        self.slider_max = slider_max
        self.slider_marks = slider_marks
        self.slider_value = slider_value
        self.slider_step = slider_step
        self.slider_updatemode = slider_updatemode


class gui_params_cls():
    def __init__(self, c: gui_comp_slider_cls = None, epsilon: gui_comp_slider_cls = None, random_sample_size: gui_comp_slider_cls = None,
                 actual_func_k: gui_comp_slider_cls = None, actual_func_alpha: gui_comp_slider_cls = None, noise_offset: gui_comp_slider_cls = None, noise_scale: gui_comp_slider_cls = None,
                 shuffle_data: gui_comp_other_params_cls = None, graph_container_id: gui_comp_other_params_cls = None, use_SQL_method: bool = True):

        
        if use_SQL_method == False:
            self.c = c
            self.epsilon = epsilon
            self.random_sample_size = random_sample_size
            self.actual_func_k = actual_func_k
            self.actual_func_alpha = actual_func_alpha
            self.noise_offset = noise_offset
            self.noise_scale = noise_scale
            self.shuffle_data = shuffle_data
            self.graph_container_id = graph_container_id
        else:
            self.query_db()

        self.gui_comp_list = [
            self.random_sample_size,
            self.c,
            self.epsilon,
            self.actual_func_k,
            self.actual_func_alpha,
            self.noise_offset,
            self.noise_scale,
            self.shuffle_data,
            self.graph_container_id
        ]

        self.tab_params_list = [
            self.random_sample_size,
            self.c,
            self.epsilon,
            self.actual_func_k,
            self.actual_func_alpha,
            self.noise_offset,
            self.noise_scale
        ]

    

    def query_db(self):
        def db_source(db_name: str, db_schema: str, db_obj: str):
            return '{db_name}.{db_schema}.{db_obj}'.format(
                db_name=db_name, db_schema=db_schema, db_obj=db_obj
            )

        def sql_qry(columns, db_source, post_syntax: str = ''):
            return 'select {columns} from {db_source} {post_syntax}'.format(
                columns=columns, db_source=db_source, post_syntax=post_syntax
            )
        
        def get_gui_other_params_results(data_obj, cls_obj = gui_comp_other_params_cls):
            return cls_obj(
                param_name=data_obj.param_name,
                comp_id_str=data_obj.comp_id_str,
                value_str=data_obj.value_str,
                additional_value_str=data_obj.additional_value_str
            )

        def get_gui_comp_slider_results(data_obj, slider_marks, cls_obj = gui_comp_slider_cls):
            return cls_obj(
                    comp_name_str=data_obj.slider_id,
                    slider_min=data_obj.slider_min,
                    slider_max=data_obj.slider_max,
                    slider_value=data_obj.slider_value,
                    slider_step=data_obj.slider_step,
                    tab_name_override_str=data_obj.tab_name_override_str,
                    slider_marks=slider_marks
            )

        username, password, port, server, driver, db_name, db_schema, db_tbl_slider_data, db_tbl_slider_marks, db_tbl_other_params = app_config.db_config.get_db_params()

        tbl_slider_data_columns = 'slider_id, slider_min, slider_max, slider_value, slider_step, tab_name_override_str'
        tbl_slider_data_post_syntax = 'order by slider_id asc, slider_min, slider_max, slider_value, slider_step, tab_name_override_str'

        tbl_slider_marks_columns = 'slider_id, mark_value'
        tbl_slider_marks_post_syntax = 'order by slider_id asc, mark_value asc'

        tbl_other_params_columns = 'param_name, comp_id_str, value_str, additional_value_str'
        tbl_other_params_post_syntax = 'order by param_name asc, comp_id_str asc, value_str asc, additional_value_str asc'

        # [ <class attr name>, <qry value name> ]
        tbl_slider_attr_list = [
            ['noise_offset','noise_offset'],
            ['noise_scale', 'noise_scale'],
            ['actual_func_alpha','predict_func_alpha'],
            ['actual_func_k','predict_func_k'],
            ['c','svr_c'],
            ['epsilon','svr_epsilon'],
            ['random_sample_size','svr_random_sample_size']
        ]
        tbl_other_params_attr_list = [
            ['shuffle_data','shuffle_data'],
            ['graph_container_id','main_plot_container_id']
        ]

        qry_params_list = [
            [tbl_other_params_columns, db_source(db_name, db_schema, db_tbl_other_params), tbl_other_params_post_syntax],
            [tbl_slider_data_columns, db_source(db_name, db_schema, db_tbl_slider_data), tbl_slider_data_post_syntax],
            [tbl_slider_marks_columns, db_source(db_name, db_schema, db_tbl_slider_marks), tbl_slider_marks_post_syntax]
        ]

        sql_queries = [
            sql_qry(column_list, tbl_name, post_syntax) for column_list, tbl_name, post_syntax in qry_params_list
        ]

        # connect and qury dev db
        cn_str = 'DRIVER={driver};SERVER={server};UID={username};PWD={password}'.format(
            driver='{'+driver+'}', server=server, username=username, password=password
        )
        cnxn = pyodbc.connect(cn_str)

        # return query results as dataframes
        other_params_data, slider_data, slider_marks = [
            pd.read_sql(qry,cnxn) for qry in sql_queries
        ]

        # get other params gui data -- assumes rows are itemized gui objs
        for gui_other_params_obj in other_params_data.itertuples():
            for attr_name_str, param_name_str in tbl_other_params_attr_list:
                if gui_other_params_obj.param_name == param_name_str:
                    # set class attribute
                    self.__setattr__(attr_name_str, get_gui_other_params_results(data_obj=gui_other_params_obj))

        # get slider gui data (including marks) -- assumes rows are itemized gui objs
        for gui_slider_obj in slider_data.itertuples():
            for attr_name_str, slider_id_str in tbl_slider_attr_list:
                if gui_slider_obj.slider_id == slider_id_str:

                    # filter the slider marks dataframe to given gui comp and return sorted mark values
                    data_mark_values = slider_marks[slider_marks.slider_id==slider_id_str]['mark_value']. \
                        sort_values(ascending=True).to_list()
                    # format data mark values to match with dcc.slider and check if marks should be 'int' or 'float'
                    #  -- can sometimes mess with gui display tick marks if mark value types aren't 'correct'
                    data_mark_values = {
                        int(value) if int(value) == float(value) else float(value): str(value) for value in data_mark_values
                    }

                    # set class attribute
                    self.__setattr__(attr_name_str, get_gui_comp_slider_results(
                        data_obj=gui_slider_obj, slider_marks=data_mark_values)
                    )

        return None

    def get_dcc_slider(self, gui_slider_comp: gui_comp_slider_cls):
        obj = gui_slider_comp
        return dcc_slider_values(
            tab_label=obj.tab_title,
            div_id=obj.container_id_str,
            slider_id=obj.slider_id_str,
            slider_min=obj.slider_min,
            slider_max=obj.slider_max,
            slider_marks=obj.slider_marks,
            slider_value=obj.slider_value,
            slider_step=obj.slider_step,
            slider_updatemode=obj.slider_updatemode
        )

if __name__ == '__main__':
    pass
