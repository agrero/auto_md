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

nohup sander -O -i {config_dir}/sander_min.in \
    -o {em_dir}/min.out \
    -p {start_dir}/{run_name}_solv.parm7 \
    -c {start_dir}/{run_name}_solv.rst7 \
    -r {em_dir}/{run_name}_solv.min

# remember to add the heating copy and run step here
sbatch amber_heating.sh