'''-----------------------------------------------------------------------------
Project: Prime Brokerage Project
Department: Prime Services
Requester: Francois Henrion
Developer: Paul Jacot-Guillarmod
CR Number: 666125 (Initial Deployment)

HISTORY
================================================================================
Date       Change no     Developer                Description
--------------------------------------------------------------------------------
2011-06-07 677654        Paul Jacot-Guillarmod    Made an update to use Client ValEnd instead of built in ValEnd when
                                                  calculating funding and to use the Client PositionEnd instead of the
                                                  builtin position end.
2011-06-17 685737        Paul Jacot-Guillarmod    Updated the pswap to store down TPL on a new leg
2011-10-05 XXXXXX        Rohan van der Walt       Added ETFs to the short rate funding adjustment
2011-12-08 850928        Herman Hoon              Updated to include the Daily Provision generator
2011-12-09 855399        Herman Hoon              Add the GetCashFlow function
2013-08-06 1232225       Peter Fabian             Funding and warehousing functions extracted out of
                                                  GenerateFunding/GenerateWarehousing functions
2014-04-15 1896053       Libor Svoboda            Left out checking for 'if total TPL' in the GenerateTotalTPL function
2014-06-05 2018619       Hynek Urban              Handling errors in PB overnight batch correctly
                                                  Warn about Nans in TradingManagerSweeper
2015-07-14 2961517       Jakub Tomaga             Sweeping report added.
2015-09-11 3090331       Jakub Tomaga             Portfolio independent sweeping
2016-03-17 3506685       Ondrej Bahounek          Accommodate PBA.
2018-11-12 CHG1001113453 Tibor Reiss              Enable fully funded CFD for MMIBETA2
2018-12-06 CHG1001204171 Tibor Reiss              Rewrite funding calculation
2018-12-28 CHG1001247290 Tibor Reiss              After aggregation, move funding to cash instrument
2019-03-27 FAPE-65       Tibor Reiss              Remove fully funded CFD for MMIBETA2 (you are reading it correctly)
2019-06-06 FAPE-83       Marian Zdrazil           Remove currency filter from FundingQuery to accommodate for CDS
                                                  non-ZAR funding
2019-07-15 FAPE-47       Iryna Shcherbina         Create a sweeping report
2019-09-25 FAU-396       Tibor Reiss              Automatic generation of cfs, resets -> fix this
2019-10-22 FAPE-91       Tibor Reiss              Put funding on correct pswap even if trade is booked in wrong pf
                                                  Don't charge funding if portfolio is fully-funded
2020-01-29 FAPE-120      Tibor Reiss              Remove code for old funding method
-----------------------------------------------------------------------------'''
from collections import defaultdict

import acm
import ael

import PS_Functions
import PS_TimeSeriesFunctions
import PS_FundingCalculations
import at
from at_calculation_space import CalculationSpace
from at_logging import getLogger


LOGGER = getLogger(__name__)
CALENDAR = acm.FCalendar['ZAR Johannesburg']


