'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_MESSAGE_Processing
PROJECT                 :       PACE MM
PURPOSE                 :       This module handles the processing of the messages coming from the ADS and Externally.
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
2012-08-08      390267          Heinrich Cronje                 Payment Instructions are now received from PACE MM
                                                                and will now be added to the Additional Info field
                                                                Settle_Type on the cashflow so that it is available
                                                                in Settlement Manager.
2012-10-16      536118          Heinrich Cronje                 Added the section for Fixed Rate subscribtion on a 
                                                                Call Account.
2012-10-22      549725          Heinrich Cronje                 Added PACE_MESSAGE_TYPE Instrument Amendment Rate Change
                                                                to cater for the scenarios where the leg and cashflow
                                                                changes are in one message.
2012-11-22      603220          Heinrich Cronje                 PACE MM EOY Deployment - SSI implementation updates.
2014-09-22                      Matthias Riedel                 Adjust Currency Check to Non ZAR, extend messages with 
                                                                the respective Non ZAR values
2016-03-03      BARXMM-65       Kirsten Good                    Add validations to test for null trade/instrument ID
                                                                
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

FOR AN ADS MESSAGE:

    An AMBA message from the ADS is received and PACE MM message properties are being determined and returned
    so that the outgoing message can be created and sent to PACE MM.

FOR AN EXTERNAL MESSAGE:

    A MMG (PACE MM originated) message, a couple of validations are applied to the message and the data in the
    message to ensure that a valid message have been received.
    
    If any of the validations fail a NOT_ACKNOWLEDGE will be sent back to MMG.
    If all validations passed, the requered action will be performed in Front Arena. The ATS will pick up the
    AMBA message resulting from the action performed and will pass through this module as an ADS message
    to sent the correct response back to MMG.
