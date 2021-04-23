#------------------------------------------------------------------------------
#Name:           TMS_Functions
#Purpose:        This AEL will be used for the Front Arena to TMS trade feed. 
#                The AEL will contain all the functions used for data retrieval 
#                as well as for mapping purposes.
#Developer:      Neil Retief
#Create Date:    2008-06-03
#
#Changes
#
#Developer:      Peter Kutnik
#Date:           2010-03-05
#Detail:         Get_Trade_TMS_ID: Changed lookup from optional_key to 
#       add_info('TMS_Trade_Id')
#
#Developer:      Peter Kutnik
#Date:           2010-03-11
#Detail:         Get_Trade_TMS_ID: Added reversion of lookup to optional_key
#
#Developer:      Jan Mach
#Date:           2011-07-05
#Detail:         Updated to add functionality needed for DIRExT representation of Bermudans and cash-settled swaptions
#------------------------------------------------------------------------------

import ael
import SAGEN_Resets
import amb
import SAGEN_Functions
import SAGEN_str_functions
import time
import SANLD_NOMINALCURR
import datetime


#Define a date for which all values will be macthed against
def Date ():
    return time.strftime("%Y-%m-%d", time.localtime())

def Expired_Date ():
    #This date has been hard coded in order for trades to be sent through after this expiry date, no trades before this date will be sent to TMS
    return '2008-05-30'

def _ReformatLocalTimeDate(date, format):
    return time.strftime(format, date)

def _ReformatTimeDate(date, format):
    return time.strftime(format, time.localtime(date))

def _ReformatStrDate(date, format):
    return date

def _ReformatAELDate(date, format):
    return date.to_string(format)

def ReformatDate(date, format = "%Y-%m-%d"):
    '''This function can be passed a time, ael_date or string object and the 
       date will be formatted  in format, default = yyyy-mm-dd as standard in this app.
    '''

    map = {time.struct_time: _ReformatLocalTimeDate,
           str: _ReformatStrDate,
           float: _ReformatTimeDate,
           int: _ReformatTimeDate,
           ael.ael_date: _ReformatAELDate}

    return map[type(date)](date, format)

""" Transformer to ordinal date (starting from 1/1/1900) """
AelDateSerialShift=365+datetime.date(2000, 1, 1).toordinal()-36526
def AelDate2Serial(date):
    return date.to_float()-AelDateSerialShift

#*********************************************************************************************************************************
#*********************************************************  TMS Filter  **********************************************************
#*********************************************************************************************************************************

#Sub-function for the TMS_FIlter function to determine if the portfolio is a valid PRD portfolio
def isPrdPortfolio(TObject,IObject,*rest):

    validPrdPortfolio = 0

    if TObject and TObject.prfnbr:
        if TObject.prfnbr.add_info('BarCap_TMS_Feed') == 'Production' \
            and TObject.status != 'FO Sales' \
            and TObject.status != 'Simulated':

            validPrdPortfolio = 1
       
    return validPrdPortfolio
    
#Sub-function for the TMS_FIlte function to determine if the portfolio is a valid Test portfolio
def isTestPortfolio(TObject,IObject,*rest):

    validTestPortfolio = 0

    if TObject and TObject.prfnbr:
        if TObject.prfnbr.add_info('BarCap_TMS_Feed') == 'Test' \
            and TObject.status == 'Simulated':

            validTestPortfolio = 1
        
    return validTestPortfolio

#Sub-function for the TMS_FIlter function to determine if the instrument is a valid PRD instrument
def isSupportedInstrument(TObject,IObject,*rest):

    validInstrument = 0

    #Determine whether the instrument is a valid TMS instrument
    if TObject and TObject.prfnbr:
        if ((IObject.instype == 'Option' and IObject.und_instype == 'Swap') or \
                (IObject.instype == 'Option' and IObject.und_instype == 'FRA') or \
                IObject.instype == 'FxSwap' or \
                IObject.instype == 'CurrSwap' or \
                IObject.instype == 'Swap' or \
                IObject.instype == 'FRA' or \
                IObject.instype == 'Cap' or \
                IObject.instype == 'Floor') and IObject.exp_day.to_string('%Y-%m-%d') >= Expired_Date():

            validInstrument = 1

    return validInstrument

