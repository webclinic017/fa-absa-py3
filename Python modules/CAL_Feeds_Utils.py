def get_ats_config(config_module, ads_ip_address):
    
    configs = __import__(config_module)
    
    for config_name in configs.__all__:
        config_dict = getattr(configs, config_name)
        if config_dict and config_dict["ads_server_ip"] == ads_ip_address:
            return config_dict
    
    raise Exception("No valid config found.")

def get_environment_classifier(config_module, ads_ip_address):
    
    configs = __import__(config_module)
    
    for environment_name in configs.__all__:
        config_dict = getattr(configs, environment_name)
        if config_dict and config_dict["ads_server_ip"] == ads_ip_address:
            return environment_name.split('_')[-2]

def get_path_rec(portfolio):
    if not portfolio:
        return []
    path_to_root = [portfolio.Name()]
    link = acm.FPortfolioLink.Select('memberPortfolio=%d' % portfolio.Oid())
    if len(link) == 0:
        return path_to_root
    elif link.At(0).OwnerPortfolio():
        path_to_root = path_to_root + get_path_rec_ael(link.At(0).OwnerPortfolio())
        
    return path_to_root