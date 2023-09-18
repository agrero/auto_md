import argparse
from email.errors import HeaderParseError
import shutil
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
header_dir = os.path.join(config_dict['auto_md directory'], 'codes', 'headers')

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
npt_dir = os.path.join(os.getcwd(), run_name, 'npt')
prod_dir = os.path.join(os.getcwd(), run_name, 'prod')

# writing directories

try:
    os.mkdir(run_name)
except:
    print('that directory already exists silly')


for dir in [start_dir, config_dir, out_dir, em_dir, npt_dir, prod_dir]:
    try:
        os.mkdir(dir)
    except:
        print('that directory already exists silly')

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
    'restart' : {
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
# list out ion concentrations and types from the config file

## this is terrible please change me
charge_dict = {
    'MG' : 2,
    'NA' : 1,
    'CL' : 1
}

ion_concentrations = config_dict['ion concentrations']
ion_types = config_dict['ion types']


# format ion components based on how many their are

if type(ion_types) != list:
    ion_types = ion_types.strip(' ').strip('()').split(',')
else: 
    ion_types = [ion.strip(' ').strip('()').split(',') for ion in ion_types]

# adding ions for gromacs setup

add_ions_text = ''

for ndx, ion in enumerate(ion_types):
    with open(os.path.join(header_dir, 'gromacs_add_ions.sh'), 'r') as f:
        add_ions = f.read().format(
            run_name = run_name,
            start_dir = start_dir,
            p_ion = ion[0],
            p_charge = charge_dict[ion[0]],
            n_ion = ion[1],
            n_charge = charge_dict[ion[1]],
            conc = ion_concentrations[ndx]
        )
        add_ions_text += f'{add_ions}\n'

# writing the rest of the system setup script

with open(os.path.join(sim_script_dir, 'gromacs_setup.sh'), 'r') as f:
    setup_text = f.read().format(
        pdb_dir = pdb_dir,
        run_name = run_name,
        pdb = pdb,
        em_dir = em_dir,
        start_dir = start_dir,
        add_ions = add_ions_text
    )

with open(os.path.join(run_name, 'gromacs_setup.sh'), 'w') as w:
    w.write(setup_text)

# moving force fields to their respective directories

for i in ['em', 'prod', 'npt']:
    shutil.copy(os.path.join(force_fields, f'{i}.mdp'), os.path.join(run_name, i))


##############################
##### formatting scripts #####
##############################

gromacs_scripts = [i for i in os.listdir(sim_script_dir) if 'gromacs' in i]

for i in gromacs_scripts:
    # determine what step this is
    step = i.strip('.sh').split('_')[-1]

    ## bit of a time waster here
    if step == 'setup':
        continue

    with open(header_path, 'r') as f:
        gromacs_header = f.read().format(
            md_type = step,
            run_name = run_name,
            email = email,
            account = account,
            ## below will change if we get rid of run_cond
            nodes = run_cond[step]['nodes'],
            partition = run_cond[step]['partition'],
            time = run_cond[step]['time'],
            mem = run_cond[step]['mem'],
            ntasks_per_node = run_cond[step]['ntasks_per_node']
        )

    with open(os.path.join(sim_script_dir, i), 'r') as f:
        script_text = f.read().format(
            run_name = run_name,
            prot_name = run_name,
            em_dir = em_dir,
            npt_dir = npt_dir,
            start_dir = start_dir,
            prod_dir = prod_dir
        )

    with open(os.path.join(run_name, f'gromacs_{step}.sh'), 'w') as w:
        w.write(f'{gromacs_header}\n{script_text}')

if run:
    os.system(f"bash {os.path.join(os.getcwd(), run_name, 'gromacs_setup.sh')}")
else:
    print('done, running "bash gromacs_setup.sh" will start the simulation')