""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorpActionsWorkbenchChoiceTableEventAdapter.py"
import acm
import FCorporateActionsWorkbenchEvent
from FHandler import Handler
from FCorpActionsWorkbenchTableEventAdapter import TableListener
from FCorpActionsWorkbenchTableEventAdapter import LISTEN_EVENTS
from FCorpActionsWorkbenchLogger import logger

class ChoiceTableEventAdapter(TableListener, Handler):

    def __init__(self, dispatcher):
        TableListener.__init__(self, 'CorpActChoice')
        Handler.__init__(self, dispatcher)
        self.HandleViewCreated()

    def HandleViewCreated(self):
        self.StartSubscription()

    def HandleViewDestroyed(self, _view):
        self.EndSubscription()

    # ---- Methods overriden from TableListener ----
    def _OnEntity(self, acmEntity, event):
        if event in LISTEN_EVENTS:
            self.SendEvent(FCorporateActionsWorkbenchEvent.OnCorporateActionChoice(self, [acmEntity, event]))
