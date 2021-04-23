import acm
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params

class DDM_MONEY_FLOW_BUILDER():
    
    #Locals
    calcSpace = None
    moneyFlowSheetColumns = None
    
    #Constructor
    def __init__(self):
        if params.includeDynamicAttributes:
            #Create the calculation space if dynamic attributes is required
            self.calcSpace = acm.FCalculationSpace('FMoneyFlowSheet')
            
            #Load the moneyflow sheet columns
            moneyFlowSheet = helper.getWorkbookSheet(params.dynamicAttributesWorkbookName, params.moneyFlowSheetName)
            self.moneyFlowSheetColumns = helper.getSheetColumns(moneyFlowSheet)
 
    
    #Create a moneyflow xml element
    def createElement(self, moneyFlow):
        try:
            #Create the moneyflow return element
            moneyFlowElement = Element('moneyFlow')
            
            #Fetch the static atributes
            if params.includeStaticAttributes:
                staticAttributes = self.getStaticAttributes(moneyFlow)
                helper.addAttributesToElement(moneyFlowElement, staticAttributes)
            
            #Fetch the dynamic attributes
            if params.includeDynamicAttributes:
                #get the moneyflow sheet attributes
                moneyFlowSheetAttributes = helper.getSheetColumnValues(self.calcSpace, self.moneyFlowSheetColumns, moneyFlow)
                helper.addAttributesToElement(moneyFlowElement, moneyFlowSheetAttributes)
                
            
            #Return the XML element
            return moneyFlowElement
            
        except Exception as error:
            raise Exception('Could not create the moneyFlow element. %s' % str(error))
    
    def getStaticAttributes(self, moneyFlow):
        try:
        
            attributes = acm.FDictionary()
            
            #counterparty
            if moneyFlow.Counterparty():
                attributes['counterpartyName'] = moneyFlow.Counterparty().Name()
                
            #createTime
            if moneyFlow.SourceObject():  
                attributes['createTime'] = helper.isoDateTimeFromInt(moneyFlow.SourceObject().CreateTime()) 
            
            #createUser
            if moneyFlow.SourceObject():
                if moneyFlow.SourceObject().CreateUser():
                    attributes['createUserName'] = moneyFlow.SourceObject().CreateUser().Name()
                    attributes['createUserNumber'] = moneyFlow.SourceObject().CreateUser().Oid()
                
            #currency
            if moneyFlow.Currency():
                attributes['currencyName'] = moneyFlow.Currency().Name()
                attributes['currencyNumber'] = moneyFlow.Currency().Oid()
            
            #legNumber, cashflowNumber and reset number
            if moneyFlow.SourceObject().IsKindOf('FCashFlow'):
                if moneyFlow.SourceObject().Leg():
                    attributes['legNumber'] = moneyFlow.SourceObject().Leg().Oid()
                attributes['cashflowNumber'] = moneyFlow.SourceObject().Oid()
                
            elif moneyFlow.SourceObject().IsKindOf('FReset'):
                attributes['resetNumber'] = moneyFlow.SourceObject().Oid()
                if moneyFlow.SourceObject().CashFlow():
                    attributes['cashflowNumber'] = moneyFlow.SourceObject().CashFlow().Oid()
                if moneyFlow.SourceObject().Leg():
                    attributes['legNumber'] = moneyFlow.SourceObject().CashFlow().Leg().Oid()
            elif moneyFlow.SourceObject().IsKindOf('FMoneyFlow'):
                 raise Exception('MoneyFlow Type found!!')
            
            
            #payDate
            attributes['payDate'] = moneyFlow.PayDate()
            
            #text
            if moneyFlow.SourceObject().IsKindOf('FPayment'):
                attributes['text'] =moneyFlow.SourceObject().Text()
            
            #type - fetch type from the sheet as exension attribute
            #attributes['type'] = moneyFlow.Type()
                
            #updateTime
            if moneyFlow.SourceObject():
                attributes['updateTime'] =helper.isoDateTimeFromInt(moneyFlow.SourceObject().UpdateTime())  
            
            #updateUser
            if moneyFlow.SourceObject():
                if moneyFlow.SourceObject().UpdateUser():
                    attributes['updateUserName'] = moneyFlow.SourceObject().UpdateUser().Name()
                    attributes['updateUserNumber'] = moneyFlow.SourceObject().UpdateUser().Oid()
             
            return attributes
                  
        except Exception as error:
            raise Exception('Could not get the money flow static attributes. %s' % str(error))
        
    
'''
#Unit test
trade = acm.FTrade[12842617]
moneyFlowElementBuilder = DDM_MONEY_FLOW_BUILDER()
for mf in trade.MoneyFlows(None,None):
    moneyFlowElement =moneyFlowElementBuilder.createElement(mf)
    print tostring(moneyFlowElement)

'''
