#------------------------------------------------------------------------------
#Name:           TMS_AMBA_GenericHook
#Purpose:        This module exposes the hook TMS_Generate_Message which will 
#        be hooked onto by AMBA. If a trade/instrument/counterparty 
#        update is done which indirectly influences a trade which needs 
#        to go (or be updated) to TMS then a trade message will be 
#        created and stored into the AMB database.
#Developer:      Eben Mare
#Create Date:    N/A
#
#Changes
#
#Developer:      Peter Kutnik
#Date:           2010-05-03
#Detail:         TradeUpdateHandler._ignoreUpdate: changed logic to ignore 
#       AddInfo('TMS_Trade_Id') rather than optional_key. Utilized
#       earlier developed code by Eben Mare.
#------------------------------------------------------------------------------ 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Purpose            : FXSwap Instrument in 4.3, Front Validation requires that both trades of an FXSwap 
#                        : be updated together, in order to cater for this limitation, we have Added a ReceiverModifyHook
#                        : to update the bounce back Message from Synthesis Adaptor to Include an FXSwap Additional Info field update 
#                        : for TMSid in a transaction.
#                        
#                        : Updated module to only send an update or insert for FXSwap for the one leg, otherwise the SendModifyHook sends duplicate 
#                        : messages to TMS for FXSwap Instruments, changed the logic for instrument update not to get all trades linked to the instrument for
#                       : FX cash Instruments, as this causes all trades linked to a currecny to be touched.
#                        
#                        : TradeUpdateHandler._ignoreUpdate : Changed to re-use AddInfo('TMS_Trade_Id'), since for FX trades this field is used for DT Compass Trades
#                        : this change has been incooporated into FX changes but a separate change will be made to current FI and EQ module, then the change will be intergrated
#                        : to FX
#Department and Desk    :
#Requester        : Mathew Berry
#Developer        : Babalo Edwana
#CR Number        : 261644

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Developer:      Peter Kutnik
#Date:           2010-04-06
#Detail:         Added code to TradeDependencyUpdateHandler to directly process
#                first trade affected, added trades where instrument is underlying
#                detection to InstrumentUpdateHandler, added orig header txnbr and 
#                source to messages
#CR number:      274189
#------------------------------------------------------------------------------
#Developer:      Peter Kutnik
#Date:           2010-04-09
#Detail:         Hotfix for TradeDependencyUpdateHandler for cases where first trade
#                in trade list is not considered for TMS.
#CR number:      277456
#------------------------------------------------------------------------------

#Developer:      Babalo Edwana
#Date:           2010-06-22
#Detail:         Ignore MOPL Downstream Trade Update AMBA Messages.
#CR number:      348925
#------------------------------------------------------------------------------

#Developer:      Babalo Edwana
#Date:           2010-07-28
#Detail:         Updated TradeDependencyUpdateHandler and InstrumentUpdateHandler
#     :        Updated InstrumentUpdateHandler to return a list object as PartyUpdateHandler returns a list Object.
#       :          Updated TradeDependencyUpdateHandler to Flatten the list return but either InstrumentUpdateHandler or PartyUpdateHandler via List comprehension
#       :          Reason for the change - the TradeDependencyUpdateHandler expects the object trades to be a list of ael.entity objects but for PartyUpdateHandler the function
#       :          _getTrades() returns a list of ael.selection objects which is itself a list of ael.entity objects, hence the solution to return the a list for both UpdateHandler classes and 
#       :          then Flatten the list to get the ael.entity object as expected by the function.
#CR number:    385876  
#------------------------------------------------------------------------------
#Developer:      Babalo Edwana
#Date:           2010-10-08
#Detail:         Added Midas Additional Info fields for Trade updates exclusion
#CR number:    458129
#------------------------------------------------------------------------------
#Developer:      Peter Kutnik
#Date:           2010-10-21
#Detail:         Added trade move functionality
#CR number:      468377
#------------------------------------------------------------------------------
#Developer:      Babalo Edwana
#Date:           2012-07-26
#Detail:         Added Error handling and logging Trade number for the trade that throws an error.
#CR number:      354551
#------------------------------------------------------------------------------
#Developer:      Babalo Edwana
#Date:           2012-08-16
#Detail:         Added filter for Party update when Additional Info is not touched.
#CR number:      CHNG0000398277
#------------------------------------------------------------------------------
#Developer:      Babalo Edwana
#Date:           2012-09-07
#Detail:         Updated InstrumentUpdateHandler to touched trades for Option Trades where 
#                underlying instrument has been updated.
#CR number:      CHNG0000440842
#------------------------------------------------------------------------------
#Developer:      Jan Mach
#Date:           2013-07-12
#Detail:         Exception in trade wrapper is converted to Amba message
#                to avoid Amba crash 
#CR number:      CHNG0001177565
#------------------------------------------------------------------------------ 
#Developer:      Jan Mach
#Date:           2015-09-03
#Detail:         Exception handler is fixed
#CR number:      CHNG0001177565
#------------------------------------------------------------------------------ 

