import pandas as pd

from datetime import datetime

errors = pd.read_csv('extra files/Report_CamData.csv')
print(errors.columns)
print(errors['Minute'].unique())

t_end = 0
t_start = 0
layer_added = 0
layers = []
for t in range(len(errors) - 1):
    if t == len(errors) - 2:
        l = errors.iloc[t_start:, :]
        print(l.shape)
        layers.append(l)

    exact_time = datetime(year=2022
                          , month=9, day=7, hour=errors.iloc[t, 1],
                          minute=errors.iloc[t, 2],
                          second=errors.iloc[t, 3])

    t = t + 1
    t2 = datetime(year=2022
                  , month=9, day=7, hour=errors.iloc[t, 1],
                  minute=errors.iloc[t, 2],
                  second=errors.iloc[t, 3])
    diff_sec = (t2 - exact_time).total_seconds()
    t = t - 1
    if diff_sec > 600:
        # print(t)
        t_end = t + 1
        l = errors.iloc[t_start:t_end, :]
        layer_added = layer_added + 1
        t_start = t_end

        print(t_end)
        print(l.shape)
        layers.append(l)
    if t == len(errors) - 1:
        l = errors.iloc[t_start:, :]
        # print(l.shape)
        layers.append(l)
print(len(layers))
map_xy = [0, 2, 5, 8, 9]
map_xy = pd.DataFrame(map_xy)

mean_val = map_xy.groupby(map_xy.index // (5 / 2)).mean()
m = map_xy.resample('3T')
print(m)
