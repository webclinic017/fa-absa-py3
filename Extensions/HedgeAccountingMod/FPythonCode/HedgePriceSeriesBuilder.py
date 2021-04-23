'''
===================================================================================================
PURPOSE: The HedgePriceSeriesBuilder class contains the business logic to build and prepare the
            data series to be used in the Hedge Effectiveness testing. Refer to the product
            documentation for specific business logic rules and methodolgy used for building the
            data series.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

import time

import acm
import FLogger

import HedgeConstants
import HedgeUtils
import HedgeTimeBucketUtils

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


def functiontimer(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('Function: %r took %2.4f seconds to execute.' % (f.__name__, te - ts))
        return result
    return timed


class price_delta_builder(object):
    '''Class to represent the historical deltas used in the effectiveness tests.
        Inputs: The two trades for which the deltas are to be calculated.
    '''

    def __init__(self, hedge_relation):
        '''
        trades: Dict {strTradeOid: [hedgeType, percentage, childTradeOid]}
                    e.g.
                        {'54581839': ['External', '100', 54584586],
                        '54588237': ['External', '100', 54581237]}

        hedgeDesignationDate [string/dateTime] - The Hedge Relationship designation date:
            eg. '2015/03/01'
        '''

        self.trade_dict = hedge_relation.get_trades()
        self.hedge_relation = hedge_relation
        self.hedge_curve_clone_name = self.hedge_relation.get_file_name()

        self.hedgeDesignationDate = hedge_relation.get_start_date()

        self.standardCalcSpace = acm.FCalculationMethods().\
            CreateStandardCalculationsSpaceCollection()

        self.tag = acm.GetGlobalEBTag()
        self.context = acm.GetDefaultContext()
        self.all_benchmark_curves = set()

        self.marketValueSeries_Original = {}
        self.marketValueSeries_External = {}
        self.marketValueDeltaSeries_Original = {}
        self.marketValueDeltaSeries_External = {}

        self.simulated_prices = []
        self.date_series = []

        self.lastMarket = HedgeConstants.STR_LAST_PRICE_MARKET
        self.mtmMarket = HedgeConstants.STR_MTM_PRICE
        self.mtmPriceMarket = HedgeConstants.STR_MTM_PRICE_MARKET

        self.sheet_type = HedgeConstants.STR_TRADE_SHEET
        self.tradeSheetCalcSpace = acm.Calculations().CreateCalculationSpace(self.context,
                                                                             self.sheet_type)

    def clear_all_series(self):
        '''Clear all data containers
        '''

        # clear dictionaries
        self.marketValueSeries_Original.clear()
        self.marketValueSeries_External.clear()
        self.marketValueDeltaSeries_Original.clear()
        self.marketValueDeltaSeries_External.clear()

        # clear list collections
        del self.date_series[:]
        del self.simulated_prices[:]

    def get_sorted_date_range(self):
        '''Returns a sorted range of dates that corresponds to the delta value series.
        '''

        sortedDateRange = sorted(self.marketValueSeries_Original.keys())
        return sortedDateRange

    def value_trades(self, simulationDate, valuationDate):
        '''Value trades in the hedge relationship.
            1. Instruments that pull prices from the Market-to-Market feed will be valued
                by retrieving the Market Value
            2. Other Instruments will be valued by calculating the Theoretical Value (PV)

        simulationDate [date] - the date used in the price simulation

        testDate [date] - valuation date
        '''

        for tradeOid in self.trade_dict.keys():
            m_type, _, childTradeId = self.trade_dict[tradeOid]
            testTrade = None

            if m_type == HedgeConstants.Hedge_Trade_Types.External:
                testTrade = acm.FTrade[childTradeId]

            elif m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
                testTrade = acm.FTrade[tradeOid]

            if testTrade:
                trade_value = 0

                self.tradeSheetCalcSpace.SimulateValue(testTrade, 'Valuation Date',
                                                       acm.Time().DateNow())

                trade_value = self.tradeSheetCalcSpace.\
                    CreateCalculation(testTrade,
                                      'Portfolio Clean PnL').Value().Number()
                trade_currency = testTrade.Currency().Name()

            # Convert non-ZAR series to ZAR for NIH.
            if (self.hedge_relation.get_type() == 'Net Investment Hedge')\
               and (trade_currency != 'ZAR'):
                trade_value = HedgeUtils.convert_currencies(trade_value,
                                                            simulationDate,
                                                            acm.FInstrument[str(trade_currency)],
                                                            acm.FInstrument['ZAR'])

            if m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
                if simulationDate in self.marketValueSeries_Original:
                    self.marketValueSeries_Original[simulationDate] += trade_value
                else:
                    self.marketValueSeries_Original[simulationDate] = trade_value

            elif m_type == HedgeConstants.Hedge_Trade_Types.External:
                if simulationDate in self.marketValueSeries_External:
                    self.marketValueSeries_External[simulationDate] += trade_value
                else:
                    self.marketValueSeries_External[simulationDate] = trade_value

    def calculate_price_delta(self):
        '''Calculate & populate the delta series from the value series
        '''

        if len(self.marketValueSeries_Original.keys())\
           != len(self.marketValueSeries_External.keys()):
            logger.ELOG('Price pairs are not available for all dates. '
                        'Hedge testing is therefore not possible.')
            return

        sortedDateRange = self.get_sorted_date_range()

        i = 1
        while i < len(sortedDateRange):

            date = sortedDateRange[i]
            previousDatePoint = sortedDateRange[i-1]

            self.marketValueDeltaSeries_Original[date] = \
                self.marketValueSeries_Original[date] - \
                self.marketValueSeries_Original[previousDatePoint]

            self.marketValueDeltaSeries_External[date] = \
                self.marketValueSeries_External[date] - \
                self.marketValueSeries_External[previousDatePoint]
            i += 1

    def calculate_curves(self):
        '''Recalculate all the touched benchmark yield curves
        '''
        for yield_curve in self.all_benchmark_curves:
            yield_curve.Simulate()
            yield_curve.Calculate()

    def undo_sim(self):
        '''Undo the price simulations
        '''
        while self.simulated_prices:
            price = self.simulated_prices[0]
            price.Undo()
            price.Unsimulate()

            # remove 'un-simulated' price from simulated prices list
            self.simulated_prices.pop(0)

        for curve in self.all_benchmark_curves:
            curve.Undo()
            curve.Unsimulate()

    def insert_retrospective_points(self):
        '''Method that will insert two Retrospective Market Values in the value
            series if sufficient Market Values are available.

        designationDate [datetime] - Hedge Relationship designation date
        '''

        designationDate = self.hedgeDesignationDate

        dateRange = self.get_sorted_date_range()

        if len(dateRange) > 2:
            timeBucketLatestDate = dateRange[len(dateRange)-1]
            timeBucketSecondLatestDate = dateRange[len(dateRange)-2]

            if designationDate < timeBucketSecondLatestDate:
                # remove first two simulated elements and replace with actual Market Values
                del self.marketValueSeries_Original[timeBucketLatestDate]
                del self.marketValueSeries_External[timeBucketLatestDate]

                del self.marketValueSeries_External[timeBucketSecondLatestDate]
                del self.marketValueSeries_Original[timeBucketSecondLatestDate]

                # Get Market to Market values and set in Value series
                self.get_set_trade_marketvalue(timeBucketSecondLatestDate)
                self.get_set_trade_marketvalue(timeBucketLatestDate)

            elif designationDate < timeBucketLatestDate:
                # remove first two simulated elements and replace with actual Market Values
                del self.marketValueSeries_Original[timeBucketLatestDate]
                del self.marketValueSeries_External[timeBucketLatestDate]

                del self.marketValueSeries_External[timeBucketSecondLatestDate]
                del self.marketValueSeries_Original[timeBucketSecondLatestDate]

                # Get Market to Market values and set in Value series
                self.get_set_trade_marketvalue(designationDate)
                self.get_set_trade_marketvalue(timeBucketLatestDate)

    def get_set_trade_marketvalue(self, valuationDate):
        '''Retrieve the Market Values for all trades in the global trade list
            on a specific date and add it to the aggregated value series.

        valuationDate [datetime] - date on which Market Value should be retrieved
        '''

        for tradeOid in self.trade_dict.keys():
            m_type, _, childTradeId = self.trade_dict[tradeOid]

            trade = None
            trade_value = None

            if m_type == HedgeConstants.Hedge_Trade_Types.External:
                trade = acm.FTrade[childTradeId]

            elif m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
                trade = acm.FTrade[tradeOid]

            # get & set the Market Value for all non-MtmFeed trades at designation date
            if trade:
                self.tradeSheetCalcSpace.SimulateValue(trade,
                                                       'Valuation Date',
                                                       valuationDate)

                trade_cleanPnL_calc = self.tradeSheetCalcSpace.\
                    CreateCalculation(trade,
                                      'Portfolio Clean PnL')

                
                if trade_cleanPnL_calc.Value():
                    trade_value = trade_cleanPnL_calc.Value().Number()
                else:   
                    trade_value = 0.0

                trade_currency = trade.Currency().Name()

            # Convert non-ZAR series to ZAR for NIH.
            if (self.hedge_relation.get_type() == 'Net Investment Hedge')\
               and (trade_currency != 'ZAR'):
                trade_value = HedgeUtils.convert_currencies(trade_value,
                                                            valuationDate,
                                                            acm.FInstrument[str(trade_currency)],
                                                            acm.FInstrument['ZAR'])

            # Insert Actual Market Values
            if m_type == HedgeConstants.Hedge_Trade_Types.Hypo:

                if valuationDate in self.marketValueSeries_Original:
                    self.marketValueSeries_Original[valuationDate] += trade_value
                else:
                    self.marketValueSeries_Original[valuationDate] = trade_value

            elif m_type == HedgeConstants.Hedge_Trade_Types.External:

                if valuationDate in self.marketValueSeries_External:
                    self.marketValueSeries_External[valuationDate] += trade_value
                else:
                    self.marketValueSeries_External[valuationDate] = trade_value

    def get_benchmarkcurves_from_trades(self):
        '''Retrieve all benchmark yield curves for all trades in the global trade list.
            All applicable yield curves are added to the global dictionary for benchmark
            curves to be used in the price simulations.
        '''

        # for trade in self.trades:
        for tradeOid in self.trade_dict.keys():

            trade = acm.FTrade[tradeOid]
            instr = trade.Instrument()

            # only simulate curves for instruments that does not pull Market-to-Market prices
            # from the market feeds.
            if not instr.MtmFromFeed():

                tradesBuilder = acm.Risk.\
                    CreateSingleInstrumentAndTradesBuilder(trade.Portfolio(),
                                                           trade.Instrument())
                sit = tradesBuilder.GetTargetInstrumentAndTrades()

                curve_or_curves = acm.GetCalculatedValueFromString(
                    sit,
                    self.context,
                    'benchmarkCurvesInThTPLAtValuationDate',
                    self.tag
                ).Value()

                if curve_or_curves:
                    if curve_or_curves.ClassName().AsString() in ('FVariantArray', 'FSet'):
                        for curve in curve_or_curves:
                            logger.LOG('%s of type %s found.' % (curve.Name(), curve.Type()))

                            curve_to_add = curve
                            if curve.DependencyCurve():
                                logger.LOG('Dependency curve found for %s curve, %s, using dependency curve %s of type %s instead.' % 
                                                (curve.Name(), curve.Type(), curve.DependencyCurve().Name(), curve.DependencyCurve().Type()))
                                curve_to_add = curve.DependencyCurve()
                                    
                            if curve_to_add not in self.all_benchmark_curves:
                                self.all_benchmark_curves.add(curve_to_add)
                    else:
                        logger.LOG('%s of type %s found.'
                                   % (curve_or_curves.Name(),
                                      curve_or_curves.Type()))

                        if curve_or_curves not in self.all_benchmark_curves:
                            self.all_benchmark_curves.add(curve_or_curves)
                else:
                    logger.WLOG("Benchmark curve for %s not found. [Trade:%s]"
                                % (sit, trade.Oid()))

    def get_price(self, date, benchmark, initialLookupMarket):
        '''Gets the price for a specific benchmark instrument on a specific date.

        date [datetime] - date for which to retrieve the price.
        '''

        benchmark_curr_name = benchmark.Currency().Name()

        query = "instrument = %d and market = '%s' and currency = '%s' and day = '%s'"\
                % (benchmark.Oid(), initialLookupMarket, benchmark_curr_name, date)

        historicPrice = acm.FPrice.Select(query)

        if historicPrice:
            historicPrice = historicPrice[0]
        else:
            # if no price is found, get the last price relative to the date
            closestPreviousPrice = self.get_closest_price(date, benchmark, HedgeConstants.STR_MTM_PRICE_MARKET)

            if not closestPreviousPrice:
                warningString = '--- Historical Price not found for %s for %s and market %s '\
                                'in %s, neither within acceptable range of previous '\
                                'dates. Attempting to retrieve price from the %s market.'\
                                % (benchmark.Name(),
                                   date,
                                   HedgeConstants.STR_MTM_PRICE_MARKET,
                                   benchmark_curr_name,
                                   HedgeConstants.STR_HE_Market)
                logger.WLOG(warningString)


                # if there are no more historical prices on the benchmark, look for a price 
                # in the Hedge Effectivness Test market to us in the simulation.
                hedgeMarketSimulatedPrice = self.get_closest_price(date, benchmark, HedgeConstants.STR_HE_Market)

                if not hedgeMarketSimulatedPrice:
                    warningString = '--- No Historical Price or Hedge Effectiveness Simualation Market Price '\
                                        'found for %s for %s and market %s '\
                                'in %s, neither within acceptable range of previous '\
                                'dates, not simulated'\
                                % (benchmark.Name(),
                                   date,
                                   HedgeConstants.STR_HE_Market,
                                   benchmark_curr_name)
                    logger.WLOG(warningString)

                    return None
                else:
                    warningString = '--- Using price from Hedge Effectiveness Simualation Market '\
                                            'for %s for %s and market %s in %s'\
                                    % (benchmark.Name(),
                                       date,
                                       HedgeConstants.STR_HE_Market,
                                       benchmark_curr_name)
                    logger.LOG(warningString)
                    
                    historicPrice = hedgeMarketSimulatedPrice

            else:
                if closestPreviousPrice.Day() != date:
                    warningString = '--- Historical price not found for %s for %s and market '\
                                    '%s in %s, using price for %s' \
                                    % (benchmark.Name(),
                                       date,
                                       HedgeConstants.STR_MTM_PRICE_MARKET,
                                       benchmark_curr_name,
                                       closestPreviousPrice.Day())
                    logger.WLOG(warningString)

                historicPrice = closestPreviousPrice

        return historicPrice

    def get_closest_price(self, date, benchmark, market):
        '''Get the previous price for a specific benchmark relative to a specific date.

        date [datetime] - Date from which to look for the latest previous price.
        '''

        benchmark_curr_name = benchmark.Currency().Name()
        price = None
        count = 0

        nearest_date = date

        while not price and count < HedgeConstants.INT_DEFAULT_DISTANCE:
            query = "instrument = %d and day = '%s' and market = '%s' and currency = '%s'" \
                    % (benchmark.Oid(), nearest_date,
                       market,
                       benchmark_curr_name)
            price = acm.FPrice.Select(query)

            if price:
                return price[0]

            count += 1
            nearest_date = acm.Time.DateAddDelta(date, 0, 0, (-1*count))

    def simulate_benchmark_prices(self, simulationDate, valuationDate):
        '''Simulate prices based on historic prices and benchmark yield curves applicable to the
            global tradelist.

        date [datetime] - date for which to retrieve a price to be used in the simulation.
        '''

        for yield_curve in self.all_benchmark_curves:
            missing_benchmarks = []

            for benchmark in yield_curve.BenchmarkInstruments():

                benchmark_curr_name = benchmark.Currency().Name()

                # get the current price (price on test date) to be replaced by the simulated
                # historic price as per time bucket dates

                currentPrice = acm.FPrice.Select(
                    "instrument = %d and market = '%s' and "
                    "currency = '%s'"
                    % (benchmark.Oid(),
                       self.mtmMarket,
                       benchmark_curr_name)
                ).SortByProperty("Day", True)

                # get the most recent price in the returend price collections
                if currentPrice:
                    currentPrice = currentPrice[-1]

                if currentPrice:
                    # get the rpice
                    historicPrice = self.get_price(simulationDate, benchmark,
                                                   HedgeConstants.STR_MTM_PRICE)

                    # simulate the test day price as the historic price.
                    if historicPrice:
                        simulateToPrice = historicPrice.\
                                                GetProperty(HedgeConstants.STR_MTM_PRICE_POSITION)
                        currentPrice.Bid(simulateToPrice)
                        currentPrice.Ask(simulateToPrice)
                        currentPrice.Last(simulateToPrice)
                        currentPrice.Settle(simulateToPrice)

                        self.simulated_prices.append(currentPrice)
                    else:
                        logger.WLOG('Removing benchmark %s from curve %s, no historic price '
                                    'found for date %s'
                                    % (benchmark.Name(),
                                       yield_curve.Name(),
                                       simulationDate))
                        missing_benchmarks.append(benchmark.Name())
                else:
                    errorMessage = '--- Price not found for %s for %s and market %s in %s.'\
                                   % (benchmark.Name(),
                                      simulationDate,
                                      HedgeConstants.STR_MTM_PRICE,
                                      benchmark.Currency().Name())
                    logger.ELOG(errorMessage)

                    raise Exception(errorMessage)

            if missing_benchmarks:
                self.remove_benchmarks(yield_curve, missing_benchmarks)

    def remove_benchmarks(self, yield_curve, missing_benchmarks):
        clone = acm.FBenchmarkCurve[self.hedge_curve_clone_name]
        if clone:
            clone.Delete()
        if isinstance(yield_curve, type(acm.FBenchmarkCurve())):
            clone = acm.FBenchmarkCurve()
        elif isinstance(yield_curve, type(acm.FSpreadCurve())):
            clone = acm.FSpreadCurve()
            clone.UnderlyingCurve(yield_curve.UnderlyingCurve())
        elif isinstance(yield_curve, type(acm.FInflationCurve())):
            clone = acm.FInflationCurve()
        clone.Name(self.hedge_curve_clone_name)
        clone.Commit()
        try:
            # add all benchmarks where we have found a historic price
            for ins in yield_curve.BenchmarkInstruments():
                if ins.Name() in missing_benchmarks:
                    continue
                clone.AddBenchmark(ins)

            # add a point for each instrument where we have found a historic price
            for point in yield_curve.Points():
                clonePoint = acm.FYieldPoint()
                clonePoint.Curve(clone.Oid())
                try:
                    if point.Instrument().Name() in missing_benchmarks:
                        continue
                except:
                    logger.LOG('Point with Oid %s has no associated instrument'
                               % point.Oid())
                    continue
                clonePoint.Instrument(point.Instrument())
                clonePoint.Commit()

            # 'clone' the rest of the curves properties
            clone.CalculationFormat(yield_curve.CalculationFormat())
            clone.ArchiveStatus(yield_curve.ArchiveStatus())
            clone.CompositeFunction(yield_curve.CompositeFunction())
            clone.ConflictInterval(yield_curve.ConflictInterval())
            clone.ConflictInterval2(yield_curve.ConflictInterval2())
            clone.Currency(yield_curve.Currency())
            clone.DualCalibrationMainCurve(yield_curve.DualCalibrationMainCurve())
            clone.EstimationFunction(yield_curve.EstimationFunction())
            clone.EstimationType(yield_curve.EstimationType())
            clone.ExtrapolationTypeLongEnd(yield_curve.ExtrapolationTypeLongEnd())
            clone.ExtrapolationTypeShortEnd(yield_curve.ExtrapolationTypeShortEnd())
            clone.ForwardPeriodCount(yield_curve.ForwardPeriodCount())
            clone.ForwardPeriodUnit(yield_curve.ForwardPeriodUnit())
            clone.HistoricalDay(yield_curve.HistoricalDay())
            clone.InterpolationFunction(yield_curve.InterpolationFunction())
            clone.InterpolationType(yield_curve.InterpolationType())
            clone.IpolRateType(yield_curve.IpolRateType())
            clone.IrFormat(yield_curve.IrFormat())
            clone.IsBidAsk(yield_curve.IsBidAsk())
            clone.IsYield(yield_curve.IsYield())
            clone.NextCurve(yield_curve.NextCurve())
            clone.OriginalCurve(yield_curve.OriginalCurve())
            clone.PayDayMethod(yield_curve.PayDayMethod())
            clone.PeriodConv(yield_curve.PeriodConv())
            clone.PeriodDaysOffset(yield_curve.PeriodDaysOffset())
            clone.Quotation(yield_curve.Quotation())
            clone.RealTimeUpdated(yield_curve.RealTimeUpdated())
            clone.RecoveryRate(yield_curve.RecoveryRate())
            clone.ReferenceDay(yield_curve.ReferenceDay())
            clone.RiskType(yield_curve.RiskType())
            clone.SpotDays(yield_curve.SpotDays())
            clone.StorageCalcType(yield_curve.StorageCalcType())
            clone.StorageCompoundingType(yield_curve.StorageCompoundingType())
            clone.StorageDayCount(yield_curve.StorageDayCount())
            clone.TextDataSize(yield_curve.TextDataSize())
            clone.UnderlyingCurve(yield_curve.UnderlyingCurve())
            clone.UpdateInterval(yield_curve.UpdateInterval())
            clone.UseBenchmarkDates(yield_curve.UseBenchmarkDates())

            # apply shortened curve
            clone.Name(yield_curve.Name())
            yield_curve.Apply(clone)

            # delete cloned curve
            clone.Name(self.hedge_curve_clone_name)
            clone.Delete()
        except:
            clone.Name(self.hedge_curve_clone_name)
            clone.Delete()
            raise

    def simulate_mtm_prices(self, mtmPriceDate, valuationDate):
        '''Retrieve the market-to-market price on a specific date for all instruments
            using the Market-to-Market feed.

        date [datetime] - date for which to retrieve the market-to-market price
        '''

        for tradeOid in self.trade_dict.keys():

            trade = acm.FTrade[tradeOid]

            instrument = trade.Instrument()

            if trade and instrument.MtmFromFeed():

                valueDayPrice = acm.FPrice.Select("instrument = %d and market = '%s' and "
                                                  "currency = '%s'"
                                                  % (instrument.Oid(),
                                                     HedgeConstants.STR_MTM_PRICE,
                                                     instrument.Currency().Name()))
                if valueDayPrice:
                    valueDayPrice = valueDayPrice[0]
                else:
                    valueDayPrice = acm.FPrice()
                    valueDayPrice.Day(valuationDate)

                simulateToPrice = instrument.MtMPrice(mtmPriceDate,
                                                      instrument.Currency().Name(),
                                                      0)

                valueDayPrice.Bid(simulateToPrice)
                valueDayPrice.Ask(simulateToPrice)
                valueDayPrice.Last(simulateToPrice)
                valueDayPrice.Settle(simulateToPrice)

                self.simulated_prices.append(valueDayPrice)

    def get_value_for_calculation(self, calcSpace, trade, column_id):
        '''Create and execute a calculation.

        calcSpace [FCalculationSpace] - calculation space to be used for calculation

        trade [FTrade] - trade on which to perform the calculation

        column_id [string] - column id to valuate

        return: [decimal] - calculation result value
        '''

        calculation = calcSpace.CreateCalculation(trade, column_id)
        try:
            return calculation.Value().Number()
        except:
            try:
                return calculation.Value()
            except:
                return None

    @functiontimer
    def build_simulated_price_series(self, timeBucketsName, testDate=acm.Time().DateNow()):
        '''Builds the simulated trade value and delta series to be used in
            Progressive Hedge Effectiveness tests

        timeBucketsName [string] - Name of the Time Bucket collection to use
                in the evaluations.

        testDate [string/dateTime] - The date on which the simulated tests shoud run.
                                    Tests can be back/forward dated. The default will
                                    be today's date. eg. '2015/06/03'
        '''

        # clear all data series
        self.clear_all_series()

        # Get applicable Yield-curves & benchmark instruments to use in simulated valuations
        self.get_benchmarkcurves_from_trades()

        # get date range from the time buckets
        dateRange = HedgeTimeBucketUtils.get_time_bucket_dates(timeBucketsName, testDate)

        for simulationPointDate in sorted(dateRange):

            # Simulate prices from curves for non MTM-feed instruments
            self.simulate_benchmark_prices(simulationPointDate, testDate)
            self.calculate_curves()

            # Retrieve & simulate for MTM-feed instruments
            self.simulate_mtm_prices(simulationPointDate, testDate)

            # value trades
            self.value_trades(simulationPointDate, testDate)

            self.date_series.append(simulationPointDate)

            # undo simulated price
            self.undo_sim()

        # cleanup
        self.calculate_curves()

        # insert 1 retrospective data points for prospective series if possible
        self.insert_retrospective_points()

        self.calculate_price_delta()

    @functiontimer
    def build_retrospective_price_series(self, timeBucketsName, testDate=acm.Time().DateNow()):
        '''Builds the Market Value and delta series to be used in
            Regression Hedge Effectiveness tests.

        timeBucketsName [string] - Name of the Time Bucket collection to use
                in the evaluations.

        testDate [string/dateTime] - The date on which the simulated tests shoud run.
                                    Tests can be back/forward dated. The default will
                                    be today's date. eg. '2015/06/03'
        '''

        self.clear_all_series()

        # get date range from the time buckets
        dateRange = HedgeTimeBucketUtils.get_retrospective_dates_sorted(timeBucketsName,
                                                                        self.hedgeDesignationDate,
                                                                        testDate)

        for simulationPointDate in sorted(dateRange):
            # Get historic price from Price table
            self.get_set_trade_marketvalue(simulationPointDate)
            self.date_series.append(simulationPointDate)

        # calculate the Price Delta Series
        self.calculate_price_delta()
