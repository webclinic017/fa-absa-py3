#************************************************************************************************************************
# Script Name             :PB_SetAddInfoDate
# Description             :Set the add info date flag on prime broker trades to include in the fund administrator extracts
# Developer               :Sarawab Bhavnisha, Momberg Heinrich
# CR Number(s)            :ABITFA-605(IDS)
# Change History          : 
#                         C710394 - 12 July 2011 - Hein Momberg
#                         Add reference to PS_Functions to re-use method
#                         SetAdditionalInfo to handle the update. Also
#                         removed transaction
#                         C761889 - 08/09/2011 - Bhavnisha
#                         Added None value check to void statement check
#                         C145434 - 2012-04-18 - Paul Jacot-Guillarmod
#                         Included trades in terminated status as criteria to have addinfo set
#                         CHNG2018619 - 2014-06-05 - Hynek Urban
#                         Handling errors in PB overnight batch correctly
#                         CHNG2450799 - 2014-11-20 Hynek Urban
#                         Fixing errors and exception handling
#************************************************************************************************************************
import acm, ael

import at_addInfo
import at_time
from at_ael_variables import AelVariableHandler
from at_logging import  getLogger, bp_start

LOGGER = getLogger(__name__)

#***********************************************************************************************
# Global constants
#***********************************************************************************************
PB_ADD_INFO_FLAG = 'PS_MsgSentDate'

FO_CONFIRMED_STATUS = 'FO Confirmed'
BO_CONFIRMED_STATUS = 'BO Confirmed'
BO_BO_CONFIRMED_STATUS = 'BO-BO Confirmed'
VOID_STATUS = 'Void'
TERMINATED_STATUS = 'Terminated'

ADD_INFO_DEFAULT = acm.Time.AsDate('1700-01-01')
TODAY = acm.Time.DateToday()

#***********************************************************************************************
# Main entry point and Variables
#***********************************************************************************************
ael_variables = AelVariableHandler()
ael_variables.add("tradeFilters",
                  label="Trade Filters",
                  cls = "FTradeSelection",
                  collection = acm.FTradeSelection.Select(''),
                  default = 'PS_SetAddInfoDate_IDS, PS_SetAddInfoDate_Maitland',
                  mandatory =True,
                  multiple=True)
ael_variables.add("clientName",
                  label="Short name",
                  cls = "string",
                  default='CLIENT',
                  mandatory =False,
                  multiple=False)

UPDATE_STATUSES = [BO_CONFIRMED_STATUS, BO_BO_CONFIRMED_STATUS, FO_CONFIRMED_STATUS, TERMINATED_STATUS]                
UPDATE_ADD_INFO_VALUES = [ADD_INFO_DEFAULT, None, '']

def ael_main(parameters):
    process_name = "ps.set_add_info.{0}".format(parameters["clientName"])
    with bp_start(process_name, ael_main_args=parameters):
            
        # Test if the Additional Info spec exists on table trade 
        addInfoSpec = acm.FAdditionalInfoSpec[PB_ADD_INFO_FLAG]
        if(not addInfoSpec):
            raise Exception("Additional Info Spec '%s' not defined" % (PB_ADD_INFO_FLAG)) 
        elif  (addInfoSpec.RecType() != 'Trade'):
            raise Exception("Additional Info Spec '%s' not defined for record type 'Trade'" % (PB_ADD_INFO_FLAG)) 
    
        # Get the trade filters from parameters
        tradeFilters = parameters['tradeFilters']
    
        # Find all the new trades in each trade filter and add them to the list for update
        tradesForUpdate = []
        trade_count = 0
        for tf in tradeFilters:
            for t in tf.Trades():
                trade_count += 1
                addInfoValue = at_addInfo.get_value(t, PB_ADD_INFO_FLAG)
                updateTime = at_time.to_date(t.UpdateTime())
                LOGGER.info("Scanning trade (no=%s, status=%s, rawUpdateTime=%s, acmUpdateTime=%s, %s=%s )",
                             t.Oid(), t.Status(), t.UpdateTime(), updateTime, PB_ADD_INFO_FLAG, addInfoValue)
                
                # Aggregate trades and Void trades are skipped
                if t.Aggregate() in (1, 2) or t.Status() == VOID_STATUS:
                    continue
                
                # NEW - BO or BO-BO Confirmed Status and add info flag default or empty 
                if t.Status() in UPDATE_STATUSES and addInfoValue in UPDATE_ADD_INFO_VALUES:
                    tradesForUpdate.append(t)
                       
        # Print the trades flagged for update
        if(len(tradesForUpdate) == 0):
            LOGGER.info("No trades were identified for update!")
        else:
            LOGGER.info("Trades identified for update:")
            for t in tradesForUpdate:
                addInfoValue = at_addInfo.get_value(t, PB_ADD_INFO_FLAG)
                updateTime = at_time.to_date(t.UpdateTime())
                LOGGER.info("Trade %s (status=%s, updateTime=%s, %s=%s)",
                            t.Oid(), t.Status(), updateTime, PB_ADD_INFO_FLAG, addInfoValue)
        LOGGER.info("Total number of trades %s.\nNumber of trades to update %s.\nStarting update....",
                    trade_count, len(tradesForUpdate))
        
        # Now update the add-info date flag
        for t in tradesForUpdate:
            LOGGER.info('Trying to update trade %s.....setting %s=%s', t.Oid(), PB_ADD_INFO_FLAG, TODAY)
            at_addInfo.save(t, PB_ADD_INFO_FLAG, TODAY)
        
        LOGGER.info('Update done')
        
        # Report completed
        LOGGER.info('Completed Successfully')