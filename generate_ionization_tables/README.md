# In This Directory

### Note to user

Running some of the code in this directory requires a working installation of [`cloudy_cooling_tools`](https://github.com/brittonsmith/cloudy_cooling_tools). To install, clone the repo as seen [here](https://github.com/brittonsmith/cloudy_cooling_tools), navigate to the `cloudy_grids` directory and run `setup.py`.

**cloudy\_input\_bin\_example** - directory acting as a bin for the output of gen\_cloudy\_input.py, as well as the input files for running the cloudy pipeline

**gen\_cloudy\_input.py** - reformats CSV files from make\_UVB\_data\_tables.py to format that CLOUDY will accept. Takes in 3 arguments:

* `-ds` (str): location of output file
* `-uvb` (str): location of UVB data
* `-rs` (str): set range for redshifts to iterate through (e.g. "1.2 2.7")

**full\_cloudy.py** - runs CLOUDY spectral synthesis simulations in parallel. Requires 6 arguments that are defined within the code:

* `start_part` - first part number in which the code will run from. The cloudy simulation is broken up into a number of parts to be run in parallel.
* `end_part` - final part number in which the code will run
* `total_parts` - total number of parts in cloudy run
* number of cores - number of gpu cores the code is run on
* `par_file` - location of parameter file (more details below)
* `CIAOLoop_file` - location of CIAOLoop file. This is where the spectral synthesis is run. Should be located within installation of [`cloudy_cooling_tools`](https://github.com/brittonsmith/cloudy_cooling_tools).

**gen\_trident\_input.py** - takes in final run file from `full_cloudy.py` and outputs an ionization table in an HDF5 format that can be used with [Trident](https://trident-project.org/).

**plot\_comp\_ion_frac.py** - creates pairwise 2D histogram comparison figures with the HDF5 files from `gen_trident_input.py`.

**uvb\_params.par** - parameter file for cloudy simulation run. Includes all of the parameters that go into the CLOUDY run that are specified within the file. The following information must be changed for CLOUDY to run:

* path to CLOUDY executable
* path to output directory
* path to ultraviolet background data
* list of redshifts to use (from the input UVB filenames)

**plot\_params.par** - parameter file for creating plot comparisons

### Example scripts for *gen\_uvb\_input.py* (FG20)

```
python gen_cloudy_input.py -ds cloudy_input_bin_example -uvb ../data_table_example/fg20 -rs "1.2 2.7"
```
