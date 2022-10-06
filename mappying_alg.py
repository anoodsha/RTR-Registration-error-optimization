# import
import os
import pandas as pd
import numpy as np
from datetime import datetime


# read created csv  files sensors
# split Report_camdata csv based on
# and then map them to report cam data
# save csv files in the mapped data folder
def map_sensors_cam_data(data_folder):
    print('mapping sensors and error data')
    # data_folder = 'original data/20220924 4 bit'
    files = os.listdir(data_folder + '/CSV')
    sensory_data = []
    sensory_data_features = []
    for f in files:
        file_path = data_folder + '/CSV/' + f
        # d-s dtr ltr data
        layer_data = pd.read_csv(file_path)

        sensory_data.append(layer_data)

    # data from report file
    errors = pd.read_csv(data_folder + '/Report_CamData.csv')

    # add timestamp to report file
    error_ts = []
    for t in range(len(errors)):
        ts = datetime(year=2022
                      , month=9, day=errors.iloc[t, 0], hour=errors.iloc[t, 1],
                      minute=errors.iloc[t, 2],
                      second=errors.iloc[t, 3])
        error_ts.append(ts)

    _ts = pd.DataFrame(error_ts, columns=['timestamp'])
    errors = pd.concat([_ts, errors], axis=1)
    # print(errors.columns)

    # split data based on layers

    t_end = 0
    t_start = 0
    layer_added = 0
    lay = []
    for t in range(len(errors) - 1):
        if t == len(errors) - 2:
            l = errors.iloc[t_start:, :]
            layer_added = layer_added + 1
            # print(l.shape)
            lay.append(l)

        exact_time = errors.iloc[t, 0]

        t = t + 1
        t2 = errors.iloc[t, 0]

        diff_sec = (t2 - exact_time).total_seconds()
        t = t - 1
        if diff_sec > 600:
            # print(t)
            t_end = t + 1
            l = errors.iloc[t_start:t_end, :]
            layer_added = layer_added + 1
            t_start = t_end

            # print(t_end)
            # print(l.shape)
            lay.append(l)
    # create report files
    layers = [lay[2], lay[0], lay[1]]
    report_path = 'report'
    report_path = os.path.join(data_folder, report_path)
    if not os.path.isdir(report_path):
        os.mkdir(report_path)
    layers[0].to_csv(report_path + '/d_s_report.csv')
    layers[1].to_csv(report_path + '/dtr_report.csv')
    layers[2].to_csv(report_path + '/ltr_report.csv')

    new_layers = []
    new_sensory = []

    for i in range(3):
        l = layers[i]
        s = sensory_data[i]

        # fix report data
        init_min = l['Minute'].unique()[0]
        # convert seconds columsn

        l.loc[l['Minute'] > init_min,
              'Second'] = l['Second'] + \
                          59 * (l['Minute'] -
                                init_min)
        l['Second'] = l['Second'] - l['Second'].values[0]

        # index col

        # fix sensors data split based on seconds

        # mapping
        second_count = np.unique(l['Second'], return_counts=True)
        sec = second_count[0]
        rep = second_count[1]

        # delete rows with no printing
        # print(l.shape)
        c = 0

        for j in range(len(second_count[0])):

            if rep[j] == 2:
                printing_start = sec[j]
                l = l.loc[(l['Second'] >= sec[j])]
                c = c + 1
            if c == 3:
                break

        # print('after rows deleted')
        start_time = l['timestamp'].unique()[0]

        # recalculate rep and sec
        second_count = np.unique(l['Second'], return_counts=True)
        sec = second_count[0]
        rep = second_count[1]

        s_ts = pd.to_datetime(s['ts'])
        s_ts.columns = ['ts']
        del s['ts']
        s = pd.concat([s_ts, s], axis=1)
        # print(s.head())
        # print(s)
        s = s.loc[s['ts'] >= start_time]

        splits = []
        ID = 0
        col_id = []
        for inx in range(s.index[0], s.index[len(s) - 1], 5):
            row_id = np.repeat(ID, 5)
            row_id = pd.DataFrame(row_id)
            row_id.columns = ['id']
            col_id.append(row_id)

            split = s.loc[inx: inx + 4]
            # for correct grouping
            split = split.reset_index()
            #split = pd.concat([row_id, split], axis=1)
            ID = ID + 1

            splits.append(split)


        print('all splits', len(splits))

        # store new data
        mapping = []
        useful_ts = []

        del splits[len(splits) - 1]
        s = 0
        min_sec = sec[0]
        for re, se in zip(rep, sec):
            map_xy = splits[se - min_sec]
            split_ts = pd.to_datetime(map_xy['ts'])
            # split_ts = split_ts.resample(str(5/re)+'S')
            mean_val = map_xy.groupby(map_xy.index // (5 / re)).mean()
            # mean_val = map_xy.resample(str(5/re) + 'S').mean()

            s = s + len(mean_val)
            # new averaed input

            mapping.append(mean_val)

            useful_ts.append(split_ts)

        # final data and index resetting
        l = l.reset_index()
        print(l.shape)
        # print(l['Second'].values)

        new_map = pd.concat(mapping, axis=0, ignore_index=True)
        # print(new_map.shape)
        new_layers.append(l)
        new_sensory.append(new_map)
        # print(l.loc[l['Second'] == 300])
        # print(splits[300 - min_sec])
        # print(split_ts)

    # print(l['Second'].values)

    print('confirmed maooed data dimensions')
    print(new_layers[2].shape)
    print(new_sensory[2].shape)

    ltr_data = pd.concat([new_layers[2],
                          new_sensory[2]],
                         axis=1,
                         ignore_index=False)

    dtr_data = pd.concat([new_layers[1],
                          new_sensory[1]],
                         axis=1, ignore_index=False)

    d_s_data = pd.concat([new_layers[0],
                          new_sensory[0]],
                         axis=1, ignore_index=False)

    # print(ltr_data)

    # print(dtr_data)
    # print(d_s_data)

    mapping_path = 'mapped data'
    mapping_path = os.path.join(data_folder, mapping_path)
    if not os.path.isdir(mapping_path):
        os.mkdir(mapping_path)
    crop_col = ['Unnamed: 0',
                'index', 'FileName']
    for col in crop_col:
        del ltr_data[col]
        del dtr_data[col]
        del d_s_data[col]
    ltr_data.to_csv(mapping_path + '/combined_ltr.csv', index=False)
    dtr_data.to_csv(mapping_path + '/combined_dtr.csv', index=False)

    d_s_data.to_csv(mapping_path + '/combined_d-s.csv', index=False)



