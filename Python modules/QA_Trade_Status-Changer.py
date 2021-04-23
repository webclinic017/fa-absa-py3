import acm
import ael
import FRunScriptGUI
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from FX_TPL_Delta_Cash_Calculation import WriteCSVFile


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
ael_variables.add('input_name',
                  label='input name',
                  mandatory=True,
                  default='QA_REG_1',
                  tab="Task Inputs")

ael_variables.add('status',
                  label='Status for trades',
                  default='FO Confirmed',
                  collection=['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'],
                  mandatory=True,
                  tab="Task Inputs")
                  
                  
        
def ael_main(ael_dict):
    trd_status = ael_dict['status']
    input = ael_dict['input_name']
    try:
        if acm.FTradeSelection[input] <> None:
            trades = acm.FTradeSelection[input].Trades()
        elif acm.FStoredASQLQuery[input] <> None:
            trades = acm.FStoredASQLQuery[input].Query().Select()
        if len(trades) >= 1:
            for trade in trades:
                if trade.Status() == 'Simulated':
                    trade.Status(trd_status)
                    trade.Commit()
                    LOGGER.info('Trade status for trade {} changed to {}'.format(trade.Oid(), trade.Status()))
            LOGGER.info('Task completed successfully.....')
    except Exception as e:
        LOGGER.error('Task failed due to the following error: {}'.format(e))

            

