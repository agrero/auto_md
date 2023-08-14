#!/bin/bash
#SBATCH --job-name=heat-%j%
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --partition=short
#SBATCH --time=0-10:00:00
#SBATCH --error=out/heat-%j%.err
#SBATCH --out=out/heat-%j%.out
#SBATCH --ntasks-per-node=10 
#SBATCH --mail-type=end
#SBATCH --mail-user=aguerre2@uoregon.edu
#SBATCH --export=ALL
#SBATCH --account=guenzagrp

source /gpfs/projects/guenzagrp/shared/amber22/amber.sh

em_dir=$1
start_dir=$2
config_dir=$3
heating_dir=$4

run_name=$5

nohup sander -O -i ${config_dir}/in.classical_heating -o ${heating_dir}/heating.out \
    -p ${start_dir}/${run_name}_solv.parm7 -c ${em_dir}/${run_name}_solv.min \
    -r ${heating_dir}/${run_name}_md_heat.rst7 -x ${heating_dir}/${run_name}_md_heat.nc

