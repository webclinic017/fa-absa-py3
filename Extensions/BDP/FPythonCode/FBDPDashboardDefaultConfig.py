""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardDefaultConfig.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

ARCHIVED = 'Archived'
EXPIRED = 'Expired'
LIVE = 'Live'
TOTAL = 'Total'


DB_TABLE_NAME_TRADE = 'trade'
DB_TABLE_NAME_INSTRUMENT = 'instrument'
DB_TABLE_NAME_PRICE_HST = 'price'
DB_TABLE_NAME_ADDITIONAL_INFO = 'additional_info'


VIEW_TYPE_DATABASE = 'database'
VIEW_TYPE_TRADES = 'trades'
VIEW_TYPE_INSTRUMENTS = 'instruments'
VIEW_TYPE_PRICES = 'prices'


DB_TABLE_NAME_TO_VIEW_TYPE_MAP = {
    DB_TABLE_NAME_TRADE: VIEW_TYPE_TRADES,
    DB_TABLE_NAME_INSTRUMENT: VIEW_TYPE_INSTRUMENTS,
    DB_TABLE_NAME_PRICE_HST: VIEW_TYPE_PRICES
}


Aggregation_Action = {
        'Description':
                'Recommend to run the FAggregation script if the result '
                'counts exceed {0} on Status = Live.',
        'Key': 'Status = Live',
        'MaxCount': '60000',
        'Action': 'FAggregation'
}

Expiration_Action = {
        'Description':
                'Recommend to run the FExpiration script if the number of '
                'expired instruments exceeds {0}.',
        'Key': 'Status = Expired',
        'MaxCount': '1000',
        'Action': 'FExpiration'
}

DeletePrices_Action = {
        'Description':
                'Recommend to run the FDeletePrices script if the number of '
                'prices without instruments exceeds {0}.',
        'Key': 'Instrument status = Without Instrument',
        'MaxCount': '0',
        'Action': 'FDeletePrices'
}

DATABASE_QUERY_SPEC = {
        'Name': 'Database',
        'Description':
                'Shows the total database size ',
        'Category Name': ['MULTIPLE RESULTS'],
        'Select Result': 'EXEC sp_databases',
        'Query Condition': [''],
        'Result Condition': [''],
        'Action': None,
        'Unit Description': 'Number of kilobytes'
}

BDP_TABLES_QUERY_SPEC = {
        'Name': 'Table',
        'Description':
                'Shows the size of each table ',
        'Category Name': [
                DB_TABLE_NAME_TRADE,
                DB_TABLE_NAME_INSTRUMENT,
                DB_TABLE_NAME_PRICE_HST,
                DB_TABLE_NAME_ADDITIONAL_INFO],
        'Select Result': 'EXEC sp_spaceused ',
        'Query Condition': [
                DB_TABLE_NAME_TRADE,
                DB_TABLE_NAME_INSTRUMENT,
                DB_TABLE_NAME_PRICE_HST,
                DB_TABLE_NAME_ADDITIONAL_INFO],
        'Result Condition': ['', '', '', ''],
        'Action': None,
        'Unit Description': 'Number of kilobytes'
}

TRADE_STATUS_QUERY_SPEC = {
        'Name': 'Status',
        'Description':
                'Shows the number of trades that are archived and not '
                'archived.',
        'Category Name': [LIVE, ARCHIVED],
        'Select Result': 'SELECT count(trdnbr) FROM trade',
        'Query Condition': [
                'WHERE archive_status = 0',
                'WHERE archive_status = 1'
        ],
        'Result Condition': [
                'WHERE archive_status = 0',
                'WHERE archive_status = 1'
        ],
        'Action': [Aggregation_Action],
        'Unit Description': 'Number of trades'
}


TRADE_PORTFOLIO_QUERY_SPEC = {
        'Name': 'Portfolio',
        'Description':
                'Shows the number of trades per portfolio.',
        'Category Name': ['EVAL_ACM(acm.FPhysicalPortfolio[prfnbr])'],
        'Select Result': 'SELECT count(trdnbr), prfnbr FROM trade',
        'Query Condition': ['GROUP BY prfnbr'],
        'Result Condition': ['prfnbr = {0}'],
        'Action': None,
        'Unit Description': 'Number of trades'
}


