"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2019-03-22  CHG1001539200  Tibor Reiss        Update and refactor to enable PS aggregation
2019-11-19  FAPE-101       Tibor Reiss        New payment type to improve PS aggregation
-----------------------------------------------------------------------------"""
import acm


ZAR_CALENDAR = acm.FCalendar["ZAR Johannesburg"]


class PARAMETERS(object):
    def __init__(self):
        self.__cashPostingInstrument = None
        self.__counterparty = None
        self.__acquirer = None
        self.__trader = None
        self.__portfolio = None
        self.__status = None
        self.__reportDate = None
        self.__restrictedPortfolios = []
        self.__calcSpace = None
        self.__grouper = None
        self.__preservePSYearlyTPL = None
        self.__queryFolder = None
        self.__calcSpaceClass = None
        self.__filterYearEndCrossTrades = None
        self.__monthlyBuckets = None
        self.__yearlyBuckets = None
        self.__tradeAdditionalInfos = []
        self.__tradeCurrency = acm.FCurrency['ZAR']
        self.__summaryDict = {}

    @property
    def cashPostingInstrument(self):
        return self.__cashPostingInstrument

    @cashPostingInstrument.setter
    def cashPostingInstrument(self, value):
        self.__cashPostingInstrument = value

    @property
    def counterparty(self):
        return self.__counterparty

    @counterparty.setter
    def counterparty(self, value):
        self.__counterparty = value

    @property
    def acquirer(self):
        return self.__acquirer

    @acquirer.setter
    def acquirer(self, value):
        self.__acquirer = value

    @property
    def trader(self):
        return self.__trader

    @trader.setter
    def trader(self, value):
        self.__trader = value

    @property
    def portfolio(self):
        return self.__portfolio

    @portfolio.setter
    def portfolio(self, value):
        self.__portfolio = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def reportDate(self):
        return self.__reportDate

    @reportDate.setter
    def reportDate(self, value):
        self.__reportDate = value

    @property
    def restrictedPortfolios(self):
        return self.__restrictedPortfolios

    @restrictedPortfolios.setter
    def restrictedPortfolios(self, value):
        self.__restrictedPortfolios = value

    @property
    def calcSpace(self):
        return self.__calcSpace

    @calcSpace.setter
    def calcSpace(self, value):
        self.__calcSpace = value

    @property
    def grouper(self):
        return self.__grouper

    @grouper.setter
    def grouper(self, value):
        self.__grouper = value

    @property
    def preservePSYearlyTPL(self):
        return self.__preservePSYearlyTPL

    @preservePSYearlyTPL.setter
    def preservePSYearlyTPL(self, value):
        self.__preservePSYearlyTPL = value

    @property
    def queryFolder(self):
        return self.__queryFolder

    @queryFolder.setter
    def queryFolder(self, value):
        self.__queryFolder = value

    @property
    def calcSpaceClass(self):
        return self.__calcSpaceClass

    @calcSpaceClass.setter
    def calcSpaceClass(self, value):
        self.__calcSpaceClass = value

    @property
    def summaryDict(self):
        return self.__summaryDict

    @summaryDict.setter
    def summaryDict(self, value):
        self.__summaryDict = value

    @property
    def filterYearEndCrossTrades(self):
        return self.__filterYearEndCrossTrades

    @filterYearEndCrossTrades.setter
    def filterYearEndCrossTrades(self, value):
        self.__filterYearEndCrossTrades = value

    @property
    def monthlyBuckets(self):
        return self.__monthlyBuckets

    @monthlyBuckets.setter
    def monthlyBuckets(self, value):
        self.__monthlyBuckets = value

    @property
    def yearlyBuckets(self):
        return self.__yearlyBuckets

    @yearlyBuckets.setter
    def yearlyBuckets(self, value):
        self.__yearlyBuckets = value

    @property
    def tradeCurrency(self):
        return self.__tradeCurrency

    @tradeCurrency.setter
    def tradeCurrency(self, value):
        self.__tradeCurrency = value

    @property
    def tradeAdditionalInfos(self):
        return self.__tradeAdditionalInfos

    @tradeAdditionalInfos.setter
    def tradeAdditionalInfos(self, value):
        self.__tradeAdditionalInfos = value
