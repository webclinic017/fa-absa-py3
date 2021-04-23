import acm
from at_ael_variables import AelVariableHandler
from at_calculation_space import prepare_calc_space
from at_progress import LineProgress
from at_report import CSVReportCreator

import contextlib

date_today_ymd = acm.Time.DateToYMD(acm.Time.DateToday())

ael_gui_parameters = {'windowCaption': 'CPI fixing',
                      'runButtonLabel': '&&Run fixing',
                      'closeWhenFinished': True}

ael_variables = AelVariableHandler()
ael_variables.add('year',
        label='Price year',
        cls='int',
        default=date_today_ymd[0])
ael_variables.add('month',
        label='Price month',
        cls='int',
        default=date_today_ymd[1] - 1)
ael_variables.add('rate',
        label='CPI rate')
ael_variables.add('index',
        label='Indef Ref',
        collection=['SACPI', 'SACPI-Bond'],
        default='SACPI')        
ael_variables.add_directory('output_folder',
        label='Output folder',
        default='c:/_temp')
ael_variables.add('difference_tolerance',
        label='Difference tolerance for the PNL impact check',
        cls='int',
        default=10000)
ael_variables.add_bool('add_price_only',
        label='Only save the price (test run of the fixing)',
        default=False)
ael_variables.add_bool('recalculate',
        label='Recalculate fixing',
        default=False)


def log(message):
    print '{0}: {1}'.format(acm.Time.TimeNow(), message)


def extension_attribute_value(entity, attribute_name):
    """Get the value of the specified extension attribute.

    This is used when the attribute doesn't have an associated column.

    """

    tag = acm.CreateEBTag()
    context = 'Standard'

    return acm.GetCalculatedValueFromString(
            entity, context, attribute_name, tag).Value()


def get_object_name(obj):
    if hasattr(obj, "Name"):
        return obj.Name()

    return obj


def get_number_from_denominated(obj):
    if hasattr(obj, "Number"):
        return obj.Number()

    return obj


class ProfitLossReportCreator(CSVReportCreator):
    """A report of profit and loss columns."""
    columns = ['Trade Number',
            'Trade Execution Time',
            'Trade Instrument',
            'Trade Price',
            'Trade Nominal',
            'Trade Portfolio',
            'Trade Currency',
            'Trade Trader',
            'Portfolio Cash End',
            'Total Val End',
            'Present Value',
            'Portfolio Currency',
            'Instrument Start Date',
            'Instrument End Date']

    _column_postprocessing = {
            'Trade Execution Time': \
                    lambda value: acm.Time.DateTimeFromTime(value),
            'Trade Instrument': lambda value: str(value)[1:-1],
            'Trade Portfolio': get_object_name,
            'Trade Currency': get_object_name,
            'Trade Trader': get_object_name,
            'Portfolio Cash End': get_number_from_denominated,
            'Total Val End': get_number_from_denominated,
            'Present Value': get_number_from_denominated,
            'Portfolio Currency': get_object_name}

    def __init__(self, file_name, file_suffix, file_path, trades):
        super(ProfitLossReportCreator, self).__init__(file_name, file_suffix, file_path)
        self._trades = trades

    def _collect_data(self):
        self.content = []

        row_getter = prepare_calc_space('FTradeSheet')
        for trade in self._trades:
            value_getter = row_getter(trade)
            row = []
            for column_name in self.columns:
                column_value = value_getter(column_name)
                postprocessing = self._column_postprocessing.get(column_name)
                if postprocessing:
                    column_value = postprocessing(column_value)
                row.append(column_value)

            self.content.append(row)

    def _header(self):
        return self.columns


