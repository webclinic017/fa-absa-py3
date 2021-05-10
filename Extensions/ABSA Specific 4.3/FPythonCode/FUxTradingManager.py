import acm
from auto_confirm import AutoConfirmation as AC


def ApplyStatusChange(eii): 
    """A simple workaround for bulk trade status confirmation to avoid error
    'Invalid portoflio and acquirer in the mirror trade'
    """
    
    selection = eii.ExtensionObject().ActiveSheet().Selection()
    shell = eii.Parameter('shell')
    
    # FIXME Remove once Prime >= 2015.3 is deployed
    for cached_trade in selection.SelectedTrades():
        try:
            trade = acm.FTrade[cached_trade.Oid()]
            AC.hotfix_confirm_trade(trade, cached_trade.Status())
        except RuntimeError as error:
            acm.UX().Dialogs().MessageBoxInformation(shell, error)
