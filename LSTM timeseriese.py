import os
import pandas as pd
import numpy as np
from datetime import datetime
import tsfresh as ts

# read created csv  files sensors
# split Report_camdata csv based on
# and then map them to report cam data
# save csv files in the mapped data folder
from tsfresh import extract_features


def map_sensors_cam_data(data_folder):
    global layer_data
    print('mapping sensors and error data')
    # data_folder = 'original data/20220924 4 bit'
    files = os.listdir(data_folder + '/CSV')
    sensory_data = []
    sensory_data_features = []
    for f in files:
        file_path = data_folder + '/CSV/' + f
        # d-s dtr ltr data
        layer_data = pd.read_csv(file_path)
        grouped = layer_data.groupby(layer_data.index//5)
        print(grouped)


        sensory_data.append(layer_data)


map_sensors_cam_data('original data/20220924 4 bit')
