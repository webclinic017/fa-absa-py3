import acm

''''
Developer : Mighty Mkansi 
FX Cash pricing utils, caters for FX Spots, FX Forwards and FX Swaps
'''

def getTradesInPosition(trade): 
    
    if  trade.IsFxSwap():
        if  trade.IsFxSwapFarLeg():
            trade = trade.FxSwapNearLeg()
            
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('GroupTrdnbr.Oid', 'EQUAL', trade.Oid())  
          
    return query.Select() 


def isCross(trade):
    if 'USD' not in (trade.CurrencyPair().Currency1().Name(), 
                        trade.CurrencyPair().Currency2().Name()):
        return True
    return False

def BaseMarketPrice(trade):
    #get Base price
    
    for ctrade in getTradesInPosition(trade):        
        if isCross(trade):           
            if  ctrade.ValueDay() == trade.ValueDay() and ctrade.Currency() != trade.Currency() and ctrade.Status() == 'Internal':               
                if trade.Instrument().Currency() == ctrade.Instrument().Currency():                   
                    return ctrade.Price()         
                                                   
        elif ctrade.ValueDay() == trade.ValueDay() and ctrade.Status() == 'Internal':          
            return ctrade.Price()

            
def CounterMarketPrice(trade):
    #get Counter price
    
    for ctrade in getTradesInPosition(trade):
        
        if isCross(trade):
           
            if  ctrade.ValueDay() == trade.ValueDay() and ctrade.Currency() == trade.Currency() and ctrade.Status() == 'Internal':              
                
                if trade.Instrument().Currency() != ctrade.Instrument().Currency(): 
            
                    return ctrade.Price()                   
            
        elif ctrade.ValueDay() == trade.ValueDay() and ctrade.Status() == 'Internal':
           
            return ctrade.Price()        
           

def MarketPrice(trade):
    if isCross(trade):
        return CounterMarketPrice(trade)*BaseMarketPrice(trade)
    else:
        return CounterMarketPrice(trade)
        

def BaseMarketFwdPrice(trade):
    #get Base price
    if  trade.IsFxSwapFarLeg():
        trade = trade.FxSwapNearLeg()
        
    for ctrade in getTradesInPosition(trade):        
        if isCross(trade):           
            if  ctrade.ValueDay() != trade.ValueDay() and ctrade.Currency() != trade.Currency() and ctrade.Status() == 'Internal':               
                if trade.Instrument().Currency() == ctrade.Instrument().Currency():                   
                    return ctrade.Price()         
                                                   
        elif ctrade.ValueDay() != trade.ValueDay() and ctrade.Status() == 'Internal':          
            return ctrade.Price()

            
def CounterMarketFwdPrice(trade):
    #get Counter price

    if trade.IsFxSwap():
        if  trade.IsFxSwapFarLeg():
            trade = trade.FxSwapNearLeg()
     
    for ctrade in getTradesInPosition(trade):
        
        if isCross(trade):
           
            if  ctrade.ValueDay() != trade.ValueDay() and ctrade.Currency() == trade.Currency() and ctrade.Status() == 'Internal':              
                
                if trade.Instrument().Currency() != ctrade.Instrument().Currency(): 
            
                    return ctrade.Price() 
                    
             
        elif ctrade.ValueDay() != trade.ValueDay() and ctrade.Status() == 'Internal':
             
            return ctrade.Price()        
           

def FwdMarketPrice(trade):
    if isCross(trade):
        return CounterMarketFwdPrice(trade)*BaseMarketFwdPrice(trade)
    else:
        return CounterMarketFwdPrice(trade)


def CalculateTradeValueDayPnL(trade):    
    
    nominal = trade.Nominal()   
      
    if len(getTradesInPosition(trade))< 3:
        if trade.IsFxSwap(): 
            farLeg = trade.FxSwapFarLeg()
            far_points = farLeg.Price() - trade.ReferencePrice()
            near_points = trade.Price()- trade.ReferencePrice()
            
            return (far_points - near_points)*nominal
        else:
            return nominal*(trade.Price() - trade.ReferencePrice())
            
    else:              
        
        if trade.IsFxSwap(): 
           
            if  trade.IsFxSwapFarLeg():
                trade = trade.FxSwapNearLeg()
                farTrade = trade.FxSwapFarLeg()
                  
                spotPrice = farTrade.Price()
               
                fwdMarketPrice = FwdMarketPrice(trade) 
               
                far_points = (fwdMarketPrice - spotPrice)
            
                return (far_points)*nominal
            else:
                marketPrice = MarketPrice(trade)   
                spotPrice = trade.Price() 
                               
                market_points = marketPrice- spotPrice
               
                return (market_points)*nominal
        else:
            marketPrice = MarketPrice(trade)
            spotPrice = trade.Price() 
            return nominal*(marketPrice - spotPrice)
    return float(nominal*(trade.Price() - trade.ReferencePrice()))


