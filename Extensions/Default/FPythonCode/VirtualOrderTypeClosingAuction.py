import acm
import VirtualOrderTypeTriggerPhase


def OnPrepare(self):
    VirtualOrderTypeTriggerPhase.OnPrepare(self)

def OnPrepared(self):
    if None != self.UserTriggerPhase():
        userTriggerPhase = self.UserTriggerPhase()
        self.TriggerPhase = userTriggerPhase.strip()
