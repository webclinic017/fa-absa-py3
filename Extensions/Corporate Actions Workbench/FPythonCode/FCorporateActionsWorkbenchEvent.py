""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchEvent.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchEvent

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm


from FEvent import (
                BaseEvent,
                OnObjectsSelected,
                )

class OnCorporateActionSelected(OnObjectsSelected):
    pass

class OnCorporateActionElectionSelected(OnObjectsSelected):
    pass
    
class OnPortfolioSelected(OnObjectsSelected):
    pass

class OnTradeSelected(OnObjectsSelected):
    pass

class OnCorporateAction(BaseEvent):
    pass

class OnCorporateActionChoice(BaseEvent):
    pass

class OnCorporateActionPayout(BaseEvent):
    pass

class OnTreeItemSelected(OnObjectsSelected):
    pass


