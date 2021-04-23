''' Cashflow upload file processing module.

This processor handles a file used for cashflow insertion on Call
Accounts in FA.

Date: 2014-02-24
Requester: Alex Boshoff
Developer: Jan Sinkora

'''

import os
import acm
import codecs
from at_feed_processing import SimpleCSVFeedProcessor, notify_log
import at_addInfo


class CashflowCSVFeedProcessor(SimpleCSVFeedProcessor):
    '''Processor used for cashflow insertion.'''

    # This must be platform and locale independent.
    # In this case it's simpler to put the list here than using complex
    # tools like calendar or locale.
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']

    # Required columns.
    COLUMN_ACCOUNT_NUMBER = 'Account_Number'
    COLUMN_FIXED_AMOUNT = 'CM_Nominal'
    COLUMN_PAY_DATE = 'Settlement_Date'
    _required_columns = [COLUMN_PAY_DATE, COLUMN_ACCOUNT_NUMBER,
        COLUMN_FIXED_AMOUNT]


    def parse_date(self, raw_date):
        '''Parses the input date.

        The expected format is D-Mon-YYYY where Mon is a three-letter
        abbreviation of the month name in english.

        Returns an ACM time.

        '''

        (day, month, year) = raw_date.split('-')
        return acm.Time.DateFromYMD(
                int(year), self.MONTHS.index(month) + 1, int(day))


    def parse_amount(self, raw_amount):
        '''Converts the input amount to a float.

        The expected input is str('A,BCD.EFGH')

        '''
        return float(raw_amount.replace(',', ''))

    @staticmethod
    def _prepare_csv_line(line):
        '''The file is in a weird MS Excel csv format, each line needs to be
        prepared first.

        Input line format:
        u'\n"column1,column2,""column,with,commas"",column3"\r'
        Output line format:
        u'column1,column2,"column,with,commas",column3'
        '''

        return line.strip()[1:-1].replace('""', '"')

    def _generate_records(self):
        '''Handles file decoding before the DictReader opens the file.'''

        # This replaces self._data with a generator.
        decoded_lines = codecs.iterdecode(self._data, 'utf-16')
        self._data = (self._prepare_csv_line(line) for line in decoded_lines)

        return super(CashflowCSVFeedProcessor, self)._generate_records()


    def _process_record(self, record, dry_run):
        '''Handles the individual cashflow inserting instructions.'''
        index, cashflow_data = record
        account_number = cashflow_data[self.COLUMN_ACCOUNT_NUMBER].strip()

        # -9,955.95
        raw_fixed_amount = cashflow_data[self.COLUMN_FIXED_AMOUNT]
        fixed_amount = self.parse_amount(raw_fixed_amount)

        # 1-Oct-13
        raw_date = cashflow_data[self.COLUMN_PAY_DATE]
        date = self.parse_date(raw_date)
        date_today = acm.Time.DateToday()

        if date < date_today:
            message = 'Cashflow on line {0} is backdated, skipping.'
            raise self.RecordProcessingException(message.format(index))

        if date > date_today:
            message = 'Cashflow on line {0} is dated in the future, skipping.'
            raise self.RecordProcessingException(message.format(index))

        # Look for the exact object ID of the instrument.
        instrument = acm.FDeposit[account_number]
        if not instrument:
            self._log_line(index, 'Call account {0} not found'.format(
                account_number))
            # Try to remove the dashes (the old naming convention).
            account_number = account_number.replace('-', '')
            self._log_line(index, 'Looking for call account {0}'.format(
                account_number))

            instrument = acm.FDeposit[account_number]

            if not instrument:
                self._log_line(index,
                    'Call account {0} not found either, aborting.'.format(
                        account_number))
                message = 'Line {0}: Call account {1} not found.'.format(
                        index, account_number)
                raise self.RecordProcessingException(message)

        self._log_line(index, 'Instrument found: ' + instrument.Name())

        self._create_cashflow(instrument, fixed_amount, date, dry_run)


    def _create_cashflow(self, instrument, fixed_amount, date, dry_run):
        '''Creates the cashflow on the instrument if it doesn't exist yet.'''

        statuses = ('BO-BO Confirmed', 'BO Confirmed', 'FO Confirmed')

        selected_trade = None
        trades = [trade for trade in instrument.Trades()
            if trade.Status() != 'Void']

        # Look for the selected trade according to the priority
        # defined in the tuple statuses (higher priority statuses
        # are in the beginning of the tuple).
        for status in statuses:
            if not selected_trade:
                for trade in trades:
                    if trade.Status() == status:
                        selected_trade = trade
                        break

        if not selected_trade:
            msg = 'A confirmed trade was not found for {0}.'.format(
                instrument.Name())
            raise self.RecordProcessingException(msg)

        instrument_trades = acm.FList()
        instrument_trades.Add(selected_trade)

        leg = instrument.Legs()[0]

        for cashflow in leg.CashFlows():
            if (cashflow.PayDate() == date
                    and cashflow.CashFlowType() == 'Fixed Amount'
                    and cashflow.FixedAmount() == fixed_amount):
                msg = ('There is already a cashflow with the specified nominal '
                    'and date: {0} on {1}')
                raise self.RecordProcessingException(msg.format(
                    date, instrument.Name()))

        self._log('Adjusting deposit with Fixed Amount: '
            '{0} and date: {1}'.format(fixed_amount, date))

        if dry_run:
            self._log('Dry run: No cashflows are being added.')
        else:
            # Adjust the deposit. The method requires trade quantity
            # because the cashflow will get automatically adjusted so that
            # cashflow_fixed_amount * trade_quantity = requested fixed amount
            action_result = instrument.AdjustDeposit(fixed_amount, date,
                selected_trade.Quantity())

            if action_result:
                acm.PollDbEvents()
                cashflows = instrument.Legs()[0].CashFlows()
                last_cashflow = max(cashflows,
                    key=lambda cashflow: cashflow.Oid())

                # This addinfo is required for filtering in Settlement Manager.
                at_addInfo.save_or_delete(last_cashflow, 'Settle_Type',
                    'Settle')

                self._log('Successfully adjusted deposit.')
            else:
                message = ('Failed to adjust deposit {0}, most likely due to '
                    'balance limit breach. See log for detailed info.')

                raise self.RecordProcessingException(message.format(
                    instrument.Name()))


ael_variables = CashflowCSVFeedProcessor.ael_variables(
    file_dir='C:/_temp',
    file_name='CollateralMovementsExtractFrontArenaAbsa.csv')


def ael_main(params):
    '''Entry point for task execution.'''
    file_dir = params['file_dir']
    file_name = params['file_name']
    file_path = os.path.join(file_dir, file_name)
    dry_run = params['dry_run']

    processor = CashflowCSVFeedProcessor(file_path)
    processor.add_error_notifier(notify_log)

    processor.process(dry_run)

    if not processor.errors:
        print("Completed successfully")