import ael, acm, amb
from TMS_AMBA_Message import *
from TMS_Config_Trade import *
from TMS_Functions import *
from time import time
from TMS_Functions_Common import *
from TMS_ResponseWrapper_FX import *

# --- Handlers for each message type ---

global MESSAGE_SUBJECT
MESSAGE_SUBJECT = "TMS MESSAGE"
SOURCE = "TMS"

def GenerateTradeMsg(aelTrade, ambaMsg, msgType):
    try:
        source = ambaMsg.mbf_find_object("SOURCE", "MBFE_BEGINNING").mbf_get_value()
        txnbr = ambaMsg.mbf_find_object("TXNBR", "MBFE_BEGINNING").mbf_get_value()        

        factory = SupportsTradeMessage(aelTrade)
        if factory:
            newMsg = CreateTradeMessage(factory, aelTrade, msgType, source, txnbr)
            
            if newMsg is not None:
                if getTradeType(aelTrade) == EnumTradeType.MOVING:
                    AdjustMovingMessage(newMsg)                
                    SetMovedFlag(aelTrade)
                else:
                    ClearMovedFlag(aelTrade)
    
            return (newMsg, MESSAGE_SUBJECT)
        else:
            return None
        
    except Exception as ex:
        errorMsg = "Error '%s' occured when generating trade message for trade [%d]" %(ex, aelTrade.trdnbr)
        print errorMsg

        newMsg = amb.mbf_start_message(
                    None,
                    "ERROR",
                    AMBA_VERSION,
                    None,
                    source)
        newMsg.mbf_add_string('TXNBR', txnbr)
        newMsg.mbf_add_string('Error', errorMsg)

        return (newMsg, "ERROR")

def AdjustMovingMessage(newMsg):
    ambTrade = newMsg.mbf_find_object("TRADE", "MBFE_BEGINNING")
    if ambTrade:
        AddOrReplaceAMBString(ambTrade, "Book_ID", "-1")
        AddOrReplaceAMBString(ambTrade, "Strategy_Book_ID", "-1")
        AddOrReplaceAMBString(ambTrade, "Strategy_Book", "ABMoved")

def AddOrReplaceAMBString(msg, key, value):
    ambObj = msg.mbf_find_object(key, "MBFE_BEGINNING")
    if ambObj:
        msg.mbf_replace_string(key, value)
    else:
        msg.mbf_add_string(key, value)

class MessageHandler:
    # NOTE: Should return a tuple of (msg, src) or None
    def __call__(self, msg):
        raise NotImplementedError

class TradeBaseHandler(MessageHandler):

    def __call__(self, msg):
        # Get the element with trade id 
        tradeElem = self._getTradeElement(msg)
        if tradeElem:
            # Lookup the trade
            tradeId = int( tradeElem.mbf_find_object("TRDNBR", 
                                                     "MBFE_BEGINNING").mbf_get_value() )
            trade = ael.Trade[tradeId]
            
            if trade:
                # Check we want this trade
                if isConsideredForTMS(trade):
                    # If we are exercising a trade a new equal and opposite trade will be booked - 
                    # we will alter the state of the original trade so that it can get booked through
                    # as expired to TMS aswell
                    '''
                    if trade.type == "Exercise":
                        trade_linked = ael.Trade[trade.contract_trdnbr]
                        if trade_linked:
                            #By setting the type on the original trade we will force a new message to be generated.
                            mirror_trade = trade_linked.clone()
                            mirror_trade.type = "Exercise"
                            mirror_trade.commit()
                    '''

                    # Okay all good, so generate the trade msg
                    tupMessage = GenerateTradeMsg(trade, msg, self._getMsgType(trade))
                    return tupMessage
            else:
                print 'Error: Trade: %s, does not exist in Front Arena.' % tradeId

    def _getTradeElement(self, msg):
        raise NotImplementedError

    def _getMsgType(self, trade):
        raise NotImplementedError
    
    

