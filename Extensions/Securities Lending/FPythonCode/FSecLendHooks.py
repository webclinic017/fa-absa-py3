""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendHooks.py"
from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendHooks

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Hooks for customising the behaviour of the Securities Lending workbenches and workflows.

------------------------------------------------------------------------------------------------"""
import collections
import acm
import ael
import FParameterSettings
import FSecLendUtils
from GenerateOrderReportAPI import GenerateOrderReport
from FSalesNotesUx import CreateFSalesNotesUxInstance
from datetime import datetime

# Many settings may be changed by simply customising the SecLendSettings FParameter in
# Extension Editor, rather than overriding the associated Python function below.


_SETTINGS = FParameterSettings.ParameterSettingsCreator.FromRootParameter('SecLendSettings')

try:
    import FSecLendCustomHooks
except StandardError:
    FSecLendCustomHooks = None

def GetCustomHook(ObjName):
    if FSecLendCustomHooks is not None:
        if hasattr(FSecLendCustomHooks, ObjName):
            return getattr(FSecLendCustomHooks, ObjName)


# ----------------------------------------------------------------------------------------------
#  Default / Common parameters
def MasterSecurityLoansQuery():
    """Return a query containing trades pertaining to active loans for the passed
    parameters, if provided.
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNodeEnum('Instrument.InsType', 'SecurityLoan')
    query.AddAttrNode('Instrument.ProductTypeChlItem.Name', 'EQUAL', 'Master Security Loan')
    query.AddAttrNode('Instrument.OpenEnd', 'NOT_EQUAL', 'Terminated')
    return query


def DefaultAcquirer():
    """The default acquirer to use for newly created security loan trades."""
    hook = GetCustomHook("DefaultAcquirer")
    if hook is not None:
        return hook()
    return acm.FParty[_SETTINGS.Acquirer()]


def DefaultMarket():
    """The default Internal Market for all order / RFQ activities."""

    hook = GetCustomHook("DefaultMarket")
    if hook is not None:
        return hook()
    return acm.FMarketPlace[_SETTINGS.InternalMarket()]


def DefaultPortfolio():
    """A default portfolio for the trader where all security loan trades are managed.
    If defined, all workbench views will only display trades stored in this portfolio.
    """
    hook = GetCustomHook("DefaultPortfolio")
    if hook is not None:
        return hook()
    return acm.FPhysicalPortfolio[_SETTINGS.TraderPortfolio()]


