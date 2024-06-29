import os
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
from gen_map_gui import gen_map
from skimage.restoration import denoise_tv_bregman
from sklearn.cluster import DBSCAN

def use_gen_map(spectra_filename, spots_filename, mass_filename, spectra_sep = ';', spot_sep = ';', mass_sep = ',', outputtype = 'pdf'):

    #masses = pd.read_csv("masses_ind.csv")
    masses = pd.read_csv(mass_filename, sep = mass_sep)
    
    os.system("mkdir results")
    
    print("A folder is made: results.")
    
    maps_all = dict() 
    added_map = np.zeros((1, 1))
    v95_max = 0
    for j in range(len(masses)):
        
        index = j + 1
        #print(j, "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:])
        #map, v95 = gen_map(index, "mz_data.csv", spots_filename)
        map, v95 = gen_map(index, mz_data_filename = spectra_filename, region_spots_filename = spots_filename, spectra_sep = spectra_sep, spot_sep = spot_sep, space = 40)
        
        if added_map.size == 1:
            added_map = map
            v95_max = v95
        
        if j > 0 and masses.iloc[j, 0] == masses.iloc[j - 1, 0]:
            added_map = added_map + map
            v95_max = max(v95_max, v95)
            
        if (j == len(masses) - 1) or (masses.iloc[j, 0] != masses.iloc[j + 1, 0]):
        
            plt.figure(figsize=(6.4, 5.2))
            ax = sn.heatmap(added_map, vmax = v95_max, square = True, cmap = 'nipy_spectral')
            plt.ylim(0, added_map.shape[0])
            title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
            print(j, title)
            ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
            plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
            plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
            plt.xticks(rotation=0)
            #plt.show()
            filename = "results/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + "." + outputtype
            plt.savefig(filename)
            print("Saving " + filename)
            # the following three commands clear too many open figures
            plt.cla()
            plt.clf()
            plt.close("all")
    
            ## denoising
            plt.figure(figsize=(6.4, 5.2))
            after_noise = denoise_tv_bregman(added_map, weight=0.03)
            maps_all[masses.iloc[j, 4] + masses.iloc[j, 5][1:]] = after_noise
            ax = sn.heatmap(after_noise, vmax = v95_max, square = True, cmap = 'nipy_spectral')
            plt.ylim(0, added_map.shape[0])
            title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
            #print(j, title)
            ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
            plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
            plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
            plt.xticks(rotation=0)
            #plt.show()
            filename = "results/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + "_denoised." + outputtype
            plt.savefig(filename)
            print("Saving " + filename)
            # the following three commands clear too many open figures
            plt.cla()
            plt.clf()
            plt.close("all")
            
            ##
            added_map = np.zeros((1, 1))
            v95_max = 0

    maps_flat = dict()
    for key in maps_all.keys():
        maps_flat[key] = maps_all[key].flatten()

    # correlation
    p_corr = pd.DataFrame(maps_flat).corr()
    p_corr.to_csv("results/correlation.csv")
    dist = 1 - p_corr

    print("Saving results/correlation.csv")

    # clustering
    clustering = DBSCAN(0.5, min_samples = 1, metric = "precomputed").fit(1 - p_corr)
    clusters = dict()
    for j in range(len(dist)):
        c = clustering.labels_[j]
        if c not in clusters:
            clusters[c] = [p_corr.columns[j]]
        else:
            clusters[c].append(p_corr.columns[j])

    f = open("results/clusters.txt", "w")
    for key in sorted(clusters.keys()):
        f.write("cluster " + str(key) + ":\n")
        for t in clusters[key]:
            f.write(t + "\n")
        f.write("\n")
        f.write("#############\n")
        f.write("\n")

    f.close()
    print("Saving results/clusters.txt")
    #print(clustering.labels_) 
