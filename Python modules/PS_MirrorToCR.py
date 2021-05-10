'''
Helper functions for the mirror ATS
'''

import json

import acm
import ael

from FBDPCommon import toDate
from at_ael_variables import AelVariableHandler
from PS_Functions import SetAdditionalInfo, get_pb_fund_counterparty
from PS_new_fees import add_cfd_execution_fee
from at_logging import getLogger


LOGGER = getLogger()
PORTFOLIO_MAP = {}
ABSA_BANK = acm.FParty['ABSA BANK LTD']
PRIME_DESK = acm.FParty['PRIME SERVICES DESK']
GENERIC_CFD_TEMPLATE = 'ZAR/DEFAULT/CFD'
CTO_PARAMS = "PS_MirrorToCR_OldTaskParams"
VALID_INS_TYPE_FOR_CFD = ["Stock", "Equity Index", "ETF"]


def AddDividendSuppression(original_trade, new_trade):
    """Copy over dividend suppression payment."""
    for payment in original_trade.Payments():
        if payment.Type() == "Dividend Suppression":
            new_payment = payment.Clone()
            new_payment.Trade(new_trade)
            new_payment.RegisterInStorage()
            new_payment.Commit()


def ReversePayments(trade):
    '''This function takes a trade as input and reverses the sign on the payments'''
    acm.BeginTransaction()
    try:
        for payment in trade.Payments():
            payment_clone = payment.Clone()
            payment_clone.Amount(payment.Amount() * -1.0)
            payment.Apply(payment_clone)
            payment.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        LOGGER.exception('Payment on trade {} not inverted!'.format(trade.Oid()))


def DeletePayments(trade):
    try:
        trade.Payments().Delete()
    except Exception:
        LOGGER.exception('Payments on trade {} not deleted!'.format(trade.Oid()))


def MirrorTrade(trade):
    '''
    Take a trade as an input and create a mirror trade, i.e. equal
    and opposite on the same instrument.
    The Optional Key is cleared out.
    '''
    tclone = trade.StorageNew()
    tclone = fillMirrorTrade(tclone, trade)
    try:
        tclone.Commit()
    except Exception:
        LOGGER.exception('Mirror Trade for trade {} was not created!'.format(trade.Oid()))
    set_addinfos(tclone)
    ReversePayments(tclone)
    return tclone


def fillMirrorTrade(tclone, trade):
    tclone.Portfolio(PORTFOLIO_MAP[trade.Portfolio().Name()])
    tclone.OptionalKey('')
    tclone.Quantity(trade.Quantity()*-1)
    tclone.Premium(trade.Premium()*-1)
    tclone.Counterparty(ABSA_BANK)
    tclone.Acquirer(PRIME_DESK)
    tclone.Status(trade.Status())
    tclone.Contract(trade)
    tclone.Text1('CR Trade')
    return tclone


def set_addinfos(tclone):
    """
    Set additional infos
    This function assumes tclone is at least registered.
    """
    acm.PollDbEvents()  # Sometimes ADS does not see the updates in time
    ais = tclone.AddInfos()
    for ai in ais:
        if ai.AddInf().FieldName() == 'CCPmiddleware_id':
            ai.Delete()
            break


def hasValidMirrorTrade(trade):
    candidate_trades = acm.FTrade.Select('contractTrdnbr = %d' % trade.Oid())
    for t in candidate_trades:
        if t.Oid() != trade.Oid() \
                and t.Status() != 'Simulated' \
                and t.Text1() == 'CR Trade':
            return True
    return False


def OriginalUpdatedToday(trade):
    today = acm.Time.DateToday()

    # Assess if the original trade was updated today
    if trade.ContractTrdnbr() == trade.Oid():
        trade_update_time = ael.date_from_time(trade.UpdateTime())
        if trade_update_time.to_string('%Y-%m-%d') == today:
            return True
    if trade.Type() == 'Closing' \
            and acm.FTrade[trade.ContractTrdnbr()].Type() == 'Normal':
        trade_update_time = ael.date_from_time(trade.UpdateTime())
        if trade_update_time.to_string('%Y-%m-%d') == today:
            return True

    # Assess if the split (stock) trade from allocation run was updated today
    if trade.ContractTrdnbr() != trade.Oid() \
            and trade.Portfolio().add_info('PS_PortfolioType') == 'CFD':
        trade_update_time = ael.date_from_time(trade.UpdateTime())
        if trade_update_time.to_string('%Y-%m-%d') == today:
            return True

    return False


