import acm
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params


class DDM_LEG_BUILDER():
    
    #Locals
    calcSpace = None
    legSheetColumns = None
    
    #Constructor
    def __init__(self):
        if params.includeDynamicAttributes:
            #Create the calculation space if dynamic attributes is required
            self.calcSpace = acm.FCalculationSpace('FPortfolioSheet')
            
            #Load the leg sheet columns
            legSheet = helper.getWorkbookSheet(params.dynamicAttributesWorkbookName, params.legSheetName)
            self.legSheetColumns = helper.getSheetColumns(legSheet)
            
    
    #Create a single leg xml element by using a calculation space 
    def createElementByLeg(self, trade, leg):
        try:
            #Create the leg return element
            legElement = Element('leg')
            
            #Fetch the static atributes
            if bool(params.includeStaticAttributes):
                staticAttributes = self.getStaticAttributes(leg)
                helper.addAttributesToElement(legElement, staticAttributes)
            
            #Fetch the dynamic attributes
            if bool(params.includeDynamicAttributes):
                #get the trade sheet attributes
                legSheetAttributes = helper.getSheetColumnValues(self.calcSpace, self.legSheetColumns, trade)
                helper.addAttributesToElement(legElement, legSheetAttributes)
                
            
            #Return the XML element
            return legElement
            
        except Exception, error:
            raise Exception('Could not create the leg element. %s' % str(error))
            
    #Create a single leg element by using a pre-built report
    def createElementByLegReport(self, trade, leg, legReport):
        try:
            #Create the leg return element
            legElement = Element('leg')
            
            #Fetch the static atributes
            if bool(params.includeStaticAttributes):
                staticAttributes = self.getStaticAttributes(leg)
                helper.addAttributesToElement(legElement, staticAttributes)
            
            #Fetch the dynamic attributes
            if bool(params.includeDynamicAttributes) and legReport:
                #get the dymanic attributes from the passed leg report
                reportAttributes = acm.FDictionary()
                parentLegElement = fromstring(legReport)
                for childLegElement in parentLegElement:
                    if childLegElement.tag <> 'legNumber':
                        #remove hash values from the calculated values
                        tagValue = ''
                        if childLegElement.text:
                            #Remove comma's and hashes from the values
                            tagValue = childLegElement.text.replace('#', '')
                            tagValue = tagValue.replace(',', '')
                        #add the value
                        reportAttributes[childLegElement.tag] = tagValue
                helper.addAttributesToElement(legElement, reportAttributes)
            
            #Return the XML element
            return legElement
            
        except Exception, error:
            raise Exception('Could not create the leg element. %s' % str(error))
    
            
    def getStaticAttributes(self, leg):
        try:
        
            attributes = acm.FDictionary()
            
            #currency
            if leg.Currency():
                attributes['currencyName'] = leg.Currency().Name()
                attributes['currencyNumber'] = leg.Currency().Oid()
            
            #currentSpread
            attributes['currentSpread'] = leg.Spread()
            
            
            #dayCountMethod
            attributes['dayCountMethod'] = leg.DayCountMethod()
            
            #floatRateReference
            if leg.FloatRateReference():
                attributes['floatRateReferenceName'] = leg.FloatRateReference().Name()
                attributes['floatRateReferenceAddress'] = leg.FloatRateReference().Oid()
            
            #legNumber
            attributes['legNumber'] = leg.Oid()
            
            #legType
            if leg.LegType():
                attributes['legType'] = leg.LegType()
            
            #payLeg
            attributes['payLeg'] = leg.PayLeg()
                
            #payReceive
            if leg.PayLeg():
                attributes['payReceive'] = 'Pay'
            else:
                attributes['payReceive'] = 'Receive'
                
            #rollingPeriod
            attributes['rollingPeriod'] = leg.RollingPeriod()
            
            #rollingPeriodCount
            attributes['rollingPeriodCount'] = leg.RollingPeriodCount()
            
            #rollingPeriodUnit
            attributes['rollingPeriodUnit'] = leg.RollingPeriodUnit()
            
            return attributes
                  
        except Exception, error:
            raise Exception('Could not get the leg static attributes. %s' % str(error))
        
    
'''
#Unit test
trade = acm.FTrade[12842617]
legElementBuilder = DDM_LEG_BUILDER()
for leg in trade.Instrument().Legs():
    legElement =legElementBuilder.createElement(trade,leg)
    print tostring(legElement)
'''
