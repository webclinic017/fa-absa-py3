"""-----------------------------------------------------------------------------
PURPOSE                 :  Change trade status of internal trades specified by trade filer from FO Confirmed to BO-BO Confirmed
REQUESTER               :  Merlene Pillay (PTS - Capital Markets)
DEVELOPER               :  Bhavnisha Sarawan
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Jira no     Developer              Description
--------------------------------------------------------------------------------
2018-10-03  FAOPS-178   Bhavnisha Sarawan      Initial Implementation 
2018-10-12  ABITFA-5542   Bhavnisha Sarawan    Remove the fullstop from the print statement so the file can be copied from the backend                                       
"""

import csv
import acm
import at
from auto_confirm import AutoConfirmation
from at_ael_variables import AelVariableHandler


def enable_audit(selected_var):
    output_path = ael_variables.get('output_path')
    output_path.enabled = selected_var.value


ael_variables = AelVariableHandler()

ael_variables.add('trade_filter',
        label='Trade Filter',
        cls='FTradeSelection',
        collection=acm.FTradeSelection.Select(''),
        mandatory=True,
        alt='Trade filter for changing trade status to BO-BO Confirmed',
        enabled=True)
        
ael_variables.add_bool('audit',
    label='Perform audit',
    alt='Perform audit action to obtain remaining trades pending for BO-BO Confirmation',
    mandatory=False,
    hook=enable_audit
)
ael_variables.add('output_path',
    label='Output path',
    mandatory=False
)


class CM_InternalsAutoconfirm(AutoConfirmation):
    
    def __strict_rule_1(self, trade):
        #Check attributes which should match between trade and mirror trade
        mirror_trade = trade.GetMirrorTrade()
        if not mirror_trade:
            raise UserWarning("No mirror trade")
        if trade.Status() in ('FO Confirmed') and mirror_trade.Status() in ('FO Confirmed'):
            if trade.Premium() == (mirror_trade.Premium() * -1):
                return True
            else:
                raise UserWarning("Premium is not equal and opposite")
        else:
            raise UserWarning("Trade not in FO Confirmed status. Not applicable for processing")

    # move trades to BO-BO Confirmed state
    state = at.TS_BOBO_CONFIRMED
    
    fields = (
        ('Trade number', lambda t: str(t.Oid())),
        ('Instrument Name', lambda t: t.Instrument().Name()),
        ('Counterparty', lambda t: t.Counterparty().Name()),
        ('Acquirer', lambda t: t.Acquirer().Name()),
        ('Portfolio', lambda t: t.Portfolio().Name()),
        ('Premium', lambda t: t.Premium()),
        ('Status', lambda t: t.Status()),
        ('Trade time', lambda t: str(t.TradeTime())),
        ('Trader', lambda t: t.Trader().Name())
    )
    
    def generate_audit(self, output_path):
        """Generates CSV audit error file for business users."""
        
        with open(output_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            header = [entry[0] for entry in self.fields]
            header.append('Reason')
            csvwriter.writerow(header)
            for trade, bo_error in self.errors.items():
                values = self.get_values(trade)
                values.append(bo_error)
                csvwriter.writerow(values)
    
        print('Output written to %s' % output_path)
    
    @classmethod
    def get_values(cls, trade):
        values = []
        for name, field in cls.fields:
            try:
                value = field(trade)
            except (AttributeError, ValueError) as exc:
                print("Failed to get '%s' for trade %s: %s" % (
                    name, trade.Oid(), str(exc)))
                value = ''
            values.append(value)
        return values
                  
                  
def ael_main(params):
    filter_trades = params["trade_filter"].Trades()
    candidates = list(filter_trades.SortByProperty('Oid', False))
    
    cm_internals_engine = CM_InternalsAutoconfirm(candidates)
    cm_internals_engine.confirm()
    
    if params['audit']:
        cm_internals_engine.generate_audit(params['output_path'])
    
    # print the errors
    cm_internals_engine.print_errors()
    
    print("Completed successfully")

