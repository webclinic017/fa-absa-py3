""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSSetUpChoiceLists.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSSetUpChoiceLists

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FAssetManagementUtils import logger

class SetUpChoiceLists(object):

    @classmethod
    def SetUp(cls):
        choiceLists = cls.GetChoiceListSetUps()
        restart_needed = False
        for cl in choiceLists:
            if not cl._GetExisting():
                cl._CreateNew()
                if cl._RestartNeeded():
                    restart_needed = True
        return restart_needed

    @classmethod
    def IsSetUp(cls):
        choiceLists = cls.GetChoiceListSetUps()
        for cl in choiceLists:
            if not cl._GetExisting():
                return False
        return True

    @staticmethod
    def GetChoiceListSetUps():

        setups = []

        setups.append(ChoiceListSetUp(cList = 'UCITS_IssuerStatus',
                                      entry = 'Corporation',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_IssuerStatus',
                                      entry = 'Authorised Credit Institution',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_IssuerStatus',
                                      entry = 'Government',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_IssuerStatus',
                                      entry = 'Strong Entity',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_FundType',
                                      entry = 'UCITS',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_FundType',
                                      entry = 'Mixed',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_FundType',
                                      entry = 'Other',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_FundType',
                                      entry = 'Fund Of Funds',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'UCITS_FundType',
                                      entry = 'Hedge Fund',
                                      descr = None))

        setups.append(ChoiceListSetUp(cList = 'Limit Type',
                                      entry = 'UCITS',
                                      descr = None))


        return setups

class ChoiceListSetUp(object):
    def __init__(self, cList, entry, descr):
        self._list = cList
        self._entry = entry
        self._descr = descr

    def __GetChoiceList(self, cList, entry):
        return acm.FChoiceList.Select01("list = '%s' and name = '%s'" % (cList, entry), None)

    def __GetMasterList(self):
        return self.__GetChoiceList('MASTER', self._list)

    def __CreateChoiceListEntry(self, cList, entry, descr):
        cl = acm.FChoiceList()
        cl.List(cList)
        cl.Name(entry)
        cl.Description(descr)
        cl.Commit()

    def _GetExisting(self):
        return self.__GetChoiceList(self._list, self._entry)

    def _CreateNew(self):
        clParent = self.__GetMasterList()
        if not clParent:
            self.__CreateChoiceListEntry('MASTER', self._list, None)
            logger.DLOG("Created choice list list '%s'" % self._list)
        self.__CreateChoiceListEntry(self._list, self._entry, self._descr)
        logger.DLOG("Created %s '%s'" % (self._list, self._entry))

    def _RestartNeeded(self):
        restart = False
        if self._list == 'Additional Payments' and not self._entry in acm.GetDomain("enum(PaymentType)").Enumerators():
            restart = True
        return restart

    def Description(self):
        return 'ChoiceList( %s )' % self._list