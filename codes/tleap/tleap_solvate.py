import argparse

# arguemnt parser for intaking the pdb in order to solvate
parser = argparse.ArgumentParser(
    prog='tleap solvate',
    description='writes a tleap.in file to solvate a given pdb'
    )

parser.add_argument('-p', '--pdb')
parser.add_argument('-c', '--config_dir')

args = parser.parse_args()


# the text that will be used to get the volume of the box
text = f"""source leaprc.protein.ff14SB

source leaprc.water.tip3p

system = loadpdb {args.pdb}

solvateBox system TIP3PBOX 14 iso
"""

# write initial tleap input file
with open(f'{args.config_dir}/solvate_tleap.in', 'w') as f:
    f.write(text)
