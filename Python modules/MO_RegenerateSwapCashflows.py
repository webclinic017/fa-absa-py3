'''----------------------------------------------------------------------
Department: Middle Office
Requester: Herman Levin
Developer: Paul Jacot-Guillarmod
CR Number: 890433 (Initial Deployment)
Purpose: Regenerates the cashflows on all swaps in the selected portfolio.  To be used to get around a bug that occurs
         after swaps are uploaded from an upload sheet and historical resets aren't fixed on floating receive legs.
----------------------------------------------------------------------'''

import acm

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['portfolio', 'Portfolio Name', 'FPhysicalPortfolio', None, None, 1, 0, 'All swaps in this portfolio will have their floating cashflows regenerated', None, 1]]

def ael_main(ael_dict):
    portfolio = ael_dict['portfolio']
    updatedInstruments = set([])

    for trade in portfolio.Trades():
        instrument = trade.Instrument()

        if instrument.InsType() == 'Swap' and instrument.Name() not in updatedInstruments:
            if instrument.PayLeg().LegType() == 'Float':
                leg = instrument.PayLeg()
            else:
                leg = instrument.RecLeg()

            leg.GenerateCashFlows(0)
            print('Regenerated float cashflows for instrument:', instrument.Name())

            updatedInstruments.add(instrument.Name())


