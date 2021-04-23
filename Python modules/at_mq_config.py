'''
Created on 29 Aug 2016

Loads the configuration from one of the specified locations.

@author: conicova
'''
import logging
import json
import os.path
import os

from async_publisher import MQConfig
from at_logging import getLogger

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = getLogger(__name__)

if os.name == 'nt':
    LOGGING_LOCATIONS = [r"\\Intranet.barcapint.com\dfs-emea\GROUP\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_logging_config.json",
                 r"Y:\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_logging_config.json"]
else:
    LOGGING_LOCATIONS = [r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/fadashboard/config/at_logging_config.json"]

if os.name == 'nt':
    HISTORY_LOCATIONS = [r"\\Intranet.barcapint.com\dfs-emea\GROUP\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_history_config.json",
                 r"Y:\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_history_config.json"]
else:
    HISTORY_LOCATIONS = [r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/fadashboard/config/at_history_config.json"]
    
if os.name == 'nt':
    REPORTS_LOCATIONS = [r"\\Intranet.barcapint.com\dfs-emea\GROUP\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_reports_config.json",
                 r"Y:\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_reports_config.json"]
else:
    REPORTS_LOCATIONS = [r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/fadashboard/config/at_reports_config.json"]


class FAMQConfigException(Exception):
    pass

class FAMQConfig(MQConfig):
    
    def __init__(self):
        super(FAMQConfig, self).__init__()
    
    def _load_config_from_json(self, instance_name, json_locations):
        LOGGER.debug("Loading config file")
        result = {}
        used_location = ""
        for location in json_locations:
            LOGGER.debug("Checking config file '%s'", location)
            if not os.path.isfile(location):
                LOGGER.debug("Config file '%s' does not exist.", location)
                continue
            with open(location) as json_data:
                result = json.load(json_data)
                json_data.close()
                LOGGER.debug("Config file '%s' loaded.", location)
                used_location = location
                break
            
        self.instance_name = instance_name
        if result.has_key(self.instance_name):
            json_config = result[self.instance_name]
            for key in json_config.keys():
                if hasattr(self, key):
                    setattr(self, key, json_config[key])
                    LOGGER.debug("%s -> %s", key, json_config[key])
                else:
                    LOGGER.warning("Attribute '%s' not found in conf object, but is specified in the conf file: '%s.", 
                                   key,
                                   used_location)
            # TODO perhaps check if all the attributes have been loaded
        else:
            raise FAMQConfigException("No MQConfig configuration defined for '{0}'".format(instance_name))
    
    def load_config(self, instance_name="Playground", json_locations=LOGGING_LOCATIONS):
        """Loads the configuration file, from the list of specified locations.
        Call this if the configuration key does not correspond to the environment name"""
        LOGGER.debug("Loading config data: %s", instance_name)
        self._load_config_from_json(instance_name, json_locations)
        
    def load_fa_config(self, json_locations=LOGGING_LOCATIONS):
        """Loads the configuration file, from the list of specified locations.
        Will use the environment name as the configuration key"""
        LOGGER.debug("Loading config data")
        instance_name = "Playground"
        try:
            import acm
            if acm.FDhDatabase['ADM']:
                instance_name = acm.FDhDatabase['ADM'].InstanceName()
            else:
                LOGGER.warning("No ADM found. Using default configuration.")
        except ImportError:
            LOGGER.exception("Could not import acm. Using default environment.")
        
        self.load_config(instance_name, json_locations)
    
    def __str__(self):
        return "MQConfig: {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    
def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    environment = "Playground"
    
    config = MQConfig.load_config(environment)
    print(config)

if __name__ == '__main__':
    main()   
