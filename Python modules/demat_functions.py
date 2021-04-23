"""demat_functions: last updated on Wed Apr 06, 2016. Extracted by """
from at_time import to_date

"""----------------------------------------------------------------------------------------------------------
MODULE                  :       demat_functions
PURPOSE                 :       The modules has functions to used by different demat modules to perform demat 
                                calculations and operations
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       Linda Breytenbach
DEVELOPER               :       Manan Ghosh
CR NUMBER               :       CHNG0003744247 (2016-08-19)
-------------------------------------------------------------------------------------------------------------
HISTORY
=============================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------
2016-08-23      CHNG0003898744  Willie van der Bank     Updated is_demat to cater for netted settlements.
2016-08-25      CHNG0003908106  Willie van der Bank     Fixed issue with is_demat
2017-01-26      CHNG0004260701  Willie van der Bank     Amended is_demat rule to take acquirer into consideration
2017-12-11      CHNG0005220511  Manan Ghosh             DIS go-live
2018-01-25      CHG1000078271   Willie vd Bank          Modified GetFirstTrade function for DIS
2019-07-09      FAOPS-553       Hugo Decloedt           Fix bug
2019-12-10      FAOPS-697       Stuart Wilson           Performance fix
2020-08-07      FAOPS-847       Jaysen Naicker          Add Demat Instype "RBD" on a CD Ticket for SARB Debentures 
2020-07-20      FAOPS-780       Ntokozo Skosana         Modified GetFirstTrade function for DIS
-------------------------------------------------------------------------------------------------------------
"""

import acm
import ael
import at_addInfo
from demat_isin_mgmt_menex import dis_unissued_amount,  MMSS_ISIN_REQUEST_STATE_CHART_NAME, DIS_ISIN_REQUEST_STATE_CHART_NAME
from at_type_helpers import to_acm
from SAGEN_IT_Functions import get_trd_from_possible_nettsettle
from demat_config import INSquery, TRADEquery, DISTRADEquery, DISINSquery
from logging import getLogger
from PTSPrimeBrokingModifier import PTSPrimeBrokingModifier

PB_MODIFIER = None

LOGGER = getLogger('demat_functions')
RELEVANT_PORTFOLIO = [
                       acm.FPhysicalPortfolio['2474']
                     ]
ISSUER_BANK = [
    acm.FParty['ABSA BANK LTD']
]

DEMAT_TRADER_CSD_BPID = 'ZA600195'

#Instrument
MM_ISSUER               = 'MM_Issuer'
MM_AGENT_PART_CODE      = 'MM_AgentPartCode'
MM_DEMAT_MIN_TRD_DENOM  = 'MM_DEMAT_MinTrdDeno'
MM_DEMAT_MIN_ISS_DENOM  = 'MM_DEMAT_MinIssDeno'
MM_COUP_PMT_INDIC       = 'MM_CouponPayIndic'
MM_COUP_PMT_MATURITY    = 'MM_CouponAtMaturity'
MM_COUP_PMT_CALC        = 'MM_AutoCoupPayCalc'
MM_ACCEPTOR_OF_MMI      = 'MM_AccepofMMI'

#Portfolio
MM_ISSUING_SOR_ACCT     = 'MM_DEMAT_SORAccNbr'

#Trade
MM_SECURITY_TYPE        = 'MM_Instype'
MM_CPY_BPID             = 'MM_DEMAT_CP_BPID'
MM_ACQ_BPID             = 'Demat_Acq_BPID'
MM_ACQ_SOR_ACC          = 'Demat_Acq_SOR_Ac'
MM_DELIV_VS_PMT         = 'Demat_Deliv_vs_Paym'

#Confirmation
MM_EVENT_NEW_TRADE       = 'New Trade'
MM_EVENT_MATCH_REQUEST   = 'Demat Match Request'
MM_EVENT_MATCH_PRESETTLE = 'Demat PreSettle Conf'

CATEGORIES = {
             'FRN': 'CAT1',
             'Bond': 'CAT2',
             'IndexLinkedBond': 'CAT3',
             'Zero': 'CAT3'
              }

INS_TYPES = {'FRN': 
                 ['FRN', 'LNCD', 'BOND', 'NOTX'],
             'CD':  
                 ['NCD', 'NCC', 'PN', 'RBD'],
             'Bill':
                 ['TB', 'SARB Debenture'],
             'CLN':
                 ['CLN'],
             'Bond':
                 ['BOND', 'NOTX'],
             'IndexLinkedBond':
                 ['BOND', 'NOTX'],
             'Zero':
                 ['BOND', 'NOTX']
             }