'''
Main TMS Filter
'''
def TMS_Filter (TObject,IObject,*rest):    

    '''
        This function determines whether a trade is valid for TMS feeding.
        
        3 Functions determine the validity of the trade:
        
        isPrdPortfolio()
        isTestPortfolio()
        isSupportedInstrument()
    '''

    if (isPrdPortfolio(TObject, IObject) == 1 or isTestPortfolio(TObject, IObject) == 1) \
        and isSupportedInstrument(TObject, IObject) == 1:
            
            SendTrade = 1
    else:
        SendTrade = 0
        
    return SendTrade
#*********************************************************************************************************************************
#*********************************************************  TMS Filter  **********************************************************
#*********************************************************************************************************************************

#List of Waste portfolios to be used when sending Void trades to TMS
def Valid_Waste_Portfolio(Port,*rest):

    '''
        prfnbr          prfid
        ----------------------------
        1874            NLD_IR_Waste
    '''
    wastelist = [1874]

    value = 0

    for l in wastelist:
        if Port == l:
            value = 1
        else:
            value = 0

    return value

def ValidFXWastePortfolio(portfolio):
    wastelist = ["NLD_FX_Waste"]
    return portfolio in wastelist

def ValidFXTerminatedPortfolio(portfolio):
    wastelist = ["NLD_FX_Terminated"]
    return portfolio in wastelist

def set_trade_addinf(trade, add_info, value,*rest):
    existing_addinfos = {}

    for ai in trade.additional_infos():

        existing_addinfos[ai.addinf_specnbr.field_name] = ai
        
    if existing_addinfos.has_key(add_info):

        clone = existing_addinfos[add_info].clone()
        clone.value = (str)(value)
        clone.commit()
            
    else:
        print value
        ai_spec = ael.AdditionalInfoSpec[add_info].clone()
        trd = trade.clone()
        new = ael.AdditionalInfo.new(trd)
        new.addinf_specnbr = ai_spec
        new.value = str(value)
        new.commit()

#Main filter used to check whether the trade should be applied to TMS again
def Send_Trade (ent_op, entity_addr):

    DateToday = Date()
    
    if ent_op == 'INSERT_TRADE':
    
        TObject = ael.Trade[(int)(entity_addr)]
        IObject = ael.Instrument[TObject.insaddr.insaddr]

        #Check whether the trade should be sent
        if TMS_Filter(TObject, IObject) == 1:
            x = 'INSERT_TRADE'
        else:
            x = 'NONE'

    elif ent_op == 'UPDATE_TRADE':
        
            TObject = ael.Trade[(int)(entity_addr)]
            IObject = ael.Instrument[TObject.insaddr.insaddr]
        
            #Check whether the trade should be sent
            if TMS_Filter(TObject, IObject) == 1:
                if TObject.optional_key:
                    x = 'UPDATE_TRADE'
                else:
                    x = 'INSERT_TRADE'
            else:
                x = 'NONE'
                
    elif ent_op == 'UPDATE_INSTRUMENT':

        #Get the instrument object
        IObject = ael.Instrument[(int)(entity_addr)]
        
        x = 'NONE'
                
        #Get all the trades linked to a specific instrument
        Trades = IObject.trades()
        
        #Get all the instruments linked to the underlying instrument
        Instruments = ael.Instrument.select('und_insaddr = %s' %IObject.insaddr)
        
        #--------------------------------------------------------------------------------------------------
        #This part will check all the trades against the main instrument if the main instrument was updated
        if Trades:
            for TObject in Trades:
                #Check whether the trade should be sent
                if TMS_Filter(TObject, IObject) == 1:
                    #The trade is valid and should be sent to TMS again because of the Instrument being updated
                    DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    SAGEN_Functions.set_trade_addinf(TObject, 'TMS_Gen_Message', DateToday)
                    
                else:
                    x = 'NONE'
        else:
            x = 'NONE'

        #--------------------------------------------------------------------------------------------------
        # This part will check all the trades against the main instrument if the underlying instrument was updated
        # and any trades exist against the main instrument
        
        if Instruments:
            for IObject in Instruments:
                for TObject in IObject.trades():
                    #Check whether the trade should be sent
                    if TMS_Filter(TObject, IObject) == 1:
                        #The trade is valid and should be sent to TMS again because of the Instrument being updated
                        DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        SAGEN_Functions.set_trade_addinf(TObject, 'TMS_Gen_Message', DateToday)
                        
                    else:
                        x = 'NONE'
        else:
            x = 'NONE'            

    elif ent_op == 'UPDATE_PARTY':

        x = 'NONE'

        PObject = ael.Party[(int)(entity_addr)] 

        #Get all the instruments linked to the underlying instrument
        CPty_Trades = ael.Trade.select('counterparty_ptynbr = %s' %PObject.ptynbr)
        Broker_Trades = ael.Trade.select('broker_ptynbr = %s' %PObject.ptynbr)
        
        #--------------------------------------------------------------------------------------------------
        #This part will check all the trades against the main instrument if the main instrument was updated
        if CPty_Trades:
            for TObject in CPty_Trades:
                IObject = TObject.insaddr
            
                #Check whether the trade should be sent
                if TObject.optional_key.__contains__('TMS') == 1 and TMS_Filter(TObject, IObject) == 1:
                    #The trade is valid and should be sent to TMS again because of the CounterParty being updated
                    DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    SAGEN_Functions.set_trade_addinf(TObject, 'TMS_Gen_Message', DateToday)


        #This part will check all the trades against the main instrument if the main instrument was updated
        if Broker_Trades:
            for TObject in Broker_Trades:
                IObject = TObject.insaddr
            
                #Check whether the trade should be sent
                if TObject.optional_key.__contains__('TMS') == 1 and TMS_Filter(TObject, IObject) == 1:
                    #The trade is valid and should be sent to TMS again because of the CounterParty being updated
                    DateToday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    SAGEN_Functions.set_trade_addinf(TObject, 'TMS_Gen_Message', DateToday)

    else:
        x = 'NONE'

    return x

