import acm
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params

class DDM_INSTRUMENT_BUILDER():
    
    #Locals
    calcSpace = None
    instrumentSheetColumns = None
    
    #Constructor
    def __init__(self):
        if params.includeDynamicAttributes:
            #Create the calculation space if dynamic attributes is required
            self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')
            
            #Load the instrument sheet columns
            instrumentSheet = helper.getWorkbookSheet(params.dynamicAttributesWorkbookName, params.instrumentSheetName)
            self.instrumentSheetColumns = helper.getSheetColumns(instrumentSheet)
 
    
    #Create a instrument xml element
    def createElement(self, instrument):
        try:
            #Create the return element
            instrumentElement = Element('instrument')

            #Fetch the static atributes
            if params.includeStaticAttributes:
                staticAttributes = self.getStaticAttributes(instrument)
                helper.addAttributesToElement(instrumentElement, staticAttributes)
            
            #Fetch the dynamic attributes
            if params.includeDynamicAttributes:
                #get the instrument sheet attributes
                instrumentSheetAttributes = helper.getSheetColumnValues(self.calcSpace, self.instrumentSheetColumns, instrument)
                helper.addAttributesToElement(instrumentElement, instrumentSheetAttributes)
                
            
            #Return the XML element
            return instrumentElement
        except Exception as error:
            raise Exception('Could not create the instrument element. %s' % str(error))
    
    def getStaticAttributes(self, instrument):
        try:
        
            attributes = acm.FDictionary()
            
            #contractSize
            attributes['contractSize'] = helper.formatNumber(instrument.ContractSize())
            
            #createTime
            attributes['createTime'] = helper.isoDateTimeFromInt(instrument.CreateTime())
            
            #createUser
            if instrument.CreateUser():
                attributes['createUserName'] = instrument.CreateUser().Name()
                attributes['createUserNumber'] = instrument.CreateUser().Oid()
                
            #currency
            if instrument.Currency():
                attributes['currencyName'] = instrument.Currency().Name()
                attributes['currencyNumber'] = instrument.Currency().Oid()
      
            #expiryDate
            attributes['expiryDate'] = helper.dateFromDateTimeString(instrument.ExpiryDate())
            
            #expiryPeriod
            attributes['expiryPeriod'] = instrument.ExpiryPeriod()
            
            #expiryPeriodCount
            attributes['expiryPeriodCount'] = instrument.ExpiryPeriod_count()
            
            #expiryPeriodUnit
            attributes['expiryPeriodUnit'] = instrument.ExpiryPeriod_unit()
            
            #expiryTime
            attributes['expiryTime'] = instrument.ExpiryTime()
            
            #instrumentAddress
            attributes['instrumentAddress'] = instrument.Oid()
            
            #instrumentName
            attributes['instrumentName'] = instrument.Name()
            
            #instrumentType
            attributes['instrumentType'] = instrument.InsType()
            
            #isin
            attributes['isin'] = instrument.Isin()
            
            #issuer
            if instrument.Issuer():
                attributes['issuerName'] = instrument.Issuer().Name()
                attributes['issuerNumber'] = instrument.Issuer().Oid()
            
            #payType
            attributes['payType'] = instrument.PayType()
            
            #settlementType
            attributes['settlementType'] = instrument.SettlementType()
            
            #startDate
            attributes['startDate'] =instrument.StartDate()
            
            #updateTime
            attributes['updateTime'] = helper.isoDateTimeFromInt(instrument.UpdateTime()) 
            
            
            #updateUser
            if instrument.UpdateUser():
                attributes['updateUserName'] = instrument.UpdateUser().Name()
                attributes['updateUserNumber'] = instrument.UpdateUser().Oid()
                
            #valuationGroup
            if instrument.ValuationGrpChlItem():
                attributes['valuationGroupName'] = instrument.ValuationGrpChlItem().Name()
                attributes['valuationGroupNumber'] = instrument.ValuationGrpChlItem().Oid()
            
            return attributes
                  
        except Exception as error:
            raise Exception('Could not get the trade static attributes. %s' % str(error))
        
'''   

#Unit test
trade = acm.FTrade[12842617]
instrumentElementBuilder = DDM_INSTRUMENT_BUILDER()
instrumentElement = instrumentElementBuilder.createElement(trade.Instrument())
print tostring(instrumentElement)
'''