TRADE_INSTNAME_QUERY_SPEC = {
        'Name': 'Instrument Name',
        'Description':
                'Shows the number of trades per instrument.',
        'Category Name': [
                'EVAL_ACM(acm.FInstrument[insaddr])'
        ],
        'Select Result': 'SELECT count(trdnbr), insaddr FROM trade',
        'Query Condition': ['GROUP BY insaddr'],
        'Result Condition': ['insaddr = {0}'],
        'Action': None,
        'Unit Description': 'Number of trades'
}

TRADE_DATE_QUERY_SPEC = {
        'Name': 'Trade Create Time',
        'Description': 'Shows the number of trades per day.',
        'Category Name': ['EVAL_TIME(time)'],
        'Select Result': 'SELECT COUNT(trdnbr), time FROM trade',
        'Query Condition': ['GROUP BY time'],
        'Result Condition': None,
        'Action': None,
        'Unit Description': 'Number of trades'
}

INST_STATUS_QUERY_SPEC = {
        'Name': 'Status',
        'Description':
                'Shows the number of instruments that are expired, live and '
                'archived.',
        'Category Name': [EXPIRED, LIVE, ARCHIVED],
        'Select Result': 'SELECT count(insaddr) FROM instrument',
        'Query Condition': [
                'WHERE archive_status = 0 and exp_day < GetDate()',
                ('WHERE archive_status = 0 and ('
                        'exp_day >= GetDate() or exp_day is NULL'
                        ')'
                ),
                'WHERE archive_status = 1'
        ],
        'Result Condition': [
                'WHERE archive_status = 0 and exp_day < GetDate()',
                ('WHERE archive_status = 0 and ('
                        'exp_day >= GetDate() or exp_day is NULL'
                        ')'
                ),
                'WHERE archive_status = 1'
        ],
        'Action': [Expiration_Action],
        'Unit Description': 'Number of instruments'
        }


INST_TYPE_QUERY_SPEC = {
        'Name': 'Instrument Type',
        'Description':
                'Shows the number of instruments by type.',
        'Category Name': [
                'EVAL_ACM(acm.FEnumeration[enum(InsType)].Enumerator(instype))'
        ],
        'Select Result': (
                'SELECT COUNT(insaddr), instype FROM instrument'
        ),
        'Query Condition': [
                'group by instype'
        ],
        'Result Condition': ['instype = {0}'],
        'Action': None,
        'Unit Description': 'Number of instruments'
}


INST_EXPIRYDATE_QUERY_SPEC = {
        'Name': 'Expiry Date',
        'Description':
                'Shows the number of instruments expiring per day.',
        'Category Name': ['EVAL_TIME(exp_day)'],
        'Select Result': 'SELECT COUNT(insaddr), exp_day FROM instrument',
        'Query Condition': ['group by exp_day'],
        'Result Condition': None,
        'Action': None,
        'Unit Description': 'Number of instruments'
}


PRICE_STATUS_QUERY_SPEC = {
        'Name': 'Instrument status',
        'Description':
                'Shows the number of prices that are linked to live, expired '
                'and without instrument.',
        'Category Name': [
                LIVE,
                EXPIRED,
                'Without Instrument'
        ],
        'Select Result': (
                'SELECT COUNT(prinbr) as "Number" '
                'FROM price_hst p'
        ),
        'Query Condition': [
                ('WHERE insaddr in ('
                        'select insaddr '
                        'from instrument '
                        'WHERE exp_day is NULL or exp_day >= GetDate()'
                        ')'
                ),
                ('WHERE insaddr in ('
                        'select insaddr '
                        'from instrument '
                        'WHERE exp_day < GetDate()'
                        ')'
                ),
                ('LEFT OUTER JOIN instrument i ON p.insaddr = i.insaddr '
                        'WHERE i.insaddr is NULL'
                )
        ],
        'Result Condition': [
                ('WHERE insaddr in ('
                        'select insaddr '
                        'from instrument '
                        'WHERE exp_day is NULL or exp_day >= GetDate()'
                        ')'
                ),
                ('WHERE insaddr in ('
                        'select insaddr '
                        'from instrument '
                        'WHERE exp_day < GetDate()'
                        ')'
                ),
                ('LEFT OUTER JOIN instrument i ON p.insaddr = i.insaddr '
                        'WHERE i.insaddr is NULL'
                )
        ],
        'Action': [DeletePrices_Action],
        'Unit Description': 'Number of prices'
}


