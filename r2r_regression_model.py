import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor as reg


def run_regression_model(data_folder, error_cam, camera):
    print('running regression model')
    # CREate folders to save analysis results
    sub_folder = 'mapped data'
    sub_path = data_folder + '/' + sub_folder
    layers = os.listdir(sub_path)

    all_data = []
    ts = []
    x = []
    zoom = []
    film = []
    for l in layers:
        file_path = sub_path + '/' + l
        df = pd.read_csv(file_path)

        df_ts = df['timestamp']  # store timestamp

        # create frequency variable
        freq = np.unique(df_ts, return_counts=True)[1]
        all_freq = []
        for fr in freq:
            for i in range(fr):
                all_freq.append(fr)
        all_freq = pd.Series(all_freq)

        df = df.iloc[:, 10:]  # start from flim result x
        film_result = df.iloc[:, error_cam:error_cam + 1]
        zoom_result = df.iloc[:, 10:12]
        input_x = df.iloc[:, 14:]
        input_x = pd.concat([all_freq, input_x], axis=1)

        # To use nip as input
        # nip1 = input_x.iloc[:, 2:4]
        # nip2 = input_x.iloc[:, 6:8]
        # input_x = pd.concat([nip1, nip2], axis=1)
        film.append(film_result)
        zoom.append(zoom_result)
        x.append(input_x)
        ts.append(df_ts)
        # input_x = pd.concat([layer[0], layer[1],
        #                    layer[4]], axis=1)
    a = x[0]
    b = film[0]
    c = zoom[0]
    del x[0]
    del film[0]
    del zoom[0]

    # LINEAR MODEL SHOWS VERY POOR RESULTS
    # Try random forest regression
    # ts = pd.concat(ts, axis=0)
    x2 = pd.concat(x, axis=0)
    # x2 = pd.concat([ts, x2], axis=1)
    film2 = pd.concat(film, axis=0)
    zoom2 = pd.concat(zoom, axis=0)
    x_y_data = pd.concat([x2, film2, zoom2], axis=1)
    # save mapped data file
    x_y_data.to_csv(data_folder + '/'
                    + 'mapped_data_all.csv')

    # xtr, xtest, film_tr, film_test = train_test_split(x2, film2)

    # print(film_test.shape)
    def train_model(xtr, film_tr, xtest, film_test):
        # random forest regression
        rf = reg(max_features='auto')
        m = rf.fit(xtr, film_tr)
        R2 = rf.score(xtr, film_tr)

        OOR2 = rf.score(xtest, film_test)

        features_imp = rf.feature_importances_

        print('model training and testing complete')

        def create_plots():
            # x_axis = np.arange((len(film_test)))
            print('saving plots')
            y_pred = rf.predict(xtest)
            plt.subplot(2, 1, 1)
            plt.plot(ts[0], y_pred, label='predicted error')
            plt.xlabel('Time')
            plt.ylabel('predicted error')
            plt.title('predicted and actual' + camera)
            plt.subplot(2, 1, 2)
            plt.plot(ts[0], film_test, label='actuak error')
            plt.xlabel('Time')
            plt.ylabel('actual error')
            plt.legend()
            plt.savefig('predicted and actual' + camera + '.pdf')
            # plt.show()

        create_plots()
        return R2, OOR2, features_imp

    return train_model(x2, film2, a, b)

