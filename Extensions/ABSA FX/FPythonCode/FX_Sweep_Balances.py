
"""----------------------------------------------------------------------------------------------------
DESCRIPTION
    This module contains code to sweep FX PnL from unmonitored Sales books to actively monitored Trading books. The script runs every morning on a business day.

-------------------------------------------------------------------------------------------------------
HISTORY
=======================================================================================================
Date            JIRA no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-07-22      FAFO-118      Jaco Swanepoel          Ena Hewitt              Initial Implementation
2020-08-12      FAFO-118      Jaco Swanepoel          Ena Hewitt              Holiday consideration, threshold changes and discounting type change
2020-11-16      FAFO-167      Amit Kardile            Midas and Ena Hewitt    Sweep trades should have a trader who is mapped in MIDAS downstream system
-------------------------------------------------------------------------------------------------------
"""

import acm
import FFxCommon
import FBDPCommon
import FBDPRollback
import FLogger

LOGGER = FLogger.FLogger(__name__, 1)

TRADE_PROCESS_FX_CASH = 4096
TRADE_PROCESS_FX_SWAP_NEAR_LEG = 16384
TRADE_PROCESS_FX_SWAP_FAR_LEG = 32768


class SalesFxToZarSweep(FBDPRollback.RollbackWrapper, FFxCommon.FxPortfolioProcess):
    def __init__(self, args):
        FBDPRollback.RollbackWrapper.__init__(self, rollbackName=_getRollbackName())
        FFxCommon.FxPortfolioProcess.__init__(self)
        
        #defauls and configurables
        self.today = acm.Time.DateToday()
        
        self.test_run = args['TestRun']
        self.default_acquirer =  args['DefaultAcquirer'][0]
        self.default_counterparty = args['DefaultCounterparty']
        self.sweep_amount_threshold = float(args['SweepThreshold'])
        self.sweep_curr = args['SweepCurrency']
        self.bucket_to_years = int(args['BucketYears'])

        self.prf_non_africa_forward = args['prf_non_africa_forward']
        self.prf_non_africa_spot = args['prf_non_africa_spot']
        self.prf_flo = args['prf_flo']
        self.prf_african_forward = args['prf_african_forward']
        self.prf_african_spot = args['prf_african_spot']
        
        self.discounting_type = args['discounting_type']
        self.system_user = args['system_user']
        self.trader = args['trader']

        #initialise time buckets
        self.time_buckets = self.build_time_buckets()
        self.curr_vector = self.getCurrObjects(None)

    def build_time_buckets(self):
        """ Build the buckets for the projected cash ladder.
            This script works with a timebucket structure of Year -> Month -> Day.
            We don't expect any extremely long positions for FX. 
        """
        today = acm.Time.DateToday()
        
        bucket_definitions = acm.FArray()
        bucket_definitions.Add(self.createDefinition(0))
        
        day_counter = None
        
        for y in range(1, self.bucket_to_years):
            year_bucket = self.createDefinition(y)
            bucket_definitions.Add(year_bucket)
            
        bucket_definitions.Add(acm.FRestTimeBucketDefinition())
        bucks = acm.Time().CreateTimeBucketsFromDefinitions(today, bucket_definitions, None, 0, 0, 0, True, True, 0)
            
        return bucks

    def get_curr_pair_today_or_next_bussiness_day(self, curr_pair, current_date):
        cal1 = curr_pair.Currency1().Calendar()
        cal2 = curr_pair.Currency2().Calendar()
        
        if cal1.IsNonBankingDay(cal1, cal2, current_date):
            cal1_next_business_day = cal1.AdjustBankingDays(current_date, 1)
            cal2_next_business_day = cal2.AdjustBankingDays(current_date, 1)
            return max(cal1_next_business_day, cal2_next_business_day)
        else:
            return current_date

    def sweep_balance(self, sweep_date, result_vector, trading_portfolio, isForward):
        """ The FX balances should be swept as per the rules below.
        
            Cash position rules:
            ----------------------------------------------
            - Cash includes balances today up to the spot day (t+2 for FX)
            - The cash + spot balances will get 1 FX Cash trade per portfolio and FX balance. The FX amount is equal and opposite to the balance
                and mirrored to the trading portfolios as below:
                + CAT for SSA (African currencies)
                + AGG for all other currencies
                
            Forward position rules:
            ----------------------------------------------
            - Book FX Swaps for all forward balances with the near leg set to spot. 
            - The swaps will be mirrored to the forward trading portfolios as below:
                + FLO for USD/ZAR positions
                + JOL for SSA (African currencies)
                + FWT for all other currencies
            - Book a FX Cash trade on spot date corresponding to the equal and opposite of the swap near leg. The trade should mirrored to the 
                to the cash trading portfolios as per the cash position rules above.
        """
        
        LOGGER.LOG('Sweep_balance: %s - %s, %s' %(sweep_date, trading_portfolio.Name(), result_vector))
        # Each currency will have a corresponding column in the column vector and hence the valuation results.
        # assume the order of the currency list is the same as the returned valuation result array.
        index = 0
        for from_curr in self.curr_vector:
            amount = result_vector[index]

            if amount:
                curr_pair = FFxCommon.currencyPair(self.sweep_curr, from_curr)
                
                #check for holidays if we don't use spot date
                sweep_date_per_calendar = self.get_curr_pair_today_or_next_bussiness_day(curr_pair, sweep_date)

                spot_date = curr_pair.SpotDate(acm.Time.DateToday())
                fx_spot_rate = FFxCommon.getFxRate(spot_date, curr_pair.Currency1(), curr_pair.Currency2())
                fx_rate = FFxCommon.getFxRate(sweep_date_per_calendar, curr_pair.Currency1(), curr_pair.Currency2())

                if curr_pair.Currency1().Name() == from_curr.Name():
                    quantity = -amount
                    premium = amount * fx_rate
                    spot_quantity = -amount
                    spot_premium = amount * fx_spot_rate
                else:
                    quantity = amount / fx_rate
                    premium = -amount
                    spot_quantity = amount / fx_spot_rate
                    spot_premium = -amount

                if abs(quantity) > self.sweep_amount_threshold and abs(premium) > self.sweep_amount_threshold:
                    trades_to_commit = []
                    if sweep_date_per_calendar > spot_date:
                        #create a FX swap trade for forward balances
                        near_leg_trade = self.createFxTrade(curr_pair.Currency1(), curr_pair.Currency2(), trading_portfolio, self.default_acquirer,
                                                    self.default_counterparty, spot_date, fx_spot_rate, -spot_quantity, -spot_premium, "PL Sweep", TRADE_PROCESS_FX_SWAP_NEAR_LEG)

                        far_leg_trade = self.createFxTrade(curr_pair.Currency1(), curr_pair.Currency2(), trading_portfolio, self.default_acquirer,
                                                    self.default_counterparty, sweep_date_per_calendar, fx_rate, quantity, premium, "PL Sweep", TRADE_PROCESS_FX_SWAP_FAR_LEG)

                        far_leg_trade.ConnectedTrade(near_leg_trade)

                        #Create sweep trade to sweep the spot balance created by the swap
                        cash_sweep_trade = self.createFxTrade(curr_pair.Currency1(), curr_pair.Currency2(), trading_portfolio, self.default_acquirer,
                                                    self.default_counterparty, spot_date, fx_spot_rate, spot_quantity, spot_premium, "PL Sweep", TRADE_PROCESS_FX_CASH)

                        #routing rules for forward balances
                        if curr_pair.AdditionalInfo().SSA():
                            near_leg_trade.MirrorPortfolio(self.prf_african_forward)
                            far_leg_trade.MirrorPortfolio(self.prf_african_forward)
                        elif curr_pair.Name() == 'USD/ZAR':
                            near_leg_trade.MirrorPortfolio(self.prf_flo)
                            far_leg_trade.MirrorPortfolio(self.prf_flo)
                        else:
                            near_leg_trade.MirrorPortfolio(self.prf_non_africa_forward)
                            far_leg_trade.MirrorPortfolio(self.prf_non_africa_forward)

                        #FxSwap's need to be committed in a transaction - this is a Front thing - has to be done like this.
                        if not self.test_run:
                            try:
                                acm.BeginTransaction()
                                near_leg_trade.Commit()
                                far_leg_trade.Commit()
                                acm.CommitTransaction()
                            except Exception, error:
                                acm.AbortTransaction()
                                raise error

                        #add new trades to the new trades list in order to add to the roll back info later
                        trades_to_commit.append(near_leg_trade)
                        trades_to_commit.append(far_leg_trade)
                    else:
                        cash_sweep_trade = self.createFxTrade(curr_pair.Currency1(), curr_pair.Currency2(), trading_portfolio, self.default_acquirer,
                                                    self.default_counterparty, sweep_date_per_calendar, fx_rate, quantity, premium, "PL Sweep", TRADE_PROCESS_FX_CASH)

                    if cash_sweep_trade:
                        #rooting rules for cash balances
                        if curr_pair.AdditionalInfo().SSA():
                            cash_sweep_trade.MirrorPortfolio(self.prf_african_spot)
                        else:
                            cash_sweep_trade.MirrorPortfolio(self.prf_non_africa_spot)
                        
                        trades_to_commit.append(cash_sweep_trade)

                    try:
                        for trade in trades_to_commit:
                            if not self.test_run:
                                # Commit the new sweep trades via the roll back functionality
                                self.add_trade(trade)

                            LOGGER.LOG('Create trade: Instr: {0} Curr: {1} Trade Time: {2} Value day: {3} Quantity: {4} Premium: {5} Price {6}'.format(
                                        trade.Instrument().Name(), trade.Currency().Name(), trade.TradeTime(), trade.ValueDay(),
                                        trade.Quantity(), trade.Premium(), trade.Price()))
                    except Exception, ex:
                        message = 'Exception sweeping %s (%s) on %s. \nException: %s' % (amount, from_curr.Name(), sweep_date, ex)
                        LOGGER.ELOG(message)
                        raise ex

            index = index + 1

    def get_column_value_wrapper(self, node, column, day=0):
        column_value = self.getColumnValue(node, column, day)
        
        if type(column_value) is list:
            return column_value
        elif column_value is None:
            return None
        else:
            return [column_value]

    def process_forward_buckets(self, from_date, to_date, top_node, trading_portfolio):
        """ Function to step into the cash ladder and find balances to sheep.
            Start by checking for balances on the top node and only drill down if there is a balance at the top level.
        """
        for year_bucket in self.time_buckets:
            if year_bucket.ChildBuckets():
                test_for_positions_at_level = [pos for pos in self.get_column_value_wrapper(top_node, 'Portfolio Projected Payments', year_bucket.Name()) 
                                                if abs(pos) > self.sweep_amount_threshold]
                
                if test_for_positions_at_level:
                    for month_bucket in year_bucket.ChildBuckets():
                        test_for_positions_at_level = [pos for pos in self.get_column_value_wrapper(top_node, 'Portfolio Projected Payments', month_bucket.Name()) 
                                                        if abs(pos) > self.sweep_amount_threshold]
                        
                        if test_for_positions_at_level:
                            for day_bucket in month_bucket.ChildBuckets():
                                process_day_bucket = True
                                if from_date: 
                                    if day_bucket.EndDate() > from_date:
                                        process_day_bucket = True
                                    else:
                                        process_day_bucket = False
                                        
                                if to_date:
                                    if day_bucket.EndDate() <= to_date:
                                        process_day_bucket = True
                                    else:
                                        process_day_bucket = False

                                if process_day_bucket:
                                    forward_balances_vector = self.get_column_value_wrapper(top_node, 'Portfolio Projected Payments', day_bucket.Name())
                                    if forward_balances_vector:
                                        self.sweep_balance(day_bucket.EndDate(), forward_balances_vector, trading_portfolio, True)

    # BEGIN - Override base class methods
    # ---------------------------------------------------- 
    def perform(self, args):
        self.performProcess(args)
        self.end()
    
    def getCurrObjects(self, currPair):

        allCurrencies = acm.FCurrencyPair.Select('')
        allCurrenciesList = [curr.Currency1() for curr in allCurrencies
                            if self.sweep_curr.Name() == curr.Currency2().Name()]
        allCurrenciesList += [curr.Currency2() for curr in allCurrencies
                            if self.sweep_curr.Name() == curr.Currency1().Name()]
        return allCurrenciesList

    def processPortfolio(self, tradingPort, nodes):
        """ Inherit function from the base class. This is called to process the portfolios.
        """
        #Set the currency vector for the Projected Payments Per Instrument column
        self.setColumnConfig(self.curr_vector)

        for (top_node, self.attributes) in nodes:  
            top_node.Expand(True, 10)
            LOGGER.LOG('Process node: %s %s %s %s' %(type(top_node), top_node, 'Portfolio Name:', tradingPort.Name()))

            tradingCalendar = acm.FCurrency['ZAR'].Calendar()
            tomorrow_date = tradingCalendar.AdjustBankingDays(acm.Time.DateToday(), 1)
            spot_date = tradingCalendar.AdjustBankingDays(acm.Time.DateToday(), 2)

            # 1. sweep forward balances
            self.process_forward_buckets(spot_date, None, top_node, tradingPort)
            
            # 2. sweep cash balances
            cash_balances_vector = self.get_column_value_wrapper(top_node, 'Portfolio Projected Payments', '0y')
            if cash_balances_vector:
                self.sweep_balance(self.today, cash_balances_vector, tradingPort, False) 

            # 3. sweep forward from today to the spot date
            self.process_forward_buckets(acm.Time.DateToday(), spot_date, top_node, tradingPort)

    def defineCalcSpace(self):
        portfolios = self.getPortfoliosFromTradingObjects(self.tradingObjects)
        currenyPairs = [x.CurrencyPair() for x in portfolios]
        currObjects = acm.FSet().AddAll(
                [self.getCurrObjects(currPair) for currPair in currenyPairs])
        currObjects = currObjects.AsList()
        if not currObjects.IsEmpty():
            currObjects = [c for c in currObjects[0]]
            
        self.createCalcSpace(self.tradingObjects, self.portfolioGrouper, acm.FTimeBucketGrouper(self.time_buckets))
                
    def createDefinition(self, year):
        today = acm.Time.DateToday()
        definition = acm.FDatePeriodTimeBucketDefinition()
        
        name = '%sy' % year
        definition.DatePeriod(name)
        definition.Name(name)
        definition.Adjust(False)
        definition.RelativeSpot(False)
        return definition
    
    def createFxTrade(self, instrument, currency, portfolio, acquirer,
            counterparty, date, price, quantity, premium, tradetype,
            trade_process):

        trade = acm.FTrade()
        trade.Instrument(instrument)
        trade.Currency(currency)
        # overridden from self.attributes if grouped on acq
        trade.Acquirer(acquirer)
        trade.Counterparty(counterparty)
        if acm.User().Name() == self.system_user.Name():
            trade.Trader(self.trader)
        else:
            trade.Trader(acm.User())
        trade.Type(tradetype)
        trade.Status('BO Confirmed')
        trade.Price(price)
        trade.ReferencePrice(price)
        roundingForInstrument = FBDPCommon.getPremiumRounding(instrument)
        trade.Quantity(self.roundValueForInstrument(quantity,
                roundingForInstrument))
        roundingForCurrency = FBDPCommon.getPremiumRounding(currency)
        trade.Premium(self.roundValueForInstrument(premium,
                roundingForCurrency))
        tradeTime = acm.Time.DateNow()
        if acm.Time().DateDifference(tradeTime, date) > 0:
            tradeTime = date
        trade.TradeTime(tradeTime)
        trade.AcquireDay(date)
        trade.ValueDay(date)
        trade.TradeProcess(trade_process)
        trade.Portfolio(portfolio)
        trade.DiscountingType(self.discounting_type)
        return trade
    # ----------------------------------------------------
    # END - Override base class methods


