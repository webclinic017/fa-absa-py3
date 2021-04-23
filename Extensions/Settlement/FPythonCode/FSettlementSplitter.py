""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementSplitter.py"
import acm
import FOperationsUtils as Utils
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator

class SettlementSplitter(object):
    def __init__(self, originalSettlement = None):
        self.__originalSettlement = originalSettlement
        self.__splittedSettlements = list()
        self.__hookAdmin = GetHookAdministrator()
        self.__isCustomHookDefined = self.__hookAdmin.HA_IsCustomHook(SettlementHooks.SPLIT_SETTLEMENT)
        self.__choiceListItems = dict()

        for choiceListItem in acm.FChoiceList.Select("list='SettlementSplitType'"):
            self.__choiceListItems[choiceListItem.Name()] = choiceListItem
        self.__choiceListItems[''] = None

    def SetOriginalSettlement(self, originalSettlement):
        self.__originalSettlement = originalSettlement

    def GetOriginalSettlement(self):
        return self.__originalSettlement

    def __SetOriginalSettlementAndClear(self, originalSettlement):
        self.SetOriginalSettlement(originalSettlement)
        del self.__splittedSettlements[:]

    def ClearSplittedSettlements(self):
        del self.__splittedSettlements[:]

    def GetSplittedSettlements(self):
        return self.__splittedSettlements

    def HasSplittedSettlements(self):
        return len(self.__splittedSettlements) > 0

    def __IsValidSplitTypes(self, splitParts):
        isValidSplitTypes = True
        for splitPart in splitParts:
            if len(splitPart) == 2 or len(splitPart) == 3:
                splitType = splitPart[1]
                if False == (splitType in self.__choiceListItems):
                    isValidSplitTypes = False
                    Utils.LogVerbose('ChoiceList SettlementSplitType or ChoiceListItem %s does not exist' % str(splitType))
                    Utils.LogVerbose('Settlement split will not be performed')
                    break
            else:
                isValidSplitTypes = False
                Utils.LogVerbose('Incorrect split part tuple length. Settlement split will not be performed')
                break
        return isValidSplitTypes

    def __SplitSettlement(self):
        if self.__originalSettlement:
            splitParts = self.__hookAdmin.HA_CallHook(SettlementHooks.SPLIT_SETTLEMENT, self.__originalSettlement)
            if self.__IsValidSplitTypes(splitParts):
                for splitPart in splitParts:
                    amount, splitType, diaryNote = (0.0, '', None)
                    if len(splitPart) == 2:
                        amount, splitType = splitPart
                    else:
                        amount, splitType, diaryNote = splitPart
                    originalClone = acm.FSettlement()
                    originalClone.RegisterInStorage()
                    originalClone.Apply(self.__originalSettlement)
                    originalClone.Amount(amount)
                    originalClone.SplitTypeChlItem(self.__choiceListItems[splitType])
                    if diaryNote != None:
                        originalClone.AddDiaryNote(diaryNote)
                    self.__splittedSettlements.append(originalClone)

    def SplitSettlement(self, originalSettlement = None):
        if self.__isCustomHookDefined:
            if originalSettlement:
                self.__SetOriginalSettlementAndClear(originalSettlement)
                self.__SplitSettlement()
            else:
                self.ClearSplittedSettlements()
                self.__SplitSettlement()
