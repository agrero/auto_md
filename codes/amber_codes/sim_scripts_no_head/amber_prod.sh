source /gpfs/projects/guenzagrp/shared/amber22/amber.sh
module purge
module load slurm
module load racs-spack
module list
echo $PWD
BD=$PWD
cd ${BD}

# spack install amber@20 %gcc +x11 +mpi +cuda ^cuda@10.2.89 ^intel-mpi
spack load /xendci3j
spack find --loaded
echo

# just verify we have GPUs
nvidia-smi
echo
hostname
echo

prod_dir=$1
start_dir=$2
heating_dir=$3
config_dir=$4
run_name=$5

cp ${heating_dir}/${run_name}_md_heat.rst7 ${prod_dir}/input.rst7

for ((K=1;K<=20;K++)); do
    cd $BD
    srun pmemd.cuda.MPI -O -i ${config_dir}/prod5ns.in \
    -o ${prod_dir}/prod5ns.out -p ${start_dir}/${run_name}_solv.parm7 \
    -c ${prod_dir}/input.rst7 -r ${prod_dir}/prod5ns.rst7 \
    -x ${prod_dir}/prod5ns.nc -inf ${prod_dir}/prod5ns.info
    ​
    mkdir ${prod_dir}/prod_${K}
    cp ${prod_dir}/prod5ns.info  ${prod_dir}/prod_${K}/prod5ns.info
    cp ${prod_dir}/prod5ns.nc	 ${prod_dir}/prod_${K}/prod5ns.nc
    cp ${prod_dir}/prod5ns.out   ${prod_dir}/prod_${K}/prod5ns.out
    cp ${prod_dir}/prod5ns.rst7  ${prod_dir}/prod_${K}/prod5ns.rst7
    cp ${prod_dir}/prod5ns.rst7  ${prod_dir}/input.rst7
done

sbatch amber_prod_restart.sh ${prod_dir} ${start_dir} ${config_dir} ${run_name} ${K}

exit
