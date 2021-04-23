""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEventDefinition.py"
import acm
import FOperationsUtils
from FConfirmationEvent import FConfirmationEvent
from FConfirmationHelperFunctions import FConfirmationHelperFunctions

class FConfirmationEventDefinition(object):

    def __init__(self, eventName, baseRule, subType = "Default", subTypeRule = None, receivers = ["Counterparty"]):
        self.eventName = eventName
        self.baseRule = baseRule
        self.subType = subType # "Default", "Cash Flow" or "Reset"
        self.subTypeRule = subTypeRule
        self.receivers = receivers
        self.niceName = ''
        self.SetNiceName(eventName, baseRule, subType, subTypeRule, receivers)

    def SetNiceName(self, eventName, baseRule, subType = "Default", subTypeRule = None, receivers = ["Counterparty"]):
        ret = "'%s', '%s'" % (eventName, baseRule)
        if subType:
            ret = "%s, subType='%s'" % (ret, str(subType))
        if str(subTypeRule):
            ret = "%s, subTypeRule='%s'" % (ret, str(subTypeRule))
        if str(receivers):
            ret = "%s, receivers=%s" % (ret, str(receivers))
        self.niceName = "(%s)" % ret

    def GetNiceName(self):
        return self.niceName

    def CreateConfirmationEvent(self, confirmationEvents):
        if isinstance(self.baseRule, str):
            storedBaseRule = acm.FStoredASQLQuery[self.baseRule]
            if not storedBaseRule:
                unknownBaseRule = self.baseRule
                self.baseRule = FConfirmationHelperFunctions.GetIsNewTradeEvent()
                FOperationsUtils.LogVerbose("No Insert Items query called %s for event %s found. Default query will be used: %s" % (unknownBaseRule, self.eventName, self.baseRule))
            else:
                self.baseRule = storedBaseRule.Query()

        if isinstance(self.subTypeRule, str):
            storedSubTypeRule = acm.FStoredASQLQuery[self.subTypeRule]
            if(not storedSubTypeRule):
                raise Exception("No Insert Items query called %s for event %s found. Check your FConfirmationParameters settings." % (self.subTypeRule, self.eventName))
            else:
                self.subTypeRule = storedSubTypeRule.Query()

        for receiver in self.receivers:
            confirmationEvent = FConfirmationEvent(self.eventName, self.baseRule, self.subType, self.subTypeRule, receiver)
            confirmationEvents.append(confirmationEvent)

