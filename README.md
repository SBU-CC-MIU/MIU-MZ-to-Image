<header>
Generating Images from MALDI Spectroscopy Data
<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->
Three CSV files are needed to run this program:
(1) Raw MALDI spectra data, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-PyMT-Spectra-TIC.csv
(2) A file of region spots, e.g., 230615PyMT-Fat-CMC-DHB-Pos-1-RegionSpots.csv
(3) A mass list, e.g., MassList-230615PyMT-Fat-CMC-DHB-Pos-1-PyMT.csv

To run the program, first type:

python select_mz_args.py

The program will ask for spectroscopy data and a mass list. Follow the instruction and provide the file names. It may take 10 - 30 minuites.
Several temporary files will be generated for the next step.

Then, type:

python use_gen_map_args.py

The program will ask for a file containing region spots. Simply provide the file name.

Images then will be generated in a folder called "figs".