class ProfitLossDiffReportCreator(CSVReportCreator):
    """A report of differences in PnL values pre/post fixing."""
    def __init__(self, file_name, file_suffix, file_path, before, after,
            difference_tolerance):
        super(ProfitLossDiffReportCreator, self).__init__(file_name, file_suffix, file_path)
        self._before = before
        self._after = after
        self._difference_tolerance = difference_tolerance

    def _column_value(self, row, column_name):
        return row[ProfitLossReportCreator.columns.index(column_name)]

    def _header(self):
        return ['Trade Number',
                'Portfolio',
                'Cash End Before',
                'Cash End After',
                'Cash End Difference',
                'Total Val End Before',
                'Total Val End After',
                'Total Val End Difference',
                'Present Value Before',
                'Present Value After',
                'Present Value Difference']

    def _collect_data(self):
        """Create a diff between self._before and self._after."""

        self.content = []
        for row_before, row_after in zip(
                self._before.content, self._after.content):

            cash_end_before = self._column_value(row_before, 'Portfolio Cash End')
            cash_end_after = self._column_value(row_after, 'Portfolio Cash End')
            cash_end_diff = cash_end_after - cash_end_before

            total_val_end_before = self._column_value(row_before, 'Total Val End')
            total_val_end_after = self._column_value(row_after, 'Total Val End')
            total_val_end_diff = total_val_end_after - total_val_end_before

            present_value_before = self._column_value(row_before, 'Present Value')
            present_value_after = self._column_value(row_after, 'Present Value')
            present_value_diff = present_value_after - present_value_before

            if (abs(cash_end_diff) > self._difference_tolerance
                    or abs(total_val_end_diff) > self._difference_tolerance
                    or abs(present_value_diff) > self._difference_tolerance):

                row = []
                row.append(self._column_value(row_before, 'Trade Number'))
                row.append(self._column_value(row_before, 'Trade Portfolio'))

                row.append(cash_end_before)
                row.append(cash_end_after)
                row.append(cash_end_diff)

                row.append(total_val_end_before)
                row.append(total_val_end_after)
                row.append(total_val_end_diff)

                row.append(present_value_before)
                row.append(present_value_after)
                row.append(present_value_diff)

                self.content.append(row)


class FixedResetsReportCreator(CSVReportCreator):
    """A report of resets affected by the fixing process."""
    def __init__(self, file_name, file_suffix, file_path, fixed_resets):
        super(FixedResetsReportCreator, self).__init__(file_name, file_suffix, file_path)
        self._fixed_resets = fixed_resets

    def _header(self):
        return ['Instrument',
                'Type',
                'Date',
                'Value (after fixing)',
                'Estimate (before fixing)',
                'Start Day',
                'End Day',
                'Reset Id']

    def _collect_data(self):
        self.content = []
        for (reset, estimate) in self._fixed_resets:
            self.content.append([
                reset.Instrument().Name(),
                reset.ResetType(),
                reset.Day(),
                reset.FixingValue(),
                estimate,
                reset.StartDate(),
                reset.EndDate(),
                reset.Oid()
                ])


