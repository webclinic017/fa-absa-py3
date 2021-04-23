import ael
import amb
import datetime
import string
import SAGEN_Resets
import TMS_Functions
import TMS_Config_Trade
import time
import SAGEN_str_functions
from TMS_AMBA_Message import MessageToString

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Name:           TMS_Recon_Template
#Purpose:        This AEL defines generation of XML for the FI recon between Front Arena and BarCap TMS
#Developer:      Neil Retief
#Create Date:    (unknown, possibly 2008-06-03)
#
#Developer:      Peter Kutnik
#Date:           2010-02-22
#Detail:         Changed trade expiry to days where date > exp_day
#                Made recon pick up trades not by TMS ID, but by whether they are considered for TMS 
#
#CR:		 342572
#Developer:    Babalo Edwana
#Date:           2010-06-15
#Detail:         Updated Logic for Action Recon Element for the trade, change precedence lowered Action new
#CR:
#Developer:     Babalo Edwana
#Date:          2010-11-12
#Purpose:       refactored code to use Modularity logic by implementing Functions
#Requester:     Mathew Berry
#
#CR:            154268 
#Developer:     Michal Spurny
#Date:          2012-04-25
#Purpose:       Add support for Combination trades and export cashflow currency
#Requester:     Mathew Berry   
#
#CR:            CHNG0001660484 
#Developer:     Jan Mach
#Date:          2014-01-23
#Purpose:       CREMW-48 added Swap
#
#CR:            CHNG0001961363
#Developer:     Michal Spurny
#Date:          2014-05-15
#Purpose:       CREMW-55 fix order for Combinations
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def TMS_Generate_XML(trdnbr):

    TObject = ael.Trade[(int)(trdnbr)]
    IObject = TObject.insaddr
                    
    #For combination All pseudo trades XMLS are returned in the string, else the trade XML returned
    TradeStr = ''
    if IObject.instype == 'Combination':
        CombIns = ael.CombinationLink.select('owner_insaddr = %d' % IObject.insaddr)
        CombIns = sorted(CombIns, key=lambda ins:ins.member_insaddr.insaddr)
        iCount = 1
        for ins in CombIns:
            instr = ins.member_insaddr
            if isInstrumentConsidered(instr):
                pseudoTrdNbr = (str)(TObject.trdnbr) + "." + (str)(iCount)
                TradeStr += TMS_Generate_XML_Helper(pseudoTrdNbr, TObject, instr, ins.weight, True)               
                iCount = iCount + 1
    else:        
        TradeStr = TMS_Generate_XML_Helper((str)(TObject.trdnbr), TObject, IObject)        
        
    return TradeStr   



def filterTradeXMLStrFromMsg(TradeMsg):
     
    Buffer = amb.mbf_create_buffer()
    TradeMsg.mbf_generate_xml(Buffer)
    TradeMsg_String = Buffer.mbf_get_buffer_data()
    if '<TRADE>' in TradeMsg_String:
        Final = SAGEN_str_functions.Substring(0, TradeMsg_String, TradeMsg_String.index('<TRADE>'), TradeMsg_String.index('</MESSAGE'))
    else:
        msgStr = MessageToString(TradeMsg)
        if '<TRADE>' in msgStr:
            Final = msgStr[msgStr.index('<TRADE>'): msgStr.index('</MESSAGE')]
        else:
            Final = ''      #MS23022012  
    return Final   

