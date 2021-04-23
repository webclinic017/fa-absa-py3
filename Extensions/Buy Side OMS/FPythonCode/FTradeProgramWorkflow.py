""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTradeProgramWorkflow.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgramWorkflow

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Implementation of Workflow class that handles the workflow after a Trade Program
    has been created but before the orders are available for trading.
    The workflow performs a compliance check and sets the orders to Pending Execution
    once everything has been approved for trading.
-----------------------------------------------------------------------------"""

from itertools import chain

import acm
import FOrderUtils
import FAlertGenerator
import FComplianceRulesUtils
import FComplianceCheckReport
from FWorkflow import AsynchronousWorkflow, ActionState, LOGGER
from FTradeProgram import LinkedTrades
from FPromise import Promise, PromiseInterface, AsynchronousCall
from FParameterSettings import ParameterSettingsCreator

SETTINGS = ParameterSettingsCreator.FromRootParameter('BSOMSSettings')


class EnsureTradesInStatus(PromiseInterface):
    
    STATUS = None
    
    def Init(self, *args, **kwargs):
        self._trades = kwargs['trades']
        
    def Fulfilled(self, *args, **kwargs):
        return all(trade.Status() == self.STATUS for trade in self._trades)

    def Subscriptions(self, *args, **kwargs):
        return self._trades
    
    def Timeout(self):
        return SETTINGS.TradesReservedTimeOut()
    
    def ErrorMessage(self):
        return 'Timeout reached before all trades in deal package was set to status {0}'.format(self.STATUS)

class TradesReserved(EnsureTradesInStatus):
    STATUS = 'Reserved'

class TradesSimulated(EnsureTradesInStatus):
    STATUS = 'Simulated'


class TradeProgramWorkflow(AsynchronousWorkflow):
    
    @classmethod
    def StateChart(cls):
        return 'Trade Program'
        
    @classmethod
    def Settings(cls):
        return ParameterSettingsCreator.FromRootParameter('TradeProgramWorkflowSettings')
    
    class StateChartDefinition(object):
        DEFINITION = {'Ready': {'Check compliance': 'Checking Compliance'},
                     'Checking Compliance': {'Successful': 'Releasing To Execution',
                                         'Failed': 'Not Compliant'},
                     'Not Compliant': {'Retry compliance check': 'Checking Compliance',
                                       'Approve breaches': 'Releasing To Execution'},
                     'Releasing To Execution': {'Orders ready': 'Ready For Execution'}
                     }
        LAYOUT = ('Reserving Trades,289,-55;'
                'Not Compliant,206,184;Compliance OK,290,-55;'
                'Checking Compliance,206,0;Ready,33,101;'
                'Awaiting Approval,448,63;'
                'Ready For Execution,629,99;'
                'Releasing To Execution,419,100;'
                 )
    
    @classmethod
    def StartUp(cls):
        cls._Connect()
        
    def SubjectName(self):
        return self.Subject().InstrumentPackage().Name() if self.Subject() is not None else None

    def Trades(self):
        return LinkedTrades(self.Subject())
    
    def OnTimeout(self, *args, **kwargs):
        self.HandleError(kwargs['errorMessage'])
    
    # ------------------------------- Compliance checks -------------------------------------               
       
    def EnsureTradesAreUpdated(self, *args):
        self.StartCheckingCompliance(trades=self.Trades())
    
    @staticmethod
    def _Alerts(ruleChecks):
        alerts = []
        for ruleCheck in ruleChecks:
            alertGenerator = FAlertGenerator.Create(ruleCheck.AppliedRule())
            alerts.append(alertGenerator.AlertsFromCheck(ruleCheck))
        return alerts
    
    def CreateComplianceReportFile(self, ruleChecks, name):
        alerts = self._Alerts(ruleChecks)
        reportId = FComplianceCheckReport.CreateComplianceReportFile(alerts, name)
        return {'Report': reportId, 'Storage': FComplianceCheckReport.SETTINGS.Storage()}
    
    @Promise(TradesReserved, onRejected=OnTimeout)
    def StartCheckingCompliance(self, trades=None):
        """ Called when all trades are set to Reserved to make sure that all trades are included in the calculation."""
        try:   
            self.ValidateValuationParameters()
            appliedRules = self._FindRelevantAppliedRules(trades)
            ruleChecks = self._RuleChecks(appliedRules)
            parameters = self.CreateComplianceReportFile(ruleChecks, self.BusinessProcess().StringKey())
        
            if self.ComplianceCheckIsNonCompliant(ruleChecks):
                self.HandleNotCompliant(parameters)
            else:
                self._activeEventResult.Event(event=('Successful', parameters))
        except Exception as e:
            self.HandleError(e)
        
    def ComplianceCheckIsNonCompliant(self, ruleChecks):
        return self._AnyErrorsInRuleChecks(ruleChecks) or self._AnyNonCompliantThresholdsBreached(ruleChecks)
    
    def HandleNotCompliant(self, parameters):
        """ Sets the orders back to Inactive and then moves the State Chart after all trades are in status Simulated."""
        self.UpdateOrderState(state='Inactive')
        self.MoveToNotCompliant(parameters=parameters, trades=self.Trades())
        
    @Promise(TradesSimulated, onRejected=OnTimeout)
    def MoveToNotCompliant(self, parameters=None, **kwargs):
        self._activeEventResult.Event(event=('Failed', parameters))
        
    @ActionState
    def CheckingCompliance(self):
        """ Sets the orders to Indication and then waits until the trades are status Reserved 
            before performing the compliance check."""
        eventResult = self.AsynchEventResult()
        self.UpdateOrderState(state='Indication', continueWith=self.EnsureTradesAreUpdated)
        return eventResult
    
    @classmethod
    def _FindRelevantAppliedRules(cls, trades):
        portfolios = FComplianceRulesUtils.AllPortfoliosForTrades(trades)
        return chain.from_iterable(FComplianceRulesUtils.GetAppliedRules(portfolio) for portfolio in portfolios)
    
    @staticmethod
    def _RuleChecks(appliedRules):
        ruleChecks = []
        for appliedRule in appliedRules:
            LOGGER.debug('Checking rule "{0}" for {1}'.format(appliedRule.ComplianceRule().Name(), appliedRule.Target().Name()))
            if not appliedRule.Inactive():
                ruleChecks.append(appliedRule.Check())
        return ruleChecks
            
    @staticmethod
    def _AnyErrorsInRuleChecks(ruleChecks):
        return any(bool(ruleCheck.Errors()) for ruleCheck in ruleChecks)
    
    @staticmethod
    def _BreachedThresholdTypes(ruleChecks):
        breaches = list(chain.from_iterable(ruleCheck.Breaches() for ruleCheck in ruleChecks)) #flatten list
        return set(breach.Threshold().Type().Name() for breach in breaches)

    @classmethod
    def _AnyNonCompliantThresholdsBreached(cls, ruleChecks):
        nonCompliantThresholdTypes = list(SETTINGS.NonCompliantThresholdTypes())
        return any(type in nonCompliantThresholdTypes for type in cls._BreachedThresholdTypes(ruleChecks))
    
    @staticmethod
    def ValidateValuationParameters():
        param = acm.GetFunction('mappedValuationParameters', 0)().Parameter()
        assert param.IncludeReservedTrades() == 1, 'Trades in Reserved Status must be included in valuation to do compliance check'
            
    # -------------------------------- Update orders ----------------------------------
    
    @ActionState
    def ReleasingToExecution(self):
        eventResult = self.AsynchEventResult()
        self.UpdateOrderState(state='Pending', continueWith=self.UpdateEventResult)
        return eventResult
    
    def UpdateEventResult(self, orders):
        self._activeEventResult.Event(event='Orders ready')
        if SETTINGS.AutoBulkOrders():
            self._BulkOrders(orders=orders) 
            
    def UpdateOrderState(self, state=None, continueWith=None):
        orderIds, orderQuery = self._OrderIdsAndQuery()
        self.GetOrdersAndUpdateState(orderIds=orderIds, orderQuery=orderQuery,
                                    state=state, continueWith=continueWith)
    
    class MultiOrderWorkflowListener(FOrderUtils.MultiOrderSenderListener):
        
        def __init__(self, orders, workflow, continueWith):
            FOrderUtils.MultiOrderSenderListener.__init__(self, orders)
            self._workflow = workflow
            self._continueWith = continueWith
        
        def HandleSuccess(self):
            self._continueWith(self._orders)
            
        @AsynchronousCall
        def HandleError(self, errorMessage):
            self._workflow.HandleError(errorMessage)
    
    @Promise(FOrderUtils.EnsureOrdersInClient, onRejected=OnTimeout)
    def GetOrdersAndUpdateState(self, orderQuery=None, state=None, continueWith=None, **kwargs):
        orders = orderQuery.AsArray()
        for order in orders:
            FOrderUtils.SetSalesState(order, state)
        listener = self.MultiOrderWorkflowListener(orders, self, continueWith)
        FOrderUtils.MultiOrderSender(orders, listener).SendAsync()

        
    def _OrderIdsAndQuery(self):
        self._Connect()
        orderIds = [trade.OptionalKey() for trade in self.Trades()]
        orderQuery = FOrderUtils.GetSalesOrderQuery(orderIds)
        return orderIds, orderQuery
            
    @Promise(FOrderUtils.EnsureOrdersCanBeSent)
    def _BulkOrders(self, orders=None):
        for bulkable in acm.Trading.GetBulkableCollections(orders):
            bulkedOrder = self._CreateBulkOrder(bulkable)
            FOrderUtils.OrderSender(bulkedOrder).SendAsync() 
            
    @staticmethod
    def _CreateBulkOrder(orders):
        if orders:
            bulkedOrder = acm.Trading.CreateBulkOrder(orders)
            order = orders[0]
            bulkedOrder.SalesPerson(order.SalesPerson())
            bulkedOrder.UserId(order.UserId())
            FOrderUtils.SetSalesState(bulkedOrder, order.SalesState())
            return bulkedOrder
    
    @classmethod
    def _Connect(cls):
        market = FOrderUtils.GetPrimaryMarket()
        mktService = acm.FMarketService(market)
        if not market.IsConnected():
            if not mktService.Connect(5000):
                raise Exception('Failed to connect to market "{0}". Please check "{0}" FExtensionValue on the workflow ATS context "{1}"'
                                        .format(market.Name(), acm.GetDefaultContext().Name()))
   
   
class TradeProgramWorkflowAdvanced(TradeProgramWorkflow):
    
    """ Works the same way as TradeProgramWorkflow but requires an additional manual approval step after
        the compliance check before the orders may be traded. Also contains functionality for redoing a compliance
        check after the program has been traded. """
    
    @ActionState
    def RecheckingCompliance(self):
        eventResult = self.AsynchEventResult()
        self.UpdateOrderState(state='Hold', continueWith=self.RedoComplianceCheck)
        return eventResult
    
    def RedoComplianceCheck(self, *args):
        """ Called when all trades are set to Reserved to make sure that all trades are included in the calculation."""
        results = self.ComplianceCheck(self.Trades())
        parameters = self.ComplianceCheckReportFile(results, self.BusinessProcess().StringKey())
        if self.ComplianceCheckIsNonCompliant(results):
            self._activeEventResult.Event(event=('Failed', parameters))
        else:
            self._activeEventResult.Event(event=('Successful', parameters))
    
    @classmethod
    def StateChart(cls):
        return 'Trade Program Advanced'
    
    class StateChartDefinition(object):
        DEFINITION = {'Ready': {'Check compliance': 'Checking Compliance'},
                     'Checking Compliance': {'Successful': 'Awaiting Approval',
                                         'Failed': 'Not Compliant'},
                     'Not Compliant': {'Retry compliance check': 'Checking Compliance',
                                       'Approve breaches': 'Awaiting Approval'},
                     'Awaiting Approval': {'Approve for trading': 'Releasing To Execution',
                                           'Redo Compliance Check': 'Checking Compliance'},
                     'Releasing To Execution': {'Orders ready': 'Ready For Execution'},
                     'Ready For Execution':    {'Redo Compliance Check': 'Rechecking Compliance'},
                     'Rechecking Compliance':     {'Successful': 'Releasing To Execution',
                                                'Failed': 'Recheck Not Compliant'},
                     'Recheck Not Compliant':     {'Approve breaches': 'Releasing To Execution',
                                                   'Retry Compliance check': 'Rechecking Compliance'},
                     }
        LAYOUT = ('Ready,0,0;'
                  'Checking Compliance,200,0;'
                  'Not Compliant,200,200;'
                  'Awaiting Approval,420,0;'
                  'Ready For Execution,850,200;'
                  'Releasing To Execution,650,200;'
                  'Recheck Not Compliant,650,0;'
                  'Rechecking Compliance,850,0;'
                 )
