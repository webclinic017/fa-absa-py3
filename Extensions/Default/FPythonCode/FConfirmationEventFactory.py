""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEventFactory.py"
from FConfirmationEventDefinition import FConfirmationEventDefinition as ConfirmationEventDefinition

class FConfirmationEventFactory():
    @staticmethod
    def GetConfirmationEvents():
        confirmationEvents = []
        for aConfirmationEventsDefinition in FConfirmationEventFactory.GetConfirmationEventDefinitions():
            aConfirmationEventsDefinition.CreateConfirmationEvent(confirmationEvents)
        return confirmationEvents

    @staticmethod
    def GetConfirmationEventDefinitions():
        import FConfirmationParameters as ConfirmationParameters

        for confEventDef in ConfirmationParameters.confirmationEvents:
            yield ConfirmationEventDefinition(*confEventDef)