PRICE_MARKET_QUERY_SPEC = {
        'Name': 'Market',
        'Description':
                'Shows the number of prices per market.',
        'Category Name': ['EVAL_ACM(acm.FParty[ptynbr])'],
        'Select Result': 'SELECT COUNT(prinbr), ptynbr FROM price_hst p',
        'Query Condition': ['group by ptynbr'],
        'Result Condition': ['ptynbr = {0}'],
        'Action': None,
        'Unit Description': 'Number of prices'
}


PRICE_DAY_QUERY_SPEC = {
        'Name': 'Date',
        'Description': 'Shows the number of prices per day.',
        'Category Name': ['EVAL_TIME(day)'],
        'Select Result': 'SELECT COUNT(prinbr), day FROM price_hst p',
        'Query Condition': ['group by day order by day DESC'],
        'Result Condition': None,
        'Action': None,
        'Unit Description': 'Number of prices'
}

DEFAULT_DATABASE_VIEW_NAME = 'Database Default'

DEFAULT_DATABASE_VIEW_DETAIL = [
        # A "View Detail" is a list, containing ordered "Query Spec"
        DATABASE_QUERY_SPEC,
        BDP_TABLES_QUERY_SPEC
]

DEFAULT_TRADE_VIEW_NAME = 'Trade Default'


DEFAULT_TRADE_VIEW_DETAIL = [
        # A "View Detail" is a list, containing ordered "Query Spec"
        TRADE_STATUS_QUERY_SPEC,
        TRADE_PORTFOLIO_QUERY_SPEC,
        TRADE_INSTNAME_QUERY_SPEC,
        TRADE_DATE_QUERY_SPEC
]


DEFAULT_INSTRUMENT_VIEW_NAME = 'Instrument Default'


DEFAULT_INSTRUMENT_VIEW_DETAIL = [
        # A "View Detail" is a list, containing ordered "Query Spec"
        INST_STATUS_QUERY_SPEC,
        INST_TYPE_QUERY_SPEC,
        INST_EXPIRYDATE_QUERY_SPEC
]


DEFAULT_PRICE_VIEW_NAME = 'Price Default'


DEFAULT_PRICE_VIEW_DETAIL = [
        # A "View Detail" is a list, containing ordered "Query Spec"
        PRICE_STATUS_QUERY_SPEC,
        PRICE_MARKET_QUERY_SPEC,
        PRICE_DAY_QUERY_SPEC
]


DEFAULT_CONFIG = {
        # A "Configuraton" is a dictionary, containing mappings from
        # "View Types" to "View Collections".
        #
        # "View Type": "View Collection"
        VIEW_TYPE_DATABASE: {
                DEFAULT_DATABASE_VIEW_NAME: DEFAULT_DATABASE_VIEW_DETAIL
        },
        VIEW_TYPE_TRADES: {
                # A "View Collections" is a dictionary, containing mappings
                # from "View Name" to "View Detail"
                #
                # "View Name": "View Detail"
                DEFAULT_TRADE_VIEW_NAME: DEFAULT_TRADE_VIEW_DETAIL
                # Some Trade View A name: Some Trade View A detail
                # Some Trade View B name: Some Trade View B detail
        },
        VIEW_TYPE_INSTRUMENTS: {
                DEFAULT_INSTRUMENT_VIEW_NAME: DEFAULT_INSTRUMENT_VIEW_DETAIL
                # Some Instrument View A name: Some Instrument View A detail
                # Some Instrument View B name: Some Instrument View B detail
        },
        VIEW_TYPE_PRICES: {
                DEFAULT_PRICE_VIEW_NAME: DEFAULT_PRICE_VIEW_DETAIL
                # Some Price View A name: Some Price View A detail
                # Some Price View B name: Some Price View B detail
        }
}


DEFAULT_VIEW_TYPES = list(DEFAULT_CONFIG.keys())
