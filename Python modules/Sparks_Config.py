from XMLProcessor import XMLProcessor
import acm

MQ_BASE_NODES = {'Send': 'MQ_NOSTRO_SEND', 
                 'Receive': 'MQ_NOSTRO_RECEIVE'}

class SparksConfig:

    def __init__(self, mode=None):
        config, node = self.get_env_settings()
        self.get_sparks_setting(config, node)
        if mode: 
            self.get_MQ_setting(config, node, MQ_BASE_NODES[mode])
        
        
    def get_env_settings(self):
        arena_data_server = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()   
        
        environment_settings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
        env_config = XMLProcessor(environment_settings)

        host_node = env_config.getNodeByAttributeValue('Environment/Host', 'Name', arena_data_server)
        env_setting = env_config.getAttributeValueFromElement(host_node, 'Setting')
        
        sparks_settings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'SparksConfigSettings')
        sparks_config = XMLProcessor(sparks_settings)
        
        env_node = sparks_config.getNodeByAttributeValue('Environment', 'ArenaDataServer', env_setting)
        
        return sparks_config, env_node
        

    def get_sparks_setting(self, config, node):
        

        self.next_day_currencies        = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/next_day_currencies')
        self.trades_cache_location      = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/data_files_location')
        self.trades_cache_file_name     = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/cache_file_name')
        self.port_segment_len           = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/percent_portfolio_list_segment_length')
        self.active_portfolios_query    = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/active_portfolios_query')
        self.active_trades_query        = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/active_trades_query')
        self.amb_server_ip              = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/amb_server_ip')
        self.mb_name                    = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/mb_name')
        self.subject_string             = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/subject_string').split(',')
        self.cut_off_time               = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/cut_off_time')
        self.intraday_reporting_active  = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/activate_intraday_reporting')
        self.status_to_report           = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/status_to_report').split(',')
        self.email_group                = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/email_group').split(';')
        self.email_group2               = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/email_group2').split(';') #Intraday
        self.environment                = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/environment_name')
        self.web_api_end_point          = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/web_api_end_point') #Message sent via an end point
        self.mongo_db_repl_set_conn_str = config.getNodeValueFromElement(node, 'RUNTIME_PARAMETERS/mongo_db_repl_set_conn_str') #Mongo db replica set connection string
        
        
    def get_MQ_setting(self, config, node, mode): 
        self.queue_name              = config.getNodeValueFromElement(node, mode + '/QueueName')
        self.queue_manager           = config.getNodeValueFromElement(node, mode + '/QueueManager')
        self.channel                 = config.getNodeValueFromElement(node, mode + '/Channel')
        self.host                    = config.getNodeValueFromElement(node, mode + '/Host')
        self.port                    = config.getNodeValueFromElement(node, mode + '/Port')
        self.client                  = "%s(%s)" % (self.host, self.port)
        self.log_path                = config.getNodeValueFromElement(node, mode + '/LogPath')
        self.log_level               = int(config.getNodeValueFromElement(node, mode + '/LogLevel'))


    def __str__ (self):
        config_str = 'Env Setting:         ' + self.env_setting + '\n' + \
                     'Next day curr:       ' + self.next_day_currencies + '\n' + \
                     'Active port query:   ' + self.active_portfolios_query + '\n' + \
                     'Active trade query:  ' + self.active_trades_query
        
        return config_str
