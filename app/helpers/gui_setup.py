import dash_core_components as dcc
import dash_html_components as html


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
    def __init__(self, c: gui_comp_slider_cls=None, epsilon: gui_comp_slider_cls=None, random_sample_size: gui_comp_slider_cls=None, actual_func_k: gui_comp_slider_cls=None, actual_func_alpha: gui_comp_slider_cls=None,
                 noise_offset: gui_comp_slider_cls=None, noise_scale: gui_comp_slider_cls=None, shuffle_data: gui_comp_slider_cls=None, graph_container_id: str = 'main_plot_container_id', use_SQL_method: bool = True):

        if use_SQL_method == False:
            self.graph_container_id = graph_container_id

            self.c = c
            self.epsilon = epsilon
            self.random_sample_size = random_sample_size
            self.actual_func_k = actual_func_k
            self.actual_func_alpha = actual_func_alpha
            self.noise_offset = noise_offset
            self.noise_scale = noise_scale
            self.shuffle_data = shuffle_data
        else:
            self.query_db()

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
        print('made it here')

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