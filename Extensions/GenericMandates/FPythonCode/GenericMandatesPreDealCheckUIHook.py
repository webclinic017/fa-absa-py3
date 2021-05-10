"""
Python module to set up the Pre-deal Check UI hook.
#
#
"""

import acm
from GenericMandatesLogger import getLogger
from GenericMandatesPredealCheckDialog import MandateCheckDialogBase
from GenericMandatesUtils import GetMandateSettingsParam, GetLimits, GetOptionalKey


def ael_custom_dialog_show(shell, params):
    """
    This is the entry point for the pre-deal check hook.
    :param shell: FUxShell
    :param params: FDictionary
    :return: FDictionary
    """
    
    originalTrader = None
    
    # Check if the pre-deal check is enabled in the FParameter settings
    preDealChecksEnabled = GetMandateSettingsParam("PreDealChecksEnabled")
    if preDealChecksEnabled == "False":
        getLogger().debug('[Mandates] Pre-deal check disabled.')
        return params
    getLogger().debug('[Mandates] Pre-deal check enabled.')

    data = params.At('initialData')
    modifiedObject = data.At('editObject')
    originalObject = data.At('originalObject')

    tradeObject = modifiedObject if modifiedObject else originalObject

    # Only do pre-deal check when a trade is saved to FO Confirmed
    trade_status = tradeObject.Status()
    if trade_status not in ['FO Confirmed']:
        getLogger().info('Skip Limit Pre-deal check. Trade status is not FO confirmed')
        return params
    # End of FO Confirmation check
    
    if tradeObject.Trader():
        # Update trader on trade ticket to logged in user
        if tradeObject.Trader().Name() != acm.User().Name():
            getLogger().info('Not logged in as trader.')
            originalTrader = tradeObject.Trader()
            tradeObject.Trader(acm.User()) 
    else:
        tradeObject.Trader(acm.User())
    
    # Get the applicable limits
    applicableLimits = GetLimits(tradeObject)
    getLogger().debug('Mandates to check total %s' % len(applicableLimits))

    if applicableLimits and len(applicableLimits) > 0:
        tradeOptionalKey = GetOptionalKey(tradeObject)
        tradeObject.OptionalKey(tradeOptionalKey)
        dialog = MandateCheckDialogBase(tradeObject, applicableLimits, tradeOptionalKey, shell, False)
        dialogResult = acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog)

        if dialogResult:
            getLogger().debug('Pre-Deal Hook: Mandates Dialog Success')
        else:
            getLogger().debug('Pre-Deal Hook: Mandates Dialog Cancel')
            
            # If the original is an infant, save the new trade as Simulated
            # so that we have a record of the trade - as per business requirement.
            # If the trade already exist in the DB, just block & discard the new changes.
            if not originalObject:
                getLogger().debug('Block new trade, save infant trade as Simulated.')
                modifiedObject.Status('Simulated')
            else:
                # The UI validation open a transactions. We need to pass the validation in order to 
                # to create and persist the Violation record in the transaction. If we fail the validation
                # by returning None, the violation record won't be created.
                getLogger().debug('Existing trade, revert changes.')
                modifiedObject.Apply(originalObject)
                modifiedObject.OptionalKey(tradeOptionalKey)
                
    # Update trader on trade ticket if logged on user is not the same as trader
    if originalTrader:
        tradeObject.Trader(originalTrader)
    
    return params


def ael_custom_dialog_main(parameters, dictExtra):
    # Not used for validation
    del parameters
    return dictExtra