#Split the TMS ID and TMS version out from optional_key field being populated
#2010-03-05 Peter Kutnik - changed from optional_key to add_info('TMS_Trade_Id')
#2010-03-11 Peter Kutnik - added reversion to optional_key for trades not moved 
def Get_Trade_TMS_ID (T,Flag,*rest):

    value = None
    
    if T:
        trade = ael.Trade[(int)(T)]
        addinfoTMSID = trade.add_info('TMS_Trade_Id')
        TMS_ID = ''
        
        if (addinfoTMSID is not None) and (addinfoTMSID.find('TMS') == 0):
            TMS_ID = addinfoTMSID 
        else: 
            TMS_ID = trade.optional_key

        map = {"Vanilla_ID": TMS_ID[4:15], 
               "Vanilla_Version": TMS_ID[16:],
               "Exotic_ID": TMS_ID[4:12],
               "Vanilla_Exotic_Check": TMS_ID[4:6]
              }

        if map.has_key(Flag):
            value = map[Flag]

    return value

#This function will return the BarCap SDS ID mapped against the Front Arena counterparty
def Get_BarCap_SDS_ID(P, *rest):
    
    if P:
        if P.add_info('BarCap_SMS_CP_SDSID') != '':
            SDS_ID = P.add_info('BarCap_SMS_CP_SDSID')
        else:
            if P.parent_ptynbr == 209 or P.type == 'Intern Dept': #Map ABSA Bank Ltd to all internal counterparties OR where the parent is ABSA Bank Ltd
                SDS_ID = '10250696'
            else:
                SDS_ID = '0'
    else:
        SDS_ID = '0'

    return SDS_ID

#This function will return the BarCap SMS Book ID mapped against the Front Arena portfolio 
def Get_BarCap_Book_ID(B, *rest):
    if B:
        if B.add_info('BarCap_SMS_BookID') != '':
            Book_ID = B.add_info('BarCap_SMS_BookID')
        else:
            Book_ID = '26656045' #This is the default ID for NLDO
    else:
        Book_ID = '26656045'
        
    return Book_ID

#This function will return the BarCap SMS Book ID mapped against the Front Arena portfolio 
def Get_BarCap_Strategy_Book_Name(B, *rest):
    if B:
        if B.add_info('BarCap_SMS_SB_Name') != '':
            Book_ID = B.add_info('BarCap_SMS_SB_Name')
        else:
            Book_ID = 'ABNLDO' #This will be the default value - Mapped against NLDO Portfolio
    else:
        Book_ID = 'ABNLDO'
        
    return Book_ID    

