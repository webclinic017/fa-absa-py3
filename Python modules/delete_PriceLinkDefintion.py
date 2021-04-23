"""
Date            JIRA                   Author          Change description
07Nov2019       PCGDEV-167             Anil Parbhoo    Script to delete invalid and unused reuters mappings   
this script is not a scheduled as this code will be used only after advising TCU what will be deleted once or twice a year
"""
import acm

dt = acm.Time().DateToday()

pls = acm.FPriceLinkDefinition.Select('')
price_links_count_before = len(pls)

delete_links = []

print 'PriceLinkOid', 'InstrumentName', 'CurrencyName', 'InsType', 'IsInstrumentGeneric', 'ExpiryDateOnly', 'IsPriceLinkNotActive', 'PriceLinkMarketName', 'Delete_Reason'

for price_link in pls:

    ins = price_link.Instrument()

    if ins.InsType() not in ['Stock', 'Curr', 'EquityIndex', 'RateIndex', 'Combination', 'FxSwap', 'Commodity', 'ETF']:
    
        if not ins.Generic():
        
            if ins.ExpiryDateOnly() < dt:
        
                print price_link.Oid(), ins.Name(), ins.Currency().Name(), ins.InsType(), ins.Generic(), ins.ExpiryDateOnly(), price_link.NotActive(), price_link.Market().Name(), 'ExpDate<Today'
                
                delete_links.append(price_link.Oid())
                
                
    if ins.InsType() not in ['Curr', 'RateIndex']:
    
        if price_link.NotActive():
       
            print price_link.Oid(), ins.Name(), ins.Currency().Name(), ins.InsType(), ins.Generic(), ins.ExpiryDateOnly(), price_link.NotActive(), price_link.Market().Name(), 'Not_Active'
            
            delete_links.append(price_link.Oid())
            
    if price_link.Market().Name() in ['SPOT_MID', 'PRICETEST']:

        print price_link.Oid(), ins.Name(), ins.Currency().Name(), ins.InsType(), ins.Generic(), ins.ExpiryDateOnly(), price_link.NotActive(), price_link.Market().Name(), 'Invalid_Market' 

        delete_links.append(price_link.Oid())
        

print '*' * 16       


delete_links = tuple(set(delete_links))

for price_link in delete_links:
    pld = acm.FPriceLinkDefinition[price_link]
    try:
        print pld.Oid(), 'delete pld'
        pld.Delete()
    except:
        print 'could NOT delete', pld.Oid(), pld.Instrument().Name(), pld.Instrument().InsType(), pld.Instrument().ExpiryDateOnly(), pld.Market().Name(), pld.NotActive()

after = acm.FPriceLinkDefinition.Select('')
price_links_count_after = len(after)

print 'Total number of PLDs that were deleted = ', price_links_count_before - price_links_count_after
    
print '*' * 16


