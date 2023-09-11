import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-pdb', '--pdb', 
                    help='pdb file to be changed')
parser.add_argument('-o', '--out', 
                    help='where to write fixed file to',
                    default='')

args = parser.parse_args()

# checking for out argument, setting it to overwrite the original file if
# nothing different is specified
if args.out == '':
    args.out = args.pdb

# read pdb
with open(args.pdb, 'r') as f:
    pdb = f.read()

# replace weirdly formatted AMBER ions
pdb = pdb.replace('MG', 'Mg')
pdb = pdb.replace('ZN', 'Zn')

# write out
with open(args.out, 'w') as w:
    w.write(pdb)