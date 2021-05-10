"""-----------------------------------------------------------------------------
PURPOSE              :  Constants and settings used in the CAL process.
REQUESTER, DEPATMENT :  Nhlanhleni Mchunu, PCG
PROJECT              :  Fix the Front - CAL
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2018-11-13  CHG1001100033  Libor Svoboda       Initial Implementation
2019-02-05  CHG1001325774  Libor Svoboda       Ignore optional_key and MTMUSER
                                               amendments
"""
import acm
from collections import OrderedDict
from at_portfolio import create_tree


DATE_TODAY = acm.Time.DateToday()
BACKDATE_CUTOFF = DATE_TODAY + ' 00:00:00'
LATE_CUTOFF = DATE_TODAY + ' 19:00:00'

UPDATE_THRESHOLD = 5.0  # in seconds

CTO_TYPE = 'Customizable'
CTO_SUBTYPE = 'CAL'

CAL_FLAGS = ('C', 'A', 'L', 'B')

CAL_PARAMS_NAME = 'CAL'  # FParameters extension object
EXCLUDE_USERS_FRONTEND_PARAM = 'ExcludeUsersFrontend'

CALCULATED_COLUMNS = (
    'Total Val End',
    'Portfolio Cash End',
    'Portfolio Accrued Interest',
    'Portfolio Profit Loss Period Position',
)
CALC_CURRENCY = acm.FCurrency['ZAR']

PRFNBR_EXCLUDE_FRONTEND = (
    7162,  # Simulate_GT Hypo Primary
    7163,  # Simulate_GT Hypo Control
)

COMP_PRFNBR_EXCLUDE_BACKEND = (
    4902,  # ABSA ALTERNATIVE ASSET MANAGEMENT
)

PRFTREE_EXCLUDE_BACKEND = [
    create_tree(acm.FPhysicalPortfolio[prfnbr])
        for prfnbr in COMP_PRFNBR_EXCLUDE_BACKEND
]

USRNBR_EXCLUDE_BACKEND = (
    1372, # ATS
    3374, # ATS_FRERATE_PRD
    1520, # ATSU5
    3695, # AGGREGATION
    915, # MTMUSER
)

USRGRP_EXCLUDE_FRONTEND = (
    627,  # AAM FO Trader
    604,  # PCG Collateral
)

USRGRP_SYSTEM = (
    494,  # Integration Process
    495,  # System Processes
)

SKIP_CALC_TRADE_FIELDS = {
    'optional_key',
    'type',
    'status',
    'trader_usrnbr',
    'group_trdnbr',
}
SKIP_CALC_CASHFLOW_FIELDS = {
    'extern_id',
}

