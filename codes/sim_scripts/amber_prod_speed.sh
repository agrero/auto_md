source /gpfs/projects/guenzagrp/shared/amber22/amber.sh
module purge
module load slurm
module load racs-spack
module load python3
module list
echo $PWD
BD=$PWD
cd $BD

# spack install amber@20 %gcc +x11 +mpi +cuda ^cuda@10.2.89 ^intel-mpi
spack load /xendci3j
spack find --loaded
echo

# just verify we have GPUs
nvidia-smi
echo
hostname
echo

prod_dir=$1 # {prod_dir}

config_dir=     {config_dir}
em_dir=         {em_dir}
start_dir=      {start_dir}
heating_dir=    {heating_dir}
npt_dir=        {npt_dir}
out_dir=        {out_dir}
sim_codes=      {sim_codes}
run_name=       {run_name}
le4pd_input=    {le4pd_input}
config_file=    {config_file}
max_iter=       {max_iter}

cp {heating_dir}/{run_name}_md_heat.rst7 $prod_dir/input.rst7

for ((K=1;K<=20;K++)); do
    cd $BD
    srun pmemd.cuda.MPI -O -i {config_dir}/prod5ns.in \
    -o $prod_dir/prod5ns.out -p {start_dir}/{run_name}_solv.parm7 \
    -c $prod_dir/input.rst7 -r $prod_dir/prod5ns.rst7 \
    -x $prod_dir/prod5ns.nc -inf $prod_dir/prod5ns.info
    ​
    mkdir $prod_dir/prod_$K
    cp $prod_dir/prod5ns.info  $prod_dir/prod_$K/prod5ns.info
    cp $prod_dir/prod5ns.nc	 $prod_dir/prod_$K/prod5ns.nc
    cp $prod_dir/prod5ns.out   $prod_dir/prod_$K/prod5ns.out
    cp $prod_dir/prod5ns.rst7  $prod_dir/prod_$K/prod5ns.rst7
    cp $prod_dir/prod5ns.rst7  $prod_dir/input.rst7
done

# formatting outputs to be LE4PD compatible

## currently not probable to pull off
## could have a script check to see if each production run is finished
## currently I'm thinking it reads in some file in the main production directory
## if the number is over whatever level it runs le4pd inptus
## if the number is not large enough, add 1 and rewrite the file

## a potentially better way would be to write a complete file where it writes in some 
## complete file and we check for n of those instead

## finally we could have the script check the queue to see if the simulation is done or not
## a mixture of both may be best for bug fixing
#python3 {le4pd_input} \
#    -i 1 \
#    -f 20 \
#    -c {config_file}

exit
