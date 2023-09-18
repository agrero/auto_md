module load intel/19
module load gromacs/2019.4

set -e

# run name = {run_name}
# prot_name = {run_name}
# em_dir = {em_dir}
# npt_dir = {npt_dir}
# start_dir = {start_dir}
# prod_dir = {prod_dir}

gmx mdrun -v -s {em_dir}/em_{prot_name}.tpr \
    -o {em_dir}/em_{prot_name}.trr \
    -c {em_dir}/em_{prot_name}.gro \
    -g {em_dir}/em_{prot_name}.log \
    -e {em_dir}/em_edr.edr \
    -ntomp 1    

sbatch {run_name}/gromacs_npteq.sh