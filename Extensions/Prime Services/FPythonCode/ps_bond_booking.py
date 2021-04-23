
"""-----------------------------------------------------------------------------
MODULE
    ps_bond_booking

DESCRIPTION
    Date                : 2016-02-18
    Purpose             : Simplify bond booking via custom form.
    Department and Desk : Prime Services
    Requester           : Eveshnee Naidoo
    Developer           : Ondrej Bahounek
    CR Number           : 3139848
ENDDESCRIPTION

HISTORY
=============================================================================================
Date       Change no    Developer          Description
---------------------------------------------------------------------------------------------
2016-02-18 3139848      Ondrej Bahounek    Initial implementation
2016-02-25 3465223      Ondrej Bahounek    Add premium. Opposite quantity on custom funds.
2016-04-05 3538867      Ondrej Bahounek    Link trades by contract number.
2016-05-05 3622794      Ondrej Bahounek    Add relative quantities.
                                           Allow valid source trades only.
2016-06-14 3703165      Ondrej Bahounek    Mark only Internal trades as 'PS No Fees'.
2017-08-10 4814265      Ondrej Bahounek    Allow booking both FF/Fin trades for same fund.
------------------------------------------------------------------------------------------"""

import acm, ael
import FUxCore
import FLogger
import decimal

from PS_Functions import (
                          get_pb_fund_counterparty,
                          get_pb_fund_shortname,
                          get_pb_fund_counterparties)

logger = FLogger.FLogger(logToConsole=False, logToPrime=True)

ALIASES = None  # will be populated after a dialog for all funds will be opened

BOOKING_STATUS = "FO Confirmed"
SIMULATED_STATUS = "Simulated"
BOOKING_TEXT1 = "PSBondBooking"

ALLOC_PORTF = acm.FPhysicalPortfolio[3043].Name()  # "Allocate_Pfolio_PrimeServices"
RISK_PORTF = acm.FPhysicalPortfolio[3498].Name()  # "PB_RISK_FV_CLIENTBONDS"
RIDGCAP_PORTF = acm.FPhysicalPortfolio[5842].Name()  # "PB_RISK_FV_INTERMED_RIDGCAP"
KEPLER_PORTF = acm.FPhysicalPortfolio[9527].Name()  # "PB_RISK_FV_INTERMED_KEPLER"
TRADIT_PORTF = acm.FPhysicalPortfolio[9988].Name()  # "PB_RISK_FV_INTERMED_TRADITION"

FO_GROUP = acm.FUserGroup[667].Name()  # "FO PSExchExe Trader" -> "FO_PRIME_BROKER"

INPUT_PORTFS = [ALLOC_PORTF, RISK_PORTF, RIDGCAP_PORTF, KEPLER_PORTF, TRADIT_PORTF]
TARGET_PORTFS = [RISK_PORTF, RIDGCAP_PORTF, KEPLER_PORTF, TRADIT_PORTF]
DISALLOWED_STATUSES = ['Simulated', 'Terminated', 'Void']

# source trade types
EXTERNAL_TYPE = "External"
INTERNAL_TYPE = "Internal"
TRADE_TYPES = [EXTERNAL_TYPE, INTERNAL_TYPE]

GOV_KEY = "Government"
CORP_KEY = "Corporate"
FF_KEY = "FF"
FIN_KEY = "Financed"
MAP110 = {GOV_KEY: {FF_KEY : "PB_FF_MAP110_CR",
                    FIN_KEY : "PB_GOVIBOND1_MAP110_CR"}}
ACUBLUEINK = {GOV_KEY: {FF_KEY : "PB_FF_Acument_BlueInk_FI_CR",
                    FIN_KEY : "PB_REPOBOND_Acumen_BlueInk_FI_CR"}}
MAP250 = {GOV_KEY: {FF_KEY : "PB_FF_MAP_250_FI_CR",
                    FIN_KEY : "PB_REPOBOND_MAP_250_FI_CR"}}

                        
FUNDS_EXTRA_NAMES = {"MAP110" : MAP110,
                    "ACU_BLUEINK":ACUBLUEINK,
                    "MAP250":MAP250}

ALLOWED_TYPES = ["Bond", "FRN", "IndexLinkedBond"]

GOV_BOND_ISSUER = "S A GOVERNMENT DOMESTIC"
RED_COLOR = acm.UX().Colors().Create(255, 55, 45)
GREEN_COLOR = acm.UX().Colors().Create(55, 255, 45)
WHITE_COLOR = acm.UX().Colors().Create(255, 255, 255)
YELLOW_COLOR = acm.UX().Colors().Create(255, 255, 180)

RIDGCAP = '-- Custom - RIDGCAP'  # alias for custom fund
_CUSTOM_CPS = {RIDGCAP : RIDGCAP_PORTF}

COUNTERPARTIES = [
    209,  # ABSA BANK LTD
    35169,  # ACAAM GOVERNMENT BOND FUND
    9527,  # CITIBANK NA SOUTH AFRICA BRANCH
    257,  # CREDIT SUISSE INTERNATIONAL
    264,  # DEUTSCHE BANK AG JHB
    19571,  # ESKOM HOLDINGS SOC LTD
    31620,  # FFO SECURITIES PTY LTD
    10426,  # FIRSTRAND BANK LTD
    455,  # GARBAN SA  PTY LTD
    17781,  # GOLDMAN SACHS INTERNATIONAL UK
    17779,  # HSBC BANK PLC JOHANNESBURG
    34506,  # INVESTEC AM ACSILB
    26147,  # INVESTEC AM ANGFLB
    297,  # INVESTEC BANK LTD
    12652,  # JP MORGAN CHASE BANK JOHANNESBURG
    484,  # LIBERTY GROUP LTD
    429,  # MERRILL LYNCH SA
    319,  # NEDBANK LIMITED
    1947,  # OLD MUTUAL SPECIALISED FINANCE
    30816,  # PERSONAL TRUST IM CO CONSERVATIVE MNG F
    34840,  # PERSONAL TRUST MANAGED FUND CIS
    1351,  # PRESCIENT SECURITIES PTY LTD
    8312,  # PSG FIXED INCOME AND COMMODITIES PTY LT
    30131,  # PUBLIC INVESTMENT CORPORATION SOC LTD
    34703,  # RIDGECAPE CAPITAL PTY LTD
    36127,  # SASFIN SECURITIES PTY LTD
    346,  # SOCIETE GENERALE JOHANNESBURG
    337,  # STANDARD BANK SA
    18005,  # TFS SECURITIES PTY LTD
    356,  # TTSA SECURITIES PTY LTD
    42265,  # TULLETT
    30087,  # VUNANI CAPITAL PTY LTD
    17891,  # WWC TRADING PTY LTD
    34980,  # INVESTEC AM NESBON
]


