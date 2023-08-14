source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

# might wanna reorder these with

# directories
em_dir=$1    # outputs
start_dir=$2 # inputs 
config_dir=$3

# files
run_name=$4

# for subsequent runs (has to be a more efficient way to do this)
heating_dir=$5



nohup sander -O -i ${config_dir}/sander_min.in -o ${em_dir}/min.out \
    -p ${start_dir}/${run_name}_solv.parm7 -c ${start_dir}/${run_name}_solv.rst7 \
    -r ${em_dir}/${run_name}_solv.min

# remember to add the heating copy and run step here
sbatch amber_heating.sh ${em_dir} ${start_dir} ${config_dir} ${heating_dir} ${run_name}