"""-----------------------------------------------------------------------------
PURPOSE              :  Alternative CAL implementation using AMB instead of
                        direct table subscriptions via AEL.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-05-16  CHG1001670427  Libor Svoboda       Initial Implementation
2019-09-21  FAU            Libor Svoboda       Implement ael_sender_add hook
2020-05-26  CHG0102232     Libor Svoboda       Refactor
"""
import acm
from at_portfolio import create_tree


CAL_PARAMS_NAME = 'CAL'  # FParameters extension

CTO_TYPE = 'Customizable'

CALC_CURRENCY = acm.FCurrency['ZAR']

AMBA_FEED_START_PARAM = 'AmbaFeedStart'
AMBA_FEED_STOP_PARAM = 'AmbaFeedStop'

CALCULATED_COLUMNS = (
    'Total Val End',
    'Portfolio Cash End',
    'Portfolio Accrued Interest',
    'Portfolio Profit Loss Period Position',
)

CAL_FLAGS = ('C', 'A', 'L', 'B')

USRNBR_EXCLUDE_BACKEND = (
    1372, # ATS
    3374, # ATS_FRERATE_PRD
    1520, # ATSU5
    3695, # AGGREGATION
    915, # MTMUSER
)

COMP_PRFNBR_EXCLUDE_BACKEND = (
    4902,  # ABSA ALTERNATIVE ASSET MANAGEMENT
)

PRFTREE_EXCLUDE_BACKEND = [
    create_tree(acm.FPhysicalPortfolio[prfnbr])
        for prfnbr in COMP_PRFNBR_EXCLUDE_BACKEND
]

IGNORED_FIELDS = (
    'UPDAT_TIME',
    'UPDAT_USRNBR',
    'UPDAT_USRNBR.USERID',
    'VERSION_ID',
    'YOUR_REF',
    'OPTIONAL_KEY',
    'INSID',
)

BO_FIELDS_SET = {
    'STATUS', 
    'BO_TRDNBR', 
    'SETTLE_CATEGORY_CHLNBR', 
    'YOUR_REF',
    'OPTIONAL_KEY',
    'TYPE',
}

SKIP_CALC_TRADE_FIELDS = {
    'OPTIONAL_KEY',
    'TYPE',
    'STATUS',
    'TRADER_USRNBR',
    'GROUP_TRDNBR',
}

VALID_STATUS = (
    'Internal',
    'Reserved',
    'BO Confirmed',
    'BO-BO Confirmed',
    'FO Confirmed',
    'Terminated',
)

INITIAL_STATUS = (
    'Internal',
    'Reserved',
    'FO Confirmed',
)

DEFAULTS = {
    'global': ('System feed/script issue', 'System Error'),
    'tcu': ('Bulk TCU Upload', 'System Limitation'),
    'treasury_hedge': ('Treasury hedge accounting', 'Trade lifecycle event'),
    'sec_loan': ('Security Loan', 'Trade lifecycle event'),
    'bo': ('BO confirmation', 'Trade lifecycle event'),
    'call_deposit': ('Call Account', 'Trade lifecycle event'),
    'amwi': ('Adapter feed issue - Market wire', 'System Error'),
    'amwi_backdate': ('Adapter fed - Market wire backdate', 'Booking Error'),
}
DEFAULT_MAPPING_PORTFOLIO = {
    7162: {  # Simulate_GT Hypo Primary
        'default': DEFAULTS['treasury_hedge'],
    },
    7163: {  # Simulate_GT Hypo Control
        'default': DEFAULTS['treasury_hedge'],
    },
}
DEFAULT_MAPPING_USER = {
    2930: {  # ATS_AMWI_PRD
        'backdate': DEFAULTS['amwi_backdate'],
        'default': DEFAULTS['amwi'],
    },
}
DEFAULT_MAPPING_GROUP = {
    494: {  # Integration Process
        'default': DEFAULTS['global'],
    },
    646: {  # FO TCU Management
        'default': DEFAULTS['tcu'],
    },
    639: {  # FO TCU
        'default': DEFAULTS['tcu'],
    },
}
DEFAULT_MAPPING_INS = {
    'SecurityLoan': {
        lambda ins: True: DEFAULTS['sec_loan'],
    },
    'Deposit': {
        lambda ins: ins.open_end == 'Open End': DEFAULTS['call_deposit'],
    },
}

VALID_INSTYPE = (
    'Stock',
    'StockRight',
    'Future/Forward',
    'Option',
    'Warrant',
    'LEPO',
    'Bond',
    'FRN',
    'PromisLoan',
    'Zero',
    'Bill',
    'CD',
    'Deposit',
    'FRA',
    'Swap',
    'CurrSwap',
    'Cap',
    'Floor',
    'Collar',
    'Curr',
    'EquityIndex',
    'BondIndex',
    'RateIndex',
    'Convertible',
    'MultiOption',
    'MultiAsset',
    'Combination',
    'FreeDefCF',
    'FxSwap',
    'Collateral',
    'Repo/Reverse',
    'BuySellback',
    'PriceIndex',
    'IndexLinkedBond',
    'TotalReturnSwap',
    'CreditDefaultSwap',
    'EquitySwap',
    'Commodity',
    'DualCurrBond',
    'MBS/ABS',
    'CLN',
    'CallAccount',
    'CashCollateral',
    'BasketRepo/Reverse',
    'CreditIndex',
    'IndexLinkedSwap',
    'BasketSecurityLoan',
    'CFD',
    'VarianceSwap',
    'Fund',
    'Depositary Receipt',
    'FXOptionDatedFwd',
    'ETF',
    'Fx Rate',
    'PriceSwap',
    'Commodity Index',
    'Commodity Variant',
    'Certificate',
    'VolatilitySwap',
    'Credit Balance',
    'Dividend Point Index',
    'Flexi Bond',
    'Average Future/Forward',
)