class TradeInsertHandler(TradeBaseHandler):
    def _getTradeElement(self, msg):
        tradeElem = msg.mbf_find_object("+TRADE", "MBFE_BEGINNING")
        if tradeElem:
            tradeId = int( tradeElem.mbf_find_object("TRDNBR", 
                                                     "MBFE_BEGINNING").mbf_get_value() )
            acmTrade = acm.FTrade[tradeId]
            #check if the insert should be ignored for FX Swap Far Trade
            if not self._ignoreFXSwapInsert(acmTrade):
                return tradeElem

    def _getMsgType(self, trade):
        return EnumOperation.INSERT
    
    # For FXSwap, ignore insert trade for Far Leg, otherwise two Insert trade Messages
    # will be generated and sent to TMS
    def _ignoreFXSwapInsert(self, acmTrade):
        if acmTrade:
            acmInstrument = acm.FInstrument[acmTrade.Instrument().Oid()]
            if acmInstrument.InsType() == 'Curr':
                if acmTrade.IsFxSwapFarLeg():
                    return True
            
        return False

class TradeUpdateHandler(TradeBaseHandler):
    def _getTradeElement(self, msg):   
        # Check if trade section has been updated
        updateElem = msg.mbf_find_object("!TRADE", "MBFE_BEGINNING") or \
                     msg.mbf_find_object("TRADE", "MBFE_BEGINNING")
        if updateElem:
            print 'Original message'
            print msg.mbf_object_to_string()
            # Ensure this isn't a TMS external key update, otherwise we will cause a loop
            # Also Ensure that the MOPL Downstream updates are not processed as this will flood the Adaptor.
            if not self._ignoreUpdate(msg):
                tradeId = int( updateElem.mbf_find_object("TRDNBR", 
                                                     "MBFE_BEGINNING").mbf_get_value() )
                acmTrade = acm.FTrade[tradeId]
                if acmTrade and acmTrade.UpdateUser().Name() == 'AMBA_TMSTRD_PRD':
                    print 'Ignoring trade update by AMBA_TMSTRD_PRD'
                    return
                if not self._ignoreFXSwapUpdate(acmTrade):
                    return updateElem

    # For TMS Id ignore update
    # For MOPL Imports, should ignore update to add info for down stream
    # For Midas Updates, should ignore update to Add Info as well...
    def _ignoreUpdate(self, msg):
        updateElem = msg.mbf_find_object("!TRADE", "MBFE_BEGINNING") or \
                     msg.mbf_find_object("TRADE", "MBFE_BEGINNING")
        if updateElem:
            addInfo = updateElem.mbf_find_object("!ADDITIONALINFO", "MBFE_BEGINNING") or \
                         updateElem.mbf_find_object("+ADDITIONALINFO", "MBFE_BEGINNING")
            addInfoFields = []
            addInfoFieldsName = ['ExternalVal', 'ExternalDelta', 'ExternalCCY', 'ExternalPurchaseAmt',
                                 'ExternalPurchasePV', 'ExternalPurchaseCCY', 'ExternalSaleAmt', 'ExternalSalePV',
                                 'ExternalSaleCCY', 'TMS_Trade_Id', 'TMS_Moved', 'Midas_ID', 'Midas_ID_BTB', 'Midas_Status', 'Midas_Status_BTB']
            while addInfo:
                addInfoFieldName = addInfo.mbf_find_object("ADDINF_SPECNBR.FIELD_NAME", "MBFE_BEGINNING")
                
                if addInfoFieldName:
                    if addInfoFieldName.mbf_get_value() in addInfoFieldsName:
                        return True

                updateElem.mbf_remove_object()
                addInfo = updateElem.mbf_find_object("!ADDITIONALINFO", "MBFE_BEGINNING") or \
                         updateElem.mbf_find_object("+ADDITIONALINFO", "MBFE_BEGINNING")
                         
            return False
        
    # For FXSwap, ignore update trade for Far Leg, otherwise two update trade Messages
    # will be generated and sent to TMS
    def _ignoreFXSwapUpdate(self, acmTrade):
        if acmTrade:
            acmInstrument = acm.FInstrument[acmTrade.Instrument().Oid()]
            if acmInstrument.InsType() == 'Curr':
                if acmTrade.IsFxSwapFarLeg():
                    return True
            
        return False

    def _getMsgType(self, trade):
        # NOTE: If this hasn"t been processed before by TMS (e.g. portfolio move), 
        # then consider it an INSERT
        return trade.add_info('TMS_Trade_Id') != '' and EnumOperation.UPDATE or EnumOperation.INSERT
    
