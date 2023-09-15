import argparse
import os

from package.utility.md_funcs import read_sysconfig

parser = argparse.ArgumentParser(
    prog='system setup',
    description='reads system config and creates the system'
)

parser.add_argument('-i', '--config', default='gen_sim_config.in')

args = parser.parse_args()

config_dict = read_sysconfig(args.config)

# testing check

run = True
if config_dict['test'] == 'True':
    run = False

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

force_fields = os.path.join(config_dict['auto_md directory'], 'codes', 'sim_codes')

# out directories

start_dir = os.path.join(os.getcwd(), run_name, 'start')
config_dir = os.path.join(os.getcwd(), run_name, 'config')
out_dir = os.path.join(os.getcwd(), run_name, 'out')
em_dir = os.path.join(os.getcwd(), run_name, 'em')
heating_dir = os.path.join(os.getcwd(), run_name, 'heating')
npt_dir = os.path.join(os.getcwd(), run_name, 'npt')
prod_dir = os.path.join(os.getcwd(), run_name, 'prod')

# other code dirs

## unsure if we need pycode anymore

tleap_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'tleap')
#pycode_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'python')
sim_script_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'sim_scripts')

# run condiitons
## can remake this using a list of 'em' and things + f strings

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

# writing system setup bash script

# formatting system bash script

with open(os.path.join(sim_script_dir, 'sys_setup.sh'), 'r') as f:
    sys_setup = f.read().format(
        pdb_dir = pdb_dir,
        force_fields = force_fields,
        pdb = pdb,
        run_name = run_name,
        start_dir = start_dir,
        config_dir = config_dir,
        out_dir = out_dir,
        em_dir = em_dir,
        heating_dir = heating_dir,
        npt_dir = npt_dir,
        prod_dir = prod_dir,
        tleap_dir = tleap_dir,
        config_file = args.config
    )

# formatting system setup header

with open(header_path, 'r') as f:
    sys_head = f.read().format(
        md_type = 'system_setup',
        run_name = pdb,
        nodes = 1,
        mem = 32,
        partition = 'short', # should put something here in the config file
        time = '0-01:00:00',
        ntasks_per_node = 10,
        email = config_dict['email'],
        account = config_dict['account']
        )


# writing system setup bash script with header

with open(os.path.join(os.getcwd(), 'sys_setup.sh'), 'w') as f:
    f.write(f'{sys_head}\n{sys_setup}')

# write the amber scripts
## we can add the formatting thing here

md_steps = ['em', 'heating', 'npteq', 'prod', 'prod_restart']

# for formattable headers

for step in md_steps:

    # checking if speedrun protocol is active

    if step in ['npteq', 'prod'] and config_dict['speedrun'] in ['t', 'T', 'true', 'True', 'TRUE']:
        script_path = f'{sim_script_dir}/amber_{step}_speed.sh'

    else:
        script_path = f'{sim_script_dir}/amber_{step}.sh'

    # writing script headers    

    with open(f'{header_path}', 'r') as f:

        header = f.read().format(
            md_type=step, ## ORGANIZE MEEEEEEEEEEEEEEEE
            run_name=run_name, 
            email=email, 
            account=account,
            ## below here will need to change if we get rid of run_cond
            nodes=run_cond[step]['nodes'],
            partition=run_cond[step]['partition'],
            time= run_cond[step]['time'],
            mem=run_cond[step]['mem'],
            ntasks_per_node=run_cond[step]['ntasks_per_node']
            )
    
    # writing script body
    with open(f'{script_path}', 'r') as f:
        
        script_body = f.read().format(
            config_dir = config_dir,
            em_dir = em_dir,
            start_dir = start_dir,
            heating_dir = heating_dir,
            npt_dir = npt_dir,
            out_dir = out_dir,
            sim_codes = force_fields,
            run_name = run_name,
            le4pd_input = config_dict['run le4pd path'],
            config_file = args.config,
            prod_dir = prod_dir,
            max_iter = config_dict['max iterations'],

        )

    with open(os.path.join(os.getcwd(), f'amber_{step}.sh'), 'w') as w:
        w.write(f"{header}\n{script_body}")

if run:
    os.system("bash sys_setup.sh")
else:
    print('done, running "bash sys_setup.sh" will start the simulation')