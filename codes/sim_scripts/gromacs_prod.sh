module load intel/19
module load gromacs/2019.4

set -e 

# run name = {run_name}
# prot_name = {run_name}
# em_dir = {em_dir}
# npt_dir = {npt_dir}
# start_dir = {start_dir}
# prod_dir = {prod_dir}/iter_i

gmx grompp -v -f {prod_dir}/pro.mdp \
    -c {em_dir}/em_{prot_name}.gro \
    -r {em_dir}/em_{prot_name}.gro \
    -o {prod_dir}/pro_{prot_name}.tpr \
    -p {start_dir}/sys.top -maxwarn 5

gmx mdrun -v -s {prod_dir}/pro_{prot_name}.tpr \
    -o {prod_dir}/pro_{prot_name}.trr \
    -c {em_dir}/em_{prot_name}.gro \
    -g {prod_dir}/pro_{prot_name}.log \
    -e {prod_dir}/pro_edr.edr \
    -ntomp 1