def getMirrorTrade(trade):
    # Old method ignored Void mirror trades completely, i.e. the script was
    # creating on every run a new voided trade. In order to accommodate
    # reinstating the on-tree trade in this case, always the highest trade
    # number will be returned.
    trade_oid = trade.Oid()
    candidate_trades = acm.FTrade.Select('contractTrdnbr = %d' % trade_oid)
    for t in sorted(candidate_trades, reverse=True, key=lambda x: x.Oid()):
        if t.Oid() != trade_oid \
                and t.Status() != 'Simulated' \
                and t.Text1() == 'CR Trade':
            return t
    return None


def MirrorTradeUpdate(trade):
    mirror_trade = getMirrorTrade(trade)
    if mirror_trade:
        t_clone_original = trade.StorageNew()
        acm.BeginTransaction()
        try:
            mirror_trade_clone = mirror_trade.Clone()
            mirror_trade_clone.Apply(t_clone_original)  # This takes care of addinfos and payments as well
            mirror_trade.Apply(mirror_trade_clone)
            mirror_trade = fillMirrorTrade(mirror_trade, trade)
            mirror_trade.Commit()
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            LOGGER.exception('Mirror Trade for trade {} was not updated!'.format(trade.Oid()))
        set_addinfos(mirror_trade)
        ReversePayments(mirror_trade)
    return mirror_trade


def fillCFDTrade(tnew, trade):
    tnew.Quantity(trade.Quantity())
    if trade.Instrument().InsType() in ['EquityIndex']:
        tnew.Price(trade.Price() * 100)  # Price in ZAc
    else:
        tnew.Price(trade.Price())
    tnew.Premium(0)
    tnew.Counterparty(ABSA_BANK)
    tnew.Acquirer(PRIME_DESK)
    tnew.Portfolio(PORTFOLIO_MAP[trade.Portfolio().Name()])
    tnew.Trader(trade.Trader())
    tnew.TradeTime(trade.TradeTime())
    d = acm.Time().AsDate(trade.TradeTime())
    tnew.ValueDay(d)
    tnew.AcquireDay(d)
    tnew.Currency(trade.Currency())
    tnew.Status(trade.Status())
    tnew.Contract(trade)
    tnew.Text1('CR Trade')
    return tnew


def getCFDInstrumentName(trade):
    StockInsName = trade.Instrument().Name()
    """
        Because all the correct combinations of actions will cause a break 
        for other desks, custom solution for Prime only is necessary: 
        amend mirror ATS to mirror ZAR/GLD to ZAR/GLD2/CFD.
        Detailed description of this prod issue in FAPE-454.
    """
    if 'ZAR/GLD' in StockInsName:
        return StockInsName + '2/CFD'
    else:
        return StockInsName + '/CFD'


def getCFDInstrument(trade):
    '''Return CFD instrument, create it when it doesn't exist'''
    CfdInsName = getCFDInstrumentName(trade)
    instrument = acm.FInstrument[CfdInsName]
    # If Stock CFD doesnt exist then create the CFD from the default template.
    # In the case of Index/ETF underlying, TCU needs to either create the
    # correct instrument or check that the one created from the template
    # is correct.
    if not instrument:
        i = trade.Instrument()
        if i.InsType() in VALID_INS_TYPE_FOR_CFD:
            LOGGER.info(
                'Instrument {} currently does not exist, process will'
                ' attempt to create it from template'.format(CfdInsName)
            )
            dummy = acm.FInstrument[GENERIC_CFD_TEMPLATE]
            if not dummy:
                LOGGER.info('Template CFD not found: {}'.format(GENERIC_CFD_TEMPLATE))
                return None
            newCFD = dummy.Clone()
            newCFD.Name(CfdInsName)
            newCFD.Underlying(i)
            newCFD.Generic(False)
            try:
                newCFD.Commit()
                LOGGER.info('{} created from template successfully'.format(CfdInsName))
                return newCFD
            except Exception:
                LOGGER.exception('Instrument {} was not committed!'.format(CfdInsName))
                return None
    return instrument


