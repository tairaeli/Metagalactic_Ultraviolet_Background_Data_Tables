# In this directory

Created for reformatting certain ultraviolet background (UVB) models (Fauchere-Guigere 
2009 (FG09), Haart and Madau 2012 (HM12), Puchwein et al (PW19) and 
Fauchere-Guigere 2020 (FG20)) such that each model is in the same units
to be utilized in direct comparison between models over a
range of redshifts ($z\approx 10$ to $z\approx 10$).

Additionally, there is also code included in this release for running a cloudy_cooling_tools
pipeline to generate ionization tables for different UVB models. This code does require
a working installation of CLOUDY, the code for installing this can be found [here]{link}.

All of these scripts come along with plotting scripts to illustrate a few use cases for
the codes in the directory


## Directories

### cloudy_formatted_data (I'm concerned about plagaism here)
Stores data formatted for use in cloudy_cooling_tools to generate ionization tables.
Directories are also used by *make_UVB_data_table.py* as input files for reformatting.

### data_tables
Contains directories for the reformatted UVBs and is the default containter 
for generating UVBs via *make_UVB_data_table.py*. The tables show the intensity
(erg$s^{-1}cm^{-2}$) binned in different energies (eV). This is done for each UVB
over a range of $z\approx 10$ to $z\approx 10$ with some variation between models.

### generate_ionization_tables
Code for running *cloudy_cooling_tools* for creating ionization tables. Takes in
cloudy-formatted data along with a large suite of parameter files that are described
in more detail within.

## Scripts

### make_UVB_data_table.py
Code for remaking cloudy-formatted data into a more user-friendly csv format

### plot_uvb_spec.py
Creates a lineplot of UVB intensity for each UVB from $10$ - $10^{2.3}$ eV. Uses
the data output from *make_UVB_data_table.py* (i.e. data_tables directory)