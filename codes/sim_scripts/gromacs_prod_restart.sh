module load intel/19
module load gromacs/2019.4

set -e

# run name = {run_name}
# prot_name = {run_name}
# em_dir = {em_dir}
# npt_dir = {npt_dir}
# start_dir = {start_dir}
# prod_dir = {prod_dir}

gmx mdrun -v -s {prod_dir}/pro_{prot_name}.tpr \
    -cpi state.cpt -append \
    -g {prod_dir}/pro_{prot_name}.log \
    -x traj_comp.xtc \
    -o {prod_dir}/pro_{prot_name}.trr \
    -e {prod_dir}/pro_edr.edr \
    -ntomp 1