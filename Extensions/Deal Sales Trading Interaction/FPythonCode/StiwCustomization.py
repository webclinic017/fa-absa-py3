import acm
from RFQUtils import Status
from SalesTradingCustomizations import OrderBookCreation, DefaultSalesPortfolio
 
COMPLETED_REQUEST_STATES = [
    'Accepted',
    'Expired',
    'Quote Expired',
    'Quote Rejected',
    'Request Cancelled']

'''********************************************************************
* Return default notification settings
********************************************************************'''  
def DefaultNotificationSettings():
    settings = {}
    settings['Role'] = 'Sales'
    settings['DefaultStatuses'] = Status.Default(settings['Role'])
    settings['EnabledByDefault'] = False
    return settings


def SalesPortfolio():
    return DefaultSalesPortfolio() 
    
'''********************************************************************
* Filters
********************************************************************'''
class Filters(object):
    
    @classmethod
    def Underlyings(cls):
        return None
        
    @classmethod
    def TradeSheet(cls, client, underlying=None):
        return Filters.PortfolioSheet(client, underlying)
    
    @classmethod
    def PortfolioSheet(cls, client, underlying=None):
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        if client:
            portfolioName = str(SalesPortfolio().Name())
            folderName = '%s / %s' %(portfolioName, str(client.Name()))
            
            query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolioName)
            query.AddAttrNode('Counterparty.Name', 'EQUAL', client.Name())
            
            if underlying:
                pass
            else:
                folder = acm.FASQLQueryFolder()
                folder.AsqlQuery(query)
                folder.Name(folderName)                
        else:
            folder = acm.FASQLQueryFolder()
            query.AddAttrNode('Oid', 'EQUAL', 0)
            folderName = 'No Counterparty Selected'
            folder.AsqlQuery(query)
            folder.Name(folderName)
            
        return folder
        
    @classmethod
    def QuoteRequestAdvancedFilter(cls, underlying):
        query = acm.CreateFASQLQuery('FQuoteRequestInfo', 'AND')
        query.AddAttrNodeEnum('Status', COMPLETED_REQUEST_STATES)
        query.AddAttrNodeString('Role', 'Sales', 'EQUAL')
        return query

    @classmethod
    def QuoteRequestPricingSheet(cls, client, underlying=None):
        filter = None
        try:
            if client:
                filter = acm.FQuoteRequestFilter()
                filter.MarketPlaces([Market()])
                filter.Client(client.Name())
                filter.FilterName(client.Name())
                filter.Latest(True)
                filter.AdvancedFilter(Filters.QuoteRequestAdvancedFilter(underlying))
        except Exception as e:
            print(("Quote Request Query filter failed", str(e)))
        return filter
        
    @classmethod   
    def OrderSheet(cls, client, underlying=None):
        orderFilter = acm.FOwnOrderFilter()
        try:
            clientName = client.Name() if client else 'NoCounterpartyCounterpartyName'
            query = acm.CreateFASQLQuery('FOwnOrder', 'AND')
            query.AddAttrNode('Client', 'EQUAL', clientName)        
            orderFilter.OrderRoles([1])
            orderFilter.Query(query)
        except Exception as e:
            print(("Order Sheet filter failed", str(e)))
        return orderFilter

'''********************************************************************
* Market
********************************************************************'''
def Market():
    return acm.FMarketPlace[OrderBookCreation.DefaultMarket(None)]
