
import acm

def Strike(impVols, book):

    dataArray = impVols.GetDataArray(book)
    return dataArray[0]
        
def VolatilityAsk(impVols, book):

    dataArray = impVols.GetDataArray(book)
    return dataArray[6]
    

def VolatilityBid(impVols, book):
    
    dataArray = impVols.GetDataArray(book)
    return dataArray[3]

def VolatilityLast(impVols, book):
    
    dataArray = impVols.GetDataArray(book)
    return dataArray[9]

def VolumeAsk(impVols, book):

    dataArray = impVols.GetDataArray(book)
    return dataArray[5]

def VolumeBid(impVols, book):
    
    dataArray = impVols.GetDataArray(book)
    return dataArray[2]

def VolumeLast(impVols, book):

    dataArray = impVols.GetDataArray(book)
    return dataArray[8]

def CheckATM(book, atmRef, books):
    strike = book.Instrument().AbsoluteStrike()
    isCall = book.Instrument().IsCall()
    fallbackBook = 0
    retVal = book
    if ((strike >= atmRef and isCall == False) or (strike <= atmRef and isCall == True)) :
    
        fallbackBook = FindCallOrPutOrderBookWithStrike(strike, books, not isCall)

        if(fallbackBook):
            retVal = fallbackBook
    
    return retVal

def FindCallOrPutOrderBookWithStrike(strike, books, call):
    
    for i in range(0, books.Size()):
        
        book = books.At(i)
        if(book.Instrument().IsCall() == call and book.Instrument().AbsoluteStrike() == strike):
            return book

    return 0
    

def FindOrderBookWithStrike(strike, books):
     
    for i in range(0, books.Size()):
        
        book = books.At(i)
        if( book ):
            if( strike == book.Instrument().AbsoluteStrike() ):
                return book

    return 0
    
    
def IsOutlier(skew,
              volStruct,
              strike,
              vol,
              excludeOutliersPercentage):


    retVal = False
    
    if( skew and volStruct ):
        
        skewParams = skew.GetSkewParametersDictionary()
        atmVol = skewParams.At("ATM Vol")
        tempVol = volStruct.CalculateVolFromSkew(skew, strike)*100.0
        volMin = 0.0
        volMax = 0.0
        
        if( tempVol != 0.0 ):
            
            volMin = (( 100.0 - excludeOutliersPercentage ) * 0.01) * tempVol
            volMax = (( 100.0 + excludeOutliersPercentage ) * 0.01) * tempVol
        else:
            
            volMin = (( 100.0 - excludeOutliersPercentage ) * 0.01) * atmVol
            volMax = (( 100.0 + excludeOutliersPercentage ) * 0.01) * atmVol
            
        retVal = vol < volMin or vol > volMax;
    
    
    return retVal


def GetMidVol(book, 
              impVols,
              volStruct,
              skew,
              excludeBidAskZeros, 
              useVolWeightedMid,
              excludeOutliers,
              excludeOutliersPercentage,
              volumeBid,
              volumeAsk):


    retVal = 0.0
    
    if( impVols and book ):
        
        dataArray = impVols.GetDataArray(book)
        strike = Strike(impVols, book)
        volAsk = VolatilityAsk(impVols, book)
        volBid = VolatilityBid(impVols, book)
        
        businessDayWeight = volStruct.BusinessDayVolatilityFactor(book)
        volAskAdjusted = volAsk / businessDayWeight
        volBidAdjusted = volBid / businessDayWeight
        
        if( excludeBidAskZeros ):
        
            if( volAsk == 0.0 ):
                return 0.0      
            
            elif( volBid == 0.0 ):
                return 0.0
            
        if(excludeOutliers and skew):
        
            askOutlier = IsOutlier(skew,
                                   volStruct,
                                   strike,
                                   volAskAdjusted*100.0,
                                   excludeOutliersPercentage)

            bidOutlier = IsOutlier(skew,
                                   volStruct,
                                   strike,
                                   volBidAdjusted*100.0,
                                   excludeOutliersPercentage)

            if(askOutlier and bidOutlier):
            
                retVal = 0.0
                volAsk = 0.0
                volBid = 0.0
                volumeAsk = 0.0
                volumeBid = 0.0

            elif(askOutlier):
            
                volAsk = volBid
                volumeAsk = volumeBid
            
            elif(bidOutlier):
            
                volBid = volAsk
                volumeBid = volumeAsk
            

        
        if(useVolWeightedMid and retVal != 0.0):
        
            if(volumeBid != 0.0 and volumeAsk != 0.0):
            
                retVal = ((volumeBid*volBid) + (volumeAsk*volAsk)) / (volumeBid + volumeAsk)
            
            else:
                retVal = 0.0
            
        
        else:
            retVal = (volAsk+volBid)/2.0
        
    
    return retVal

def CalibrateSkew(skew, 
                  volStruct, 
                  strikes, 
                  volsAndStrikes):


    resVols = acm.FArray()
    sortedStrikes = strikes.Sort()
    
    for i in range(0, sortedStrikes.Size()):
        key = sortedStrikes.At(i)
        vol = volsAndStrikes.At(key)
        resVols.Add(vol)
    
    volStruct.CalcImpliedSkewParameters(sortedStrikes, resVols, 0.3, skew)
    