class TradeDependencyUpdateHandler(MessageHandler):
    """ Note that the AMB Message generation (via the TMS_TradeWrapper classes) always
    generates a TRADE level message. When an update occurs on one of the Trade Dependencies
    levels (e.g. Instrument, Counterparty - note ) we will populate a "dummy" field on 
    the trade to simulate a Trade update.
    """
    def __call__(self, msg):
        # Build a list of trades to which the current table can link
        trades = self._getTrades(msg)
        tupMessage = None
        #Flatten the List Comprehension, since PartyUpdateHandler returns a list of ale.selection object which is a list of trades
        #therefore you have a list within a list and the list must be flatten to get the trades
        if trades:
            listConsideredTrades = [trade for x in trades for trade in x if isConsideredForTMS(trade)]
            if len(listConsideredTrades) > 0:
                #create update for listConsideredTrades[0]
                tupMessage = GenerateTradeMsg(listConsideredTrades[0], msg, EnumOperation.UPDATE)
                #touch rest            
                for trade in listConsideredTrades[1:]:
                    TouchTrade(trade, self._getUpdateType())                
        return tupMessage

    def _getTrades(self, msg):
        raise NotImplementedError

    def _getUpdateType(self):
        raise NotImplementedError

class InstrumentUpdateHandler(TradeDependencyUpdateHandler):
    def _getTrades(self, msg):
        insElem = msg.mbf_find_object("!INSTRUMENT", "MBFE_BEGINNING") or \
            msg.mbf_find_object("INSTRUMENT", "MBFE_BEGINNING")

        trades = []
        if insElem:
            insAddrElem = insElem.mbf_find_object("INSADDR", "MBFE_BEGINNING")
            if insAddrElem:
                insId = int(insAddrElem.mbf_get_value())

                instr = ael.Instrument[insId]
                if instr and instr.instype != "Curr":
                    trades.extend(instr.trades())
                    linkedInstruments = ael.Instrument.select("und_insaddr = %d" %(instr.insaddr))
                    if linkedInstruments:
                        for linkedInstrument in linkedInstruments:
                            trades.extend(linkedInstrument.trades())

        return [trades]

    def _getUpdateType(self):
        return "INSTR UPDT"

class PartyUpdateHandler(TradeDependencyUpdateHandler):
    def _getTrades(self, msg):
        partyElem = msg.mbf_find_object("!PARTY", "MBFE_BEGINNING") or \
            msg.mbf_find_object("PARTY", "MBFE_BEGINNING")

        if partyElem:
            if not self._ignoreUpdate(msg):
                ptynbrElem = partyElem.mbf_find_object("PTYNBR", "MBFE_BEGINNING")
                if ptynbrElem:
                    party_nbr = int(ptynbrElem.mbf_get_value())
                    return [ael.Trade.select("%s = %s" % (party_type, party_nbr) ) for \
                            party_type in ("counterparty_ptynbr", "broker_ptynbr", "acquirer_ptynbr")]


    def _getUpdateType(self):
        return "PARTY UPDT"
        
    def _ignoreUpdate(self, msg):
    
        updateElem = msg.mbf_find_object("!PARTY", "MBFE_BEGINNING") or \
                     msg.mbf_find_object("PARTY", "MBFE_BEGINNING")
                     
        if updateElem:
            
            addInfo = updateElem.mbf_find_object("!ADDITIONALINFO", "MBFE_BEGINNING")or \
                         updateElem.mbf_find_object("+ADDITIONALINFO", "MBFE_BEGINNING")
            addInfoFields = []
            addInfoFieldsName = 'BarCap_SMS_CP_SDSID'
            
            while addInfo:
                addInfoFieldName = addInfo.mbf_find_object("ADDINF_SPECNBR.FIELD_NAME", "MBFE_BEGINNING")
                addInfoValue = addInfo.mbf_find_object("!VALUE", "MBFE_BEGINNING")
                if addInfoFieldName:
                    if addInfoFieldName.mbf_get_value() == addInfoFieldsName and addInfoValue:
                        return False

                updateElem.mbf_remove_object()
                
                addInfo = updateElem.mbf_find_object("!ADDITIONALINFO", "MBFE_BEGINNING")or \
                         updateElem.mbf_find_object("+ADDITIONALINFO", "MBFE_BEGINNING")
                         
            return True

