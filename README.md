# Generating Images from MALDI Spectroscopy Data for a given list of compounds

### Contact:
email: xiaolu.cheng@stonybrookmedicine.edu

## What files are needed:

Three CSV files are needed to run this program:

(1) Raw MALDI spectra data, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-PyMT-Spectra-TIC.csv

(2) A file of region spots, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-RegionSpots.csv

(3) A mass list, e.g., MassList-230615PyMT-Fat-CMC-DHB-Pos-1-PyMT.csv

## How to run the program:

First, type

```bash
python select_mz_args.py
```
The program will ask for spectroscopy data and a mass list. Follow the instruction and provide the file names. It may take 10 - 30 minuites. Several temporary files will be generated for the next step.

Then, type:

```bash
python use_gen_map_args.py
```

The program will ask for a file containing region spots. Simply provide the file name.

Images then will be generated in a folder called "figs".

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
The index relates the position x,y in the Spectra file. Note: The index in the RegionSpots.cvs begins from 0; but in the Spectra file, the index begins from 1. So, spot index 0 in RegionSpots actually corresponds to spot 1 in the Spectra file. When these two data frames are merged, we then have an XY position for a point and the spectra for that point.