class FundingSweeper_transaction(object):
    def __init__(self, pswap):
        self.pswap = pswap
        self.acm_legs = []
        self.acm_cashFlows = []
        self.cf_addInfos = {}
        self.resets = []
        self.resets_to_delete = []

    def CreateLeg(self, portfolioSwap, legType, instrument, startDate, endDate, floatRef=None):
        try:
            leg = portfolioSwap.CreateLeg(False)
            leg.LegType(legType)
            leg.IndexRef(instrument)
            leg.NominalFactor(1.0)
            leg.Currency(instrument.Currency())
            leg.StartDate(startDate)
            leg.EndDate(endDate)
            leg.DayCountMethod('Act/365')
            leg.PassingType('Dividend Payday')
            leg.ResetCalendar(CALENDAR)
            leg.ResetDayOffset(0)
            if legType == 'Float':
                leg.ResetType('Simple Overnight')
                leg.FloatRateReference(floatRef)
                leg.NominalScaling('Dividend')
            elif legType == 'Total Return':
                leg.ResetType('Daily Return')
                leg.NominalScaling('Dividend')
            else:
                leg.NominalScaling('None')
            self.acm_legs.append(leg)
            LOGGER.info("Creating a new leg for instrument %s" % instrument.Name())
        except Exception as e:
            LOGGER.exception('Failed to create portfolio swap leg for {0}. {1}'.format(instrument.Name(), e))
            raise e
        return leg

    def CreateCashFlow(self, leg, cashFlowType, startDate, endDate, payDate, fixedAmount=None, warehouseFundingType=None):
        ''' Create a cashflow for a leg
        '''
        try:
            cashFlow = leg.CreateCashFlow()
            cashFlow.StartDate(startDate)
            cashFlow.EndDate(endDate)
            cashFlow.PayDate(payDate or endDate)
            cashFlow.CashFlowType(cashFlowType)
            cashFlow.NominalFactor(leg.NominalFactor())
            if cashFlowType == 'Float Rate':
                cashFlow.FixedRate(1.0)
            elif cashFlowType == 'Fixed Amount':
                cashFlow.FixedAmount(fixedAmount)
            self.acm_cashFlows.append(cashFlow)

        except Exception as e:
            LOGGER.exception('Failed to create a cashflow for {0}. {1}'.format(leg.Instrument().Name(), e))
            raise e
        # it is important here to use the cf ref as key because the cash flow
        # can be committed by committing leg and its oid will change  
        if warehouseFundingType:
            self.cf_addInfos[cashFlow] = ('PS_FundWarehouse', warehouseFundingType)

        return cashFlow

    def CreateReset(self, cashFlow, resetType, date, startDate, endDate, fixingValue):
        ''' Create new reset
        '''
        try:
            reset = acm.FReset()
            reset.CashFlow(cashFlow)
            reset.ResetType(resetType)
            reset.Day(date)
            reset.StartDate(startDate)
            reset.EndDate(endDate)
            reset.FixingValue(fixingValue)
            reset.ReadTime(acm.Time.TimeNow())
            self.resets.append(reset)

        except Exception as e:
            LOGGER.exception('Failed to create a reset for {0} of type {1} on date {2}. {3}'.format(cashFlow.Leg().IndexRef().Name(),
                                                                                                    resetType,
                                                                                                    date,
                                                                                                    e))
            raise e

    def DeleteReset(self, reset):
        if reset:
            self.resets_to_delete.append(reset)  

    def ExtendLeg(self, leg, endDate):
        ''' Extend the leg to the new end date
        '''
        if leg.EndDate() < endDate:
            leg.EndDate(endDate)
            if not leg in self.acm_legs:
                self.acm_legs.append(leg)
            # print "Extend leg %s to %s" % (leg.Oid(), endDate)

    def ExtendCashFlow(self, cashFlow, endDate):
        ''' Extend the cashflow to the new end date
        '''
        if cashFlow.EndDate() < endDate:
            cashFlow.EndDate(endDate)
            cashFlow.PayDate(endDate)
            if cashFlow not in self.acm_cashFlows:
                self.acm_cashFlows.append(cashFlow)
            # print "Extend cf %s to %s" % (cashFlow.Oid(), endDate)

    def AdjustCashFlowFixedAmount(self, cashFlow, fixedAmount):
        cashFlow.FixedAmount(fixedAmount)
        if cashFlow not in self.acm_cashFlows:
            self.acm_cashFlows.append(cashFlow)
    
    def UpdateResetFixingValue(self, reset, fixingValue):
        reset.FixingValue(fixingValue)
        reset.ReadTime(acm.Time.TimeNow())
        self.resets.append(reset)

    def Commit(self):
        LOGGER.info("Pswap {0}".format(self.pswap.Name()))

        acm.BeginTransaction()
        try:
            for reset in self.resets_to_delete:
                reset.Delete()
            acm.CommitTransaction()

            if self.resets_to_delete:
                LOGGER.info("Old resets deleted successfully")
            self.resets_to_delete = []
        except:
            acm.AbortTransaction()
            raise


        acm.BeginTransaction()
        try:
            for leg in self.acm_legs:
                leg.Commit()
            acm.CommitTransaction()

            if self.acm_legs:
                LOGGER.info("Legs committed successfully")
            self.acm_legs = []
        except:
            acm.AbortTransaction()
            raise

        acm.BeginTransaction()
        try:
            for cf in self.acm_cashFlows:
                cf.Commit()
            acm.CommitTransaction()

            if self.acm_cashFlows:
                LOGGER.info("Cash Flows committed successfully")
        except:
            acm.AbortTransaction()
            raise

        acm.BeginTransaction()
        try:
            for cf in self.acm_cashFlows:
                if cf in self.cf_addInfos:
                    at.addInfo.save(cf, self.cf_addInfos[cf][0], self.cf_addInfos[cf][1])
            acm.CommitTransaction()

            if self.cf_addInfos:
                LOGGER.info("Cash Flow Additional Infos committed successfully")
            self.acm_cashFlows = []
            self.cf_addInfos = {}
        except:
            acm.AbortTransaction()
            raise

        acm.BeginTransaction()
        try:
            for reset in self.resets:
                reset.Commit()
            acm.CommitTransaction()

            if self.resets:
                LOGGER.info("Resets committed successfully")
            self.resets = []
        except:
            acm.AbortTransaction()
            raise

def CreateLeg(portfolioSwap, legType, instrument, startDate, endDate, floatRef=None):
    ''' Create a leg for a given instrument
    '''
    try:
        leg = portfolioSwap.CreateLeg(False)
        leg.LegType(legType)
        leg.IndexRef(instrument)
        leg.NominalFactor(1.0)
        leg.Currency(instrument.Currency())
        leg.StartDate(startDate)
        leg.EndDate(endDate)
        leg.DayCountMethod('Act/365')
        leg.PassingType('Dividend Payday')
        leg.ResetCalendar(CALENDAR)
        leg.ResetDayOffset(0)
        if legType == 'Float':
            leg.ResetType('Simple Overnight')
            leg.FloatRateReference(floatRef)
            leg.NominalScaling('Dividend')
        elif legType == 'Total Return':
            leg.ResetType('Daily Return')
            leg.NominalScaling('Dividend')
        else:
            leg.NominalScaling('None')
        leg.Commit()
    except Exception as e:
        LOGGER.exception('Failed to create portfolio swap leg for {0}. {1}'.format(instrument.Name(), e))
        raise e
    return leg

def CreateCashFlow(leg, cashFlowType, startDate, endDate, payDate, fixedAmount=None, warehouseFundingType=None):
    ''' Create a cashflow for a leg
    '''
    try:
        cashFlow = leg.CreateCashFlow()
        cashFlow.StartDate(startDate)
        cashFlow.EndDate(endDate)
        cashFlow.PayDate(payDate or endDate)
        cashFlow.CashFlowType(cashFlowType)
        cashFlow.NominalFactor(leg.NominalFactor())
        if cashFlowType == 'Float Rate':
            cashFlow.FixedRate(1.0)
        elif cashFlowType == 'Fixed Amount':
            cashFlow.FixedAmount(fixedAmount)
        if warehouseFundingType:
            cashFlow.AddInfoValue('PS_FundWarehouse', warehouseFundingType)
        cashFlow.Commit()
    except Exception as e:
        LOGGER.exception('Failed to create a cashflow for {0}. {1}'.format(leg.Instrument().Name(), e))
        raise e

    return cashFlow 

