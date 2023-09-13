import argparse
import os

from package.utility import md_funcs as mdf

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--initial', 
                    help="initial trajectory folder # which contains trajectory that we will merge")
parser.add_argument('-f', '--final', 
                    help="final trajectory folder # which contains trajectory that we will merge")
parser.add_argument('-c', '--config', help='configuration file for auto_md')

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

analysis_script_repo = os.path.join(config_dict['auto_md directory'], 'codes', 'analysis') # change my name later
analysis_dir = os.path.join(working_dir, protname, 'analysis')

# path to the headers

header_path = os.path.join(config_dict['auto_md directory'], 'codes', 'headers', 'slurm.head')

start = int(args.initial)
end = int(args.final)
total_time = (end - start + 1)*5

## i a m still not a fan of a lot of these variable names

traj = f"combine_traj_{start}_{end}"
pdb = f"{protname}.pdb" # this is a pdb
rem_rotation = f"remove_rotation_{start}_{end}"
new_structure = f"{rem_rotation}/top.pdb"

# make analysis directory for cleanliness

if not os.path.isdir(analysis_dir):
    os.mkdir(analysis_dir)

# Write Initial Bash Script

# analysis setup script

## some of these filenames need to be changed

with open(os.path.join(analysis_script_repo, 'analysis.sh'), 'r') as f:
    analysis_setup = f.read().format(
        initial = start,
        final = end,
        directory = working_dir,
        fix_pdb_path = os.path.join(config_dict['auto_md directory'], 
                                    'package', 'utility', 'fix_pdb.py'),
        pdb = os.path.join(os.getcwd(), protname, 'start', pdb), # this may not be the correct path
        protname = protname,
        total_time = total_time,
        top = os.path.join(protname,'start', pdb),
        analysis_directory = analysis_dir,
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

with open(os.path.join(analysis_dir,'run_combinetraj.sh'), 'w') as w:
    w.write(f'{analysis_header}\n{analysis_setup}')
    
# Write cpptraj command list
## this is a terrible way to do this but it's the only thing that 
## works with both our installs


with open(os.path.join(analysis_dir,'combinetraj.cpptraj'), 'w') as w:
    w.write(f'parm {topology}\n')
    for i in range(start, end):
        w.write(f'trajin {protname}/prod/prod_{i}/prod5ns.nc\n')
    w.write(f'\ntrajout {start}-{end}_{protname}_prod{total_time}ns.nc\ngo')

combine_traj_text = f"""
parm {topology}

for i={start};i<{end};i++
    trajin {protname}/prod/prod_$i/prod5ns.nc
done

trajout {start}-{end}_{protname}_prod{total_time}ns.nc

go"""

#Write initial tcl_script
## i dont like how long this is

write_trr_text = f"""mol new {topology}
animate read netcdf combinetraj_{args.initial}_{args.final}/{args.initial}-{args.final}_{protname}_prod{total_time}ns.nc waitfor all 0
animate write trr trajectory.trr waitfor all 0 
quit"""

with open(os.path.join(analysis_dir, 'write_trr_test.tcl'), 'w') as w:
    w.write(write_trr_text)
    
# Write process_1.sh
## using previsouly made header

# formatting script text

with open(os.path.join(analysis_script_repo, 'le4pd_setup.sh'), 'r') as f:
    le4pd_setup = f.read().format(
        out_directory = rem_rotation,
        trajectory = os.path.join(f'amber2gromacs_{start}_{end}', 'trajectory.trr'),
        top = pdb,
        new_top = new_structure,
        run_name = protname,
        amber_solv_pdb = os.path.join(protname, 'start', f'amber_{protname}.pdb')
    )

# writing script

with open(os.path.join(analysis_dir, 'process_1.sh'), 'w') as f:
    f.write(f'{analysis_header}\n{le4pd_setup}')

#Execute bash script
## hashed it out here to see if the new sys_setup works

os.system(f"bash {protname}/analysis/run_combinetraj.sh")