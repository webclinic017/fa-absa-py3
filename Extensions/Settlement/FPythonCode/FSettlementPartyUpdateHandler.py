""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementPartyUpdateHandler.py"
import acm
import FOperationsAMBAMessage
from FSettlementEnums import SettlementStatus
from FOperationsExceptions import AMBAMessageException

class PartyUpdateHandler():
    def __init__(self, ambaMsg):
        assert ambaMsg.GetNameOfUpdatedTable() == 'PARTY'
        self.__tables = ambaMsg.GetTableAndChildTables()

    def FindConnectedSettlements(self):
        connectedSettlements = list()
        partyTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'PARTY')
        assert len(partyTables) == 1
        partyTable = partyTables[0]
        query = acm.CreateFASQLQuery(acm.FSettlement, 'OR')
        partyOid = partyTable.GetAttribute('PTYNBR')
        query.AddAttrNode('Acquirer.Oid', 'EQUAL', partyOid.GetValueBeforeUpdate())
        query.AddAttrNode('Counterparty.Oid', 'EQUAL', partyOid.GetValueBeforeUpdate())
        partyId = partyTable.GetAttribute('PTYID')
        query.AddAttrNode('TheirCorrBank', 'EQUAL', partyId.GetValueBeforeUpdate())
        query.AddAttrNode('TheirCorrBank2', 'EQUAL', partyId.GetValueBeforeUpdate())
        query.AddAttrNode('TheirCorrBank3', 'EQUAL', partyId.GetValueBeforeUpdate())
        query.AddAttrNode('TheirCorrBank4', 'EQUAL', partyId.GetValueBeforeUpdate())
        query.AddAttrNode('TheirCorrBank5', 'EQUAL', partyId.GetValueBeforeUpdate())
        resultSet = query.Select()
        for result in resultSet:
            connectedSettlements.append(result)
        return connectedSettlements

    def __HasValueChanged(self, table, attributeName):
        valueChanged = False
        try:
            partyId = table.GetAttribute(attributeName)
            valueChanged = partyId.HasChanged()
        except AMBAMessageException:
            valueChanged = False
        return valueChanged

    def HasAnyValuesAffectingSettlementsChanged(self):
        partyTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'PARTY')
        assert len(partyTables) == 1
        partyTable = partyTables[0]
        if self.__HasValueChanged(partyTable, 'PTYID'):
            return True
        if self.__HasValueChanged(partyTable, 'CLS'):
            return True
        if self.__HasValueChanged(partyTable, 'SWIFT'):
            return True
        accountTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'ACCOUNT')
        for accountTable in accountTables:
            if accountTable.GetTypeOfChange() == FOperationsAMBAMessage.TypeOfChange.DELETE:
                return True
            if self.__HasValueChanged(accountTable, 'NAME'):
                return True
            if self.__HasValueChanged(accountTable, 'NETWORK_ALIAS_TYPE') or \
               self.__HasValueChanged(accountTable, 'NETWORK_ALIAS_TYPE.ALIAS_TYPE_NAME'):
                return True
            if self.__HasValueChanged(accountTable, 'ACCOUNT'):
                return True
            if self.__HasValueChanged(accountTable, 'ACCOUNT2'):
                return True
            if self.__HasValueChanged(accountTable, 'ACCOUNT3'):
                return True
            if self.__HasValueChanged(accountTable, 'ACCOUNT4'):
                return True
            if self.__HasValueChanged(accountTable, 'ACCOUNT5'):
                return True
            if self.__HasValueChanged(accountTable, 'CORRESPONDENT_BANK_PTYNBR.PTYID'):
                return True
            if self.__HasValueChanged(accountTable, 'CORRESPONDENT_BANK2_PTYNBR.PTYID'):
                return True
            if self.__HasValueChanged(accountTable, 'CORRESPONDENT_BANK3_PTYNBR.PTYID'):
                return True
            if self.__HasValueChanged(accountTable, 'CORRESPONDENT_BANK4_PTYNBR.PTYID'):
                return True
            if self.__HasValueChanged(accountTable, 'CORRESPONDENT_BANK5_PTYNBR.PTYID'):
                return True
            if self.__HasValueChanged(accountTable, 'NETWORK_ALIAS_SEQNBR'):
                return True
        return False


    @staticmethod
    def FindAccountTableByName(tables, name):
        accounts = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(tables, 'ACCOUNT')
        for account in accounts:
            accountName = account.GetAttribute('NAME')
            if accountName.GetValueBeforeUpdate() == name:
                return account
        return None

    def __GetUpdatedCorrespondentBankName(self, oldCorrBank, oldCP, accountTable, corrBankAttributeName):
        bankName = oldCorrBank
        partyTable = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'PARTY')[0]
        try:
            partyId = partyTable.GetAttribute('PTYID')
            if oldCorrBank == partyId.GetValueBeforeUpdate():
                bankName = partyId.GetCurrentValue()
            elif oldCP == partyId.GetValueBeforeUpdate() and accountTable:
                if accountTable.GetTypeOfChange() == FOperationsAMBAMessage.TypeOfChange.DELETE:
                    bankName = ''
                else:
                    bankName = accountTable.GetAttribute(corrBankAttributeName).GetCurrentValue()
        except AMBAMessageException:
            bankName = oldCorrBank
        return bankName

    def __GetUpdatedCorrespondentAccountNumber(self, oldAccountNumber, oldCP, accountTable, accountAttributeName):
        accountNumber = oldAccountNumber
        partyTable = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'PARTY')[0]
        try:
            partyId = partyTable.GetAttribute('PTYID')
            if oldCP == partyId.GetValueBeforeUpdate() and accountTable:
                if accountTable.GetTypeOfChange() == FOperationsAMBAMessage.TypeOfChange.DELETE:
                    accountNumber = ''
                else:
                    accountNumber = accountTable.GetAttribute(accountAttributeName).GetCurrentValue()
        except AMBAMessageException:
            accountNumber = oldAccountNumber
        return accountNumber

    def __GetNameBeforeUpdateOfUpdatedParty(self):
        partyTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(self.__tables, 'PARTY')
        assert len(partyTables) == 1
        partyTable = partyTables[0]
        return partyTable.GetAttribute('PTYID').GetValueBeforeUpdate()

    def __UpdateCounterpartyInfoOnSettlement(self, settlement):
        cpInfo = PartyInfo()
        cpNameBeforeUpdate = settlement.CounterpartyName()
        cpInfo.SetPartyName(cpNameBeforeUpdate)
        accountNameBeforeUpdate = settlement.CounterpartyAccName()
        account = PartyUpdateHandler.FindAccountTableByName(self.__tables, accountNameBeforeUpdate)
        cpInfo.SetAccountName(accountNameBeforeUpdate)
        cpInfo.SetAccountNumber(settlement.CounterpartyAccount())
        cpInfo.SetNetworkName(settlement.CounterpartyAccountNetworkName())
        cpInfo.UpdateFromTables(self.__tables)
        settlement.CounterpartyName(cpInfo.GetPartyName())
        settlement.CounterpartyAccName(cpInfo.GetAccountName())
        settlement.CounterpartyAccount(cpInfo.GetAccountNumber())
        settlement.CounterpartyAccountNetworkName(cpInfo.GetNetworkName())
        account = PartyUpdateHandler.FindAccountTableByName(self.__tables, accountNameBeforeUpdate)
        settlement.TheirCorrBank(self.__GetUpdatedCorrespondentBankName(settlement.TheirCorrBank(), cpNameBeforeUpdate, account, 'CORRESPONDENT_BANK_PTYNBR.PTYID'))
        settlement.TheirCorrBank2(self.__GetUpdatedCorrespondentBankName(settlement.TheirCorrBank2(), cpNameBeforeUpdate, account, 'CORRESPONDENT_BANK2_PTYNBR.PTYID'))
        settlement.TheirCorrBank3(self.__GetUpdatedCorrespondentBankName(settlement.TheirCorrBank3(), cpNameBeforeUpdate, account, 'CORRESPONDENT_BANK3_PTYNBR.PTYID'))
        settlement.TheirCorrBank4(self.__GetUpdatedCorrespondentBankName(settlement.TheirCorrBank4(), cpNameBeforeUpdate, account, 'CORRESPONDENT_BANK4_PTYNBR.PTYID'))
        settlement.TheirCorrBank5(self.__GetUpdatedCorrespondentBankName(settlement.TheirCorrBank5(), cpNameBeforeUpdate, account, 'CORRESPONDENT_BANK5_PTYNBR.PTYID'))
        settlement.TheirCorrAccount(self.__GetUpdatedCorrespondentAccountNumber(settlement.TheirCorrAccount(), cpNameBeforeUpdate, account, 'ACCOUNT'))
        settlement.TheirCorrAccount2(self.__GetUpdatedCorrespondentAccountNumber(settlement.TheirCorrAccount2(), cpNameBeforeUpdate, account, 'ACCOUNT2'))
        settlement.TheirCorrAccount3(self.__GetUpdatedCorrespondentAccountNumber(settlement.TheirCorrAccount3(), cpNameBeforeUpdate, account, 'ACCOUNT3'))
        settlement.TheirCorrAccount4(self.__GetUpdatedCorrespondentAccountNumber(settlement.TheirCorrAccount4(), cpNameBeforeUpdate, account, 'ACCOUNT4'))
        settlement.TheirCorrAccount5(self.__GetUpdatedCorrespondentAccountNumber(settlement.TheirCorrAccount5(), cpNameBeforeUpdate, account, 'ACCOUNT5'))

    def __UpdateAcquirerInfoOnSettlement(self, settlement):
        acqInfo = PartyInfo()
        acqInfo.SetPartyName(settlement.AcquirerName())
        acqInfo.SetAccountName(settlement.AcquirerAccName())
        acqInfo.SetAccountNumber(settlement.AcquirerAccount())
        acqInfo.SetNetworkName(settlement.AcquirerAccountNetworkName())
        acqInfo.UpdateFromTables(self.__tables)
        settlement.AcquirerName(acqInfo.GetPartyName())
        settlement.AcquirerAccName(acqInfo.GetAccountName())
        settlement.AcquirerAccount(acqInfo.GetAccountNumber())
        settlement.AcquirerAccountNetworkName(acqInfo.GetNetworkName())

    def CreateUpdatedSettlement(self, oldSettlement):
        updatedSettlement = acm.FSettlement()
        updatedSettlement.RegisterInStorage()
        updatedSettlement.Status(SettlementStatus.NEW)
        updatedSettlement.Apply(oldSettlement)
        updatedSettlement.Owner(oldSettlement.Owner())  #owner is not copied when performing Apply()
        self.__UpdateCounterpartyInfoOnSettlement(updatedSettlement)
        self.__UpdateAcquirerInfoOnSettlement(updatedSettlement)
        updatedSettlement.Diary(None)
        return updatedSettlement

