

class AutoMd:
    """The main class engine behind the AUTO_MD program
    
    Handles the generation of md scripts/headers, tleap codes,
    and file handling
    
    ADD MORE HERE"""
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        # initialize necessary variables as None, read-in from method

        # header info
        self.account = None
        self.email = None
        self.header_path = None

        # pdbs 
        self.pdb_dir = None
        self.pdb = None
        self.run_name = None

        # configs 
        ## the second part of this should be reconfigured to series of 
        ## nested dictionaries
        self.config_storage = None 
        
        self.start_dir = None
        self.config_dir = None 
        self.out_dirs = None
        self.em_dir = None
        self.heating_dir = None
        self.npt_dir = None
        self.prod_dir = None

        # scripts
        ## i think i should just merge these first two

        self.tleap_dir = None
        self.pycode_dir = None
        self.sim_script_dir = None

    def read_config(self):
        """Protocol for reading in the configuration file for auto_md
        returns a dictionary of all the input parameters.

        config_path: filepath of the configuration file
        """
        from ..utility.md_funcs import read_sysconfig

        config_dict = read_sysconfig(self.config_file)
        print(self.__dict__)

        # matching attributes and config inputs
        att_key_match = [i for i in config_dict if i in self.__dict__]
        for i in att_key_match: # this should match everything listed above
            self.__dict__[i] = config_dict[i]
        
        
        return config_dict

# I think we should iterate through the objects components and pass the corresponding 
# pieces of the object to here
