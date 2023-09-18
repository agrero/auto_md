### runs md from scratch, copying from the base directory

module load intel/19
module load gromacs/2019.4

# change me depending on what the run name is
run_name={run_name} # cw = closed with

set -e

# prepare the box
gmx pdb2gmx -f {pdb_dir}/{pdb} \
    -o {em_dir}/{run_name}.gro \
    -p {start_dir}/sys.top \
    -ignh -ff "amber03" -water "tip3p" \
    -i {start_dir}/ff_{run_name}

gmx editconf -f {em_dir}/{run_name}.gro \
    -bt cubic -d 0.9 -box 25 25 25 \
    -o {em_dir}/boxed.gro

# solvate system
gmx solvate -cp {em_dir}/boxed.gro \
    -p {start_dir}/sys.top \
    -o {em_dir}/solvated.pdb

# add ions
touch {start_dir}/ions.mdp

# neutralizing

gmx grompp -c {em_dir}/solvated.pdb \
    -r {em_dir}/solvated.pdb \
    -f {start_dir}/ions.mdp \
    -p {start_dir}/sys.top \
    -o {start_dir}/temp_ions.tpr \
    -maxwarn 5

echo "SOL" | gmx genion -s {start_dir}/temp_ions.tpr \
    -p {start_dir}/sys.top \
    -o {start_dir}/temp_{run_name}.gro \
    -pname NA -pq 1 -nname CL -nq 1 -neutral 

{add_ions}

# energy minimzation

sbatch gromacs_em.sh