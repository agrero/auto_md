from package.classes.AutoMd import AutoMd



auto = AutoMd('ignore_config.in')
auto_dict = auto.read_config()
print(auto.__dict__)
