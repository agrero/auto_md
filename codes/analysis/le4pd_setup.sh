
## talapas
module load intel/19
module load gromacs/2019.4

## expanse
#module load cpu/0.17.3b  gcc/10.2.0/npcyll4  openmpi/4.1.3/oq3qvsv
#module load gromacs/2020.4/65gq3je-omp


set -e

gmx=`which gmx_mpi`

#Dump centered topology file

echo "Dump Centered Topology File "

echo "1" | $gmx trjconv -f {trajectory} \
    -s {amber_solv_pdb} -dump 0 \
    -o {out_directory}/top.pdb

echo "edit configuration"

$gmx editconf -f {out_directory}/top.pdb -c -center 0 0 0 \
    -o {out_directory}/{run_name}_top.pdb

#Do this for PCA

# sasa
echo "1" | $gmx sasa -quiet -f {trajectory} \
    -s {amber_solv_pdb} \
    -or {out_directory}/resarea.xvg -dt 10

echo "part 5"

#Correct PBCs
echo "3 1" | $gmx trjconv -quiet -f {trajectory} \
    -s {new_top} \
    -o {out_directory}/after_pbc.xtc \
    -pbc whole -center -boxcenter zero


echo "part 6"

echo "3 1" | $gmx trjconv -quiet -f {out_directory}/after_pbc.xtc \
    -s {new_top} -fit rot \
    -o {out_directory}/after_rot.xtc

echo "part 7"

#Dump the processed trajectory, CA only
echo "3 3" | $gmx trjconv -quiet -f {out_directory}/after_rot.xtc \
    -s {new_top} \
    -o {out_directory}/CA.xtc 

echo "part 8"

echo "3" | $gmx trjconv -quiet -f {out_directory}/after_rot.xtc \
    -s {new_top} \
    -o {out_directory}/CA.pdb -dump 0

#Create g96 for LE4PD-XYZ
## echo only works if all you have is ions and protein\

echo "part 9"

echo "3" | $gmx trjconv -f {out_directory}/after_pbc.xtc \
    -s {new_top} \
    -o {out_directory}/{run_name}_rot.g96 #alpha-carbons with rotations

echo "part 10"

echo "1 1" | $gmx trjconv -f {out_directory}/after_pbc.xtc \
    -s {new_top} \
    -o {out_directory}/after_rot_{run_name}.xtc \
    -fit rot+trans #remove rotations and translations of protein

echo "part 11"

echo "3" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc \
    -s {new_top} \
    -o {out_directory}/{run_name}.g96  #alpha-carbons 

echo "part 12"

echo "3" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc \
    -o {out_directory}/{run_name}_first.pdb \
    -s {new_top} -dump 0 #make pdb file

echo "part 13"

echo "1" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc \
    -o {out_directory}/{run_name}.gro \
    -s {new_top} -dump 0 #make .gro file

echo "part 14"

echo "1" | $gmx sasa -f {out_directory}/after_rot_{run_name}.xtc \
    -s {new_top} \
    -or {out_directory}/resarea.xvg  -dt 1000 #solvent exposed surface area calculation

echo "part 15"

mkdir {out_directory}/LE4PD_Inputs
cp {out_directory}/{run_name}.g96 {out_directory}/LE4PD_Inputs
cp {out_directory}/{run_name}_first.pdb {out_directory}/LE4PD_Inputs
cp {out_directory}/resarea.xvg {out_directory}/LE4PD_Inputs

exit