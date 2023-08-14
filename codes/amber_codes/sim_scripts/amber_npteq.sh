#!/bin/bash
#SBATCH --job-name="amber2-npteq_gp32"
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --partition=short
#SBATCH --time=0-10:00:00
#SBATCH --error=out/npt-%j.err
#SBATCH --out=out/npt-%j.err
#SBATCH --ntasks-per-node=10
#SBATCH --mail-type=end
#SBATCH --mail-user=aguerre2@uoregon.edu
#SBATCH --export=ALL
#SBATCH --account=guenzagrp

source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

npt_dir=$1
start_dir=$2
config_dir=$3
out_dir=$4
heating_dir=$5

run_name=$6

# to add
prod_dir=$7



nohup sander -O -i ${config_dir}/in.npt -o ${out_dir}/npt.out -p ${start_dir}/${run_name}_solv.parm7 \
    -c ${heating_dir}/${run_name}_md_heat.rst7 -r ${npt_dir}/${run_name}_npt.rst7 \
    -x ${npt_dir}/${run_name}_npt.nc -inf ${npt_dir}/${run_name}_npt.mdinfo

cp /home/aguerre2/guenzagrp/codes/amber_codes/sim_codes/prod5ns.in ${config_dir}/prod5ns.in

sbatch simul.sh ${prod_dir} ${start_dir} ${heating_dir} ${config_dir} ${run_name}