def TMS_Generate_XML_Helper(trdnbr, trdObj, instrObj, weight = 1.0, isCombination = False):
    
    TObject = trdObj
    IObject = instrObj

    Und_IObject = _getUnderlyingInstrument(TObject, IObject)
    LObject = _getLegs(IObject, Und_IObject)
    DateToday = TMS_Functions.Date()
            
    message = amb.mbf_start_message(None, "GENERATE_RECON_XML", "1.0", None, "AMBA_DEV")
    
    
            
    if ((not isCombination) and TMS_Config_Trade.isConsideredForTMS(TObject)) or (isCombination and isInstrumentConsidered(IObject)):
    
        Instrument = len(_mapInstrumentTypes(IObject)) > 0 and _mapInstrumentTypes(IObject)[0] or ""
        TMS_Instrument = len(_mapInstrumentTypes(IObject)) > 0 and _mapInstrumentTypes(IObject)[1] or ""
        
        Trade_msg = message.mbf_start_list("TRADE")
        
        _getTradeDetails(Trade_msg, TObject, IObject, Und_IObject, DateToday, Instrument, trdnbr)
                
        if TObject.status != 'Terminated' and TObject.status != 'Void':
            _getInstrumentDetails(Trade_msg, TObject, IObject, Und_IObject, LObject, TMS_Instrument, Instrument, DateToday, isCombination, weight, trdnbr)
        else:
            _getBlankInstrumentDetails(Trade_msg, TMS_Instrument)
                
        Trade_msg.mbf_end_list()
    else:
        if string.lower(TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Vanilla_Exotic_Check')) == 'jj' and (not isCombination):
            _getQASysTrades(message, TObject, IObject, LObject)
            
                        
    FinalMsg = message.mbf_end_message()
    #MS22022012 trade string conversion added
    FinalStr = filterTradeXMLStrFromMsg(FinalMsg)
    return FinalStr
    
                                

def _mapTradeAction(TObject, IObject, Und_IObject, DateToday):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function Maps Front Arena Trade Status to TMS Trade Action
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
    if TObject.status == 'Void':
        Action = 'Cancel'
    elif TObject.status == 'Terminated':
        Action = 'Termination'
    elif (IObject.exp_day is not None) and (IObject.exp_day.to_string('%Y-%m-%d') < DateToday): #MS 23022012
        Action = 'Mature'
    elif IObject.und_instype != 'None':
        if (TMS_Functions.Get_Global_Reset_Day(Und_IObject.insaddr, DateToday) == DateToday) or \
           (TMS_Functions.Get_Global_Reset_Day(Und_IObject.insaddr, DateToday) == time.strftime("%Y-%m-%d", time.localtime(TObject.updat_time))):
            Action = 'Reset'
        else: 
            Action = 'Amend'
    elif IObject.und_instype == 'None':
        if (TMS_Functions.Get_Global_Reset_Day(IObject.insaddr, DateToday) == DateToday) or \
           (TMS_Functions.Get_Global_Reset_Day(IObject.insaddr, DateToday) == time.strftime("%Y-%m-%d", time.localtime(TObject.updat_time))):
            Action = 'Reset'
        else:
            Action = 'Amend'
    elif TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Vanilla_Version') == '1':
        Action = 'New'
    else:
        Action = 'Amend'
            
    return Action
        
def _mapTradeStatus(TObject, IObject, DateToday):

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function Maps Front Arena Trade Status to TMS Trade Status
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    if TObject.status == 'Void':
        State = 'Cancelled'
    elif (IObject.exp_day is not None) and (IObject.exp_day.to_string('%Y-%m-%d') < DateToday): #MS23022012
        State = 'Expired'
    elif TObject.status == 'Terminated':
        State = 'Expired'
    elif TObject.status == 'FO Confirmed':
        State = 'AwaitingVerification'
    else:
        State = 'Verified'
            
    return State
                
def _mapInstrumentTypes(IObject):

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function Maps Front Arena Instrument Types to TMS Instrument Types
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    ins_types = []
    
    if IObject.instype in ('FRA', 'Swap', 'Cap', 'Floor'):
        if IObject.instype in ('Cap', 'Floor'):
            ins_types.append('IRG')
            ins_types.append('IRG')
        else:
            ins_types.append(IObject.instype)
            ins_types.append(IObject.instype)
    elif IObject.instype == 'Option':
        ins_types.append(IObject.und_instype == 'Swap' and 'IRSwaption' or 'IRG')
        ins_types.append(IObject.und_instype == 'Swap' and 'IRSwaption' or 'IRG')
    elif IObject.instype in ('CurrSwap', 'FxSwap'):
        ins_types.append(IObject.instype == 'FxSwap' and 'FxSwap' or 'CurrSwap')
        ins_types.append('Swap')
            
    return ins_types
                       
        
def isInstrumentConsidered(IObject):

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function checks if the Instruments for the Combination trades are considered for TMS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    considered = False
    
    if IObject.instype in ('FRA', 'Swap', 'Cap', 'Floor'):
        considered = True
    elif IObject.instype == 'Option':
        considered = True
    elif IObject.instype in ('CurrSwap', 'FxSwap'):
        considered = True
        
    return considered
    
def _getTradeDetails(Trade_msg, TObject, IObject, Und_IObject, DateToday, Instrument, trdnbr):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function populates the Common TradeDetails for all Instrument Types
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    Trade_msg.mbf_add_string("TrdNbr", trdnbr)
    Trade_msg.mbf_add_string("TMSId", len(string.lower(TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Vanilla_ID'))) > 0 and \
                            string.lower(TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Vanilla_ID')) or ' ')
    Trade_msg.mbf_add_string("TMS_Version_ID", TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Vanilla_Version'))
    
    C_Date = time.strftime("%Y-%m-%d", time.localtime(TObject.creat_time))
    C_Time = time.strftime("%H:%M:%S", time.localtime(TObject.creat_time))
    Trade_msg.mbf_add_string("TradeDate", C_Date + 'T' + C_Time)

    if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TObject.updat_time)) > time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(IObject.updat_time)):
        Trade_msg.mbf_add_string("UpdateUser", TMS_Functions.Get_BarCap_User_ID(TObject.updat_usrnbr))
    else:
        Trade_msg.mbf_add_string("UpdateUser", TMS_Functions.Get_BarCap_User_ID(IObject.updat_usrnbr))
    
    #Add the relevant Actions & States
    Trade_msg.mbf_add_string("Action", _mapTradeAction(TObject, IObject, Und_IObject, DateToday))
    Trade_msg.mbf_add_string("State", _mapTradeStatus(TObject, IObject, DateToday))
    
    Trade_msg.mbf_add_string("Trader", TMS_Functions.Get_BarCap_User_ID(TObject.trader_usrnbr))
    Trade_msg.mbf_add_string("CP", TMS_Functions.Get_BarCap_SDS_ID(TObject.counterparty_ptynbr))

    #Pass both the Portfolio name as well as the SMS Book ID
    Trade_msg.mbf_add_string("Book_ID", TMS_Functions.Get_BarCap_Book_ID(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book", TMS_Functions.Get_BarCap_Strategy_Book_Name(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book_ID", TMS_Functions.Get_BarCap_Strategy_Book_ID(TObject.prfnbr))
    Trade_msg.mbf_add_string("Acquirer", TMS_Functions.Get_BarCap_SDS_ID(TObject.acquirer_ptynbr))
    
    if Instrument:
        _getBrokerDetails(Trade_msg, TObject, Instrument)
        
def _getInstrumentDetails(Trade_msg, TObject, IObject, Und_IObject, LObject, TMS_Instrument, Instrument, DateToday, isCombination, weight, trdnbr):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Functions populates the Instrument details, and the logic is implemented per Instrument Type
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    Inst_msg = Trade_msg.mbf_start_list("INSTRUMENT")
    Inst_msg.mbf_add_string("Instype", TMS_Instrument)
    
    if TMS_Instrument == 'IRG':
        Inst_msg.mbf_add_string("exercise_type", '')
        Inst_msg.mbf_add_string("settlement", '')
        Inst_msg.mbf_add_string("Und_Instype", '')
    else:
        #Get the instrument objects
        if IObject.und_instype != 'None':
            Inst_msg.mbf_add_string("Und_Instype", Und_IObject.instype)
        else:
            Inst_msg.mbf_add_string("Und_Instype", '')
            
        #Exercise_Type
        if IObject.exercise_type != 'None':
            Inst_msg.mbf_add_string("exercise_type", IObject.exercise_type)
        else:
            Inst_msg.mbf_add_string("exercise_type", '')
        
        #Settlement
        if IObject.settlement != 'None':
            if IObject.settlement == 'Physical Delivery':
                Settlement = 'Asset'
            else:
                Settlement = 'Cash'
                
            Inst_msg.mbf_add_string("settlement", Settlement)
        else:
            Inst_msg.mbf_add_string("settlement", '')
            
    #OTC or Exchange mapping
    if IObject.otc == 1:
        otc = 'OTC'
    else:
        otc = 'Exchange'
    
    Inst_msg.mbf_add_string("otc", otc)
    
    if TMS_Instrument == 'IRSwaption':
        if IObject.exercise_type != 'Bermudan':
            Inst_msg.mbf_add_string("InsCurr", IObject.display_id('curr'))
            Inst_msg.mbf_add_string("exp_day", IObject.exp_day.to_string('%Y-%m-%d'))
        else:
            Inst_msg.mbf_add_string("InsCurr", IObject.display_id('curr'))
    
    #Display only the call option attribute for IRG instruments
    if TMS_Instrument == 'IRG':
        if IObject.instype != 'Cap' and IObject.instype != 'Floor':
            if IObject.call_option == 1:
                Call_Put = 'Call'
            else:
                Call_Put = 'Put'
            
            Inst_msg.mbf_add_string("call_option", Call_Put)
    
    
    
    _getLegDetails(Inst_msg, TObject, IObject, Und_IObject, LObject, TMS_Instrument, Instrument, DateToday, isCombination, weight, trdnbr)
        

def _getBlankInstrumentDetails(Trade_msg, TMS_Instrument):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# When the trade in question is not supported by the Front TMS TradeFeed, this fucntion will return an empty Instrument tag
# with minimal Instrument details.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #Start Blank Instrument list
    Inst_msg = Trade_msg.mbf_start_list("INSTRUMENT")
    
    #Generate the correct InsType
    if TMS_Instrument == 'IRSwaption':
        Inst_msg.mbf_add_string("Instype", 'IRSwaption')
    elif TMS_Instrument == 'Swap':
        Inst_msg.mbf_add_string("Instype", 'Swap')
    elif TMS_Instrument == 'FRA':
        Inst_msg.mbf_add_string("Instype", 'FRA')
    elif TMS_Instrument == 'IRG':
        Inst_msg.mbf_add_string("Instype", 'IRG')
    else:
        Inst_msg.mbf_add_string("Instype", ' ')
            
    Inst_msg.mbf_end_list()


def _getLegDetails(Inst_msg, TObject, IObject, Und_IObject, LObject, TMS_Instrument, Instrument, DateToday, isCombination, weight, trdnbr):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function populates the Leg Details for all the Legs within an Instrument
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    Legs = []
        
    for l in LObject:
        L_Tuple = (l.type, l)
        Legs.append(L_Tuple)
    
    Legs.sort()
        
    for Leg in Legs:
    
        
        l = Leg[1]
        
        #Start Leg list
        Leg_msg = Inst_msg.mbf_start_list("LEG")
        
        #Get the call_option attribute for Cap's and Floors
        if (IObject.instype == 'Cap' or IObject.instype == 'Floor'):
            if l.type == 'Cap':
                Inst_msg.mbf_add_string("call_option", 'Call')
            elif l.type == 'Floor':
                Inst_msg.mbf_add_string("call_option", 'Put')
            else:
                Inst_msg.mbf_add_string("call_option", 'Call')
                
        #Include for all legs of the instrument
        Leg_msg.mbf_add_string("L_Curr", l.display_id('curr'))
        
        if IObject.instype in ('Floor', 'Cap'):
            Leg_msg.mbf_add_string("Type", 'Float')
        else:
            Leg_msg.mbf_add_string("Type", l.type)
        
        Leg_msg.mbf_add_string("start_day", l.start_day.to_string('%Y-%m-%d'))
        Leg_msg.mbf_add_string("end_day", l.end_day.to_string('%Y-%m-%d'))
        
        #Only for legs not equal to fixed leg
        if l.type != 'Fixed':
            Leg_msg.mbf_add_string("ResetCal", TMS_Functions.Get_BarCap_Calendar(l.display_id('reset_calnbr'), l.display_id('reset2_calnbr'), l.display_id('reset3_calnbr'), l.display_id('reset4_calnbr'), l.display_id('reset5_calnbr')))
            Leg_msg.mbf_add_string("PayCal", TMS_Functions.Get_BarCap_Calendar(l.display_id('pay_calnbr'), l.display_id('pay2_calnbr'), l.display_id('pay3_calnbr'), l.display_id('pay4_calnbr'), l.display_id('pay5_calnbr')))
        else:
            Leg_msg.mbf_add_string("PayCal", TMS_Functions.Get_BarCap_Calendar(l.display_id('pay_calnbr'), l.display_id('pay2_calnbr'), l.display_id('pay3_calnbr'), l.display_id('pay4_calnbr'), l.display_id('pay5_calnbr')))
        
        if l.spread != 'None' and l.type != 'Fixed':
            if TMS_Instrument == 'FRA':
                Leg_msg.mbf_add_double("Spread", ((l.fixed_rate*-1)/100))
            else:
                Leg_msg.mbf_add_double("Spread", l.spread/100)
        
        #Fixed Rate
        if l.type == 'Fixed':
                Leg_msg.mbf_add_double("fixed_rate", l.fixed_rate)
        
        Leg_msg.mbf_add_double("LegNominal", _getLegNominal(TObject, IObject, Und_IObject, Instrument, TMS_Instrument, l, isCombination, weight))
                
        #Convert the Front Arena daycount method to YearPart and DayPart
        #YearPart
        Leg_msg.mbf_add_string("YearPart", TMS_Functions.DayCount_YearPart_Convert(l.daycount_method))
        #DayPart
        Leg_msg.mbf_add_string("DayPart", TMS_Functions.DayCount_DayPart_Convert(l.daycount_method))
        
        #Convert the Pay Day Method
        Leg_msg.mbf_add_string("RollConvention", TMS_Functions.Pay_Day_Method_Convert(l.pay_day_method))

        #Convert the Reset Day Method
        if l.type != 'Fixed':
            Leg_msg.mbf_add_string("FixingRollConvention", TMS_Functions.Pay_Day_Method_Convert(l.reset_day_method))
        #Get the pay_day offset    
        Leg_msg.mbf_add_int("PaymentDelay", getattr(l, 'pay_day_offset.count'))
        #----------------------------------------------------------
        #Create an if statement to get the value of pay and receive
        Leg_msg.mbf_add_string("payleg", _getPayleg(TObject, TMS_Instrument, Instrument, l, isCombination, weight))
                
        _getCashFlowDetails(Leg_msg, TObject, IObject, Und_IObject, TMS_Instrument, Instrument, DateToday, l, isCombination, weight)
        
        needPBAPayments = (isCombination and trdnbr[-2:]=='.1') or (not isCombination) #Added to first combination trade
        if needPBAPayments:
            _getPremiumBrokeragePayments(Leg_msg, TObject, IObject, TMS_Instrument, l, isCombination, weight)
            _getAdditionalPayments(Leg_msg, TObject, IObject, TMS_Instrument, Instrument, l, isCombination, weight)
        
    Inst_msg.mbf_end_list()
    Leg_msg.mbf_end_list()
                
                                                
                
def _getCashFlowDetails(Leg_msg, TObject, IObject, Und_IObject, TMS_Instrument, Instrument, DateToday, l,  isCombination, weight):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function populates cashflow details for all cashflows that belong to the supplied Leg
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    wfactor = isCombination and weight or 1.0    
    CFS = []
    
    for c in l.cash_flows():
        CF_Tuple = (c.pay_day, c.end_day, c)
        CFS.append(CF_Tuple)

    #Sort the cashflows
    TMS_Functions.SortListOfListsByCriteria(CFS, [0, 1], [-1, 1])
    #Add all relevant columns for CashFlows

    for c in CFS:
        cf = c[2]
        
        if cf.type != 'Fixed Amount':
            reset_rate = 0
            #Start cashflow list
            CF_msg = Leg_msg.mbf_start_list("CASHFLOW")
            
            CF_msg.mbf_add_string("CF_Key", cf.end_day.to_string('%Y-%m-%d') + '_Interest')
            CF_msg.mbf_add_string("start_day", cf.start_day.to_string('%Y-%m-%d'))
            CF_msg.mbf_add_string("end_day", cf.end_day.to_string('%Y-%m-%d'))
            
            #For Option on FRA's the pay day should be the end day of teh cashflow
            if IObject.instype == 'Option' and IObject.und_instype == 'FRA':
                CF_msg.mbf_add_string("pay_day", cf.end_day.to_string('%Y-%m-%d'))
            else:
                CF_msg.mbf_add_string("pay_day", cf.pay_day.to_string('%Y-%m-%d'))
                    
            #Pass the cashflow rate only for fixed legs
            if l.type == 'Fixed':
                CF_msg.mbf_add_double("CFRate", cf.rate)
                    
            #Pass the projected cashflow amount only for float legs
            if cf.spread != 'None' and l.type != 'Fixed':
                if TMS_Instrument == 'FRA':
                    CF_msg.mbf_add_double("spread", ((l.fixed_rate*-1)/100))
                else:
                    CF_msg.mbf_add_double("spread", cf.spread/100)
            
            #Work out the correct cashflow amount
            if TMS_Instrument == 'IRSwaption':
                CF_msg.mbf_add_double("CFNominal", TObject.quantity * IObject.contr_size * cf.nominal_factor * wfactor)
            elif Instrument == 'FXSwap':
                CF_msg.mbf_add_double("CFNominal", cf.projected_cf() * TObject.quantity * wfactor)
            elif Instrument == 'Swap':
                isAverage = l.reset_type == "Weighted" and 1 or 0
                resetDay = isAverage and cf.end_day or cf.start_day
                
                #Calc reset rate - this will happen here as we will only produce a proj cashflow if the reset
                #has fixed else we will output the nominal
                reset_rate = 0
                if isAverage:
                    reset_rate = cf.known_cashflow() and cf.period_rate(cf.start_day, cf.end_day) or 0
                else:
                    if len(cf.resets()) >= 1:
                        r = cf.resets()[0]
                        reset_rate = r.value

                #If our rate has been fixed send through the projected cashflow through to TMS else send
                #through the cashflow nominal.
                cf_amt = reset_rate and cf.known_cashflow() * TObject.quantity * wfactor or abs(IObject.contr_size * cf.nominal_factor * TObject.quantity * wfactor)
                CF_msg.mbf_add_double("CFNominal", cf_amt)
            elif Instrument == 'CurrSwap':
                if cf.start_day.to_string('%Y-%m-%d') <= DateToday and l.type == 'Float':
                    CF_msg.mbf_add_double("CFNominal", cf.projected_cf() * TObject.quantity * wfactor)
                else:
                    CF_msg.mbf_add_double("CFNominal", abs(TObject.quantity * IObject.contr_size * cf.nominal_factor * l.nominal_factor * wfactor))
            elif Instrument == 'FRA':
                if cf.start_day.to_string('%Y-%m-%d') <= DateToday and l.type == 'Float':
                    CF_msg.mbf_add_double("CFNominal", cf.projected_cf() * TObject.quantity * wfactor)
                else:
                    CF_msg.mbf_add_double("CFNominal", abs(TObject.quantity * IObject.contr_size * cf.nominal_factor * wfactor))
            elif IObject.instype == 'Option' and Und_IObject.instype == 'FRA':
                CF_msg.mbf_add_double("CFNominal", abs(IObject.contr_size * TObject.quantity * wfactor))
            else:
                CF_msg.mbf_add_double("CFNominal", abs(TObject.quantity * IObject.contr_size * cf.nominal_factor * wfactor))
            
            CF_msg.mbf_add_string("CF_Currency", l.curr.insid) 
            _getResetFixingDetails(CF_msg, TMS_Instrument, DateToday, l, reset_rate, cf)
            
            CF_msg.mbf_end_list()
        #MS 20/02/2012, only for FxSwap and CurrSwap        
        if cf.type == 'Fixed Amount' and Instrument in ('FxSwap', 'CurrSwap', 'Swap'):
            #Start Payment list
            CF_msg = Leg_msg.mbf_start_list("CASHFLOW")
            CF_msg.mbf_add_string("pay_day", cf.pay_day.to_string('%Y-%m-%d'))
            CF_msg.mbf_add_double("CFNominal", cf.projected_cf() * TObject.quantity * wfactor)
            CF_msg.mbf_add_string("CF_Key", cf.pay_day.to_string('%Y-%m-%d') + '_' + 'Exchange')
            CF_msg.mbf_add_string("CF_Currency", l.curr.insid)
            #End Payment list
            CF_msg.mbf_end_list()
                                        
        
def _getPayleg(TObject, TMS_Instrument, Instrument, l, isCombination, weight):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function returns the paytype for the Leg specified
# It returns a string which specifies whether the Leg is a payleg or receiveleg
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    wfactor = isCombination and weight or 1.0       
       
    if (Instrument == 'CurrSwap' or Instrument == 'FRA' or Instrument == 'Swap'):
        if ((l.payleg == 1 and TObject.quantity * wfactor > 0) or (l.payleg == 0 and TObject.quantity * wfactor < 0)):
            PayRec = 'Pay'
        else:
            PayRec = 'Receive'
    elif TMS_Instrument == 'IRSwaption':
        #-----------------------------------------------------------
        CFS = []
        
        for c in l.cash_flows():
            CF_Tuple = (c.pay_day, c.end_day, c)
            CFS.append(CF_Tuple)

        #Sort the cashflows
        CFS.sort()
        
        #Add all relevant columns for CashFlows
        count = 0
        
        while count < 1:
            cf = CFS[count][2]
    
            count = count + 1
            
            if (TObject.quantity * cf.projected_cf() * wfactor) < 0:
                PayRec = 'Pay'
            else:
                PayRec = 'Receive'
               
            
        #----------------------------------------------------------
    elif Instrument == 'FxSwap':  #MS29022012
        if ((l.payleg == 1 and TObject.quantity * wfactor > 0) or (l.payleg == 0 and TObject.quantity * wfactor < 0)):
            PayRec = 'Pay'
        else:
            PayRec = 'Receive'
        
    else:
        if (TObject.quantity * wfactor) < 0:
            PayRec = 'Pay'
        else:
            PayRec = 'Receive'
    
    return PayRec 	
        
def _getLegNominal(TObject, IObject, Und_IObject, Instrument, TMS_Instrument, l, isCombination, weight):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This fucntion calculates the LegNominal Amount for the Leg supplied
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    #Work out the correct Leg Nominal amount
    wfactor = isCombination and weight or 1.0
    
    if TMS_Instrument == 'IRSwaption':
        return (TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor)                 
    elif Instrument == 'FxSwap':
        return (TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor) #MS29022012
    elif Instrument == 'Swap':
        return (abs(TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor))
    elif Instrument == 'CurrSwap':
        return (abs(TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor))
    elif Instrument == 'FRA':
        return (TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor)
    elif IObject.instype == 'Option' and Und_IObject.instype == 'FRA':
        return (abs(IObject.contr_size * TObject.quantity* wfactor) )
    else:
        return (abs(TObject.quantity * IObject.contr_size * l.nominal_factor * wfactor))
        

def _getBrokerDetails(Trade_msg, TObject, Instrument):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function populates the Broker details if there is a brokerage fee associated with the trade
# This is the Broker Fee on the face of the trade and not the Broker fee added as additional payments
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    if Instrument in ('IRSwaption', 'IRG', 'CurrSwap', 'Swap'):
        list=[]
        for P in TObject.payments():
            if P.type == 'Broker Fee':
                PayM = (P.type, P.ptynbr)
                list.append(PayM)
        
        list.sort()
        if TObject.broker_ptynbr:
            Trade_msg.mbf_add_string("Broker", TMS_Functions.Get_BarCap_SDS_ID(TObject.broker_ptynbr))
        else:
            if list:
                Trade_msg.mbf_add_string("Broker", TMS_Functions.Get_BarCap_SDS_ID(list[0][1]))
            else:
                Trade_msg.mbf_add_string("Broker", '0')
                                
        
def _getUnderlyingInstrument(TObject, IObject):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function returns the underlying instrument for a derivative instrument
#---MS-21022012--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    if IObject:
        if IObject.und_instype != 'None':
            return ael.Instrument[IObject.und_insaddr.insaddr]   
        else:
            return ''

def _getLegs(IObject, Und_IObject):
                
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function returns all the legs associated with an instrument or the underlying instrument if the instrument supplied is a Derivative Instrument.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    if IObject.und_instype != 'None':
        return ael.Leg.select('insaddr = %d' % Und_IObject.insaddr)
    else:
        return ael.Leg.select('insaddr = %d' % IObject.insaddr)
                
def _getResetFixingDetails(CF_msg, TMS_Instrument, DateToday, l, reset_rate, cf):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function returns the Reset Fixing details for Interrest Rate Derivative Instruments
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if TMS_Instrument == 'IRG' and l.reset_type == 'Weighted':
        if cf.end_day.to_string('%Y-%m-%d') <= DateToday:
            CF_msg.mbf_add_double("reset_fixing_rate", cf.forward_rate()*100)
        else:
            CF_msg.mbf_add_string("reset_fixing_rate", 0)

        CF_msg.mbf_add_string("reset_day", cf.start_day.to_string('%Y-%m-%d'))
        CF_msg.mbf_add_string("reset_start_day", cf.start_day.to_string('%Y-%m-%d'))
        CF_msg.mbf_add_string("reset_end_day", cf.end_day.to_string('%Y-%m-%d'))
            
    elif TMS_Instrument == 'Swap' and l.reset_type == "Weighted": #Handle Prime swaps differently.
        #Has our cashflow been fixed yet?
        if reset_rate:
            CF_msg.mbf_add_double("reset_fixing_rate", reset_rate)
        else:
            CF_msg.mbf_add_string("reset_fixing_rate", "")
            
        CF_msg.mbf_add_string("reset_day", cf.end_day.to_string('%Y-%m-%d'))
        CF_msg.mbf_add_string("reset_start_day", cf.start_day.to_string('%Y-%m-%d'))
        CF_msg.mbf_add_string("reset_end_day", cf.end_day.to_string('%Y-%m-%d'))                       
            
    else:
        for r in cf.resets():
            #Start reset list
            if ((r.value == 0) or (TMS_Instrument == 'IRSwaption')):
                reset_val = ''
            else:
                if r.day.to_string('%Y-%m-%d') <= DateToday:
                    reset_val = TMS_Functions.ValueCheck(r.value)
                else:
                    reset_val = ''
                                    
            CF_msg.mbf_add_string("reset_fixing_rate", string.upper(reset_val))
            CF_msg.mbf_add_string("reset_day", r.day.to_string('%Y-%m-%d'))
            CF_msg.mbf_add_string("reset_start_day", r.start_day.to_string('%Y-%m-%d'))
            CF_msg.mbf_add_string("reset_end_day", r.end_day.to_string('%Y-%m-%d'))
            
            
def _addCashFlowMsgToLegMsg(Leg_msg, PayDayDateObj, nominalValue, keySuffixStr, currId):
    CF_msg = Leg_msg.mbf_start_list("CASHFLOW")
    CF_msg.mbf_add_string("pay_day", PayDayDateObj.to_string('%Y-%m-%d'))
    CF_msg.mbf_add_double("CFNominal", nominalValue)
    CF_msg.mbf_add_string("CF_Key", PayDayDateObj.to_string('%Y-%m-%d') + keySuffixStr + TMS_Functions.ValueCheck(round(nominalValue)))
    CF_msg.mbf_add_string("CF_Currency", currId)
    CF_msg.mbf_end_list()
    
                        
def _getPremiumBrokeragePayments(Leg_msg, TObject, IObject, TMS_Instrument, l, isCombination, weight):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function populates the Premium and Broker Fee on the face of the trade for the corresponding Leg as a cashflow.
# This excludes any Premium or Broker Fee Added as Additional payments.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    wfactor = isCombination and weight or 1.0    
    if TMS_Instrument == 'IRG':
        if TObject.premium:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.premium, '_' + 'Premium_', TObject.curr.insid)            
                
        #If a brokerage exists - send it through
        if TObject.fee:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.fee, '_' + 'Brokerage_', TObject.curr.insid)            
                    
    elif TMS_Instrument == 'IRSwaption':
        #-----------------------------------------------------------
        #Get a list of all the cashflows for pay and receive calcs.
        #Get the value of the current cashflows projected cashflow
        CFS = []
        
        for c in l.cash_flows():
            CF_Tuple = (c.pay_day, c.end_day, c)
            CFS.append(CF_Tuple)
                
        #Sort the cashflows
        CFS.sort()
        
        #Add all relevant columns for CashFlows
        count = 0
        
        while count < 1:
            cf = CFS[count][2]
            
            count = count + 1
            
            if (TObject.quantity * cf.projected_cf()* wfactor) < 0:
                if TObject.premium:                    
                    _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.premium, '_' + 'Premium_', TObject.curr.insid)                     
                        
                #If a brokerage exists - send it through
                if TObject.fee:                    
                    _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.fee, '_' + 'Brokerage_', TObject.curr.insid)                    
                                    
    elif TMS_Instrument == 'FRA':
        if TObject.premium:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.premium, '_' + 'Premium_', TObject.curr.insid)            
                
        #If a brokerage exists - send it through
        if TObject.fee:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.fee, '_' + 'Brokerage_', TObject.curr.insid)            

    elif ((l.payleg == 1 and TObject.quantity * wfactor > 0) or (l.payleg == 0 and TObject.quantity * wfactor < 0)):
        if TObject.premium:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.premium, '_' + 'Premium_', TObject.curr.insid)             
        
        #If a brokerage exists - send it through
        if TObject.fee:            
            _addCashFlowMsgToLegMsg(Leg_msg, TObject.value_day, TObject.fee, '_' + 'Brokerage_', TObject.curr.insid)            
                        
