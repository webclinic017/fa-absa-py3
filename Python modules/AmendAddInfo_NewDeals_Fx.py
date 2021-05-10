import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

ael_variables.add("query_folder",
                  label="Query Folder",
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Select("subType='FTrade'"))


PRODUCT_CODE = {'Flat Forward': '9FF',
                'Synthetic Forward': '9SF',
                'Leveraged Forward': '9LF',
                'Collar Plus': '9CP',
                'Geared Collar Plus': '9GCP',
                'Geared Collar ': '9GC ',
                'EDD Extention ': '9EDDE',
                'EDD Cancellation': '9EDDC',
                'Geared Forward': '9GF',
                'Geared Collar': '9GC',
                'EDD extension of Flat Forward': '9EDDF',
                'EDD extension of Synthetic Forward': '9EDDSF',
                'EDD Cancellation Flat Forward': '9EDDCFF',
                'EDD Cancellation of Synthetic Forward': '9EDDCSF',
                'Forward Plus': '9FP',
                'Geared Forward Plus': '9GFP',
                'Geared Extendable Forward': '9GEF',
                'Limited Protection Forward': '9MPF',
                'Forward Enhancer Plus': '9FEP',
                'Forward Spread': '9FS',
                'Calendar Spread': '9CS',
                'Knock out Forwards': '9KO',
                'Knock in Forwards': '9KI',
                'Geared Forward Spreads': '9GFS',
                'Calendar Spread ': '9CS',
                'Collar': '9ZCC',
                'Custom': '9CUST',
                'Forward': '9FWD',
                'Straddle': '9STRD',
                'Strangle': '9STRNG',
                'Call Spread': '9CSP',
                'Put Spread': '9PSP'
                }


def amend_add_info(trade, product_code):
    """
    Amend Approx. load, Approx. load ref and InsOverride for a given
    trade and product code is based on product type
    """
    clone_trade = trade.Clone()
    clone_trade.AddInfoValue('Approx. load', 'Yes')
    clone_trade.AddInfoValue('Approx. load ref', product_code)
    clone_trade.AddInfoValue('InsOverride', 'Combination - FX option')
    trade.Apply(clone_trade)
    try:
        trade.Commit()
        LOGGER.info("Successful Trade: %s, Product: %s, Code: %s",
                    trade.Name(),
                    trade.Instrument().ProductTypeChlItem().Name(),
                    product_code)
    except Exception as exc:
        LOGGER.exception("Error while committing the changes on the trade: %s", exc)


def get_product_code(trade):
    """Returns product code for a given product type"""
    try:
        instrument = trade.Instrument()
        product_type = instrument.ProductTypeChlItem().Name()
        product_code = PRODUCT_CODE[product_type]
        return product_code
    except Exception as exc:
        LOGGER.exception("Product type does not exist: %s", exc)


def ael_main(ael_dict):
    trades = ael_dict["query_folder"].Query().Select()
    for trade in trades:
        product_code = get_product_code(trade)
        amend_add_info(trade, product_code)