def run_bond_booking(eii):
    eobj = eii.ExtensionObject()
    if eobj.IsKindOf(acm.FUiTrdMgrFrame):
        try:
            trades = eobj.ActiveSheet().Selection().SelectedCell().RowObject().Trades()
            if trades.Size() != 1:
                raise RuntimeError('Too many trades given: expected 1 trade, got %i' % trades.Size())
            trade = trades[0]
        except Exception, ex:
            raise RuntimeError('Unable to select source trade because of the following error: ' + str(ex))
    else:
        trade = eobj.OriginalTrade()
    if not trade:
        raise RuntimeError("Expecting source trade for the input.")
    validate_trade(trade)
    start_dialog(eobj, trade)


def validate_trade(trade):
    """Check conditions needed to book bonds.
    
    Source trade:
        -- needs to be Bond, FRN, IndexLinkedBond
        -- in any of portfs: Allocation, FV_RISK, RIDGCAP
        -- needs to have valid status
    """
    try:
        if not trade:
            raise RuntimeError("No trade for the input")
        if not trade.Instrument().InsType() in ALLOWED_TYPES:
            raise RuntimeError("Invalid instrument type. Allowed only: %s" %ALLOWED_TYPES)
        if trade.PortfolioId() not in INPUT_PORTFS and trade.Text1() != "PS_ExternalBond":
            raise RuntimeError("Invalid source trade. "
                "Allowed only External trade or from portfolio: %s" %INPUT_PORTFS)
        if trade.Status() in DISALLOWED_STATUSES:
            raise RuntimeError("Invalid source trade's status. These are disallowed: %s" 
                %DISALLOWED_STATUSES)
        if trade.ValueDay() < acm.Time.DateToday():
            raise RuntimeError("You are not allowed to use settled source trade.")
    except Exception as exc:
        trade = trade.Oid() if hasattr(trade, "Oid") else trade
        msg = "Trade '%s' is not valid for Bond booking process due to: %s" \
            %(trade, str(exc))
        logger.ELOG(msg)
        raise RuntimeError("ERROR: " + msg)


def start_dialog(eobj, acm_trade):
    shell = eobj.Shell()
    customDlg = EI_CustomDialog(acm_trade)
    builder = customDlg.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg)


def get_recent_aliases():
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    qor = query.AddOpNode('OR')
    for portf in TARGET_PORTFS:
        qor.AddAttrNode('Portfolio.Name', 'EQUAL', portf)
    #query.AddAttrNode('Text1', 'EQUAL', BOOKING_TEXT1)

    qor = query.AddOpNode('OR')
    for ins_type in ALLOWED_TYPES:
        qor.AddAttrNode('Instrument.InsType', 'EQUAL', ins_type)

    qor = query.AddOpNode('OR')
    for trd_status in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        qor.AddAttrNode('Status', 'EQUAL', trd_status)

    # only recently used counterparties
    query.AddAttrNode('TradeTime', 'GREATER', '-2m')

    trades = query.Select()
    cparties = set(t.Counterparty() for t in trades)
    return sorted(get_pb_fund_shortname(cp) for cp in cparties 
                  if cp.Alias("SoftBroker"))
    
    
def _is_custom_fund(fundname):
    return fundname in _CUSTOM_CPS.keys()
    
    
def _is_gov_bond(bond):
    if type(bond) == str:
        bond = acm.FInstrument[bond]
    return bond.Issuer().Name() == GOV_BOND_ISSUER
    
    
def _get_issuer_type(acm_bond):
    if _is_gov_bond(acm_bond):
        return "Government"
    return "Corporate"
    

def _exists_portf(portf_name):
    return acm.FPhysicalPortfolio[portf_name] is not None
    

def _get_fund_portf(party, is_fully_funded, is_government):
    """ Return portfolio name for party, isFF flag portfolio and issuer of a bond.
    There are 4 possible groups:
        Fin-Corp -- [CORPBOND]
        Fin-Gov -- [REPOBOND, GOVIBOND]
        FF-Corp -- [CORPBOND_FF]
        FF-Gov -- [GOVIBOND_FF, NAKEDBOND_FF, NAKEDBOND]
    
    There should exist only one (or none) portfolio for given input.
    """
    if party in _CUSTOM_CPS.keys():
        if _exists_portf(_CUSTOM_CPS[party]):
            return _CUSTOM_CPS[party]
        raise RuntimeError("Party '{0}' refers to nonexisting portfolio '{1}'".format(
            party, _CUSTOM_CPS[party]))
        
    alias = party
    
    if alias in FUNDS_EXTRA_NAMES.keys():
        iss_type_key = GOV_KEY if is_government else CORP_KEY
        strategy_key = FF_KEY if is_fully_funded else FIN_KEY
        try:
            portf = FUNDS_EXTRA_NAMES[alias][iss_type_key][strategy_key]
        except Exception:
            raise RuntimeError('Nonexisting portfolio (alias:{0}, FF:{1}, isGOV:{2})'
                .format(alias, is_fully_funded, is_government))
        return portf
        
    ff = 'FF_' if is_fully_funded else ''
    govi_ff_names = ['GOVIBOND_FF', 'NAKEDBOND_FF', 'NAKEDBOND']
    govi_fin_names = ['GOVIBOND', 'REPOBOND']
    portfs_result = []
    if not is_government:
        portf_name = 'PB_CORPBOND_' + ff + alias + '_CR'
        if _exists_portf(portf_name):
            portfs_result.append(portf_name)
    else:
        if is_fully_funded:
            for bond_type in govi_ff_names:
                portf_name = 'PB_' + bond_type + '_' + alias + '_CR'
                if _exists_portf(portf_name):
                    portfs_result.append(portf_name)
        else:
            for bond_type in govi_fin_names:
                portf_name = 'PB_' + bond_type + '_' + alias + '_CR'
                if _exists_portf(portf_name):
                    portfs_result.append(portf_name)
    
    if not portfs_result:
        raise RuntimeError('Nonexisting portfolio (alias:{0}, FF:{1}, isGOV:{2})'
            .format(alias, is_fully_funded, is_government))
    if  len(portfs_result) > 1:
        raise RuntimeError('Too many candidate portfolios (alias:{0}, FF:{1}, isGOV:{2}): {3}'
            .format(alias, is_fully_funded, is_government, ','.join(portfs_result)))
    return portfs_result[0]


