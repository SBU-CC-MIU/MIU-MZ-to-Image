import os
import math
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import pickle
from gen_map_gui import gen_map
from skimage.restoration import denoise_tv_bregman
from sklearn.cluster import DBSCAN

def use_gen_map_addup_ions(spectra_filename, spots_filename, mass_filename, spectra_sep = ';', spot_sep = ';', mass_sep = ',', out_dir = '.', outputtype = 'pdf'):

    #masses = pd.read_csv("masses_ind.csv")
    masses = pd.read_csv(mass_filename, sep = mass_sep)
    
    
    mass_maps = dict()    
    maps_all = dict() 
    
    for j in range(len(masses)):
        
        index = j + 1
        #print(j, "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:])
        #map, v95 = gen_map(index, "mz_data.csv", spots_filename)
        map, v95 = gen_map(index, mz_data_filename = spectra_filename, region_spots_filename = spots_filename, spectra_sep = spectra_sep, spot_sep = spot_sep, space = 40)

        common_name = masses.iloc[j, 4]
        if common_name in mass_maps:
            mass_maps[common_name] = mass_maps[common_name] + map
        else:
            mass_maps[common_name] = map


    j = 0
    for common_name, added_map in mass_maps.items():

        b = added_map.flatten()

        if sum(b > 0) < 1:
            v95_max = 0
        else:
            v95_max = np.percentile(b[b > -1], 95)


        

        plt.figure(figsize=(6.4, 5.7))
        # changed font 01/28/2026
        sn.set(font_scale=1.8)
        sn.set_style('ticks')
        plt.subplots_adjust(bottom=0.15)

        ax = sn.heatmap(added_map, vmax = v95_max, square = True, cmap = 'rainbow')
        plt.ylim(0, added_map.shape[0])
        #title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
        title = common_name
        print(j, title)
        ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
        plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.xticks(rotation=0)
        #plt.show()
        #filename = out_dir + "/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + "." + outputtype
        filename = out_dir + "/" + str(j) + "_" + "-".join("".join(common_name.split(" ")).replace("/", ":").split(":")) +  "." + outputtype
        plt.savefig(filename)
        print("Saving " + filename)
        # the following three commands clear too many open figures
        plt.cla()
        plt.clf()
        plt.close("all")

        ## denoising
        # record no data region
        no_data = []
        for l2 in range(added_map.shape[0]):
            for n2 in range(added_map.shape[1]):
                if math.isnan(added_map[l2, n2]): 
                    no_data.append((l2, n2))
                    added_map[l2, n2] = 0

        

        plt.figure(figsize=(6.4, 5.7))
        # changed font 01/28/2026
        sn.set(font_scale=1.8)
        sn.set_style('ticks')
        plt.subplots_adjust(bottom=0.15)

        after_noise = denoise_tv_bregman(added_map, weight=0.03)
        
        # restore no data region
        for l2, n2 in no_data:
            after_noise[l2, n2] = np.nan

        b = after_noise.flatten()

        if sum(b > 0) < 1:
            v95_max = 0
        else:
            v95_max = np.percentile(b[b > -1], 95)
            

        if v95_max > 0:
            maps_all[common_name] = after_noise
        
        ax = sn.heatmap(after_noise, vmax = v95_max, square = True, cmap = 'rainbow')
        plt.ylim(0, added_map.shape[0])
        #title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
        title = common_name
        #print(j, title)
        ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
        plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.xticks(rotation=0)
        #plt.show()
        #filename = out_dir + "/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + "_denoised." + outputtype
        filename = out_dir + "/" + str(j) + "_" + "-".join("".join(common_name.split(" ")).replace("/", ":").split(":")) +  "_denoised." + outputtype
        plt.savefig(filename)
        print("Saving " + filename)
        # the following three commands clear too many open figures
        plt.cla()
        plt.clf()
        plt.close("all")
        
        ##
        j += 1

    # save data for cross-sample correlation
    spectra_filename = spectra_filename.split("/")[-1]    
    with open(out_dir + "/" + spectra_filename[:-8] + ".pickle", "wb") as handle:
        pickle.dump(maps_all, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # 1-sample correlation
    for key in maps_all.keys():
        flattened = maps_all[key].flatten()
        maps_all[key] = flattened[flattened > -1]

    # correlation
    p_corr = pd.DataFrame(maps_all).corr()
    p_corr.to_csv(out_dir + "/correlation.csv")
    dist = 1 - p_corr

    print("Saving correlation.csv")

    # clustering
    clustering = DBSCAN(0.5, min_samples = 1, metric = "precomputed").fit(1 - p_corr)
    clusters = dict()
    for j in range(len(dist)):
        c = clustering.labels_[j]
        if c not in clusters:
            clusters[c] = [p_corr.columns[j]]
        else:
            clusters[c].append(p_corr.columns[j])

    f = open(out_dir + "/clusters.txt", "w")
    for key in sorted(clusters.keys()):
        f.write("cluster " + str(key) + ":\n")
        for t in clusters[key]:
            f.write(t + "\n")
        f.write("\n")
        f.write("#############\n")
        f.write("\n")

    f.close()
    print("Saving clusters.txt")
    #print(clustering.labels_) 
