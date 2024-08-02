import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from select_mz_gui import select_mz
from use_gen_map_gui import use_gen_map
from use_gen_map_addup_ions import use_gen_map_addup_ions
import time

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

## row 8
ttk.Label(mainframe, text="Output Folder").grid(column=1, row=8, sticky=W)

## row 9
outfolder=ttk.Entry(mainframe)
outfolder.grid(row=9,column=1, sticky=W)

folder_name = ""
def browsefunc4():
    global folder_name
    filename = filedialog.askdirectory()
    outfolder.insert(END, filename) # add this
    folder_name = filename


b4=ttk.Button(mainframe,text="Browse",command=browsefunc4)
b4.grid(row=9,column=2, sticky=W)

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


## row 10
ttk.Label(mainframe, text="Combine data for different adduct ions").grid(column=1, row=10, sticky=W)

yes_or_no = StringVar()
choice = ttk.Combobox(mainframe, textvariable=yes_or_no)
choice.grid(column=2, row=10, sticky=W)


choice['values'] = ('yes', 'no')
choice.state(["readonly"])

yes_or_no = False
def set_choice(event):
    global yes_or_no
    if choice.get() == "yes":
        yes_or_no = True

choice.bind("<<ComboboxSelected>>", set_choice)


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
    
    #s.configure('TProgressbar', text = '10 %')
    progressbar['value'] = 10
    root.update_idletasks()
    time.sleep(0.5)

    temp_spec = spectra_file[:-4] + "_ind.csv"
    temp_mass = mass_file[:-4] + "_ind.csv"
    
    if not(os.path.exists(temp_spec) and os.path.exists(temp_mass)):

        select_mz(spec_file = spectra_file, mass_file = mass_file, mass_sep = mass_sep)
    
    #s.configure('TProgressbar', text = '50 %')
    progressbar['value'] = 50
    root.update_idletasks()
    time.sleep(1)

    if yes_or_no:
        use_gen_map_addup_ions(spectra_filename = temp_spec, spots_filename = spot_file, mass_filename = temp_mass, mass_sep = mass_sep, out_dir = folder_name, outputtype = outputtype)
    else:
        use_gen_map(spectra_filename = temp_spec, spots_filename = spot_file, mass_filename = temp_mass, mass_sep = mass_sep, out_dir = folder_name, outputtype = outputtype)
    
    #s.configure('TProgressbar', text = '100 %')
    progressbar['value'] = 100
    root.update_idletasks()
    print("Completed. You can quit now.")
    exit

#s = ttk.Style()
#s.theme_use("default")
#s.configure("TProgressbar", thickness=20)
#progressbar = ttk.Progressbar(mainframe, variable = 0, maximum = 100, length = 200, mode = 'determinate', style = 'TProgressbar')
progressbar = ttk.Progressbar(mainframe, length = 200, mode = 'determinate')
progressbar.grid(column=2, row = 12)
#progressbar.pack(ipady = 10)

ttk.Button(mainframe, text="Run", command=run_function).grid(column=2, row=11)


ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=2, row=13)



root.mainloop()    
