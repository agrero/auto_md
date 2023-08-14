import argparse
import os 

parser = argparse.ArgumentParser(
    prog='tleap solvate read',
    description='reads tleap out files for the box volume'
)

parser.add_argument('-i', '--tleap_out')
parser.add_argument('-c', '--conc', type=int)
parser.add_argument('-dna', action='store_true')
parser.add_argument('-p', '--pdb')
parser.add_argument('-o', '--start_dir', default='start')
parser.add_argument('-con', '--config_dir', default='config')

args = parser.parse_args()
no_dot_pdb = args.pdb.split('.')[0] # because things are dumb sometimes

testing_path = '/home/aguerre2/guenzagrp/gp32-59/gp32_gp59_complex/out/solvate_tleap.out' # this will need to be changed

with open(args.tleap_out, 'r') as f:
    volume_text = [i for i in f.read().split('\n') if 'Volume' in i]
    vol_comp = volume_text[0].split(' ')
    volume = float(vol_comp[3])

volume_L = volume / (((10**10)**3)) * ((10**2)**3) / (10**3)
no_atoms = args.conc / (10**3) * (6.022*10**23)
no_ions = volume_L * no_atoms
with open(os.path.join(args.config_dir,'tleap.in'), 'w') as f:
    f.write('source leaprc.protein.ff14SB\nsource leaprc.water.tip3p')
    if args.dna:
        f.write('\nsource leaprc.DNA.OL21')
    f.write(f'\nsystem = loadpdb {os.path.join(args.start_dir,args.pdb)}')
    text = f"""\nsolvateBox system TIP3PBOX 14 iso
addIonsRand system Na+ 0
addIonsRand system Na+ {round(no_ions)} Cl- {round(no_ions)}
addIonsrand system MG {round(6/args.conc * no_ions)} Cl- {round(12/args.conc * no_ions)}
savePDB system {os.path.join(args.start_dir,f'amber_{args.pdb}')}
saveAmberParm system {os.path.join(args.start_dir, f'{no_dot_pdb}_solv.parm7')} {os.path.join(args.start_dir, f'{no_dot_pdb}_solv.rst7')}
quit
"""
    f.write(text)

