
def read_sysconfig(config_path):
    """Protocol for reading in the configuration file for auto_md
    returns a dictionary of all the input parameters.

    config_path: filepath of the configuration file
    """
    config_dict = {}
    try:
        # open file
        with open(config_path, 'r') as f:
            text = [i for i in f.read().split('\n') if '>' in i]

            # parse each line delineated by '>' and create 
            # matching key value pairs
            for i in text:
                
                var = i.strip('>')
                
                # if there are multiple accepted values 
                ## in the future might want to have some sort of error handling 
                ## if the incorrect amount of things are added
                if len(var.split(':')) > 2:
                    config_dict[var.split(':')[0]] = [j.strip(' ') for j in var.split(':')[1:]]
                # if there is only a single value
                else:
                    config_dict[var.split(':')[0]] = var.split(':')[1].strip(' ')

    except:
        raise FileNotFoundError('File could not be found')
    
    ## a potential way to make this faster would be to somehow filter out unwanted items
    ## might be easier to split up the config file
    ## however if it's in a memory loaded object it should just open just as fast
    return config_dict