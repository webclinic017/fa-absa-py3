"""
AEL Hook that provides entry point to split specific settlements.

Fixed Amount settlements created for zero day deposits that are ceded are required to be split and the ceded amount
should be placed on hold.
---------------------------------------------------------------------------------------------------------
HISTORY
---------------------------------------------------------------------------------------------------------
2020-05-19      FAOPS-798       Tawanda Mukhalela       Removed call accounts from splitting logic
"""

import acm
       
    
def SplitSettlement(settlement):
    """
    DESCRIPTION: This function returns a list of Python tuples. The tuple values
                 are used for automatic split of settlement records.
    INPUT:       An FSettlement. Treat input as read-only.
    OUTPUT:      A list containing the split configurations. See FCA 2105, section
                 FSettlementHooksTemplate, for data preparation and hook implementation.
    """

    split_settlements = list()
    instrument = settlement.Trade().Instrument()
    if settlement.Type() == 'Fixed Amount':
        if settlement.Trade().Instrument().InsType() == 'Deposit' and not instrument.IsCallAccount():
            if settlement.Trade().AdditionalInfo().MM_Account_Ceded() is True:
                acm.Log('CALCULATE CEDED AMOUNT')
                ceded_amount = settlement.Trade().AdditionalInfo().MM_Ceded_Amount()*-1
                new_amount = settlement.Amount() - ceded_amount

                if round(settlement.Amount(), 2) > ceded_amount:
                    acm.Log('CREATE SPLIT SETTLEMENTS')
                    acm.Log('CEDED Amount: %s' % ceded_amount)
                    acm.Log('NEW Amount: %s' % new_amount)
                    
                    split_settlements.append((ceded_amount, 'CededAmount'))
                    split_settlements.append((new_amount, ''))

    return split_settlements