INS_TYPE_CODE = {'SARB Debenture': 'DEB'}

MM_ADDINFO_FIELDS = [
                         MM_CPY_BPID,
                         MM_ACQ_BPID,
                         MM_ACQ_SOR_ACC
                    ]

"""################################################################################
# 
# Following functions are used to validate the  'Request ISIN' time series
#
###################################################################################"""


def is_active(subject):
    """
    This indicates if the Instrument is in Business Process and the Current State is 'Ready'
    """
    process = get_business_process(subject and subject.Name() or '', MMSS_ISIN_REQUEST_STATE_CHART_NAME)
    if process:
        cs = process.CurrentStep()
        return True, (cs.State().Name() == 'Active')
    else:
        return False, False


def is_active_dis(subject):
    """
    This indicates if the Instrument is in Business Process and the Current State is 'Ready'
    """

    process = get_business_process(subject and subject.Name() or '', DIS_ISIN_REQUEST_STATE_CHART_NAME)
    if process:
        return True, True
    else:
        return False, False


def get_business_process(subject_name, process_name):
    if subject_name:
        ins = acm.FInstrument.Select01("name = '%s' " % subject_name, "")
        bp = acm.FBusinessProcess.Select01("subject_seqnbr = %d " % ins.Oid(), "")
        if bp is not None and bp.StateChart().Name() == process_name:
            return bp

    return None


def dis_coupon_amount(cf):
    """
    This function is to calculate the coupon amount for the net amount = authorised amount - issued amount
    """
    leg = cf.Leg()
    ins = cf.Instrument()
    staticLegInfo = leg.StaticLegInformation(ins, acm.Time().DateToday(), None)
    legInfo = leg.LegInformation(acm.Time().DateToday())
    nettAmount = dis_unissued_amount(ins)
    cashflowAmount = 0.0
    nominalAmount = cf.Instrument().NominalAmount()
    cumweight = 0.0
    cumweightrate = 0.0

    cfInfo = cf.CashFlowInformation(staticLegInfo)
    if cf.CashFlowType() == 'Fixed Rate':
        cashflowAmount = cfInfo.Rate(legInfo) * cfInfo.CashFlowBase(legInfo, acm.Time().DateToday()).Number()

    if cf.CashFlowType() == 'Float Rate':
        rate = None
        for reset in cf.Resets():

            if reset.ResetType() == 'Single':
                rate = reset.FixingValue() / 100.0

            if reset.ResetType() == 'Weighted':
                weight = (to_date(reset.EndDate()) - to_date(reset.StartDate())).days
                cumweight = cumweight + weight
                cumweightrate += reset.FixingValue() * weight

            if cumweight != 0.0 and cumweightrate != 0.0:
                rate = (cumweightrate / (cumweight * 100.0))

        if rate is None or rate == 0.0:
            forwardCurve = leg.Calculation().MappedForwardCurve(acm.Calculations()
                                                                .CreateStandardCalculationsSpaceCollection())
            leg.CurrentFixingValue(leg.FloatRateReference(), None, forwardCurve, acm.Time().DateToday())
            dvaRate = leg.CurrentFixingValue(leg.FloatRateReference(), None, forwardCurve, acm.Time().DateToday())
            dvRate = dvaRate.Size() > 0 and dvaRate.At(0) or None
            rate = dvRate and dvRate.Number() or 0.0
        cashflowAmount = (rate + cfInfo.Spread()) * cfInfo.CashFlowBase(legInfo, acm.Time().DateToday()).Number()

    paymentAmount = (cashflowAmount * nettAmount / nominalAmount)

    return paymentAmount


def dis_coupon_amount_calc(cf):
    """
    This function is to calculate the coupon amount for the net amount = authorised amount - issued amount
    """
    ins = cf.Instrument()
    nettAmount = dis_unissued_amount(ins)
    cashflowAmount = 0.0
    nominalAmount = cf.Instrument().NominalAmount()
    first_trade = GetFirstTrade(ins)
    quantity = first_trade and first_trade.Quantity() or 1.0

    if cf.CashFlowType() in ['Float Rate', 'Fixed Rate']:
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        cashflowAmount = cf.Calculation().Projected(calcSpace, first_trade).Number()

    paymentAmount = (cashflowAmount * nettAmount / (nominalAmount * quantity))

    return paymentAmount


def child_portfolios(prf_name):
    prf = ael.Portfolio[prf_name]
    portfolios = [prf.prfid]
    for chld in prf.children():
        if hasattr(chld, 'member_prfnbr'):
            portfolios = portfolios + [chld.member_prfnbr.prfid]

    return portfolios