BO_FIELDS_SET = {
    'status', 
    'bo_trdnbr', 
    'settle_category_chlnbr', 
    'your_ref',
    'optional_key',
    'type',
}
IGNORED_FIELDS = (
    'updat_time',
    'updat_usrnbr',
    'version_id',
    'your_ref',
    'optional_key',
    'insid',
)
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
AMEND_REASONS = OrderedDict([
    ('Adapter fed - Market wire backdate', ('Booking Error', 'System Error')),
    ('Adapter fed - Neutron backdate', ('Booking Error', 'System Error')),
    ('Adapter feed issue - Market wire', ('System Error',)),
    ('Adapter feed issue - Neutron', ('System Error',)),
    ('Addition of Fees/Commission/Brokerage - new', ('Trade lifecycle event',)),
    ('Allocations', ('Counterparty Request',)),
    ('Approximate loading indicator', ('Trade enrichment',)),
    ('Barrier lifecycle', ('Trade lifecycle event',)),
    ('Booking error', ('Booking Error',)),
    ('Calendar update', ('System limitation',)),
    ('Cancellation by CP', ('Counterparty request',)),
    ('Cash addition - new cash flow', ('Transaction event - deal specific',)),
    ('Cash addition - previously omitted', ('Booking Error',)),
    ('Cash addition - Counterparty Request', ('Counterparty Request',)),
    ('Close out of expired positions', ('Trade lifecycle event',)),
    ('Counterparty name update - system feed update', ('System Error',)),
    ('CPI Fixings', ('System Limitation',)),
    ('Dividend update', ('Trade lifecycle event',)),
    ('FA static clean up', ('System optimisation',)),
    ('Fund Linked Product', ('Trade lifecycle event',)),
    ('Graveyard update', ('Restructure/Portfolio Optimisation',)),
    ('Incorrect calendar information', ('Booking Error', 'System Error')),
    ('Incorrect calendar information - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect counter party', ('Booking Error',)),
    ('Incorrect counter party - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Dividend amend', ('Booking Error',)),
    ('Incorrect Dividend amend - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Fees/Commission/Brokerage amend', ('Booking Error',)),
    ('Incorrect Fees/Commission/Brokerage amend - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Fixed Rate', ('Booking Error',)),
    ('Incorrect Fixed Rate - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Funding Instype (MM)', ('Booking Error',)),
    ('Incorrect notional/nominal', ('Booking Error',)),
    ('Incorrect notional/nominal - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect portfolio', ('Booking Error',)),
    ('Incorrect premium', ('Booking Error',)),
    ('Incorrect premium - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Price', ('Booking Error',)),
    ('Incorrect Price - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Incorrect Reset', ('System Error', 'Booking Error')),
    ('Incorrect value date', ('Booking Error',)),
    ('Incorrect value date - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Mirror link amend', ('System Error',)),
    ('Mirror trade booking errors', ('Booking Error',)),
    ('Payment/Fee addition - new invoice', ('Transaction event - deal specific',)),
    ('Payment/Fee addition - previously omitted', ('Booking Error',)),
    ('Payment/Fee addition - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('Portfolio amend - booked in error', ('Booking Error',)),
    ('Portfolio amend - risk view optimisation', ('Restructure/Portfolio Optimisation',)),
    ('Portfolio amend', ('System Error',)),
    ('Sales credits', ('Trade enrichment',)),
    ('Trade incorrectly fed to source system', ('Booking Error',)),
    ('Trade incorrectly fed to source system - System Feed Issue', ('System Error',)),
    ('Trade omission', ('Booking Error',)),
    ('Trade omission - Feed Issue', ('System Error',)),
    ('Trade Restructure', ('Restructure/Portfolio Optimisation',)),
    ('Trioptima', ('Trade enrichment',)),
    ('Valuation Group change', ('Booking Error',)),
    ('Valuation Group change - Updated to align to Client Confirmation', ('Change required to agree with client on confirmation',)),
    ('System Flow', ('Trade enrichment',)),
    ('Incorrect ISIN', ('Booking Error',)),
    ('Trade in exception (Demat failure)', ('System Error',)),
    ('Incorrect BPID', ('Booking Error',)),
    ('PM Client Request - Cashflow', ('Counterparty Request',)),
    ('PM Client Request - Drawdown', ('Drawdown',)),
    ('PM Client Request - Prepayment', ('Prepayment',)),
    ('PM Client Request - Rollover', ('Rollover',)),
    ('PM Client Request - Interest Period Amend', ('Interest Period Amend',)),
    ('PM Client Request - Extension', ('Extension',)),
    ('PM Client Request - Additional Payment', ('Additional Payment',)),
    ('PM Client Request - Margin Adjustment', ('Margin Adjustment',)),
    ('PM Client Request - IFRS Loan Modification', ('IFRS Loan Modification',)),
    ('PM Trade correction - Margin Adjustment', ('Margin Adjustment',)),
    ('PM Trade correction - Interest Period Amend', ('Interest Period Amend',)),
    ('PM Trade correction - Cashflow', ('Cashflow',)),
    ('PM Trade correction - Additional Payment', ('Additional Payment',)),
    ('PM Trade correction - Calendar related', ('Calendar related',)),
    ('PM Trade Correction - IFRS Loan Modification', ('IFRS Loan Modification',)),
    ('PM Additional Payments - EOD Fee Script Run', ('EOD Fee Script Run',)),
    ('Duplicate', ('Booking Error',)),
    ('Incorrect direction', ('Booking Error',)),
    ('Quotation/Strike/CallPutAmend/rolling/ContSize/End&StartDate/DayCount/SettlementType', ('Static Update',)),
    ('Bond TRS Fixing', ('System Error',)),
    ('Additional info amend - Insoverride/Approx. load (&ref)/instype/PM_FacilityCPY/PM_FacilityID/etc', ('Trade enrichment',)),
    ('InsNameUpdate', ('Static Update',)),
    ('Incorrect client instruction', ('Counterparty Error',)),
    ('Late affirmation processed', ('Counterparty Error',)),
])
AMEND_REASONS_BACKDATE = (
    'Allocations',
    'Booking error',
    'Client Request',
    'Front Onboarding',
    'Marketwire trade',
    'Previously Simulated',
    'Trade omission',
    'Barrier Triggered',
    'Nominal scaling amend',
    'Trade Flow Failure',
    'Interest payments',
    'System issues',
)
AMEND_TYPE_BACKDATE = (
    'Backdate',
    'Booking Error',
    'Counter party requested amends',
    'System Error',
    'Restructure/Portfolio Optimisation',
    'System Limitation',
    'System optimisation',
    'Trade enrichment',
    'Trade lifecycle event',
    'Transaction event - deal specific',
    'Onboarding',
)

DEFAULTS = {
    'global': ('System feed/script issue', 'System Error'),
    'tcu': ('Bulk TCU Upload', 'System Limitation'),
    'treasury_hedge': ('Treasury hedge accounting', 'Trade lifecycle event'),
    'sec_loan': ('Security Loan', 'Trade lifecycle event'),
    'bo': ('BO confirmation', 'Trade lifecycle event'),
    'call_deposit': ('Call Account', 'Trade lifecycle event'),
    'amwi': ('Adapter feed issue - Market wire', 'System Error'),
    'amwi_backdate': ('Adapter fed - Market wire backdate', 'System Error'),
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
