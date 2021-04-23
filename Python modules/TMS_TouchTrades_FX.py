''' ==========================================================================================
    Purpose		: This module is used to touch an additional info field on a group of 
                        : trades such as to send those trades through to TMS for FX Trades, 
                        : this is to handle FXSwaps where both legs have to be updated.
    Department and Desk	:
    Requester		: Mathew Berry
    Developer		: Babalo Edwana
    CR Number		: 261644
    ========================================================================================== '''

import ael, acm

from TMS_Config_Trade import *
from TMS_Functions import TMS_Filter

from pprint import pprint
from time import clock

import TMS_Functions_Common


class FXTouchTrades:
    def _setAdditionalInfoFX(self, entity_near, entity_far, addInfo_fieldName, value):
        existing_addinfos = {}
        if entity_far:
            for ai in entity_near.additional_infos():
                
                existing_addinfos[ai.addinf_specnbr.field_name] = ai

                if existing_addinfos.has_key(addInfo_fieldName):
                    new_near = existing_addinfos[addInfo_fieldName].clone()
                else:
                    ai_spec = ael.AdditionalInfoSpec[addInfo_fieldName].clone()
                    new_near = ael.AdditionalInfo.new(entity_near.clone())
                    new_near.addinf_specnbr = ai_spec

                new_near.value = value
                
            for ai in entity_far.additional_infos():
                
                existing_addinfos[ai.addinf_specnbr.field_name] = ai

                if existing_addinfos.has_key(addInfo_fieldName):
                    new_far = existing_addinfos[addInfo_fieldName].clone()
                else:
                    ai_spec = ael.AdditionalInfoSpec[addInfo_fieldName].clone()
                    new_far = ael.AdditionalInfo.new(entity_far.clone())
                    new_far.addinf_specnbr = ai_spec

                new_far.value = value
            
            ael.begin_transaction()
            new_near.commit()
            new_far.commit()
            ael.commit_transaction()
        else:
            for ai in entity_near.additional_infos():
                existing_addinfos[ai.addinf_specnbr.field_name] = ai

                if existing_addinfos.has_key(addInfo_fieldName):
                    new = existing_addinfos[addInfo_fieldName].clone()
                else:
                    ai_spec = ael.AdditionalInfoSpec[addInfo_fieldName].clone()
                    new = ael.AdditionalInfo.new(entity_near.clone())
                    new.addinf_specnbr = ai_spec

            new.value = value
            new.commit()


def FX_TouchTrade(near_trade,far_trade, operation=None):
    try:
        objTouchTrades = FXTouchTrades()
        objTouchTrades._setAdditionalInfoFX(near_trade, far_trade, 'TMS_Gen_Message', TMS_Functions_Common.ReformatDate(time(), TIME_FORMAT, TIME_FORMAT))
    except Exception, e:
        print e
        return "The additional info field 'TMS_Gen_Message' could not be set on trade %d - %s" % (near_trade.trdnbr, e)
    
    return "Success"
    
    
def isFarLeg(trade):
        acmTrade = acm.FTrade[trade.trdnbr]
        #return(acmTrade.TradeProcess() == EnumFXCash.SWAP_FAR_LEG and True or False)
        return acmTrade.IsFxSwapFarLeg()

def getFXTrade(trade):
    if trade:
        instr = ael.Instrument[trade.insaddr.insaddr]
        if instr:
            if instr.instype == "Curr": 
                if isFarLeg(trade):
                    acmTrade = TMS_Functions_Common.otherleg(trade)
                    if acmTrade:
                        return ael.Trade[acmTrade.Oid()]
    return trade

def getOtherTrade(trade):
    if trade:
        instr = ael.Instrument[trade.insaddr.insaddr]
        if instr:
            if instr.instype == "Curr":
                acmTrade = TMS_Functions_Common.otherleg(trade)
                if acmTrade:
                    return ael.Trade[acmTrade.Oid()]
    return None
            
	
def isConsidered(trade, force):
    #Skip checking neccesary pre-post conditionas if we are forcing the trade through
    if force: return 1

    #Determine the desk of the trade and do the correct check
    return TMS_Filter(trade, trade.insaddr)

def TouchTrades(trades, force = 0):
    status = {}
    for trade in trades:
        
        #Only send the trade if it satisfies the neccesary conditions
	near_trade = trade
	far_trade = getOtherTrade(trade)
	
	if isConsidered(trade, force):
            status[trade.trdnbr] = FX_TouchTrade(near_trade, far_trade, __name__)
          
        else:
            status[trade.trdnbr] = "Trade Not Considered for CRE"

    return status

# ################
# User Interface
# ################

ael_variables = [("tf", "Trade Filter", "string", [tf.fltid for tf in ael.TradeFilter], "", 1, 0),
                 ("log", "Log File Name", "string", None, r"C:\temp\touched_log.txt", 1, 0),
                 ("force", "Force", "bool", [0, 1], 0, 1, 0)]

def ael_main(ael_dict):
    tic = clock()
    results = TouchTrades(ael.TradeFilter[ael_dict["tf"]].trades(), ael_dict["force"])

    file = open(ael_dict["log"], "w")
    try:
        file.write( "\n".join( ["%d: %s" % (k, results[k]) for k in results.keys()] ))
    finally:
        file.close()

    print "Done in %f seconds" % (clock() - tic)
    print "Processed %d trades. Please see %s for more detail." % (len(results), ael_dict["log"])
