import acm
from xml.etree.ElementTree import ElementTree, Element, tostring, fromstring
import DDM_ATS_HELPER as helper
import DDM_ATS_PARAMS as params

class DDM_SALES_CREDITS_BUILDER():
    
    
    #Create a instrument xml element
    def createElement(self, trade):
        try:
            salesCreditCounter=0
            salesCreditsElement = Element('salesCredits')
            
            #Load the built-in sales credit
            if trade.SalesPerson() and trade.SalesCredit():
                salesCreditCounter = salesCreditCounter + 1
                salesCreditElement = Element('salesCredit')
                standardSalesCredit = str(trade.SalesCredit())
                totalValueAddCredit = trade.add_info('ValueAddCredits')
                salesPerson = trade.SalesPerson().Name()
                salesCreditSubTeam = trade.add_info('SalesCreditSubTeam1')
                #Add the attributes
                helper.AddXmlChildElement(salesCreditElement, 'standardSalesCredit', str(standardSalesCredit))
                helper.AddXmlChildElement(salesCreditElement, 'totalValueAddSalesCredit', str(totalValueAddCredit))
                helper.AddXmlChildElement(salesCreditElement, 'salesPerson', str(salesPerson))
                helper.AddXmlChildElement(salesCreditElement, 'salesCreditSubTeam', str(salesCreditSubTeam))
                salesCreditsElement.append(salesCreditElement)
               
                
            #Now the additional info sales credits - WARNING, the might work diffeent when Front gets updated from 2010.2
            salesCreditNo = 2
            totalSalesCredits = 5
            while salesCreditNo <= totalSalesCredits:
                salesPerson = trade.add_info('Sales_Person%s' % salesCreditNo)
                standardSalesCredit = trade.add_info('Sales_Credit%s' % salesCreditNo)
                if salesPerson and str(salesPerson)!='' and standardSalesCredit and str(standardSalesCredit)!='':
                    salesCreditCounter = salesCreditCounter + 1
                    salesCreditElement = Element('salesCredit')
                    totalValueAddCredit = trade.add_info('ValueAddCredits%s' % salesCreditNo)
                    salesCreditSubTeam = trade.add_info('SalesCreditSubTeam%s' % salesCreditNo)
                    #Add the attributes
                    helper.AddXmlChildElement(salesCreditElement, 'standardSalesCredit', str(standardSalesCredit))
                    helper.AddXmlChildElement(salesCreditElement, 'totalValueAddSalesCredit', str(totalValueAddCredit))
                    helper.AddXmlChildElement(salesCreditElement, 'salesPerson', str(salesPerson))
                    helper.AddXmlChildElement(salesCreditElement, 'salesCreditSubTeam', str(salesCreditSubTeam))
                    salesCreditsElement.append(salesCreditElement)
                salesCreditNo = salesCreditNo + 1
            
            #Add the sales credits level attributes (not 5)
            shadowRevenueType = trade.add_info('Shadow_Revenue_Type')
            rwaCounterparty = trade.add_info('RWA_Counterparty')
            relationshipParty = trade.add_info('Relationship_Party')
            countryPortfolio = trade.add_info('Country')
            brokerStatus = trade.add_info('Broker Status')
            #Add the attributes
            
            helper.AddXmlChildElement(salesCreditsElement, 'shadowRevenueType', str(shadowRevenueType))
            helper.AddXmlChildElement(salesCreditsElement, 'rwaCounterparty', str(rwaCounterparty))
            helper.AddXmlChildElement(salesCreditsElement, 'relationshipParty', str(relationshipParty))
            helper.AddXmlChildElement(salesCreditsElement, 'countryPortfolio', str(countryPortfolio))
            helper.AddXmlChildElement(salesCreditsElement, 'brokerStatus', str(brokerStatus))
            
            #return
            return salesCreditsElement, salesCreditCounter
        
        except Exception, error:
            raise Exception('Could not create the sales credits element. %s' % str(error))
    
    
        
    

#Unit test
'''
trade = acm.FTrade[12842617]
salesCreditsElementBuilder = DDM_SALES_CREDITS_BUILDER()
(salesCreditsElement,salesCreditCounter)  = salesCreditsElementBuilder.createElement(trade)
print salesCreditCounter
print tostring(salesCreditsElement)
'''