def _getRollbackName():
    return 'FX_Risk_Sweep'


def get_disc_types():
    return [c.Name() for c in acm.FChoiceList['DiscType'].Choices()]

    
# AEL Variables definition = [[1.name, 2.Label, 3.Type, 4.PossibleValues, 5.DefaultValue, 6.Mandatory(1/0), 7.AllowMultiple(1/0) 8.Description, 9.InputHook, 10.Enabled, 11.CustomDialog]]]
ael_variables = [['test_run', 'Test Run:', 'bool', ['0', '1'], '1', 1, 0, 'Run in test mode - nothing will be commited.', None, 1, None],
                ['portfolio_list', 'Portfolios to sweep:', acm.FPhysicalPortfolio, None, None, 1, 1, 'Portfolios to sweep.', None, 1, None],
                ['default_acquirer', 'Default Acquirer:', acm.FParty, None, acm.FParty['FX SPOT'], 1, 0, 'Acquirer to be set on sweep trades.', None, 1, None],
                ['default_counterparty', 'Default Counterparty:', acm.FInternalDepartment, None, acm.FInternalDepartment['FX SPOT'], 1, 0, 'Counterparty on sweep trades.', None, 1, None],
                
                ['prf_non_africa_forward', 'Non-Africa Forward Portfolio:', acm.FPhysicalPortfolio, None, 'FWT', 1, 0, 'Non-Africa forward portfolio.', None, 1, None],
                ['prf_non_africa_spot', 'Non-Africa Spot Portfolio:', acm.FPhysicalPortfolio, None, 'AGG', 1, 0, 'Non-Africa forward portfolio.', None, 1, None],
                ['prf_flo', 'Flow Portfolio:', acm.FPhysicalPortfolio, None, 'FLO', 1, 0, 'Flow Portfolio for USD/ZAR forward positions.', None, 1, None],
                ['prf_african_forward', 'Africa Forward Portfolio:', acm.FPhysicalPortfolio, None, 'JOL', 1, 0, 'Africa forward portfolio.', None, 1, None],
                ['prf_african_spot', 'Africa Spot Portfolio:', acm.FPhysicalPortfolio, None, 'CAT', 1, 0, 'Africa spot portfolio.', None, 1, None],
                
                ['discounting_type', 'Disc Type:', 'string', get_disc_types, 'CCYBasis', 1, 0, 'Default discounting type.', None, 1, None],
                ['sweep_threshold', 'Sweep Threshold:', 'float', None, 0.01, 0, 0, 'Non denominated decimal. No amounts larger than the threshold will be swept', None, 1, None],
                ['sweep_currency', 'Sweep to currency:', 'FCurrency', None, acm.FCurrency['ZAR'], 1, 0, 'Sweep to currency', None, 0, None],
                ['bucket_years', 'Number of years to sweep:', 'int', None, 5, 1, 0, 'Number of years to into the future to process.', None, 1, None],
                ['system_user', 'The system user:', acm.FUser, None, 'UPGRADE43', 1, 0, 'The system user which runs the script.', None, 1, None],
                ['trader', 'The trader:', acm.FUser, None, 'HEWITTEN', 1, 0, 'The trader whose ID is mapped in MIDAS.', None, 1, None]]