MessageHandlers = {
       "INSERT_TRADE": TradeInsertHandler(),
       "UPDATE_TRADE": TradeUpdateHandler(),
       "UPDATE_INSTRUMENT": InstrumentUpdateHandler(),
       "UPDATE_PARTY": PartyUpdateHandler(),
}

"""
*********************************************************************************************************************************
************************************************************* MAIN TMS HOOK *****************************************************
*********************************************************************************************************************************
"""

def TMS_Generate_Message(msg, src):
    # Get the type of message being passed
    msgTypeObject = msg.mbf_find_object("TYPE", "MBFE_BEGINNING")
    if msgTypeObject:
        msgType = msgTypeObject.mbf_get_value()

        # Is there a handler?
        msgHandler = MessageHandlers.get(msgType)
        if msgHandler:
            # Instantiate a message handler and create its message 
            # (__call__ enables us to treat the instance as a callable function.)
            return msgHandler(msg)
            
            
class ResponseMessageHandler(MessageHandler):

    def __call__(self, msg):
        # Get the element with trade id 
        tradeElem = self._getTradeElement(msg)
        if tradeElem:
            # Lookup the trade
            tradeId = int( tradeElem.mbf_find_object("TRDNBR", "MBFE_BEGINNING").mbf_get_value() )
            trade = ael.Trade[tradeId]

            if trade:
                factory = TMSResponseMsgFactory()
                if factory.supports(trade):
                    newMsg = CreateResponseMessage(factory, trade, self._getFieldName(msg), self._getTMSId(msg), self._getSource(msg))
                    return newMsg
        return msg
                    
    def _getMsgType(self, trade):
        return EnumOperation.UPDATE

    def _getTradeElement(self, msg):
        updateElem = msg.mbf_find_object("!TRADE", "MBFE_BEGINNING") or msg.mbf_find_object("TRADE", "MBFE_BEGINNING")
        return updateElem
            
    def _getAddInfoElement(self, msg):
        tradeElem = self._getTradeElement(msg)
        return tradeElem.mbf_find_object("!ADDITIONALINFO", "MBFE_BEGINNING") or tradeElem.mbf_find_object("ADDITIONALINFO", "MBFE_BEGINNING")
    
    def _getFieldName(self, msg):
        addInfoElem = self._getAddInfoElement(msg)
        return addInfoElem.mbf_find_object("ADDINF_SPECNBR.FIELD_NAME", "MBFE_BEGINNING").mbf_get_value() 
    
    def _getTMSId(self, msg):
        addInfoElem = self._getAddInfoElement(msg)
        return  addInfoElem.mbf_find_object("VALUE", "MBFE_BEGINNING").mbf_get_value()

    def _getSource(self, msg):
        updateElem = msg.mbf_find_object("SOURCE", "MBFE_BEGINNING")
        return updateElem.mbf_get_value()

"""
*********************************************************************************************************************************
********************************* Recieve modify TMS HOOK for FXSwaps************************************************************
*********************************************************************************************************************************
"""

def TMS_Generate_AckMessage(msg):
    msgHandler = ResponseMessageHandler()
    if msgHandler:
        return msgHandler(msg)
    return msg 

