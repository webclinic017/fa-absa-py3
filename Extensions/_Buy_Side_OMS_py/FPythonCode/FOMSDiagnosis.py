""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FOMSDiagnosis.py"
"""--------------------------------------------------------------------------
MODULE
    FOMSDiagnosis

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    OMS Diagnosis Tool is used to verify that basic OMS workfow is working properly. 
    If some parts of the workflow are failing, it points to the malfunctioning 
    component (e.g. Internal Market related issue)

-----------------------------------------------------------------------------"""

import acm
import FOrderUtils
import FTradeProgram
import FTradeToOrder
import time
import FLogger
from FParameterSettings import ParameterSettingsCreator

logger = FLogger.FLogger(name = 'OMS Diagnosis:')

def IsConnectedToIM():
    market = FOrderUtils.GetPrimaryMarket()
    return market.IsConnected()

def Create_candidate_trade(object):
    trade = acm.DealCapturing.CreateNewTrade(object.stock)
    trade.Portfolio(object.portfolio)
    trade.Quantity(object.quantity)
    trade.Price(object.price)
    trade.Acquirer(object.acquirer)
    return trade

_FPARAMETER_ATTRIBUTES = (
        ("Not Connected to Primary Internal Market", "Connected to Primary Internal Market"),
        ("Order Program Not Created!", "Order Program Created"),
        ('Deal Package not Created!', 'Deal Package Created'),
        ("Found only {0} out of {1} reserved trades!", "Mirror Trades Created"),
        ('No Trade Program business process found for deal package {0}!', 'Business Process "Trade Program" created'),
        ("Sales Order not in Released for Execution state but in '{}' state!", "Sales Order Released for Execution"),
        ("Fill trade not created!", "Fill Trades Properly Created"),
        ("", "BSOMS Workflow Successfully Executed. All Components are Working Properly")
)