def StockToCFD(trade):
    '''This function takes a trade and creates an equivalent cfd trade'''
    CfdIns = getCFDInstrument(trade)
    if CfdIns is not None:
        tnew = acm.FTrade()
        tnew.Instrument(CfdIns)
        tnew = fillCFDTrade(tnew, trade)
        try:
            tnew.Commit()
            DeletePayments(tnew)
            if trade.AdditionalInfo().XtpTradeType():
                SetAdditionalInfo(tnew,
                                  'XtpTradeType',
                                  trade.AdditionalInfo().XtpTradeType())
            return tnew
        except Exception:
            LOGGER.exception('Mirror Trade for trade {} was not created!'.format(trade.Oid()))
            return None
    else:
        CfdInsName = getCFDInstrumentName(trade)
        LOGGER.error('CFD Instrument {} does not exist!'.format(CfdInsName))
        return None


def StockToCFDUpdate(trade):
    CfdIns = getCFDInstrument(trade)
    mirrorTrade = getMirrorTrade(trade)
    if mirrorTrade:
        mirrorTrade.Instrument(CfdIns)
        mirrorTrade = fillCFDTrade(mirrorTrade, trade)
        try:
            mirrorTrade.Commit()
            DeletePayments(mirrorTrade)
            if trade.AdditionalInfo().XtpTradeType():
                SetAdditionalInfo(mirrorTrade,
                                  'XtpTradeType',
                                  trade.AdditionalInfo().XtpTradeType())
            return mirrorTrade
        except Exception:
            LOGGER.exception(
                'Mirror Trade for trade {} was not updated:'
                ' {1}'.format(trade.Oid())
            )


def GetCRPortfolio(portfolio, default):
    '''This function takes a portfolio and returns the matching client
    reporting portfolio or the default portfolio
    '''
    if portfolio.AdditionalInfo().PS_MirrorCRBook():
        # KUTNIKPE 2012-05-02
        # Addinfo-based lookup added for multistrat clients
        return portfolio.AdditionalInfo().PS_MirrorCRBook()
    port = acm.FPhysicalPortfolio[portfolio.Name() + '_CR']
    if not port:
        return default
    return port


def GeneratePortfolioMapping(compoundPortfolio, extraPortfolio,
                             compoundCRPortfolio, default, portfolioTypes):
    cfdPort = None
    for portfolio in compoundCRPortfolio.AllPhysicalPortfolios():
        if portfolio.Name().find('CFD') > 0:
            cfdPort = portfolio
    if not cfdPort:
        cfdPort = default
    all_physical_portfolios = compoundPortfolio.AllPhysicalPortfolios()
    if extraPortfolio:
        added_portfolio = all_physical_portfolios.Add(extraPortfolio)
        if not added_portfolio:
            LOGGER.warning('Could not add portfolio {}'.format(extraPortfolio.Name()))
    for portfolio in all_physical_portfolios:
        if portfolio.add_info('PS_PortfolioType') in portfolioTypes:
            if portfolio.Name() not in PORTFOLIO_MAP and \
                    portfolio.add_info('PS_PortfolioType') == 'General':
                PORTFOLIO_MAP[portfolio.Name()] = GetCRPortfolio(portfolio, default)
            if portfolio.add_info('PS_PortfolioType') == 'CFD' \
                    and portfolio.Name() not in PORTFOLIO_MAP:
                # KUTNIKPE 2012-05-02
                # Fixed to map correctly for multistrat clients while
                # preserving existing behaviour
                mappedCRPortfolio = GetCRPortfolio(portfolio, cfdPort)
                PORTFOLIO_MAP[portfolio.Name()] = mappedCRPortfolio


def _PhysicalPortfoliosExist(compoundPortfolio, extraPortfolio, portfolioType):
    '''Check if the Compound Portfolio has valid Physical Portfolios'''
    all_physical_portfolios = compoundPortfolio.AllPhysicalPortfolios()
    if extraPortfolio:
        added_portfolio = all_physical_portfolios.Add(extraPortfolio)
        if not added_portfolio:
            LOGGER.warning('Could not add portfolio {}'.format(extraPortfolio.Name()))
    for portfolio in all_physical_portfolios:
        if portfolio.add_info('PS_PortfolioType') in portfolioType:
            return True
    return False


