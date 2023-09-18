gmx grompp -c {start_dir}/temp_{run_name}.gro \
    -r {start_dir}/temp_{run_name}.gro \
    -f {start_dir}/ions.mdp \
    -p {start_dir}/sys.top \
    -o {start_dir}/temp_ions.tpr -maxwarn 5

echo "SOL" | gmx genion -s {start_dir}/temp_ions.tpr \
    -p {start_dir}/sys.top \
    -o {start_dir}/temp_{run_name}.gro \
    -pname {p_ion} -pq {p_charge} -nname {n_ion} -nq {n_charge} -conc {conc} 
