'''
Created on 29 Aug 2016

Loads the configuration from one of the specified locations.

@author: conicova
'''
import logging
import json
import os.path
import os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

if os.name == 'nt':
    LOCATIONS = [r"\\Intranet.barcapint.com\dfs-emea\GROUP\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_logging_config.json",
                 r"Y:\Jhb\FAReports\AtlasEndOfDay\fadashboard\config\at_logging_config.json"]
else:
    LOCATIONS = [r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/fadashboard/config/at_logging_config.json"]

CONFIG_SOURCE_CODE = "code"
CONFIG_SOURCE_JSON = "json"
CONFIG_SOURCE = CONFIG_SOURCE_JSON

class FAMQConfigException(Exception):
    pass

class FAMQConfig(object):
    
    def __init__(self):
        self.connection_string = ""
        self.amqp = ""
        self.exchange = 'playground'
        self.routing_key = 'consumer.playground'
        self.queue_dashboard = 'fa_dashboard';
        self.queue_elasticsearch = 'fa_elasticsearch'
        self.delivery_mode = 1 
        ''' set delivery mode to 2 to make messages persistent.
            The queue has to be declared Durable.
        '''
        self.durable_exchange = False
        self.durable_queue = False
        self.host = "http://jhbdwmvdi000210:8080/"
        self.instance_name = "Playground"
        
    @staticmethod 
    def _get_config(instance_name="Playground"):
        config = FAMQConfig()
        config.instance_name = instance_name
        if instance_name == "Production":
            config.connection_string = "DRIVER={SQL Server};SERVER=JHBDSM050000052\ADPT_MAIN1_DEV;DATABASE=fa_log_prod;Integrated Security=True"
            config.amqp = "amqp://fa_user:fa_user@jhbdwmvdi000210:5672/%2F?connection_attempts=3&heartbeat_interval=3600"
            config.exchange = 'production'
            config.queue_dashboard = 'fa_dashboard_production';
            config.routing_key = 'consumer.production'
            config.durable_exchange = True
            config.host = "http://jhbdwmvdi000210:8000/"
            
        elif instance_name == "Playground":
            # SLGDSM020002022\MSSQL_12_IAAS
            config.connection_string = "DRIVER={SQL Server};SERVER=JHBDSM050000052\ADPT_MAIN1_DEV;DATABASE=fa_log;Integrated Security=True"
            config.amqp = "amqp://fa_user:fa_user@jhbdwmvdi000210:5672/%2F?connection_attempts=3&heartbeat_interval=3600"
            config.exchange = 'playground'
            config.routing_key = 'consumer.playground'
            
        elif instance_name == "SNAP":
            config.connection_string = "DRIVER={SQL Server};SERVER=JHBDSM050000052\ADPT_MAIN1_DEV;DATABASE=fa_log;Integrated Security=True"
            config.amqp = "amqp://fa_user:fa_user@jhbdwmvdi000210:5672/%2F?connection_attempts=3&heartbeat_interval=3600"
            config.exchange = 'snap'
            config.queue_dashboard = 'fa_dashboard_snap';
            config.routing_key = 'consumer.snap'
            config.durable_exchange = True
            config.host = "http://jhbdwmvdi000210:8080/"
            
        elif instance_name == "dev":
            config.connection_string = "DRIVER={SQL Server};SERVER=JHBDSM050000052\ADPT_MAIN1_DEV;DATABASE=fa_log_prod;Integrated Security=True"
            config.amqp = "amqp://fa_user_dev:fa_user_dev@jhbdsm020000411:5672/%2F?connection_attempts=3&heartbeat_interval=3600"
            config.exchange = 'dev'
            config.queue_dashboard = 'fa_dashboard_dev';
            config.routing_key = 'consumer.dev'
            config.durable_exchange = True
            config.durable_queue = True
            config.host = "http://jhbdsm020000411:3333/"
        else:
            raise FAMQConfigException("No FAMQConfig configuration defined for '{0}'".format(instance_name))
            
        return config
    
    @staticmethod 
    def _get_config_from_json(instance_name="Playground"):
        LOGGER.debug("Loading config file")
        result = {}
        for location in LOCATIONS:
            LOGGER.debug("Checking config file '%s'", location)
            if not os.path.isfile(location):
                LOGGER.debug("Config file '%s' does not exist.", location)
                continue
            with open(location) as json_data:
                result = json.load(json_data)
                json_data.close()
                LOGGER.debug("Config file '%s' loaded.", location)
                break
            
        config = FAMQConfig()
        config.instance_name = instance_name
        if result.has_key(config.instance_name):
            json_config = result[config.instance_name]
            for key in json_config.keys():
                if hasattr(config, key):
                    setattr(config, key, json_config[key])
                else:
                    LOGGER.warning("Attribute '%s' not found in config object, but is specified in the configuration file.")
        else:
            raise FAMQConfigException("No FAMQConfig configuration defined for '{0}'".format(instance_name))
        
        return config
    
    @staticmethod 
    def get_config(instance_name="Playground"):
        LOGGER.debug("Loading config data: %s, %s", CONFIG_SOURCE, instance_name)
        if CONFIG_SOURCE==CONFIG_SOURCE_CODE:
            return FAMQConfig._get_config(instance_name)
        else:
            return FAMQConfig._get_config_from_json(instance_name)
        
    @staticmethod 
    def get_fa_config():
        LOGGER.debug("Loading config data: %s", CONFIG_SOURCE)
        instance_name = "Playground"
        try:
            import acm
            if acm.FDhDatabase['ADM']:
                instance_name = acm.FDhDatabase['ADM'].InstanceName()
            else:
                LOGGER.warning("No ADM found. Using default configuration.")
        except ImportError:
            LOGGER.exception("Could not import acm. Using default configuration.")
        
        return FAMQConfig.get_config(instance_name)
    
    def __str__(self):
        return "FAMQConfig: {0}".format(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    
def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    environment = "Playground"
    
    config = FAMQConfig.get_config_from_json(environment)
    print(config)
    print(config.durable_queue)


if __name__ == '__main__':
    main()   