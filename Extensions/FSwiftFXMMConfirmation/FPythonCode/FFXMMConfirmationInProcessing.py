"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationInProcessing

DESCRIPTION:
    OPEN EXTENSION MODULE
    User can write custom logic to be executed in each state of the
    FSwiftFXMMConfirmationIn business process. It is derived from
    FFXMMConfirmationInProcessingBase

    The function prototype should be : process_state_xxx(business_process)
    where xxx is state name e.g. process_state_ready

    Base class implements following state processing:
     - process_state_ready
     - process_state_paired
     - process_state_unpaired

    If user wishes to add some extra processing for conditional entry state
     e.g. 'ready' he can implement method as
    def process_state_ready(self):
        # Custom logic before core logic
        super(FFXMMConfirmationInProcessing, self).process_state_ready()
        # Custom logic after core logic

VERSION: 3.0.1-0.5.3470
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('FXMMConfIn', 'FFXMMConfirmationInNotify_Config')
import FFXMMConfirmationInProcessingBase
import FNarrativeInProcessingBase

class FFXMMConfirmationInProcessing(FFXMMConfirmationInProcessingBase.FFXMMConfirmationInProcessingBase):
    def __init__(self, bpr):
        super(FFXMMConfirmationInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")

            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            pass

class FNarrativeInProcessing(FNarrativeInProcessingBase.FNarrativeInProcessingBase):
    def __init__(self, bpr):
        super(FNarrativeInProcessing, self).__init__(bpr)

    def process_state_xxx(self):
        """ process bpr state xxx"""
        try:
            notifier.INFO("Processing BPR step xxx")

            notifier.INFO("Completed processing BPR step xxx")
        except Exception as e:
            pass