def book_mirror_trades(trade, alloc, is_gov):
    
    trades = []
    risk_portf = acm.FPhysicalPortfolio[RISK_PORTF]
    
    chl_no_fees = acm.FChoiceList.Select01('list="TradeKey3" and name="PS No Fees"', '')
    
    logger.LOG("Source trade: {0}".format(trade.Oid()))
    
    ins = trade.Instrument()
    t1_ins_name = ins.Name() if is_gov else ins.Name() + '/MTM'
    t1_ins = acm.FInstrument[t1_ins_name]
    if not t1_ins:
        msg = "Nonexisting instrument '{0}'. Please, contact TCU.".format(t1_ins_name)
        logger.ELOG(msg)
        raise RuntimeError(msg)
    
    for trd in alloc.get_trades():
        
        party = get_pb_fund_counterparty(trd.fund()) 
        client_portf = acm.FPhysicalPortfolio[trd.portfolio()]
        
        # ========================
        # trade 1 (CR trade or target portfolio trade):
        # instrument: 
        #    if instr type is Corporate: orig_instr + '/MTM'
        #    if instr type is Government: orig_instr
        # quantity sign: same for CR trade, opposite for custom funds
        # premium sign: same for CR trade, opposite for custom funds
        # cpty: if CR trade: ABSA BANK LTD
        #       else: cpty from form
        # portf: fund's target portfolio (CR portf)
        # acquirer: PRIME SERVICES DESK
        # OptKey3: PS No Fees - only for _CR portfolio trades
        # price: if custom fund: from form
        #        else (normal fund): source trade's price
        
        quantity = float(trd.quantity())
        quantity = -quantity if isinstance(trd, CustomTrade) else quantity
        logger.LOG("Booking trade (Qty: {0}) into '{1}'".format(
            quantity, client_portf.Name()))
            
        t1 = acm.FTrade()
        t1.Instrument(t1_ins)
        t1.Currency(t1_ins.Currency())
        t1.Portfolio(client_portf)
        t1.Counterparty(trd.counterparty())
        t1.Acquirer(acm.FParty['PRIME SERVICES DESK'])
        t1.Price(trd.price())
        t1.Quantity(quantity)
        t1.TradeTime(trade.TradeTime())
        t1.ValueDay(trade.ValueDay())
        t1.AcquireDay(trade.AcquireDay())
        t1.Trader(acm.User())
        t1.Status("Simulated")
        t1.Contract(trade)
        t1.Text1(BOOKING_TEXT1)
        t1.PremiumCalculationMethod('Consideration')
        
        # Client's CR trade should be marked as "PS No Fees"
        # when the source trade is booked by internal desk.
        # Trades booked from external source trade should NOT have "PS No Fees"
        if client_portf.Name().endswith("_CR"):
            if alloc.is_ps_no_fees():
                t1.OptKey3(chl_no_fees)
            if t1.Counterparty().Name() != "ABSA BANK LTD":
                logger.WLOG("CR trade doesn't have 'ABSA BANK LTD' counterparty!")
            
        t1.Commit()
        trades.append(t1)
    
        if isinstance(trd, CustomTrade):
            logger.LOG("Custom fund trade booked - booking of a mirror trade " \
                "into RISK portfolio skipped")
            continue
        
        
        # ========================
        # trade 2 - mirror trade (only for standard fund):
        # instrument: orig_instr
        # quantity: opposite to CR
        # premium: opposite to CR
        # cpty: fund party
        # portf: risk portf PB_RISK_FV_CLIENTBONDS
        # acquirer: PRIME SERVICES DESK
        
        # create trade2 - mirror RISK portf
        logger.LOG("Booking mirror trade (Qty: {0}) into '{1}'".format(
            -t1.Quantity(), risk_portf.Name()))
            
        t2 = acm.FTrade()        
        t2.Instrument(ins)
        t2.Currency(ins.Currency())
        t2.Portfolio(risk_portf)        
        t2.Counterparty(party)
        t2.Acquirer(acm.FParty['PRIME SERVICES DESK'])        
        t2.Price(trd.price())
        t2.Quantity(-t1.Quantity())
        t2.TradeTime(trade.TradeTime())
        t2.ValueDay(trade.ValueDay())
        t2.AcquireDay(trade.AcquireDay())
        t2.Trader(acm.User())
        t2.Status("Simulated")
        t2.Contract(trade)
        t2.Text1(BOOKING_TEXT1)
        t2.PremiumCalculationMethod('Consideration')
        t2.RegisterInStorage()
        
        # PB trades fed into Nutron must have Prime_Broker flag set from 2016-06-20
        if acm.FAdditionalInfoSpec.Select01('name="Prime_Broker"', ''):
            t2.AdditionalInfo().Prime_Broker('Yes')
        t2.Commit()
        trades.append(t2)
    return trades


