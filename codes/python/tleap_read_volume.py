import argparse
import os 

parser = argparse.ArgumentParser(
    prog='tleap solvate read',
    description='reads tleap out files for the box volume'
)

parser.add_argument('-c', '--config', default='gen_sim_config.in')
parser.add_argument('-to', '--tleap_out', default='tleap.out')

parser.add_argument('-o', '--start_dir', default='start')
parser.add_argument('-cond', '--config_dir', default='test')
parser.add_argument('-p', '--pdb_path')

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

ion_concentrations = config_dict['ion concentrations']
ion_types = config_dict['ion types (same order)']

if type(ion_types) != list:
    ion_types = ion_types.strip(' ').strip('()').split(',')
    print(ion_types)
else: 
    ion_types = [ion.strip(' ').strip('()').split(',') for ion in ion_types]
    print(ion_types)


with open(args.tleap_out, 'r') as f:
    volume_text = [i for i in f.read().split('\n') if 'Volume' in i]
    vol_comp = volume_text[0].split(' ')
    volume = float(vol_comp[3])

volume_l = volume / (((10**10)**3)) * ((10**2)**3) / (10**3)

no_ions_lines = []

if type(ion_concentrations) == list:

    for ndx, conc in enumerate(ion_concentrations):
        no_atoms = int(conc) / (10 ** 3) * (6.022 * 10 ** 23)
        no_ions = (no_atoms * volume_l)
        # need to zip the two together

        if ion_types[ndx][0] == 'Mg': # be more clever later
            line = f'addIonsRand system {ion_types[ndx][0]} {round(no_ions)} {ion_types[ndx][1]} {2*round(no_ions)}'    
        else:
            line = f'addIonsRand system {ion_types[ndx][0]} {round(no_ions)} {ion_types[ndx][1]} {round(no_ions)}'
        no_ions_lines.append(line)

else:
    no_atoms = int(ion_concentrations) / (10 ** 3) * (6.022 * 10 ** 23)
    no_ions = (no_atoms * volume_l)
    
    if ion_types[0] == 'Mg':
        line = f'addIonsRand system {ion_types[0]} {round(no_ions)} {ion_types[1]} {2*round(no_ions)}'
    else:
        line = f'addIonsRand system {ion_types[0]} {round(no_ions)} {ion_types[1]} {round(no_ions)}'


with open(os.path.join(args.config_dir, 'tleap.in'), 'w') as f:

    f.write('source leaprc.protein.ff14SB\nsource leaprc.water.tip3p\n')

    if config_dict['contains dna (boolean)'] in ['True', 'T', 'true', 't']:
        f.write('source leaprc.DNA.OL21\n')
    f.write(f"""system = loadpdb {args.pdb_path}
solvateBox system TIP3PBOX 14 iso""")
    
    if config_dict['neutralize system (boolean)'] in ['True', 't', 'T', 'true']:
        f.write('addIonsRand system Na 0\n')

    for line in no_ions_lines:
        f.write(f'{line}\n')

    # change this to take directories from the contig file
    f.write(
        f"""savePDB system {os.path.join(args.start_dir, f"amber_{config_dict['run_name (string)']}")}
saveAmberParm system {os.path.join(args.start_dir, f"{config_dict['run_name (string)']}_solv.parm7")} \\
    {os.path.join(args.start_dir, f"{config_dict['run_name (string)']}_solv.rst7")}\n
quit"""
    )