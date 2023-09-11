
## talapas
module load intel/19
module load gromacs/2019.4

## expanse
#module load cpu/0.17.3b  gcc/10.2.0/npcyll4  openmpi/4.1.3/oq3qvsv
#module load gromacs/2020.4/65gq3je-omp

mkdir {out_directory}

set -e

gmx=`which gmx_mpi`
#Dump centered topology file
echo "1" | $gmx trjconv -f {trajectory} -s {structure} -dump 0 -o {out_directory}/top.pdb

$gmx editconf -f {out_directory}/top.pdb -c -center 0 0 0 -o {out_directory}/{run_name}top.pdb

#Do this for PCA

# sasa
echo "1" | $gmx sasa -quiet -f {trajectory} -s {structure} -or {out_directory}/resarea.xvg -dt 10

#Correct PBCs
echo "3 1" | $gmx trjconv -quiet -f {trajectory} -s {new_top} -o {out_directory}/after_pbc.xtc -pbc whole -center -boxcenter zero

echo "3 1" | $gmx trjconv -quiet -f {out_directory}/after_pbc.xtc -s {new_top} -fit rot -o {out_directory}/after_rot.xtc

#Dump the processed trajectory, CA only
echo "3 3" | $gmx trjconv -quiet -f {out_directory}/after_rot.xtc -s {new_top} -o {out_directory}/CA.xtc 
echo "3" | $gmx trjconv -quiet -f {out_directory}/after_rot.xtc -s {new_top} -o {out_directory}/CA.pdb -dump 0

#Create g96 for LE4PD-XYZ

echo "3" | $gmx trjconv -f {out_directory}/after_pbc.xtc -s {new_top} -o {out_directory}/{run_name}_rot.g96 #alpha-carbons with rotations
echo "1 1" | $gmx trjconv -f {out_directory}/after_pbc.xtc -s {new_top} -o {out_directory}/after_rot_{run_name}.xtc -fit rot+trans #remove rotations and translations of protein

echo "3" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc -s {new_top} -o {out_directory}/{run_name}.g96  #alpha-carbons 
echo "3" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc -o {out_directory}/{run_name}_first.pdb -s {new_top} -dump 0 #make pdb file
echo "1" | $gmx trjconv -f {out_directory}/after_rot_{run_name}.xtc -o {out_directory}/{run_name}.gro -s {new_top} -dump 0 #make .gro file
echo "1" | $gmx sasa -f {out_directory}/after_rot_{run_name}.xtc -s {new_top} -or {out_directory}/resarea.xvg  -dt 1000 #solvent exposed surface area calculation

mkdir {out_directory}/LE4PD_Inputs
cp {out_directory}/{run_name}.g96 {out_directory}/LE4PD_Inputs
cp {out_directory}/{run_name}_first.pdb {out_directory}/LE4PD_Inputs
cp {out_directory}/resarea.xvg {out_directory}/LE4PD_Inputs

exit