
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_MF
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade moneyflow data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
from datetime import datetime
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_DATA_BASE

#*********************************************************#
#Static Creator method for all legs of a trade (not use self)
#*********************************************************#
worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_MONEYFLOW
def CreateAllForTrade(reportDate, trade, historicalCashflowRange):
    global worksheetName
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)

    """if trade.Oid() in (87083353,87083354):
        worksheetName = 'FC_TRADE_MONEYFLOW_OVERRIDE'
    else:"""
    worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_MONEYFLOW
        
    tradeMoneyflows = []
    moneyflowTreeProxys = FC_DATA_BASE.GetTopLevelNodeChildrenTreeProxies(worksheetName, trade)
    for moneyflowTreeProxy in moneyflowTreeProxys:
        moneyflow = FC_DATA_TRD_MF(worksheetName, moneyflowTreeProxy)
        #cast the reportDate as a datetime
        reportDateTime = FC_UTILS.dateFromISODateTimeString(reportDate)
        #Current
        if moneyflow.PayDate == reportDateTime:
            moneyflow.PayDateType = 'C'
        #Historical
        elif moneyflow.PayDate < reportDateTime:
            moneyflow.PayDateType = 'H'
        #Future
        elif moneyflow.PayDate > reportDateTime:
            moneyflow.PayDateType = 'F' 
            
        #Test historical cashflows for exclusion
        includeMoneyflow = True
        if historicalCashflowRange>-1:
            if moneyflow.SourceObject.IsKindOf(UTILS.Constants.fcGenericConstants.FCASHFLOW):
                updateTime = FC_UTILS.dateTimeFromInt(moneyflow.SourceObject.UpdateTime())
                delta = reportDateTime - updateTime
                #Rule = exclude historical cashflows not updated more than inclusiveDays ago
                if moneyflow.PayDateType=='H' and delta.days > historicalCashflowRange:
                    includeMoneyflow = False
                    
        #finally add the moneyflow
        if bool(includeMoneyflow):
            tradeMoneyflows.append(moneyflow)
    return tradeMoneyflows
    
#*********************************************************#
#Class definition
#*********************************************************#
class FC_DATA_TRD_MF(FC_DATA_BASE.FC_DATA_BASE): 
    
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FMoneyflow - get from the fTree proxy to ensure the same object is used
    @property
    def FMoneyflow(self):
        return self.GetFObject()
        
    #PayDate
    @property
    def PayDate(self):
        if self.FMoneyflow:
            return datetime.strptime(self.FMoneyflow.PayDate(), '%Y-%m-%d')
    
    #PayDateType
    @property
    def PayDateType(self):
        return self._payDateType
    
    @PayDateType.setter
    def PayDateType(self, value):
        self._payDateType = value
        
        
    #SourceObject
    @property
    def SourceObject(self):
        if self.FMoneyflow:
            return self.FMoneyflow.SourceObject()
    
    #SourceObjectType
    @property
    def SourceObjectType(self):
        if self.SourceObject:
            return str(self.SourceObject.ClassName())
    
    #SourceObjectNumber
    @property
    def SourceObjectNumber(self):
        if self.SourceObject:
            #legNumber, cashflowNumber and reset number - dont like this...!!!!
            if self.FMoneyflow.SourceObject().IsKindOf(UTILS.Constants.fcGenericConstants.FCASHFLOW):
                if self.FMoneyflow.SourceObject().Leg():
                    return self.FMoneyflow.SourceObject().Leg().Oid()
            elif self.FMoneyflow.SourceObject().IsKindOf(UTILS.Constants.fcGenericConstants.FRESET):
                if self.FMoneyflow.SourceObject().CashFlow():
                   return self.FMoneyflow.SourceObject().CashFlow().Oid()
                if self.FMoneyflow.SourceObject().Leg():
                   return self.FMoneyflow.SourceObject().CashFlow().Leg().Oid()
            elif self.FMoneyflow.SourceObject().IsKindOf(UTILS.Constants.fcGenericConstants.FMONEYFLOW):
                return  0
            elif self.FMoneyflow.SourceObject().IsKindOf(UTILS.Constants.fcGenericConstants.FTRADE):
                return  self.FMoneyflow.SourceObject().Oid()
            else:
                return  0
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, worksheetName, fMoneyflowTreeProxy):
        #Construct the base class
        FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
        
        
        #Get an FTreeProxy
        if not fMoneyflowTreeProxy:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FMONEYF_TREEPROXY_MUST_BE_PROVIDED)
        else:
            self._fTreeProxy = fMoneyflowTreeProxy
       
            
    #**********************************************************#
    #Methods
    #*********************************************************#
    
    #GetFObject override 
    def GetFObject(self):
        try:
            if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().MoneyFlow():
                return self._fTreeProxy.Item().MoneyFlow()
        except:
            return None


