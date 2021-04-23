"""-----------------------------------------------------------------------------
MODULE
    Credit_Set_CCDS_Nominal

DESCRIPTION
    Date                : 2012-02-17
    Purpose             : Sets the nominal on Contingent CDSs to the sum of the MTM of underlying trades.
    Department and Desk : Credit
    Requester           : De Clercq Wentzel
    Developer           : Herman Hoon
    CR Number           : 48746
ENDDESCRIPTION

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2012-02-17 48746        Herman Hoon        Initial implementation
-----------------------------------------------------------------------------"""
import acm

def setNominal(trade):
    '''Calculate the sum of the PVs of the underlying Swap trades and set the nominal to this value
    '''
    sumOfPV = 0
    trxTrades = trade.TrxTrades()
    
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()                                                                                                                                                                                                                                                                                                                                                     
    currency = trade.Currency().Name()
    
    for trxTrade in trxTrades:
        if trxTrade.Oid() > 0:
            pv = 0
            try:
                pv = trxTrade.Calculation().PresentValue(calculationSpace, currency).Number()
            except e:
                print('ERROR: Failed to calculate PV on trade: %s' %(trxTrade.Oid()))
                pv = 0
            sumOfPV += pv 
    
    #only want have positive exposure to PV
    if sumOfPV < 0:
        sumOfPV = 0
    
    trade.Nominal(sumOfPV)
    try:
        trade.Commit()
        print('INFO: Updated the nominal of trade: %s on Instrument: %s to %s from the PV of underlying trades: %s ' %(trade.Oid(), trade.Instrument().Name(), sumOfPV, trxTrades))
    except ex:
        print('ERROR: Failed to commit trade: %s' %(trade.Oid()))

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [['instruments', 'Contingent Credit Default Swaps', 'FInstrument', None, None, 1, 1, 'Contingent Default Swaps for which the nominal will be updated,\n based on the sum of the PVs of transaction linked underlying trades.', None, 1]]
                
def ael_main(parameters):
    instruments = parameters['instruments'] 
    
    for instrument in instruments:
        trades = instrument.Trades()
        if trades:
            for trade in trades:
                setNominal(trade)
        else:
            print('No trades specified for %s' %(instrument))
    print('Completed successfully')