'''

import acm
import PACE_MM_Parameters as Params
import FOperationsUtils as Utils
import PACE_MM_Booking_Class as Booking_Utils
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as PACE_Utils
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils

class PACE_MM_Data_Struct():
    def __init__(self, subject, message):
        self.message = message
        if not self.message:
            self.messageAsString = message
        else:
            self.messageAsString = self.message.mbf_object_to_string()
        self.ACM_object = None
        self.subject = subject
        self.PACE_Message_Type = ''
        self.Instrument_Type = ''
        self.cashFlowList = []
        self.AMBA_Message_Type = ''
        self.AMB_TRD_INSTR_Obj = None
        self.ERROR_NUMBER = 0
        self.Free_Text = ''
        self.OPTIONAL_KEY = ''

class PACE_MM_Message_Processing():

    def __init__(self, subject, message):
        self.data_Struct = PACE_MM_Data_Struct(subject, message)

    def __processTradeMessage(self):
        amb_obj = AMBA_Utils.object_by_name(self.data_Struct.message, ['+', '!'], 'TRADE')
        if amb_obj:
            self.data_Struct.AMB_TRD_INSTR_Obj = amb_obj
            
            '''--------------------------------------------------------------------------
                                    Common Variables
            --------------------------------------------------------------------------'''
            status = AMBA_Utils.get_AMBA_Object_Value(amb_obj, 'STATUS')
            optional_key = AMBA_Utils.get_AMBA_Object_Value(amb_obj, 'OPTIONAL_KEY')
            valid_optionalKey = PACE_Utils.is_Valid_Optional_Key(optional_key)
            
            '''--------------------------------------------------------------------------
                                    Insert Trade Processing
            --------------------------------------------------------------------------'''
            if self.data_Struct.AMBA_Message_Type == 'INSERT_TRADE':
                if valid_optionalKey:
                    return False
                else:
                    if status in Params.CANCELLATION_TRADE_STATUS:
                        return False
                        
                    self.data_Struct.PACE_Message_Type = 'New Trade'
                '''--------------------------------------------------------------------------
                                        Update Trade Processing
                --------------------------------------------------------------------------'''
            elif self.data_Struct.AMBA_Message_Type == 'UPDATE_TRADE':
                original_trade_status = AMBA_Utils.get_AMBA_Object_Value(amb_obj, '!STATUS')
                original_quantity = AMBA_Utils.get_AMBA_Object_Value(amb_obj, '!QUANTITY')
                
                '''--------------------------------------------------------------------------
                                Only Trade Status and Quantity are Valid Updates
                --------------------------------------------------------------------------'''
                if (not original_trade_status) and (not original_quantity):
                    return False
                
                if original_quantity and (not original_trade_status):
                    if not valid_optionalKey:
                        return False
                    
                    self.data_Struct.PACE_Message_Type = 'Trade Amendment'
                    
                if original_trade_status:
                    '''--------------------------------------------------------------------------
                                                Status Movements
                    --------------------------------------------------------------------------'''
                    original_valid_status = PACE_Utils.is_Valid_Status(original_trade_status)
                    original_cancel_status = PACE_Utils.is_Valid_Cancel_Status(original_trade_status)
                    current_valid_status = PACE_Utils.is_Valid_Status(status)
                    currenct_cancel_status = PACE_Utils.is_Valid_Cancel_Status(status)
                    
                    '''--------------------------------------------------------------------------
                                        Trade is Voided that is not in PACE
                    --------------------------------------------------------------------------'''
                    if original_valid_status and currenct_cancel_status and not valid_optionalKey:
                        return False
                    
                    '''--------------------------------------------------------------------------
                                        Trade Status Moves From Non Valid to Valid
                    --------------------------------------------------------------------------'''
                    if (not original_valid_status) and current_valid_status:
                        if valid_optionalKey:
                            self.data_Struct.PACE_Message_Type = 'New Trade Acknowledgement'
                        else:
                            self.data_Struct.PACE_Message_Type = 'New Trade'
                    
                    '''--------------------------------------------------------------------------
                                        Trade Status Moves From Void to Valid
                    --------------------------------------------------------------------------'''
                    if original_cancel_status and current_valid_status:
                        self.data_Struct.PACE_Message_Type = 'New Trade From Void'
                    
                    '''--------------------------------------------------------------------------
                                        Trade Status Moves From Valid to Void
                    --------------------------------------------------------------------------'''
                    if original_valid_status and currenct_cancel_status:
                        freeText1 = AMBA_Utils.get_AMBA_Object_Value(amb_obj, 'TEXT1')
                        is_valid_freeText1 = PACE_Utils.is_Valid_Optional_Key(freeText1)
                        if is_valid_freeText1:
                            self.data_Struct.PACE_Message_Type = 'Cancellation - Acknowledgement'
                        else:
                            self.data_Struct.PACE_Message_Type = 'Cancellation'
            
            trdnbr = AMBA_Utils.get_AMBA_Object_Value(amb_obj, 'TRDNBR')
            if valid_optionalKey:
                self.data_Struct.OPTIONAL_KEY = optional_key
            
            '''--------------------------------------------------------------------------
                                Instrument Type Identification
            --------------------------------------------------------------------------'''
            if self.data_Struct.ACM_object.Instrument().Legs() and self.data_Struct.ACM_object.Instrument().Legs()[0].LegType() in Params.VALID_CALL_LEG_TYPE:
                self.data_Struct.Instrument_Type = 'CALL_DEPOSIT'
            else:
                self.data_Struct.Instrument_Type = 'FIXED_TERM_DEPOSIT'
            
            if self.data_Struct.Instrument_Type and self.data_Struct.PACE_Message_Type:
                return self.data_Struct
                
        return False
    
    def __processInstrumentMessage(self):
        amb_obj = AMBA_Utils.object_by_name(self.data_Struct.message, ['!'], 'INSTRUMENT')
        if amb_obj:
            self.data_Struct.AMB_TRD_INSTR_Obj = amb_obj
            
            '''--------------------------------------------------------------------------
                                    Instrument Type Identification
            --------------------------------------------------------------------------'''
            leg_obj = AMBA_Utils.object_by_name(amb_obj, ['', '+', '!'], 'LEG')
            if leg_obj:
                leg_type = AMBA_Utils.get_AMBA_Object_Value(leg_obj, 'TYPE')
                if leg_type:
                    if leg_type in Params.VALID_CALL_LEG_TYPE:
                        self.data_Struct.Instrument_Type = 'CALL_DEPOSIT'
                    else:
                        self.data_Struct.Instrument_Type = 'FIXED_TERM_DEPOSIT'
            
            '''--------------------------------------------------------------------------
                        FIXED_TERM_DEPOSIT Expiry Day Amendment Identification
            --------------------------------------------------------------------------'''
            if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                original_exp_day = AMBA_Utils.get_AMBA_Object_Value(amb_obj, '!EXP_DAY')
                if not original_exp_day:
                    return False
                else:
                    self.data_Struct.PACE_Message_Type = 'Instrument Amendment'
            elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                for leg_obj in AMBA_Utils.objects_by_name(amb_obj, ['', '+', '!'], 'LEG'):
                    '''--------------------------------------------------------------------------
                                CALL_DEPOSIT amendment for Interest Reinvest Flag
                    --------------------------------------------------------------------------'''
                    original_Reinvest = AMBA_Utils.get_AMBA_Object_Value(leg_obj, '!REINVEST')
                    if original_Reinvest:
                        self.data_Struct.PACE_Message_Type = 'Instrument Amendment'
                        
                    '''--------------------------------------------------------------------------
                                CALL_DEPOSIT amendment for Interest Rate - Fixed Rate
                    --------------------------------------------------------------------------'''
                    original_FixedRate = AMBA_Utils.get_AMBA_Object_Value(leg_obj, '!FIXED_RATE')
                    if original_FixedRate:
                        self.data_Struct.PACE_Message_Type = 'Instrument Amendment Rate Change'

                    '''--------------------------------------------------------------------------
                            Select Inserted, Updated and Deleted Cashflows from Message
                    --------------------------------------------------------------------------'''
                    for cashFlow in AMBA_Utils.objects_by_name(leg_obj, ['+', '!', '-'], 'CASHFLOW'):
                        self.data_Struct.cashFlowList.append(cashFlow)
                if self.data_Struct.cashFlowList:
                    if self.data_Struct.PACE_Message_Type != 'Instrument Amendment Rate Change':
                        self.data_Struct.PACE_Message_Type = 'Call Trading'

            if self.data_Struct.Instrument_Type and self.data_Struct.PACE_Message_Type:
                return self.data_Struct
        return False
    
    def __processADSMessage(self):
        messageProcess = False
        try:
            self.data_Struct.ACM_object = acm.AMBAMessage.CreateSimulatedObject(self.data_Struct.messageAsString)
        except Exception, error:
            Utils.Log(True, 'Error in creation of simulated object: %s. \nAMBA Message:\n %s' %(error, self.data_Struct.messageAsString))

        if self.data_Struct.ACM_object:
            self.data_Struct.AMBA_Message_Type = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'TYPE')
            if self.data_Struct.ACM_object.IsKindOf(acm.FTrade):
                messageProcess = self.__processTradeMessage()
            elif self.data_Struct.ACM_object.IsKindOf(acm.FInstrument):
                messageProcess = self.__processInstrumentMessage()
                
        return messageProcess
    
    def __set_Exception_Detail(self, message_type, error_code, error_text):
        self.data_Struct.PACE_Message_Type = message_type
        self.data_Struct.ERROR_NUMBER = str(error_code)
        self.data_Struct.Free_Text = error_text
        return self.data_Struct
        
    def __processExternalMessage(self):
        '''-------------------------------------------------------------------------------------------------------
                            Retreive all relevant information from external message
        -------------------------------------------------------------------------------------------------------'''
        try:
            self.data_Struct.PACE_Message_Type = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'EVENT_TYPE').strip()
            self.data_Struct.Instrument_Type = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'INSTRUMENT_TYPE').strip()
            mmg_msg_id = AMBA_Utils.get_AMBA_Object_Value(self.data_Struct.message, 'MMG_MSG_ID').strip()
            
            data                            = AMBA_Utils.object_by_name(self.data_Struct.message, [''], 'DATA')
            amount                          = AMBA_Utils.get_AMBA_Object_Value(data, 'AMOUNT').strip()
            pace_mm_original_deal_id        = AMBA_Utils.get_AMBA_Object_Value(data, 'PACE_MM_ORIGINAL_DEAL_ID').strip()
            pace_mm_event_id                = AMBA_Utils.get_AMBA_Object_Value(data, 'PACE_MM_EVENT_ID').strip()
            fa_trade_id                     = AMBA_Utils.get_AMBA_Object_Value(data, 'FA_TRADE_ID').strip()
            fa_event_id                     = AMBA_Utils.get_AMBA_Object_Value(data, 'FA_EVENT_ID').strip()
            reinvest                        = AMBA_Utils.get_AMBA_Object_Value(data, 'CAPITALISE_INTEREST').strip()
            counterparty                    = AMBA_Utils.get_AMBA_Object_Value(data, 'COUNTERPARTY_ID').strip()
            rate                            = AMBA_Utils.get_AMBA_Object_Value(data, 'RATE').strip()
            currency                        = AMBA_Utils.get_AMBA_Object_Value(data, 'CURRENCY').strip()
            start_date                      = AMBA_Utils.get_AMBA_Object_Value(data, 'START_DATE').strip()
            trade_date                      = AMBA_Utils.get_AMBA_Object_Value(data, 'TRADE_DATE').strip()
            expiry_date                     = AMBA_Utils.get_AMBA_Object_Value(data, 'EXPIRY_DATE').strip()
            payment_instructions            = AMBA_Utils.get_AMBA_Object_Value(data, 'PAYMENT_INSTRUCTIONS').strip()            
        except:
            return False
        
        self.data_Struct.OPTIONAL_KEY       = 'BARXMM-%s-MMG-%s' %(str(pace_mm_original_deal_id), str(mmg_msg_id))
        barxID                              = 'BARXMM-%s-MMG-%s' %(str(pace_mm_event_id), str(mmg_msg_id))
        
        valid_CP = None
                
        '''----------------------------------------------------------------------------------------------------------------------------
            Checking Currency, Interest Rate, Counterparty SDS and Existance of Instrument and Trades before trying to action request
        ----------------------------------------------------------------------------------------------------------------------------'''

        if self.data_Struct.PACE_Message_Type == 'NEW':
            if not currency:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300013, 'ERROR: Currency supplied is blank on the message.')
                
            curr = acm.FCurrency[currency]
            
            '''--------------------------------------------------------------------------
                                        Valid Currency Check
            --------------------------------------------------------------------------'''
            if not curr:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300009, 'ERROR: Currency %s does not exist in Front Arena.'  % str(currency))
            
            '''--------------------------------------------------------------------------
                                        Currency Check
            --------------------------------------------------------------------------'''
            if curr.Name() not in Params.VALID_CURRENCIES:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300011, 'ERROR: Currency %s is not a valid currency.'  % str(currency))
            
            '''--------------------------------------------------------------------------
                                        Interest Rate Check
            --------------------------------------------------------------------------'''
            if curr.Name() == 'ZAR':
                rate_test = round(float(rate), 0)
                if rate_test == 0:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300010, 'ERROR: Front Arena does not take a 0 interest rate.')

        if self.data_Struct.PACE_Message_Type in ('NEW', 'CANCEL', 'DEPOSIT/WITHDRAWAL'):
            SDS = PACE_Utils.get_SDS_AddInfo(counterparty)
            
            '''--------------------------------------------------------------------------
                                        Existance of SDS ID Check
            --------------------------------------------------------------------------'''
            if not SDS:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300001, 'ERROR: SDS ID %s does not exist in Front Arena.' % str(counterparty))
                
            valid_CP = PACE_Utils.get_Counterparty(SDS)
            
            '''--------------------------------------------------------------------------
                                        Existance of PACE Client Check
            --------------------------------------------------------------------------'''
            if not valid_CP:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300003, 'ERROR: No valid PACE Client for SDS ID %s in Front Arena.' % str(counterparty))
            
            '''--------------------------------------------------------------------------
                                    Existance of Multiple PACE Client Check
            --------------------------------------------------------------------------'''
            if len(valid_CP) > 1:
                return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300002, 'ERROR: Multiple PACE Clients for SDS ID %s in Front Arena.'  % str(counterparty))
        
            booking_CP = valid_CP[0]
        
        if self.data_Struct.PACE_Message_Type in ('CANCEL', 'ACKNOWLEDGE'):
        
            '''--------------------------------------------------------------------------
                            Existance of Front Arena Trade and Instrument Check
            --------------------------------------------------------------------------'''
            trades = acm.FSortedCollection()
            if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                if (fa_trade_id is None) or (fa_trade_id.strip() == ""):
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: The trade ID has not been set.')
                trade = acm.FTrade[fa_trade_id]
                if not trade:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: Could not find trade: %s in Front Arena.' % str(fa_trade_id))
                    
                trades.Add(trade)
                
            elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                if (fa_trade_id is None) or (fa_trade_id.strip() == ""):
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: The instrument ID has not been set.')                    
                instrument = acm.FInstrument[fa_trade_id]
                if not instrument:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: Could not find instrument: %s in Front Arena.' % str(fa_trade_id))
                    
                if self.data_Struct.PACE_Message_Type == 'CANCEL':
                    trades = PACE_Utils.get_Trades(instrument.Oid())
                else:
                    trades = PACE_Utils.get_Trades(instrument.Oid(), True)
            
                if not trades:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: Could not find trade: %s in Front Arena.' % str(fa_trade_id))

        '''-----------------------------------------------------------------------------------------------------------------
            Process Message Types CANCEL, NEW, DEPOSIT/WITHDRAWAL, ACKNOWLEDGE and Existance of Front Arena entity check
        -----------------------------------------------------------------------------------------------------------------'''

        if self.data_Struct.PACE_Message_Type == 'CANCEL':

            '''--------------------------------------------------------------------------
                            Trade Status Check and Process CANCEL Message 
            --------------------------------------------------------------------------'''
            for trade in trades:
                '''--------------------------------------------------------------------------
                                        Valid Trade Status Check
                --------------------------------------------------------------------------'''
                if not ((trade.Status() in Params.VALID_TRADE_STATUS) and trade.Status() not in Params.CANCELLATION_TRADE_STATUS):
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300008, 'ERROR: Trade: %s is in an incorrect status in Front Arena.' % str(trade.Oid()))
                
                '''--------------------------------------------------------------------------
                                            Process CANCEL Message
                --------------------------------------------------------------------------'''
                tradeVoiding = Booking_Utils.PACE_MM_Trade_Voiding(trade, self.data_Struct.OPTIONAL_KEY)
                try:
                    tradeVoiding.voidTrade()
                    Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_original_deal_id), str(fa_trade_id)))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300006, 'ERROR: Trade: %s could not be Voided in Front Arena. %s' % (str(trade.Oid()), str(e)))

        if self.data_Struct.PACE_Message_Type == 'NEW':
            '''--------------------------------------------------------------------------
                                        Process NEW Message
            --------------------------------------------------------------------------'''
            if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                tradeBooking = Booking_Utils.PACE_MM_Trade_Booking(Params.FIXED_TERM_DEPOSIT_PORTFOLIO, self.data_Struct.Instrument_Type, currency, booking_CP, rate, amount, self.data_Struct.OPTIONAL_KEY, start_date, trade_date, payment_instructions, expiry_date)
                try:
                    trade_id = tradeBooking.termBooking()
                    Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_original_deal_id), str(trade_id)))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300007, 'ERROR: Could not create a new trade: %s.' % str(e))
            elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                tradeBooking = Booking_Utils.PACE_MM_Trade_Booking(Params.CALL_DEPOSIT_PORTFOLIO, self.data_Struct.Instrument_Type, currency, booking_CP, rate, amount, self.data_Struct.OPTIONAL_KEY, start_date, trade_date, payment_instructions)
                try:
                    trade_id = tradeBooking.callAccountBooking(reinvest, barxID)
                    Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_original_deal_id), str(trade_id)))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300007, 'ERROR: Could not create a new trade: %s.' % str(e))
        
        if self.data_Struct.PACE_Message_Type == 'DEPOSIT/WITHDRAWAL':
            if self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                if (fa_trade_id is None) or (fa_trade_id.strip() == ""):
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: The instrument ID has not been set.')
                    
                instrument = acm.FInstrument[fa_trade_id]

                '''--------------------------------------------------------------------------
                                        Instrument Existance Check
                --------------------------------------------------------------------------'''
                if not instrument:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: Could not find instrument %s in Front Arena.' % fa_trade_id)
                
                '''-------------------------------------------------------------------------------------------------
                            Work around code for SunGard core bug. ACM is a version behind the latest
                            ADS version of the instrument. Need to force a simulation on the instrument
                            and then un simulate it to get the latest version.
                -------------------------------------------------------------------------------------------------'''
                instrument.FreeText('Refresh Cache')
                instrument.Unsimulate()
                acm.PollDbEvents()
                
                valid_trades = PACE_Utils.get_Trades(instrument.Oid())
                
                '''--------------------------------------------------------------------------
                                        Valid Trade Existance Check
                --------------------------------------------------------------------------'''
                if not valid_trades:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300004, 'ERROR: Could not find a valid trade for instrument: %s.' % fa_trade_id)
                
                '''--------------------------------------------------------------------------
                                        Process DEPOSIT/WITHDRAWAL Message
                --------------------------------------------------------------------------'''
                tradeTransaction = Booking_Utils.Call_Account_Trading(instrument, amount, trade_date, barxID, payment_instructions)
                try:
                    cf_id = tradeTransaction.callAccountTrading()
                    Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA CASHFLOW ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_event_id), str(cf_id.Oid())))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300005, 'ERROR: Could not adjust instrument %s in Front Arena.' % str(fa_trade_id))
        
        if self.data_Struct.PACE_Message_Type == 'ACKNOWLEDGE':
            '''--------------------------------------------------------------------------
                                    Process ACKNOWLEDGE Message
            --------------------------------------------------------------------------'''
            
            if self.data_Struct.Instrument_Type == 'FIXED_TERM_DEPOSIT':
                for trade in trades:
                    ackClass = Booking_Utils.PACE_MM_Acknowledgement(trade, self.data_Struct.OPTIONAL_KEY)
                    try:
                        ackClass.ackFixedTermDeposit()
                        Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA TRADE NBR : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_original_deal_id), str(fa_trade_id)))
                    except Exception, e:
                        return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300012, 'ERROR: Could not accept Acknowledgement message from MMG %s. %s' % (str(mmg_msg_id), str(e)))
            elif self.data_Struct.Instrument_Type == 'CALL_DEPOSIT':
                ackClass = Booking_Utils.PACE_MM_Acknowledgement(instrument, self.data_Struct.OPTIONAL_KEY)
                try:
                    ackClass.ackCallDeposit()
                    Utils.Log(True, '%s - %s : BARX ID : %s : FRONT ARENA INSTRUMENT ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_original_deal_id), str(fa_trade_id)))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300012, 'ERROR: Could not accept Acknowledgement message from MMG %s. %s' % (str(mmg_msg_id), str(e)))
            elif self.data_Struct.Instrument_Type == 'DEPOSIT/WITHDRAWAL':
                '''--------------------------------------------------------------------------
                                        Valid Cash Flow Check
                --------------------------------------------------------------------------'''
                cfQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
                cfQuery.AddAttrNode('Oid', 'EQUAL', fa_event_id)
                cfs = cfQuery.Select()
                
                if not cfs:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300013, 'ERROR: Could not find Front Arena Cash Flow number %s.' % str(fa_event_id))
                    
                cf = cfs[0]
                ackClass = Booking_Utils.PACE_MM_Acknowledgement(cf, barxID)
                try:
                    ackClass.ackCallDepositTransaction()
                    Utils.Log(True, '%s - %s : PACE EVENT ID : %s : FRONT ARENA CASHFLOW ID : %s' % (self.data_Struct.PACE_Message_Type, self.data_Struct.Instrument_Type, str(pace_mm_event_id), str(fa_event_id)))
                except Exception, e:
                    return self.__set_Exception_Detail('NOT_ACKNOWLEDGE', 300012, 'ERROR: Could not accept Acknowledgement message from MMG %s. %s' % (str(mmg_msg_id), str(e)))
                    
        return False

    def process_AMBA_message(self):
        messageProcess = False
        if self.data_Struct.subject in Params.adsSubscriptionList:
            messageProcess = self.__processADSMessage()
        elif self.data_Struct.subject in Params.subscriptionExternalSource:
            messageProcess = self.__processExternalMessage()
        
        return messageProcess
