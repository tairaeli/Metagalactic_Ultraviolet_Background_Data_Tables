"""
Creates a figure showing the intensity of different UVBs at 
different energies
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import pandas as pd
import unyt as u
import argparse
import os


def read_cloudy_in(file):
    """
    Reads in CLOUDY input files as Pandas Data Frames

    args:

        file (str) - path to CLOUDY input file
    
    returns:

        df (Data Frame): the read in / formatted data file
    """
    df = pd.read_csv(file,
                     header = None,
                    skiprows = 5,
                    skipfooter = 3,
                    delim_whitespace = True)
    
    df = df.drop(columns = 0)
    
    for i in range(len(df[1])):
        df[1][i] = float(df[1][i].replace(")","").replace("(",""))
        df[2][i] = float(df[2][i].replace(")","").replace("(",""))
    
    return df

# reading in arguments
parser = argparse.ArgumentParser(description = "Generate UVB data tables for different UVBs")

parser.add_argument('-out_path', action='store', 
                    required=False, dest='out_path', 
                    default= "./",
                    help='output directory for figure')

parser.add_argument('-table_dir', action='store', 
                    required=False, dest='table_dir', 
                    default= "./data_table_example/",
                    help='Directory where UVB tables have been saved to. Should be the only items in the directory')

# parser.add_argument('-uvb_names', action='store', 
#                     required=False, dest='uvb_names', 
#                     default= "FG09 FG20 HM12 PW19",
#                     help='Names of UVB tables')

parser.add_argument('-rs', action='store', 
                    required=False, dest='rs', 
                    default= "2.5",
                    help='redshift to plot. Not all redshifts between UVBs are the sound, so will pick the closest redshift ')

args = parser.parse_args()

# reading in arguments
table_loc = args.table_dir
table_dirs = os.listdir(table_loc)
uvb_names = os.listdir(table_loc)
print(table_dirs)
rs = float(args.rs)

# reading in data
uvb_tables = {}
for i,table in enumerate(table_dirs):
    
    uvb_dir = table_loc+table
    rs_dir = os.listdir(uvb_dir)
    
    # searching for closest redshift to set value
    rs_dist = [999,999,999]
    for j,file in enumerate(rs_dir):
        file_rs = float(file[2:7])
        if np.abs(rs-float(file_rs)) < rs_dist[0]:
            rs_dist[0] = np.abs(rs-file_rs)
            rs_dist[1] = j
            rs_dist[2] = file_rs
    
    print(uvb_dir+"/"+rs_dir[rs_dist[1]])
    uvb_tables[uvb_names[i]] = pd.read_csv(uvb_dir+"/"+rs_dir[rs_dist[1]], 
                                           usecols = ["E (eV)",  "I (erg/s/cm**2)"])


# reading in ion data
ion_energies = pd.read_csv("./ionization_energies.txt", delimiter = "  ")

# creating a mask for all ions we are not using
imask = ["N_II","N_IV","Ne_VII", "C_II",
         "S_II", "S_III", "S_IV","Mg_II", "Al_III", "O_III", 'Ne_VIII', 'Mg_X']

for ion in imask:
    ion_energies = ion_energies[ion_energies["ion"] != ion]
ion_energies = ion_energies.reset_index()

ion_name_dict = {"H_I":r"H $\mathrm{\i}$",
                 "Si_II":r"Si $\mathrm{\i\i}$",
                 "Si_III":r"Si $\mathrm{\i\i\i}$",
                 "C_III":r"C $\mathrm{\i\i\i}$",
                 "Si_IV":r"Si $\mathrm{\i v}$",
                 "C_IV":r"C $\mathrm{\i v}$",
                 "N_V":r"N $\mathrm{v}$",
                 "O_VI":r"O $\mathrm{v\i}$"}

# creating colors for figure
cmap = colormaps["Dark2"]
colors = cmap(np.linspace(0, 0.7, len(ion_energies["ion"])))

fig, ax = plt.subplots()
trans = ax.get_yaxis_transform()

min_x = 10
max_x = 10**2.3
lw = 2.5
fs = 17

# plotting vertical lines at ion ionization energies
for i,ion in enumerate(ion_energies["ion"]):
    ax.axvline(ion_energies["ionization energy (eV)"][i],
             linestyle = "-", color = "grey")

# H I
ax.text(ion_energies["ionization energy (eV)"][2]-10**0.2, 10**(-6.0),
                ion_name_dict[ion_energies["ion"][2]], 
                fontsize=fs, color = "black", rotation="vertical")

# Si II
ax.text(ion_energies["ionization energy (eV)"][4]-10**0.27, 10**(-6.0),
                ion_name_dict[ion_energies["ion"][4]], 
                fontsize=fs, color = "black", rotation="vertical")

# Si III
ax.text(ion_energies["ionization energy (eV)"][5]-10**0.60, 10**(-6.0),
                ion_name_dict[ion_energies["ion"][5]], 
                fontsize=fs, color = "black", rotation="vertical")

# Si IV
ax.text(ion_energies["ionization energy (eV)"][6]-10**0.72, 10**(-6.0),
                ion_name_dict[ion_energies["ion"][6]], 
                fontsize=fs, color = "black", rotation="vertical")

# C III
ax.text(ion_energies["ionization energy (eV)"][0]-10**0.74, 10**(-4.4),
                ion_name_dict[ion_energies["ion"][0]], 
                fontsize=fs, color = "black", rotation="vertical")

# C IV
ax.text(ion_energies["ionization energy (eV)"][1]-10**0.88, 10**(-4.4),
                ion_name_dict[ion_energies["ion"][1]], 
                fontsize=fs, color = "black", rotation="vertical")

# N V
ax.text(ion_energies["ionization energy (eV)"][7]-10**1.05, 10**(-4.4),
                ion_name_dict[ion_energies["ion"][7]], 
                fontsize=fs, color = "black", rotation="vertical")

# O VI
ax.text(ion_energies["ionization energy (eV)"][3]-10**1.2, 10**(-4.4),
                ion_name_dict[ion_energies["ion"][3]], 
                fontsize=fs, color = "black", rotation="vertical")

for i, table in enumerate(uvb_tables.keys()):
    # print(uvb_tables[i].head())
    ax.plot(uvb_tables[table]["E (eV)"],
         uvb_tables[table]["I (erg/s/cm**2)"], label = uvb_names[i],
         linewidth = lw)

ax.set_xlim(min_x,max_x)
ax.set_ylim(bottom=10**(-6.5))
ax.legend()
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_ylabel(r"4$\pi$$\nu$$J_{\nu}$ (erg $s^{-1}$ $cm^{-2}$)", fontsize = 16)
ax.set_xlabel("log(E) (eV)", fontsize = 16)
plt.savefig(args.out_path+"uvb_intens_plot.png")

print("Plot Complete")