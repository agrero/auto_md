import argparse
import os

from package.utility import md_funcs as mdf

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--initial', 
                    help="initial trajectory folder # which contains trajectory that we will merge")
parser.add_argument('-f', '--final', 
                    help="final trajectory folder # which contains trajectory that we will merge")

args = parser.parse_args()

#### Generating Configuration Dictionary ####

config_dict = mdf.read_sysconfig(args.config)

#### Defining Directories ####

# current working directory

working_dir = os.getcwd()
protname = config_dict['run name']

# start_directory is directory to parm7 file with file name included

topology = os.path.join(working_dir, protname, 'start', f"{protname}_solv.parm7") 

# pdb directory is directory to pdb file with file name included

pdb_directory= os.path.join(config_dict['pdb directory'], config_dict['pdb name'])

# directory containing analysis script material

analysis_directory = os.path.join(config_dict['auto_md directory'], 'codes', 'analysis')

# path to the headers

header_path = os.path.join(config_dict['auto_md directory'], 'codes', 'headers', 'slurm.head')


start = int(args.initial)
end = int(args.final)
total_time = (end - start + 1)*5

## i a m still not a fan of a lot of these variable names

traj = f"combine_traj_{start}_{end}"
pdb = f"{protname}_solvated.pdb" # this is a pdb
rem_rotation = "remove_rotation"
new_structure = f"{rem_rotation}/structure.pdb"

# Write Initial Bash Script

# analysis setup script

with open(os.path.join(analysis_directory, 'analysis.sh'), 'r') as f:
    analysis_setup = f.read().format(
        initial = start,
        final = end,
        directory = working_dir,
        fix_pdb_path = os.path.join(config_dict['auto_md directory'], 
                                    'package', 'utility', 'fix_pdb.py'),
        pdb = os.path.join(os.getcwd(), protname, 'start', pdb) # this may not be the correct path
    )

## should make filling out a header a function
# slurm header

with open(header_path, 'r') as f:
    analysis_header = f.read().format(
        md_type = 'analysis',
        run_name = protname,
        nodes = config_dict['analysis nodes'],
        mem = config_dict['analysis mem'],
        partition = config_dict['analysis partition'],
        time = config_dict['analysis time'],
        ntasks_per_node = config_dict['analysis ntasks-per-node'],
        email = config_dict['email'],
        account = config_dict['account']
    )

# write script

with open(os.path.join(os.getcwd(),'run_combinetraj.sh'), 'w') as w:
    w.write(f'{analysis_header}\n{analysis_setup}')
    
# Write cpptraj command list

combine_traj_text = f"""
parm {topology}

for i={start};i<{end};i++
    trajin prod/prod_$i/prod5ns.nc
done

trajout {start}-{end}_{protname}_prod{total_time}ns.nc

go"""

with open(os.path.join(os.getcwd(),'combinetraj_test.cpptraj'), 'w') as w:

    w.write(combine_traj_text)

#Write initial tcl_script
## i dont like how long this is
write_trr_text = f"""mol new {topology}
animate read netcdf combinetraj_{args.initial}_{args.final}/{args.initial}-{args.final}_{protname}_prod{total_time}ns.nc waitfor all 0
animate write trr trajectory.trr waitfor all 0 
quit"""

with open(os.path.join(os.getcwd(), 'write_trr_test.tcl'), 'w') as w:
    w.write(write_trr_text)
    
# Write process_1.sh
## using previsouly made header

# formatting script text
with open(os.path.join(analysis_directory, 'le4pd_setup.sh'), 'r') as f:
    le4pd_setup = f.read().format(
        out_directory = rem_rotation,
        trajectory = traj,
        top = pdb,
        new_top = new_structure,
        run_name = protname
    )

# writing script
with open(os.path.join(os.getcwd(), 'process_1.sh'), 'w') as f:
    f.write(f'{analysis_header}\n{le4pd_setup}')

#Execute bash script
## hashed it out here to see if the new sys_setup works

#os.system("bash run_combinetraj.sh")