def _GenerateQuery(compoundPortfolio, extraPortfolio, date, counterParty,
                   portfolioType):
    '''Generate a query that selects all trades that need to be mirrored.'''
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status',
                      'NOT_EQUAL',
                      acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Instrument.InsType',
                      'NOT_EQUAL',
                      acm.EnumFromString('InsType', 'Deposit'))
    query.AddAttrNode('Instrument.InsType',
                      'NOT_EQUAL',
                      acm.EnumFromString('InsType', 'Portfolio Swap'))

    if counterParty:
        query.AddAttrNode('Counterparty.Name', 'EQUAL', counterParty.Name())

    # Don't mirror aggregated trades
    query.AddAttrNode('Aggregate', 'EQUAL', 0)

    # If create_time, trade_time or update_time is equal to date,
    # include it in the query
    orNode1 = query.AddOpNode('OR')
    andNode1 = orNode1.AddOpNode('AND')
    andNode1.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    andNode1.AddAttrNode('CreateTime', 'LESS_EQUAL', date)

    andNode2 = orNode1.AddOpNode('AND')
    andNode2.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    andNode2.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    andNode3 = orNode1.AddOpNode('AND')
    andNode3.AddAttrNode('UpdateTime', 'GREATER_EQUAL', date)
    andNode3.AddAttrNode('UpdateTime', 'LESS_EQUAL', date)

    # Add the sub portfolios to the query
    orNode2 = query.AddOpNode('OR')
    all_physical_portfolios = compoundPortfolio.AllPhysicalPortfolios()
    if extraPortfolio:
        added_portfolio = all_physical_portfolios.Add(extraPortfolio)
        if not added_portfolio:
            LOGGER.warning('Could not add portfolio {}'.format(extraPortfolio.Name()))
    for portfolio in all_physical_portfolios:
        if portfolio.add_info('PS_PortfolioType') == portfolioType:
            orNode2.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())

    return query


def check_compound_portfolio(compound_pf):
    if compound_pf.value and not acm.FCompoundPortfolio[compound_pf.value]:
        acm.GetFunction('msgBox', 3)('ERROR', "Invalid compound portfolio!", 0)


def check_physical_portfolio(physical_pf):
    if physical_pf.value and not acm.FPhysicalPortfolio[physical_pf.value]:
        acm.GetFunction('msgBox', 3)('ERROR', "Invalid physical portfolio!", 0)


def check_counterparty(cp):
    if cp.value and not acm.FCounterParty[cp.value]:
        acm.GetFunction('msgBox', 3)('ERROR', "Invalid counterparty!", 0)


def get_params_from_cto(cto_name, short_name):
    cto = acm.FCustomTextObject[cto_name]
    data_dict = json.loads(cto.Text())
    data_client = data_dict[short_name]
    compoundPortfolio = acm.FPhysicalPortfolio[str(data_client['compound'])]
    extraPortfolio = acm.FPhysicalPortfolio[str(data_client['extra'])]
    compoundCRPortfolio = acm.FPhysicalPortfolio[str(data_client['compound_cr'])]
    defaultPortfolio = acm.FPhysicalPortfolio[str(data_client['default'])]
    return (compoundPortfolio,
            extraPortfolio,
            compoundCRPortfolio,
            defaultPortfolio)


def prepare_ael_variables():
    params = AelVariableHandler()
    params.add('clientName',
               label='Fund Short Name',
               cls='string',
               alt=('SoftBroker alias (short name). Only trades with counterparty'
                    ' equal to client will have fees added to them.'))
    params.add('idate',
               label='Date',
               cls='string',
               collection=[acm.Time.DateToday(), 'Today'],
               default='Today',
               mandatory=False)
    params.add_bool('force_update',
                    label="Force Update?",
                    default=False)
    return params