class PartyInfo():
    def __init__(self):
        self.__partyName = ''
        self.__accountName = ''
        self.__accountNumber = ''
        self.__networkName = ''

    def SetPartyName(self, partyName):
        self.__partyName = partyName

    def GetPartyName(self):
        return self.__partyName

    def SetAccountName(self, accountName):
        self.__accountName = accountName

    def GetAccountName(self):
        return self.__accountName

    def SetAccountNumber(self, accountNumber):
        self.__accountNumber = accountNumber

    def GetAccountNumber(self):
        return self.__accountNumber

    def SetNetworkName(self, networkName):
        self.__networkName = networkName

    def GetNetworkName(self):
        return self.__networkName

    def UpdateFromTables(self, tables):
        partyTables = FOperationsAMBAMessage.AMBAMessage.GetTablesByName(tables, 'PARTY')
        assert len(partyTables) == 1
        partyTable = partyTables[0]
        partyId = partyTable.GetAttribute('PTYID')
        if self.GetPartyName() == partyId.GetValueBeforeUpdate():
            self.SetPartyName(partyId.GetCurrentValue())
            accountTable = PartyUpdateHandler.FindAccountTableByName(tables, self.GetAccountName())
            if accountTable != None:
                if accountTable.GetTypeOfChange() == FOperationsAMBAMessage.TypeOfChange.DELETE:
                    self.SetAccountName('')
                    self.SetAccountNumber('')
                    self.SetNetworkName('')
                else:
                    self.SetAccountName(accountTable.GetAttribute('NAME').GetCurrentValue())
                    self.SetAccountNumber(accountTable.GetAttribute('ACCOUNT').GetCurrentValue())
                    networkAlias = ''
                    try:
                        networkAlias = accountTable.GetAttribute('NETWORK_ALIAS_TYPE.ALIAS_TYPE_NAME').GetCurrentValue()
                    except AMBAMessageException:
                        networkAlias = ''
                    self.SetNetworkName(networkAlias)
            else:
                self.SetAccountName('')
                self.SetAccountNumber('')
                self.SetNetworkName('')


