import os
import sys
import yaml
import pyodbc
import subprocess
import numpy as np
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html


if __name__ == '__main__':
    sys.path.insert(0,os.environ['app_working_dir'])

# custom module(s)
from helpers.app_config import app_config_cls
from helpers.gui_setup import gui_comp_other_params_cls, gui_comp_slider_cls, gui_params_cls

app_config = app_config_cls()

def get_default_gui_cls_values(use_SQL_method: bool = False):
    c = gui_comp_slider_cls(
        comp_name_str='svr_c',
        slider_min=100,
        slider_max=100000,
        slider_marks={
            i*10000: '{num}'.format(num=i*10000) for i in range(11)
        },
        slider_value=5000,
        slider_step=100,
        tab_name_override_str='SVR Model Parameter: Regularization'
    )
    epsilon = gui_comp_slider_cls(
        comp_name_str='svr_epsilon',
        slider_min=0.1,
        slider_max=10,
        slider_marks={
            i: '{num}'.format(num=i) for i in range(11)
        },
        slider_value=0.3,
        slider_step=.1,
        tab_name_override_str='SVR Model Parameter: Training Loss No-Penalty Range'
    )
    random_sample_size = gui_comp_slider_cls(
        comp_name_str='svr_random_sample_size',
        slider_min=25,
        slider_max=500,
        slider_marks={
            i*25: '{num}'.format(num=i*25) for i in range(21)
        },
        slider_value=250,
        slider_step=25,
        tab_name_override_str='Random Sample Size'
    )
    actual_func_k = gui_comp_slider_cls(
        comp_name_str='predict_func_k',
        slider_min=0.01,
        slider_max=0.50,
        slider_marks={
            i/20: '{num}'.format(num=i/20) for i in range(21)
        },
        slider_value=0.25,
        slider_step=0.01,
        tab_name_override_str='Actual Function Parameter: k'
    )
    actual_func_alpha = gui_comp_slider_cls(
        comp_name_str='predict_func_alpha',
        slider_min=-3,
        slider_max=3,
        slider_marks={
            value: '{num}'.format(num=value) for value in [
                -3, -2, -1, 0, 1, 2, 3
            ]
        },
        slider_value=1.0,
        slider_step=0.01,
        tab_name_override_str='Actual Function Parameter: alpha'
    )
    noise_offset = gui_comp_slider_cls(
        comp_name_str='noise_offset',
        slider_min=0.01,
        slider_max=10,
        slider_marks={
            i: '{num}'.format(num=i) for i in range(11)
        },
        slider_value=0.50,
        slider_step=0.01,
        tab_name_override_str='Observations Data: Noise Deviation Addition'
    )
    noise_scale = gui_comp_slider_cls(
        comp_name_str='noise_scale',
        slider_min=0.01,
        slider_max=10,
        slider_marks={
            i: '{num}'.format(num=i) for i in range(11)
        },
        slider_value=2.00,
        slider_step=0.01,
        tab_name_override_str='Observations Data: Noise Deviation Magnitude'
    )
    graph_container_id = gui_comp_other_params_cls('main_plot_container_id')

    shuffle_data = gui_comp_other_params_cls(
        param_name='shuffle_data', value_str='False', additional_value_str='Use Fixed Random Seed for Data:')
    
    var = gui_params_cls(
        c=c,
        epsilon=epsilon,
        random_sample_size=random_sample_size,
        actual_func_k=actual_func_k,
        actual_func_alpha=actual_func_alpha,
        noise_offset=noise_offset,
        noise_scale=noise_scale,
        shuffle_data=shuffle_data,
        graph_container_id=graph_container_id,
        use_SQL_method=use_SQL_method
    )

    return var

if __name__ == '__main__':

    def insert_into_table_str(db_name, db_schema, db_table, db_columns, db_value_list):
        return "INSERT INTO {db_name}.{db_schema}.{table_name} {table_columns} {values}".format(
            db_name=db_name,
            db_schema=db_schema,
            table_name=db_table,
            table_columns=db_columns,
            values=db_value_list
        )

    try:
        sh_seed_file_name = app_config.get_env_var_value('mssql_seed_db_sh_file_name')

        relative_path = os.path.realpath(os.path.join(
            os.getcwd(), os.path.dirname(__file__))
        )
        
        db_data_seed = get_default_gui_cls_values().gui_comp_list


        username, password, port, server, driver, db_name, db_schema, db_tbl_slider_data, db_tbl_slider_marks, db_tbl_other_params = app_config.db_config.get_db_params()

        # call on bash file to set the dev db
        sh_file = "{dir}/{bash_script}".format(
            dir=relative_path, bash_script=sh_seed_file_name
        )
        sh_file_x_cmd = 'bash {sh_file}'.format(sh_file=sh_file)
        subprocess.call(sh_file_x_cmd, shell=True)

        cn_str = 'DRIVER={driver};SERVER={server};UID={username};PWD={password}'.format(
            driver='{'+driver+'}',
            server=server,
            username=username,
            password=password
        )
        cnxn = pyodbc.connect(cn_str)
        cursor = cnxn.cursor()

        # seed the dev db
        for gui_element in db_data_seed:

            # check if pertains to other params table
            if hasattr(gui_element, 'param_name'):
                # fill other params table
                cursor.execute(
                    insert_into_table_str(
                        db_name=db_name,
                        db_schema=db_schema,
                        db_table=db_tbl_other_params,
                        db_columns='(param_name,comp_id_str,value_str,additional_value_str)',
                        db_value_list='values (?,?,?,?)'
                    ),
                    str(gui_element.param_name),
                    str(gui_element.comp_id_str),
                    str(gui_element.value_str),
                    str(gui_element.additional_value_str) if gui_element.additional_value_str != 'NULL' else None
                )

            # slider tab tables
            else:
                # fill slider table
                cursor.execute(
                    insert_into_table_str(
                        db_name=db_name,
                        db_schema=db_schema,
                        db_table=db_tbl_slider_data,
                        db_columns='(slider_id,slider_min,slider_max,slider_value,slider_step,tab_name_override_str)',
                        db_value_list='values (?,?,?,?,?,?)'
                    ),
                    str(gui_element.comp_name),
                    float(gui_element.slider_min),
                    float(gui_element.slider_max),
                    float(gui_element.slider_value),
                    float(gui_element.slider_step),
                    str(gui_element.tab_title)
                )

                # fill slider marks table
                df_slider_marks = pd.DataFrame(
                    [value for value, str_value in gui_element.slider_marks.items()], columns={gui_element.comp_name}
                )
                
                for index, row in df_slider_marks.iterrows():
                    cursor.execute(
                        insert_into_table_str(
                            db_name=db_name,
                            db_schema=db_schema,
                            db_table=db_tbl_slider_marks,
                            db_columns='(slider_id,mark_value)',
                            db_value_list='values (?,?)'
                        ),
                        str(gui_element.comp_name),
                        float(row.values)
                    )

        # save changes
        cnxn.commit()
        cursor.close()
        print('Seeded dev database from python script')

    except:
        print('***Error: Attempted to seed the dev database but something went wrong.***')
