""" Compiled: 2019-07-01 15:14:12 """

#__src_file__ = "extensions/settlement/etc/FSettlementModificationInspector.py"
import acm
import types

import FOperationsUtils as Utils
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementHierarchy import HierarchyTree
from FSettlementEnums import SettlementStatus
import FSettlementSettledAmountHandler as SettledAmountHandler

def IsPythonBuildInType(objectOrPrimitive):
    isPythonBuildInType = False
    if type(objectOrPrimitive) == bytes:
        isPythonBuildInType = True
    elif type(objectOrPrimitive) == float:
        isPythonBuildInType = True
    elif type(objectOrPrimitive) == int:
        isPythonBuildInType = True
    elif type(objectOrPrimitive) == type(None):
        isPythonBuildInType = True
    elif type(objectOrPrimitive) == bool:
        isPythonBuildInType = True
    return isPythonBuildInType

class SettlementModificationInspector(object):
    __fields = [
               'Status',
               'Acquirer.Oid',
               'AcquirerAccName',
               'AcquirerAccount',
               'AcquirerAccountNetworkName',
               'AcquirerName',
               'Amount',
               'Counterparty.Oid',
               'CounterpartyAccName',
               'CounterpartyAccount',
               'CounterpartyAccountNetworkName',
               'CounterpartyName',
               'TheirCorrBank',
               'TheirCorrBank2',
               'TheirCorrBank3',
               'TheirCorrBank4',
               'TheirCorrBank5',
               'TheirCorrAccount',
               'TheirCorrAccount2',
               'TheirCorrAccount3',
               'TheirCorrAccount4',
               'TheirCorrAccount5',
               'Currency.Oid',
               'FromPortfolio.Oid',
               'Owner.Oid',
               'Protection',
               'PrimaryIssuance',
               'SecurityInstrument.Oid',
               'NotificationDay',
               'SettleInstruction.Oid',
               'ToPortfolio.Oid',
               'Trade.Oid',
               'StateChart',
               'ValueDay',
               'DeliveryType',
               ]


    __settlementModificationHookFields = [
                                         'Acquirer',
                                         'AcquirerAccName',
                                         'AcquirerAccount',
                                         'AcquirerAccountNetworkName',
                                         'AcquirerName',
                                         'Amount',
                                         'Counterparty',
                                         'CounterpartyAccName',
                                         'CounterpartyAccount',
                                         'CounterpartyAccountNetworkName',
                                         'CounterpartyName',
                                         'Currency',
                                         'FromPortfolio',
                                         'IsValueDayCheckIgnored',
                                         'Protection',
                                         'PrimaryIssuance',
                                         'RestrictNet',
                                         'TheirCorrBank',
                                         'TheirCorrBank2',
                                         'TheirCorrBank3',
                                         'TheirCorrBank4',
                                         'TheirCorrBank5',
                                         'TheirCorrAccount',
                                         'TheirCorrAccount2',
                                         'TheirCorrAccount3',
                                         'TheirCorrAccount4',
                                         'TheirCorrAccount5',
                                         'ToPortfolio',
                                         'ValueDay',
                                         'PartialSettlementType',
                                         'DeliveryType',
                                         ]

    def __init__(self):
        ''' SettlementModificationInspector init method. '''
        1


    @staticmethod
    def IsModifiedLog(fieldString, oldSettlement):
        index = fieldString.find('.')
        if index > -1:
            fieldString = fieldString[0:index]
        Utils.LogVerbose('%s should be updated for settlement %d.' % (fieldString, oldSettlement.Oid()))


    def __IsModifiedStatus(self, oldSettlement, newSettlement):
        isModifiedStatus = False
        if oldSettlement.IsDirty():
            oldSettlement.IsDirty(False)
            isModifiedStatus = True
        elif (oldSettlement.IsValidForSTP() or
              oldSettlement.Status() == SettlementStatus.PENDING_AMENDMENT or
              oldSettlement.Status() == SettlementStatus.RECALLED):
            newSettlement.STP()
            if oldSettlement.Status() != newSettlement.Status():
                isModifiedStatus = True


        if isModifiedStatus == False:
            hierarchyTree = HierarchyTree(oldSettlement)
            if len(hierarchyTree.GetTopmostNodes()) > 0:
                newSettlement.STP()
                if newSettlement.IsUndeterminedAmount():
                    for node in hierarchyTree.GetTopmostNodes():
                        settlement = node.GetSettlement()
                        if settlement.IsValidForSTP():
                            if settlement.Status() != newSettlement.Status():
                                isModifiedStatus = True
                                break
        return isModifiedStatus
    
    def is_SBL_settlement(self, oldSettlement):
        if not oldSettlement.Trade():
            return False
                
        if oldSettlement.Trade().TradeInstrumentType() != 'SecurityLoan' and oldSettlement.Trade().TradeCategory() != 'Collateral':
            return False
        
        if not oldSettlement.Acquirer():
            return False
        
        if oldSettlement.Acquirer().Name() != 'SECURITY LENDINGS DESK':
            return False
            
        return True
        
    def IsModified(self, oldSettlement, newSettlement):
        ''' IsModified. '''
        isModified = False
        for field in self.__fields:
            if self.__IsFieldModified(oldSettlement, newSettlement, field):
                isModified = True
                SettlementModificationInspector.IsModifiedLog(field, oldSettlement)
                break
        else:
            Utils.LogVerbose('No relevant updates for settlement %d' % oldSettlement.Oid())
        return isModified

    def GetModifiedFields(self, oldSettlement, newSettlement):
        modifiedFields = list()
        for field in self.__fields:
            if self.__IsFieldModified(oldSettlement, newSettlement, field):
                modifiedFields.append(field)
        return modifiedFields

    def __IsFieldModified(self, oldSettlement, newSettlement, field):
        isModified = False
        hookAdmin = GetHookAdministrator()
        
        if field == "Amount":
            if not hookAdmin.HA_CallHook(SettlementHooks.COMPARE_SETTLEMENT_AMOUNTS, oldSettlement, newSettlement):
                isModified = True
        elif field == 'Status':
            if self.__IsModifiedStatus(oldSettlement, newSettlement) == True:
                isModified = True
        elif field == 'StateChart':
            if not oldSettlement.IsChildInHierarchy():
                if newSettlement.StateChart() is not oldSettlement.StateChart():
                    isModified = True
        elif field == 'CounterpartyName' and self.is_SBL_settlement(oldSettlement):
            Utils.LogVerbose('Skipping CounterpartyName check. SBL settlement %d' % oldSettlement.Oid())
            return False
        else:
            method = acm.FMethodChain(acm.FSymbol(field))
            if method.Call([oldSettlement]) != method.Call([newSettlement]):
                isModified = True
        return isModified
        
    def GetClientModifiedValues(self, newSettlement, settlementToModify):

        valuesList = list()
        for i in self.__settlementModificationHookFields:
            method = acm.FMethodChain(acm.FSymbol(str(i)))
            newValue = method.Call([newSettlement])
            oldValue = method.Call([settlementToModify])

            if newValue != oldValue:
                if IsPythonBuildInType(oldValue):
                    oldValueString = str(oldValue)
                else:
                    oldValueString = str(oldValue.Name())

                if IsPythonBuildInType(newValue):
                    newValueString = str(newValue)
                else:
                    newValueString = str(newValue.Name())

                valuesList.append((i, newValueString, oldValueString))
        return valuesList