def CreateReset(cashFlow, resetType, date, startDate, endDate, fixingValue):
    ''' Create new reset
    '''
    try:
        cashFlowClone = ael.CashFlow[cashFlow.Oid()].clone()
        reset = ael.Reset.new(cashFlowClone)
        reset.type = resetType
        reset.day = ael.date(date)
        reset.start_day = ael.date(startDate)
        reset.end_day = ael.date(endDate)
        reset.value = fixingValue
        reset.read_time = ael.date(date).to_time()
        cashFlowClone.commit()
    except Exception as e:
        LOGGER.exception('Failed to create a reset for {0} of type {1} on date {2}. {3}'.format(cashFlow.Leg().IndexRef().Name(), resetType, date, e))
        raise e

def GetLeg(portfolioSwap, legType, instrument):
    ''' Return the leg of legType for a given instrument
    '''
    for leg in portfolioSwap.Legs():
        if leg.IndexRef().Name() == instrument.Name() and leg.LegType() == legType:
            return leg
    return None

def GetCashFlow(leg):
    ''' Used to get cashflows on the funding leg or total return (tpl) leg
        where there will only be one cashflow with multiple resets.
    '''
    for cashFlow in leg.CashFlows():
        return cashFlow
    return None

def GetReturnCashFlow(leg, cashFlowReturnType='TPL'):
    ''' Return th cashflows on the total return leg (TPL cashflows).  If the addinfo hasn't been set on the cashflow
        and the return type is 'Position Total Return', then assume its a TPL cashflow for backwards compatibility.
    '''
    for cashFlow in leg.CashFlows():
        cashFlowType = cashFlow.add_info('PS_FundWarehouse')
        if not cashFlowType and cashFlowReturnType == 'TPL':
            return cashFlow
        elif cashFlowType and cashFlowType == cashFlowReturnType:
            return cashFlow
    return None

def GetFloatCashFlow(leg, cashFlowReturnType='Funding'):
    ''' Return the Warehousing or Funding cashflow.  If the addinfo hasn't been set on the cashflow
        and the return type is Funding, then assume its a funding cashflow for backwards compatibility.
    '''
    for cashFlow in leg.CashFlows():
        cashFlowType = cashFlow.add_info('PS_FundWarehouse')
        if not cashFlowType and cashFlowReturnType == 'Funding':
            return cashFlow
        elif cashFlowType and cashFlowType == cashFlowReturnType:
            return cashFlow
    return None

def GetFixedCashFlow(leg, date):
    for cashFlow in leg.CashFlows():
        if cashFlow.CashFlowType() == "Fixed Amount" and cashFlow.PayDate() == date:
            return cashFlow
    return None

def GetFeeCashFlow(leg, payDate, feeType):
    ''' There will be multiple fee cashflows on a fee leg.  Return the one corresponding to the given 
        pay date and fee type.
    '''    
    for cashFlow in leg.CashFlows():
        if cashFlow.add_info('PS_FeeType') == feeType and cashFlow.PayDate() == payDate:
            return cashFlow
    return None

def ExtendLeg(leg, endDate):
    ''' Extend the leg to the new end date
    '''
    if leg.EndDate() < endDate:
        leg.EndDate(endDate)
        leg.Commit()
        LOGGER.info("Extend leg %s" % leg.Oid())

def ExtendCashFlow(cashFlow, endDate):
    ''' Extend the cashflow to the new end date
    '''
    if cashFlow.EndDate() < endDate:
        cashFlow.EndDate(endDate)
        cashFlow.PayDate(endDate)
        cashFlow.Commit()
        LOGGER.info("Extend cf %s" % cashFlow.Oid())

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber

def TradingManagerSweeper(queryFolder, date, columnNames, setPrevBusDay=False, grouper=None,
                          inCurrency="ZAR"):
    ''' Return a dictionary of grouper rownames (default will be instruments) mapped to a list of column values corresponding to the list of column names.
    '''
    calculationSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    calculationSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calculationSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    calculationSpace.SimulateGlobalValue('Valuation Date', date)
    calculationSpace.SimulateGlobalValue('Position Currency Choice', 'Instrument Curr')
    if inCurrency:
        calculationSpace.SimulateGlobalValue('Position Currency Choice', 'Fixed Curr')
        calculationSpace.SimulateGlobalValue('Fixed Currency', inCurrency)
    if setPrevBusDay:
        calculationSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'PrevBusDay')

    topNode = calculationSpace.InsertItem(queryFolder)
    if grouper:
        topNode.ApplyGrouper(grouper)
    calculationSpace.Refresh()

    valueDictionary = {}
    instrumentIterator = topNode.Iterator().FirstChild()
    while instrumentIterator:
        rowName = instrumentIterator.Tree().Item().StringKey()

        # Create a list of column values corresponding to column names which will get updated in the dictionary
        columnValues = []
        for columnName in columnNames:
            value = 0
            value = calculationSpace.CalculateValue(instrumentIterator.Tree(), columnName)
            try:
                value = value.Number()
            except AttributeError:
                value = value

            # If a value is a NaN, # or #QNaN return 0. This logic is being
            # logged for now and subsequent analysis of the logs will determine
            # whether it can be gotten rid of completely.
            if _isNumber(value):
                columnValues.append(value)
            else:
                LOGGER.warning('WARNING: Converting a NaN or # to zero: %s for %s' % (
                    columnName, rowName))
                columnValues.append(0)

        valueDictionary[rowName] = columnValues
        instrumentIterator = instrumentIterator.NextSibling()
    calculationSpace.RemoveGlobalSimulation('Valuation Date')
    calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    if setPrevBusDay:
        calculationSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    if inCurrency:
        calculationSpace.RemoveGlobalSimulation('Position Currency Choice')
        calculationSpace.RemoveGlobalSimulation('Fixed Currency')


    return valueDictionary