ael_variables = prepare_ael_variables()
ael_gui_parameters = {'windowCaption': 'Prime Broker: Client Reporting Mirroring Script'}


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()

    short_name = ael_dict['clientName']
    counterParty = get_pb_fund_counterparty(short_name)
    (compoundPortfolio, extraPortfolio, compoundCRPortfolio,
        defaultPortfolio) = get_params_from_cto(CTO_PARAMS, short_name)
    date = toDate(ael_dict['idate'])
    force_update = ael_dict['force_update']
    desks_with_cfd = [acm.FParty[desk] for desk
                      in ['JSE', 'EQ Derivatives Desk', 'ABSA BANK LTD', 'PRIME SERVICES DESK']]

    propQuery = None
    if _PhysicalPortfoliosExist(compoundPortfolio, extraPortfolio,
                                ['General']):
        propQuery = _GenerateQuery(compoundPortfolio, extraPortfolio, date,
                                   counterParty, 'General').Select()

    cfdQuery = None
    if _PhysicalPortfoliosExist(compoundPortfolio, extraPortfolio, ['CFD']):
        cfdQuery = _GenerateQuery(compoundPortfolio, extraPortfolio, date,
                                  None, 'CFD').Select()

    GeneratePortfolioMapping(compoundPortfolio, extraPortfolio,
                             compoundCRPortfolio, defaultPortfolio,
                             ['General', 'CFD'])

    if propQuery:
        for t in propQuery:
            if not hasValidMirrorTrade(t):
                LOGGER.info(
                    'OLD - New {0} {1} {2}'.format(
                        t.Oid(),
                        t.Instrument().Name(),
                        t.Portfolio().Name()
                    )
                )
                tnew = MirrorTrade(t)
                if tnew:
                    LOGGER.info(
                        'NEW - New {0} {1} {2}'.format(
                            tnew.Oid(),
                            tnew.Instrument().Name(),
                            tnew.Portfolio().Name()
                        )
                    )
                else:
                    LOGGER.error('Mirror was not created for trade {0}'.format(t.Oid()))
            elif OriginalUpdatedToday(t) or force_update:
                LOGGER.info(
                    'OLD - Updated {0} {1} {2}'.format(
                        t.Oid(),
                        t.Instrument().Name(),
                        t.Portfolio().Name()
                    )
                )
                tnew = MirrorTradeUpdate(t)
                if tnew:
                    LOGGER.info(
                        'NEW - Updated {0} {1} {2}'.format(
                            tnew.Oid(),
                            tnew.Instrument().Name(),
                            tnew.Portfolio().Name()
                        )
                    )
                else:
                    LOGGER.error('Mirror for trade {} was not updated'.format(t.Oid()))
            else:
                LOGGER.info(
                    'No new trade created for {}, client reporting '
                    'trade already exists.'.format(t.Oid())
                )

    if cfdQuery:
        for t in cfdQuery:
            if t.Counterparty() in desks_with_cfd \
                    and t.Instrument().InsType() in VALID_INS_TYPE_FOR_CFD:
                if not hasValidMirrorTrade(t):
                    LOGGER.info(
                        'OLD - New {0} {1} {2}'.format(
                            t.Oid(),
                            t.Instrument().Name(),
                            t.Portfolio().Name()
                        )
                    )
                    tnew = StockToCFD(t)
                    if tnew:
                        execution_fee = add_cfd_execution_fee(tnew)
                        AddDividendSuppression(t, tnew)
                        LOGGER.info(
                            'NEW - New {0} {1} {2}, execution fee: {3}'.format(
                                tnew.Oid(),
                                tnew.Instrument().Name(),
                                tnew.Portfolio().Name(),
                                execution_fee
                            )
                        )
                    else:
                        LOGGER.error('Mirror was not created for trade {}'.format(t.Oid()))
                elif OriginalUpdatedToday(t) or force_update:
                    LOGGER.info(
                        'OLD - Updated {0} {1} {2}'.format(
                            t.Oid(),
                            t.Instrument().Name(),
                            t.Portfolio().Name()
                        )
                    )
                    tnew = StockToCFDUpdate(t)
                    if tnew:
                        execution_fee = add_cfd_execution_fee(tnew)
                        AddDividendSuppression(t, tnew)
                        LOGGER.info(
                            'NEW - Updated {0} {1} {2}, execution fee: {3}'.format(
                                tnew.Oid(),
                                tnew.Instrument().Name(),
                                tnew.Portfolio().Name(),
                                execution_fee
                            )
                        )
                    else:
                        LOGGER.error('Mirror was not updated for trade {}'.format(t.Oid()))
                else:
                    LOGGER.info(
                        'No new trade created for {}, client reporting '
                        'trade already exists.'.format(t.Oid())
                    )

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully")