class BSOMSDiagnosis():
    def __init__(self):
        self._conected_to_market = [0, '']
        self._order_program_created = [0, '']
        self._deal_package_created = [0, '']
        self._mirror_trade_created = [0, '']
        self._business_process_created = [0, '']
        self._sales_order_released_ex = [0, '']
        self._fill_trades_properly_created = [0, '']
        self._bsmos_workflow_successfully = [0, '']
        self._progress_aims = 0
        self._progress_ats = 0
        self._progress_tab = 0
        self._aims = 0
        self._ats = 0
        self._tab = 0
        self._settings = ParameterSettingsCreator.FromRootParameter('BSOMSDiagnosisSettings')
        self._aims_time = self._settings.Aims_time()
        self._ats_time = self._settings.Ats_time()
        self._tab_time = self._settings.Tab_time()
        self.quantity = 1100
        self.price = 9
        self.stock = None
        self.portfolio = None
        self.cpty = None
        self.acquirer = None
        self.bp = None
        self.orderProgram = None
        self.trades = acm.FArray()
        self.trades.AddDependent(self)
        self.dp = acm.FArray()
        self.dp.Add(acm.FDealPackage())
        self.dp.AddDependent(self)
        self._pos = 0
        self._time = 0
    
    def TabWork(self):
        if self._progress_tab == 0 and self._tab == 0:
            return 'Start'
        elif self._progress_tab == 100 and self._tab == 1:
            return 'Yes'
        elif self._progress_tab == 100 and self._tab == 0:
            return 'No'
        else:
            return 'Undefine'
            
    def AtsWork(self):
        if self._progress_ats == 0 and self._ats == 0:
            return 'Start'
        elif self._progress_ats == 100 and self._ats == 1:
            return 'Yes'
        elif self._progress_ats == 100 and self._ats == 0:
            return 'No'
        else:
            return 'Undefine'       
            
    def AimsWork(self):
        if self._progress_aims == 0 and self._aims == 0:
            return 'Start'
        elif self._progress_aims == 100 and self._aims == 1:
            return 'Yes'
        elif self._progress_aims == 100 and self._aims == 0:
            return 'No'
        else:
            return 'Undefine'
    
    def NextStep(self):
        self._pos = self._pos + 1
    
    def DeleteObject(self, *args):
        for object in args:
            if hasattr(object, '__iter__'):
                    for obj in object:
                        if 'Delete' in dir(obj):
                            obj.Delete()
            else:
                if 'Delete' in dir(object):
                    object.Delete()
                    
    def DeleteCreatedObject(self):
        object_list = [self.bp, self.dp[0]]
        for obj in object_list:
            if obj:
                self.DeleteObject(obj)
        
    def LoadObejcts(self):
        self.portfolio = acm.FPhysicalPortfolio[self._settings.Default_Portfolio()]
        self.stock = acm.FStock[self._settings.Default_Stock()]
        self.cpty = acm.FParty[self._settings.Default_Cpty()]
        self.acquirer = acm.FInternalDepartment[self._settings.Default_Acquirer()]
    
    def BPCurrentStepName(self):
        return self.bp.First().CurrentStep().State().Name()
    
    def StepMessage(self, index, param_first=None, param_second=None):
        _att_list = ('_conected_to_market',  '_order_program_created', 
        '_deal_package_created', '_mirror_trade_created', 
        '_business_process_created', '_sales_order_released_ex', 
        '_fill_trades_properly_created', '_bsmos_workflow_successfully')
        msg = _FPARAMETER_ATTRIBUTES[self._pos][index]
        msg = msg.format(param_first, param_second)
        exec('self.' + _att_list[self._pos] + '[0] = index')
        exec('self.' + _att_list[self._pos] + '[1] = ">" + msg')
        if index:
            logger.info(msg)
            return
        logger.error(msg)
    
    def ProgressValue(self):
        _value_list = ((50, 0, 0, 1, 0, 0), (100, 0, 0, 1, 0, 0), (100, 0, 10, 1, 0, 0),
        (100, 0, 25, 1, 0, 0), (100, 0, 50, 1, 0, 0), (100, 100, 50, 1, 1, 0),
        (100, 100, 100, 1, 1, 1))
        _message_list = ('', '', 'AIMS IS WORKING', '', '', 'WORKFLOW ATS IS WORKING', 'TAB IS WORKING')
        self._progress_aims = _value_list[self._pos][0]
        self._progress_ats = _value_list[self._pos][1]
        self._progress_tab = _value_list[self._pos][2]
        self._aims = _value_list[self._pos][3]
        self._ats = _value_list[self._pos][4]
        self._tab = _value_list[self._pos][5]
        if _message_list[self._pos] != '':
            logger.info(_message_list[self._pos])
            
    def ProgressValueError(self):
        _value_list = ((100, 0, 0, 0, 2, 2), (100, 0, 0, 0, 0, 0), (100, 0, 100, 0, 0, 0),
        (100, 0, 100, 1, 0, 0), (100, 0, 100, 1, 0, 0), (100, 100, 99, 1, 0, 0),
        (100, 100, 100, 1, 0, 0)
        )
        _message_list_error = ('', 'AIMS RELATED ISSUE!', 'TAB RELATED ISSUE!', 
        'TAB RELATED ISSUE!', 'TAB RELATED ISSUE!', 'WORKFLOW ATS RELATED ISSUE!',
        'TAB RELATED ISSUE!')
        self._progress_aims = _value_list[self._pos][0]
        self._progress_ats = _value_list[self._pos][1]
        self._progress_tab = _value_list[self._pos][2]
        self._aims = _value_list[self._pos][3]
        self._ats = _value_list[self._pos][4]
        self._tab = _value_list[self._pos][5]
        if _message_list_error[self._pos] != '':
            logger.error(_message_list_error[self._pos])
    
    def GetOrdersFromOrderProgram(self):
        orders_handler = self.orderProgram.GetOrders()
        while not orders_handler.IsCompleted():
            pass
        return orders_handler.Result()
        
    def ServerUpdate(self, sender, aspect, param):
        funct = {1: self.WaitUntilAimsTimeOrderProgramInactive, 2:self.WaitUntilAimsTimeDealPackage, 
            3:self.WaitUntilTabTime, 6: self.WaitUntilTabTimeFillOrder}
        if aspect == acm.FSymbol('insert'):
            if self._pos in funct.keys():
                funct[self._pos]()
        
    def InitTime(self):
        self._time = time.time()
    
    def WaitUntilAimsTimeDealPackage(self):
        if (time.time()-self._time < self._aims_time) and (self.dp[0].Oid() < 0): 
            self.dp[0] = acm.FDealPackage[self.orderProgram.Id()] if acm.FDealPackage[self.orderProgram.Id()] else acm.FDealPackage()
    
    def WaitUntilAimsTimeOrderProgramInactive(self):
        if (time.time() - self._time < self._aims_time) and (self.dp[0].Oid() < 0) and (self.orderProgram.IsOrderProgramActive() is False):
            self.dp[0] = acm.FDealPackage[self.orderProgram.Id()] if acm.FDealPackage[self.orderProgram.Id()] else acm.FDealPackage()
        
    def WaitUntilTabTimeFillOrder(self):
        if (time.time()-self._time < self._tab_time) and self.trades.Size() != 1:
            self.trades = acm.FTrade.Select('orderUuid={}'.format(orderId)) if acm.FTrade.Select('orderUuid={}'.format(orderId)) else acm.FArray()
    
    def WaitUntilTabTime(self):
        while (time.time()-self._time) < self._tab_time:
            pass

    def WaitUnitAtsTimeNotReadyForExecution(self):
        self.InitTime()
        while ((time.time()-self._time < self._ats_time ) and self.BPCurrentStepName() != "Ready For Execution" ):
            self._progress_ats = int((time.time()-self._time)*2.5)
    
    def SucessPassStep(self):
        self.StepMessage(1)
        self.ProgressValue()
        self.NextStep()
    
    def IsNotConnectedToPrimaryMarket(self):
        if IsConnectedToIM() is True:
            self.SucessPassStep()
        else:
            self.StepMessage(0)
            self.ProgressValueError()
            return 1

    def OrderProgramCreationCheck(self):
        self.LoadObejcts()
        self.candTrade = Create_candidate_trade(self)
        OPName = 'OMSDiagnosis_{0}'.format(acm.Time.TimeNow())
        self.orderProgram = FTradeToOrder.CreateOrderProgramFromTrades([self.candTrade], OPName, 'Inactive')
        FOrderUtils.OrderProgramSender(self.orderProgram, None).SendAsync()
        self.InitTime()
        self.WaitUntilAimsTimeOrderProgramInactive()
        if self.orderProgram.IsOrderProgramActive() is True:
            self.SucessPassStep()
            self.DealPackageCreationCheck()
        else:
            self.DeleteObject(self.stock.Trades())
            self.DeleteCreatedObject()
            self.StepMessage(0)
            self.ProgressValueError()
            return
    
    def DealPackageCreationCheck(self):
        self.InitTime()
        self.WaitUntilAimsTimeDealPackage()
        if self.dp[0].Oid() > 0:
            self.bp = acm.BusinessProcess.FindBySubjectAndStateChart(self.dp[0], 'Trade Program')
            self.SucessPassStep()
            self.MirrorTradesCreationCheck()
        else:
            self.StepMessage(0)
            self.DeleteObject()
            self.DeleteObject(self.stock.Trades())
            self.ProgressValueError()
            self._mirror_trade_created[0] = 0
            self._mirror_trade_created[1] = "> " + 'TAB related issue!'

    def MirrorTradesCreationCheck(self):
        self.InitTime()
        self.WaitUntilTabTime()
        self.trades = FTradeProgram.LinkedTrades(self.dp[0])
        orders = self.GetOrdersFromOrderProgram()
        if len(self.trades) == len(orders):
            self.SucessPassStep()
            self.BusinessProcessCreationCheck()
        else:
            self.StepMessage(0, len(self.trades), len(orders))
            self.ProgressValueError()
            self.DeleteCreatedObject()
            return
    
    def BusinessProcessCreationCheck(self):
        if self.bp:
            self.SucessPassStep()
            self.SalesOrderStatusReadyForExecutionCheck()
        else:
            self.StepMessage(0, self.dp[0].Name())
            self._business_process_created[0] = 0
            self._business_process_created[1] = "> TAB RELATED ISSUE!"
            self.ProgressValueError()
            self.trades[0].Delete()
            self.DeleteCreatedObject()
            return
    
    def SalesOrderStatusReadyForExecutionCheck(self):
        self.WaitUnitAtsTimeNotReadyForExecution()
        if self.BPCurrentStepName() == "Ready For Execution":
            self.SucessPassStep()
            self.FillingOrder()
        else:
            self.StepMessage(0, self.BPCurrentStepName())
            self.ProgressValueError()
            self.trades[0].Delete()
            self.DeleteCreatedObject()
            return
    
    def FillingOrder(self):
        orders = self.GetOrdersFromOrderProgram()
        match_order_handler = FOrderUtils.CreateMatchOrderHandler(orders[0], self.quantity, self.price, self.cpty.Name(), 'Manual Fill', None)
        match_order_handler.Send(None)
        self.InitTime()
        self.WaitUntilTabTimeFillOrder()
        if self.trades.Size() == 1:
            self.SucessPassStep()
        else:
            self.StepMessage(0)
            self.trades[0].Delete() 
            self.DeleteCreatedObject()
            self.ProgressValueError()
            return
        
    def OMSDiagnosis(self, parameter=None):
        if self.IsNotConnectedToPrimaryMarket():
            return
        self.OrderProgramCreationCheck()
        self.trades[0].Delete()
        self.DeleteObject(self.stock.Trades())
        self.DeleteCreatedObject()
        self.StepMessage(1)