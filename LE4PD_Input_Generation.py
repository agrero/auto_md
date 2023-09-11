import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--name', help="name of experiment condition")
parser.add_argument('-i', '--initial', help="initial trajectory folder # which contains trajectory that we will merge")
parser.add_argument('-f', '--final', help="final trajectory folder # which contains trajectory that we will merge")

args = parser.parse_args()


## REPLACE ME WITH AN IMPORTED FUNCTION PLEASE
config_dict = {}

try:
    with open(args.config, 'r') as f:
        text = [i for i in f.read().split('\n') if '>' in i]
        for i in text:
            
            var = i.strip('>')
            
            if len(var.split(':')) > 2:
                config_dict[var.split(':')[0]] = [j.strip(' ') for j in var.split(':')[1:]]
            else:
                config_dict[var.split(':')[0]] = var.split(':')[1].strip(' ')

except:
    raise FileNotFoundError('File could not be found')

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
        directory = working_dir
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
with open('run_combinetraj.sh', 'w') as w:
    w.write(f'{analysis_header}\n{analysis_setup}')
    
# Write cpptraj command list

combine_traj_text = f"""
parm {topology}

for i={start};i<{end};i++
    trajin prod/prod_$i/prod5ns.nc
done

trajout {start}-{end}_{protname}_prod{total_time}ns.nc

go"""

with open('combinetraj_test.cpptraj', 'w') as w:
    w.write(combine_traj_text)


#Write initial tcl_script

write_trr_text = f"""mol new {topology}
animate read netcdf combinetraj_{args.initial}_{args.final}/{args.initial}-{args.final}_{protname}_prod{total_time}ns.nc waitfor all 0
animate write trr trajectory.trr waitfor all 0 
quit"""

with open('write_trr_test.tcl', 'w') as w:
    w.write(write_trr_text)
    
#Write correct_pdb.py
## i'm coming back to you

correct_pdb_text = f"""# Read in the file
with open('{pdb_directory}', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('MG', 'Mg')
filedata = filedata.replace('ZN', 'Zn')

# Write the file out again
with open('{pdb}', 'w') as file:
  file.write(filedata)"""

with open('correct_pdb.py', 'w') as w:
    w.write(correct_pdb_text)
    
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
with open('process_1.sh', 'w') as f:
    f.write(f'{analysis_header}\n{le4pd_setup}')

#Execute bash script

## its a bash script here but they don't queue it with sbatch (even though it does have a header)

os.system("bash run_combinetraj.sh")







