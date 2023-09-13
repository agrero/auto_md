# just to be safe

# Expanse
## these imports should be standardizedper platform
#module load python3
#module load cpu/0.17.3b  gcc/10.2.0/npcyll4  openmpi/4.1.3/oq3qvsv
#module load amber/22

# Talapas

module load python3
source /gpfs/projects/guenzagrp/shared/amber22/amber.sh
#module load intel/17 amber/12

## make this prettier later
echo $PWD

set -e

cpptraj -i {analysis_directory}/combinetraj.cpptraj

## wait why didn't he do this when he made the files?
mkdir combinetraj_{initial}_{final}

mv {initial}-{final}_{protname}_prod{total_time}ns.nc combinetraj_{initial}_{final}

module load vmd/1.9.3
vmd -dispdev text \
    -e {analysis_directory}/write_trr_test.tcl

python3 {fix_pdb_path} -pdb {pdb} \
    -o {pdb}


mkdir amber2gromacs_{initial}_{final}
mv trajectory.trr amber2gromacs_{initial}_{final}
## he never should have moved this
## change the code so you can remove this line entirely 
cp {top} amber2gromacs_{initial}_{final}

## change this later to make it put these in the analysis directory
#mv combinetraj_{initial}_{final} {directory}

mkdir remove_rotation_{initial}_{final}

bash {analysis_directory}/process_1.sh

exit