def _getAdditionalPayments(Leg_msg, TObject, IObject, TMS_Instrument, Instrument, l, isCombination, weight):
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function icnludes all teh additional payments as cashflow to their respective legs.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    wfactor = isCombination and weight or 1.0    
    if Instrument == 'Swap':
        for p in TObject.payments():
            if p.display_id('curr') == l.display_id('curr'):
                if ((l.payleg == 1 and TObject.quantity * wfactor > 0) or (l.payleg == 0 and TObject.quantity * wfactor < 0)):                    
                    _addCashFlowMsgToLegMsg(Leg_msg, p.payday, p.amount, '_' + p.type + '_', p.curr.insid)                    
                            
            else:
                if ((l.payleg == 1 and TObject.quantity * wfactor > 0) or (l.payleg == 0 and TObject.quantity * wfactor < 0)):                    
                    _addCashFlowMsgToLegMsg(Leg_msg, p.payday, p.amount, '_' + p.type + '_', p.curr.insid)                     
                                    
    elif TMS_Instrument == 'IRSwaption':
        for p in TObject.payments():
            if p.display_id('curr') == l.display_id('curr'):
                #-----------------------------------------------------------
                #Get a list of all the cashflows for pay and receive calcs.
                #Get the value of the current cashflows projected cashflow
                CFS = []
                
                for c in l.cash_flows():
                    CF_Tuple = (c.pay_day, c.end_day, c)
                    CFS.append(CF_Tuple)
                        
                #Sort the cashflows
                CFS.sort()
                
                #Add all relevant columns for CashFlows
                count = 0
                
                while count < 1:
                    cf = CFS[count][2]
                    
                    count = count + 1
                    
                    if (TObject.quantity * cf.projected_cf() * wfactor ) < 0:                        
                        #if ((IObject.call_option == 0 and l.type == 'Float') or (IObject.call_option == 1 and l.type == 'Fixed')):                        
                        _addCashFlowMsgToLegMsg(Leg_msg, p.payday, p.amount, '_' + p.type + '_', p.curr.insid)                        
            else:
                if ((IObject.call_option == 0 and l.type == 'Float') or (IObject.call_option == 1 and l.type == 'Fixed')):                    
                    _addCashFlowMsgToLegMsg(Leg_msg, p.payday, p.amount, '_' + p.type + '_', p.curr.insid)                    
    else:
        for p in TObject.payments():
            if p.display_id('curr') == l.display_id('curr'):                
                _addCashFlowMsgToLegMsg(Leg_msg, p.payday, p.amount, '_' + p.type + '_', p.curr.insid)                 
                                
