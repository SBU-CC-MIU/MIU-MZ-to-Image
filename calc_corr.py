import pickle
import pandas as pd
import numpy as np
from scipy.ndimage import rotate
from sklearn.cluster import DBSCAN

def correlation(filename_pickle_1, filename_pickle_2, out_dir):

    with open(filename_pickle_1, 'rb') as handle:
        p1 = pickle.load(handle)
    with open(filename_pickle_2, 'rb') as handle:
        p2 = pickle.load(handle)
    
    contour_1 = list(p1.values())[0] > -1
    contour_2 = list(p2.values())[0] > -1
    
    contour_1 = contour_1.astype(int)
    contour_2 = contour_2.astype(int)
    
    y1, x1 = contour_1.shape
    y2, x2 = contour_2.shape
    
    ymax, ymin = max(y1, y2), min(y1, y2)
    xmax, xmin = max(x1, x2), min(x1, x2)
    
    min_diff = 1.0E9
    best_mv = []
    for ydiff in range(ymax - ymin + 1):
        for xdiff in range(xmax - xmin + 1):
            for ag in range(-10, 11, 1):
                big_fig_1 = np.zeros((ymax, xmax))
                big_fig_2 = np.zeros((ymax, xmax))
    
                big_fig_1[max(ymin + ydiff, y1) - y1 : max(ymin + ydiff, y1), max(xmin + xdiff, x1) - x1 : max(xmin + xdiff, x1)] = rotate(contour_1, ag, order = 0,reshape = False)
                big_fig_2[max(ymin + ydiff, y2) - y2 : max(ymin + ydiff, y2), max(xmin + xdiff, x2) - x2 : max(xmin + xdiff, x2)] = contour_2
                
                diff = sum(sum(abs(big_fig_1 - big_fig_2)))
    
                if diff < min_diff:
                   min_diff = diff
                   best_mv = [ydiff, xdiff, ag]
    
    print("best_mv", best_mv, "min_diff", min_diff)
    ydiff, xdiff, ag = best_mv
    
    
    
    for key in p1.keys():
        big_fig_1 = np.zeros((ymax, xmax))
        big_fig_1.fill(np.nan)
        big_fig_1[max(ymin + ydiff, y1) - y1 : max(ymin + ydiff, y1), max(xmin + xdiff, x1) - x1 : max(xmin + xdiff, x1)] = rotate(p1[key], ag, cval = np.nan, order = 0,reshape = False)
        p1[key] = big_fig_1
    
    for key in p2.keys():
        big_fig_2 = np.empty((ymax, xmax))
        big_fig_2.fill(np.nan)
        big_fig_2[max(ymin + ydiff, y2) - y2 : max(ymin + ydiff, y2), max(xmin + xdiff, x2) - x2 : max(xmin + xdiff, x2)] = p2[key]
        #Note this p1, we combine the two
        p1[key] = big_fig_2
        
    
    
    maps_all = p1
    
    for key in maps_all.keys():
        flattened = maps_all[key].flatten()
        maps_all[key] = flattened
    
    # correlation
    p_corr = pd.DataFrame(maps_all).corr(numeric_only = True)
    p_corr.to_csv(out_dir + "/correlation_cross_sample.csv")
    dist = 1 - p_corr
    
    print("Saving correlation_cross_sample.csv")
    
    # clustering
    clustering = DBSCAN(0.5, min_samples = 1, metric = "precomputed").fit(1 - p_corr)
    clusters = dict()
    for j in range(len(dist)):
        c = clustering.labels_[j]
        if c not in clusters:
            clusters[c] = [p_corr.columns[j]]
        else:
            clusters[c].append(p_corr.columns[j])
    
    f = open(out_dir + "/clusters_cross_sample.txt", "w")
    for key in sorted(clusters.keys()):
        f.write("cluster " + str(key) + ":\n")
        for t in clusters[key]:
            f.write(t + "\n")
        f.write("\n")
        f.write("#############\n")
        f.write("\n")
    
    f.close()
    print("Saving clusters_cross_sample.txt")
    #print(clustering.labels_)

    return 
