module load intel/19
module load gromacs/2019.4

set -e

# run name = {run_name}
# prot_name = {run_name}
# em_dir = {em_dir}
# npt_dir = {npt_dir}
# start_dir = {start_dir}
# prod_dir = {prod_dir}

gmx grompp -v -f {npt_dir}/npt.mdp \
    -c {em_dir}/em_{prot_name}.gro \
    -r {em_dir}/em_{prot_name}.gro \
    -o {npt_dir}/npt_{prot_name}.tpr \
    -p {start_dir}/sys.top -maxwarn 5

gmx mdrun -v -s {npt_dir}/npt_{prot_name}.tpr \
    -o {npt_dir}/npt_{prot_name}.trr \
    -c {em_dir}/em_{prot_name}.gro \
    -g {npt_dir}/npt_{prot_name}.log \
    -e {npt_dir}/npt_edr.edr \
    -ntomp 1

#sbatch {run_name}/gromacs_prod.sh