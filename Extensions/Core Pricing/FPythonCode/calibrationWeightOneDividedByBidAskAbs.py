import acm
import math

ael_variables = []

'''Weight function for a calibration equation. One divided by the bid/ask spread squared.
   If only, on side exists exception is thrown'''       
def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.

    #Unpack extra provided data for Weight functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObject = dict.At('calibrationRowObject')
    
    result = 1.0
    
    # A Volatility calibration row object encapsulates either an instrument, an orderbook or a volatility point.
    # Only an instrument or an orderbook has an instrument.
    # So, a bid ask spread is only valid for an instrument or an orderbook.
    # Hence volatility point with neither will use the weight 1.0
    if calibrationRowObject.Instrument():
    
        try:
        
            marketPriceBidValue = calibrationRowObject.MarketPriceBid().Value().Number()
            marketPriceAskValue = calibrationRowObject.MarketPriceAsk().Value().Number()
            
            if acm.Math.IsFinite(marketPriceBidValue) and acm.Math.IsFinite(marketPriceAskValue):
            
                result = 1 / acm.Math.Abs(marketPriceBidValue - marketPriceAskValue)
            
        except Exception as e:
        
            result = 1.0
        
    return [result]
