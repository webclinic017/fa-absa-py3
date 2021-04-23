
import acm
import volFittingAlgoHelper
from math import log


def MoveSkewToCallPut(volStruct,
                      skew,
                      books,
                      impliedVols,
                      excludeBidAskZeros,
                      useVolumeWeightedMid,
                      excludeOutliers,
                      outlierPercentage):


    volDict = acm.FDictionary()
    paramStrikes = acm.FArray()
    resVols = acm.FArray()
    skewParams = skew.GetSkewParametersDictionary()
    atmRef = skewParams.At('ATM Ref')
    
    for n in range(0, books.Size()):
        bookCall = books[n]
        strike = bookCall.Instrument().AbsoluteStrike()
        bookPut = 0
        if( bookCall.Instrument().IsCall() ):
            bookPut = volFittingAlgoHelper.FindCallOrPutOrderBookWithStrike(strike, books, False)
        else:
            continue
        
        if( bookPut ):
            
            
            callMid = 0.0
            putMid = 0.0
            midVol = 0.0

            volumeBidCall = 0.0
            volumeAskCall = 0.0
            volumeBidPut = 0.0
            volumeAskPut = 0.0

            if( useVolumeWeightedMid ):
                
                dataArrayPut = impliedVols.GetDataArray(bookPut)
                dataArrayCall = impliedVols.GetDataArray(bookCall)
                
                
                
                volumeBidCall = dataArrayCall[2]
                volumeAskCall = dataArrayCall[5]

                volumeBidPut = dataArrayPut[2]
                volumeAskPut = dataArrayPut[5]
            

            callMid = volFittingAlgoHelper.GetMidVol(bookCall,
                                                     impliedVols,
                                                     volStruct,
                                                     skew,
                                                     excludeBidAskZeros,
                                                     useVolumeWeightedMid,
                                                     excludeOutliers,
                                                     outlierPercentage,
                                                     volumeBidCall,
                                                     volumeAskCall)

            putMid = volFittingAlgoHelper.GetMidVol(bookPut,
                                                    impliedVols,
                                                    volStruct,
                                                    skew,
                                                    excludeBidAskZeros,
                                                    useVolumeWeightedMid,
                                                    excludeOutliers,
                                                    outlierPercentage,
                                                    volumeBidPut,
                                                    volumeAskPut);

            midVol = (callMid+putMid)/2.0
            midVol /= volStruct.BusinessDayVolatilityFactor( bookPut )

            if(midVol != 0.0):
                volDict.AtPut(log(strike/atmRef), midVol)
                paramStrikes.Add(log(strike/atmRef))
            
            
    
    volFittingAlgoHelper.CalibrateSkew(skew, volStruct, paramStrikes, volDict)

def MovePointsToCallPut(volStruct,
                        points,
                        books,
                        impliedVols,
                        excludeBidAskZeros,
                        useVolumeWeightedMid):
                        
    
     for i in range(0, points.Size()):
    
        pnt = points[i]
        if( pnt ):
        
            bookCall = volFittingAlgoHelper.FindCallOrPutOrderBookWithStrike(pnt.ConvertedStrike(), books, True);
            bookPut = volFittingAlgoHelper.FindCallOrPutOrderBookWithStrike(pnt.ConvertedStrike(), books, False);
            callMid = 0.0
            putMid = 0.0
            volMid = 0.0

            volumeBidCall = 0.0
            volumeAskCall = 0.0
            volumeBidPut = 0.0
            volumeAskPut = 0.0

            if( useVolumeWeightedMid ):
            
                if( bookCall ):
                
                    volumeBidCall = volFittingAlgoHelper.VolumeBid(impliedVols, bookCall)
                    volumeAskCall = volFittingAlgoHelper.VolumeAsk(impliedVols, bookCall)
                
                if( bookPut ):
                
                    volumeBidPut = volFittingAlgoHelper.VolumeBid(impliedVols, bookPut)
                    volumeAskPut = volFittingAlgoHelper.VolumeAsk(impliedVols, bookPut)
                
            

            if( bookCall ):
            

                callMid = volFittingAlgoHelper.GetMidVol(bookCall,
                                                         impliedVols,
                                                         volStruct,
                                                         0,
                                                         excludeBidAskZeros,
                                                         useVolumeWeightedMid,
                                                         False,
                                                         0,
                                                         volumeBidCall,
                                                         volumeAskCall)
            
            if( bookPut ):
            

                putMid = volFittingAlgoHelper.GetMidVol(bookPut,
                                                        impliedVols,
                                                        volStruct,
                                                        0,
                                                        excludeBidAskZeros,
                                                        useVolumeWeightedMid,
                                                        False,
                                                        0,
                                                        volumeBidPut,
                                                        volumeBidCall)
            


            volMid = (callMid+putMid)/2.0
            pnt.Volatility(volMid)
            
            
def MoveToCallPut(parameters):
    
    '''The dictionary "parameters" contains data sent by the
       Volatility Manager. The data is:
       
       volstruct: The volatility structure that is being edited in the VM.
       keystobefitted: Keys to the dictionary "skeworpointsandbooks".
                       One key for each expiry for which points or a skew should be fitted,
       skeworpointsandbooks: A dictionary that contains volatility skews and orderbooks,
                             if it's a parametric structure, 
                             or volatility points and orderbooks, if it's a benchmark
                             structure.
       impliedvols: A FIVPCollection containing the implied volatility values
                    currently being plotted in the VM.
       excludebidaskzeros: Should bid/ask zeros be excluded? A boolean.
       usevolumeweightedmid: Should volume weighted mid be used? A boolean.
       excludeoutliers: Should outliers be excluded? A boolean.
       excludeoutlierspercentage: At what percentage from the curve should
                                  implied volatilities be excluded? An integer.'''
    
    volStruct = parameters.At('volstruct')
    keys = parameters.At('keystobefitted')
    skewOrPointsAndBooks = parameters.At('skeworpointsandbooks')
    impliedVols = parameters.At('impliedvols')
    excludeBidAskZeros = parameters.At('excludebidaskzeros')
    useVolWeightedMid = parameters.At('usevolumeweightedmid')
    excludeOutliers = parameters.At('excludeoutliers')
    outlierPercentage = parameters.At('excludeoutlierspercentage')
    
    for i in range(0, keys.Size()) : 
        skewOrPoints = skewOrPointsAndBooks.At(keys[i]).First()
        books = skewOrPointsAndBooks.At(keys[i]).Second()
        
        if( volStruct.IsParametricStructure() ) :
            
            MoveSkewToCallPut(volStruct,
                              skewOrPoints,
                              books,
                              impliedVols,
                              excludeBidAskZeros,
                              useVolWeightedMid,
                              excludeOutliers,
                              outlierPercentage)
                              
        else:
        
            MovePointsToCallPut(volStruct,
                                skewOrPoints,
                                books,
                                impliedVols,
                                excludeBidAskZeros,
                                useVolWeightedMid)
                
            
def ael_custom_dialog_main( parameters, dictExtra ):
    '''The dictExtra dictionary contains data sent from the Volatility Manager.
       parameters contains any data gathered in the custom GUI executed in 
       ael_custom_dialog_show. In this case no custom GUI is used.'''
       
    eii = dictExtra.At('customData')
    fittingDict = eii.ExtensionObject()
    MoveToCallPut(fittingDict)


def ael_custom_dialog_show(shell, params):
    '''We don't need to show any GUI for this algorithm 
       so just return an empty dictionary'''
    return acm.FDictionary()
