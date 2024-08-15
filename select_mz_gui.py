import os
import sys
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np


def select_mz(spec_file, mass_file, spec_sep = ';', mass_sep = ','):

    os.system("grep m/z " + spec_file + " > mz")
    
    print("m/z is written in a file mz.")
    
    f = open("mz", "r")
    mz = f.readline()
    mz = mz.split(spec_sep)
    f.close() 
    
    os.system("rm mz")
    print("mz is deleted.")
    
    for j in range(1, len(mz)):
        mz[j] = float(mz[j])
    
    masses = pd.read_csv(mass_file, sep = mass_sep)
    masses.sort_values(by=['Masses from LIPID MAPS'], ascending = True, inplace = True)
    
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
    
    temp_name = mass_file[:-4] + "_ind.csv"
     
    out.to_csv(temp_name, sep = mass_sep, index = False)
    
    print("A new mass list is written in " + temp_name + ".")
    
    new_col =[0]
    new_col.extend(out["m/z index"])

    select_mz = pd.read_csv(spec_file, sep = spec_sep, comment = "#",  usecols = new_col, low_memory=False)

    temp_name2 = spec_file[:-4] + "_ind.csv"
    select_mz.to_csv(temp_name2, sep = spec_sep, index = False)
    
    print("Selected spectroscopy data is written in " + temp_name + ".")
