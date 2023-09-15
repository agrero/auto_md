source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

# all paths because .format is tedious
## will be removed in future iterations

config_dir=     {config_dir}
em_dir=         {em_dir}
start_dir=      {start_dir}
heating_dir=    {heating_dir}
npt_dir=        {npt_dir}
out_dir=        {out_dir}
prod_dir=       {prod_dir}
sim_codes=      {sim_codes}
run_name=       {run_name}
le4pd_input=    {le4pd_input}
config_file=    {config_file}
max_iter=       {max_iter}

nohup sander -O -i {config_dir}/in.npt \
    -o {out_dir}/npt.out \
    -p {start_dir}/{run_name}_solv.parm7 \
    -c {heating_dir}/{run_name}_md_heat.rst7 \
    -r {npt_dir}/{run_name}_npt.rst7 \
    -x {npt_dir}/{run_name}_npt.nc \
    -inf {npt_dir}/{run_name}_npt.mdinfo

## changet this from being manual later
cp auto_md/codes/sim_codes/prod5ns.in {config_dir}/prod5ns.in

for (( i=1; i<{max_iter} ; i++))
do
    mkdir {prod_dir}/iter$i
    sbatch amber_prod.sh {prod_dir}/iter$i
done