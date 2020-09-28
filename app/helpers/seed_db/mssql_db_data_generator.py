import dash_core_components as dcc
import dash_html_components as html

import os
import sys
import yaml
import pyodbc
import pandas as pd


if __name__ == '__main__':
    sys.path.insert(0,os.environ['app_working_dir'])

from helpers.app_config import app_config_cls
from helpers.gui_setup import gui_comp_slider_cls, gui_params_cls

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
    shuffle_data = gui_comp_slider_cls(
        'shuffle_data', tab_name_override_str='Use Fixed Random Seed for Data:')

    var = gui_params_cls(
        c=c,
        epsilon=epsilon,
        random_sample_size=random_sample_size,
        actual_func_k=actual_func_k,
        actual_func_alpha=actual_func_alpha,
        noise_offset=noise_offset,
        noise_scale=noise_scale,
        shuffle_data=shuffle_data,
        use_SQL_method=use_SQL_method
    )

    return var

# if __name__ == '__main__':
#     db_data_seed = get_default_gui_cls_values()
#     def get_db_value(env_var: str):
#         return os.environ[app_config.db_config.__getattribute__(env_var)]
    
#     relative_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#     var = db_data_seed.c
#     df = pd.DataFrame( 
#         [value for value, str_value  in var.slider_marks.items()],columns={var.comp_name}
#     )
#     print(df.head(10))

#     driver, server, username, password, port = [
#         get_db_value(value) for value in ['driver','server','username','password','port']
#     ]
#     cn_str = 'DRIVER={driver};SERVER={server};UID={username};PWD={password}'.format(
#             driver='{'+driver+'}',
#             server=server,
#             username=username,
#             password=password
#         )
#     cnxn = pyodbc.connect(cn_str)
    
#     cursor = cnxn.cursor()
#     for index, row in df.iterrows():
#         cursor.execute(
#             "INSERT INTO {table_name} (slider_id,mark_value) values(?,?)".format(table_name=app_config.table_name), row.svr_c, row.mark_value
#         )
#     cursor.commit()
#     # insert dataframe into SQL Server:
#     for index, row in df.iterrows():
#         cursor.execute(
#             "INSERT INTO test_table (type,ref_name) values(?,?)", row.type, row.ref_name
#         )

#     cursor.execute('SELECT @@VERSION as [SQL SERVER VERSION DETAILS]')
#     for row in cursor:
#         print('MS SQL Server Version: \n{version}'.format(version=row))

#     cnxn.commit()
#     cursor.close()
#     print('Seeded dev db from python script')

    # except:
    #     print('***Error: Attempted to seed the dev database but something went wrong.***')


if __name__ == '__main__':
    try:        
        def get_db_value(env_var: str):
            return os.environ[app_config.db_config.__getattribute__(env_var)]
        
        relative_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        file_name = '{relative_path}/_tmp_test_import.csv'.format(relative_path=relative_path)
        df = pd.read_csv(file_name)

        driver, server, username, password, port = [
            get_db_value(value) for value in ['driver','server','username','password','port']
        ]
        cn_str = 'DRIVER={driver};SERVER={server};UID={username};PWD={password}'.format(
                driver='{'+driver+'}',
                server=server,
                username=username,
                password=password
            )
        cnxn = pyodbc.connect(cn_str)
        
        cursor = cnxn.cursor()
        cursor.execute('DROP TABLE IF EXISTS test_table')
        cursor.execute('''
            create table test_table(
                type nvarchar(100) NOT NULL,
                ref_name nvarchar(100) NOT NULL
            )
        ''')
        cursor.commit()
        # insert dataframe into SQL Server:
        for index, row in df.iterrows():
            cursor.execute(
                "INSERT INTO test_table (type,ref_name) values(?,?)", row.type, row.ref_name
            )

        cursor.execute('SELECT @@VERSION as [SQL SERVER VERSION DETAILS]')
        for row in cursor:
            print('MS SQL Server Version: \n{version}'.format(version=row))

        cnxn.commit()
        cursor.close()
        print('Seeded dev db from python script')

    except:
        print('***Error: Attempted to seed the dev database but something went wrong.***')

