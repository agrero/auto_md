# just to be safe
module purge

# Expanse
## these imports should be standardizedper platform
#module load python3
#module load cpu/0.17.3b  gcc/10.2.0/npcyll4  openmpi/4.1.3/oq3qvsv
#module load amber/22

# Talapas
source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

## make this prettier later

cpptraj combinetraj.cpptraj

mkdir combinetraj_{initial}_{final}
mv combinetraj.cpptraj combinetraj_{initial}_{final}
mv {initial}-{final}_{protname}_prod{total_time}ns.nc combinetraj_{initial}_{final}

set -e

module load vmd/1.9.3
vmd -dispdev text -e write_trr_test.tcl

python3 {fix_pdb_path} -pdb {pdb} -o {pdb}

bash process_1.sh

mv remove_rotation remove_rotation_{initial}_{final}

mkdir amber2gromacs_{initial}_{final}
mv trajectory.trr amber2gromacs_{initial}_{final}
mv {top} amber2gromacs_{initial}_{final}

mv combinetraj_{initial}_{final} {directory}
mv amber2gromacs_{initial}_{final} {directory}
mv remove_rotation_{initial}_{final} {directory}
