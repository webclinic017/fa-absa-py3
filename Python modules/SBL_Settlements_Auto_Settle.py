"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SBL_Settlements_Auto_Settle
    
DESCRIPTION
    Date                    : 2020-06-03
    Purpose                 : Auto settle SBL settlments until fully of Global One
    Department and Desk     : Product Control Team
    Requester               : Gasant Thulsie
    Developer               : Jaysen Naicker
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2020-06-03                         Jaysen Naicker         Initial Implementation.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from time import time

LOGGER = getLogger()
TODAY = acm.Time().DateToday()
ael_variables = AelVariableHandler()

ael_variables.add(
        'date',
        label='Date',
        cls='string',
        default='Today')


# Select all valid SBL settlements
def get_settlements(date):
    settl_query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    settl_query.AddAttrNode('Trade.Acquirer.Name', 'EQUAL', 'SECURITY LENDINGS DESK')
    settl_query.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    settl_query.AddAttrNode('CreateTime', 'LESS_EQUAL', date)
    settl_query.AddAttrNode('Currency.Name', 'EQUAL', 'ZAR')
    
    valid_status_node = settl_query.AddOpNode('OR')
    for valid_status in ['Authorised', 'Exception', 'Hold']:
        valid_status_node.AddAttrNode('Status', 'EQUAL', valid_status)
        
    instrument_node = settl_query.AddOpNode('OR')
    instrument_node.AddAttrNode('Trade.TradeCategory', 'EQUAL', 'Collateral')
    sl_node = instrument_node.AddOpNode('AND')
    sl_node.AddAttrNode('Trade.Instrument.InsType', 'EQUAL', 'SecurityLoan')
    openend_node = sl_node.AddOpNode('OR')
    openend_node.AddAttrNode('Trade.Instrument.OpenEnd', 'EQUAL', 'Open End')
    openend_node.AddAttrNode('Trade.Instrument.OpenEnd', 'EQUAL', 'Terminated')
    
    type_node = settl_query.AddOpNode('OR')
    type_node.AddAttrNode('Type', 'EQUAL', 'Security Nominal')
    type_node.AddAttrNode('Type', 'EQUAL', 'End Security')

    return settl_query.Select()


# Move all valid SBL settlments to Settled status
def settle_SBL_trades(date):
    start = time()
    settlements = get_settlements(date)
    LOGGER.info('Processing {} settlements'.format(len(settlements)))

    for settlement in settlements:
        if settlement.Status() == 'Hold':
            try:
                settlement_clone = settlement.Clone()
                settlement_clone.Status('Authorised')
                settlement.Apply(settlement_clone)
                settlement.Commit()
                LOGGER.info('Settlement {} status changed successfully to Authorised'.format(settlement.Oid()))
            except:
                LOGGER.exception('Could not set status to Authorised {}'.format(settlement.Oid()))
            
        try:
            settlement_clone = settlement.Clone()
            settlement_clone.Status('Settled')
            settlement.Apply(settlement_clone)
            settlement.Commit()
            LOGGER.info('Settlement {} status changed successfully to Settled'.format(settlement.Oid()))
        except:
            LOGGER.exception('Could not set status to Settled {}'.format(settlement.Oid()))
            
    end = time()
    LOGGER.info('Time taken: {}'.format(end - start))



def ael_main(config):
    LOGGER.msg_tracker.reset()
    date = config['date']
    if date == 'Today': 
        date = TODAY
    settle_SBL_trades(date)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully')
