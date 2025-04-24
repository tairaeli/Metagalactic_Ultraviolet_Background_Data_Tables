# reformat the information from different UV backgrounds to match the format CLOUDY cooling tools prefers
import numpy as np
import unyt as u
from scipy.interpolate import interp1d
import argparse
import pickle
import pandas as pd
import os


parser = argparse.ArgumentParser(description = "Pipeline variables and constants for running FSPS")
parser.add_argument('-ds', nargs='?', action='store', required=True, dest='path', help='Path where  output data will be stored')
parser.add_argument('-uvb', nargs='?',action='store', required=True, dest='uvb_dir', help='Path to UV ackground data')
parser.add_argument('-rs', action='store', dest='rs_range', default="1.2 2.7", type=str, help='Range of redshifts to analyze. Input is a list of 2 values from the lower to upper bound')

args = parser.parse_args()
dic_args = vars(args)

# converting rs argument into a list
rs_range = args.rs_range.split(" ")

# load in location of dirctory
uvb_dir =  args.uvb_dir
uvb_dir_list = os.listdir(uvb_dir)
# filter out all the files that do not have redshifts I want
in_rs_range = []
for i,filename in enumerate(uvb_dir_list):
    rs = float(filename[2:10])
    if (rs >= float(rs_range[0])) and (rs <= float(rs_range[1])):
        in_rs_range.append(uvb_dir+"/"+filename)

# convert those into the units that cloudy is happy with
rs_dict = {}
for filename in in_rs_range:
    rs = float(filename[-13:-5])
    f = pd.read_csv(filename, 
        usecols = ["E (eV)",  "I (erg/s/cm**2)"])
    nu = f["E (eV)"].to_numpy()/13.605703976
    intens = ((f['E (eV)'].to_list()*u.eV).to("J")/(u.h)).to_value()
    spec = (f["I (erg/s/cm**2)"]/intens/(4*np.pi)).to_numpy()

    # storing energy bins (nu) and intensity (sepc) for each rs in range
    rs_dict[rs] = [nu,spec]

# initializing list to store redshift data
conv_rs = []

# setting a source name
source = "NA"

# setting lowest alloted intensity
lJ_pad = -50

# iterating through each redshift
for rs in rs_dict.keys():

    # setting the current redshift
    # rs = uvb_rs[irs]
    
    print("Running redshift",f"{rs:.4e}")
    
    conv_rs.append(f"{rs:.4e}")
    
    # calling the uvb intensity data for the current redshift
    nu = np.flip(rs_dict[rs][0])
    spec = np.flip(rs_dict[rs][1])
    
    spec = np.log10(spec)
    
    # generate interpolation function
    interp = interp1d(nu, spec, fill_value = "extrapolate")
    
    # generating file where data is stored
    fname = args.path+f"/z_{rs:.4e}.out"
    
    with open(fname, "w") as f:
        f.write(f"# {source}\n")
        f.write(f"# z = {rs:.6f}\n")
        f.write("# E [Ryd] log (J_nu)\n")
        
        f.write(f"interpolate ({1e-8:.10f}) ({lJ_pad:.10f})\n")
        f.write(f"continue ({nu[-1]*0.99:.10f}) ({lJ_pad:.10f})\n")
        
        # loop backwards through wavelengths so that lowest energy is first
        for i in range(nu.size-1,-1,-1):
            f.write(f"continue ({nu[i]:.10f}) ({spec[i]:.10f})\n")
            
        f.write(f"continue ({nu[0]*1.01:.10f}) ({lJ_pad:.10f})\n")
        f.write(f"continue ({7.354e6:.10f}) ({lJ_pad:.10f})\n")
        
        x = 10**interp(1)
        f.write(f"f(nu) = {np.log10(x * 4 * np.pi):.10f} at {1:.10f} Ryd\n")
    
    assert os.path.exists(fname), "file did not write"
    