def move_trade(trade, portf):
    """ Move source trade into portfolio. """
    if trade.PortfolioId() == portf.Name():
        return
    trade.Portfolio(portf)
    trade.Commit()
    logger.LOG("Source trade '{0}' was moved into risk portf '{1}'".format(
        trade.Oid(), portf.Name()))


def _set_premiums(trades):
    acm.BeginTransaction()
    try:
        for trd in trades:
            ael_trade = ael.Trade[trd.Oid()]
            premium = ael_trade.premium_from_quote(ael.date(trd.ValueDay()), trd.Price())
            trd.Premium(premium)
            trd.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        raise
        
def _set_final_status(trades, status):
    acm.BeginTransaction()
    try:
        for trd in trades:
            trd.Status(status)
            trd.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        raise
    

def perform_booking(trade, alloc, is_gov, target_portf_name, trd_status):
    """ Main booking procedure.
    
    Move source trade into risk portfolio.
    Book CR trades and mirror trades.
    """
    acm.BeginTransaction()
    try:
        move_trade(trade, acm.FPhysicalPortfolio[target_portf_name])
        trades = book_mirror_trades(trade, alloc, is_gov)
        acm.CommitTransaction()
        logger.LOG("Trades created: {0}".format(map(str, [t.Oid() for t in trades])))
    except Exception as exc:
        acm.AbortTransaction()
        logger.ELOG("Error while booking: {0}".format(str(exc)))
        raise
    logger.LOG("Setting premiums...")
    _set_premiums(trades)
    logger.LOG("Setting final status...")
    _set_final_status(trades, trd_status)
    logger.LOG("==== Booking completed successfully.")

    
def _get_source_trade_type(trade):
    """ Get type of the group which booked the trade. """
    if trade.CreateUser().UserGroup().Name() == FO_GROUP:
        return EXTERNAL_TYPE
    return INTERNAL_TYPE

    
def _is_ps_no_fees(trade):
    """ Find out whether trades should be marked as 'PS No Fees'.
    
    If source trade is of EXTERNAL type (was booked by anyone 
    from "FO PSExchExe Trader" group), then 'PS No Fees' should be False.
    Otherwise True.
    """
    return _get_source_trade_type(trade) == INTERNAL_TYPE
    

