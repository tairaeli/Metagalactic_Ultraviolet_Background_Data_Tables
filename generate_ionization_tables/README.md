# In This Directory

**gen\_cloudy\_input.py** - reformats UVB models into a format that CLOUDY will accept. Takes in 3 arguments:
* --ds (str): location of output file
* --uvb (str): location of UVB data
* --rs (str): set range for redshifts to iterate through (e.g. "1.2,2.7")

**full\_cloudy.py** - runs cloudy spectral synthesis simulations in parallel. Requires 6 arguments that are defined within the code:
* start_part - first part number in which the code will run from. The cloudy simulation is broken up into a number of parts to be run in parallel.
* end_part - final part number in which the code will run
* total_parts - total number of parts in cloudy run
* number of cores - number of gpu cores the code is run on
* par_file - location of parameter file (more details below)
* CIAOLoop_file - location of CIAOLoop file. Is where the spectral synthesis is run. Should be located within installation of cloudy_cooling_tools

**uvb\_params.par** - parameter file for cloudy simulation run. Includes all of the parameters that go into the cloudy run that are specified within the file. Here, there are two files of note that are required for cloudy to run:
* path to cloudy executable
* path to ultraviolet background data

**backup\_jobs** - directory containing job scripts for running cloudy simulations in several parts. Should only be used if 1-2 parts take significantly longer to converge than the rest. Otherwise, 'full_cloudy.py' should be run instead.

**combine\_runfile\_parts.pl** - if job scripts from 'backup_jobs' directory are run, combines output files of each job into a single run file. Note that this file is written in Perl, so it will need to be run as such.

**gen\_trident\_input.py** - takes in final run file (either from the output of full_cloudy.py or the output of combine_runfile_parts.pl) and outputs an ionization table in an h5 format that can be used in the trident.

**plot\_comp\_ion_frac.py** - creates pairwise 2D histogram comparison figures with the h5 files from *gen_trident_input.py*

**plot\_params.par** - parameter file for creating plot comparisons

### Example scripts for *gen\_uvb\_input.py*
### *Puchwein et al. 2019*

```
python gen_cloudy_input.py --ds /mnt/scratch/tairaeli/pcw_uvb_dat  --uvb /mnt/home/tairaeli/trident_uncertainty/mods/abundances/data_bin puchwein19_bkgthick.out
```

###  *Fauchere Guigere 2020*

```
python gen_cloudy_input.py --ds /mnt/scratch/tairaeli/fg_2020_uvb_dat --uvb /mnt/home/tairaeli/trident_uncertainty/mods/abundances/data_bin/fg20_spec_lambda.dat
```