#This function will return the BarCap SMS Book ID mapped against the Front Arena portfolio 
def Get_BarCap_Strategy_Book_ID(B, *rest):
    if B:
        if B.add_info('BarCap_SMS_SB_ID') != '':
            Book_ID = B.add_info('BarCap_SMS_SB_ID')
        else:
            Book_ID = '30858048' #This will be the default value - Mapped against NLDO Portfolio
    else:
        Book_ID = '30858048'
        
    return Book_ID    

#This function will return the BarCap SMS User ID mapped against the Front Arena User
def Get_BarCap_User_ID(U, *rest):
    if U:
        if U.add_info('BarCap_SMS_UserID') != '':
            User_ID = U.add_info('BarCap_SMS_UserID')
        else: 
            User_ID = '47702213' #This is the userid for Eugene Booysen - will be used as the default
    else:
        User_ID = '47702213' #This is the userid for Eugene Booysen - will be used as the default
        
    return User_ID

#This function will return the Global_Reset_Day
def Get_Global_Reset_Day (I,Date, *rest):

    value = '0001-01-01'

    #Get the legs associated with the instrument
    LObject = ael.Leg.select('insaddr=%d'%I)

    #Loop through the legs
    for l in LObject:
        if l.type in ('Float', 'Cap', 'Floor'):
            if SAGEN_Resets.CurrentReset(1, l.legnbr, Date, 3) != '0001-01-01':
                value = ael.date_from_string(SAGEN_Resets.CurrentReset(1, l.legnbr, Date, 3)).to_string('%Y-%m-%d')
                return value
            else:
                if SAGEN_Resets.FirstResetAfter(1, l.legnbr, Date, 3) != 'NULL':
                    value = ael.date_from_string(SAGEN_Resets.FirstResetAfter(1, l.legnbr, Date, 3)).to_string('%Y-%m-%d')
                    return value
                else:
                    value = '0001-01-01'
                    return value
            
    return value

#This function will return the mapped BarCap calendar value
def Get_BarCap_Calendar (Cal1,Cal2,Cal3,Cal4,Cal5, *rest):

    Calendars = []
    
    #Create a list with all the calendars
    if Cal1:
        Calendars.append(Cal1)
    if Cal2:
        Calendars.append(Cal2)
    if Cal3:
        Calendars.append(Cal3)
    if Cal4:
        Calendars.append(Cal4)
    if Cal5:
        Calendars.append(Cal5)

    FinalValue = ''
    value = ''

    for Cal in Calendars:
        if Cal == 'AED - UAE Dirham': 
            value = '[NYB]'
        elif Cal == 'AUD Sydney': 
            value = '[SYB]'
        elif Cal == 'BRL Brasilia': 
            value = '[BRZ]'
        elif Cal == 'BWP Gaborone': 
            value = '[GAB]'
        elif Cal == 'CAD Toronto': 
            value = '[TRB]'
        elif Cal == 'CHF Zurich': 
            value = '[ZUB]'
        elif Cal == 'CZK Prague': 
            value = '[CZB]'
        elif Cal == 'DKK Copenhagen': 
            value = '[COB]'
        elif Cal == 'EGP Cairo': 
            value = '[CRO]'
        elif Cal == 'EUR Euro': 
            value = '[TGT]'
        elif Cal == 'GBP London': 
            value = '[LNB]'
        elif Cal == 'GHC Accra': 
            value = '[JOB]'
        elif Cal == 'HKD Hong Kong': 
            value = '[HKB]'
        elif Cal == 'HUF Budapest': 
            value = '[BDB]'
        elif Cal == 'ILS - Israel': 
            value = '[TAB]'
        elif Cal == 'INR New Delhi': 
            value = '[BMB]'
        elif Cal == 'JPY Tokyo': 
            value = '[LTO]'
        elif Cal == 'KES Nairobi': 
            value = '[JOB]'
        elif Cal == 'KWD Kuwait City': 
            value = '[KUB]'
        elif Cal == 'MUR Port Louis': 
            value = '[PLB]'
        elif Cal == 'MXN Mexico': 
            value = '[MXB]'
        elif Cal == 'MYR Kuala Lumpur': 
            value = '[KLX]'
        elif Cal == 'NGN Lagos': 
            value = '[JOB]'
        elif Cal == 'NOK Oslo': 
            value = '[OSS]'
        elif Cal == 'NZD Auckland': 
            value = '[AKW]'
        elif Cal == 'PKR Islamabad': 
            value = '[KAB]'
        elif Cal == 'PLN Warsaw': 
            value = '[WAB]'
        elif Cal == 'SAR Riyad':
            value = '[RIB]'
        elif Cal == 'SEK Stockholm': 
            value = '[STB]'
        elif Cal == 'SGD Singapore': 
            value = '[SIB]'
        elif Cal == 'THB - Thai': 
            value = '[BKB]'
        elif Cal == 'TZS Dar es Salaam': 
            value = '[JOB]'
        elif Cal == 'Target': 
            value = '[TGT]'
        elif Cal == 'UGX Uganda': 
            value = '[JOB]'
        elif Cal == 'USD New York': 
            value = '[NYB]'
        elif Cal == 'ZAR Johannesburg': 
            value = '[JOB]'
        elif Cal == 'ZMK Lusaka': 
            value = '[JOB]'
        elif Cal == 'ZMW Lusaka': 
            value = '[JOB]'
    
        if not FinalValue:
            FinalValue = FinalValue + value
        else:
            FinalValue = FinalValue + "+" + value

    return FinalValue

