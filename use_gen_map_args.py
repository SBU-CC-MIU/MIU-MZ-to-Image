import os
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
from gen_map_args import gen_map
from skimage.restoration import denoise_tv_bregman

print("Need one argument: Region spots file name.")
print("It should be a csv file.")
print("Please type the Region spots file name.")

spots_filename = input()

masses = pd.read_csv("masses_ind.csv")

os.system("mkdir figs")

print("A folder is made: figs.")

added_map = np.zeros((1, 1))
v95_max = 0
for j in range(len(masses)):
    
    index = j + 1
    #print(j, "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:])
    map, v95 = gen_map(index, "mz_data.csv", spots_filename)
    
    if added_map.size == 1:
        added_map = map
        v95_max = v95
    
    if j > 0 and masses.iloc[j, 0] == masses.iloc[j - 1, 0]:
        added_map = added_map + map
        v95_max = max(v95_max, v95)
        
    if (j == len(masses) - 1) or (masses.iloc[j, 0] != masses.iloc[j + 1, 0]):
    
        plt.figure(figsize=(6.4, 5.2))
        ax = sn.heatmap(added_map, vmax = v95_max, square = True)
        plt.ylim(0, added_map.shape[0])
        title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
        print(j, title)
        ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
        plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.xticks(rotation=0)
        #plt.show()
        filename = "figs/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + ".jpg"
        plt.savefig(filename)
        print("Saving " + filename)
        # the following three commands clear too many open figures
        plt.cla()
        plt.clf()
        plt.close("all")

        ## denoising
        plt.figure(figsize=(6.4, 5.2))
        after_noise = denoise_tv_bregman(added_map, weight=0.03)
        ax = sn.heatmap(after_noise, vmax = v95_max, square = True)
        plt.ylim(0, added_map.shape[0])
        title = "m/z: " + str(round(masses.iloc[j, 0], 4)) + '\n' + masses.iloc[j, 4] + masses.iloc[j, 5][1:]
        #print(j, title)
        ax.set(xlabel = 'x (mm)', ylabel = 'y (mm)', title = title)
        plt.xticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.yticks(np.arange(0,201,50), np.arange(0,9,2))
        plt.xticks(rotation=0)
        #plt.show()
        filename = "figs/" + str(j) + "_" + "-".join(masses.iloc[j, 4].replace("/", ":").split(":")) + masses.iloc[j, 5][1:] + "_denoised.jpg"
        plt.savefig(filename)
        print("Saving " + filename)
        # the following three commands clear too many open figures
        plt.cla()
        plt.clf()
        plt.close("all")
        
        ##
        added_map = np.zeros((1, 1))
        v95_max = 0