def getIssuerList(ins):
    _return = []
    query = acm.CreateFASQLQuery('FParty', 'OR')

    for cpty in query.Select():
        _return.append(cpty.Name())
    return _return


def is_dis(fobj):
    fobj = to_acm(fobj)
    ins = None

    if fobj.IsKindOf(acm.FInstrument):
        ins = fobj

    elif fobj.IsKindOf(acm.FSettlement):
        ins = fobj.SecurityInstrument()

    elif fobj.IsKindOf(acm.FTrade):
        if acm.FStoredASQLQuery[DISTRADEquery].Query().IsSatisfiedBy(fobj):
            ins = fobj.Instrument()

    if ins:
        return acm.FStoredASQLQuery[DISINSquery].Query().IsSatisfiedBy(ins)
    return False


def is_demat(fobj):
    fobj = to_acm(fobj)
    ins = None
    if fobj.IsKindOf(acm.FInstrument):
        ins = fobj
    elif fobj.IsKindOf(acm.FSettlement):
        trade = get_trd_from_possible_nettsettle(fobj)
        if trade:
            return is_demat(trade)
    elif fobj.IsKindOf(acm.FTrade):
        if acm.FStoredASQLQuery[TRADEquery].Query().IsSatisfiedBy(fobj):
            ins = fobj.Instrument()
        else:
            return False
    if ins:
        return acm.FStoredASQLQuery[INSquery].Query().IsSatisfiedBy(ins)


def is_demat_dis(fobj):
    fobj = to_acm(fobj)
    ins = None
    if fobj.IsKindOf(acm.FInstrument):
        ins = fobj
    elif fobj.IsKindOf(acm.FSettlement):
        trade = get_trd_from_possible_nettsettle(fobj)
        if trade:
            return is_demat_dis(trade)
    elif fobj.IsKindOf(acm.FTrade):
        if acm.FStoredASQLQuery[TRADEquery].Query().IsSatisfiedBy(fobj) \
                or acm.FStoredASQLQuery[TRADEquery].Query().IsSatisfiedBy(fobj):
            ins = fobj.Instrument()

    if ins:
        return acm.FStoredASQLQuery[INSquery].Query().IsSatisfiedBy(ins) \
                or acm.FStoredASQLQuery[DISINSquery].Query().IsSatisfiedBy(ins)


def is_valid_trade(trade):
    instr = trade.Instrument()
    missing_fields = []

    if instr.InsType() not in ['FRN', 'CD', 'CLN', 'Bill', 'Bond', 'Zero', 'IndexLinkedBond']:
        return False,  []

    if not trade.Counterparty():
        LOGGER.debug('Trade Counterparty is missing')
        return False,  []

    if not trade.Portfolio():
        LOGGER.debug('Trade Portfolio is missing')
        return False, []

    if not trade.Acquirer():
        LOGGER.debug('Trade Acquirer is missing')
        return False, []

    if not trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        LOGGER.debug('Trade Status is invalid')
        return False, []

    if trade.TradeCategory() == "Collateral" and trade.match_portfolio(acm.FCompoundPortfolio[13923]):
        # Prfnbr 13923 = SBL_NONCASH_COLLATERAL portfolio
        LOGGER.debug("SBL collateral management trade")
        return False, []

    for add_info in MM_ADDINFO_FIELDS:
        add_info_value = at_addInfo.get_value(trade, add_info)
        if not add_info_value:
            missing_fields.append(add_info)
    print 'missing_fields', missing_fields

    if is_demat(trade):
        return True,  missing_fields

    if is_dis(trade):
        return True, []

    return False, []


def GetFirstTrade(fobj):
    """
    The first trade done for an instrument
    GValidation should also be tested for any changes to this function
    """
    valid_status = ['BO-BO Confirmed']
    if is_dis(fobj):
        valid_status = ['BO Confirmed', 'BO-BO Confirmed']

    ins_trade_start = 0
    ins = None
    first_trade = None

    if fobj is not None:
        if fobj.IsKindOf(acm.FTrade):
            ins = fobj.Instrument()
            if fobj.Status() in valid_status:
                if _qualifying_trade(fobj):
                    ins_trade_start = fobj.CreateTime()
                    first_trade = fobj

        elif fobj.IsKindOf(acm.FInstrument):
            ins = fobj

        instr = acm.FInstrument.Select01("name = '%s' " % (ins.Name()), "")
        for trd in instr.Trades():
            if trd.Status() in valid_status:
                if _qualifying_trade(trd):
                    if ins_trade_start == 0:
                        ins_trade_start = trd.CreateTime()
                        first_trade = trd

                    elif ins_trade_start > trd.CreateTime():
                        first_trade = trd
                        ins_trade_start = trd.CreateTime()
    return first_trade


