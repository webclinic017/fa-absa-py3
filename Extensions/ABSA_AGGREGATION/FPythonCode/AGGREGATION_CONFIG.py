import acm


DEFAULT_COUNTERPARTY = acm.FParty['FMAINTENANCE']
DEFAULT_ACQUIRER = acm.FParty['FMAINTENANCE']
DEFAULT_TRADER = acm.FUser['AGGREGATION']
TRADE_STATUS_LIST = ['Simulated', 'BO-BO Confirmed', 'Void']