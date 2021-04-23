import TMS_AMBA_Message
import os
import ael
import amb
import TMS_Functions_Common

''' ==========================================================================================================
    Purpose        : This Module will generate the XML for the recon between Front Arena and BarCap TMS,
                        : this recon is for FX Hedge trades and FX Options
    Department and Desk    :
    Requester        : Mathew Berry
    Developer        : Babalo Edwana
    CR Number        : TBO
    
    Changes            : Update Module for the Front Recon Extract to Retrieve all trades for the specified Trade Filter regardless if the trade type
                : has a Factory Class for Trade Feed as this will cause wrongly booked trades from being extracted and therefore not reconciled.
                : Added extra parameters for TMS_AMBA_Message.CreateTradeMessage(factory, trade, msgType,source,txnbr) as per HotFix for TradeFeed
                : due to Message delays.
    Date            : 12/04/2010
    Developer        : Babalo Edwana
    Requester        : Mathew Berry
    CR Number        : 282095
    
    Changes            : For FX Option trades Booked incorrectly, the Function TMS_AMBA_Message.CreateTradeMessage() fails because of assertion 
                                : of factory.supports(), since these trades are already booked in correctly. 
                : Added Import line for AMBA and also updated error log to include original error message
                
                : For FXSwap the Recon extract is extracting 2 trades per FxSwap Instrument which causes duplicate Trades in the Recon Extract.
                : Updated logic for FxSwap to extract one trade message same as Trade Feed. Only using FXSwap Near Leg to extract FXSwap Trade Message.
    Date            : 18/05/2010, 21/05/2010, 19/07/2010
    Developer        : Babalo Edwana
    Requester        : Mathew Berry
    CR Number        : 314825, 320945, 375319
    
    Changes            : Added logic to exclude expired trades for trade recon, inline with EMTradePublisher Config changes to exclude expired trades as well.
                : This is to reduce the size of the TMS extract file is growing large.
                : Logic in isExpired has been updated to check for expiry date less than today
                : For Currency instruments, must only eclude expired FarTrade, Near trade could be expired while Far Trade has not expired and in TMS the trade
                : will be expired only when the Far trade has expired.
    Date            : 09/09/2010, 15/09/2010, 18/10/2010
    Developer        : Babalo Edwana
    Requester        : Mathew Berry
    CR Number        : 429927,433209, 467753
 
=================================================================================================================== '''

AMBA_VERSION = "1.0"

def ael_main(ael_dict):

    ReportDate = ael_dict["ReportDate"]
    Server = ael_dict["Server"]
    TradeFilter = ael_dict["TradeFilter"]

    FX_TMS_Recon_Extract(Server, TradeFilter, ReportDate)

def getTradeFilters():
    tfs = [tf.fltid for tf in ael.TradeFilter]
    tfs.sort()
    return tfs

ael_variables = [('ReportDate', 'ReportDate', 'date', None, ael.date_today(), 1),
                  ('Server', 'Server', 'string', None, r'//services/frontnt/development/', 1),
                  ('TradeFilter', 'TradeFilter', 'string', getTradeFilters(), 'BVOE', 1)]

def getTrades(trade_filter):
    return [t.trdnbr for t in ael.TradeFilter[trade_filter].trades()]
    
def getFXTradeXML(factory, trade, msgType, source, txnbr):
    if factory:
        wrapper = factory.create(trade)
        
        if type(wrapper) == amb.mbf_object:
            return wrapper
        else:
            # Create a message for this trade
            msg = amb.mbf_start_message(
                        None,
                        msgType == TMS_AMBA_Message.EnumOperation.UPDATE and "UPDATE_TRADE" or "INSERT_TRADE",
                        AMBA_VERSION,
                        None,
                        source)
            
            msg.mbf_add_string('TXNBR', txnbr)
                       
            TMS_AMBA_Message._processElement(msg, wrapper)
            return msg

def isExpired(trade, repDate):
    instr = trade.insaddr
    if instr.instype == "Curr": 
        return CurrencyInsExpired(trade, repDate)
    else:
        if instr.exp_day < repDate:
            return True
    
    return False

def CurrencyInsExpired(trade, repDate):
    if trade:
        if trade.trade_process == 16384:
            acmTrade = TMS_Functions_Common.otherleg(trade)
            if acmTrade:
                    return ael.Trade[acmTrade.Oid()].value_day < repDate
        else:
            return trade.value_day < repDate

def FX_TMS_Recon_Extract(server, trade_filter, rep_date):
       
    FileDate = rep_date
    FileDate = FileDate.to_string('%Y%m%d')

    file_path = os.path.join(server, "FX_ABCAP_FRONTTMS_Extract_" + FileDate + ".xml")
    log_path = os.path.join(server, "FX_ABCAP_FRONTTMS_Extract_Log_" + FileDate + ".txt")
    
    outfile = open(file_path, 'w')
    Log = open(log_path, 'w')
    
    outfile.write('<?xml version="1.0"?>')
    outfile.write('<TRADES>')
    
    source='FRONTTMSRECON'
    txnbr = ''
    msgType = "INSERT_TRADE"
        
    tradeIds = getTrades(trade_filter)
    for trdnbr in tradeIds:
        try:
        
            trade = ael.Trade[trdnbr]
            instr = trade.insaddr
            
            if not isExpired(trade, rep_date):
                if instr.instype == "Curr" and trade.trade_process != 32768:
                    factory = TMS_AMBA_Message.SupportsTradeMessage(trade)
                    newMsg = TMS_AMBA_Message.CreateTradeMessage(factory, trade, msgType, source, txnbr)
                else:
                    factory = TMS_AMBA_Message._fxSupportsTradeMessage_(instr)
                    newMsg = getFXTradeXML(factory, trade, msgType, source, txnbr)
                
                if  newMsg:
                    msgExtract = "\n".join(newMsg.mbf_object_to_string_xml().split("\n")[1:])
                    outfile.write(msgExtract)
                
        except Exception, error:
            Log.write('Trade cannot be extracted - %s . Error: %s\n' %(trdnbr, error))
                      
    outfile.write('</TRADES>')
    outfile.close()
    Log.close()
    
    print file_path
