"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceXMLFunctions


DESCRIPTION
    All Common Functions in the entire project are defined in this Module in 
    Class ResetAdviceFunctions

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
"""

import acm


TEMPLATE = 'ABSA_IRS_Presettlement'

INVALID_ACQUIRERS = ['FMAINTENANCE',
                     'ZZZ DO NO USE MANAGEMENT',
                     'MIDAS DUAL KEY',
                     'Money Market Desk',
                     'Metals Desk',
                     'GT Internal Trades',
                     'Agris Desk']

INVALID_PORTFOLIOS = acm.FStoredASQLQuery['LCH_PORTFOLIOS'].Query().Select()

today = acm.Time.DateToday()

class ResetAdviceFunctions(object):
    """
    DESCRIPTION
    ResetAdviceAcquirerFunc  class
    """

    def __init__(self):
        pass

    @staticmethod
    def acquirer_contact_email(confirmation):
        """This Function returns contact email  from acquirer contact
            that will be passed to the email function"""
        party = confirmation.Acquirer()
        for i in party.Contacts():
            if i.Name() == confirmation.AcquirerContact():
                return i.Email()
                
        return None

    @staticmethod
    def acquirer_telephone(confirmation):
        """This Function returns telephone from acquirer contact
            that will be passed to the email function"""
        party = confirmation.Acquirer()
        for i in party.Contacts():
            if i.Name() == confirmation.AcquirerContact():
                return i.Telephone()
                
        return None

    @staticmethod
    def acquirer_attention(confirmation):
        """This Function returns attention from acquirer contact
            that will be passed to the email function"""
        party = confirmation.Acquirer()
        for i in party.Contacts():
            if i.Name() == confirmation.AcquirerContact():
                return i.Attention()
                
        return None

    @staticmethod
    def get_conf_event_type(confirmation):
        """This Function returns the confirmation event type
            that will be passed to the email function"""
            
        types = ['Reset Advice', 'Reset Confirmation']
        
        if confirmation.EventChlItem().Name() in types:
            conf_event = confirmation.EventChlItem().Name()
            if confirmation.Type() == 'Amendment':
                return conf_event + ' ' + confirmation.Type()
            elif confirmation.Type() == 'Cancellation':
                return conf_event + ' ' + confirmation.Type()
            else:
                if conf_event == 'Reset Confirmation':
                    return 'Presettlement Confirmation'
                else:
                    return conf_event
            
        return None
        
    @staticmethod
    def get_conf_date(confirmation):
        """This Function returns the Confirmation create time
        :rtype : date
        """
        date = acm.Time.DateFromTime(confirmation.CreateTime())
        if date:
            return date
        else:
            return acm.Time.DateToday()
        
    @staticmethod
    def check_prime_leg(trade):
        """"
        Checking Prime Trade
        """
        is_prime = False
        for leg in trade.Instrument().Legs():
            if ResetAdviceFunctions.is_prime_leg(leg):
                is_prime = True
                
        return is_prime
        
    @staticmethod
    def is_prime_leg(leg):
        """
        Checks if leg is prme linked
        """
        valid = False
        if leg.IsFloatLeg():
            if leg.FloatRateReference().Name() == "ZAR-PRIME":
                valid = True
            
        return valid
    
    @staticmethod
    def get_cp_cash_account_from_ssi(ssi):
        """Return the CP Cash Account from the Settle Instruction.

        Arguments:
        ssi (FSettleInstruction) -- Settle Instruction to get the CP account from.

        Returns FAccount, or None if no CP Cash Account is set.
        """
        cp_cash_account = None
        effective_rule = ResetAdviceFunctions.get_effective_rule(ssi)
        if effective_rule is not None:
            cp_cash_account = effective_rule.CashAccount()
            
        return cp_cash_account
        
    @staticmethod
    def get_effective_rule(ssi):
        """Return the effective SSI Rule, or None if none exists.

        Arguments:
        ssi (FSettleInstruction) -- Settle Instruction to test.
        """
        effective_rule = None
        for rule in ssi.Rules():
            if rule.EffectiveFrom() > acm.Time.DateNow():
                continue
            if rule.EffectiveTo() and rule.EffectiveTo() < acm.Time.DateNow():
                continue
            effective_rule = rule
            break
            
        return effective_rule

    @staticmethod
    def get_effective_ssis(trade, cftype=None):
        """Return a list of effective Settle Instructions (SSIs).

        The returned list of SSIs is ordered by the number of criteria matching
        the trade and cashflow type (the count of statements in the corresponding
        FASQLQuery) in descending order; the most specific SSIs appear first in
        the list.

        Arguments:
        trade (FTrade) -- Trade for which the settlement is to be done.
        cftype (str)   -- Type of the cashflow that is to be settled; e.g.
                          "Fixed Rate" or "Float Rate".
        """
        acquirer = trade.Acquirer()
        counterparty = trade.Counterparty()
        currency = trade.Currency()

        # Create a simulated settlement to get the matching SSIs.
        tmp_settlement = acm.FSettlement()
        tmp_settlement.Trade(trade)
        tmp_settlement.Acquirer(acquirer)
        tmp_settlement.Counterparty(counterparty)
        tmp_settlement.Currency(currency)
        tmp_settlement.Type(cftype)

        if counterparty is None:
            return []
        ssis = []
        for ssi in acquirer.SettleInstructions():
            # Get SSI query either from the Query() or QueryFilter() method.
            if ssi.Query():
                ssi_query = ssi.Query().Query()
            elif ssi.QueryFilter():
                ssi_query = ssi.QueryFilter()
            else:
                continue
            if (ssi_query.IsSatisfiedBy(tmp_settlement)
                    and ResetAdviceFunctions.get_effective_rule(ssi) is not None):
                ssis.append((ssi, ssi_query.StatementCount()))

        return [i[0] for i in sorted(ssis, key=lambda x: x[1], reverse=True)]
        
    @staticmethod    
    def is_valid_swap_trade(trade):
        """
        Evaluates trade against valid Swap business criteria
        """            
        if trade:
            if trade.Portfolio() in INVALID_PORTFOLIOS:
                return False
            if trade.Acquirer() and trade.Acquirer().Name() in INVALID_ACQUIRERS:
                return False
            if trade.Instrument().InsType() != 'Swap':
                return False
            if not ResetAdviceFunctions.valid_reset_advice_trade(trade):
                return False
                    
        return True

    @staticmethod
    def is_valid_fra_trade(trade):
        """
        Evaluates trade against valid FRA business criteria
        """
        if trade.Instrument().InsType() != 'FRA':
            return False
        if not ResetAdviceFunctions.valid_reset_advice_trade(trade):
            return False

        return True

    @staticmethod
    def is_valid_ccs_trade(trade):
        """
         Evaluates trade against valid CCS business criteria
        """
        if trade.Instrument().InsType() != 'CurrSwap':
            return False
        if trade.Instrument().NonDeliverable() is True:
            return False
        if trade.Counterparty().Type() == 'Intern Dept':
            return False
        if not ResetAdviceFunctions.valid_reset_advice_trade(trade):
            return False

        return True

    @staticmethod
    def valid_reset_advice_trade(trade):
        if trade.Type() != 'Normal':
            return False
        if trade.AdditionalInfo().Approx_46_load() is True:
            return False
        if trade.Status() in ('BO Confirmed', 'BO-BO Confirmed'):
            return True

        return False

    @staticmethod
    def evaluate_confinstruction_and_rule_setup(counterparty, instype, event):
        for confinstr in counterparty.ConfInstructions():
            if confinstr.EventChlItem() is None:
                continue
            elif confinstr.EventChlItem().Name() == event and confinstr.InsType() == instype:
                for rule in confinstr.ConfInstructionRules():
                    if rule.TemplateChoiceList() is None:
                        continue
                    elif rule.TemplateChoiceList().Name() == TEMPLATE:
                        return True
                        
    @staticmethod                  
    def is_compound(trade):
        for leg in trade.Instrument().Legs():
            if leg.IsFloatLeg():
                for cashflow in leg.CashFlows():
                    if cashflow.StartDate() <= today < cashflow.EndDate():
                        for reset in cashflow.Resets():
                            if reset.ResetType() in ('Compound', 'Weighted'):
                                return True
                        
        return False

    @staticmethod
    def get_last_reset_day(leg, date=today):
        for cashflow in leg.CashFlows():
            if cashflow.CashFlowType() == 'Float Rate' \
                    and cashflow.StartDate() <= date < cashflow.EndDate():
                if leg.IsFloatLeg() and cashflow.Resets():
                    last_reset = cashflow.Resets()[-1]
                    return last_reset.Day()
        raise RuntimeError('Unable to find last reset.')

    @staticmethod
    def get_multiple_reset_dates_from_legs(trade):
        receive_leg = trade.Instrument().RecLeg()
        pay_leg = trade.Instrument().PayLeg()

        if receive_leg.IsFloatLeg() and pay_leg.IsFloatLeg():
            rec_leg_date = ResetAdviceFunctions.get_last_reset_day(receive_leg)
            pay_leg_date = ResetAdviceFunctions.get_last_reset_day(pay_leg)
            return [rec_leg_date, pay_leg_date]

        if receive_leg.IsFloatLeg():
            return [ResetAdviceFunctions.get_last_reset_day(receive_leg)]
        elif pay_leg.IsFloatLeg():
            return [ResetAdviceFunctions.get_last_reset_day(pay_leg)]

        return [today]

    @staticmethod
    def format(value):
        """
        Function to format the values to 2 decimal places
        """
        return '{0:.2f}'.format(value)
