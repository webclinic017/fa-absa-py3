""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationMatcher.py"
import acm
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
import FOperationsUtils as Utils
from FConfirmationChecksum import CreateChecksum

class ConfirmationMatcher:

    def __init__(self, newConfirmations, oldConfirmations):
        self.__newConfirmations = newConfirmations
        self.__oldConfirmations = oldConfirmations
        self.__matchedConfirmations = list()
        self.__FindMatchingConfirmations()

    def GetMatchedConfirmations(self):
        return self.__matchedConfirmations

    def __FindMatchingConfirmations(self):
        for newConfirmation in self.__newConfirmations:
            matchedConfirmation = None
            for oldConfirmation in self.__oldConfirmations:
                bottommostConfirmation = HelperFunctions.GetBottommostConfirmation(oldConfirmation)
                if bottommostConfirmation.EventChlItem() == newConfirmation.EventChlItem():
                    if bottommostConfirmation.Receiver() == newConfirmation.Receiver():
                        if HelperFunctions.HasConfirmationStructureBeenInReleased(oldConfirmation):
                            if oldConfirmation.ReceiverMethod():
                                method = acm.FMethodChain(acm.FSymbol(str(oldConfirmation.ReceiverMethod())))
                                if oldConfirmation.Receiver() != method.Call([newConfirmation]):
                                    break
                        if bottommostConfirmation.Subject():
                            if bottommostConfirmation.Subject() == newConfirmation.Subject():
                                matchedConfirmation = oldConfirmation
                                self.__oldConfirmations.remove(oldConfirmation)
                                break
                        elif not newConfirmation.Subject():
                            matchedConfirmation = oldConfirmation
                            self.__oldConfirmations.remove(oldConfirmation)
                            break

            self.__matchedConfirmations.append((newConfirmation, matchedConfirmation))

        for oldConfirmation in self.__oldConfirmations:
            self.__matchedConfirmations.append((None, oldConfirmation))