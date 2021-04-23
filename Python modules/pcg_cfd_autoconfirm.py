"""-----------------------------------------------------------------------------
PURPOSE                 :  Automated BO confirmation script for CFD 
                           instruments booked in Prime Services books.
REQUESTER               :  Lwandlekazi Mtholo
DEVELOPER               :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no     Developer              Description
--------------------------------------------------------------------------------
20/09/2016  3963415       Libor Svoboda          Initial Implementation
2018-10-12  ABITFA-5542   Bhavnisha Sarawan      Remove the fullstop from the print statement so the file can be copied from the backend                                         
"""
import csv
import acm
import at
from auto_confirm import AutoConfirmation
from at_ael_variables import AelVariableHandler


cs = acm.FCalculationSpace('FTradeSheet')


def enable_audit(selected_var):
    output_path = ael_variables.get('output_path')
    output_path.enabled = selected_var.value


ael_variables = AelVariableHandler()
ael_variables.add('trades',
    label='Trades',
    alt='Trades that will be used for automatic BO-Confirmation',
    cls='FTrade',
    multiple=True
)
ael_variables.add_bool('audit',
    label='Perform audit',
    alt='Perform audit action to obtain remaining trades pending for BO-Confirmation',
    mandatory=False,
    hook=enable_audit
)
ael_variables.add('output_path',
    label='Output path',
    mandatory=False
)


class CFDAutoconfirm(AutoConfirmation):

    # move trades to BO-Confirmed state
    state = at.TS_BO_CONFIRMED
    
    fields = (
        ('Trade number', lambda t: str(t.Oid())),
        ('Counterparty', lambda t: t.Counterparty().Name()),
        ('Instrument Name', lambda t: t.Instrument().Name()),
        ('Underlying', lambda t: t.Instrument().Underlying().Name()),
        ('Quantity', lambda t: str(t.Quantity())),
        ('Price', lambda t: str(t.Price())),
        ('Total Val End', lambda t: str(float(cs.CalculateValue(t, 'Total Val End')))),
        ('Portfolio', lambda t: t.Portfolio().Name()),
        ('Trade time', lambda t: str(t.TradeTime())),
        ('Acquire Day', lambda t: str(t.AcquireDay())),
        ('Acquirer', lambda t: t.Acquirer().Name()),
        ('Trader', lambda t: t.Trader().Name()),
    )
    
    def generate_audit(self, output_path):
        """Generates CSV audit error file for business users."""
        
        with open(output_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow([entry[0] for entry in self.fields])
            for trade, bo_error in self.errors.items():
                values = self.get_values(trade)
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
    trades = params['trades']
    candidates = list(trades.SortByProperty('Oid', False))
    
    cfd_engine = CFDAutoconfirm(candidates)
    cfd_engine.confirm()
    
    if params['audit']:
        cfd_engine.generate_audit(params['output_path'])
    
    # print the errors
    cfd_engine.print_errors()
    
    print("Completed successfully")