def TradingManagerSweeperBreakdown(query_folder, date, instrument_type, column_names, set_prev_bus_day=False, grouper=None,
                                   inCurrency="ZAR"):
    calc_space = CalculationSpace.from_source(query_folder, grouper=grouper)
    calc_space.simulate_value('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.simulate_value('Portfolio Profit Loss End Date Custom', date)
    calc_space.simulate_value('Valuation Date', date)
    calc_space.simulate_value('Position Currency Choice', 'Instrument Curr')

    if inCurrency:
        calc_space.simulate_value('Position Currency Choice', 'Fixed Curr')
        calc_space.simulate_value('Fixed Currency', inCurrency)

    if set_prev_bus_day:
        calc_space.simulate_value('Portfolio Profit Loss Start Date', 'PrevBusDay')

    result = defaultdict(list)
    for ins_type, instruments in calc_space.iteritems():
        if ins_type != instrument_type:
            continue
        for ins_name, cell in instruments.iteritems():
            for column_id in column_names:
                value = cell.calc_space.CalculateValue(cell.node.Tree(), column_id)
                if hasattr(value, 'Number'):
                    value = value.Number()
                result[ins_name].append(value)
    return result


def GetOvernightFundingRate(fundingIndex, date, longShort):
    ''' Get the fund rate for a particular date from a given spread index
    '''
    market = acm.FParty['internal']
    underlyingInstrument = fundingIndex.Underlying()
    underlyingPrice = PS_Functions.GetInstrumentPrice(underlyingInstrument, date, market)

    if underlyingPrice:
        underlyingSettle = underlyingPrice.Settle()
    else:
        underlyingSettle = 0

    spreadPrice = PS_Functions.GetInstrumentPrice(fundingIndex, date, market)
    spread = 0
    if spreadPrice:
        if longShort == 'Long':
            try:
                spread = spreadPrice.Bid()
            except AttributeError:
                spread = 0
        elif longShort == 'Short':
            try:
                spread = spreadPrice.Ask()
            except AttributeError:
                spread = 0

    if _isNumber(spread):
        return underlyingSettle + spread
    else:
        return underlyingSettle

def GetShortFundingRate(portfolioSwap, instrument, date):
    shortFundingType = portfolioSwap.add_info('PSShortPremiumType')
    fundingRate = 0.0

    if shortFundingType == 'Fixed':
        fundingRate = PS_TimeSeriesFunctions.GetShortPremiumRate(portfolioSwap, date)
    elif shortFundingType == 'Float':
        # Get the short rate from an index mapped to the instrument to be funded
        fundingIndexName = instrument.add_info('PSShortPremCost')
        if fundingIndexName:
            fundingIndex = acm.FInstrument[fundingIndexName]
            market = acm.FParty['internal']
            indexPrice = PS_Functions.GetInstrumentPrice(fundingIndex, date, market)
            if indexPrice:
                # The Fixed Funding Rate represents the spread to be added to the short rate
                shortSpread = PS_TimeSeriesFunctions.GetShortPremiumRate(portfolioSwap, date)
                fundingRate = indexPrice.Settle() + shortSpread

    return fundingRate

def _readDefaultExtensionAttribute(obj, extensionAttribute):
    defaultContext = acm.GetDefaultContext()
    evaluator = acm.GetCalculatedValue(obj, defaultContext, extensionAttribute)
    if not evaluator:
        raise Exception('Could not load extension attribute [%s]' % extensionAttribute)
    else:
        return evaluator.Value()

def _IsOvernightSpreadInstrument(instrument):
    ''' Check to see if an instrument is an overnight spread instrument, in which case the funding
        spread is selected according to the sign of total val start.
    '''
    extensionAttribute = 'isOvernightSpreadInstrument'
    try:
        return _readDefaultExtensionAttribute(instrument, extensionAttribute)
    except Exception as ex:
        raise Exception('Could not get isOvernightSpreadInstrument for instrument %s, extension attribute [%s]: %s' % \
                        (instrument.Name(), extensionAttribute, ex))

def FundingQuery(portfolio, currency="ZAR"):
    """ Generate query folder to be used by the TradingManagerSweeper to calculate ValEnd which will be used for funding.
    Exchange traded options and futures are excluded from the query folder as they will not have funding.
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    ApplyFundingRestriction(query)
    return query


def ApplyFundingRestriction(query):
    or_node = query.AddOpNode('OR')
    or_node.AddAttrNode('Instrument.Otc', 'EQUAL', True)
    and_node = or_node.AddOpNode('AND')
    and_node.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', 'Option')
    and_node.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', 'Future/Forward')


def update_with_zero_values(total_funding, portfolioSwap, date, reporting_portfolio=None):
    for ins_type, data in sweep_zero_values(portfolioSwap, date, "Float", "Funding", reporting_portfolio).items():
        total_funding[ins_type].update(data)


def CalculateFundingRate(pswap, ins, val_end, funding_index, prev_bank_day):
    if val_end < 0:
        funding_rate = GetOvernightFundingRate(funding_index, prev_bank_day, 'Short')
        if ins.InsType() in ['Stock', 'Bond', 'ETF']:
            short_rate = GetShortFundingRate(pswap, ins, prev_bank_day)
            funding_rate = funding_rate - short_rate
    else:
        funding_rate = GetOvernightFundingRate(funding_index, prev_bank_day, 'Long')
    return funding_rate


def GenerateFunding(portfolio_swap, date):
    # Add funding resets for date. In the case of new trades first generate legs and cashflows if necessary.
    total_funding = defaultdict(dict)

    if CALENDAR.IsNonBankingDay(None, None, date):
        LOGGER.info("{} is a non-banking day, funding calculation skipped".format(date))
        return total_funding

    trade = PS_Functions.get_instrument_trade(portfolio_swap)
    reporting_portfolio = PS_Functions.get_pb_reporting_portfolio(trade.Counterparty())
    is_fully_funded = PS_Functions.get_pb_pswap_ff_flag(portfolio_swap)
    if is_fully_funded:
        LOGGER.info("No funding is charged on fully-funded pswap {}".format(portfolio_swap.Name()))
        update_with_zero_values(total_funding, portfolio_swap, date, reporting_portfolio)
        return total_funding

    sweeping_class = portfolio_swap.AdditionalInfo().PB_Sweeping_Class()
    funding_index = acm.FInstrument[portfolio_swap.AdditionalInfo().PSONPremIndex().Name()]
    LOGGER.info("Sweeping class: {}, funding index: {}, fully-funded: {}"
                .format(sweeping_class, funding_index.Name(), is_fully_funded))

    # Generate query folder to be used by the TradingManagerSweeper to calculate ValEnd for previous_banking_day.
    query_folder = acm.FStoredASQLQuery[sweeping_class]
    if query_folder is None:
        LOGGER.warning("Skipping portfolio swap {} with sweeping class {}".format(portfolio_swap.Name(), sweeping_class))
        update_with_zero_values(total_funding, portfolio_swap, date, reporting_portfolio)
        return total_funding
    query = query_folder.Query()
    query = PS_Functions.modify_asql_query(
        query,
        "Portfolio.Name",
        False,
        new_value=reporting_portfolio.Name())
    if is_fully_funded:
        query = PS_Functions.add_ff_flag_to_query(query)
    if portfolio_swap.Currency().Name() != "ZAR":
        LOGGER.info("Non ZAR portfolio swap; searching for trades with currency  {}".format(portfolio_swap.Currency().Name()))
        query = PS_Functions.add_currency_to_query(query, portfolio_swap.Currency().Name())
    ApplyFundingRestriction(query)
    nr_of_trades = len(query.Select())
    LOGGER.info("Trades found: {}".format(nr_of_trades))
    if not nr_of_trades:
        update_with_zero_values(total_funding, portfolio_swap, date, reporting_portfolio)
        return total_funding

    trans = FundingSweeper_transaction(portfolio_swap)
    previous_banking_day = CALENDAR.AdjustBankingDays(date, -1)
    start_date = acm.Time().DateAddDelta(previous_banking_day, 0, 0, 1)
    end_date = acm.Time().DateAddDelta(date, 0, 0, 1)
    instrument_val_ends = TradingManagerSweeper(query, previous_banking_day, ["Portfolio Value End"], False)
    for ins, val_end_list in instrument_val_ends.iteritems():
        # Only add a reset if it is non-zero.
        val_end = val_end_list[0]
        instrument = acm.FInstrument[ins]
        instrument_type = instrument.InsType()

        # BSB's will be booked into the same portfolio as bonds and their funding will be built
        # into the funding rates for the bond positions.
        if val_end and instrument_type not in ['BuySellback', 'Repo/Reverse']:
            leg = GetLeg(portfolio_swap, 'Float', instrument)
            if not leg:
                leg = CreateLeg(portfolio_swap, 'Float', instrument, start_date, end_date, funding_index)

            cash_flow = GetFloatCashFlow(leg, 'Funding')
            if not cash_flow:
                cash_flow = CreateCashFlow(leg, 'Float Rate', start_date, end_date, None, None, 'Funding')
            else:  # Upgrade2018
                if cash_flow.AdditionalInfo().PS_FundWarehouse() != "Funding":
                    cash_flow.AddInfoValue('PS_FundWarehouse', "Funding")
                    cash_flow.Commit()
                    two_days_ago = CALENDAR.AdjustBankingDays(previous_banking_day, -1)
                    start_date_first_reset = acm.Time().DateAddDelta(two_days_ago, 0, 0, 1)
                    end_date_first_reset = acm.Time().DateAddDelta(previous_banking_day, 0, 0, 1)
                    CreateReset(cash_flow, 'Return', previous_banking_day,
                                start_date_first_reset, end_date_first_reset, 0.0)
                    for reset in cash_flow.Resets()[:]:
                        if reset.ResetType() in ("Nominal Scaling", "Simple Overnight"):
                            reset.Delete()

            trans.ExtendLeg(leg, end_date)
            trans.ExtendCashFlow(cash_flow, end_date)

            funding_rate = CalculateFundingRate(portfolio_swap, instrument, val_end, funding_index, previous_banking_day)
            value = acm.Time().DateDifference(end_date, start_date) * funding_rate * val_end / PS_FundingCalculations.DAYS_PERCENT
            reset = PS_FundingCalculations.GetReset(cash_flow, 'Return', date, True)
            if reset:
                trans.DeleteReset(reset)
            prev_reset = PS_FundingCalculations.GetReset(cash_flow, 'Return', previous_banking_day, False, True)
            if prev_reset:
                value += prev_reset.FixingValue()
            trans.CreateReset(cash_flow, 'Return', date, start_date, end_date, value)
            msg = """Created a funding reset with the following data:
                     Reset Date:{0}
                     Previous Banking Day:{1}
                     Instrument:{2}
                     Instrument Type:{3}
                     ValEnd:{4}
                     Funding Rate:{5}
                     Value:{6}""".format(date, previous_banking_day, instrument.Name(),
                                         instrument.InsType(), val_end, funding_rate, value)
            LOGGER.info(msg)
            total_funding[instrument.InsType()][instrument.Name()] = value
    trans.Commit()

    update_with_zero_values(total_funding, portfolio_swap, date, reporting_portfolio)
    return total_funding


def has_non_voided_trades(all_phys_pf, instrument_name,  sweeping_class):
    if sweeping_class != "CFDs" and all_phys_pf:
        query_folder = acm.CreateFASQLQuery("FTrade", "AND")
        query_folder.AddAttrNode("Instrument.Name", "EQUAL", instrument_name)
        query_folder.AddAttrNodeString("Portfolio.Name", [pf.Name() for pf in all_phys_pf],
                                       "EQUAL")
        query_folder.AddAttrNode("Status", 'NOT_EQUAL',
                                 acm.EnumFromString('TradeStatus', 'Void'))
        if query_folder.Select().Size() == 0:
            LOGGER.info("There are only voided trades on instrument {}".format(instrument_name))
            return False
    return True


def sweep_zero_values(portfolio_swap, date, leg_type, cash_flow_type, reporting_portfolio=None):
    zero_funding = defaultdict(dict)
    trans = FundingSweeper_transaction(portfolio_swap)
    previous_banking_day = CALENDAR.AdjustBankingDays(date, -1)
    start_date = acm.Time().DateAddDelta(previous_banking_day, 0, 0, 1)
    end_date = acm.Time().DateAddDelta(date, 0, 0, 1)
    sweeping_class = portfolio_swap.AdditionalInfo().PB_Sweeping_Class()
    all_phys_pf = None
    if reporting_portfolio:
        if reporting_portfolio.Compound():
            all_phys_pf = reporting_portfolio.AllPhysicalPortfolios()
        else:
            all_phys_pf = [reporting_portfolio]
    for leg in portfolio_swap.Legs():
        if leg.LegType() == leg_type:
            cash_flow = GetFloatCashFlow(leg, cash_flow_type)
            if cash_flow:
                # Applies for: provision, new funding method; doesn't apply for old funding method
                resets = cash_flow.Resets()
                if resets:
                    instrument = leg.IndexRef()
                    instrument_name = instrument.Name()
                    instrument_type = instrument.InsType()
                    reset_type = cash_flow.Resets()[0].ResetType()
                    if reset_type in ("Nominal Scaling", "Simple Overnight"):
                        LOGGER.warning("Invalid reset on {}".format(instrument_name))
                        continue

                    trans.ExtendLeg(leg, end_date)
                    trans.ExtendCashFlow(cash_flow, end_date)
                    reset = PS_FundingCalculations.GetReset(cash_flow, 'Return', date, True)
                    if not reset:
                        fixing_value = 0.0
                        # If there are only voided trades, set the reset to 0.0.
                        # Otherwise set it to be equal to the previous one.
                        if sweeping_class == "CFDs" or has_non_voided_trades(all_phys_pf, instrument_name,
                                                                             sweeping_class):
                            prev_reset = PS_FundingCalculations.GetReset(cash_flow, 'Return', date, False, True)
                            if prev_reset:
                                fixing_value = prev_reset.FixingValue()
                        trans.CreateReset(cash_flow, 'Return', date, start_date, end_date, fixing_value)
                        msg = """Created a {0} reset with 0.0 daily value:
                                 Reset Date:{1}
                                 Previous Banking Day:{2}
                                 Instrument:{3}
                                 Instrument Type:{4}
                                 Value:{5}""".format(cash_flow_type, date, previous_banking_day,
                                                     instrument_name, instrument_type, fixing_value)
                        LOGGER.info(msg)
                    else:
                        fixing_value = reset.FixingValue()
                        msg = """A {0} reset with 0.0 daily value already exists:
                                 Instrument:{1}
                                 Instrument Type:{2}
                                 Value:{3}""".format(cash_flow_type, instrument_name,
                                                     instrument_type, fixing_value)
                        LOGGER.info(msg)
                    zero_funding[instrument_type][instrument_name] = fixing_value
    trans.Commit()
    return zero_funding


def WarehousingQuery(portfolio):
    # Generate query folder to be used by the TradingManagerSweeper to calculate Warehousing Nominal.
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    orNode = query.AddOpNode('OR')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Bond')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'FRA')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Swap')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Cap')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Floor')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'BuySellback')
    orNode.AddAttrNode('Instrument.InsType', 'EQUAL', 'Repo/Reverse')
    # Select OTC Futures
    andNodeFuture = orNode.AddOpNode('AND')
    andNodeFuture.AddAttrNode('Instrument.InsType', 'EQUAL', 'Future/Forward')
    andNodeFuture.AddAttrNode('Instrument.Otc', 'EQUAL', True)
    # Select OTC Options
    andNodeOption = orNode.AddOpNode('AND')
    andNodeOption.AddAttrNode('Instrument.InsType', 'EQUAL', 'Option')
    andNodeOption.AddAttrNode('Instrument.Otc', 'EQUAL', True)
    return query

def GenerateWarehousing(portfolioSwap, date):
    ''' Add warehousing resets for each day between StartDate and EndDate.  In the case of new positions
        first generate legs and cashflows.
    '''
    trans = FundingSweeper_transaction(portfolioSwap)
    portfolio = portfolioSwap.FundPortfolio()
    fundingIndex = acm.FInstrument[portfolioSwap.add_info('PSONPremIndex')]

    # Generate query folder to be used by the TradingManagerSweeper to calculate Warehousing Nominal.
    query = WarehousingQuery(portfolio)

    if not CALENDAR.IsNonBankingDay(None, None, date):
        previousBankingDay = CALENDAR.AdjustBankingDays(date, -1)
        startDate = acm.Time().DateAddDelta(previousBankingDay, 0, 0, 1)
        endDate = acm.Time().DateAddDelta(date, 0, 0, 1)

        instrumentWarehousingNominal = TradingManagerSweeper(query, date, ['Warehousing Nominal'], False)
        for ins, nominalList in instrumentWarehousingNominal.iteritems():
            nominal = nominalList[0]
            if nominal:
                instrument = acm.FInstrument[ins]

                leg = GetLeg(portfolioSwap, 'Float', instrument)
                if not leg:
                    leg = CreateLeg(portfolioSwap, 'Float', instrument, startDate, endDate, fundingIndex)

                cashFlow = GetFloatCashFlow(leg, 'Warehousing')
                if not cashFlow:
                    cashFlow = CreateCashFlow(leg, 'Float Rate', startDate, endDate, None, None, 'Warehousing')

                trans.ExtendLeg(leg, endDate)
                trans.ExtendCashFlow(cashFlow, endDate)

                nominalReset = PS_FundingCalculations.GetReset(cashFlow, 'Nominal Scaling', startDate, True)
                if nominalReset:
                    trans.DeleteReset(nominalReset)
                trans.CreateReset(cashFlow, 'Nominal Scaling', date, startDate, endDate, nominal)

                warehousingRate = PS_TimeSeriesFunctions.GetWarehousingRate(portfolio, date)
                simpleReset = PS_FundingCalculations.GetReset(cashFlow, 'Simple Overnight', startDate, True)
                if simpleReset:
                    trans.DeleteReset(simpleReset)
                trans.CreateReset(cashFlow, 'Simple Overnight', date, startDate, endDate, warehousingRate)

                msg = """Created warehousing resets with the following data:
                         Reset Date{0}
                         Instrument:{1}
                         Instrument Type:{2}
                         Nominal:{3}
                         Warehousing Rate:{4}""".format(date, instrument.Name(), instrument.InsType(),
                                                        nominal, warehousingRate)
                LOGGER.info(msg)

    trans.Commit()


def GenerateProvision(portfolioSwap, date):
    '''Generate the provision on the Portfolio Swap,
       the provision is calculated from the Portfolio Swap start date.
    '''
    trans = FundingSweeper_transaction(portfolioSwap)
    trade = PS_Functions.get_instrument_trade(portfolioSwap)
    portfolio = PS_Functions.get_pb_reporting_portfolio(trade.Counterparty())

    total_provision = defaultdict(dict)

    sweeping_class = portfolioSwap.AdditionalInfo().PB_Sweeping_Class()
    LOGGER.info(sweeping_class)
    if sweeping_class == "Unknown":
        LOGGER.info("Skipping portfolio swap {0} with sweeping class 'Unknown'".format(portfolioSwap.Name()))
    else:
        # Generate query folder to be used by the TradingManagerSweeper to calculate Provisioning.
        query_folder = acm.FStoredASQLQuery[sweeping_class]
        query = query_folder.Query()
        query = PS_Functions.modify_asql_query(
            query,
            "Portfolio.Name",
            False,
            new_value=portfolio.Name())
        if portfolioSwap.Currency().Name() != "ZAR":
            LOGGER.info("Non ZAR pswap; searching for trades with currency: {0}".format(portfolioSwap.Currency().Name()))
            query = PS_Functions.add_currency_to_query(query, portfolioSwap.Currency().Name())
        LOGGER.info("Trades found: %s" % len(query.Select()))

        provision_column = ["Provision"]

        # Use PBA column if grouper is used and top level values are converted
        # from instrument's currency to "ZAR"
        # if portfolioSwap.Currency().Name() != "ZAR":
        #    provision_column = ["PBA Provision"]

        # It is necessary to use a clone,
        # because otherwise the query folder stays modified in memory.
        qf_clone = query_folder.Clone()
        qf_clone.Query(query)

        if not CALENDAR.IsNonBankingDay(None, None, date):
            previousBankingDay = CALENDAR.AdjustBankingDays(date, -1)
            startDate = acm.Time().DateAddDelta(previousBankingDay, 0, 0, 1)
            endDate = acm.Time().DateAddDelta(date, 0, 0, 1)

            instrumentProvision = TradingManagerSweeper(qf_clone, date, provision_column, False)
            for ins, provisionList in instrumentProvision.iteritems():
                provision = provisionList[0]
                if provision:
                    instrument = acm.FInstrument[ins]

                    leg = GetLeg(portfolioSwap, 'Total Return', instrument)
                    if not leg:
                        leg = CreateLeg(portfolioSwap, 'Total Return', instrument, startDate, endDate, None)

                    cashFlow = GetReturnCashFlow(leg, 'Provision')
                    if not cashFlow:
                        cashFlow = CreateCashFlow(leg, 'Position Total Return', startDate, endDate, None, None, 'Provision')

                    trans.ExtendLeg(leg, endDate)
                    trans.ExtendCashFlow(cashFlow, endDate)

                    reset = PS_FundingCalculations.GetReset(cashFlow, 'Return', startDate, True)
                    if reset:
                        trans.DeleteReset(reset)
                    trans.CreateReset(cashFlow, 'Return', date, startDate, endDate, provision)

                    msg = """Created provision resets with the following data:
                             Reset Date:{0}
                             Previous Banking Day:{1}
                             Instrument:{2}
                             Instrument Type:{3}
                             Provision:{4}""".format(date, previousBankingDay, instrument.Name(),
                                                     instrument.InsType(), provision)
                    LOGGER.info(msg)
                    total_provision[instrument.InsType()][instrument.Name()] = provision

        trans.Commit()
    # Provision is 0 for expired/closed out trades, so it doesn't need to be tracked, i.e. sweep_zero_values not needed
    return total_provision


def GenerateTotalTPL(portfolioSwap, date):
    ''' Add a TPL from inception reset for each position that include new trades
        traded on the date.  In the case where a cashflow or leg doesn't exist
        create them.  This value will get used to lookup yesterdays TPL when
        sweeping to the call account.  Yesterdays TPL can't be recalculated by
        backdating trading manager, because the yield curves wont be the same.
    '''
    trans = FundingSweeper_transaction(portfolioSwap)
    trade = PS_Functions.get_instrument_trade(portfolioSwap)
    portfolio = PS_Functions.get_pb_reporting_portfolio(trade.Counterparty())

    sweeping_class = portfolioSwap.AdditionalInfo().PB_Sweeping_Class()
    LOGGER.info("Sweeping class:%s" % sweeping_class)

    total_tpl = defaultdict(dict)

    # If a portfolio is fully funded we'll sweep the difference in cash (buy/sell price, dividends and execution fees
    is_fully_funded = PS_Functions.get_pb_pswap_ff_flag(portfolioSwap)
    if is_fully_funded:
        tplColumns = ['Portfolio Cash End']
    else:
        tplColumns = ['Client TPL']

    if sweeping_class == "Unknown":
        LOGGER.info("Skipping portfolio swap {0} with sweeping class 'Unknown'".format(portfolioSwap.Name()))
    else:
        # Generate query folder to be used by the trading manager sweeper
        # to calculate execution premiums
        query_folder = acm.FStoredASQLQuery[sweeping_class]
        query = query_folder.Query()
        query = PS_Functions.modify_asql_query(
            query,
            "Portfolio.Name",
            False,
            new_value=portfolio.Name())
        if is_fully_funded:
            query = PS_Functions.add_ff_flag_to_query(query)
        if portfolioSwap.Currency().Name() != "ZAR":
            LOGGER.info("Non ZAR pswap; searching for trades with currency:%s" % portfolioSwap.Currency().Name())
            query = PS_Functions.add_currency_to_query(query, portfolioSwap.Currency().Name())
        LOGGER.info("Trades found:%s" % len(query.Select()))

        # It is necessary to use a clone,
        # because otherwise the query folder stays modified in memory.
        qf_clone = query_folder.Clone()
        qf_clone.Query(query)

        if not CALENDAR.IsNonBankingDay(None, None, date):
            previousBankingDay = CALENDAR.AdjustBankingDays(date, -1)
            startDate = acm.Time().DateAddDelta(previousBankingDay, 0, 0, 1)
            endDate = acm.Time().DateAddDelta(date, 0, 0, 1)

            instrumentTotalTPL = TradingManagerSweeper(qf_clone, date, tplColumns, False)
            for ins, totalTPLList in instrumentTotalTPL.iteritems():
                totalTPL = totalTPLList[0]
                instrument = acm.FInstrument[ins]

                leg = GetLeg(portfolioSwap, 'Total Return', instrument)
                if not leg:
                    leg = CreateLeg(portfolioSwap, 'Total Return', instrument, startDate, endDate, None)

                cashFlow = GetReturnCashFlow(leg, 'TPL')
                if not cashFlow:
                    cashFlow = CreateCashFlow(leg, 'Position Total Return', startDate, endDate, None, None, 'TPL')
                else:  # Upgrade2018
                    cashFlow.CashFlowType("Position Total Return")
                    cashFlow.AddInfoValue('PS_FundWarehouse', "TPL")
                    cashFlow.Commit()

                trans.ExtendLeg(leg, endDate)
                trans.ExtendCashFlow(cashFlow, endDate)

                reset = PS_FundingCalculations.GetReset(cashFlow, 'Return', date, True)
                if reset:
                    trans.DeleteReset(reset)
                trans.CreateReset(cashFlow, 'Return', date, startDate, endDate, totalTPL)
                
                msg = """Created TPL resets with the following data:
                         Reset Date:{0}
                         CF End Date:{1}
                         Instrument:{2}
                         Instrument Type:{3}
                         TPL:{4}
                         Columns:{5}""".format(date, endDate, instrument.Name(), instrument.InsType(),
                                               totalTPL, tplColumns)
                total_tpl[instrument.InsType()][instrument.Name()] = totalTPL
                LOGGER.info(msg)

    trans.Commit()
    return total_tpl