#Check whether a value must be rounded
def ValueCheck (Value, *rest):
    
    Value = (str)(Value)
    Value = (float)(Value)
    
    #Get the value of the decimal part
    Dec = Value.__mod__(1)
    
    if Dec > 0.0:
        Result = (str)(Value)
    else:
        Result = (str)((int)(Value))

    return Result


#Function with mapping to convert the Front Arena Daycount method to a TMS Yearpart method
def DayCount_YearPart_Convert (DayCount, *rest):
    
    YearPart = ''

    if (DayCount == 'Act/365' or DayCount == '30E/365' or DayCount ==  '30/365'):
        YearPart = '365F'
    elif (DayCount == 'Act/360' or DayCount == '30E/360' or DayCount ==  '30U/360' or DayCount == '30/360' or DayCount  == '30/360GERMAN'):
        YearPart = '360'
    elif DayCount == 'Act/ActAFB':
        YearPart = 'ActA'
    elif DayCount == 'Act/ActISMA':
        YearPart = 'ISMA'
    elif DayCount == 'Act/364':
        YearPart = '365'
    else:
        YearPart = 'Invalid Selection'

    return YearPart

#Function with mapping to convert the Front Arena Daycount method to a TMS Daypart method
def DayCount_DayPart_Convert (DayCount, *rest):

    DayPart = ''

    if (DayCount == 'Act/365' or DayCount == 'Act/360' or DayCount ==  'Act/ActAFB' or DayCount == 'Act/ActISMA' or DayCount ==  'Act/364'):
        DayPart = 'Act'
    elif (DayCount == '30E/360' or DayCount == '30E/365'):
        DayPart = '30E'
    elif (DayCount == '30/360' or DayCount == '30/365'):
        DayPart = '30'
    elif DayCount == '30U/360':
        DayPart = '30N'
    elif DayCount == '30/360GERMAN':
        DayPart = '30G'
    else:
        DayPart = 'Invalid Selection'
        
    return DayPart

#Function with mapping to convert the Front Arena Pay Day Method to a TMS RollConvention method
def Pay_Day_Method_Convert (PayDayMethod, *rest):

    RollConvention = ''

    if PayDayMethod == 'None':
        RollConvention = 'None'
    elif PayDayMethod == 'Following':
        RollConvention = 'Following'
    elif PayDayMethod == 'Mod. Following':
        RollConvention = 'ModifiedFollowing'
    elif PayDayMethod == 'Preceding':
        RollConvention = 'Previous'
    elif PayDayMethod == 'Mod. Preceding':
        RollConvention = 'ModifiedPrevious'
    elif PayDayMethod == 'EOM':
        RollConvention = 'EndOfMonth'
    else:
        RollConvention = 'Invalid Selection'
        
    return RollConvention
    
#Function to sort the list of cashflows
def SortListOfListsByCriteria(ListToSort, ListCriteria, ListSortType):
# Criteria is a list of integers which determines by what and in what order you
# want to sort ListToSort...
# ListSortType - either 1 or -1
    ListCriteria.reverse()
    i = 0
    for lstCrit in ListCriteria:
        ListToSort.sort(lambda x, y: ListSortType[i] *  cmp(x[lstCrit], y[lstCrit]))
    i = i + 1

    return ListToSort
