import acm
import string
import VirtualOrderType


def OnPrepare(self):    
    VirtualOrderType.OnPrepare(self)
    if None != self.UserTriggerPhase():
        userTriggerPhase = self.UserTriggerPhase()
        self.TriggerPhase = userTriggerPhase.strip()
