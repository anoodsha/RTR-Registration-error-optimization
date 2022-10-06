
import pandas as pd
from datetime import datetime
import datetime as dt
import os
import shutil
import matplotlib.pyplot as plt


def txt_to_csv(data_folder):
    #raw data path
    print('convert text files to csv')
    src_path = data_folder + '/'
    folder_files = os.listdir(data_folder)
    csv_folder = 'CSV'
    splitting = 'splitting'
    csv_path = os.path.join(data_folder, csv_folder)
    split_path = os.path.join(data_folder, splitting)
    layer_folders = ['D-S', 'DTR', 'LTR']
    layers = layer_folders
    if not os.path.isdir(csv_path):
        os.mkdir(csv_path)

    if not os.path.isdir(split_path):
        os.mkdir(split_path)
        # craete directories
        for lf in layer_folders:
            os.mkdir(split_path + '/' + lf)
        for ff in folder_files:

            src = src_path + ff
            for ll in layer_folders:
                if ll in ff or ll.lower() in ff:
                    dest = split_path + '/' + ll + '/' + ff
                    shutil.copy(src, dest)

    # create
    global nip1, nip2, tension

    for l in layers:

        csv_layer = []

        print(l)
        layer = []
        all_files_ts = []
        layers_path = split_path + '/' + l
        files = os.listdir(layers_path)
        #print(files)

        for f in files:
            if 'st' in f:
                nip1 = files.index(f)
            elif 'nd' in f:
                nip2 = files.index(f)
            elif 'ension' in f:
                tension = files.index(f)

            with open(layers_path + '/' + f) as fi:
                data = fi.readlines()
            # print(len(data), len(data)/5)
            # create time stamp
            file_date = data[0].strip().split(' : ')[1]
            file_date = file_date.split(' ')[0]
            file_time = data[1].strip().split(' : ')
            file_time = file_time[1]
            d = datetime.strptime(file_date,
                                  '%Y/%m/%d').date()

            t = datetime.strptime(file_time,
                                  '%H:%M:%S').time()

            exact_ts = datetime(year=d.year, month=d.month, day=d.day,
                                hour=t.hour+9, minute=t.minute,
                                second=t.second)

            end = exact_ts
            #print('end   ', end)
            dif = dt.timedelta(seconds=0.2)

            del data[0:4]
            file_ts = [end]  # date and time

            for ts in range(len(data)):
                end = end - dif
                file_ts.append(end)

            #print(len(data), len(file_ts))
            file_ts.reverse()
            del file_ts[0]

            file_ts = pd.DataFrame(file_ts, columns=['ts'])
            layer.append(data)
            all_files_ts.append(file_ts)

        #print(nip1, nip2, tension)
        for i in [nip1, nip2, tension]:
            print(i)
            data2 = []
            for line in layer[i]:
                line.strip()

                line2 = line.split('  ')

                data2.append(line2)

            # for fixing tension and nip files

            for j in range(len(data2)):
                unw = 0
                if i in [nip1, nip2]:
                    if j in range(1000, len(data2)):
                        del data2[j][8]

                    if j in range(10, 1000):
                        unwanted = [0, 2, 4, 6, 8]
                        for ele in unwanted:
                            del data2[j][ele]

                    if j in range(0, 10):
                        unwanted = [0, 0, 2, 2,
                                    4, 4, 6, 6, 8]
                        unw = unwanted
                        for ele in unw:
                            del data2[j][ele]

                if i == tension:
                    if j in range(1000, len(data2)):
                        unwanted = [1, 3, 5, 6]
                        for ele in unwanted:
                            del data2[j][ele]

                    if j in range(10, 1000):
                        unwanted = [0, 1, 2, 3, 4, 5, 6]
                        for ele in unwanted:
                            del data2[j][ele]

                    if j in range(0, 10):
                        unwanted = [0, 0, 1, 2, 2, 3,
                                    4, 4, 5, 6]
                        unw = unwanted
                        for ele in unw:
                            del data2[j][ele]

            # convert strings to floats
            data3 = []
            for v in range(len(data2)):
                line3 = []

                for val in data2[v]:
                    val = val.replace(' ', '')

                    val2 = float(val)

                    line3.append(val2)
                data3.append(line3)

            data3 = pd.DataFrame(data3)
            #print(data3.shape)
            data3 = pd.concat([all_files_ts[i], data3], axis=1)
            csv_layer.append(data3)

        # find the common starting timestamp

        csv_data = pd.merge(csv_layer[0],
                            csv_layer[1], on='ts')  # combine all sensors
        csv_data = pd.merge(csv_data, csv_layer[2], on='ts')
        #print(csv_data)
        del_col = [0, 2, 4,
                   '0_x', '2_x', '4_x', '6_x',
                   '0_y', '2_y', '4_y', '6_y']
        for col in del_col:
            del csv_data[col]
        # intital names
        input_col = ['ts1', 't1', 't2', 'nip1', 'nip2',
                     't3', 't4', 'nip3', 'nip4',
                     'unkinder', 'outfeeder1', 'outfeeder2']

        csv_data.columns = input_col
        #print(csv_data.shape)

        # merge outfeeder columns
        out_feeder = csv_data.iloc[:, 9:]

        out_feeder2 = (out_feeder['outfeeder1']
                       + out_feeder['outfeeder2']) / 2

        out_feeder2 = pd.DataFrame(out_feeder2)

        del csv_data['outfeeder1']
        del csv_data['outfeeder2']
        csv_data = pd.concat([csv_data, out_feeder2], axis=1)
        # new column names
        input_col = ['ts', 'T2', 'T3', 'NIP1_M', 'NIP1_F',
                     'T4', 'T5', 'NIP2_M', 'NIP2_F',
                     'T1', 'T6_OF']

        csv_data.columns = input_col

        csv_data.to_csv(csv_path + '/' + l + '_comb_csv_file.csv')



