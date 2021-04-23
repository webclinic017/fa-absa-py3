
import acm
import volFittingAlgoHelper
from math import log

def MoveSkewToMid(volStruct,
                  skew,
                  books,
                  impVols,
                  excludeBidAskZeros,
                  useVolumeWeightedMid,
                  excludeOutliers,
                  outlierPercentage):
                  

    volDict = acm.FDictionary()
    paramStrikes = acm.FArray()
    resVols = acm.FArray()
    skewParams = skew.GetSkewParametersDictionary()
    
    
    for n in range(0, books.Size()):
        book = books[n]
        book = volFittingAlgoHelper.CheckATM(book, skewParams.At('ATM Ref'), books)
        
        if book:
        
            dataArray = impVols.GetDataArray(book)
            
            
            volAsk = volFittingAlgoHelper.VolatilityAsk(impVols, book)
            volBid = volFittingAlgoHelper.VolatilityBid(impVols, book)
            volumeAsk = 0.0
            volumeBid = 0.0
            
            if( useVolumeWeightedMid ):
                
                volumeAsk = volFittingAlgoHelper.VolumeAsk(impVols, book)
                volumeBid = volFittingAlgoHelper.VolumeBid(impVols, book)
            
            
            strike = book.Instrument().AbsoluteStrike()
            midVol = volFittingAlgoHelper.GetMidVol(book,
                                                    impVols,
                                                    volStruct,
                                                    skew,
                                                    excludeBidAskZeros,
                                                    useVolumeWeightedMid,
                                                    excludeOutliers,
                                                    outlierPercentage,
                                                    volumeBid,
                                                    volumeAsk)
            
            midVol /= volStruct.BusinessDayVolatilityFactor(book)
            
            if midVol:
                
                volDict.AtPut(log(strike / skewParams.At('ATM Ref')), midVol)
                paramStrikes.Add(log(strike / skewParams.At('ATM Ref')))
        
    volFittingAlgoHelper.CalibrateSkew(skew, volStruct, paramStrikes, volDict)
                  

def MovePointsToMid(volStruct,
                    points,
                    books,
                    impVols,
                    excludeBidAskZeros,
                    useVolumeWeightedMid):

    for i in range(0, points.Size()):
    
        pnt = points[i]
        if( pnt ):

            strike = pnt.ConvertedStrike()
            call = True
            if( strike <= volStruct.GetUnderlyingForward(pnt.ActualExpiryDay()) ):
                call = False

            book = volFittingAlgoHelper.FindCallOrPutOrderBookWithStrike(strike, books, call)

            if( book ):
                
                
                volumeBid = 0.0;
                volumeAsk = 0.0;

                if( useVolumeWeightedMid ):
                    
                    volumeBid = volFittingAlgoHelper.VolumeBid(impVols, book)
                    volumeAsk = volFittingAlgoHelper.VolumeAsk(impVols, book)
                

                
                
                volMid = volFittingAlgoHelper.GetMidVol(book,
                                                        impVols,
                                                        volStruct,
                                                        0,
                                                        excludeBidAskZeros,
                                                        useVolumeWeightedMid,
                                                        False,
                                                        0,
                                                        volumeBid,
                                                        volumeAsk)

                if( excludeBidAskZeros == False ):
                    pnt.Volatility(volMid)
                
                elif( volMid ):
                    pnt.Volatility(volMid)
                
def MoveToMid(parameters):

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
            
            MoveSkewToMid(volStruct,
                          skewOrPoints,
                          books,
                          impliedVols,
                          excludeBidAskZeros,
                          useVolWeightedMid,
                          excludeOutliers,
                          outlierPercentage)
        else:
            
            MovePointsToMid(volStruct,
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
    MoveToMid(fittingDict)

def ael_custom_dialog_show(shell, params):
    '''We don't need to show any GUI for this algorithm 
       so just return an empty dictionary'''
    return acm.FDictionary()
