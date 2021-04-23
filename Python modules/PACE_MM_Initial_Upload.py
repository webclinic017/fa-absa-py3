'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Initial_Upload
PROJECT                 :       PACE MM
PURPOSE                 :       This module will be used to generate messages for a new client that is being
                                on boerded onto PACE MM
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

2012-11-22      603220          Heinrich Cronje                 PACE MM EOD Deployment - Made Balance 0 for initial
                                                                upload.
                                                                
2013-03-09      851429          Heinrich Cronje                 Made Balance valid for initial upload.
2013-09-27      XXXXXX          Heinrich Cronje                 Front Arena Upgrade - 2013.3 Changes Calculation Space
                                                                and Global Variable.
                                                                
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module can be used to upload existing Call Deposit detail to PACE MM.
    NEW, DEPOSIT, WITHDRAWAL and INTERET_REINVESTMENT messages can be loaded for specific counterparties
    respectively.
'''

import acm, ael, amb
import PACE_MM_Parameters as Params
import FOperationsUtils as OpsUtils
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils
from AMB_Reader_Writer import AMB_Writer as AMB_Writer

def applyGlobalSimulation(date):
    global calcSpace
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    calcSpace.Refresh()
    
def clearGlobalSimulation():
    global calcSpace
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    calcSpace.Refresh()

def get_Call_Accounts(counterparties):
    CallTradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    CallTradeQuery.AddAttrNode('Instrument.OpenEnd', 'EQUAL', Utils.GetEnum('OpenEndStatus', 'Open End'))
    CallTradeQuery.AddAttrNode('Quantity', 'EQUAL', 1)

    if counterparties:
        counterparty = CallTradeQuery.AddOpNode('OR')
        for cp in counterparties:
            counterparty.AddAttrNode('Counterparty.Oid', 'EQUAL', cp.Oid())
            
    trades = Utils.get_Common_Trade_Selection(CallTradeQuery)

    return trades


def get_Message_Detail(message_type, trade, StartDate, cashFlow = None):
    global calcSpace
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
    leg_Detail['START_DAY'] = StartDate
    leg_Detail['REINVEST'] = leg.Reinvest()
    leg_Detail['RATE'] = leg.FixedRate()
    
    cashFlow_Detail = {}
    cashFlow_Detail['OID'] = ''
    cashFlow_Detail['PAY_DAY'] = ''
    cashFlow_Detail['FIXED_AMOUNT'] = ''
    cashFlow_Detail['NOMINAL_FACTOR'] = ''
    cashFlow_Detail['PACE_MM_EVENT_ID'] = ''
    
    if cashFlow:
        cashFlow_Detail['OID'] = cashFlow.Oid()
        cashFlow_Detail['PAY_DAY'] = str(cashFlow.PayDate())
        if cashFlow.StartDate():
            cashFlow_Detail['PAY_DAY'] = str(cashFlow.StartDate())
        cashFlow_Detail['FIXED_AMOUNT'] = str(cashFlow.FixedAmount())
        cashFlow_Detail['NOMINAL_FACTOR'] = str(cashFlow.NominalFactor())
        cashFlow_Detail['PACE_MM_EVENT_ID'] = cashFlow.ExternalId()

    calculation_Detail = {}
    calculation_Detail['DAILY_ACCRUED_INTEREST'] = 0
    calculation_Detail['ACCRUED_INTEREST'] = 0
    calculation_Detail['BALANCE'] = round(calcSpace.CalculateValue(trade, 'Deposit balance').Number(), 2)

    return trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail, calculation_Detail

def construct_Message(message_type, insType, trade, StartDate, cashFlow = None):
    trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail, calculation_Detail = get_Message_Detail(message_type, trade, StartDate, cashFlow)
    
    trade_section = [('TRADE', trade_Detail), ('PARTY', party_Detail)]
    instrument_section = [('INSTRUMENT', instrument_Detail), ('LEG', leg_Detail), ('CASHFLOW', cashFlow_Detail)]
    calculation_section = [('CALCULATION', calculation_Detail)]
    complete_section = [trade_section, instrument_section, calculation_section]
    
    message = amb.mbf_start_message(None, 'INITIAL_TAKE_ON', "1.0", None, Params.senderExternalSource)
    message.mbf_add_string('EVENT_TYPE', message_type)
    message.mbf_add_string('INSTRUMENT_TYPE', insType)
    message.mbf_add_string('ERROR_NUMBER', '0')
    message.mbf_add_string('FREE_TEXT', 'Initial Take On')
    message.mbf_add_string('UNDERLYING_EVENT', '')
    
    message.mbf_add_string('MESSAGE_CODE', Utils.get_Message_Event_Code(insType, message_type, ''))
    
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

def get_StartDate(trade, date):
    StartDate = ael.date(trade.Instrument().Legs()[0].StartDate())
    if StartDate < date:
        StartDate = date.add_days(-1)

    return StartDate

def event_cb_AMB_Sender(channel, event, arg):
    pass

def post_message(msg):
    post_To_AMB_Success = AMBWriter.post_Message_To_AMB(msg)
    if not post_To_AMB_Success:
        OpsUtils.Log(True, 'ERROR: Could not post the following message onto the AMB. %s' % msg.mbf_object_to_string())

global calcSpace
calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext().Name(), 'FTradeSheet')

AMBWriter = AMB_Writer(Params.ambAddress, Params.senderMBName, event_cb_AMB_Sender, Params.senderExternalSource, Params.senderExternalSource)
MESSAGE_TYPES = ['NEW', 'FIXED AMOUNT DEPOSIT', 'FIXED AMOUNT WITHDRAWAL', 'INTEREST REINVESTMENT DEPOSIT', 'INTEREST REINVESTMENT WITHDRAWAL']

ael_variables = [
                    ['takeOnDate', 'Take On Date', 'date', None, ael.date_today().add_months(-3).first_day_of_month(), 1, 0, 'Date for which the take on will start.', None, 1],
                    ['messageType', 'Type of Message', 'string', MESSAGE_TYPES, MESSAGE_TYPES[0], 1, 0, 'Type of messages that will be sent.', None, 1],
                    ['counterparties', 'Counterparty', acm.FParty, acm.FParty, '', 1, 1, 'Take on for a specific counterparty', None, 1]
                ]

def ael_main(dict):
    new_Trade_Msg = []
    FA_deposit_msg_List = []
    FA_withdrawal_msg_List = []
    IR_deposit_msg_List = []
    IR_withdrawal_msg_List = []

    messageMapping = {'NEW' : new_Trade_Msg,
                    'FIXED AMOUNT DEPOSIT' : FA_deposit_msg_List,
                    'FIXED AMOUNT WITHDRAWAL' : FA_withdrawal_msg_List,
                    'INTEREST REINVESTMENT DEPOSIT' : IR_deposit_msg_List,
                    'INTEREST REINVESTMENT WITHDRAWAL' : IR_withdrawal_msg_List}

    takeOnDate = dict['takeOnDate']
    messageType = dict['messageType']
    counterparties = dict['counterparties']

    trades = get_Call_Accounts(counterparties)
    OpsUtils.Log(True, 'Number of Parties on this batch %s' %str(len(counterparties)))
    OpsUtils.Log(True, 'Number of Call Accounts on this batch %s' %str(len(trades)))

    for t in trades:
        if messageType == 'NEW':
            StartDate = get_StartDate(t, takeOnDate)
            applyGlobalSimulation(StartDate)
            message = construct_Message('NEW', 'CALL_DEPOSIT', t, StartDate)
            new_Trade_Msg.append(message)
            clearGlobalSimulation
        else:
            ins = t.Instrument()
            cfs = Utils.get_Valid_CF_From_Date(ins, takeOnDate)
            for c in cfs:
                StartDate = get_StartDate(t, takeOnDate).add_days(1)
                if c.CashFlowType() == 'Fixed Amount':
                    if c.StartDate() and ael.date(c.StartDate()) < takeOnDate:
                        continue
                        
                    if c.FixedAmount() < 0:
                        FA_withdrawal_msg_List.append(construct_Message('WITHDRAWAL', 'CALL_DEPOSIT', t, StartDate, c))
                    else:
                        FA_deposit_msg_List.append(construct_Message('DEPOSIT', 'CALL_DEPOSIT', t, StartDate, c))
                elif c.CashFlowType() == 'Interest Reinvestment':
                    if c.FixedAmount() < 0:
                        IR_withdrawal_msg_List.append(construct_Message('INTEREST_REINVESTMENT', 'CALL_DEPOSIT', t, StartDate, c))
                    else:
                        IR_deposit_msg_List.append(construct_Message('INTEREST_REINVESTMENT', 'CALL_DEPOSIT', t, StartDate, c))

    OpsUtils.Log(True, 'Number of Messages on this batch %s' %str(len(messageMapping[messageType])))
    AMBWriter.open_AMB_Sender_Connection()
    
    postingCounter = 0
    
    for msg in messageMapping[messageType]:
        post_message(msg)
        postingCounter = postingCounter + 1
        
    OpsUtils.Log(True, 'Number of Messages posted to the AMB %s.' % str(postingCounter))
    
    if AMBWriter.close_AMB_Connection():
        OpsUtils.Log(True, 'Connection to AMB is closed.')
