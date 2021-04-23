""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOPostUploadContractHandler.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOPostUploadContractHandler -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Handler class for dealing with persisted and non-persisted FRN:s.

-------------------------------------------------------------------------------------------------------"""

import acm

from FWSODictToFrnDict import WsoDictToFrnDict
from FWSODictToFrnDetailsDict import WsoDictToFrnDetailsDict
from FWSOFrnFactory import FrnFactory
from FWSOCashflowFactory import CashflowFactory
from FWSODictAccessor import WSODictAccessor
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class PostUploadContractHandler(object):

    def __init__(self, frn):
        self.frn = frn
        self.leg = self.frn.FirstFloatLeg()
        self.contractDict = self._RetrieveContractDict()
        self.frnLegDict = self._RetrieveFrnLegDict()
        self.frnDetailsDict = self._RetrieveFrnDetailsDict()
        
    def _ContractId(self):
        frnName = self.frn.Name()
        contractId = frnName.split('_')[1]
        return contractId
        
    def ContractDicts(self):
        return WSODictAccessor.Contract()
        
    def _RetrieveContractDict(self):
        contractId = self._ContractId()
        contractDicts = self.ContractDicts()
        contractDict = contractDicts.get(contractId)
        return contractDict

    def _RetrieveFrnLegDict(self):
        wsoDictToFrnDict = WsoDictToFrnDict(self.contractDict)
        return wsoDictToFrnDict.FrnLegDict()    
        
    def _RetrieveFrnDetailsDict(self):
        wsoDictToFrnDetailsDict = WsoDictToFrnDetailsDict(self.contractDict) 
        return wsoDictToFrnDetailsDict.FrnDetailsDict()  

    def _WSODictToFrnDict(self):
        return WsoDictToFrnDict(self.contractDict)   
    
    def _IsProjectedCashflow(self, cashflow):
        contractMaturityDate = self.contractDict.get('Contract_MaturityDate')[0:10]
        isProjected = bool(cashflow.StartDate() >= contractMaturityDate)
        return isProjected
    
    def _IsFixedAmountCashflow(self, cashflow):
        return bool(cashflow.CashFlowType() == 'Fixed Amount')
    
    def CreateIpfCashflows(self):
        logger.debug('Generating IPF cashflows for FRN %s.' % self.frn.Name())
        for contractDetailIpfDicts in self.frnDetailsDict.values():
            for ipfDict in contractDetailIpfDicts.values():
                cashflowFactory = CashflowFactory(self.frn, ipfDict)
                cashflow = cashflowFactory.Create()
                logger.debug('Created IPF cashflow with start date %s, end date %s, and pay date %s.' % (
                              cashflow.StartDate(), cashflow.EndDate(), cashflow.PayDate()))
        logger.debug('Finished creating IPF cashflows for frn %s.' % self.frn.Name())
    
    def AdjustNominalOfProjectedCashflows(self):
        wsoDictToFrnDict = self._WSODictToFrnDict()  
        frnOriginalNominalFactor = wsoDictToFrnDict.OriginalNominalAmount()
        for cashflow in self.leg.CashFlows():
            if self._IsProjectedCashflow(cashflow) or self._IsFixedAmountCashflow(cashflow):
                logger.debug('Projected cashflow nominal set from %f to %f using the scaling factor %f for FRN %s.' % (
                              cashflow.NominalFactor(), frnOriginalNominalFactor, frnOriginalNominalFactor, self.frn.Name()))
                cashflow.NominalFactor(frnOriginalNominalFactor)
    
    def UpdateLegAsTransaction(self, frnFactory):
        try:
            acm.BeginTransaction()
            frnFactory.UpdateLeg()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            logger.error('Transaction aborted due to error when updating leg:', e)
    
    def CommitFrn(self):
        self.frn.Commit()
        
    def ProcessCashflows(self, frnFactory):
        frnFactory.ClearRedundantCashFlowFromActiveContract()
        self.CreateIpfCashflows()
        self.AdjustNominalOfProjectedCashflows()
        self.CommitFrn()

    def ProcessCashflowsAsTransaction(self, frnFactory):
        try:
            acm.BeginTransaction()
            self.ProcessCashflows(frnFactory)
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            logger.error('Post Upload Transaction aborted due to an error:', e)

    def Run(self):
        frnFactory = FrnFactory(self.frn, self.frnLegDict)
        self.UpdateLegAsTransaction(frnFactory)
        self.ProcessCashflowsAsTransaction(frnFactory)
