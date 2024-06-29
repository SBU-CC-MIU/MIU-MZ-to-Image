import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from select_mz_gui import select_mz
from use_gen_map_gui import use_gen_map

## root window
root = Tk()
root.title("MIU-MZ-to-Image")

## main frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

## row 1
ttk.Label(mainframe, text="Three CSV files are needed:").grid(column=1, row=1, sticky=W)

## row 2
ttk.Label(mainframe, text="(1) Raw MALDI spectra data").grid(column=1, row=2, sticky=W)

## row 3
ent1=ttk.Entry(mainframe)
ent1.grid(row=3,column=1, sticky=W)

spectra_file = ""
def browsefunc():
    global spectra_file
    filename = filedialog.askopenfilename(filetypes=(("csv files","*.csv"),("All files","*.*")))
    ent1.insert(END, filename) # add this
    spectra_file = filename


b1=ttk.Button(mainframe,text="Browse",command=browsefunc)
b1.grid(row=3,column=2, sticky=W)

#ttk.Label(mainframe, text="separator").grid(column=3, row=3, sticky=E)

#sepvar1 = StringVar()
#sep1 = ttk.Combobox(mainframe, textvariable=sepvar1)
#sep1.grid(column=4, row=3, sticky=W)


#sep1['values'] = (',', ';', 'tab')
#sep1.state(["readonly"])

#spectra_sep = ""

#def set_sep1(event):
#    global spectra_sep
#    spectra_sep = sep1.get()
#    if spectra_sep == 'tab':
#        spectra_sep = '\t'

#sep1.bind("<<ComboboxSelected>>", set_sep1)

   

## row 4
ttk.Label(mainframe, text="(2) A file of region spots").grid(column=1, row=4, sticky=W)

## row 5
ent2=ttk.Entry(mainframe)
ent2.grid(row=5,column=1, sticky=W)

spot_file = ""
def browsefunc2():
    global spot_file
    filename = filedialog.askopenfilename(filetypes=(("csv files","*.csv"),("All files","*.*")))
    ent2.insert(END, filename) # add this
    spot_file = filename


b2=ttk.Button(mainframe,text="Browse",command=browsefunc2)
b2.grid(row=5,column=2, sticky=W)

#ttk.Label(mainframe, text="separator").grid(column=3, row=5, sticky=E)

#sepvar2 = StringVar()
#sep2 = ttk.Combobox(mainframe, textvariable=sepvar2)
#sep2.grid(column=4, row=5, sticky=W)


#sep2['values'] = (',', ';', 'tab')
#sep2.state(["readonly"])

#spot_sep = ""
#def set_sep2(event):
#    global spot_sep
#    spot_sep = sep2.get()
#    if spot_sep == 'tab':
#        spot_sep = '\t'

#sep2.bind("<<ComboboxSelected>>", set_sep2)


## row 6
ttk.Label(mainframe, text="(3) A mass list").grid(column=1, row=6, sticky=W)

## row 7
ent3=ttk.Entry(mainframe)
ent3.grid(row=7,column=1, sticky=W)

mass_file = ""
def browsefunc3():
    global mass_file
    filename = filedialog.askopenfilename(filetypes=(("csv files","*.csv"),("All files","*.*")))
    ent3.insert(END, filename) # add this
    mass_file = filename


b3=ttk.Button(mainframe,text="Browse",command=browsefunc3)
b3.grid(row=7,column=2, sticky=W)

ttk.Label(mainframe, text="separator").grid(column=3, row=7, sticky=E)

sepvar3 = StringVar()
sep3 = ttk.Combobox(mainframe, textvariable=sepvar3)
sep3.grid(column=4, row=7, sticky=W)


sep3['values'] = (',', ';', 'tab')
sep3.state(["readonly"])

mass_sep = ""
def set_sep3(event):
    global mass_sep
    mass_sep = sep3.get()
    if mass_sep == 'tab':
        mass_sep = '\t'

sep3.bind("<<ComboboxSelected>>", set_sep3)

## row 8 empty

## row 9

ttk.Label(mainframe, text="Output image type").grid(column=3, row=9, sticky=W)

outtype = StringVar()
out = ttk.Combobox(mainframe, textvariable=outtype)
out.grid(column=4, row=9, sticky=W)


out['values'] = ('pdf', 'jpg', 'png')
out.state(["readonly"])

outputtype = ""
def set_out(event):
    global outputtype
    outputtype = out.get()

out.bind("<<ComboboxSelected>>", set_out)


## last row
def open_csv():
    print(spectra_sep, spot_sep, mass_sep)
    df = pd.read_csv(spectra_file, sep = spectra_sep)
    print(df.columns)
    df = pd.read_csv(spot_file, sep = spot_sep)
    print(df.columns)
    df = pd.read_csv(mass_file, sep = mass_sep)
    print(df.columns)

def pr():
    print(spectra_sep, spot_sep, mass_sep, outputtype)


def run_function():
    temp_spec = spectra_file[:-4] + "_ind.csv"
    temp_mass = mass_file[:-4] + "_ind.csv"
    
    if not(os.path.exists(temp_spec) and os.path.exists(temp_mass)):

        select_mz(spec_file = spectra_file, mass_file = mass_file, mass_sep = mass_sep)
    
    use_gen_map(spectra_filename = temp_spec, spots_filename = spot_file, mass_filename = temp_mass, mass_sep = mass_sep, outputtype = outputtype)
    print("Completed. You can quit now.")
    exit

ttk.Button(mainframe, text="Run", command=run_function).grid(column=2, row=10, sticky=W)

ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=2, row=11)



root.mainloop()    
