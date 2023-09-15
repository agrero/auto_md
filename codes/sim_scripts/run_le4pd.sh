module load racs-eb/1 
module load MDTraj/1.9.1-intel-2017b-Python-3.6.3

vim +"set nobomb | set fenc=utf-8 | x" {le4pd_inputs}/{run_name}_first.pdb

python3 {run_le4pd} \
    -tr {le4pd_inputs}/{run_name}.g96 \
    -to {le4pd_inputs}/{run_name}_first.pdb \
    -ar {le4pd_inputs}/ \
    -o {analysis_dir}