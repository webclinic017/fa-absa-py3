'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_EOD
PROJECT                 :       PACE MM
PURPOSE                 :       This module will be ran from the Back end at the end of each day. It will
                                send end of day interest messages to PACE MM and will sen tNext Day Maturity
                                Fixed Term Deposits through.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Module needs to be scheduled to run once a day at close of business.
    
    It will generate Interest/Balance messages for all valid Call Deposits that exist in Front Arena and
    PACE MM.
    It will also generate Interest/Balance messages for valid Fixed Term Deposits that exist in Front Arena
    and PACE MM that expire the following day.
'''

import acm, ael, amb, time
import PACE_MM_Parameters as Params
import FOperationsUtils as OpsUtils
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils
from AMB_Reader_Writer import AMB_Writer as AMB_Writer

class PACE_MM_Interest():
    def __init__(self, date):
        self.__date = date
        self.__calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
        
    def get_PACE_MM_Call_Accounts(self):
        tradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        tradeQuery.AddAttrNode('Instrument.OpenEnd', 'EQUAL', Utils.GetEnum('OpenEndStatus', 'Open End'))
        tradeQuery.AddAttrNode('Quantity', 'EQUAL', 1)
        
        return Utils.get_Common_Trade_Selection_PACE(tradeQuery)
    
    def get_Next_Day_MaturingFixed_Term_Deposits(self):
        tradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        tradeQuery.AddAttrNode('Instrument.OpenEnd', 'NOT_EQUAL', Utils.GetEnum('OpenEndStatus', 'Open End'))
        valid_Trades = acm.FSortedCollection()
        trades = Utils.get_Common_Trade_Selection_PACE(tradeQuery)
        for t in trades:
            #if (ael.date(t.Instrument().Legs()[0].EndDate()) == self.__date.add_banking_day(ael.Instrument['ZAR'],1)) and (t.Nominal() < 0):
            if (ael.date(t.Instrument().Legs()[0].EndDate()) >= self.__date) and (t.Nominal() < 0):
                valid_Trades.Add(t)
        return valid_Trades
    
    def applyGlobalSimulation(self):
        self.__calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        self.__calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.__date)
        self.__calcSpace.Refresh()
        
    def clearGlobalSimulation(self):
        self.__calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        self.__calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        self.__calcSpace.Refresh()
    
    def __get_Message_Detail(self, trade, values_Date, accrue_Prev):
        trade_Detail = {}
        trade_Detail['OID'] = trade.Oid()
        trade_Detail['TIME'] = trade.TradeTime()
        trade_Detail['OPTIONAL_KEY'] = trade.OptionalKey()
        trade_Detail['QUANTITY'] = trade.Quantity()
    
        party_Detail = {}
        party_Detail['COUNTERPARTY_SDS'] = trade.Counterparty().add_info('BarCap_SMS_CP_SDSID')
    
        instr = trade.Instrument()
        instrument_Detail = {}
        instrument_Detail['NAME'] = instr.Name()
        instrument_Detail['CURRENCY'] = instr.Currency().Name()
        instrument_Detail['CONTRACT_SIZE'] = instr.ContractSize()
        instrument_Detail['EXPIRY_DATE'] = instr.ExpiryDate()
        
        leg = instr.Legs()[0]
        leg_Detail = {}
        leg_Detail['START_DAY'] = leg.StartDate()
        leg_Detail['REINVEST'] = leg.Reinvest()
        leg_Detail['RATE'] = leg.FixedRate()
        
        cashFlow_Detail = {}
        cashFlow_Detail['OID'] = ''
        cashFlow_Detail['PAY_DAY'] = ''
        cashFlow_Detail['FIXED_AMOUNT'] = ''
        cashFlow_Detail['NOMINAL_FACTOR'] = ''
        cashFlow_Detail['PACE_MM_EVENT_ID'] = ''
        
        calculation_Detail = {}
        calculation_Detail['DAILY_ACCRUED_INTEREST'] = str(values_Date[0] - accrue_Prev)
        calculation_Detail['ACCRUED_INTEREST'] = str(values_Date[0])
        calculation_Detail['BALANCE'] = str(values_Date[1])
        
        return trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail, calculation_Detail
        
    def construct_Interest_Message(self, trade, values_Date, accrue_Prev, insType):
        trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail, calculation_Detail = self.__get_Message_Detail(trade, values_Date, accrue_Prev)

        trade_section = [('TRADE', trade_Detail), ('PARTY', party_Detail)]
        instrument_section = [('INSTRUMENT', instrument_Detail), ('LEG', leg_Detail), ('CASHFLOW', cashFlow_Detail)]
        calculation_section = [('CALCULATION', calculation_Detail)]
        complete_section = [trade_section, instrument_section, calculation_section]
        
        message = amb.mbf_start_message(None, 'EOD_GENERATED', '1.0', None, Params.senderExternalSource)
        message.mbf_add_string('EVENT_TYPE', 'EOD_INTEREST')
        message.mbf_add_string('INSTRUMENT_TYPE', insType)
        message.mbf_add_string('ERROR_NUMBER', '0')
        message.mbf_add_string('FREE_TEXT', '')
        message.mbf_add_string('UNDERLYING_EVENT', '')
        
        message.mbf_add_string('MESSAGE_CODE', Utils.get_Message_Event_Code(insType, 'EOD_INTEREST', ''))
        
        msgList = message.mbf_start_list('DATA')
        
        for section in complete_section:
            tag_list = [msgList]
            
            for tuple in section:
                mb_msg = tag_list[len(tag_list) - 1].mbf_start_list(tuple[0])
                for item in tuple[1]:
                    mb_msg.mbf_add_string(item, str(tuple[1][item]))
                tag_list.append(mb_msg)
            
            item = len(tag_list) - 1
            for i in range(item, 0):
                tag_list[i].mbf_end_list()
        
        msgList.mbf_end_list()
        message.mbf_end_message()
        
        return message

    def get_Trading_Manager_Column_Value(self, trade, columnName):
        try:
            return round(self.__calcSpace.CalculateValue(trade, columnName).Number(), 2)
        except:
            return round(self.__calcSpace.CalculateValue(trade, columnName), 2)
        
def event_cb_AMB_Sender(channel, event, arg):
    pass
    
ael_variables = [
                    ['date', 'Date', 'string', None, 'TODAY', 1, 0, 'Date for which EOD process should run.', None, 1]
                ]

def ael_main(dict):
    OpsUtils.Log(True, '========================================================================')
    OpsUtils.Log(True, '>> Starting PACE MM End of Day Procedure at %s' % time.asctime(time.localtime()))
    OpsUtils.Log(True, '========================================================================')
    
    #######################################################
    # 1: Connecting to AMB
    #######################################################
    OpsUtils.Log(True, '>> Step 1 of 6 - Connecting to the AMB...\n')
    AMBWriter = AMB_Writer(Params.ambAddress, Params.senderMBName, event_cb_AMB_Sender, Params.senderExternalSource, Params.senderExternalSource)
    try:
        AMBWriter.open_AMB_Sender_Connection()
    except Exception, e:
        OpsUtils.Log(True, 'Error: Could not connect to the AMB: %s. ' %str(e))
        return
    
    trade_dict = {}
    
    #######################################################
    # 2: Retreiving Call Account Trading Manager Information
    #######################################################
    OpsUtils.Log(True, '>> Step 2 of 6 - Retreiving Call Account Trading Manager Information...\n')
    dateString = dict['date']
    if dateString == 'TODAY':
        date = ael.date_today()
    else:
        date = ael.date(dict['date'])
    pace_MM_Interest = PACE_MM_Interest(date)
    pace_MM_Interest.applyGlobalSimulation()

    call_accounts = pace_MM_Interest.get_PACE_MM_Call_Accounts()
    for t in call_accounts:
        if ael.date(t.Instrument().Legs()[0].EndDate()) >= date:
            accrue = pace_MM_Interest.get_Trading_Manager_Column_Value(t, 'Portfolio Accrued Call Interest')
            balance = pace_MM_Interest.get_Trading_Manager_Column_Value(t, 'Deposit balance')
            trade_dict[t] = (accrue, balance)
                
    pace_MM_Interest.clearGlobalSimulation()
    
    date = date.add_days(-1)
    pace_MM_Interest = PACE_MM_Interest(date)
    pace_MM_Interest.applyGlobalSimulation()
    
    #######################################################
    # 3: Creating and Posting Call Account EOD messages to AMB
    #######################################################
    OpsUtils.Log(True, '>> Step 3 of 6 - Creating and Posting Call Account EOD messages to AMB...\n')
    for key in trade_dict:
        accrue_Prev = pace_MM_Interest.get_Trading_Manager_Column_Value(key, 'Portfolio Accrued Call Interest')
        interest_message = pace_MM_Interest.construct_Interest_Message(key, trade_dict[key], accrue_Prev, 'CALL_DEPOSIT')
        post_To_AMB_Success = AMBWriter.post_Message_To_AMB(interest_message)
        if not post_To_AMB_Success:
            OpsUtils.Log(True, 'Error: Could not post the following message to the AMB: %s. ' %interest_message.mbf_object_to_string())
            return
                
    pace_MM_Interest.clearGlobalSimulation()

    #######################################################
    # 4: Retreiving Next Day Maturing Fixed Term Deposit Information
    #######################################################
    trade_dict = {}
    OpsUtils.Log(True, '>> Step 4 of 6 - Retreiving Next Day Maturing Fixed Term Deposit Information...\n')

    dateString = dict['date']
    if dateString == 'TODAY':
        date = ael.date_today()
    else:
        date = ael.date(dict['date'])

    pace_MM_Interest = PACE_MM_Interest(date)
    pace_MM_Interest.applyGlobalSimulation()

    fixed_Term_Deposits = pace_MM_Interest.get_Next_Day_MaturingFixed_Term_Deposits()
    for t in fixed_Term_Deposits:
        accrue = pace_MM_Interest.get_Trading_Manager_Column_Value(t, 'Portfolio Accrued Interest')
        balance = pace_MM_Interest.get_Trading_Manager_Column_Value(t, 'Current Nominal')
        trade_dict[t] = (accrue, balance)
                
    pace_MM_Interest.clearGlobalSimulation()
    
    date = date.add_days(-1)
    pace_MM_Interest = PACE_MM_Interest(date)
    pace_MM_Interest.applyGlobalSimulation()

    #######################################################
    # 5: Creating and Posting Fixed Term Deposit EOD messages to AMB
    #######################################################
    OpsUtils.Log(True, '>> Step 5 of 6 - Creating and Posting Fixed Term Deposit EOD messages to AMB...\n')
    for key in trade_dict:
        accrue_Prev = pace_MM_Interest.get_Trading_Manager_Column_Value(key, 'Portfolio Accrued Interest')
        interest_message = pace_MM_Interest.construct_Interest_Message(key, trade_dict[key], accrue_Prev, 'FIXED_TERM_DEPOSIT')
        post_To_AMB_Success = AMBWriter.post_Message_To_AMB(interest_message)
        if not post_To_AMB_Success:
            OpsUtils.Log(True, 'Error: Could not post the following message to the AMB: %s. ' %interest_message.mbf_object_to_string())
            return
                
    pace_MM_Interest.clearGlobalSimulation()

    #######################################################
    # 6: Closing AMB Connection
    #######################################################
    OpsUtils.Log(True, '>> Step 6 of 6 - Closing AMB Connection...\n')
    try:
        if AMBWriter.close_AMB_Connection():
            OpsUtils.Log(True, 'PACE_MM_EOD completed successfully.')
    except Exception, e:
        OpsUtils.Log(True, 'Error: Could not close the connection to the AMB: %s' % str(e))
