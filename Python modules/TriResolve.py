'''
Modifications:
    Melusi Maseko       MINT-1000       2017-01-27      Add logic for FX - Spot, FX - Swap, and FX Forward
    Bhavik Mistry       ABITFA-4924     2017-06-09      Added new Trade Group ID column
'''
import acm

# Much enhanced version of this file (one that adheres to TriResolve specs)
# can be found in P4 history (look for TriOptima.py)!

PRECIOUS_METALS = ['XAU', 'XAG', 'XPT', 'XPD']

COL_TRADE_ID        = 'TRADE_ID'
COL_TRADE_GROUP_ID  = 'TRADE_GROUP_ID'
COL_PARTY_ID        = 'PARTY_ID'
COL_CP_ID           = 'CP_ID'
COL_PRODUCT_CLASS   = 'PRODUCT_CLASS'
COL_TRADE_DATE      = 'TRADE_DATE'
COL_END_DATE        = 'END_DATE'
COL_NOTIONAL        = 'NOTIONAL'
COL_TRADE_CURR      = 'TRADE_CURR'
COL_NOTIONAL_2      = 'NOTIONAL_2'
COL_TRADE_CURR_2    = 'TRADE_CURR_2'
COL_UNDERLYING      = 'UNDERLYING'
COL_UNDERLYING_ISIN = 'UNDERLYING_ISIN'
COL_MTM_DATE        = 'MTM_DATE'
COL_MTM_VALUE       = 'MTM_VALUE'
COL_MTM_CURR        = 'MTM_CURR'
COL_CP_TRADE_ID     = 'CP_TRADE_ID'
COL_SWAPSWIRE_ID    = 'SWAPSWIRE_ID'
COL_PAY_REC         = 'PAY_REC'
COL_START_DATE      = 'START_DATE'
COL_STRIKE_PRICE    = 'STRIKE_PRICE'
COL_OPTION_TYPE     = 'OPTION_TYPE'
COL_BOOK            = 'BOOK'
COL_LEI             = 'LEI'
COL_DATA_SOURCE     = 'DATA_SOURCE'
COL_RATE            = 'RATE'
COL_COUPON_RATE     = 'COUPON_RATE'



COL_BROKER_CODE = "BROKER_CODE"


ABSA_LEI = 'SLI1CVYMJ21DST0Q8K25'
DATA_SOURCE_FRONT = 'FA'  # Front Arena

def insis(ins, *kinds):
    """Return a value indicating whether the specified instrument
    is of one of the kinds specified."""

    return any(ins.IsKindOf(kind) for kind in kinds)

def is_precmet(*instruments):
    """Return a value indicating whether any of the specified instruments
    can be classified as precious metals."""

    return any(ins.Name() in PRECIOUS_METALS for ins in instruments)

def product_class(trade):
    """Return TriResolve product class for the specified trade. Note that
    ABSA has it's own flavor which does not adhere to the official specs."""

    ins = trade.Instrument()
    if ins.IsKindOf(acm.FCurrency):
        if is_precmet(ins, trade.Currency()):
            return 'PreciousMetal - Forward' if trade.IsFxForward() else 'PreciousMetal'
        #MINT-1000 - Only define for Barclays
        elif (trade.Counterparty().Oid() in (10395, 33075) or trade.AdditionalInfo().Source_Ctpy_Id() in ('10538', '522623')) and trade.IsFxSwap():
            return 'FX - Swap'
        elif (trade.Counterparty().Oid() in (10395, 33075) or trade.AdditionalInfo().Source_Ctpy_Id() in ('10538', '522623')) and trade.IsFxSpot():
            return 'FX - Spot'
        elif (trade.Counterparty().Oid() in (10395, 33075) or trade.AdditionalInfo().Source_Ctpy_Id() in ('10538', '522623')) and trade.IsFxForward():
            return 'FX - Forward'
        else:
            return 'FX'
    if ins.IsKindOf(acm.FCreditDefaultSwap): return 'Credit Default Swap'
    if ins.IsKindOf(acm.FCurrencySwap): return 'CrossCurrency'
    if ins.IsKindOf(acm.FTotalReturnSwap):
        und = ins.IndexReference() or ins.Legs()[0].FloatRateReference()
        if not und: return
        if insis(und, acm.FStock, acm.FEquityIndex): return 'Equity - Swap'
        if und.IsKindOf(acm.FCommodity): return 'TRS - Commodity'
    if ins.IsKindOf(acm.FFuture):
        und = ins.Underlying()
        if insis(und, acm.FStock, acm.FEquityIndex): return 'Equity - Forward'
        if und.IsKindOf(acm.FCommodity): return 'Commodity - Forward'
        if und.IsKindOf(acm.FRateIndex): return 'InterestRate - Future/Forward'
    if ins.IsKindOf(acm.FOption):
        und = ins.Underlying()
        if is_precmet(und): return 'PreciousMetal - Option'
        if und.IsKindOf(acm.FCurrency): return 'FX - Option'
        if und.IsKindOf(acm.FCommodity): return 'Commodity - Option'
        if insis(und, acm.FStock, acm.FEquityIndex): return 'Equity - Option'
        if und.IsKindOf(acm.FSwap): return 'InterestRate - Option'

    if insis(ins, acm.FFra, acm.FCap, acm.FFloor): return 'InterestRate'
    if ins.IsKindOf(acm.FSwap): return 'InterestRate - Swap'
