
import acm
import volFittingAlgoHelper
from math import log

def MoveSkewToLast(volStruct,
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
    
    atmRef = skewParams.At('ATM Ref')
    for i in range(books.Size()):
    
        book = books[i]
        if( book ):
        
            volLast = volFittingAlgoHelper.VolatilityLast(impVols, book)
            strike = book.Instrument().AbsoluteStrike()

            volLast /= volStruct.BusinessDayVolatilityFactor( book )

            if(volLast != 0.0):
            
                volDict.AtPut(log(strike/atmRef), volLast)
                paramStrikes.Add(log(strike/atmRef));
            

        

    
    volFittingAlgoHelper.CalibrateSkew(skew,
                                       volStruct,
                                       paramStrikes,
                                       volDict)
    
def MovePointsToLast(volStruct,
                     points,
                     books,
                     impVols,
                     excludeBidAskZeros,
                     useVolumeWeightedMid):

    for i in range(0, points.Size()):
    
        pnt = points[i]
        if( pnt ):
        
            book = volFittingAlgoHelper.FindOrderBookWithStrike(pnt.ConvertedStrike(), books)
            if( book ):
            
                volLast = volFittingAlgoHelper.VolatilityLast(impVols, book)
                pnt.Volatility(volLast)
            
                


                
def MoveToLast(parameters):

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
            
            MoveSkewToLast(volStruct,
                           skewOrPoints,
                           books,
                           impliedVols,
                           excludeBidAskZeros,
                           useVolWeightedMid,
                           excludeOutliers,
                           outlierPercentage)
        else:
            
            MovePointsToLast(volStruct,
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
    MoveToLast(fittingDict)
    
def ael_custom_dialog_show(shell, params):
    '''We don't need to show any GUI for this algorithm 
       so just return an empty dictionary'''
    return acm.FDictionary()

