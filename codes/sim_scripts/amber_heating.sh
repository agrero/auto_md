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

nohup sander -O -i {config_dir}/in.classical_heating \
    -o {heating_dir}/heating.out \
    -p {start_dir}/{run_name}_solv.parm7 \
    -c {em_dir}/{run_name}_solv.min \
    -r {heating_dir}/{run_name}_md_heat.rst7 \
    -x {heating_dir}/{run_name}_md_heat.nc

sbatch amber_npteq.sh 