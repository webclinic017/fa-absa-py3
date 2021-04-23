'''
-------------------------------------------------------------------------------------------------------------
HISTORY
=============================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Rohan vd Walt
2016-08-23      CHNG0003898744  Willie van der Bank     Added PG and updated Prod config
2017-01-26      CHNG0004260701  Willie van der Bank     Added TRADEquery
2017-12-11      CHNG0005220511  Manan Ghosh             DIS go-live
2019-07-04      Upgrade2018     Jaysen Naicker          Update file location to point to Linux folders.
2020-03-18      FAOPS-777       Cuen Edwards            Update of email addresses. Small formatting fixes.
-------------------------------------------------------------------------------------------------------------
'''

import acm

INSquery = 'Demat Valid Instruments'
CFquery = 'Demat Valid CFs'
TRADEquery = 'Demat Valid Trades'
DISINSquery = 'DIS Valid Instruments'
DISTRADEquery = 'DIS Valid Trades'

demat_config_dict = {
    'playground': {
        'swift_msg_to_process_dir': '/apps/services/frontnt/Task/SWIFT_CUST/ToProcess',
        'swift_msg_processed_dir': '/apps/services/frontnt/Task/SWIFT_CUST/Processed',
        'swift_msg_error_dir': '/apps/services/frontnt/Task/SWIFT_CUST/Error',
        'swift_msg_to_process_manually_dir': '/apps/services/frontnt/Task/SWIFT_CUST/ToProcessManual',
        'mq_connection_notifications': ['CIBAfricaTSDevPTSCl@absa.africa'],
        'agent_participant_code': 'ZA600200',
        'routing_code': 'MS10',
        'dis_routing_code': 'MS30',
        'strate_env': 'C',
        'dis_strate_env': 'C',
        'message_version': '002'
    },
    'production': {
        'swift_msg_to_process_dir': '/apps/services/frontnt/Task/SWIFT_CUST/ToProcess',
        'swift_msg_processed_dir': '/apps/services/frontnt/Task/SWIFT_CUST/Processed',
        'swift_msg_error_dir': '/apps/services/frontnt/Task/SWIFT_CUST/Error',
        'swift_msg_to_process_manually_dir': '/apps/services/frontnt/Task/SWIFT_CUST/ToProcessManual',
        'mq_connection_notifications': ['ABCapITRTBAMFrontAre@absa.africa'],
        'agent_participant_code': 'ZA600200',
        'routing_code': 'MS10',
        'dis_routing_code': 'MS30',
        'strate_env': 'P',
        'dis_strate_env': 'P',
        'message_version': '002'
    }
}


def get_config():
    env = acm.FInstallationData.Select('').At(0).Name().lower()
    if env in demat_config_dict.keys():
        return demat_config_dict[env]
    else:
        print('Could not find config for ' + env + ', using default values.')
        return demat_config_dict['playground']
