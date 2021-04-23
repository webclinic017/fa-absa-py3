''' =======================================================================
    TMS_Config_Trade
    Purpose                 :   This module is used to verify whether a given trade should be passed
                                through the TMS trade feed by means of checking its trade type, trade 
                                status and/or portfolio it belongs to.
    Department and Desk     :   SM IT Pricing & Risk
    Requester               :   Matthew Berry
    Developer               :   Eben Mare, Peter Kutnik
    CR Number               :   TBD
    
    ======================================================================= 
    
    Purpose                 :   Added Asset Portfolio Mappings for Foreign Exchange Trading, also added function to handle 
                            :   FX Portfolios not under FOREIGN EXCHANGE TRADING
    Department and Desk     :   SM IT Pricing & Risk
    Requester               :   Matthew Berry
    Developer               :   Babalo Edwana
    CR Number               :   261644
    
    Changes			: Removed FO Sales status from the exclusion list for trades taht must be ignored, FO Sales trades must feed to TMS
    Date			: 12/04/2010
    Developer		: Babalo Edwana
    Requester		: Mathew Berry
    CR Number		: 282095
    ============================================================================================================ '''
#------------------------------------------------------------------------------
#Developer:      Peter Kutnik
#Date:           2010-10-21
#Detail:         Added trade move functionality
#CR number:      468377
#------------------------------------------------------------------------------
#Developer:      Jan Mach
#Date:           2013-07-18
#Detail:         Removed equity trade configuration
#CR number:      CHNG0001177565
#------------------------------------------------------------------------------
#Developer:      Vaughan Reid
#Date:           2017-11-28
#Detail:         Added Reserved status to exclusion list
#CR number:      
#------------------------------------------------------------------------------

    
import ael, acm

from TMS_Functions_Common import setTradeAddInfo, isPrfElement, ReformatDate
from TMS_AssetClasses import IRDAssetConfig, FXAssetConfig, TradeFactories
from time import time

#We will use this mapping list to determine which asset class we are considering
#based on a portfolio's position in the portfolio tree.
ASSET_PRF_MAPPING = {"FIXED INCOME TRADING": IRDAssetConfig(), 
                     "FIXED INCOME BANKING": IRDAssetConfig(),
                     "FOREIGN EXCHANGE TRADING"   : FXAssetConfig()}

# Do not conider trades that expired before this date
CUTOFF_EXPIRY_DATE = ael.date_from_ymd(2007, 5, 30)
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Determine the trade type
class EnumTradeType:
    PRODUCTION = 1
    TEST = 2
    MOVING = 3


def getTradeFactories():
    return TradeFactories
    
def getTradeType(trade):
    if trade.prfnbr:
        pofoType = trade.prfnbr.add_info("BarCap_TMS_Feed")
        if pofoType == "Production":
            return EnumTradeType.PRODUCTION
        elif pofoType == "Test":
            return EnumTradeType.TEST
        elif (trade.add_info("TMS_Trade_Id") != '' or trade.optional_key.startswith('TMS')) and trade.add_info("TMS_Moved") == '':
            return EnumTradeType.MOVING
        else:
            return None
        

#Determine the asset class of a trade
def getPrfAssetClass(portfolio):
    for prfid in ASSET_PRF_MAPPING.keys():
        if isPrfElement(ael.Portfolio[prfid], portfolio):
            return ASSET_PRF_MAPPING[prfid]

def getTradeAssetClass(trade):
    return getPrfAssetClass(trade.prfnbr)

# Define the valid status
def isValidStatus(tradeType, status):
    if tradeType == EnumTradeType.PRODUCTION:
        return status not in ('Simulated', 'Reserved')
    elif tradeType == EnumTradeType.TEST:
        return status in ('Simulated')
    elif tradeType == EnumTradeType.MOVING:
        return True
    else:
        raise ValueError("Unhandled trade type: %s" % repr(tradeType))

# All conditions
def isConsideredForTMS(trade):
    # Check trade status
    tradeType = getTradeType(trade)
    if tradeType and isValidStatus(tradeType, trade.status):
        # Check instrument's expiry
        # Note: do this last for performance of additional lookup
        instr = ael.Instrument[trade.insaddr.insaddr]
        if instr.exp_day >= CUTOFF_EXPIRY_DATE:
            return True
        else:
            if instr.instype == "Curr": 
                if trade.value_day >= CUTOFF_EXPIRY_DATE:
                    return True
    return False

def TouchTrade(trade, operation=None):
    return setTradeAddInfo(trade, 'TMS_Gen_Message', ReformatDate(time(), TIME_FORMAT, TIME_FORMAT) )
    
def SetMovedFlag(trade):
    return setTradeAddInfo(trade, 'TMS_Moved', ReformatDate(time(), TIME_FORMAT, TIME_FORMAT) )    

def ClearMovedFlag(trade):
    listAddInfos = acm.FAdditionalInfo.Select("recaddr = %d and addInf = 'TMS_Moved'" % trade.trdnbr)
    if len(listAddInfos) > 0:
        listAddInfos[0].Delete()
        
    
def getPrfAssetClassConversions(trade):
    if trade:
        instr = trade.insaddr
        if instr:
            if instr.instype == "Curr" or (instr.instype == "Option" and instr.und_instype == "Curr"):
                return ASSET_PRF_MAPPING["FOREIGN EXCHANGE TRADING"]
