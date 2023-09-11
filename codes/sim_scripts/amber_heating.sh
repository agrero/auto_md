source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

em_dir=$1
start_dir=$2
config_dir=$3
heating_dir=$4

run_name=$5
npt_dir=$6
out_dir=$7
prod_dir=$8

nohup sander -O -i ${config_dir}/in.classical_heating -o ${heating_dir}/heating.out \
    -p ${start_dir}/${run_name}_solv.parm7 -c ${em_dir}/${run_name}_solv.min \
    -r ${heating_dir}/${run_name}_md_heat.rst7 -x ${heating_dir}/${run_name}_md_heat.nc

sbatch amber_npteq.sh ${npt_dir} ${start_dir} ${config_dir} ${out_dir} ${heating_dir} \
    ${run_name} ${prod_dir}