class EI_CustomDialog(FUxCore.LayoutDialog):
    
    def __init__(self, acm_trade):
        self.source_trade = acm_trade
        
    def _set_colors(self, color):
        self.m_fuxDlg.SetBackgroundColor(color)
        self.vertbox1.SetColor(0, color)
        self.vertbox1.SetColor(1, color)
        
        self.vertbox2.SetColor(0, color)
        self.vertbox2.SetColor(1, color)
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Prime Services - Bond Booking')
        
        self.m_list = layout.GetControl('list_trades')
        
        self.vertbox1 = layout.GetControl('vertbox1')
        self.vertbox2 = layout.GetControl('vertbox2')
        
        # buttons
        self.btnLoadTrade = layout.GetControl('btn_load_trade')
        self.btnAddTrade = layout.GetControl('btn_add_trade')
        self.btnUpdateTrade = layout.GetControl('btn_update_trade')
        self.btnDelTrade = layout.GetControl('btn_delete_trade')
        self.btnBook = layout.GetControl('btn_book')
        self.btnClose = layout.GetControl('btn_close')
        self.btnAddCpty = layout.GetControl('btn_add_cpty')
        self.btnAddRest = layout.GetControl('btn_add_rest')
        self.btnAddFund = layout.GetControl('btn_add_fund')
        
        # inputs
        self.inptTradeOid = layout.GetControl('inpt_trade_source_alloc')
        self.inptTradeQty = layout.GetControl('inpt_trade_qty')
        self.inptQuantityOrig = layout.GetControl('inpt_quantity_orig')
        self.inptQuantityRem = layout.GetControl('inpt_quantity_remain')
        self.inptQuantityRemPct = layout.GetControl('inpt_quantity_remain_pct')
        self.inptPortfOrig = layout.GetControl('inpt_portfolio_orig')
        self.inptRelship = layout.GetControl('inpt_relationship')
        self.inptPrice = layout.GetControl('inpt_price')
        self.inptInstr = layout.GetControl('inpt_instr')
        self.inptTradeType = layout.GetControl('inpt_trade_type')
        
        # option boxes
        self.optIssuerType = layout.GetControl('opt_issuer_type')
        self.optTargetPortf = layout.GetControl('opt_target_portf')
        self.optFund = layout.GetControl('opt_fund')
        self.optCpty = layout.GetControl('opt_cpty')
        
        #check boxes
        self.chbFF = layout.GetControl('chb_ff')
        self.chbNoFees = layout.GetControl('chb_no_fees')
        self.chb_simulated = layout.GetControl('chb_simulated')
        
        
        # ========================
        # setting controls
        self.inptQuantityOrig.Editable(False)
        self.inptQuantityRem.Editable(False)
        self.inptQuantityRemPct.Editable(False)
        self.inptPortfOrig.Editable(False)
        self.inptRelship.Editable(False)
        self.inptInstr.Editable(False)
        self.inptTradeType.Editable(False)
        
        self.optTargetPortf.Enabled(True)
        
        self.m_list.ShowGridLines()
        self.m_list.ShowColumnHeaders()
        self.m_list.AddColumn("Fund", -1, "Fund name")
        self.m_list.AddColumn("Quantity", -1, "Quantity of a new trade")
        self.m_list.AddColumn("Fully Funded", -1, "Is fully funded trade?")
        self.m_list.AddColumn("Price", -1, 
            "Price (applicable only for custom funds; " + \
            "otherwise: source price used)")
        self.m_list.AddColumn("Counterparty", -1, "CR trades' Cpty " + \
            "(applicable for custom funds; " + \
            "otherwise: 'ABSA CAPIPAL LTD')")
        self.m_list.AddColumn("Portfolio", -1, "Portfolio of a new trade")
        
        self.m_list.AdjustColumnWidthToFitItems(0)
        self.m_list.AdjustColumnWidthToFitItems(1)
        self.m_list.AdjustColumnWidthToFitItems(2)
        self.m_list.AdjustColumnWidthToFitItems(3)
        self.m_list.AdjustColumnWidthToFitItems(4)
        self.m_list.AdjustColumnWidthToFitItems(5)
        
        
        cp_aliases = get_recent_aliases()
        names = _CUSTOM_CPS.keys() + cp_aliases
        for cp_name  in names:
            self.optFund.AddItem(cp_name)
            
        for cp_name in sorted(acm.FParty[poid].Name() for poid in COUNTERPARTIES):
            self.optCpty.AddItem(cp_name)
        
        for portf in TARGET_PORTFS:
            self.optTargetPortf.AddItem(portf)
        
        self.optIssuerType.AddItem('Government')
        self.optIssuerType.AddItem('Corporate')
        
        
        # callbacks
        self.m_list.AddCallback("SelectionChanged", self.OnListSelectionChanged, None)
        self.btnLoadTrade.AddCallback("Activate", self.OnLoadTradeButtonPressed, None)
        self.btnAddTrade.AddCallback("Activate", self.OnAddTradeButtonPressed, None)
        self.btnUpdateTrade.AddCallback("Activate", self.OnUpdateTradeButtonPressed, None)
        self.btnDelTrade.AddCallback("Activate", self.OnDelTradeButtonPressed, None)
        self.btnBook.AddCallback("Activate", self.OnBookButtonPressed, None)
        self.btnClose.AddCallback("Activate", self.OnCloseButtonPressed, None)
        self.btnAddCpty.AddCallback("Activate", self.OnAddCptyButtonPressed, None)
        self.optFund.AddCallback("Changing", self.OnOptFundSelectionChanged, None)
        self.btnAddRest.AddCallback("Activate", self.OnAddRestPressed, None)
        self.chbNoFees.AddCallback("Activate", self.OnChbNoFeesChecked, None)
        self.btnAddFund.AddCallback("Activate", self.OnAddFundButtonPressed, self.optFund)
        self.chb_simulated.AddCallback("Activate", self.OnChbSimulatedChecked, None)

        self.SetFromTrade(self.source_trade)
        
    def SetFromTrade(self, source_trade):
        try:
            validate_trade(source_trade)
            self.source_trade = source_trade
        except Exception as ex:
            self.ShowError(str(ex))
            raise
        finally:
            self.SetDefaults()
            self.PopulateData()
        self._validate_existing_split_trades(msg_type="warning")
        
    def SetDefaults(self):
        logger.LOG("Booking process -- setting initial form.")
        logger.LOG("Source trade: {0}, Portfolio: {1}, Issuer type: {2}".format(
            self.source_trade.Oid(), self.source_trade.PortfolioId(), 
            _get_issuer_type(self.source_trade.Instrument())))
        self.m_list.RemoveAllItems()
        
        self.allocation = Allocation(decimal.Decimal(str(self.source_trade.Quantity())),
            _is_ps_no_fees(self.source_trade))
        
        self.trd_status = BOOKING_STATUS
        self.chb_simulated.Checked(False)
        self._set_colors(WHITE_COLOR)
        
        self.inptTradeQty.SetData('')
        self.optIssuerType.SetData(_get_issuer_type(self.source_trade.Instrument()))
        self.inptQuantityRem.SetColor("BackgroundReadonly", RED_COLOR)
        self.inptQuantityRemPct.SetColor("BackgroundReadonly", RED_COLOR)
        
        self.optTargetPortf.SetData(RISK_PORTF)
        if self.source_trade.PortfolioId() in TARGET_PORTFS:
            self.optTargetPortf.SetData(self.source_trade.PortfolioId())
        
        self.btnAddTrade.Enabled(False)
        self.btnUpdateTrade.Enabled(False)
        self.btnDelTrade.Enabled(False)
        self.btnBook.Enabled(False)
        
    def PopulateData(self):
        if not self.source_trade:
            return
        
        self.m_list.RemoveAllItems()
        root_item = self.m_list.GetRootItem()
        for trd in sorted(self.allocation.get_trades()):
            child = root_item.AddChild()
            child.Label(trd.fund(), 0)
            child.Label(str(trd.quantity()), 1)
            child.Label(trd.fully_funded(), 2)
            child.Label(trd.price(), 3)
            child.Label(trd.counterparty(), 4)
            child.Label(trd.portfolio(), 5)
            child.SetData(trd)
        
        for i in range(6):
            self.m_list.AdjustColumnWidthToFitItems(i)
        
        if root_item.ChildrenCount() > 0:
            self.optIssuerType.Enabled(False)
        else:
            self.optIssuerType.Enabled(True)
        
        self.inptTradeOid.SetData(self.source_trade.Oid())
        self.inptQuantityOrig.SetData(self.source_trade.Quantity())
        self.inptQuantityRem.SetData(self.source_trade.Quantity())
        self.inptPortfOrig.SetData(self.source_trade.PortfolioId())
        if self.source_trade.AdditionalInfo().Relationship_Party():
            self.inptRelship.SetData(self.source_trade.AdditionalInfo().Relationship_Party().Name())
            
        self.inptInstr.SetData(self.source_trade.Instrument().Name())
        
        # external/internal source trade type
        # if trade is external type, uncheck PS No Fees
        self.inptTradeType.SetData(_get_source_trade_type(self.source_trade))
        self.chbNoFees.Checked(self.allocation.is_ps_no_fees())
        
        rem_qty = self.allocation.get_remaining_qty()
        self.inptQuantityRem.SetData(str(rem_qty))
        rem_qty_pct = rem_qty / self.allocation.max_quantity * 100
        rem_qty_pct = round(rem_qty_pct, 2)
        self.inptQuantityRemPct.SetData(str(rem_qty_pct) + "%")
        
        if rem_qty != 0:
            self.inptQuantityRem.SetColor("BackgroundReadonly", RED_COLOR)
            self.inptQuantityRemPct.SetColor("BackgroundReadonly", RED_COLOR)
            self.btnBook.Enabled(False)
        else:
            self.inptQuantityRem.SetColor("BackgroundReadonly", GREEN_COLOR)
            self.inptQuantityRemPct.SetColor("BackgroundReadonly", GREEN_COLOR)
            self.btnBook.Enabled(True)

        self._list_item_selected()        
    
    def _get_issuer_type(self):
        return self.optIssuerType.GetData()
        
    def _is_gov_bond(self):
        return self._get_issuer_type() == 'Government'

    def _get_inpt_quantity(self):
        orig_qty = self.inptTradeQty.GetData().strip()
        if not len(orig_qty) > 0:
            self.ShowError("Missing quantity")
            return None
        is_percent = False
        qty = orig_qty
        if orig_qty[-1] == "%":
            qty = orig_qty[:-1]
            is_percent = True
        try:
            qty = decimal.Decimal(str(qty))
            if qty == 0:
                raise RuntimeError("Zero quantity is not allowed")
            if is_percent:
                qty = qty * self.allocation.max_quantity / 100
        except Exception as exc:
            logger.ELOG(str(exc))
            self.ShowError("Invalid input quantity: %s" %orig_qty)
            return None
        return qty
        
    def _list_item_selected(self):
        selected_item = self.m_list.GetSelectedItem()
        if not selected_item:
            self.optFund.SetData('')
            self.optCpty.SetData('')
            self.inptTradeQty.SetData('')
            self.inptPrice.SetData(str(self.source_trade.Price()))
            self.inptPrice.Enabled(False)
            self.btnAddTrade.Enabled(True)
            self.btnUpdateTrade.Enabled(False)
            self.btnDelTrade.Enabled(False)
            self.chbFF.Enabled(True)
            self.chbFF.Checked(False)
            self.optFund.Enabled(True)
            self.optCpty.Enabled(True)
            return
        
        trade = selected_item.GetData()
        self.inptPrice.SetData(trade.price())
        self.inptTradeQty.SetData(str(trade.quantity()))
        self.optFund.SetData(trade.fund())
        self.optCpty.SetData(trade.counterparty())
        self.chbFF.Checked(trade.fully_funded())
        self.btnAddTrade.Enabled(False)
        self.btnUpdateTrade.Enabled(True)
        self.btnDelTrade.Enabled(True)
        self.optFund.Enabled(False)       
        if isinstance(trade, CustomTrade):
            self.inptPrice.Enabled(True)
            self.chbFF.Enabled(False)
            self.optCpty.Enabled(True)
            self.btnAddCpty.Enabled(True)
        else:
            self.inptPrice.Enabled(False)
            self.chbFF.Enabled(True)
            self.optCpty.Enabled(False)
            self.btnAddCpty.Enabled(False)

    def ShowInformation(self, msg):
        """ Show message in information dialog. """
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)
        
    def ShowError(self, msg):
        """ Show error message box."""
        acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', "Error: " + msg,
            'Cancel', None, None, 'Button1', 'Button1')
        
    def _check_price(self, price):
        try:
            p = float(price)
            if p < 0.0 or p > 100000000:  # current max price: 40712950.0
                raise RuntimeError("Invalid price")
        except Exception, exc:
            raise RuntimeError("Invalid price")
        return p
        
    def OnChbNoFeesChecked(self, cd, data):
        """ Checkbox for PS No Fees was changed."""
        self.allocation.set_ps_no_fees(self.chbNoFees.Checked())
        
    def OnChbSimulatedChecked(self, cd, data):
        if self.chb_simulated.Checked():
            self._set_colors(YELLOW_COLOR)
            self.trd_status = SIMULATED_STATUS
        else:
            self._set_colors(WHITE_COLOR)
            self.trd_status = BOOKING_STATUS
        
    def OnLoadTradeButtonPressed(self, cd, data):
        """ Load new source trade into the form.
        
        Discard all previous changes.
        """        
        trade = self.inptTradeOid.GetData().strip()
        if len(trade) == 0:
            return
        trade = acm.FTrade[trade]
        self.SetFromTrade(trade)
    
    def OnAddFundButtonPressed(self, cd, data):
        """Display all PB funds' aliases.
           Add fund alias to the option box.
        """
        
        global ALIASES
        if not ALIASES:
            ALIASES = sorted(get_pb_fund_shortname(cparty) for cparty 
                in get_pb_fund_counterparties())
        alias = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Fund',
                                                'Counterparties',
                                                ALIASES,
                                                None)
        if not alias:
            return

        if not cd.ItemExists(alias):
            cd.AddItem(alias)

        cd.SetData(alias)
        self._fund_seletction_changed()
        
    def OnAddTradeButtonPressed(self, cd, data):
        """ Add trade to the list."""
        qty = self._get_inpt_quantity()
        if not qty:
            return
        fund = self.optFund.GetData()
        is_custom = _is_custom_fund(fund)
        if not fund:
            self.ShowError("Invalid fund: '%s'" %fund)
            return
        ff = self.chbFF.Checked()
        cpty = self.optCpty.GetData()
        if not cpty:
            self.ShowError("Missing counterparty")
            return
        try:
            price = self._check_price(self.inptPrice.GetData())
            portf = _get_fund_portf(fund, ff, self._is_gov_bond())
            if is_custom:
                trade = CustomTrade(fund, qty, ff, portf, cpty, price)
            else:
                trade = TradeData(fund, qty, ff, portf, cpty, price)
            self.allocation.add_trade(trade)
        except Exception as exc:
            self.ShowError(str(exc))
            raise
        self.PopulateData()
            
    def OnUpdateTradeButtonPressed(self, cd, data):
        """ Update selected trade in the list."""
        qty = self._get_inpt_quantity()
        if not qty:
            return
        trd_selected = self.m_list.GetSelectedItem().GetData()
        fund = trd_selected.fund()
        is_custom = _is_custom_fund(fund)
        ff = self.chbFF.Checked()
        cpty = self.optCpty.GetData()
        if not cpty:
            self.ShowError("Missing counterparty")
            return
        
        try:
            price = self._check_price(self.inptPrice.GetData())
            portf = _get_fund_portf(fund, ff, self._is_gov_bond())
            if is_custom:
                trade = CustomTrade(fund, qty, ff, portf, cpty, price)
                if cpty != trd_selected.counterparty():
                    self.allocation.remove_trade(trd_selected)
                    self.allocation.add_trade(trade)
            else:
                trade = TradeData(fund, qty, ff, portf, cpty, price)
            self.allocation.update_trade(trd_selected, trade)
        except Exception as exc:
            self.ShowError(str(exc))
            raise
        self.PopulateData()
    
    def OnDelTradeButtonPressed(self, cd, data):
        """ Delete trade from list view."""
        trd_selected = self.m_list.GetSelectedItem().GetData()
        try:
            self.allocation.remove_trade(trd_selected)
        except Exception as exc:
            self.ShowError(str(exc))
            raise
        self.PopulateData()
        
    def OnAddRestPressed(self, cd, data):
        """Insert remaining quantity into quantity input field."""
        rem_qty = self.allocation.get_remaining_qty()
        trd_selected = self.m_list.GetSelectedItem()
        if trd_selected:
            rem_qty += trd_selected.GetData().quantity()
        self.inptTradeQty.SetData(str(rem_qty))        
        
    def OnAddCptyButtonPressed(self, cd, data):
        """ Show dialog with all counterparties
            Add counterparty to the counterparty option box.
        """
        parties = acm.FCounterParty.Select('').AsSet()
        parties.Union(acm.FClient.Select(''))
        cpty = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Counterparty',
                                                'Counterparties',
                                                parties,
                                                None)
        if not cpty:
            return            
        if not self.optCpty.ItemExists(cpty.Name()):
            self.optCpty.AddItem(cpty.Name())
        self.optCpty.SetData(cpty.Name())
            
    def OnOptFundSelectionChanged(self, cd, data):
        self._fund_seletction_changed()
            
    def _fund_seletction_changed(self):
        fund = self.optFund.GetData()
        if not fund:
            return
        is_custom = _is_custom_fund(fund)
        if is_custom:
            self.inptPrice.Enabled(True)
            self.chbFF.Enabled(False)
            self.optCpty.Enabled(True)
            self.optCpty.SetData('')
            self.btnAddCpty.Enabled(True)
        else:
            self.inptPrice.Enabled(False)
            self.chbFF.Enabled(True)
            self.optCpty.Enabled(False)
            self.optCpty.SetData('ABSA BANK LTD')
            self.btnAddCpty.Enabled(False)
    
    def _find_existing_split_trades(self):
        """Find out if any split trades point to source trade.
        
        Every split trade is connected with the source trade via Contract.
        """
        trade = self.source_trade
        _contracts = acm.FTrade.Select('oid <> %d and contractTrdnbr= %d' %(trade.Oid(), trade.Oid()))
        contracts = [t.Oid() for t in _contracts if t.Status() not in ["Simulated", "Void", "Terminanted"]]
        return contracts
        
    def _validate_existing_split_trades(self, msg_type="error"):
        """Check if source trade was already used for bond booking.
        
        Arguments:
            -- msg_type 
                = "error" - display Yes/No dialog and raise an exception if "No" was selected
                = "warning" or anything else - display just warning dialog
        """
        contracts = self._find_existing_split_trades()
        if contracts:
            print("Existing split trades:", contracts)
            if msg_type=="error":
                msg = ("This source trade was already used for bond booking" +
                    "\n(existing trades can be found in the Log)." +
                    "\n\nDo you want to book new trades anyway?")
                ret_val = acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), "Question", msg,
                    "Yes", "No", None, "Button1", "Button2")
                if ret_val == "Button2":
                    raise RuntimeError("Aborted by the user.")
            else:
                msg = ("This source trade was already used for bond booking" +
                    "\n(existing trades can be found in the Log).")
                self.ShowInformation(msg)
                
    def OnBookButtonPressed(self, cd, data):
        """Book split trades."""
        logger.LOG("==== Booking started.")
        try:
            self._validate_existing_split_trades()
            perform_booking(self.source_trade, self.allocation, 
                self._is_gov_bond(), self.optTargetPortf.GetData(),
                self.trd_status)
            self.ShowInformation("Booking process completed. View log for trade numbers.")
        except Exception as exc:
            self.ShowError("Booking failed: %s" %str(exc))
            raise
    
    def OnCloseButtonPressed(self, cd, data):
        """ Close main dialog. """
        self.m_fuxDlg.CloseDialogOK()
    
    def OnListSelectionChanged(self, cd, data):
        self._list_item_selected()
    
    def OnQuantityChanged(self, cd, data):
        if len(self.inptTradeQty.GetData()) > 0:
            self.btnAddTrade.Enabled(True)
        else:
            self.btnAddTrade.Enabled(False)
            
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Source trade', 'vertbox1')
        b.    BeginHorzBox('None')
        b.      AddInput('inpt_trade_source_alloc', 'Source trade:', 15, 15)
        b.      AddFill()
        b.      AddButton('btn_load_trade', 'Load / Reset')
        b.    EndBox()
        b.    BeginVertBox('None')
        b.      AddInput('inpt_quantity_orig', 'Quantity:', 15, 15)
        b.      BeginHorzBox('None')
        b.        AddInput('inpt_trade_type', 'Trade Type:', 15, 15)
        b.        AddCheckbox('chb_no_fees', 'PS No Fees?')
        b.      EndBox()
        b.      AddInput('inpt_portfolio_orig', 'Portfolio:', 40, 40)
        b.      AddOption('opt_target_portf', 'Target Portfolio:', 40, 40)
        b.      AddInput('inpt_relationship', 'Relationship:', 40, 40)
        b.      AddOption('opt_issuer_type', 'Issuer Type:', 40, 40)
        b.      AddInput('inpt_instr', 'Instrument:', 40, 40)
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(10)
        b.  BeginVertBox('EtchedIn', 'New trades', 'vertbox2')
        b.    BeginHorzBox('None')
        b.      AddInput('inpt_quantity_remain', 'Remaining quantity:', 15, 15)
        b.      AddSpace(30)
        b.      AddInput('inpt_quantity_remain_pct', 'Remaining in pct (%):', 15, 15)
        b.    EndBox()
        b.    AddList('list_trades', 10, -1, 120, -1)
        b.    BeginVertBox('None')
        b.      BeginHorzBox('None')
        b.        AddOption('opt_fund', 'Fund:', 50, 50)
        b.        AddButton('btn_add_fund', 'Add Fund...')
        b.      EndBox()
        b.      BeginHorzBox('None')
        b.        AddInput('inpt_trade_qty', 'Quantity or %:', 15, 15)
        b.        AddButton('btn_add_rest', 'Add Residual')
        b.      EndBox()
        b.      BeginHorzBox('None')
        b.        AddOption('opt_cpty', 'Counterparty:', 50, 50)
        b.        AddButton('btn_add_cpty', 'Add...')
        b.      EndBox()
        b.      AddCheckbox('chb_ff', "Fully Funded")
        b.      AddInput('inpt_price', 'Price:', 15, 15)
        b.    EndBox()
        b.    AddSpace(10)
        b.    BeginHorzBox('None')
        b.      AddButton('btn_add_trade', 'Add')
        b.      AddSpace(10)
        b.      AddButton('btn_update_trade', 'Update')
        b.      AddSpace(10)
        b.      AddButton('btn_delete_trade', 'Delete')
        b.    EndBox()
        b.  EndBox()        
        b.  AddSpace(10)
        b.  BeginHorzBox('None')
        b.    AddButton('btn_book', 'Book')
        b.    AddSpace(10)
        b.    AddCheckbox('chb_simulated', 'Simulated?')
        b.    AddFill()
        b.    AddButton('btn_close', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
        
    
class TradeData(object):
    """ Standard fund trade.
    
    Maximally 1 trade can be booked for each fund.
    FundID is the unique key.
    """
    def __init__(self, fund, quantity, ff, portf, cpty, price):
        self.fund_id = fund
        self.data = {'qty': quantity, 'ff':ff, 
            'portf':portf, 'cpty':cpty, 'price':price}
    
    def __lt__(self, other):
        return str(self) < str(other)
        
    def __str__(self):
        return self.fund_id + str(self.data['ff'])
        
    def quantity(self):
        return self.data['qty']
        
    def fund(self):
        return self.fund_id
    
    def fully_funded(self):
        return self.data['ff']
        
    def portfolio(self):
        return self.data['portf']
        
    def counterparty(self):
        return self.data['cpty']
        
    def price(self):
        return self.data['price']


class CustomTrade(TradeData):
    """ Represents custom fund's trade.
    
    More than 1 custom trade can be booked for custom fund.
    These trades must differ in counterparty.
    FundId + Counterparty is the trade key.
    """
    def __str__(self):
        return self.fund_id + str(self.data['ff']) + ":" + self.counterparty()


class Allocation(object):
    """ Container for all trades.
    
    Custom funds can have more trades that must differ in counterparty.
    Sum of all trades' quantity must be less or equal than original quantity.
    """
    def __init__(self, max_quantity, is_ps_no_fees):
        self.max_quantity = max_quantity
        self._is_ps_no_fees = is_ps_no_fees
        self.trades = {}
    
    def is_ps_no_fees(self):
        return self._is_ps_no_fees
        
    def set_ps_no_fees(self, true_false):
        self._is_ps_no_fees = true_false

    def get_current_qty(self):
        return sum(t.quantity() for t in self.trades.values())
    
    def get_remaining_qty(self):
        return self.max_quantity - self.get_current_qty()
    
    def _is_same_sign(self, num):
        return (num * self.max_quantity) > 0
    
    def _is_in_limit(self, quantity, old_quantity):
        return abs(quantity + self.get_current_qty() - old_quantity) <= abs(self.max_quantity)
    
    def _all_trades_same_type(self, new_trade):
        for trd in self.trades.values():
            if type(trd) != type(new_trade):
                return False
        return True
    
    def check_trades_same_type(self, new_trade):
        """ Only trades with same type are allowed to store."""
        if not self._all_trades_same_type(new_trade):
            raise RuntimeError("Mixing normal and custom funds not allowed.")
    
    def check_quantity(self, quantity, old_quantity=0):
        if quantity == 0:
            raise RuntimeError("Quantity '0' is not allowed")
        if not self._is_same_sign(quantity):
            raise RuntimeError("Quantity '%s' has wrong sign" %quantity)
        if not self._is_in_limit(quantity, old_quantity):
            raise RuntimeError("Sum of quantities is above the limit '%s'" 
                %self.max_quantity)
    
    def add_trade(self, trade):
        if self.trades.get(str(trade)):
            raise RuntimeError("Trade with fund '{0}' already exists. Use Update instead." 
                .format(str(trade)))
        self.check_quantity(trade.quantity())
        self.check_trades_same_type(trade)
        self.trades[str(trade)] = trade
    
    def update_trade(self, orig_trade, trade):
        old_trade = self.trades.get(str(trade))
        if not old_trade:
            raise RuntimeError("Can't update nonexisting trade. Use Add instead.")
        if id(old_trade) != id(orig_trade):
            raise RuntimeError("Update collision: New state already exists on another existing trade.")
        self.check_quantity(trade.quantity(), old_trade.quantity())
        self.trades[str(trade)] = trade
    
    def remove_trade(self, trade):
        if self.trades.get(str(trade)):
            self.trades.pop(str(trade))
    
    def get_trades(self):
        return self.trades.values()


