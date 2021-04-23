'''----------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementNettingProcess
PURPOSE                 :       This module is the worker module for the Netting ATS. Here new Netting Rules can be defined.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       Miguel Da Silva
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       662927
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-05-28      662927          Heinrich Cronje                 Initial Implementation
2012-07-13      335129          Heinrich Cronje                 Gold Netting Rule Implementation.
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    In the function CreateSettlementNetting enw netting rules can be defined.
    
    The new netting rule should be implemented as a class and this new netting rule class will call the helper class
    to commit the net.
'''

import acm
import FOperationsUtils as Utils
import FOperationsAMBAMessage
from SettlementNettingRuleSND import SettlementNettingRuleSND as SND_Netting
from SettlementNettingRuleGold import SettlementNettingRuleGold as Gold_Netting

#Settlement Types not needed for Netting.
INVALID_SETTLEMENT_TYPES = ['Security Nominal']

def GetPortfolio(obj):
    if obj.FromPortfolio():
        return obj.FromPortfolio()
    return obj.ToPortfolio()

def CreateSettlementNetting(obj):
    #Add more functions for diffrent netting rules here.
    isUpdateCollision = False
    snd_Netting_Execution = SND_Netting(obj)
    isUpdateCollision = snd_Netting_Execution.isUpdateCollision
    if not isUpdateCollision:
        gold_Netting_Execution = Gold_Netting(obj)
        isUpdateCollision = gold_Netting_Execution.isUpdateCollision
        
    return isUpdateCollision

def IsValidSettlement(obj):
    if obj.Status() == 'Authorised' and obj.RelationType() == 'None' and not obj.Parent():
        if obj.Type() not in (INVALID_SETTLEMENT_TYPES):
            return True
    return False

def objects_by_name(parent_obj, name_prefixes, name):
    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()
        
def __NettingProcessingUpdate(message):
    Utils.LogTrace()
    messageAsString = message.mbf_object_to_string()
    isUpdateCollision = False
    obj = None
    validSettlement = False

    for settlement_obj in objects_by_name(message, ['', '+', '!'], 'SETTLEMENT'):
        seqnbr_obj = settlement_obj.mbf_find_object('SEQNBR')
        if seqnbr_obj:
            seqnbr_value = seqnbr_obj.mbf_get_value()
            if seqnbr_value:
                settlement = acm.FSettlement[seqnbr_value]
                if settlement:
                    validSettlement = IsValidSettlement(settlement)
    if validSettlement:
        try:
            obj = acm.AMBAMessage.CreateSimulatedObject(messageAsString)
        except Exception, error:
            Utils.Log(True, 'Error in acm.AMBAMessage.CreateSimulatedObject: %s. \nAMBA message:\n %s' % \
                     (error, messageAsString))
        
        if not obj:
            Utils.Log(True, 'No object found in SettlementProcess')
            # The object was deleted and was not found by CreateSimulatedObject
            return isUpdateCollision
        
        Utils.Log(True, 'Got ' + str(obj.Class().Name()) + ' with name ' + str(obj.Name() + \
              ' updated by user ' + obj.UpdateUser().Name()))
        
        isUpdateCollision = CreateSettlementNetting(obj)
        
        #Clear simulated object from the dh
        try:
            acm.AMBAMessage.DestroySimulatedObject(obj)
        except Exception, error:
            Utils.Log(True, 'Error in acm.AMBAMessage.DestroySimulatedObject: %s. \nAMBA message:\n %s' % \
                     (error, messageAsString))

    return isUpdateCollision

def SettlementNettingProcess(msg):
    Utils.LogTrace()
    
    isUpdateCollision = False
    ambaMessage = FOperationsAMBAMessage.AMBAMessage(msg)
    if ambaMessage.GetNameOfUpdatedTable() == 'SETTLEMENT':
        isUpdateCollision = __NettingProcessingUpdate(msg)
    
    return isUpdateCollision
