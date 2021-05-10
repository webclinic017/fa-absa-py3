"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementInProcessing

DESCRIPTION:
    OPEN EXTENSION MODULE
    User can write custom logic to be executed in each state of the
    FSwiftSecuritySettlementIn business process. It is derived from
    FSecuritySettlementInProcessingBase

    The function prototype should be : process_state_xxx(business_process)
    where xxx is state name e.g. process_state_ready

    The base class implements following state processing:
     - process_state_ready
     - process_state_paired
     - process_state_partialmatch

    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def process_state_ready(self):
        # Custom logic before core logic
        super(FSecuritySettlementInProcessing, self).process_state_ready()
        # Custom logic after core logic

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FSecuritySettlementInProcessingBase

class FSecuritySettlementInProcessing(FSecuritySettlementInProcessingBase.FSecuritySettlementInProcessingBase):
    def __init__(self, bpr):
        super(FSecuritySettlementInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")
            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step xxx: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

class FSecuritySettlementStatusProcessingAdviceInProcessing(FSecuritySettlementInProcessingBase.FSecuritySettlementStatusProcessingAdviceInProcessingBase):
    def __init__(self, bpr):
        super(FSecuritySettlementStatusProcessingAdviceInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")
            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step xxx: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

class FClientStatementOfHoldingInProcessing(FSecuritySettlementInProcessingBase.FClientStatementOfHoldingInProcessingBase):
    def __init__(self, bpr):
        super(FClientStatementOfHoldingInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")
            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            notifier.ERROR("Error occurred while processing BPR step xxx: %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

