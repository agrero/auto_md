# auto_md
## a program designed to streamline the setting up and running of molecular dynamics simulations

# config
the most important aspect of this program is the config file as it controls how all the code 
will be run! below will detail each major section fo the configuration file and a general description on how
it is read in and what each component does.

## directories
all of the necessary directories to be read in and made for auto_md to run. a genereal theme
is that you should store all related files in the same directories. however if you wisehd
you could store everyting in a mega directory (set it as your working directory)
and just fill in the configuration file with just your working directory.

### pdb directory (read)
the directory in which you have your input pdb stored, don't put in the pdb name here just the 
path to the directory.

### config directory (read)
the directory where you store your md simulation run-configuration files

### out directories (write)
these are the output/input directories for each component of the molecular dynamics process,
these are: energy minimization (em), heating, npt (or nvt), and production (prod). in additon 
there are the start, out, and config directories. the start directory mainly handles the inputs into the energy 
miniimzation step as well as storing a copy of the input pdb, the out directory mainly is for slurm outputs to
keep each directory clean. the order in which these are inputed are:
> start : config : out : em : heating : npt : production
note the colons are used to seperate each instance, think of it as a comma for a list

### tleap code directories (read)
! in the future will be merged with python codes !
this is specifically where tleap.solvate is stored

### simulation script directory (read)
the directory in which you store bash scripts for running specific pieces of your simulation.
the currently required scripts are for energy minimization, heating, npt or nvt, production, and production from restart
these would prefereably not have any job queing headers like that for a slurm system, as a main component of the script 
is to generate said headers from the configuration file. However there are plans in the future to allow for 
just general scripts to be used so you dont have to make them each time, or if some 'special touch' may be necessary

### python codes (read)
! in the future will be the repo for all python codes sans the system_setup script !

## filenames
consists of the **pdb name** and the **run name** the latter of which will default to the pdb name if empty

## ion concentrations
the concentrations and types are directly linked and if improperly entered will cause a litany of issues
currently only accepts compounds with 2 species **(Mg is the only currently accepted divalent cation)**
example:
> ion concentrations: 150: 6

> ion types: (Na+,Cl-) : (Mg,Cl-)

this will add 150 mM NaCl to your system in addition to 6mM MgCl2

so the general pattern is **cation** : **anion** and the order of which should match the concentrations

! for later iterations we will make a chemical formula parser for simpler ion type entry !

for an unknown reason, monovalent ions need to have charges associated with them! Mg seems to work fine as 
just itself

## header 
specifically for a slurm job header, a template of what this looks like is available in **codes/headers**
this just adds the email for the job starting and finishing
the account is for which account to be charged
the header path should point to whichever header you're going to be using

## components
these components are specifically for controlling a slurm managed job's resources

## misc

### contains dna 
adds the OB21 force field during the system setup phase using tleap

## future wants/dreams
- make changes so that it can also be run on expanse/locally
    - mostly involve allowing for amber function calls to be different (i'm looking at you mpi)
- all filepaths be run through a custom implementation of the os module
    - makes handling different filetypes easier regardless of operating system
    - custom implementation mostly is in regards to handling local/./global imports
- functionalize a lot of the repeated code
- oopify the whole thing
- error handling from the configuration file, makes sure that if the correct number
of options is not inputted, the program will just put/read everything from the main directory