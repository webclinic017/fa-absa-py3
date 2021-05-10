import acm
import math

ael_variables = []

def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.

    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()

    for calibrationRowObject in calibrationRowObjects:
    
        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())

        #Only possible to filter if calibrationRowObject has an instrument
        #Filter one side market. 
        # Require that both bid/ask exist and that they are not the same.
        if not calibrationCostFunctionResult.Filtered() and calibrationRowObject.Instrument():
        
            marketPriceBidCalculation = calibrationRowObject.MarketPriceBid()
            marketPriceAskCalculation = calibrationRowObject.MarketPriceAsk()
            
            if not acm.Math.IsFinite(marketPriceBidCalculation.Value().Number()):
            
                calibrationCostFunctionResult.FilterReason("One-Sided Market, " + "No Valid Bid Price")
            
            elif not acm.Math.IsFinite(marketPriceAskCalculation.Value().Number()):
            
                calibrationCostFunctionResult.FilterReason("One-Sided Market, " + "No Valid Ask Price")
            
            elif acm.Math.AlmostEqual(marketPriceBidCalculation.Value().Number(), marketPriceAskCalculation.Value().Number()):
            
                calibrationCostFunctionResult.FilterReason("One-Sided Market, " + "Bid/Ask Price Considered Equal")
                    
    return [calibrationCostFunctionsResult]
