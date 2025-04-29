import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import configparser
import os
import h5py
import roman

def get_true_rs(val): ##define how to get actual rshift numbers
    if val == 20:
        true_rs = '2.0'
    elif val == 18:
        true_rs = '2.5'
    return true_rs

# reformatting ion labels
ion_name_dict = {"H_I":r"H $\mathrm{\i}$",
                 "Si_II":r"Si $\mathrm{\i\i}$",
                 "Si_III":r"Si $\mathrm{\i\i\i}$",
                 "C_III":r"C $\mathrm{\i\i\i}$",
                 "Si_IV":r"Si $\mathrm{\i v}$",
                 "C_IV":r"C $\mathrm{\i v}$",
                 "N_V":r"N $\mathrm{v}$",
                 "O_VI":r"O $\mathrm{v\i}$"}

# reading in arguments
plot_args = configparser.ConfigParser()
# plot_args.read("/mnt/home/tairaeli/trident_uncertainty/mods/backgrounds/uv_sal/pipeline/sal_params.par")
plot_args.read("./plot_params.par")

# set desired halo pattern
halo = plot_args["galaxy_settings"]["gal_pattern"]
rs = plot_args["galaxy_settings"]["redshift"]
nrays = int(plot_args["galaxy_settings"]["nrays"])

# identifying the path argument as a variable
out_path = plot_args["base_settings"]["output_file"]
if os.path.exists(out_path) == False:
    os.mkdir(out_path)

# initializing UVB data
uvb_names = plot_args["uvb_analysis"]["uvb_names"].split(" ")
uvb_filenames = plot_args["uvb_analysis"]["uvb_filenames"].split(" ")
ion_list = plot_args["uvb_analysis"]["ion_list"].split(" ")
num_ion = len(ion_list)

# defining size of axis labels
ax_lab_size = 20
title_size = 20

# defining bounds of colorbar (in logscale)
lb_cutoff = -6 # 10**-30 # 10**-3
ub_cutoff = 0 #-0.00001

# Parameter1 = gas density: column 2
# Parameter2 = redshift: column 3
# Temperature = column 4

comp_paths = {}

# iterating through each parwise comparison
for i in range(len(uvb_names)):
    print(f"Creating ion fraction plot for {uvb_names[i]}") 
    # iterating through each ion
    for ion in ion_list:
        print("Ion: "+ion)

        # creating figure
        fig, ax = plt.subplots(1, 1, figsize=(6,5))
        cmap = cm.get_cmap('viridis')
        im = cm.ScalarMappable()
        w_size = 10

        atom, istate = ion.split("_")
        istate_num = roman.fromRoman(istate)
        
        # loading in "old" data and masking out data based on set bounds
        atom, istate = ion_list[0].split("_")
        istate_num = roman.fromRoman(istate)

        itable_f = h5py.File(uvb_filenames[0],'r')
        col_dens = itable_f[atom].attrs["Parameter1"]
        temp = itable_f[atom].attrs["Temperature"]
        rs_list = itable_f[atom].attrs["Parameter2"]

        # store rs and index in ionization table
        rs_dat = [999,999]
        for j,rs_temp in enumerate(rs_list):
            if np.abs(float(rs)-rs_temp) < rs_dat[0]:
                rs_dat[0] = np.abs(float(rs)-rs_temp)
                rs_dat[1] = j
        itable_f_filter = itable_f[atom][istate_num-1,:,rs_dat[1],:]
        itable_f_filter[itable_f_filter < lb_cutoff] = np.nan
        itable_f_filter[itable_f_filter > ub_cutoff] = np.nan
        itable_f.close()

        # setting up the 'old' 2d histogram
        f1 = ax.pcolormesh(10**col_dens, 10**temp, itable_f_filter.T, 
                                cmap = cmap)
        # setting up contours 
        ax.contour(10**col_dens, 10**temp, itable_f_filter.T, 
                        colors = "black")

        ax.set_ylabel("$T$ [K]", fontsize=ax_lab_size)
        ax.set_xlabel(r"n [$cm^{-3}$]", fontsize=ax_lab_size)
        ax.set_yscale("log")
        ax.set_xscale("log")

        ax.text(0.1,0.82,uvb_names[i], 
                fontsize=ax_lab_size+4, transform=ax.transAxes)
        
        cb1 = fig.colorbar(f1,ax = ax)

        ax.text(1.2, 0.1, 
                f'log({ion_name_dict[ion]}) Fraction Ratio', fontsize=ax_lab_size,
                transform=ax.transAxes, rotation=270)


        plt.tight_layout()
        # saving figure
        plt.savefig(out_path+f"/ion_frac_{uvb_names[i]}_{ion}.png",
                    dpi=400,bbox_inches='tight')
        plt.clf()