def _qualifying_trade(trade):
    if is_demat(trade):
        return True
    if _aquirer_same_as_issuer(trade):
        return True
    if _struct_note_desk_trade(trade):
        return True
    return False


def _aquirer_same_as_issuer(trade):
    """
    This function checks if trade is 'dis' and
    if instrument issuer is the same as trade
    acquirer.
    """
    acquirer = _get_aquirer(trade)
    issuer = _get_instrument_issuer(trade)
    if not is_dis(trade):
        return False
    if not acquirer == issuer:
        return False
    return True


def _struct_note_desk_trade(trade):
    acquirer = _get_aquirer(trade)
    issuer = _get_instrument_issuer(trade)
    if not is_dis(trade):
        return False
    if not acquirer == 'STRUCT NOTES DESK':
        return False
    if not issuer == 'ABSA BANK LTD':
        return False
    return True


def _get_aquirer(trade):
    acquirer = trade.Acquirer()
    if acquirer is None:
        return None
    return acquirer.Name()

def _get_instrument_issuer(trade):
    instrument = trade.Instrument()
    if instrument is None:
        return None
    if instrument.Issuer() is None:
        return None
    return instrument.Issuer().Name()


def cpncalc_choices(object):
    return ['1', '2', '3']


def get_prime_broking_clients(portfolio):
    global PB_MODIFIER
    if PB_MODIFIER is None:
        PB_MODIFIER = PTSPrimeBrokingModifier()
    return PB_MODIFIER.get_cp_from_pb_trade_portfolio(portfolio)


def sor_accounts(object):
    accounts = []
    pty = None

    if object.IsKindOf(acm.FTrade):
        pty = object.Acquirer()
        if pty.Name() == 'PRIME SERVICES DESK':
            if object.Portfolio():
                pty = get_prime_broking_clients(object.Portfolio())
            else:
                LOGGER.error('Trade does not have portfolio to derive SOR account')
                return None

    if object.IsKindOf(acm.FInstrument):
        ins = object
        pty = ins and ins.Issuer() or None

    if pty:
        accounts = [pty.Accounts().At(i).Depository()
                    for i in range(0, pty.Accounts().Size())
                    if not (pty.Accounts().At(i).Depository() is None or pty.Accounts().At(i).Depository() == '')]

    return accounts


def bp_ids(object):
    partc_ids = []
    pty = None
    add_info_name = None

    if object.IsKindOf(acm.FTrade):
        pty = object.Acquirer()
        isDIS = object.Instrument().AdditionalInfo().DIS_Instrument()
        add_info_name = isDIS and 'DIS_Trader_BPID' or 'MM_DEMAT_Trader_BPID'

    if object.IsKindOf(acm.FInstrument):
        ins = object
        isDIS = ins.AdditionalInfo().DIS_Instrument()
        pty = ins and ins.Issuer() or None
        add_info_name = isDIS and 'DIS_Issuer_BPID' or 'MM_DEMAT_Issuer_BPID'

    if pty:
        partc_ids = [pty.Aliases().At(i).Name() for i in range(0, pty.Aliases().Size())
                     if pty.Aliases().At(i).Type().Name() == add_info_name]

    return partc_ids


def cp_bp_ids(object):

    partc_ids = []
    pty = None

    if object.IsKindOf(acm.FTrade):
        pty = object.Counterparty()

    if pty:
        partc_ids = [pty.Aliases().At(i).Name()  for i in range(0, pty.Aliases().Size()) if  pty.Aliases().At(i).Type().Name() == 'MM_DEMAT_Trader_BPID']

    return partc_ids


def mm_ins_types(object):

    mm_ins_types = []

    if object.IsKindOf(acm.FInstrument):
        instype = object.InsType()
        mm_ins_types = instype in INS_TYPES.keys() and INS_TYPES[instype] or []

    return mm_ins_types


def mm_instype(object):
    ins = None
    if object is not None:
        if object.IsKindOf(acm.FTrade):
            ins = object.Instrument()
        if object.IsKindOf(acm.FInstrument):
            ins = object

    instype = ins and ins.InsType() or None
    mminstype = ins and instype in ['CD', 'FRN'] or False

    return mminstype and ins.AdditionalInfo().MM_MMInstype() or instype

