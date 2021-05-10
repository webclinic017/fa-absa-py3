
import acm
import FLogger

logger = FLogger.FLogger.GetLogger('FQuoteMonitor')

def handle_result(task):
    try:
        group = task.ResultOrThrow()
    except Exception as e:
        logger.error("Failed to enable quote group: %s", str(e))
        
def enable_quotes(invokation_info):
    button = invokation_info.Parameter('ClickedButton')
    if button:
        group = button.RowObject().QuoteGroup()
        if group and group.State() == 'Disabled':
            acm.MarketMaking.EnableQuoteGroup(group).ContinueWith(handle_result)
            
