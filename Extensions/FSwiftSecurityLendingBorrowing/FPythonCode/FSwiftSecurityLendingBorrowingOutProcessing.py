"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecurityLendingBorrowingOutProcessing

DESCRIPTION:
    OPEN EXTENSION MODULE
    User can write custom logic to be executed in each state of the
    FSwiftCustomMessageSettlementOutProcessing business process. It is derived from
    FSwiftCustomMessageSettlementOutProcessingBase

    The function prototype should be : process_state_xxx(business_process)
    where xxx is state name e.g. process_state_ready


    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def process_state_ready(self):
        # Custom logic before core logic
        super(FSwiftCustomMessageSettlementOutProcessing, self).process_state_ready()
        # Custom logic after core logic

VERSION: 2.1.1-0.5.2995
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
import FSwiftSecurityLendingBorrowingOutProcessingBase

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', 'FSwiftSecurityLendingBorrowingOutNotify_Config')


class FSwiftSecurityLendingBorrowingOutProcessing(FSwiftSecurityLendingBorrowingOutProcessingBase.FSwiftSecurityLendingBorrowingOutProcessingBase):
    def __init__(self, bpr):
        super(FSwiftSecurityLendingBorrowingOutProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")

            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            pass

