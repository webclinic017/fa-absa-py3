"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceXMLGenerator


DESCRIPTION
    
    This Module is mainly used for xml generation for both the advice and confirmation 
    generation it contains classes and modules that help generate the xml needed for 
    the confirmation generation

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
"""

from datetime import datetime

import acm

from at_logging import getLogger
from DocumentXMLGenerator import GenerateDocumentXMLRequest, DocumentXMLGenerator
import DocumentConfirmationGeneral
import DocumentGeneral
from ResetAdviceXMLFunctions import ResetAdviceFunctions


LOGGER = getLogger(__name__)
daysBetween = acm.GetFunction('days_between', 4)


class ResetDocumentGenerator(GenerateDocumentXMLRequest):

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact, confirmation):
        """
        Constructor.
        """
        super(ResetDocumentGenerator, self).__init__(from_party, from_party_contact, to_party, to_party_contact)
        self.trade = confirmation.Trade()
        self.instype = confirmation.Trade().Instrument().InsType()


class ResetXMLGenerator(DocumentXMLGenerator):

    def __init__(self, trade, confirmation):
        self.trade = trade      
        self.date = acm.Time.DateToday()
        
        self.original_confirmation = DocumentConfirmationGeneral.get_original_confirmation(confirmation)
        self.second_reset_date = DocumentConfirmationGeneral.get_confirmation_to_date(self.original_confirmation)

        if self.original_confirmation:
            date = DocumentConfirmationGeneral.get_confirmation_from_date(self.original_confirmation)
            second_reset_date = DocumentConfirmationGeneral.get_confirmation_to_date(self.original_confirmation)
            if date:
                self.date = date
                self.second_reset_date = second_reset_date
            elif confirmation.EventChlItem().Name() == 'Reset Confirmation' and not date:
                date_list = []
                date_list.extend(ResetAdviceFunctions.get_multiple_reset_dates_from_legs(trade))
                if len(date_list) > 1:
                    self.date = date_list[0]
                    self.second_reset_date = date_list[1]
                self.date = date_list[0]
                                    
            elif confirmation.EventChlItem().Name() == 'Reset Advice' and not date:
                self.date = ResetAdviceFunctions.get_conf_date(confirmation)
            
        self.calculation_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self.confirmation = confirmation      

    def generate_xml(self, xml_request):
        try:
            return super(ResetXMLGenerator, self).generate_xml(xml_request)
            
        except Exception as exception:
            LOGGER.exception(exception)
            raise ValueError(exception)

    def _generate_subject_element(self, request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        instype = request.instype
        event = self.confirmation.EventChlItem().Name()
        if event == 'Reset Advice' and self.confirmation.Type() == 'Default':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'INTEREST RATE SWAP RESET ADVICE')
            elif instype == 'FRA':
                element = self._generate_element('SUBJECT', 'FORWARD RATE AGREEMENT PRESETTLEMENT CONFIRMATION')

        if event == 'Reset Advice' and self.confirmation.Type() == 'Amendment':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'AMENDMENT : INTEREST RATE SWAP RESET ADVICE')
            elif instype == 'FRA':
                element = self._generate_element('SUBJECT',
                                                 'AMENDMENT : FORWARD RATE AGREEMENT PRESETTLEMENT CONFIRMATION')

        if event == 'Reset Advice' and self.confirmation.Type() == 'Cancellation':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'CANCELLATION : INTEREST RATE SWAP RESET ADVICE')
            elif instype == 'FRA':
                element = self._generate_element('SUBJECT',
                                                 'CANCELLATION : FORWARD RATE AGREEMENT PRESETTLEMENT CONFIRMATION')

        if event == 'Reset Advice' and self.confirmation.Type() == 'Resend':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'INTEREST RATE SWAP RESET ADVICE')
            elif instype == 'FRA':
                element = self._generate_element('SUBJECT',
                                                 'FORWARD RATE AGREEMENT PRESETTLEMENT CONFIRMATION')
            
        if event == 'Reset Confirmation' and self.confirmation.Type() == 'Default':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'INTEREST RATE SWAP PRESETTLEMENT CONFIRMATION')
            elif instype == 'CurrSwap':
                element = self._generate_element('SUBJECT', 'CURRENCY SWAP PRESETTLEMENT CONFIRMATION')
            
        if event == 'Reset Confirmation' and self.confirmation.Type() == 'Amendment':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'AMENDMENT : INTEREST RATE SWAP PRESETTLEMENT CONFIRMATION')
            elif instype == 'CurrSwap':
                element = self._generate_element('SUBJECT', 'AMENDMENT : CURRENCY SWAP PRESETTLEMENT CONFIRMATION')
            
        if event == 'Reset Confirmation' and self.confirmation.Type() == 'Cancellation':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT',
                                                 'CANCELLATION : INTEREST RATE SWAP PRESETTLEMENT CONFIRMATION')
            elif instype == 'CurrSwap':
                element = self._generate_element('SUBJECT',
                                                 'CANCELLATION : CURRENCY SWAP PRESETTLEMENT CONFIRMATION')

        if event == 'Reset Confirmation' and self.confirmation.Type() == 'Resend':
            if instype == 'Swap':
                element = self._generate_element('SUBJECT', 'INTEREST RATE SWAP PRESETTLEMENT CONFIRMATION')
            elif instype == 'CurrSwap':
                element = self._generate_element('SUBJECT', 'CURRENCY SWAP PRESETTLEMENT CONFIRMATION')
        try:
            return element
        except Exception as exception:
            LOGGER.exception(exception)
            raise ValueError("Could not generate subject header for this Confirmation Type")

    def _generate_document_specific_element(self, xml_request):
        """
        Get Document Specific element RESET ADVICE
        """
        element = self._generate_element('RESET_ADVICE')
        element.append(self.get_trade())
        element.append(self.get_instrument(xml_request))
        element.append(self.get_party_ssi())

        return element

    def get_trade(self):
        """
        Get Trade Details
        """
        date_format = '%d/%m/%Y' if self.trade.Instrument().InsType() in ('Swap', 'CurrSwap') else '%d-%b-%Y'
        start_date = datetime(*acm.Time.DateToYMD(self.trade.Instrument().StartDate())).strftime(date_format)
        end_date = datetime(*acm.Time.DateToYMD(self.trade.Instrument().EndDate())).strftime(date_format)
        trade_date = datetime(*acm.Time.DateToYMD(self.trade.TradeTime())).strftime(date_format)
        element = self._generate_element('TRADE')
        element.append(self._generate_element('ACQUIRERCONTACTFULLNAME', str('Absa Bank Limited')))
        element.append(self._generate_element('TRDNUMBER', str(self.trade.Oid())))        
        element.append(self._generate_element('STARTDATE', str(start_date)))
        element.append(self._generate_element('ENDDATE', str(end_date)))
        element.append(self._generate_element('TRADEDATE', str(trade_date)))
        element.append(self._generate_element('CURRENCY', str(self.trade.Instrument().Currency().Name())))
        element.append(self._generate_element('NOTIONAL', str(self.trade.Nominal())))
        element.append(self._generate_element('INSTYPE', str(self.trade.Instrument().InsType())))
        
        return element

    def get_instrument(self, xml_request):
        """"
        Get Instrument Details
        """
        element = self._generate_element('INSTRUMENT')
        if xml_request.instype in ('Swap', 'CurrSwap'):
            element.append(self.get_swap_legs(xml_request.instype))
        elif xml_request.instype == 'FRA':
            element.append(self.get_fra_leg())

        return element

    def get_fra_leg(self):
        """"
        Get Instrument Details
        """
        trade = self.trade
        leg = trade.Instrument().Legs()[0]
        cashflow = leg.CashFlows()[0]
        element = self._generate_element('LEGS')
        element.append(self._generate_element('BUSINESS_DAY_CALENDAR', str(DocumentGeneral
            .get_leg_payment_calendars(leg))))
        element.append(self._generate_element('BUSINESS_DAY_CONVENTION', str(leg.PayDayMethod())))
        element.append(self._generate_element('DAY_COUNT_METHOD', str(leg.DayCountMethod())))
        element.append(self._generate_element('PAYMENT_DATE', str(cashflow.PayDate())))
        element.append(self._generate_element('FRA_DISCOUNTING', str('Applicable')))
        element.append(self._generate_element('FIXED_RATE_PAYER', str(DocumentGeneral.get_trade_buyer_name(trade))))
        element.append(self._generate_element('FIXED_RATE', str(leg.FixedRate())))
        element.append(self._generate_element('FLOAT_RATE_PAYER', str(DocumentGeneral.get_trade_seller_name(trade))))
        element.append(self._generate_element('FLOATING_RATE', str(cashflow.Resets().First().FixingValue())))
        element.append(self._generate_element('RATE_FIXING_OFFSET', str(leg.ResetDayOffset())))
        element.append(self._generate_element('RATE_REFERENCE', str(DocumentGeneral.get_float_rate_reference_name(
            leg.FloatRateReference()))))
        element.append(self._generate_element('RESET_BUSINESS_DAY_CALENDAR', str(DocumentGeneral
            .get_leg_reset_calendars(leg))))
        element.append(self._generate_element('FLOAT_RATE_SPREAD', str(leg.Spread())))
        element.append(self._generate_element('NET_AMOUNT_DUE', str(self.get_casflow_amount(cashflow))))
        direction_of_payment = \
            'Due To You' if float(self.get_casflow_amount(cashflow)) < 0 else 'Due To Absa Bank Limited'
        element.append(self._generate_element('DIRECTION_OF_PAYMENT', str(direction_of_payment)))

        return element

    def get_swap_legs(self, instype):
        """"
        Get Leg Details
        """
        element = self._generate_element('LEGS')
        receive_leg = self.trade.Instrument().RecLeg()
        pay_leg = self.trade.Instrument().PayLeg()

        element.append(self.get_swap_leg(pay_leg, 'PAY'))
        element.append(self.get_swap_leg(receive_leg, 'RECEIVE'))

        if instype == 'Swap':
            if receive_leg.RollingPeriod() == pay_leg.RollingPeriod():
                element.append(self.get_net_payment())
                element.append(self.get_payment_direction())
                element.append(self.get_payment_currency())
                element.append(self._generate_element('NET_AMOUNT_DUE', str('Net Amount Due')))

        return element

    def get_notional_amount(self, leg):
        """
        Function to get nominal
        """
        if leg.IsFloatLeg():
            cashflow = self.get_current_float_cf(leg)
        else:
            cashflow = self.get_current_cf(leg)

        if cashflow:
            amount = cashflow.Calculation().Nominal(self.calculation_space, self.trade, leg.Currency()).Number()
            return '{0:.2f}'.format(amount)
        else:
            raise ValueError('Could not find cashflow on instrument {ins}'.format(ins=leg.Instrument().Name()))

    def get_current_float_cf(self, leg):
        """
        Function to get current cashflow for float leg
        """
        if leg.IsFloatLeg():
            if ResetAdviceFunctions.check_prime_leg(self.trade):
                for cf in leg.CashFlows():
                    if cf.CashFlowType() == 'Float Rate' and cf.Resets():
                        if cf.StartDate() <= self.date < cf.EndDate():
                            last_reset = cf.Resets()[-1]
                            return last_reset.CashFlow()
            else:
                for cf in leg.CashFlows():
                    if cf.CashFlowType() == 'Float Rate':
                        for reset in cf.Resets():
                            if reset.Day() == self.date and cf.Resets()[-1].FixingValue() != 0.00:
                                return cf
                            elif reset.Day() == self.second_reset_date and cf.Resets()[-1].FixingValue() != 0.00:
                                return cf
        raise ValueError('Could not find cashflow with reset date: {date} for trade: {trade}'.format(date=self.date,
                                                                                                     trade=self.trade))

    def get_current_cf(self, leg):
        """
        Function to get current cashflow for fixed leg
        """        
        
        date = self.date
        for _leg in self.trade.Instrument().Legs():
            if _leg.IsFloatLeg():
                if self.get_current_float_cf(_leg):
                    date = self.get_current_float_cf(_leg).StartDate()
                
        for cashflow in leg.CashFlows():
            if cashflow.StartDate() <= date < cashflow.EndDate():
                return cashflow

    def get_casflow_amount(self, cashflow):
        """
        Function to get Cashflow Projected Amount
        """
        projected = cashflow.Calculation().Projected(self.calculation_space, self.trade).Number()
        proj_amount = round(projected, 4)
        
        return proj_amount

    def get_cashflow_nominal_amount(self, leg, cashflow):
        """
        Function to get nominal amount for cashflow
        """
        amount = cashflow.Calculation().Nominal(self.calculation_space, self.trade, leg.Currency()).Number()

        return amount

    def get_net_amount(self):
        """
        Returns the net amount for the settlement
        """
        trade = self.trade
        legs = trade.Instrument().Legs()
        _net_amount = 0
        for leg in legs:
            cf = None
            
            if leg.IsFixedLeg():
                cf = self.get_current_cf(leg)
            else:
                cf = self.get_current_float_cf(leg)
                
            _net_amount += self.get_casflow_amount(cf)            
        net_amount = round(_net_amount, 4)

        return net_amount
        
    def get_forward_rate(self, cashflow):
        """
        Function to get cashflow rate
        """
        forward_rate = (cashflow.Calculation().ForwardRate(self.calculation_space) * 100)
        
        return forward_rate

    def get_swap_leg(self, leg, leg_type):
        """
        Get Leg Element
        """
        element = self._generate_element(leg_type)
        trade = self.trade
        ins = self.trade.Instrument()
        direction = 'Floating Amount' if leg.IsFloatLeg() else 'Fixed Amount'
        rate = self.get_forward_rate(self.get_current_float_cf(leg)) if leg.IsFloatLeg() else leg.FixedRate()
        cashflow = self.get_current_float_cf(leg) if leg.IsFloatLeg() else self.get_current_cf(leg)
        notional_amount = self.get_notional_amount(leg)
        day_count_method = leg.DayCountMethod()
        days = days_between_cf_days(cashflow.StartDate(), cashflow.EndDate(), leg)
        pay_day = datetime(*acm.Time.DateToYMD(cashflow.PayDate())).strftime('%d/%m/%Y')
        payment_amount = ResetAdviceFunctions.format(float(self.get_casflow_amount(cashflow)))
        rolling_period = str(leg.RollingPeriodCount()) + ' ' + leg.RollingPeriodUnit()
        instype = ins.InsType()
        element.append(self._generate_element('DIRECTION', str(direction)))
        element.append(self._generate_element('NOMINAL', str(notional_amount)))
        element.append(self._generate_element('CURRENCY', str(leg.Currency().Name())))
        element.append(self._generate_element('SPREAD', str((leg.Spread()))))
        element.append(self._generate_element('DAY_COUNT_METHOD', str(day_count_method)))
        element.append(self._generate_element('RATE', str(rate)))
        element.append(self._generate_element('DAYS', str(days)))
        element.append(self._generate_element('PAYDAY', str(pay_day)))
        element.append(self._generate_element('INSTYPE', str(instype)))

        if instype == 'Swap':
            element.append(self._generate_element('AMOUNT', str(payment_amount)))
        elif instype == 'CurrSwap':
            pay_1_calendar = leg.PayCalendar().Name()
            pay_2_calendar = leg.Pay2Calendar().Name()
            element.append(self._generate_element('INTEREST_CALCULATION', str(payment_amount)))
            element.append(self._generate_element('ROLLING_PERIOD', str(rolling_period)))
            element.append(self._generate_element('PAYMENT_BUSINESS_DAY_CALENDAR_1', str(pay_1_calendar)))
            element.append(self._generate_element('PAYMENT_BUSINESS_DAY_CALENDAR_2', str(pay_2_calendar)))

        if leg_type == "PAY":
            if trade.Nominal() < 0:
                element.append(self._generate_element('PAYER', str(self.confirmation.Counterparty().Fullname())))
            if trade.Nominal() > 0:
                element.append(self._generate_element('PAYER', str('Absa Bank Limited')))
        elif leg_type == "RECEIVE":
            if trade.Nominal() < 0:
                element.append(self._generate_element('PAYER', str('Absa Bank Limited')))
            if trade.Nominal() > 0:
                element.append(self._generate_element('PAYER', str(self.confirmation.Counterparty().Fullname())))

        return element

    def get_net_payment(self):
        """
        Get Net Payment Details
        """        
        net_amount = str(ResetAdviceFunctions.format(float(self.get_net_amount())))
        element = self._generate_element('NET_AMOUNT', str(net_amount))

        return element
    
    def get_payment_direction(self):
        """
        Get Direction of Payment
        """
        direction = ' '
        if self.get_net_amount() < 0:
            direction = 'Due to You'
        elif self.get_net_amount() > 0:
            direction = 'Due to Absa Bank Limited'
        element = self._generate_element('DIRECTION_MESSAGE', str(direction))
        
        return element
        
    def get_payment_currency(self):
        """
        Get Direction of Payment
        """
        element = self._generate_element('CURRENCY', str(self.trade.Instrument().Currency().Name()))
        
        return element

    def get_party_ssi(self):
        """
        Get Party SSI Element Details
        """
        element = self._generate_element('PARTY_SSI')
        element.append(self.get_account())

        return element

    def get_account(self):
        """
        Get Account Element Details
        """
        element = self._generate_element('ACCOUNT')
        element.append(self.get_acquirer_ssi())

        return element

    def get_acquirer_ssi(self):
        """
        Get Acquirer SSI Acount Details
        """
        element = self._generate_element('ACQUIRER_SSI')        
        for ssi in ResetAdviceFunctions.get_effective_ssis(self.trade, 'None'):
            cash_account = ResetAdviceFunctions.get_cp_cash_account_from_ssi(ssi)
            if ssi and cash_account.Account():
                element.append(self._generate_element('BENEFICIARY', str('Absa Bank Limited')))
                element.append(self._generate_element('BENEFICIARYBIC', str('ABSAZAJJXXX')))                
                account = cash_account.Account().split()                
                if len(account) == 2:
                    account_number = account[1]
                else:
                    account_number = account[0]                     
                element.append(self._generate_element('ACCNUM', str(account_number)))
                if not cash_account.Currency().Name() == 'ZAR':
                    element.append(self._generate_element('CORRESBIC', str(cash_account.Bic().Name())))
                    element.append(self._generate_element('CORRESBANK', str(cash_account.CorrespondentBank().Name())))
                else:
                    element.append(self._generate_element('CORRESBIC', str('')))
                    element.append(self._generate_element('CORRESBANK', str('')))                    
                intermediary_bic = cash_account.Bic2()
                intermediary_account = cash_account.Account2()
                if intermediary_bic is not None:
                    element.append(self._generate_element('INTERMEDBIC', str(intermediary_bic.Name())))
                else:
                    element.append(self._generate_element('INTERMEDBIC', str(' ')))
                if intermediary_account is not None:
                    element.append(self._generate_element('INTERMEDACCNUM', str(cash_account.Account2())))
                else:
                    element.append(self._generate_element('INTERMEDACCNUM', str(' ')))

                return element
        
        raise ValueError('Unable To Load Account Number From applicable SSI\'s')


def reset_advice_xml(confirmation):
    xml_creator = ResetXMLGenerator(confirmation.Trade(), confirmation)
    doc_generator = ResetDocumentGenerator(confirmation.Acquirer(),
                                           confirmation.AcquirerContactRef(),
                                           confirmation.Counterparty(),
                                           confirmation.CounterpartyContactRef(),
                                           confirmation)
                                
    return xml_creator.generate_xml(doc_generator)


def get_reset_advice_email_body(confirmation):
    """This Function creates an html email body"""
    email_body = ('\n'
                  '        <!DOCTYPE html>\n'
                  '        <html>\n'
                  '          <head>\n'
                  '            <meta http-equiv="Content-Type" content="text/html; '
                  'charset=utf-8">\n'
                  '            <title>ResetAdvice</title>\n'
                  '            <style type="text/css" media="screen">\n'
                  '              table{{\n'
                  '                font-weight: normal;\n'
                  '                font-family: Verdana, Arial, Helvetica, sans-serif;\n'
                  '                font-size: 12;\n'
                  '                background-color: white;\n'
                  '                color:#5a5a5a;\n'
                  '              }}\n'
                  '            </style>\n'
                  '          </head>\n'
                  '            <body>\n'
                  '              <table>\n'
                  '                <tr><td style="font-weight:bold;padding-bottom: 15px;">'
                  'Dear Valued Customer</td></tr>\n'
                  '                <tr><td style="padding-bottom: 15px;">'
                  'Attached is your {event_Type} for {get_conf_date}</td></tr>\n'
                  '                <tr><td style="font-weight: bold; padding-bottom: 15px;">'
                  'Contact us</td></tr>\n'
                  '                <tr><td style="padding-bottom: 15px;">'
                  'If you have any questions or concerns related to this e-mail,'
                  ' please contact us.</td></tr>\n'
                  '                <tr><td style="padding-bottom: 15px;">'
                  'Yours sincerely,</td></tr>\n'
                  '                <tr><td>Absa | {acquirer_attention}</td></tr>\n'
                  '                <tr><td>{acquirer_telephone}</td></tr>\n'
                  '                <tr><td href="mailto:{acquirer_contact_email}">'
                  '{acquirer_contact_email}</td></tr>\n'
                  '              </table>\n'
                  '            </body>\n'
                  '        </html>')
                  
    return email_body.format(
        event_Type=ResetAdviceFunctions.get_conf_event_type(confirmation),
        get_conf_date=ResetAdviceFunctions.get_conf_date(confirmation),
        acquirer_attention=ResetAdviceFunctions.acquirer_attention(confirmation),
        acquirer_telephone=ResetAdviceFunctions.acquirer_telephone(confirmation),
        acquirer_contact_email=ResetAdviceFunctions.acquirer_contact_email(confirmation))


def get_reset_advice_email_subject(confirmation):
    """Function for creates email subject"""
    space = " "
    conf_date = ResetAdviceFunctions.get_conf_date(confirmation)
    counterparty = str(confirmation.Receiver().Fullname())
    event_name = confirmation.EventChlItem().Name()
    event = event_name if confirmation.Trade().Instrument().InsType() == 'Swap' else 'Presettlement Advice'
    if event_name == 'Reset Confirmation':
        event = 'Presettlement Confirmation'
    seq = (event + ":",
           counterparty,
           conf_date)
           
    return space.join(seq)


def get_bcc_address(confirmation):
    """This Function returns the acquirer contact email address"""
    prod_env = acm.FInstallationData.Select('').At(0).Name() == 'Production'
    if prod_env:
        return ResetAdviceFunctions.acquirer_contact_email(confirmation)
        
    return None


def get_reset_advice_filename(confirmation):
    """This Function returns filename which is event name + counterparty + confirmation date"""
    space = "_"
    conf_date = acm.Time.DateFromTime(confirmation.CreateTime())
    counterparty = str(confirmation.Receiver().Id())
    event_name = confirmation.EventChlItem().Name()
    event = event_name if confirmation.Trade().Instrument().InsType() == 'Swap' else 'Presettlement Advice'
    if event_name == 'Reset Confirmation':
        event = 'Presettlement Confirmation'
    seq = (event, counterparty, conf_date)
    
    return space.join(seq)


def days_between_cf_days(start_date, end_date, leg):
    """
    Calculates Days in a cash flow period
    """
    days = daysBetween(start_date,
                       end_date,
                       leg.DayCountMethod(),
                       leg.Currency().Calendar())
                        
    return int(days)
