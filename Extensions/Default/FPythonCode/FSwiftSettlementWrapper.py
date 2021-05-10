""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftSettlementWrapper.py"
"""----------------------------------------------------------------------------
MODULE
    FSwiftSettlement - Module that provides a wrapper class for the ACM entity
    Confirmation


    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

class FSwiftSettlement(object):

    def __init__(self, boEntity):
        self.boEntity = boEntity

    def __getattr__(self, attr):
        return getattr(self.boEntity, attr)

    def GetAccountBic(self):
        '''Returns SWIFT bic code of the FAccount,
        if empty fallback value is BIC from the general tab.'''
        bic = ''
        cpRef = self.boEntity.CounterpartyAccountRef()
        if cpRef and cpRef.NetworkAlias():
            bic = cpRef.NetworkAlias().Alias()
        if not bic and self.boEntity.Counterparty():
            bic = self.boEntity.Counterparty().Swift()
        return bic

    def GetCounterpartyType(self):
        counterPartyType = ''
        counterParty = self.boEntity.Counterparty()
        if (counterParty and len(counterParty.Accounts()) != 0) :
            counterPartyType = counterParty.Type()
        return counterPartyType

    def GetNotifyReceipt(self):
        notifyReceipt = ''
        acqRef = self.boEntity.AcquirerAccountRef()
        if acqRef:
            correspondentBank = acqRef.CorrespondentBank()
            if correspondentBank:
                notifyReceipt = correspondentBank.NotifyReceipt()
        return notifyReceipt

    def IsTargetTwo(self):
        """This method is used to determine if settlement is for
            Target2 or not. Target2 is a Sub Network choice list on
            the counterparty account.
        """

        import FSwiftParameters as Global

        SWIFT_SUB_NETWORKS = Global.SWIFT_SUB_NETWORKS
        if not SWIFT_SUB_NETWORKS:
            return False

        if self.boEntity:
            if self.Amount() >= 0:
                return False
            if self.Currency().Name() != 'EUR':
                return False

        subNetwork = self.CounterpartyAccountSubNetworkName()
        if subNetwork:
            return (subNetwork.upper() == "TARGET2"
                    and subNetwork in SWIFT_SUB_NETWORKS)

        return False



    def IsEba(self):
        """This method is used to determine if settlement is for
            EBA or not. EBA is a Sub Network choice list on
            the counterparty account.
        """

        import FSwiftParameters as Global

        SWIFT_SUB_NETWORKS = Global.SWIFT_SUB_NETWORKS
        if not SWIFT_SUB_NETWORKS:
            return False

        if self.boEntity:
            if self.Amount() >= 0:
                return False
            if self.Currency().Name() != 'EUR':
                return False

        subNetwork = self.CounterpartyAccountSubNetworkName()
        if subNetwork:
            return (subNetwork.upper() == "EBA"
                    and subNetwork in SWIFT_SUB_NETWORKS)

        return False



