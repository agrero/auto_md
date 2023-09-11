import argparse
import os

parser = argparse.ArgumentParser(
    prog='system setup',
    description='reads system config and creates the system'
)

parser.add_argument('-i', '--config', default='gen_sim_config.in')

args = parser.parse_args()

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

# i'm going to need to split this up like i have the .in structured

# header info
account = config_dict['account']
email = config_dict['email']
header_path = os.path.join(config_dict['auto_md directory'], 'codes', 'headers', 'slurm.head')

# pdbs 
pdb_dir = config_dict['pdb directory']
pdb = config_dict['pdb name']
run_name = config_dict['run name']

# configs
force_fields = os.path.join(config_dict['auto_md directory'], 'codes', 'amber_codes', 'sim_codes')

## should really make this into a nested dictionary

start_dir=config_dict['out directories'][0]
config_dir=config_dict['out directories'][1]
out_dir=config_dict['out directories'][2]
em_dir=config_dict['out directories'][3]
heating_dir=config_dict['out directories'][4]
npt_dir=config_dict['out directories'][5]
prod_dir=config_dict['out directories'][6]

tleap_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'tleap')
pycode_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'python')

sim_script_dir = os.path.join(config_dict['auto_md directory', 'codes', 'amber_codes', 'sim_scripts']) #config_dict['simulation script directory']

# run condiitons
run_cond = {
    'em' : {
        'partition': config_dict['em partition'],
        'time' : config_dict['em time'],
        'mem' : config_dict['em mem'],
        'gpus_per_task' : 0, # will see later if its allowed to run with 0 here, if it does add it to config file
        'nodes' : config_dict['em nodes'],
        'ntasks_per_node' : config_dict['em ntasks-per-node'],
        'cpus_per_node' : config_dict['em cpus-per-node']
    },
    'heating' : {
        'partition': config_dict['heating partition'],
        'time' : config_dict['heating time'],
        'mem' : config_dict['heating mem'],
        'gpus_per_task' : 0, # see comment above in em
        'nodes' : config_dict['heating cpus-per-node'],
        'ntasks_per_node' : config_dict['heating ntasks-per-node'],
        'cpus_per_node' : config_dict['heating cpus-per-node']
    },
    'npteq' : {
        'partition': config_dict['npteq partition'],
        'time' : config_dict['npteq time'],
        'mem' : config_dict['npteq mem'],
        'gpus_per_task' : 0,
        'nodes' : config_dict['npteq nodes'],
        'ntasks_per_node' : config_dict['npteq ntasks-per-node'],
        'cpus_per_node' : config_dict['npteq cpus-per-node']
    },
    'prod' : {
        'partition': config_dict['production partition'],
        'time' : config_dict['production time'],
        'mem' : config_dict['production mem'],
        'gpus-per-task' : config_dict['production gpus-per-task'], 
        'nodes' : config_dict['production nodes'],
        'ntasks_per_node' : config_dict['production ntasks-per-node'],
        'cpus_per_node' : config_dict['production cpus-per-node']
    },
    'prod_restart' : {
        'partition': config_dict['production restart partition'],
        'time' : config_dict['production restart time'],
        'mem' : config_dict['production restart mem'],
        'gpus-per-task' : config_dict['production restart gpus-per-task'],
        'nodes' : config_dict['production restart nodes'],
        'ntasks_per_node' : config_dict['production restart ntasks-per-node'],
        'cpus_per_node' : config_dict['production restart cpus-per-node']
    }
}


new_text = f"""#!/bin/bash
# AMBER SYSTEM SETUP

# directories for pdbs and amber sim codes

set -e

pdb_dir={pdb_dir}
force_fields={force_fields}

pdb={pdb}
run_name={run_name}

# make the run name directory and cd into it

mkdir {run_name}
cd {run_name}

# source amber for tleap

source /gpfs/projects/guenzagrp/shared/amber22/amber.sh 

# define new directories for md run and make them 

start_dir={start_dir}
config_dir={config_dir}
out_dir={out_dir}
em_dir={em_dir}
heating_dir={heating_dir}
npt_dir={npt_dir}
prod_dir={prod_dir}

mkdir {start_dir} {config_dir} {out_dir} {em_dir} {heating_dir} {npt_dir} {prod_dir}

# fetch all necessary amber configs

cp {force_fields}/"in.classical_heating"   {config_dir}
cp {force_fields}/"in.npt"                 {config_dir}
cp {force_fields}/"prod5ns.in"             {config_dir}
cp {force_fields}/"sander_min.in"          {config_dir}

# get tleap.in file makers

cp {tleap_dir}/tleap_solvate.py        {config_dir}/tleap_solvate.py
cp {pycode_dir}/tleap_read_volume.py   {config_dir}/tleap_read_volume.py

# convert pdb to amber pdb

pdb4amber -i {pdb_dir}/{pdb} -o {start_dir}/{run_name}.pdb -y 

# get volume of the box as well as charge

python3 {config_dir}/tleap_solvate.py -p {start_dir}/{run_name}.pdb -c {config_dir} 

tleap -s -f {config_dir}/solvate_tleap.in > {out_dir}/tleap.out

# solvate the box with salt concentrations as determined by previous step

python3 {config_dir}/tleap_read_volume.py -to {out_dir}/tleap.out -c ../{args.config} \\
    -cond {config_dir} -p {start_dir}/{run_name}.pdb

tleap -s -f {config_dir}/tleap.in

mv leap.log out/

# Energy Minimization

# importing all scripts for running simulations 
## in the future will allow for custom script integration
mv ../amber_em.sh               amber_em.sh
mv ../amber_heating.sh          amber_heating.sh
mv ../amber_npteq.sh            amber_npteq.sh
mv ../amber_prod.sh             amber_prod.sh
mv ../amber_prod_restart.sh     amber_prod_restart.sh

sbatch amber_em.sh {em_dir} {start_dir} {config_dir} \\
    {run_name} {heating_dir} {npt_dir} {out_dir} {prod_dir}"""


# write the amber scripts
## we can add the formatting thing here
md_steps = ['em', 'heating', 'npteq', 'prod', 'prod_restart']
for step in md_steps:
    path = f"{sim_script_dir}_no_head/amber_{step}.sh" # what path amigo

    with open(f'/{header_path}', 'r') as f: # will need to change header so all parameters are mutable
        header = f.read().format(md_type=step, # ORGANIZE MEEEEEEEEEEEEEEEE
                                run_name=run_name, 
                                email=email, 
                                account=account,
                                nodes=run_cond[step]['nodes'],
                                partition=run_cond[step]['partition'],
                                time=':'.join(run_cond[step]['time']), # because of the colons
                                mem=run_cond[step]['mem'],
                                ntasks_per_node=run_cond[step]['ntasks_per_node'])
        if 'prod' in step:
            header += f"\n#SBATCH --gpus-per-task={run_cond[step]['gpus-per-task']}"
    with open(f'/{path}', 'r') as f:
        text = f.read()

    with open(f'amber_{step}.sh', 'w') as w:
        w.write(f"{header}\n{text}")

# write the system setup files
with open('sys_setup.sh', 'w') as w:
    w.write(new_text)

if config_dict['start here end there'] in ['t', 'T', 'True', 'true']:
    os.system(f"scp -r {run_name} {remote_user}@{remote_host}:{config_dict['remote directory']}")
else:
    os.system("bash sys_setup.sh")