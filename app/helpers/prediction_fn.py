import numpy as np
import pandas as pd
from sklearn.svm import SVR


def prediction_func(
    random_sample_size: int, svr_c: int, svr_epsilon: float,
    actual_func_k: float, actual_func_alpha: float,
    noise_offset: float, noise_scale: float,
    shuffle_random_data: bool = False
):

    # function(s)
    def concat_df(dataframe_var: pd.DataFrame, column_name: str, data_var):
        return pd.concat([dataframe_var, pd.DataFrame(data_var, columns={column_name})], ignore_index=False, axis=1)

    def add_noise(t_dim, offset: float = 2.5, scale: float = 1.5):
        def random_noise(mean, noise_scale):
            return np.random.normal(mean, noise_scale)

        delta_t = offset + scale * np.random.random(t_dim.shape)
        t_dim += random_noise(mean=0.0, noise_scale=delta_t)
        return t_dim

    def actual_func_1(t, k: float, alpha: float):
        k = k if k != 0.0 else 0.0000001
        r = alpha * np.exp(k * t)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return x.astype(float), y.astype(float)

    def actual_func(t, func, *params):
        return func(t, *params)

    # declaration(s)
    random_seed = 42
    np.random.seed(random_seed) if not shuffle_random_data else None
    min_range = 0.0
    prediction_max_range = 5 * np.pi
    prediction_sample_size = 1000
    random_sample_size = random_sample_size
    random_sample_max_range = prediction_max_range
    df = pd.DataFrame()

    actual_func_params = (actual_func_1, actual_func_k, actual_func_alpha)

    # create observation(s)
    t_sample = np.atleast_2d(np.random.uniform(min_range, int(random_sample_max_range), size=int(random_sample_size))).T
    t_sample = np.sort(t_sample, axis=0)
    x, y = actual_func(t_sample, *actual_func_params)
    x, y = [add_noise(axis_dim.ravel(), offset=noise_offset,
                      scale=noise_scale) for axis_dim in [x, y]
    ]

    # create 't' steps for making predictions along curve
    t_predict = np.atleast_2d(np.linspace(min_range, int(prediction_max_range), int(prediction_sample_size))).T
    t_predict = np.sort(t_predict, axis=0)

    predict_model_x, predict_model_y = [SVR(
        kernel='rbf', gamma='scale', C=svr_c, epsilon=svr_epsilon) for model in range(2)
    ]

    # train model(s)
    predict_model_x, predict_model_y = [
        predict_model.fit(t_sample, axis_dim) for predict_model, axis_dim in [
            [predict_model_x, x],
            [predict_model_y, y]
        ]
    ]

    # predict with trained model(s)
    x_pred, y_pred = [
        predict_model.predict(value_array) for predict_model, value_array in [
            [predict_model_x, t_predict],
            [predict_model_y, t_predict]
        ]
    ]
    # print(predict_model_x.support_vectors_)
    # load predictions into dataframe
    df['X Actual Function'], df['Y Actual Function'] = actual_func(
        t_predict.ravel(), *actual_func_params
    )
    df['X Prediction'], df['Y Prediction'], df['t'] = x_pred, y_pred, t_predict

    # sample data
    df = concat_df(df, 'X Sample Data', x)
    df = concat_df(df, 'Y Sample Data', y)

    # support vectors
    ## grab all unique sv indices for both SVR models from training data and plot together as total support vectors
    concat_models = (predict_model_x.support_, predict_model_y.support_)
    total_support_vector_indices = np.unique(
        np.concatenate(concat_models, axis=0), axis=0
    )
    ## use numpy.take because 'support_vectors_' returns sorted array
    df = concat_df(df, 'X Support Vectors', np.take(
        a = x, indices = total_support_vector_indices)
    )
    df = concat_df(df, 'Y Support Vectors', np.take(
        a = y, indices = total_support_vector_indices)
    )
    return df

if __name__ == '__main__':
    pass