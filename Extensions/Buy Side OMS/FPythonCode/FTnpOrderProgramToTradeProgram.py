""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTnpOrderProgramToTradeProgram.py"
"""--------------------------------------------------------------------------
MODULE
    FTnpOrderProgramToTradeProgram

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Used for creating Deal Packages and initiating their workflow from Order Programs in TAB
-----------------------------------------------------------------------------"""

import acm
import FTnpUtils
from ACMPyUtils import Transaction
from FParameterSettings import ParameterSettingsCreator
from FTradeProgram import _ValidDealPackageDefinitions as validTradePrograms, LinkedTrades
import FBusinessProcessUtils as utils

class OrderProgramToTradeProgram(object):
    
    DEAL_PACKAGE_DEFINITION = 'External'
    
    def __init__(self, tnpOrderProgram):
        self._tnpOrderProgram = tnpOrderProgram
    
    @classmethod
    def InitializeFromOrder(cls, tnpOrder):
        tnpOrderProgram = FTnpUtils.GetOrderProgramForOrder(tnpOrder)
        return cls(tnpOrderProgram) if tnpOrderProgram else None
    
    def DealPackage(self):
        return acm.FDealPackage[self._OrderProgramId()]
    
    def BusinessProcess(self):
        return self._BusinessProcess(self.DealPackage())
    
    def CreateDealPackage(self):
        definition = self._DealPackageDefinition(self._tnpOrderProgram)
        dealPackage = acm.DealPackage.New(definition)
        dealPackage.OptionalId(self._OrderProgramId())
        dealPackage.SuggestName(self._tnpOrderProgram.TNPORDERPROGRAMNAME.szOrderProgramName())
        owner = acm.FUser.Select01('name like {0}'.format(self._tnpOrderProgram.TNPBROKERID.szBrokerId()), '')
        dealPackage.Owner(owner)
        return self._SaveDealPackage(dealPackage)
    
    def AddTradeToDealPackage(self, trade):
        trade.OpeningDealPackage = self.DealPackage()

    def AreAllTradesInDealPackage(self):
        return self._tnpOrderProgram.dwOrderCount() == len(LinkedTrades(self.DealPackage()))
    
    def StartWorkflow(self):
        self._WorkflowClass().InitializeFromSubject(self.DealPackage())
    
    def CanBusinessProcessBeMoved(self):
        businessProcess = self.BusinessProcess()
        return businessProcess.CurrentStep().IsInReadyState() if businessProcess else False
    
    def MoveWorkflowFromReady(self):
        businessProcess = self.BusinessProcess()
        if businessProcess and businessProcess.CurrentStep().IsInReadyState():
            try:
                stateChart = businessProcess.StateChart()
                eventName = stateChart.ReadyState().Transitions().At(0).EventName()
                businessProcess.HandleEvent(eventName, None, None)
                businessProcess.Commit()
            except Exception as e:
                self.Log().error('Could not handle event {0} for Business Process {1}'.format(eventName, businessProcess.Oid()))
                self.HandleError('Problem moving workflow from state ready, reason: {0}'.format(e))
                
    def HandleError(self, error):
        businessProcess = self.BusinessProcess()
        if businessProcess:
            self.Log().error('Setting business process {0} to error, reason: {1}'.format(businessProcess.Oid(), error))
            utils.SetBusinessProcessToError(businessProcess, str(error))       

    def DeleteTradeProgram(self):
        if self.DealPackage():
            trades = LinkedTrades(self.DealPackage())
            setting = self._Settings().OnOrderProgramDeleted()
            acm.PollAllDbEvents()
            acm.BeginTransaction()
            try:
                if setting == 'Delete':
                    self._DeleteBusinessProcess(self.DealPackage())
                    ambaMessage = self._DeleteTradesAndDealPackage(trades, self.DealPackage())
                elif setting == 'Archive':
                    self._ArchiveBusinessProcess(self.DealPackage())
                    ambaMessage = self._ArchiveTrades(trades)
                    self._ArchiveDealPackage(self.DealPackage())
                elif setting == 'Void':
                    ambaMessage = self._VoidTrades(trades)
                else:
                    self.Log().error('Invalid setting for "OnOrderProgramDeleted". Setting should be Delete, Archive or Void')
                acm.CommitTransaction()
            except Exception as e:
                acm.AbortTransaction()
                self.Log().warning('Could not delete trade program {0}'.format(str(e)))
                self.HandleError('Problem deleting trade program, reason: {0}'.format(e))
            else:
                return ambaMessage
            
    def _OrderProgramId(self):
        return self._tnpOrderProgram.szOrderProgramId()
    
    def HasBusinessProcess(self):
        return bool(self._BusinessProcess(self.DealPackage()))
        
    @classmethod
    def _VoidTrades(cls, trades):
        for trade in trades:
            trade.Status('Void')
        return FTnpUtils.AMBAMessageForObjects(trades, 'UPDATE TRADE')
    
    @classmethod
    def _ArchiveTrades(cls, trades):
        for trade in trades:
            trade.Status('Void')
            trade.ArchiveStatus(1)
        return FTnpUtils.AMBAMessageForObjects(trades, 'UPDATE TRADE')
    
    def _DeleteTradesAndDealPackage(self, trades, dealPackage):
        objects = trades.AddAll([dealPackage, dealPackage.InstrumentPackage()])
        return FTnpUtils.AMBAMessageForObjects(objects, 'DELETE')
        
    @classmethod        
    def _DealPackageDefinition(cls, tnpOrderProgram):
        tradePrograms = [tradeProgram.DisplayName() for tradeProgram in validTradePrograms()]
        orderProgramName = tnpOrderProgram.TNPORDERPROGRAMNAME.szOrderProgramName()
        return next((tradeProgram for tradeProgram in tradePrograms
                     if orderProgramName.startswith(tradeProgram)), cls.DEAL_PACKAGE_DEFINITION)
    
    @classmethod
    def _WorkflowClass(cls):
        moduleName, className = cls._Settings().WorkflowClass().split('.')
        module = __import__(moduleName)
        return getattr(module, className)
    
    @staticmethod
    def _SaveDealPackage(dealPackage):
        with Transaction():
            return dealPackage.Save()[0].DealPackage()
    
    @classmethod
    def _ArchiveDealPackage(cls, dealPackage):
        instrumentPackage = dealPackage.InstrumentPackage()
        dealPackage.ArchiveStatus(1)
        dealPackage.Commit()
        instrumentPackage.ArchiveStatus(1)
        instrumentPackage.Commit()
    
    @classmethod
    def _BusinessProcess(cls, dealPackage):
        try:
            bp = acm.BusinessProcess.FindBySubjectAndStateChart(dealPackage, cls._WorkflowClass().StateChart())[0]
            if bp.Subject().Oid() == dealPackage.Oid():
                return bp
        except (IndexError, TypeError):
            return None
    
    @classmethod
    def _DeleteBusinessProcess(cls, dealPackage):
        try:
            cls._BusinessProcess(dealPackage).Delete()
        except AttributeError:
            cls.Log().info('No business process found')
    
    @classmethod
    def _ArchiveBusinessProcess(cls, dealPackage):
        try:
            bp = cls._BusinessProcess(dealPackage)
            bp.ArchiveStatus(1)
            bp.Commit()
            for step in bp.Steps():
                step.ArchiveStatus(1)
                step.Commit()
        except AttributeError:
            cls.Log().info('No business process found')
    
    @staticmethod
    def _Settings():
        return ParameterSettingsCreator.FromRootParameter('TABSettings')
        
    @staticmethod
    def Log():
        return FTnpUtils.TnpDependecies.LOG