class CPIFixer(object):
    """This class is used for the fixing itself."""


    def __init__(self, price_date, price, output_path,
            difference_tolerance, recalculate, index_ref):
        """Initialize the fixing instance.

        price_date -- the date of the SACPI price, first day of a month
        price -- new SACPI price
        output_path -- a folder where the reports will be dumped
        difference_tolerance -- only report PnL difference higher than this
        recalculate -- if this is is evaluated as False, the process will
                fail if there already is a price in SACPI

        """

        self._price_date = price_date
        self._previous_price_date = acm.Time.DateAddDelta(
                self._price_date, 0, -1, 0)

        # The previous dates are used for interpolation for the month that's
        # four months from the price date.
        self._fixing_month = acm.Time.DateAddDelta(
                self._price_date, 0, 3, 1)

        log('Fixing the month starting with {0}.'.format(self._fixing_month))

        self._index_ref = index_ref
        self._price = price
        self._instrument = acm.FInstrument[self._index_ref]
        self._output_path = output_path
        self._file_suffix = 'csv'
        self._difference_tolerance = difference_tolerance
        self._recalculate = recalculate
        

    def run(self, add_price_only):
        """Run the fixing.

        add_price_only -- this will only add the price, no fixing will be done.

        Returns a list of fixed resets and another with exceptions encountered
        during the fixing. These will be tuples (reset, exception).

        """

        # The rest of the run is testing only.
        test_run = add_price_only

        # Precalculate the fixing values and find all resets that need to
        # be fixed.
        resets = self._get_resets()
        log('{0} resets found in the fixing month.'.format(len(resets)))
        trades = self._get_trades(resets)
        log('{0} trades could be affected by the fixing process.'.format(len(trades)))

        exceptions = []

        # Temporarily disable realtime prices, re-enable after all is done.
        with self._disable_realtime_prices():
            if not test_run:
                log('Creating pre-fixing profit/loss report.')
                before = self._pnl_report(trades, 'CPI_resets_pnl_before')

            # Add the new CPI rate to the SACPI instrument.
            log('Setting CPI rate.')
            self._add_price()

            # The fixing itself.
            log('Fixing resets (test run: {0}).'.format(test_run))
            fixed_resets, exceptions = self._fix_resets(resets, test_run)
            log('Creating report of fixed resets.')
            self._fixed_resets_report(fixed_resets, 'CPI_fixed_resets')

            if not test_run:
                log('Creating post-fixing profit/loss report.')
                after = self._pnl_report(trades, 'CPI_resets_pnl_after')
                self._diff_report(before, after, self._difference_tolerance,
                        file_name='CPI_resets_pnl_diff')

                # Repair wrongly created legs/cashflows.
                # These only get created during fixing, so only when not doing
                # a test run.
                # This doesn't seem to happen, but might be added later.
                # self._repair_wrong_legs()

        return map(lambda tupl: tupl[0], fixed_resets), exceptions


    def _get_resets(self):
        """Find all resets that should be fixed based on the new price."""
        end_of_fixing_month = acm.Time.DateAddDelta(self._fixing_month, 0, 1, 0)

        reset_query = acm.CreateFASQLQuery('FReset', 'AND')
        reset_query.AddAttrNode('Day', 'GREATER_EQUAL', self._fixing_month)
        reset_query.AddAttrNode('Day', 'LESS', end_of_fixing_month)
        reset_query.AddAttrNode('Leg.IndexRef.Name', 'EQUAL', self._index_ref)
        reset_query.AddAttrNode('Leg.Instrument.InsType', 'NOT_EQUAL', 'CurrSwap')
        reset_query.AddAttrNode('Leg.Instrument.InsType', 'NOT_EQUAL', 'TotalReturnSwap')
        reset_query.AddAttrNode('Leg.Instrument.InsType', 'NOT_EQUAL', 'EquitySwap')
        type_node = reset_query.AddOpNode('OR')
        type_node.AddAttrNode('ResetType', 'EQUAL', 'Return')
        type_node.AddAttrNode('ResetType', 'EQUAL', 'Nominal Scaling')

        resets = reset_query.Select()

        return resets

    def _get_trades(self, resets):
        """Find all trades associated with the given resets."""
        instruments = set(reset.Instrument() for reset in resets)
        return [trade
                for instrument in instruments
                for trade in instrument.Trades()
                if trade.Status() not in ('Simulated', 'Void')]

    def _fix_resets(self, resets, test_run):
        """Fix the resets if test_run has false value."""
        date_start = self._previous_price_date
        date_end = self._price_date

        query = 'instrument = "{0}" and day = "{1}" and market = "internal"'

        # Find the two rates which the interpolation will be based on.
        try:
            rate_base = acm.FPrice.Select01(
                query.format(self._instrument.Name(), date_start), None).Settle()
            rate_next = acm.FPrice.Select01(
                query.format(self._instrument.Name(), date_end), None).Settle()
        except:
            log("ERROR: No or multiple prices for SACPI found.")
            raise

        days_in_month = acm.Time.DaysInMonth(self._fixing_month)
        rate_coefficient = (rate_next - rate_base) / days_in_month

        log('Base rate: {0}.'.format(rate_base))
        log('Rate per day coefficient: {0}.'.format(rate_coefficient))

        progress = LineProgress(len(resets))

        # This will contain tuples (committed_reset, original fixing estimate).
        fixed_resets = []
        exceptions = []
        for reset in resets:
            # Cache the current legs.
            leg_ids = set(leg.Oid() for leg in reset.Instrument().Legs())

            # For each reset in self._fixing_month, the fixing rate will be:
            # rate_base + d * rate_coefficient, where d is how many days
            # is the reset day after the starting day of the fixing month.
            # The fixing period is (2nd of month M, 1st of month M+1) and the
            # right edge of the interval is aligned with the newly added price.
            day = acm.Time.DateDifference(reset.Day(), self._fixing_month) + 1

            rate = round(rate_base + day * rate_coefficient, 5)

            # Get the estimate value before fixing is done.
            estimate = get_number_from_denominated(
                    extension_attribute_value(reset, 'hybridFixingValue'))

            reset.FixingValue(rate)
            reset.ReadTime(acm.Time.DateToday())
            try:
                if not test_run:
                    reset.Commit()
                    acm.PollDbEvents()

                    # Check if new legs were created. If so, report them so that
                    # they can be investigated. This didn't happen during
                    # testing, but it was previously experienced when users
                    # were doing this manually, therefore this check.
                    instrument = acm.FInstrument[reset.Instrument().Oid()]
                    tmp_leg_ids = set(leg.Oid() for leg in instrument.Legs())
                    new_leg_ids = tmp_leg_ids - leg_ids
                    if new_leg_ids:
                        message = "WARNING: New legs created, ids: {0}."
                        log(message.format(new_leg_ids))

                fixed_resets.append((reset, estimate))
            except Exception as ex:
                log("Error on reset {0}, instrument {1}: {2}".format(
                    reset.Oid(), reset.Instrument().Name(), ex))
                exceptions.append((reset, ex))

            progress.inc()

        return fixed_resets, exceptions

    def _fixed_resets_report(self, fixed_resets, file_name):
        report_creator = FixedResetsReportCreator(file_name, self._file_suffix,
                self._output_path, fixed_resets)
        report_creator.create_report()

    def _diff_report(self, before, after, difference_tolerance, file_name):
        diff_report = ProfitLossDiffReportCreator(
                file_name, self._file_suffix, self._output_path, before, after,
                difference_tolerance)
        diff_report.create_report()

    def _pnl_report(self, trades, file_name):
        """Create a PnL report and return it for difference calculations."""
        report_creator = ProfitLossReportCreator(
                file_name, self._file_suffix, self._output_path, trades)
        report_creator.create_report()
        return report_creator

    @contextlib.contextmanager
    def _disable_realtime_prices(self):
        """Disable realtime prices and then return the original settings."""
        preferences = acm.UX.SessionManager().SessionPreferences()
        original_settings = preferences.RealtimePrices()

        log('Disabling realtime prices.')
        preferences.RealtimePrices(False)

        try:
            yield
        finally:
            log('Restoring realtime prices settings.')
            preferences.RealtimePrices(original_settings)

    def _add_price(self):
        """Add price to the instrument (SACPI).

        If self._recalculate is False, this will fail if a price already exists
        for the fixing date.

        """

        instrument = self._instrument
        date = self._price_date
        rate = self._price
        market = acm.FParty['internal']

        existing_price = None
        prices = acm.FPrice.Select('instrument = {0}'.format(instrument.Name()))
        for price in prices:
            if price.Market() == market and price.Day() == date:
                if not self._recalculate:
                    raise ValueError('Rate already exists for this date.')
                else:
                    existing_price = price
                    break

        if existing_price:
            # If self._recalculate is False, an exception would be raised
            # That means we're recalculating.
            price = existing_price
        else:
            price = acm.FPrice()
            price.Instrument(instrument)
            price.Day(date)
            price.Market(market)
            price.Currency(acm.FInstrument['ZAR'])

        price.Ask(rate)
        price.Bid(rate)
        price.High(rate)
        price.Low(rate)
        price.Settle(rate)
        price.Last(rate)
        price.Commit()

        log('The price was updated in SACPI.')


def ael_main(params):
    price_date = acm.Time.DateFromYMD(params['year'], params['month'], 1)
    price = float(params['rate'])
    difference_tolerance = params['difference_tolerance']
    recalculate = params['recalculate']
    add_price_only = params['add_price_only']
    output_path = str(params['output_folder'].SelectedDirectory())
    index = params['index']

    log('Starting the fixing script for date {0} with rate {1}.'.format(
        price_date, price))

    fixer = CPIFixer(price_date, price, output_path, difference_tolerance, recalculate, index)
    fixed_resets, exceptions = fixer.run(add_price_only)

    log("Finished. Summary:")

    log("Successfully updated resets: {0}.".format(len(fixed_resets)))
    log("Exceptions on resets: {0}, see log for details.".format(len(exceptions)))

    if exceptions:
        print "Completed with errors."
    else:
        print "Completed successfully."
