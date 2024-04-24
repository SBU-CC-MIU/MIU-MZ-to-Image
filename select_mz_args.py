import os
import sys
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np



print("Need two arguments: mz data file name and mass list.")
print("Both should be csv files.")

print("Please type the mz data file name.")
spec_file = input()

print("Please type the mass list file name.")
mass_file = input()

os.system("grep m/z " + spec_file + " > mz")

print("m/z is written in a file mz.")

f = open("mz", "r")
mz = f.readline()
mz = mz.split(";")
f.close() 

for j in range(1, len(mz)):
    mz[j] = float(mz[j])

masses = pd.read_csv(mass_file)

out = pd.DataFrame(columns = ["Masses from LIPID MAPS", "Measured m/z", "m/z index", "Sphingolipid profile", "Common Name", "Adduct ion"])

k = 1
j = 0

## 10 ppm; If needed, this can be changed.
epsilon = 10E-6

while k < len(mz) and j < len(masses):
    m_exp = mz[k]
    m_theory = masses["Masses from LIPID MAPS"][j]
    
    if m_exp <= m_theory - epsilon * m_theory:
        k += 1
    elif abs(m_exp - m_theory) < epsilon * m_theory:
        temp = pd.DataFrame({"Masses from LIPID MAPS": [masses["Masses from LIPID MAPS"][j]],
                              "Measured m/z": [mz[k]],
                              "m/z index": [k],
                              "Sphingolipid profile": [masses["Sphingolipid profile"][j]],
                              "Common Name": [masses["Common Name"][j]],
                              "Adduct ion": [masses["Adduct ion"][j]]})
        
        if len(out) == 0:
            out = temp
        else:
            out = pd.concat([out, temp])
        k += 1
    else:
        j += 1

out.to_csv("masses_ind.csv", index = False)

print("A new mass list is written in masses_ind.csv.")

new_col =[0]
new_col.extend(out["m/z index"])

select_mz = pd.read_csv(spec_file, sep = ";", comment = "#",  usecols = new_col)

select_mz.to_csv("mz_data.csv", index = False)

print("Selected spectroscopy data is written in mz_data.csv.")
