import dash_core_components as dcc
import dash_html_components as html


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
    def __init__(self):
        self.graph_container_id = 'main_plot_container_id'

        self.c = gui_comp_slider_cls(
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
        self.epsilon = gui_comp_slider_cls(
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
        self.random_sample_size = gui_comp_slider_cls(
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
        self.actual_func_k = gui_comp_slider_cls(
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
        self.actual_func_alpha = gui_comp_slider_cls(
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
        self.noise_offset = gui_comp_slider_cls(
            comp_name_str='noise_offset',
            slider_min=0.01,
            slider_max=10,
            slider_marks={
                i: '{num}'.format(num=i) for i in range(11)
            },
            slider_value=0.50,
            slider_step=0.01,
            tab_name_override_str='Obvservations Data: Noise Deviation Addition'
        )
        self.noise_scale = gui_comp_slider_cls(
            comp_name_str='noise_scale',
            slider_min=0.01,
            slider_max=10,
            slider_marks={
                i: '{num}'.format(num=i) for i in range(11)
            },
            slider_value=2.00,
            slider_step=0.01,
            tab_name_override_str='Obvservations Data: Noise Deviation Magnitude'
        )
        self.shuffle_data = gui_comp_slider_cls(
            'shuffle_data', tab_name_override_str='Use Fixed Random Seed for Data:')

        self.tab_params_list = [
            self.random_sample_size,
            self.c,
            self.epsilon,
            self.actual_func_k,
            self.actual_func_alpha,
            self.noise_offset,
            self.noise_scale
        ]


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


def dcc_slider_wrapper(obj: gui_comp_slider_cls):
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
