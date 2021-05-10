"""----------------------------------------------------------------------------
MODULE:
    FCashOutProcessing

DESCRIPTION:
    OPEN EXTENSION MODULE
    User can write custom logic to be executed in each state of the
    FXTradeConfMsg business process. It is derived from
    FFXTradeConfMsgProcessingBase

    The function prototype should be : process_state_xxx(business_process)
    where xxx is state name e.g. process_state_ready


    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def process_state_ready(self):
        # Custom logic before core logic
        super(FFXTradeConfOutMsgProcessing, self).process_state_ready()
        # Custom logic after core logic

VERSION: 3.0.0-0.5.3383
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')
import FCashOutProcessingBase


class FCashOutProcessing(FCashOutProcessingBase.FCashOutProcessingBase):
    def __init__(self, bpr):
        super(FCashOutProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")

            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            pass



