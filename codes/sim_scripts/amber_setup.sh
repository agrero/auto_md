# AMBER SYSTEM SETUP
# source amber for tleap
module load python3

source /gpfs/projects/guenzagrp/shared/amber22/amber.sh 

# directories for pdbs and amber sim codes

pdb_dir={pdb_dir}
force_fields={force_fields}

pdb={pdb}
run_name={run_name}

# make the run name directory and cd into it

mkdir {run_name}
cd {run_name}

# define new directories for md run and make them 

start_dir={start_dir}
config_dir={config_dir}
out_dir={out_dir}
em_dir={em_dir}
heating_dir={heating_dir}
npt_dir={npt_dir}
prod_dir={prod_dir}

mkdir $start_dir $config_dir $out_dir $em_dir $heating_dir $npt_dir $prod_dir

cp {force_fields}/"in.classical_heating"   {config_dir}
cp {force_fields}/"in.npt"                 {config_dir}
cp {force_fields}/"prod5ns.in"             {config_dir}
cp {force_fields}/"sander_min.in"          {config_dir}

# convert pdb to amber pdb

pdb4amber -i {pdb_dir}/{pdb} \
    -o {start_dir}/{run_name}.pdb -y 

# get volume of the box as well as charge

python3 {tleap_dir}/tleap_solvate.py \
    -p {start_dir}/{run_name}.pdb \
    -c {config_dir} 

tleap -s -f {config_dir}/solvate_tleap.in > {out_dir}/tleap.out

# solvate the box with salt concentrations as determined by previous step

python3 {tleap_dir}/tleap_read_volume.py \
    -to {out_dir}/tleap.out \
    -c {config_file} \
    -cond {config_dir} \

tleap -s -f {config_dir}/tleap.in

mv leap.log out/

# Energy Minimization

# importing all scripts for running simulations 
## move this to sys_setup.py
mv ../amber_em.sh               amber_em.sh
mv ../amber_heating.sh          amber_heating.sh
mv ../amber_npteq.sh            amber_npteq.sh
mv ../amber_prod.sh             amber_prod.sh
mv ../amber_prod_restart.sh     amber_prod_restart.sh

sbatch amber_em.sh 