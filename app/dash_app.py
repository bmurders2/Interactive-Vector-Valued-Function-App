import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import os
import yaml
import numpy as np
import pandas as pd


# custom import(s)
import helpers.gui_setup as gui_setup
from helpers.seed_db.mssql_db_data_generator import get_default_gui_cls_values
from helpers.prediction_fn import prediction_func
from helpers.app_config import app_config_cls

# initialize gui helper class
gui_params = get_default_gui_cls_values()
app_config = app_config_cls()

app = dash.Dash(__name__)
app.config.update({
    'routes_pathname_prefix': app_config.dash_config.routes_pathname_prefix, #app_config['dash_config']['routes_pathname_prefix'],
    'requests_pathname_prefix': app_config.dash_config.requests_pathname_prefix #app_config['dash_config']['requests_pathname_prefix']
})
# serve as Flask app
flask_app = app.server

# app layout
app.layout = html.Div([
    html.H2(
        children='Interactive Support Vector Machine for Regression (SVR) Demo',
        style={'textAlign': 'center'}
    ),
    html.H4(
        children='Actual Function (Logarithmic Spiral): c(t) = <[alpha * e^(k * t) * cos(t)], [alpha * e^(k * t) * sin(t)]>',
        style={'textAlign': 'left'}
    ),
    html.Div([
        # plot
        html.Div(
            html.Div(id=gui_params.graph_container_id),
        ),
        # determine if data should be random or fixed with a seed
        html.Div([
            html.Div(
                html.P(gui_params.shuffle_data.tab_title),
                style={'display': 'inline-block'}
            ),
            html.Div(
                dcc.RadioItems(
                    id=gui_params.shuffle_data.container_id_str,
                    options=[
                        {'label': 'True', 'value': 'True'},
                        {'label': 'False', 'value': 'False'}
                    ], value='False'
                ),
                style={'display': 'inline-block'}
            ),
        ]),
        # return array of interactive sliders as a tab list (horizontal)
        html.Div(
            dcc.Tabs(vertical=False, children=[
                gui_params.get_dcc_slider(obj) for obj in gui_params.tab_params_list
                # gui_setup.dcc_slider_wrapper(obj) for obj in gui_params.tab_params_list
            ]),
        ),
    ])
])

# update gui sliders
@app.callback(
    [Output(obj.container_id_str, 'children') for obj in gui_params.tab_params_list],
    [Input(obj.slider_id_str, 'value') for obj in gui_params.tab_params_list]
)
def slider_strs_update(random_sample_size, svr_c, svr_epsilon, actual_func_k, actual_func_alpha, noise_offset, noise_scale):
    return (
        'random sample size: {value}'.format(value=random_sample_size),
        'regularization value: {value}'.format(value=svr_c),
        'training loss no-penalty range: {value}'.format(value=svr_epsilon),
        'prediction function parameter "k" value: {value}'.format(value=actual_func_k),
        'prediction function parameter "alpha" value: {value}'.format(value=actual_func_alpha),
        'observation noise deviation offset value: {value}'.format(value=noise_offset),
        'observation noise deviation scale value: {value}'.format(value=noise_scale)
    )

# update plot
@app.callback(
    Output(gui_params.graph_container_id, 'children'),
    (
        [Input(obj.slider_id_str, 'value') for obj in gui_params.tab_params_list] +
        [Input(gui_params.shuffle_data.container_id_str, 'value')]
    )
)
def update_graph(random_sample_size, svr_c, svr_epsilon, actual_func_k, actual_func_alpha, noise_offset, noise_scale, shuffle_data):
    
    # train model and return predictions in a pandas dataframe
    dff = prediction_func(
        random_sample_size=random_sample_size,
        svr_c=svr_c,
        svr_epsilon=svr_epsilon,
        actual_func_k=actual_func_k,
        actual_func_alpha=actual_func_alpha,
        noise_offset=noise_offset,
        noise_scale=noise_scale,
        shuffle_random_data=True if shuffle_data == 'True' else False
    )

    # lists to reference from in dcc.Graph
    column_list = [
        ['X Actual Function', 'Y Actual Function'],
        ['X Prediction', 'Y Prediction'],
        ['X Sample Data', 'Y Sample Data'],
        ['X Support Vectors', 'Y Support Vectors']
    ]
    data_points_list = ['X Sample Data', 'X Support Vectors']

    # return plot in JSON format
    return [
        dcc.Graph(
            id='graph_id',
            animate=True,
            config={
                'responsive': True,
                'showTips': True
            },
            figure={
                'data': [
                    {
                        'x': dff[column_x],
                        'y': dff[column_y],
                        'name': '{col_name}'.format(col_name=column_x.replace('X ', '')),
                        'legend': 'legendonly',
                        'type': 'line' if column_x not in data_points_list else 'scatter',
                        'line': {'shape': 'linear' if column_x not in data_points_list else None},
                        'mode': 'markers' if column_x in data_points_list else None
                    } for column_x, column_y in column_list if column_x in dff.columns
                ],
                'layout': {
                    'xaxis': {'automargin': True},
                    'yaxis': {'automargin': True},
                    'autosize': True,
                    'automargin': True,
                    'width': '1500',
                    'height': '850',
                    'hovermode': 'closest',
                    'legend': {
                        'orientation': 'v'
                    }
                },
            },
        )
    ]


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=app_config.dash_config.port,
        host=app_config.dash_config.host
    )
