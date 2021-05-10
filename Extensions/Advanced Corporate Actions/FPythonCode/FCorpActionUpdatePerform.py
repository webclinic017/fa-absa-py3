""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionUpdatePerform.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionPerformArchiving - Manages the archiving and archive logging for
                                  corporate action related objects.

    (c) Copyright 201X FIS FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import acm, ael

#BDP
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

def Perform(args):
    handler = CorpActionsUpdateHandler(args)
    handler.Perform()

class CorpActionsUpdateHandler():
    def __init__(self, args):
        self.args = args
        self.testmode = None
        self.entityDict = None
        self.reportPath = None
        self.reportFilename = None

    def __needToUpdate(self, action):
        caChoices = action.CaChoices()
        if caChoices:
            Logme()("No need to update corp action {}.".format(action.Name()), "INFO") 
            return False

        oldQ = action.OldQuantity()
        newQ = action.NewQuantity()
        if (oldQ == 0 or newQ == 0) and action.CashAmount() == 0:
            Logme()("Ignore corp action {}, As there is no valid quanitity or cash amount "
                    "Not support to update to the new data format. ".format(action.Name()), "INFO")
            return False
            
        return True
    
    def __update(self, action):
        oldQ = action.OldQuantity()
        newQ = action.NewQuantity()
        cashAmount = action.CashAmount() 
        
        action.CaChoiceType("Mandatory")
        action.Commit()
        
        caNewChoice = acm.FCorporateActionChoice()
        caNewChoice.CorpAction(action)
        caNewChoice.IsDefault(True)
        caNewChoice.Commit()
        
        if (oldQ != 0 and newQ != 0):
            caPayout = acm.FCorporateActionPayout()
            caPayout.PayoutRate(newQ / oldQ)
            caPayout.CaChoice(caNewChoice);
            caPayout.Commit()

        if cashAmount:
            caPayout = acm.FCorporateActionPayout()
            caPayout.PayoutAmount(cashAmount)
            caPayout.CaChoice(caNewChoice);
            caPayout.Commit()

    def ReadArguments(self, args):
        self.corpActions = args.get("CorpActions", []) 
        self.testmode =  args.get("Testmode", 0)
        self.reportPath = args.get("report_path", None)

    def Perform(self):
        self.ReadArguments(self.args)
        for action in self.corpActions:
            if not action or not self.__needToUpdate(action):
                continue
            self.__update(action)
        return 
