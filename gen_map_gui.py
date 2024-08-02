import pandas as pd
import numpy as np

def gen_map(index, mz_data_filename, region_spots_filename, spectra_sep = ",", spot_sep = ",", space = 40):
    # only read a particular column of the m/z data file
    df = pd.read_csv(mz_data_filename, sep = spectra_sep, usecols = [0, index])
    print("spectra has been read")
    # extract the spot index
    df['Spot index'] = df['m/z'].apply(lambda x: int(x.split(" ")[1]) - 1)

    # read the X,Y position file
    positions = pd.read_csv(region_spots_filename, sep = spot_sep, comment = "#")

    # merge these two dataframes
    com = positions.merge(df, on = "Spot index")

    # determine sample size and the number of grids
    xmin, xmax = min(com['x']), max(com['x'])
    xgrids = round((xmax - xmin) / space + 1)

    ymin, ymax = min(com['y']), max(com['y'])
    ygrids = round((ymax - ymin) / space + 1)

    # this is the output map
    map = np.zeros((ygrids, xgrids))
    
    # part with no data, set to NA
    for j3 in range(ygrids):
        for k3 in range(xgrids):
            map[j3, k3] = np.nan

    # build the map
    for j2 in range(len(com)):
        x = round((com['x'][j2] - xmin) / space)
        y = round((com['y'][j2] - ymin) / space)
        map[y, x] = com.iloc[j2, 4]
    
    # value of the 95 percentile
    print("output is [map, v95]")
    if sum(com.iloc[:, 4] > 0) < 10:
        return [map, 0]
    v95 = np.percentile(com.iloc[:, 4][com.iloc[:, 4] > 0], 95)

    return [map, v95]
