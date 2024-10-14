# Generating Images from MALDI Spectroscopy Data for a given list of compounds

### Contact:
email: xiaolu.cheng@stonybrookmedicine.edu

MIU@StonyBrookMedicine.edu 

## What files are needed:

Three CSV files are needed to run this program:

(1) Raw MALDI spectra data, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-PyMT-Spectra-TIC.csv

(2) A file of region spots, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-RegionSpots.csv

(3) A mass list, e.g., MassList-230615PyMT-Fat-CMC-DHB-Pos-1-PyMT.csv

## How to run the program:

Install python. It's recommended to use Anaconda (https://www.anaconda.com/download/success).

Download the files in this repository. Open a terminal, cd to the folder where your downloaded files are, and type

```bash
python run_mz2image.py
```
The program will ask for spectroscopy data, a file containing region spots, and a mass list. Follow the instruction and provide the file names, the separator of the CSV file, and the image type. It may take 10 - 30 minuites. Several temporary files will be generated.

Images then will be generated in the output folder you specified. Correlations and clustering results will be saved in the same folder.

After running the first step, a pickle file containing the selected raw data will be saved in the output folder too. If cross-sample correlation is to be calculated, run the first step for the two samples separately, and then provide the program the pickle files from two samples. 

## Example output:
![alt text](https://github.com/SBU-CC-MIU/MIU-MZ-to-Image/blob/main/images/11_SM(d18-1-16-0)%2BH.jpg)

## Structure required for the MassList.csv file

The program will read comma-separated values (CSV) files with the following columns:
```bash
Masses from LIPID MAPS,	Sphingolipid profile, Common Name, Adduct ion  
```

Example:

```bash
Masses from LIPID MAPS,Sphingolipid profile,,Common Name,,Adduct ion
300.2897,Sphingosine,,Sphingosine (d18:1),,M+H
302.3053,Dihydrosphingosine,,Dihydrosphingosine (d18:0),,M+H
703.5748,C16-SM,,SM(d18:1/16:0),,M+H
725.5568,C16-SM,,SM(d18:1/16:0),,M+Na
```

## Structure required for the RegionSpots.csv file.

```bash

# (comments and metadata)

Spot index;x;y
0;3438.2888183594;9799.4345703125
1;3478.2888183594;9799.4345703125
2;3518.2888183594;9799.4345703125
3;3318.2888183594;9759.4345703125
4;3358.2888183594;9759.4345703125
```
The index relates the position x,y in the Spectra file. Note: The index in the RegionSpots.cvs begins from 0; but in the Spectra file, the index begins from 1. So, spot index 0 in RegionSpots actually corresponds to spot 1 in the Spectra file. When these two data frames are merged, we then have an (X,Y) position for a point and the spectra for that point.


## Structure of the Spectra.csv file

```bash

# (comments and metadata)
m/z;300;300.00150000075;300.003000009;300.00450002475;300.00600004801;300.00750007876;300.00900011701;300.01050016276;300.01200021601; ...
Spot 1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;
Spot 2;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;35.766609604734;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;356.53662416509;0;0;0;0;0;0;
Spot 3;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;142.80817433434;0;0;0;0;0;0;0;35.766609604734;0;0;0;0;0;0;0;0;0;
...
Spot 36050;0;0;0;0;0;0;0;0;0;0;17.420674348041;0;0;0;0;0;0;0;0;0;0;0;0;21.58083538638;0;0;0;0;0;0;0;0;35.766609604734;0;0;0;0;0;0;0;0;0;
Spot 36051;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;73.652558664859;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;35.766609604734;0;0;0;0;0;0;0;0;0;
```

This file contains a Table where columns are the list of m/z, and rows contain an index (Spot #). For each m/z x index, the table contains the Intensity of the signal.
The index can be used in RegionSpots.csv to find the position (X,Y) in the sample
