'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Resend_Message
PROJECT                 :       PACE MM
PURPOSE                 :       This module give the user the opertunity to resend a message from Front Arena
                                to PACE MM via the AMB - MMG integration.
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

                NB      :       THIS MODULE SHOULD ONLY BE EXECUTED BY RTB
    
    With this module the user can resend any one of the message combination by inseting only a trade number
    and then selected the message type that should be resend.
'''

import ael, acm, amb
import PACE_MM_Parameters as Params
import FOperationsUtils as OpsUtils
from AMB_Reader_Writer import AMB_Writer as AMB_Writer
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils

'''------------------------------------------------------------------------
    Functions to handle the interaction of the AEL Variable intup screen
------------------------------------------------------------------------'''
def set_Values_From_Trade_Nbr(index, fieldValues):
    fieldValues[1] = ''
    fieldValues[2] = ''
    fieldValues[3] = ''
    ael_variables[2][3] = []
    ael_variables[2][9] = 0
    ael_variables[3][9] = 0
    ael_variables[4][3] = []
    ael_variables[4][9] = 0
    fieldValues[4] = ''
    fieldValues[5] = ''
    ael_variables[5][9] = 0
    
    if fieldValues[0] != 0:
        trade = acm.FTrade[fieldValues[0]]
        if trade:
            if trade.Instrument().InsType() == 'Deposit':
                if trade.Instrument().OpenEnd() == 'Open End':
                    fieldValues[1] = 'CALL_DEPOSIT'
                    fieldValues[2] = CALL_ACCOUNT_MESSAGE_TYPES[0]
                    ael_variables[2][3] = CALL_ACCOUNT_MESSAGE_TYPES
                    ael_variables[2][9] = 1
                else:
                    fieldValues[1] = 'FIXED_TERM_DEPOSIT '
                    fieldValues[2] = FIXED_TERM_MESSAGE_TYPES[0]
                    ael_variables[2][3] = FIXED_TERM_MESSAGE_TYPES
                    ael_variables[2][9] = 1
                    
    return fieldValues

def set_Message_Type_Details(index, fieldValues):
    fieldValues[3] = ''
    fieldValues[4] = ''
    fieldValues[5] = ''
    ael_variables[2][9] = 1
    ael_variables[3][9] = 0
    ael_variables[4][3] = []
    ael_variables[4][9] = 0
    if fieldValues[1].strip() == 'CALL_DEPOSIT' and fieldValues[2].strip() == 'TRADING':
        CF_List = []
        trade = acm.FTrade[fieldValues[0]]
        for l in trade.Instrument().Legs():
            for c in l.CashFlows():
                if c.CashFlowType() in ('Fixed Amount', 'Interest Reinvestment'):
                    CF_List.append(c.Oid())
        
        ael_variables[4][3] = CF_List
        ael_variables[4][9] = 1
    if fieldValues[2].strip() == 'ACKNOWLEDGE' or (fieldValues[1].strip() == 'CALL_DEPOSIT' and fieldValues[2].strip() in ('CANCEL', 'AMENDMENT')):
        if fieldValues[1].strip() == 'FIXED_TERM_DEPOSIT':
            ael_variables[3][3] = TERM_ACKNOWLEDGE_EVENTS
            ael_variables[3][9] = 1
        elif fieldValues[1].strip() == 'CALL_DEPOSIT':
            ael_variables[3][3] = CALL_ACCOUNT_ACKNOWLEDGE_EVENTS
            ael_variables[3][9] = 1
        
    return fieldValues

def get_Call_Account_Trading_Type(index, fieldValues):
    fieldValues[5] = ''
    if fieldValues[4]:
        cf = acm.FCashFlow[fieldValues[4]]
        if cf:
            if cf.CashFlowType() == 'Interest Reinvestment':
                fieldValues[5] = 'INTEREST_REINVESTMENT'
            elif cf.CashFlowType() == 'Fixed Amount':
                if cf.FixedAmount() * cf.NominalFactor() < 0:
                    fieldValues[5] = 'WITHDRAWAL'
                else:
                    fieldValues[5] = 'DEPOSIT'
    return fieldValues

def set_Call_Ack_Trading(index, fieldValues):
    fieldValues[4] = ''
    fieldValues[5] = ''
    ael_variables[4][9] = 0
    ael_variables[5][9] = 0
    if fieldValues[3] == 'TRADING':
        CF_List = []
        trade = acm.FTrade[fieldValues[0]]
        for l in trade.Instrument().Legs():
            for c in l.CashFlows():
                if c.CashFlowType() in ('Fixed Amount', 'Interest Reinvestment'):
                    CF_List.append(c.Oid())
        ael_variables[4][3] = CF_List
        ael_variables[4][9] = 1
    return fieldValues

FIXED_TERM_MESSAGE_TYPES = ['NEW', 'CANCEL', 'AMENDMENT', 'ACKNOWLEDGE']
CALL_ACCOUNT_MESSAGE_TYPES = ['NEW', 'CANCEL', 'AMENDMENT', 'TRADING', 'ACKNOWLEDGE']
TERM_ACKNOWLEDGE_EVENTS = ['NEW', 'CANCEL']
CALL_ACCOUNT_ACKNOWLEDGE_EVENTS = ['NEW', 'CANCEL', 'TRADING']

ael_variables = [['trdnbr', 'Trade Nbr', 'int', None, 0, 1, 0, 'Trade Number requested resend event.', set_Values_From_Trade_Nbr, 1],
                ['insType', 'Instrument Type', 'string', None, '', 1, 0, 'Instrument Type of resend message.', None, 0],
                ['messageType', 'Message Type', 'string', [], '', 1, 0, 'Message Type for the chosen instrument.', set_Message_Type_Details, 0],
                ['ackEvent', 'Acknowledge Event', 'string', [], '', 0, 0, 'Event that will be acknowledged.', set_Call_Ack_Trading, 0],
                ['callCF', 'Call Account Cash Flow', 'int', [], '', 0, 0, 'Call Account CF to be resend.', get_Call_Account_Trading_Type, 0],
                ['callTradingType', 'Call Account Trading Type', 'string', None, '', 0, 0, 'Call Account Message Type.', None, 0]]

def get_Message_Detail(trade, cashFlow = None):
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

    if cashFlow:
        cashFlow_Detail['OID'] = cashFlow.Oid()
        cashFlow_Detail['PAY_DAY'] = str(cashFlow.PayDate())
        if cashFlow.StartDate():
            cashFlow_Detail['PAY_DAY'] = str(cashFlow.StartDate())
        cashFlow_Detail['FIXED_AMOUNT'] = cashFlow.FixedAmount()
        cashFlow_Detail['NOMINAL_FACTOR'] = cashFlow.NominalFactor()
        cashFlow_Detail['PACE_MM_EVENT_ID'] = cashFlow.ExternalId()

    return trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail

def event_cb(channel, event, arg):
    pass    

def ael_main(ael_dict):
    trade = acm.FTrade[ael_dict['trdnbr']]
    event_type = ael_dict['messageType'].strip()
    instrument_type = ael_dict['insType'].strip()
    call_trading_type = ael_dict['callTradingType'].strip()
    ackEvent = ael_dict['ackEvent'].strip()
    
    cf = ael_dict['callCF']
    cashFlow = None
    if cf:
        cashFlow = acm.FCashFlow[cf]

    '''------------------------------------------------------------------------
                    Determining Message Type and Detail
    ------------------------------------------------------------------------'''
    underlyingEvent = ''
    if event_type in ('ACKNOWLEDGE', 'CANCEL', 'AMENDMENT'):
        if call_trading_type:
            underlyingEvent = call_trading_type
        else:
            underlyingEvent = ackEvent
            if instrument_type == 'FIXED_TERM_DEPOSIT' and event_type in ('AMENDMENT', 'CANCEL'):
                underlyingEvent = 'NEW'

    '''------------------------------------------------------------------------
                            Constructing AMBA Message
    ------------------------------------------------------------------------'''
    message = amb.mbf_start_message(None, 'MANUALLY_GENERATED', '1.0', None, Params.senderExternalSource)
    if event_type == 'TRADING':
        event_type = call_trading_type

    message.mbf_add_string('EVENT_TYPE', event_type)
    message.mbf_add_string('INSTRUMENT_TYPE', instrument_type)
    message.mbf_add_string('ERROR_NUMBER', '')
    message.mbf_add_string('FREE_TEXT', '')
    message.mbf_add_string('UNDERLYING_EVENT', underlyingEvent)
    
    if cashFlow:
        trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail = get_Message_Detail(trade, cashFlow)
    else:
        trade_Detail, party_Detail, instrument_Detail, leg_Detail, cashFlow_Detail = get_Message_Detail(trade)

    trade_section = [('TRADE', trade_Detail), ('PARTY', party_Detail)]
    instrument_section = [('INSTRUMENT', instrument_Detail), ('LEG', leg_Detail), ('CASHFLOW', cashFlow_Detail)]
    complete_section = [trade_section, instrument_section]

    message.mbf_add_string('MESSAGE_CODE', Utils.get_Message_Event_Code(instrument_type, event_type, underlyingEvent))

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

    '''------------------------------------------------------------------------
                    Write Constructed Message onto the AMB
    ------------------------------------------------------------------------'''
    amb_Writer = AMB_Writer(Params.ambAddress, Params.senderMBName, event_cb, Params.senderExternalSource, Params.senderExternalSource)
    if amb_Writer.open_AMB_Sender_Connection():
        amb_Writer.post_Message_To_AMB(message)
        if amb_Writer.close_AMB_Connection():
            OpsUtils.Log(True, 'AMB Connection Closed.')
