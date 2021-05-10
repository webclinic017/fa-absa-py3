""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRSettings.py"
import acm

#----------------Calculation parameters-----------------------
# SACCR Parameters

#---------------Market data path functions---------
def MarketDataFilePath(valuationDate):
    '''---------------------------------------
    The valuationDate parameter enables the use of historical price
    factors in valuation. Example:
    if valutionDate < acm.Time().DateToday():
        return 'C:/Adaptiv/bin/MarketDataBaseVal' + str(valuationDate) + '.dat'
    '''
    return 'C:/Adaptiv/bin/MarketData.dat'

def RateFixingFilePath():
    return 'C:/temp/saccr/'

def SACCRDealOutFilePath():
    return 'C:/temp/saccr/'

def SACCRMarketDataOutFilePath():
    return 'C:/temp/saccr/'
