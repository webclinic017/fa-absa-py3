""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementParams - Parameters for the Settlement population procedure.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    Extracts and computes parameters for the Settlement population procedure.

----------------------------------------------------------------------------"""

import ael

"""----------------------------------------------------------------------------
CLASS
    FSettlement - Parameters for FSettlement scripts.

INHERITS


DESCRIPTION
    The class extracts all parameters needed to perform Settlement population.

CONSTRUCTION
    acc_curr    string      Accounting currency, ussualy fetched via
                            ael.used_acc_curr()
    days        int         The number of days from today that settlements
                            should be generated.
    days_back   int         The numbers of days back from today
    days_curr   dictionary  Should contain Currency (string) and it's int value
                            i.e. 'SEK':10
    status      List        A list of trade status levels to generate
                            settlements for.
    verbosity   int         Integer that indicate the level of information that
                            will be generated in the AEL console.
                            0 means print everything,
                            4 is the least one can print.

----------------------------------------------------------------------------"""
import sys, traceback

class Params:
    def __init__(self,**kwrds):
        self.acc_curr = 'EUR'
        self.days = 10
        self.days_back = 10
        self.days_curr = {}
        self.status = ['BO Confirmed']
        self.verbosity = 2
        self.amb_login = ''
        self.print_mode = 1
        self.RECEIVER_MB_NAME = ''
        self.RECEIVER_SOURCE = ''
        self.valid_instrument_types = \
            ['BasketRepo/Reverse', 'BasketSecurityLoan', 'Bill', 'Bond',
             'BuySellback', 'Cap', 'CD', 'CFD', 'Combination',
             'CreditDefaultSwap', 'Curr', 'CurrSwap', 'Deposit', 'DualCurrBond',
             'EquityIndex', 'EquitySwap', 'Floor', 'FRA', 'FreeDefCF', 'FRN', 'Future/Forward',
             'FxSwap', 'IndexLinkedBond', 'IndexLinkedSwap', 'MBS/ABS', 'Option', 'PromisLoan',
             'Repo/Reverse', 'SecurityLoan', 'Stock', 'Swap', 'TotalReturnSwap',
             'VarianceSwap', 'Warrant', 'Zero']
        self.valid_instrument_types_accrued_interest= \
            ['CreditDefaultSwap', 'EquitySwap', 'Swap', 'TotalReturnSwap']
        self.ZoneInfoImported = 1
        self.trans_size = 1000
        self.payment_types_cardinal = 18 #adapt also in get_system_default_params
        '''
        self.authorise_historic_value_day = 1
        Lets Settlements with status Exception and status_explanation Historic Value Date 
        to be Authorised. Triggers also End of Day procedure not to convert Authorised 
        settlements with old payday to status Exception and status explanation Historic Value Date
        Default value for authorise_historic_value_day is 0, meaning that the
        authorisation will not be done by default plus FSettlementEOD will do conversion.
        '''
        #self.authorise_historic_value_day = 1
        self.authorise_historic_value_day = 0
        self.handle_combination_cash_flows = 0
        self.keep_status = ['Exception']
        self.keep_old_settlements_when_void = 0 
        self.net_after_unnet = 1
        self.round_net_amount = 0
        self.alternative_coupon_handling = 0
        self.exclude_acq = []
        self.exclude_portfolio = []
        self.update_void = 1
        self.special_otc_instrument_handling = 0
        self.consider_resets_for_eq_swap_dividends = 1
        self.recall_if_trade_status_is_void = 1
        self.update_recalled = 1
        self.network_update = self.has_network_update()
        self.forward_early_termination = 0
        self.invert_exclude_acq = 0
        self.invert_exclude_portfolio = 0
        self.CALL_BACK_SLEEP = 0.5
        self.cash_flow_additional_infos = []
        self.days_forward_for_call_account = 1

        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to params ignored ARG = ", k
            else:
                if k not in ['valid_instrument_types', 'valid_instrument_types_accrued_interest']:
                    self.__dict__[k] = v
                elif k == 'valid_instrument_types':
                    use = []
                    for instype in v:
                        if instype in self.valid_instrument_types:
                            use.append(instype)
                        else:
                            print 'Warning: Unsupported instype', instype,\
                            'in FSettlementVariables.valid_instrument_types'
                            print 'This instrument type will be ignored.'
                    self.__dict__[k] = use
                elif k == 'valid_instrument_types_accrued_interest':
                    use = []
                    for instype in v:
                        if instype in self.valid_instrument_types_accrued_interest:
                            use.append(instype)
                        else:
                            print 'Warning: Unsupported instype', instype,\
                            'in FSettlementVariables.valid_instrument_types_accrued_interest'
                            print 'This instrument type will be ignored.'
                    self.__dict__[k] = use
                    
        # add verification code here
        if self.days < 0 : raise "Error days must be > 0 "

        i = 0
        while ael.enum_to_string('PaymentType', i) != '?':
            i += 1
        if i - 1 != self.payment_types_cardinal:
            print 'Warning: Unexpected number of elements (%d) in the '\
            'PaymentType enum.\n'\
            'Check FSettlementParams.payment_types_cardinal and '\
            'FSettlementGeneral.invalid_payment_types' % (i - 1)

    def __str__(self):
        user_var_module = import_user_variables()
        s = ""
        for k, v in user_var_module.__dict__.items():
            if k[0] != '_' and k != 'ael':
                s += ( str(k) +  " --> " + str(v) + "\n")
        return s
        
    def has_network_update(self):
        columns = ael.Settlement.columns()
        returned_boolean = False
        if 'party_account_network_name' in columns and \
           'acquirer_account_network_name' in columns:
            returned_boolean = True
        return returned_boolean

def dump_trace():
    try:
        traceback.print_exc(file=sys.stdout)
    except:
        print "Failed to print traceback"

def import_user_variables():
    try:
        import FSettlementVariables as var
    except ImportError:
        import FSettlementVariablesTemplate as var
    except Exception:
        print "Failed to import module FSettlementVariables : "
        dump_trace()
        print "Using defaults"
        var = None
    return var

def get_system_default_params(user_pars):
    try:
        import zoneinfo
        user_pars['ZoneInfoImported'] = 1
    except:
        user_pars['ZoneInfoImported'] = 0

    user_pars['trans_size'] = 1000
    user_pars['payment_types_cardinal'] = 18

def get_user_default_params(user_pars):
    user_var_module = import_user_variables()
    for k, v in user_var_module.__dict__.items():
        if k[0] != '_':
            if not isinstance(v, type(sys)):
                user_pars[k] = v

def get_default_params():
    user_pars = {}
    get_user_default_params(user_pars)
    get_system_default_params(user_pars)
    p = Params(**user_pars)
    return p

#print "Used params:\n",get_default_params()