def ael_main(params):
    import FBDPString
    reload(FBDPString)
    logme = FBDPString.logme
    scriptName = "FX Sweep"
    logme = FBDPString.logme
    # Set the logMe vars as the base class depends on this.
    # we will be logging with the Flogger.
    logme.setLogmeVar(scriptName, # ScriptName
                          0,  # LogMode
                          0,  # LogToConsole
                          0,  # LogToFile
                          "", # LogFile
                          0,  # SendReportByMail
                          "", # MailList
                          "") # ReportMessageType

    portfolio_list = acm.FArray()
    for portfolio in params['portfolio_list']:
        if portfolio.Class() == acm.FCompoundPortfolio:
            portfolio_list.AddAll(portfolio.AllPhysicalPortfolios())
        else:
            portfolio_list.Add(portfolio)

    args = {}
    # The base class in FxCommon expects the following args in the format as below:
    # DefaultPortfolio, TradingPortfolios, DefaultAcquirer DefaultCounterparty.
    args['DefaultPortfolio'] = portfolio_list
    args['TradingPortfolios'] = portfolio_list
    args['DefaultAcquirer'] = [params['default_acquirer']] 
    args['DefaultCounterparty'] = params['default_counterparty']
    # Custom ars for logic in this script
    args['TestRun'] = params['test_run']
    args['SweepCurrency'] = params['sweep_currency']
    args['SweepThreshold'] = params['sweep_threshold']
    args['BucketYears'] = params['bucket_years']
    
    args['prf_non_africa_forward'] = params['prf_non_africa_forward']
    args['prf_non_africa_spot'] = params['prf_non_africa_spot']
    args['prf_flo'] = params['prf_flo']
    args['prf_african_forward'] = params['prf_african_forward']
    args['prf_african_spot'] = params['prf_african_spot']
    
    args['discounting_type'] = params['discounting_type']
    args['system_user'] = params['system_user']
    args['trader'] = params['trader']
    sweeper = SalesFxToZarSweep(args)
    sweeper.perform(args)
