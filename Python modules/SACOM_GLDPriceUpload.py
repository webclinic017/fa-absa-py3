import ael, math, acm
'''----------------------------------------------------------------------------------------------------------------------------------
# Purpose                       :  Changed the name of STKs to have a suffix '_OLD' 
# Department and Desk           :  PCG
# Requester                     :  Herman Levin, Marko Milutinovic
# Developer                     :  Bhavnisha Sarawan, Anil Parbhoo
# CR Number                     :  C378889, C382688, C409966
----------------------------------------------------------------------------------------------------------------------------------'''
class SheetCalcSpace( object ):

    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet' )
  
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''----------------------------------------------------------------------------------------------------------------------------------
# eq = equity instrument name
# stk = stock instrument name
# copy price from equity instrument to stock instrument (bid, ask, last, settle)
----------------------------------------------------------------------------------------------------------------------------------'''
def update_stock_price_from_equity(eq,stk,d,*rest):
    
   
    #M.KLIMKE tag = acm.CreateEBTag()
    #M.KLIMKE v = acm.GetCalculatedValueFromString(i, 'Standard','object:*"portPriceSourceTheorPrice"' ,tag)
    i           = acm.FInstrument[eq]
    try:
        calc        = SheetCalcSpace.get_column_calc(i, 'Price Theor')
        SpotPrice   = calc.Value().Number()
    except AttributeError, e:
        calc = SheetCalcSpace.get_column_calc(i, 'Instrument Market Price')
        SpotPrice   = calc.Value().Number()

    div = eq + '_DivCash'
    # div = Divident cash instrument name
    # check if divdent cash instrument exits then add to equity price
    if ael.Instrument[div] != None:
        SpotPrice = SpotPrice + float(ael.Instrument[div].mtm_price(d, 'ZAR'))
    
    
    stkIns = ael.Instrument[stk]
        
    for p in stkIns.prices():
    
        if p.ptynbr.ptyid == 'SPOT':
        
            if p.day == d:
                try:
                    p_clone = p.clone()
                    p_clone.bid = SpotPrice
                    p_clone.ask = SpotPrice
                    p_clone.last = SpotPrice
                    p_clone.settle = SpotPrice
                    p_clone.curr = stkIns.curr
                    p_clone.commit()
                except:
                    pass
    return           
'''----------------------------------------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------------------'''
# main#
d = ael.date_today()
#d = ael.date_today().add_days(-1)

update_stock_price_from_equity('ZAR/ERAFI', 'ZAR/RAFISA_OLD', d)
update_stock_price_from_equity('ZAR/NEWRAND', 'ZAR/NRD_OLD', d)
update_stock_price_from_equity('ZAR/NEWFSAETF', 'ZAR/NEWFSA_OLD', d)
update_stock_price_from_equity('ZAR/SHARIAH', 'ZAR/NFSH40_OLD', d)
update_stock_price_from_equity('ZAR/ERAFIFIN', 'ZAR/RAFFIN_OLD', d)
update_stock_price_from_equity('ZAR/ERAFIINDI', 'ZAR/RAFIND_OLD', d)
update_stock_price_from_equity('ZAR/ERAFIRES', 'ZAR/RAFRES_OLD', d)
update_stock_price_from_equity('ZAR/DIVI_STX', 'ZAR/STXDIV_OLD', d)
update_stock_price_from_equity('ZAR/ALSI_STX', 'ZAR/STX40_OLD', d)
update_stock_price_from_equity('ZAR/SWIX_STX', 'ZAR/STXSWX_OLD', d)
update_stock_price_from_equity('ZAR/FINI_STX', 'ZAR/STXFIN_OLD', d)
update_stock_price_from_equity('ZAR/RESI_STX', 'ZAR/STXRES_OLD', d)
update_stock_price_from_equity('ZAR/INDI_STX', 'ZAR/STXIND_OLD', d)





'''
2259.440497
1825.125117
2235.4731447
260.68916
'''