def DefaultTradeStatus():
    """The default trade status for newly created security loan trades.
    trade in this status does not affect the availability
    Default: Simulated"""
    hook = GetCustomHook("DefaultTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnCreation()


def DefaultHoldTime(trade):
    hook = GetCustomHook("DefaultHoldTime")
    if hook is not None:
        return hook(trade)
    if _SETTINGS.EndOfBusinessDay() is not None:
        hour, min = _SETTINGS.EndOfBusinessDay().split(':')
        return datetime.today().replace(hour=int(hour), minute=int(min), second=0, microsecond=0)
    else:
        return datetime.today().replace(hour=18, minute=0, second=0, microsecond=0)

def ActiveLoansQuery(counterparty=None, instruments=None, portfolio=DefaultPortfolio()):
    """Return a query containing trades pertaining to active loans for the passed
    parameters, if provided.
    """
    hook = GetCustomHook("ActiveLoansQuery")
    if hook is not None:
        return hook(counterparty, instruments)

    query = FSecLendUtils.ActiveLoansBaseQuery()
    if counterparty:
        query.AddAttrNodeString('Counterparty.Name', counterparty.Name(), 'EQUAL')
    if instruments:
        query.AddAttrNodeString('Instrument.Underlying.Name', [instrument.Name() for instrument in instruments], 'EQUAL')
    if portfolio:
        prtfs = portfolio.AllPhysicalPortfolios() if portfolio.IsKindOf(acm.FCompoundPortfolio) else [portfolio]
        FSecLendUtils.AddQueryAttrNodeList(query, 'Portfolio.Name', [prtf.Name() for prtf in prtfs])

    return query


def OnHoldTradeStatus():
    """The default trade status for trades that are not validated with SL yet
    and they affect the availability
    Default: Reserved
    """
    hook = GetCustomHook("OnHoldTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnHold()


def ClipBoardTextHookFromTrades(trades, event=None):
    """The default clipboard text for a trade when clicking on copy to clipboard menu."""
    hook = GetCustomHook("ClipBoardTextHookFromTrades")
    if hook is not None:
        return hook(trades, event)

    counterparty = None
    for t in trades:
        counterparty = counterparty or trades[0].Counterparty()
        if t.Counterparty() != counterparty:
            counterparty = None
            break
    return GenerateOrderReport([t.Oid() for t in trades], 'Clipboard', counterparty)

# ----------------------------------------------------------------------------------------------
#  Rerate parameters


_RERATE_SETTINGS = FParameterSettings.ParameterSettingsCreator.FromRootParameter('SecLendReratePanel')

# FixFeeReratePeriodBDays are considered as Business Days.
FIXED_FEE_DAYS = _RERATE_SETTINGS.FixFeeReratePeriodBDays()

def IsSuggestedFeeValue(rerateHandler):
    """Returns True/False if the value to suggest is the suggested fee or a previous fee. Used in column Security Loan Fixing Value. """
    hook = GetCustomHook("IsSuggestedFeeValue")
    if hook is not None:
        return hook(rerateHandler)
        
    lastFixingChangeDate = rerateHandler.GetLastFeeChangeDate()
    calendar = rerateHandler.FixedOrRebateLeg().PayCalendar()
    adjustedDate = calendar.AdjustBankingDays(lastFixingChangeDate, FIXED_FEE_DAYS)
    
    # If adjustedDate (lastFixingChangeDate + Fixed Fee Period) is later than the default DefaultExtendDate, fixing value should be popuplated with the Last Fixed Fee.
    if adjustedDate >= rerateHandler.DefaultExtendDate():
        return False
    # If adjustedDate is not later, fixing value is populated with Suggested Fee
    else:
        return True

def IsValidForRerate(instrument):
    """ Returns True/False if the instrument is valid for rerating. If the result is True, the instrument will appear on the Rerate panel."""
    hook = GetCustomHook("IsValidForRerate")
    if hook is not None:
        return hook(instrument)

    if instrument.ProductTypeChlItem() and instrument.ProductTypeChlItem().Name() == 'Master Security Loan':
        return False

    if (instrument.IsExpired()) or (not instrument.InsType() == 'SecurityLoan'):
        return False

    for leg in instrument.Legs():
            for cf in leg.CashFlows():
                for r in cf.Resets():
                    if r.ResetType() == "Spread":
                        return True

def IsValidTradeForRerate(trade):
    """ Returns True/False if the trade is valid for rerating. If the result is True, the instrument will appear on the Rerate panel."""
    hook = GetCustomHook("IsValidTradeForRerate")
    if hook is not None:
        return hook(trade)

    return True if trade.Status() not in ('Simulated', 'Void') else False


# ----------------------------------------------------------------------------------------------
#  Deal parameters

def ClientCounterparty(user):
    """Return the counterparty for the passed user. Used for setting the trade counterparty
    on deals created by the client (logged in user) themselves."""
    hook = GetCustomHook("ClientCounterparty")
    if hook is not None:
        return hook(user)
    return user.AddInfoValue("SL_Counterparty")


def IsValidForReturn(trade, counterparty=None):
    """Evaluate to whether or not the trade is allowed to be returned."""
    hook = GetCustomHook("IsValidForReturn")
    if hook is not None:
        return hook(trade, counterparty)
    if counterparty and trade.Counterparty() != counterparty:
        return False
    return not trade.IsClosingTrade() and FSecLendUtils.HasRemainingNominal(trade)

def AllocateReturnByPrice(activeTrades, quantity, highCostFirst=True):
    hook = GetCustomHook("AllocateReturnByPrice")
    if hook is not None:
        return hook(activeTrades, quantity, highCostFirst)

def AllocateCoverByPrice(availabilities, quantityToCover, highCostFirst=False):
    hook = GetCustomHook("AllocateCoverByPrice")
    if hook is not None:
        return hook(availabilities, quantityToCover, highCostFirst)

def AssertTradeValidity(trade):
    """Evaluate to whether or not the trade is allowed to be commited"""
    hook = GetCustomHook("AssertTradeValidity")
    if hook is not None:
        return hook(trade)
    pass


def ReturnTradeStatus():
    """The initial trade status for trades representing a return of a loan.
    Default:Simulated
    """
    hook = GetCustomHook("ReturnTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnReturn()


def ApprovedTradeStatus():
    """The trade status after validation checks.
    Default:FO Confirmed
    """
    hook = GetCustomHook("ApprovedTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnApproval()


def FillTradeStatus():
    """The final trade status after successful workflow processing.
    Default: BO Confirmed
    """
    hook = GetCustomHook("FillTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnFill()


def SettlementTradeStatus():
    """The trade status representing settled trades.
    Default:Legally Confirmed
    """
    hook = GetCustomHook("SettlementTradeStatus")
    if hook is not None:
        return hook()
    return _SETTINGS.TradeStatusOnSettlement()


def IsValidUserForRibbon(trades):
    hook = GetCustomHook("IsValidUserForRibbon")
    if hook is not None:
        return hook(trades)
    validUser = []
    for trade in trades:
        if trade.Trader() != acm.User():
            validUser.append(trade.Trader())
    return True if (len(validUser) == 0) else False


# ----------------------------------------------------------------------------------------------
#  Workflow parameters

def IsValidForOrderWorkflow(trade):
    """Returns whether or not the passed trade should initiate a new order workflow process."""
    hook = GetCustomHook("IsValidForOrderWorkflow")
    if hook is not None:
        return hook(trade)
    return (trade.Instrument().IsKindOf(acm.FSecurityLoan) and
            trade.Status() in [DefaultTradeStatus(), OnHoldTradeStatus()] and
            trade.Type() in ('Normal', 'Reservation', 'Adjust', 'Closing', 'Corporate Action', 'Rollout') and
            not FSecLendUtils.IsAvailabilityTrade(trade)
            # TODO: add here if not a portfolio pricer trade
            )


def Ready_WorkflowHook(workflow_instance):
    hook = GetCustomHook('Ready_WorkflowHook')
    if hook is not None:
        return hook(workflow_instance)
    else:
        return (None, {}, [])


def Rejected_WorkflowHook(workflow_instance):
    hook = GetCustomHook('Rejected_WorkflowHook')
    if hook is not None:
        return hook(workflow_instance)
    else:
        return (None, {}, [])


def Validating_WorkflowHook(workflow_instance):
    hook = GetCustomHook('Validating_WorkflowHook')
    if hook is not None:
        return hook(workflow_instance)
    else:
        return (None,  {}, [])


def IsValidForProcessing(trade):
    """
    Mandatory trade fields needed to be validated here
    This function may return a string with missing required parameters for
    a sec loan to be valid.
    Always return FSecLendUtils.getTradeTooltip(validity_attr, size_of_field):String with size_of_field
    the size of the field (not the size of the value) that will be used to store the tooltip and the return value
    the message to show to the user about what is missing for the trade to be valid.
    """
    hook = GetCustomHook('IsValidForProcessing')
    if hook is not None:
        return hook(trade)
    validity_attr = collections.OrderedDict([("Counterparty", trade.Counterparty()),
                                    ("Portfolio", trade.Portfolio()),
                                    ("Quantity", trade.Quantity())])

    return all(validity_attr.values()), FSecLendUtils.getTradeTooltip(validity_attr)

def IsOverClosingPosition(closingTrades):
    """
    Used to prevent the user to book trades that will over close the position. 
    """
    hook = GetCustomHook('IsOverClosingPosition')
    if hook is not None:
        return hook(closingTrades)
    if closingTrades:
        from FSecLendHandler import SecurityLoanTradeAction
        q = {}
        for t in closingTrades:
            instrument = t.Instrument().Name()
            if not q.has_key(instrument):
                q[instrument] = SecurityLoanTradeAction()._RemainingQuantity(t.ContractTrade())
            remaining = q[instrument]
            q[instrument] += t.Quantity()
            if not abs(q[instrument]) < abs(remaining) >= abs(t.Quantity()): 
                #Remaining Quantity < Quantity of selected trade OR Remaing quantity and quantity have same sign 
                return True, instrument
    return False, None


# delete this later
def SetAlias(ins, alias_type_name, alias_value):
    """Set an instrument alias. The instrument should already be committed."""
    import acm
    alias_type = acm.FInstrAliasType[alias_type_name]
    if not alias_type:
        alias_type = acm.FInstrAliasType()
        alias_type.Name = alias_type_name
        alias_type.AliasTypeDescription = 'TradeGroup.Id from SLS'
        alias_type.Commit()
    alias = acm.FInstrumentAlias.Select01(
        'type=%d and instrument=%d' % (alias_type.Oid(), ins.Oid()),
        ''
    )

    if not alias_value:
        if alias:
            alias.Delete()
        return
    if alias and alias.Alias() == alias_value:
        return
    misplaced_alias = acm.FInstrumentAlias.Select01(
        'alias="%s" and type=%d' % (
            alias_value,
            alias_type.Oid()
        ),
        ''
    )
    if misplaced_alias:
        print('%s: Removing alias <%s:%s>' % (misplaced_alias.Instrument().Name(), alias_type_name, alias_value))
        misplaced_alias.Delete()
    if not alias:
        alias = acm.FInstrumentAlias()
    alias.Instrument = ins
    alias.Type = alias_type
    alias.Alias = alias_value
    alias.Commit()


def SetTradeTooltip(trade, trade_tooltip):
    """
    :param trade: acm trade
    :param trade_tooltip: a string where to save the validation error string
    """
    hook = GetCustomHook("SetTradeTooltip")
    if hook is not None:
        hook(trade)
        return


def ValidSecLoanIcon(trade):
    """Checks if minimum needed parameters of a loan are set or not"""
    hook = GetCustomHook("ValidSecLoanIcon")
    if hook is not None:
        return hook(trade)
    isvalid, trade_tooltip = IsValidForProcessing(trade)
    return "GreenBall" if isvalid else "RedBall", trade_tooltip


class WorkflowStateChart(object):
    """Defines the state chart used for the workflow surrounding securities lending
    order handling.
    """
    NAME = 'Securities Lending'
    DEFINITION = {'Ready'            : {'Start': 'Validating',
                                         'Book directly' : 'Booked'},
                  'Validating'        : {'OK'        : 'Ready for processing',
                                         'Failed'     : 'Validation failed'},
                  'Validation failed' : {'Reject'            : 'Rejected',
                                         'Re-check'          : 'Validating',
                                         'Manual approve'    : 'Ready for processing'},
                  'Ready for processing' : {'Re-check'  : 'Validating',
                                         'Reject'    : 'Rejected',
                                         'Book': 'BO Export',
                                         'Respond'    : 'Awaiting Reply'},
                  'Awaiting Reply'    : {'Re-check'    : 'Validating',
                                         'Reply received': 'Ready for processing',
                                         'Book': 'BO Export',
                                         'Reject': 'Rejected'},
                  'BO Export'         : {'OK':'Booked'} ,
                  'Booked'            : {'Modify Trade': 'BO Export'}
             }

    LAYOUT = (
        'Ready for processing,309,113;'
        'Validating,43,-121;'
        'Validation failed,570,-123;'
        'Rejected,566,337;'
        'Awaiting Reply,40,332;'
        'Booked,-173,589;'
        'BO Export,311,593;'
        'Ready,-172,-122;'
    )


# ----------------------------------------------------------------------------------------------
#  Diary Last Entry 

def DiaryLastEntry(trade):
    """Checks if the last entry of the diary contains any information"""
    hook = GetCustomHook("DiaryLastEntry")
    if hook is not None:
        return hook(trade)
    isEmpty, trade_tooltip = GetDiaryLastEntry(trade)
    return "NoNotification" if isEmpty else "Notification", trade_tooltip

def GetDiaryLastEntry(trade):
    hook = GetCustomHook("GetDiaryLastEntry")
    if hook is not None:
        return hook(trade)
    isEmpty = True
    notes = None
    bps = GetBusinessProcessFromTrade(trade)
    if bps:
        diary = bps[0].CurrentStep().DiaryEntry()
        isEmpty = not (diary.Notes())
        if not isEmpty:
            notes = "Notes: " + '  '.join(diary.Notes())
    return isEmpty, notes

def GetBusinessProcessFromTrade(trade):
    hook = GetCustomHook("GetBusinessProcessFromTrade")
    if hook is not None:
        return hook(trade)
    stateChartDefinition = WorkflowStateChart
    bps = [ bp for bp in acm.BusinessProcess.FindBySubjectAndStateChart(trade, stateChartDefinition.NAME)]
    return bps

# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------
#  Entry Group Info

def CreateTradeOriginInfo(text, parsingErrors, **kwargs):
    hook = GetCustomHook("CreateTradeOriginInfo")
    if hook is not None:
        return hook(text, parsingErrors, **kwargs)
    
    reference = kwargs.get('Reference', '')
    fileName = kwargs.get('FileName', '')

    entryInformation = "Security Loan %s Import %s\n" % (reference, acm.Time.TimeNow())
    if fileName:
        entryInformation += fileName
    else:
        entryInformation += text
        
    if parsingErrors:
        entryInformation += '\n\nErrors from parsing:\n'
        entryInformation += parsingErrors
        
    return entryInformation

def GetTradeOriginInfo(trade):
    hook = GetCustomHook("GetTradeOriginInfo")
    if hook is not None:
        return hook(trade)
    textObjId = trade.AddInfoValue('SBL_TradeOriginId')
    info = acm.FCustomTextObject[textObjId] and acm.FCustomTextObject[textObjId].Text() 
    return info or ''

# ----------------------------------------------------------------------------------------------
#  Deal entry hooks

def PresetOnUnderlyingChanged(trade):
    hook = GetCustomHook("PresetOnUnderlyingChanged")
    if hook is not None:
        return hook(trade)
    return dict()


def PresetOnCounterpartyChanged(trade):
    hook = GetCustomHook("PresetOnCounterpartyChanged")
    if hook is not None:
        return hook(trade)
    return dict()


def PresetOnAccountChanged(trade):
    hook = GetCustomHook("PresetOnAccountChanged")
    if hook is not None:
        return hook(trade)
    return dict()


def DefaultDealEntryColumns():
    hook = GetCustomHook("DefaultDealEntryColumns")
    if hook is not None:
        return hook()
    return ['Security Loan Collateral Cost (Replication)',
            'Security Loan Collateral Cost (Sourcing)',
            'Security Loan Marginal Source Cost',
            'Security Loan Sourcing Fee',
            'Security Loan Suggested Fee']


def SuggestRateColumn():
    hook = GetCustomHook("SuggestRateColumn")
    if hook is not None:
        return hook()
    return 'Security Loan Suggested Fee'


def GetCollateralAgreementChoices(cpty):
    hook = GetCustomHook("GetCollateralAgreementChoices")
    if hook is not None:
        return hook(cpty)
    collateralAgreements = acm.FArray()
    if cpty:
        collateralAgreements.AddAll([l.CollateralAgreement() for l in cpty.CollateralAgreementLinks()])

    q = ael.asql("""select distinct l.coll_agreement_seqnbr , c.seqnbr
                    into temp_table
                    from CollateralAgreement c, CollAgreementLink l
                    where l.coll_agreement_seqnbr =* c.seqnbr
                    select seqnbr from temp_table
                    where coll_agreement_seqnbr = 0
                    """)

    collateralAgreements.AddAll([acm.FCollateralAgreement[int(a[0])] for a in q[1][0]])
    return collateralAgreements


def GetOrderSources():
    hook = GetCustomHook("GetOrderSources")
    if hook is not None:
        return hook()
    markets = []
    for source in _SETTINGS.OrderSources():
        market = acm.FMarketPlace[source]
        if market:
            markets.append(market)
    return markets

def IsCompliantToSourceMapping(selected_trades):
    """
    This function is to handle activation or desactivation of the Respond buttons based on the source and target
    :param selected_trades:
    :return: Boolean

    """
    hook = GetCustomHook("IsCompliantToSourceMapping")
    if hook is not None:
        return hook()
    return True


def GetAccountChoices(obj):  # Returns lists of ShortNames for GUI
    hook = GetCustomHook("GetAccountChoices")
    if hook is not None:
        return hook(obj)
    return []


def EnrichTradeData(trade, originalTrade = None):
    hook = GetCustomHook("EnrichTradeData")
    if hook is not None:
        hook(trade, originalTrade)
    else:
        collateralAgreements = GetCollateralAgreementChoices(trade.Counterparty())
        if collateralAgreements:
            originalCollAgree = originalTrade and originalTrade.AddInfoValue("CollateralAgreement")
            collAgree = originalCollAgree if originalCollAgree and (originalCollAgree in collateralAgreements) else collateralAgreements[0]
            trade.AddInfoValue("CollateralAgreement", collAgree)
        accounts = GetAccountChoices(trade.Counterparty())
        if accounts:
            originalAccount = originalTrade and originalTrade.AddInfoValue("SL_Account")
            account = originalAccount if originalAccount and (originalAccount in accounts) else accounts[0]
            trade.AddInfoValue("SL_Account", account)


def FromShortNameToId(obj, ShortName):  # Transform a GUI ShortName to an Id for trade mapping
    hook = GetCustomHook("FromShortNameToId")
    if hook is not None:
        return hook(obj, ShortName)
    return ShortName


def FromIdToShortName(obj, id):  # Transform a GUI ShortName to an Id for trade mapping
    hook = GetCustomHook("FromIdToShortName")
    if hook is not None:
        return hook(obj, id)
    return id


# ----------------------------------------------------------------------------------------------
# Web hooks
def OnAddWebOrder(trade):
    """This function can be used to fill in more parameters to the trades"""
    hook = GetCustomHook("OnAddWebOrder")
    if hook is not None:
        return hook(trade)
    pass

# ----------------------------------------------------------------------------------------------
#  UI event handlers
def GetSalesNotesLastEntry(security):
    master = FSecLendUtils.GetMasterSecurityLoan(security)
    diary = None
    if master:
        diary = acm.FSalesActivityDiary['SalesNotes_{0}'.format(master.Oid())]
    return (True, None) if not diary else (False, diary.Text())

def SalesNotes(security, realTimeClock=None):
    (isEmpty, tooltip) = GetSalesNotesLastEntry(security)
    return (None, None) if isEmpty else ("Diary", tooltip)

def OnDealSheetGridDoubleClickCell(invokationInfo): 
    # Double Click on 'Security Loan Diary Last Entry' column/cell
    hook = GetCustomHook("OnDealSheetGridDoubleClickCell")
    if hook is not None:
        return hook(invokationInfo)
    
    cell = invokationInfo.Parameter('sheet').Selection().SelectedCell()
    column = cell.Column()
    if column.ColumnId().Text() == 'Security Loan Diary Last Entry':
        trade = cell.RowObject().Trade()
        bps = GetBusinessProcessFromTrade(trade)
        if bps:
            acm.StartApplication('Business Process Details', bps[0])
            return
    elif column.ColumnId().Text() == 'Security Loan Sales Notes':
        if cell.RowObject().IsKindOf("FMultiInstrumentAndTrades"):
            insortrade = cell.RowObject().SingleInstrumentOrSingleTrade()
            if insortrade and insortrade.IsKindOf("FInstrument"):
                CreateFSalesNotesUxInstance(invokationInfo, insortrade)
    else:
        from FUIEventHandlers import DealSheet_DoubleClick
        DealSheet_DoubleClick(invokationInfo)