def _getQASysTrades(message, TObject, IObject, LObject):

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Function handles QASys trades.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Trade_msg = message.mbf_start_list("TRADE")
    
    Trade_msg.mbf_add_string("TrdNbr", string.lower(TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Exotic_ID')))
    Trade_msg.mbf_add_string("TMSId", string.lower(TMS_Functions.Get_Trade_TMS_ID(TObject.trdnbr, 'Exotic_ID')))
    Trade_msg.mbf_add_string("Trader", TMS_Functions.Get_BarCap_User_ID(TObject.trader_usrnbr))
    Trade_msg.mbf_add_string("CP", TMS_Functions.Get_BarCap_SDS_ID(TObject.counterparty_ptynbr))
    
    #Pass both the Portfolio name as well as the SMS Book ID
    Trade_msg.mbf_add_string("Book_ID", TMS_Functions.Get_BarCap_Book_ID(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book", TMS_Functions.Get_BarCap_Strategy_Book_Name(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book_ID", TMS_Functions.Get_BarCap_Strategy_Book_ID(TObject.prfnbr))
    # MS22022012NoState Trade_msg.mbf_add_string("State", TObject.status)
    
    Inst_msg = Trade_msg.mbf_start_list("INSTRUMENT")
    
    #Generate the correct InsType
    Inst_msg.mbf_add_string("Instype", 'QASys')
    
    #Create the third list - LEG
    #Create a list object with the legs in so that legs can be sorted on type
    Legs = []
    
    for l in LObject:
        L_Tuple = (l.type, l)
        Legs.append(L_Tuple)
            
    #Sort the cashflows
    Legs.sort()
    
    #Leg will be a child of Instrument
    for Leg in Legs:
        l = Leg[1]
        
        #Start Leg list
        Leg_msg = Inst_msg.mbf_start_list("LEG")
        
        #Currency
        Leg_msg.mbf_add_string("L_Curr", l.display_id('curr'))
        
        #Start & End Day
        Leg_msg.mbf_add_string("start_day", l.start_day.to_string('%Y-%m-%d'))
        Leg_msg.mbf_add_string("end_day", l.end_day.to_string('%Y-%m-%d'))
        
        #Pay or Receive
        if ((l.payleg == 1 and TObject.quantity > 0) or (l.payleg == 0 and TObject.quantity < 0)):
                PayRec = 'Pay'
        else:
                PayRec = 'Receive'
        
        Leg_msg.mbf_add_string("payleg", PayRec)
        
        #Nominal
        Leg_msg.mbf_add_double("LegNominal", abs(TObject.quantity * IObject.contr_size * l.nominal_factor))
        
        Leg_msg.mbf_end_list()
    
    Trade_msg.mbf_end_list()
    Inst_msg.mbf_end_list()
    
        
	
