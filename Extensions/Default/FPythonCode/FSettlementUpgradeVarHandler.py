""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeVarHandler.py"
from FSettlementEnums import SettlementStatus
   
class VariableHandler:
    def __init__(self):
        self.__variables = {}
        self.SetTradeFilterVariables()
    
    def SetVariable(self, variableName, defaultValue):
        import FSettlementVariables as OldVariables
        variable = getattr(OldVariables, variableName, defaultValue)
        self.__variables[variableName] = variable
        
    def GetVariables(self):
        return self.__variables
    
    def GetVariable(self, variableName):
        return self.__variables[variableName]

    def SetTradeFilterVariables(self):
        validInstrumentTypes =  ['BasketRepo/Reverse', 'BasketSecurityLoan', 'Bill',
                                 'Bond', 'BuySellback', 'Cap', 'CD', 'CFD', 
                                 'Combination', 'CreditDefaultSwap', 'Curr', 'CurrSwap', 
                                 'Deposit', 'DualCurrBond', 'EquityIndex', 'EquitySwap', 
                                 'Floor', 'FRA', 'FreeDefCF', 'FRN', 'Future/Forward',
                                 'FxSwap', 'IndexLinkedBond', 'IndexLinkedSwap', 'MBS/ABS', 'Option',
                                 'PromisLoan', 'Repo/Reverse', 'SecurityLoan', 'Stock', 
                                 'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Warrant', 'Zero']
        currDaysForwardDict = {'AUD':10, 'CAD':10, 'CHF':10, 'DKK':10, 'EUR':10, 'GBP':10, 'JPY':10, \
                               'LUF':10, 'NOK':10, 'NZD':10, 'SEK':10, 'SGD':10, 'USD':10, 'ZAR':10}
        keepStatuses = [SettlementStatus.NEW, SettlementStatus.RECALLED, SettlementStatus.UPDATED, SettlementStatus.EXCEPTION, SettlementStatus.MANUAL_MATCH, \
                       SettlementStatus.HOLD, SettlementStatus.VOID, SettlementStatus.AUTHORISED, SettlementStatus.NOT_ACKNOWLEDGED]
        validAccruedInsTypes = ['TotalReturnSwap', 'Swap']
        
        self.SetVariable('valid_instrument_types', validInstrumentTypes)
        self.SetVariable('status', ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'])
        self.SetVariable('exclude_acq', [])
        self.SetVariable('invert_exclude_acq', False)
        self.SetVariable('exclude_portfolio', [])
        self.SetVariable('invert_exclude_portfolio', False)
        self.SetVariable('special_otc_instrument_handling', 0)
        self.SetVariable('days_back', 10)
        self.SetVariable('days_curr', currDaysForwardDict)
        self.SetVariable('verbosity', 0)
        self.SetVariable('trace_level', 0)
        self.SetVariable('amb_login', '127.0.0.1:9137')
        self.SetVariable('print_mode', 1)
        self.SetVariable('RECEIVER_MB_NAME', 'BO_RECEIVER')
        self.SetVariable('RECEIVER_SOURCE', 'BO')
        self.SetVariable('handle_combination_cash_flows', 0)
        self.SetVariable('keep_status', keepStatuses)
        self.SetVariable('keep_old_settlements_when_void', 0)
        self.SetVariable('valid_instrument_types_accrued_interest', validAccruedInsTypes)
        self.SetVariable('round_net_amount', 0)
        self.SetVariable('alternative_coupon_handling', 0)
        self.SetVariable('update_void', 1)
        self.SetVariable('special_otc_instrument_handling', 0)
        self.SetVariable('recall_if_trade_status_is_terminated', 1)
        self.SetVariable('recall_if_trade_status_is_void', 1)
        self.SetVariable('update_recalled', 1)
        self.SetVariable('authorise_historic_value_day', 0)
        self.SetVariable('consider_resets_for_eq_swap_dividends', 1)
        self.SetVariable('forward_early_termination', 0)
        self.SetVariable('invert_exclude_acq', 0)
        self.SetVariable('invert_exclude_portfolio', 0)
    
