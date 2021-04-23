"""
-------------------------------------------------------------------------------
MODULE
    SAFI_SalesCredit

DESCRIPTION
    This script updates the Sales_Credit2 and Sales_Person2 additional info
    fields for Fixed Income trades in a batch run at the end of the day.
    Only trades that have counterparties included in the sales person filters
    are updated with a sales credit.

    Date                : 2010-04-08
    Purpose             : Calculates the sales credit for Fixed Income trades
    Department and Desk : PCG SM Middle Office
    Requester           : Kelly Chetty
    Developer           : Herman Hoon
    CR Number           : 271252

HISTORY
===============================================================================
Date       Change no    Developer           Description
-------------------------------------------------------------------------------
2010-04-08 271252       Herman Hoon         Initial implementation
2010-05-17 312981       Ickin Vural         Remove Filter and adapt for
                                            FValidation Changes
2010-05-31 327617       Ickin Vural         Isolate Job4 trades to Henry
2011-05-19 658000       Herman Hoon         Amend code to work on a task from
                                            the backend
2011-06-24 696273       Heinrich Cronje     Replaced ABHI006 with ABAR546
2011-12-07 852541       Heinrich Cronje     Changed sales credit formula as
                                            instructed by business.
2013-04-23 972468       Ntuthuko Matthews   Replaced ABAR546 with PETOUSIT
2013-06-06 1067843      Sanele Macanda      Changed the specificBondDelta bonds
                                            value to reflect each DV Bonds
2013-06-13 1091578      Sanele Macanda      Replace Thalia Petousis and with
                                            Riweena Perumal (ABRP358)
2013-07-09 1146171      Sanele Macanda      Updated ILB tariffs
2013-09-10 1298865      Sanele Macanda      Moving Dite's clients to Thisen
                                            for Fixed Income.
2014-02-27 1756639      Andrei Conicov      If counterparty is DRA Transaksies
                                            the sales credit is calculated only
                                            for JOB11 portfolio
2014-02-08 1829143      Sanele Macanda      Amendment to FI script
2014-02-08 1829143      Sanele Macadna      Add new counterparty and Sales
                                            person to FI script
-------------------------------------------------------------------------------
2014-06-03 2018517      Jan Sinkora         Complete rewrite. The logic for
                                            specific bonds was moved to other
                                            modules: SAFI_SalesCredit_Corp and
                                            SAFI_SalesCredit_Govi
-------------------------------------------------------------------------------
2014-09-08 2292647      Nada Jasikova       Added parameters to optionally:
                                            - Save trades
                                            - Write results to file
                                            - Write errors to file
-------------------------------------------------------------------------------
2014-11-28 2493978      Nada Jasikova       - Processing of very small values
                                            - Fixed selection of parties based
                                            on issuer sector
                                            - Modified selecting sales person
                                            based on other sales credit fields
                                            - Added logging of errors within
                                            the sales-person process for future
                                            use
2015-06-30 ABITFA-3662 Vojtech Sidorin      Fix multiline strings.
--------------------------------------------------------------------------------
2016-02-16 ABITFA-4013 Faize Adams	    -Enable dynamic sales person
                                            allocations based on ratios.
                                            -Enable sales person allocation
                                            through task parameters.
2016-04-13 ABITFA-4211 Faize Adams          -Enable certain counterparties to be
                                            excluded through task parameters.
                                            -Updated to exclude all internal desk
                                            counterparties, except Prime services.
                                            -Code will exclude mirror trades from
                                            being allocated a sales credit.
                                            -Updated trade filter to only allocate
                                            credits on BO-BO confirmed trades.
2017-03-08 ABITFA-4745 Andrei Conicov    Setting the SalesCreditSubTeam to "Fixed Income Flow"
                                         Using at_logging
                                         
2018-04-18 ABITFA-5333 Bhavnisha Sarawan Replace default of Sales Person Name 2 from ABJMA38 to ABJR456
ENDDESCRIPTION

2018-12-06 ABITFA-5637 Shalini Lala	Remove excluded counterparties and add to trade filter
					Remove sales person parameters
					
--------------------------------------------------------------------------------
"""

import acm
import at_addInfo
import FValidation
import os
import traceback
import csv
import re
import random

from at_ael_variables import AelVariableProvider
from at_progress import start_stopwatch
from at_logging import getLogger

LOGGER = getLogger(__name__)

class BondSalesCreditGenerator(AelVariableProvider):
    """An abstract class for sales credit generating."""
    CALENDAR = acm.FCalendar['ZAR Johannesburg']
    INCEPTION = acm.Time().DateFromYMD(1970, 1, 1)
    TODAY = acm.Time().DateToday()
    FIRSTOFYEAR = acm.Time().FirstDayOfYear(TODAY)
    FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
    YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
    TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
    PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
    TWOBUSDAYSAGO = CALENDAR.AdjustBankingDays(TODAY, -2)
    ONEWEEKAGO = CALENDAR.AdjustBankingDays(TODAY, -7)

    START_DATES = {'Inception': INCEPTION,
                   'First Of Year': FIRSTOFYEAR,
                   'First Of Month': FIRSTOFMONTH,
                   'PrevBusDay': PREVBUSDAY,
                   'TwoBusinessDaysAgo': TWOBUSDAYSAGO,
                   'TwoDaysAgo': TWODAYSAGO,
                   'OneWeekAgo': ONEWEEKAGO,
                   'Yesterday': YESTERDAY,
                   'Custom Date': TODAY,
                   'Now': TODAY}

    END_DATES = {'Now': TODAY,
                 'TwoDaysAgo': TWODAYSAGO,
                 'PrevBusDay': PREVBUSDAY,
                 'Yesterday': YESTERDAY,
                 'Custom Date': TODAY}


    # Valid instrument types
    VALID_INSTRUMENT_TYPES = ('Bond', 'FRN', 'IndexLinkedBond')
    PRIME_SERVICES_DESK = 'PRIME SERVICES DESK'

    # Minimum credit value (for x: 0 < x < 0.01)
    MINIMUM_CREDIT = 0.01

    @staticmethod
    def _toggle_enable_custom_date(variables, variable_name):
        """Create a hook which toggle enable on custom dates."""
        def toggle_hook(var):
            variables.get(variable_name).enabled = (var.value == 'Custom Date')
        return toggle_hook

    @staticmethod
    def _toggle_enable(variables, *field_names):
        """Create a hook which toggles 'enable' on given output fields."""
        def toggle_hook(var):
            for field_name in field_names:
                field = variables.get(field_name)
                field.enabled = var.value
                field.mandatory = var.value
        return toggle_hook

    @staticmethod
    def _all_trade_filters():
        return [trade_filter.Name()
                for trade_filter in acm.FTradeSelection.Select('')]

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        super(BondSalesCreditGenerator, cls)._populate_ael_variables(variables,
                                                                     defaults)
        default_out_path = '/services/frontnt/Task/'

        variables.add('start_date',
                      label='Start Date',
                      collection=sorted(cls.START_DATES.keys()),
                      default=defaults.pop('start_date', 'Now'),
                      alt=('Execution date from which sales credit should '
                           'be calculated.'),
                      hook=cls._toggle_enable_custom_date(variables,
                                                          'start_date_custom'))
        variables.add('start_date_custom',
                      label='Start Date Custom',
                      default=defaults.pop('start_date_custom', cls.TODAY),
                      mandatory=False,
                      alt='Custom start date')
        variables.add('end_date',
                      label='End Date',
                      collection=sorted(cls.END_DATES.keys()),
                      default=defaults.pop('end_date', 'Now'),
                      alt=('Execution date up to which sales credit should '
                           'be calculated.'),
                      hook=cls._toggle_enable_custom_date(variables,
                                                          'end_date_custom'))
        variables.add('end_date_custom',
                      label='End Date Custom',
                      default=defaults.pop('end_date_custom', cls.TODAY),
                      mandatory=False,
                      alt='Custom end date')
        variables.add('trade_filter',
                      label='Filter',
                      collection=cls._all_trade_filters(),
                      default=defaults.pop('trade_filter', 'SAFI_SalesCredit'),
                      alt=('Trade filter on which sales credit should '
                           'be calculated.'))

        variables.add_bool('save_trades',
                           label='Save processed trades',
                           default=True,
                           alt=('Save calculated sales credit value and sales '
                                'person on the processed trades'))
        variables.add_bool('log_results',
                           label='Write results to file',
                           default=True,
                           hook=cls._toggle_enable(variables,
                                                   'result_output_path',
                                                   'result_output_filename'),
                           alt=('Write calculated sales credit value '
                                'and sales person to file'))
        variables.add_directory('result_output_path',
                                label='Output folder for results',
                                default=defaults.pop('result_output_path',
                                                     default_out_path))
        variables.add('result_output_filename',
                      label='Result file name',
                      default=defaults.pop('result_output_filename', None))
        variables.add_bool('log_errors',
                           label='Log errors to file',
                           default=True,
                           hook=cls._toggle_enable(variables,
                                                   'error_output_path',
                                                   'error_output_filename'),
                           alt='Log trade processing errors to a file')
        variables.add_directory('error_output_path',
                                label='Output folder for error reporting',
                                default=defaults.pop('error_output_path',
                                                     default_out_path))
        variables.add('error_output_filename',
                      label='Error report file name',
                      default=defaults.pop('error_output_filename', None))

    def getSalesSplit(self, params, number_of_persons):
        persons = {}
        nameLabel = "person"
        counter = 0
        ratioLabel = "personRatio"
        
        for i in range (1, number_of_persons):
            person = params["%s%i" % (nameLabel, i)]
            ratio = params["%s%i" % (ratioLabel, i)]
            
            if '/' in ratio:
                i, j = ratio.split('/')
                ratio = float(i) / float(j)
            
            if person and (float(ratio) > 0):
                persons[person] = float(ratio)
                
        if sum(persons.values()) != 1:
            print "Ratios don't add up: %s" % sum(persons.values())
                
        return persons

    def getValidTrades(self, trades):
        validTrades = []
        
        for trade in trades:
            try:
                mirror = trade.GetMirrorTrade().Oid()
                if mirror not in validTrades:
                    validTrades.append(trade.Oid())
                else:
                    LOGGER.info('Trade %s is mirror of Trade %s. %s excluded from allocation.',
                                trade.Oid(), mirror, trade.Oid())
            except:
                validTrades.append(trade.Oid())

        return [acm.FTrade[t] for t in validTrades]
        

    def calculate_sales_credit(self, start_date, end_date,
                               trade_filter, sales_split_ratios):
        """The main worker method to loop through given trades and process
        these for sales credit generation."""

        self.wrote_error_output = False

        get_duration = start_stopwatch()
        successful_count = 0
        trades = self.getValidTrades(trade_filter.Trades())
        
        LOGGER.info('%s trades found in the provided trade filter', len(trades))

        for trade in trades:
            print trade.Oid()
            create_date = acm.Time.DateFromTime(trade.CreateTime())
            if start_date <= create_date <= end_date:
                if self._process_trade(trade, sales_split_ratios):
                    successful_count += 1
        
        LOGGER.info('%s trades have been processed in %.0f seconds',
                    successful_count, get_duration())

        if self._log_errors:
            self._error_report()

        if self._log_results:
            self._log_totals()
            self._result_report()
            

    def _error_report(self):
        """Creates a text file and outputs the processing errors"""
        if not self._trade_errors:
            return
        with open(self.full_error_output_path, 'wb') as f:
            for trade_error in self._trade_errors:
                f.write(trade_error + '\n')
        self.wrote_error_output = True

    def _result_report(self):
        """Creates a CSV file and outputs the trade records"""
        LOGGER.info("The results will be written to file %s",
                    self.full_result_output_path)

        if not os.path.isdir(self._result_output_directory):
            LOGGER.info('The folder %s does not exist, creating one.',
                        self._result_output_directory)
            try:
                os.mkdir(self._result_output_directory)
            except OSError as exception:
                LOGGER.error('Output folder %s not created: %s.',
                             self._result_output_directory, exception)
                return

        try:
            csv_file = open(self.full_result_output_path, 'wb')

            columns = ['Trade_Number',
                       'Trade_Creation_Date',
                       'Trade_Date',
                       'Counterparty',
                       'Relationship_Party',
                       'Issuer_Sector',
                       'Portfolio',
                       'Instrument_Id',
                       'Instrument_Type',
                       'Nominal',
                       'Absolute_Nominal',
                       'Sales_Person',
                       'Sales_Credit']

            writer = csv.writer(csv_file, dialect='excel')
            writer.writerow(columns)

            for trade_row in self._trade_results:
                writer.writerow(trade_row)

            csv_file.close()

            self.wrote_result_output = True

        except Exception:
            self.wrote_result_output = False
            LOGGER.exception("Did not manage to write to file %s", self.full_result_output_path)

        if self.wrote_result_output:
            LOGGER.info("The results were written to file %s", self.full_result_output_path)
            

    def _validate_trade(self, trade, sales_split_ratios):
        trade_oid = trade.Oid()

        if not sales_split_ratios:
            LOGGER.error("Trade %s: No sales person found", trade_oid)
            return

        if not self._perform_trade_validations(trade):
            LOGGER.info("Trade %s: Trade validation failed", trade_oid)
            return

        if not self._validate_trade_single_sales_credit(
                trade, sales_split_ratios):
            LOGGER.info("Trade %s: Trade single SC validation failed", trade_oid)
            return

        return True

    def _process_trade(self, trade, sales_split_ratios):
        """Method to process a single trade for sales credit generation."""
        trade_oid = trade.Oid()

        if not sales_split_ratios:
            LOGGER.error("Trade %s: No sales person set found", trade_oid)
            return False

        # sales_person = self._choose_sales_person(trade, salesSplit)

        if not self._validate_trade(trade, sales_split_ratios):
            return False

        raw_sales_credit = abs(self._calculate_sales_credit(trade))
        sales_credit = self._get_credit_or_minimum(raw_sales_credit)

        if sales_credit == 0:
            LOGGER.error("Trade %s: Sales credit calculated to be 0, skipping allocation.", trade_oid)
            return False

        if self._save_trades:
            try:
                self._save_trade(trade, sales_split_ratios, sales_credit)
                LOGGER.info("Trade %s: Sales credit %s, Sales persons %s",
                            trade_oid, sales_credit, "|".join(sales_split_ratios))
            except Exception:
                validation_exception = FValidation.last_exc_info
                if validation_exception:
                    ex = "".join(traceback.format_exception(
                        *validation_exception))
                message = 'Trade {0} has not been updated with the Sales Credit additional info fields: {1}'.format(
                               trade_oid, ex)
                LOGGER.warning(message)
                self._trade_errors.append(message)
                return False

        if self._log_results:
            self._log_trade(trade, sales_split_ratios, sales_credit)
            try:
                self._update_totals(trade, sales_split_ratios, sales_credit)
            except Exception:
                LOGGER.exception("Error updating trade totals for the result file.")

        return True

    def __init__(self, result_output_path, result_output_filename,
                 error_output_path, error_output_filename):
        """Initializes the generator, setting the validation methods array."""

        self.full_error_output_path = os.path.join(*map
                                                   (str,
                                                    [error_output_path,
                                                     error_output_filename]))

        self.full_result_output_path = os.path.join(*map
                                                    (str,
                                                     [result_output_path,
                                                      result_output_filename]))

        self._result_output_directory = str(result_output_path)

        self._validation_methods = [self._validate_trade_type]
        self.wrote_error_output = False

        self._trade_errors = []
        self._trade_results = []

        self._totals_by_sales_person = {}
        self._totals_by_portfolio = {}
        self._totals_by_portfolio_and_sales_person = {}
        self._totals_by_ins_type_and_sales_person = {}

    def _get_credit_or_minimum(self, credit):
        if 0 < credit < self.MINIMUM_CREDIT:
            LOGGER.info("Calculated sales credit is too low (%s), using MINIMUM value (%s)",
                        credit, self.MINIMUM_CREDIT)
            return self.MINIMUM_CREDIT

        return credit

    def _perform_trade_validations(self, trade):
        """Goes through and calls all registered validation functions.

        If a validation function returns an error, trade is not valid.

        """
        for validate in self._validation_methods:
            error = validate(trade)
            if error != None:
                LOGGER.info("Trade %s is not entitled for sales credit: %s",
                            trade.Oid(), error)
                return False

        return True

    def _validate_trade_type(self, trade):
        """Validate the current trade against the basic Sales Credit rules."""

        # Only bond, index linked bond are allowed, exclude the rest.
        if (trade.Instrument().InsType() not in self.VALID_INSTRUMENT_TYPES):
            message = "Only instruments of types: {0} are allowed."
            return message.format(self.VALID_INSTRUMENT_TYPES)

        # If the SC addinfo is set to "No", don't generate.
        if trade.AdditionalInfo().SC() == 'No':
            return "The SC addinfo is set to 'No'"

    def _validate_trade_single_sales_credit(self, trade, sales_split_ratios):
        """Only one sales credit person and value can be entered.

        This would cause a popup when run from the GUI, that is not desirable
        for batch trade processing.

        """
        # Sales_Person2-5
        addinfo_fields = ['Sales_Person{0}'.format(i) for i in (3, 4, 5)]
        for field in addinfo_fields:
            original_sp = getattr(trade.AdditionalInfo(), field)()
            if original_sp:
                if self._sales_person_already_set(trade.Oid(), sales_split_ratios,
                                                  original_sp.Name(), field):
                    return False

        # Sales_Person1
        if trade.SalesPerson() and trade.SalesPerson() in sales_split_ratios.keys():
            if self._sales_person_already_set(trade.Oid(), sales_split_ratios,
                                              trade.SalesPerson(),
                                              'Sales_Person1'):
                return False

        return True

    def _sales_person_already_set(self, trade_oid, target_sp,
                                  original_sp, field_name):
        if original_sp in target_sp.keys():
            LOGGER.info("Trade %s: %s is already assigned to %s.",
                        trade_oid, field_name, original_sp)
            return True
        return False
    
    def _calculate_sales_credit(self, trade):
        """Hook that calculates the sales credit value.

        This must be implemented by subclasses.

        """
        raise NotImplementedError

    def _save_trade(self, trade, salesPersons, sales_credit):
        """Set trade attributes and save it.

        Set Sales_Person2 and Sales_Credit2 additional infos
        for the given trade and save the trade.
        If exception is thrown, it is raised on.

        """
        numberOfSalesPersons = len(salesPersons.keys())
        allocatedSoFar = 0.0

        acm.BeginTransaction()
        try:
            for salesPerson, i in zip(salesPersons.keys(), list(range(numberOfSalesPersons))):
                toAllocate = sales_credit * salesPersons[salesPerson]
                at_addInfo.save(trade, 'Sales_Person%s' % str(i + 2), salesPerson)
                at_addInfo.save(trade, 'SalesCreditSubTeam%s' % str(i + 2), 'Fixed Income Flow')
                if i == (numberOfSalesPersons - 1):
                    at_addInfo.save(trade, 'Sales_Credit%s' % str(i + 2), '{0:f}'.format(sales_credit - allocatedSoFar))
                else:
                    at_addInfo.save(trade, 'Sales_Credit%s' % str(i + 2), '{0:f}'.format(toAllocate))
                allocatedSoFar = allocatedSoFar + toAllocate
            acm.CommitTransaction()
        except Exception, e:
            acm.AbortTransaction()
            raise

    def _log_trade(self, trade, sales_split_ratios, salesCredit):
        """Retrieve and log the trade data.

        Retrieve the trade attributes that should be logged to
        the result output file, create an array of these values (row)
        and append the array to the existing rows.

        """

        for sales_person in sales_split_ratios:
            sales_credit = round(salesCredit * (sales_split_ratios[sales_person]))
            trade_number = trade.Name()
            trade_creation_date = trade.CreateTime()
            trade_date = trade.TradeTime()
            counterparty = trade.Counterparty().Name()
            rel_pty = None
            if trade.AdditionalInfo().Relationship_Party():
                rel_pty = trade.AdditionalInfo().Relationship_Party().Name()
            issuer_sector = None
            issuer = trade.Instrument().Issuer()
            if issuer and issuer.Free4ChoiceList():
                issuer_sector = issuer.Free4ChoiceList().Name()
            portfolio = trade.Portfolio().Name()
            instrument_id = trade.Instrument().Name()
            instrument_type = trade.Instrument().InsType()
            nominal = trade.Nominal()
            sales_person = sales_person
            sales_credit = sales_credit

            trade_row = self._get_result_line(trade_number, trade_creation_date,
                                              trade_date, counterparty, rel_pty,
                                              issuer_sector, portfolio,
                                              instrument_id, instrument_type,
                                              nominal, sales_person, sales_credit)
            self._trade_results.append(trade_row)

    def _update_totals(self, trade, sales_split_ratios, salesCredit):
        """Update the totals for the result output files.

        Update all dictionaries that store totals of sales credit
        based on several criteria for the output file.

        The totals dictionaries are:
        _totals_by_sales_person
        _totals_by_portfolio
        _totals_by_portfolio_and_sales_person
        _totals_by_ins_type_and_sales_person

        """

        for sales_person in sales_split_ratios.keys():
            sales_credit = round(salesCredit * (sales_split_ratios[sales_person]))
            self._increment_value(self._totals_by_sales_person,
                                  sales_person, sales_credit)
            self._increment_value(self._totals_by_portfolio,
                                  trade.Portfolio().Name(), sales_credit)
            self._increment_value(self._totals_by_portfolio_and_sales_person,
                                  [trade.Portfolio().Name(), sales_person],
                                  sales_credit)
            self._increment_value(self._totals_by_ins_type_and_sales_person,
                                  [trade.Instrument().InsType(), sales_person],
                                  sales_credit)

    def _log_totals(self):
        """Append the totals for the result output file to the result rows."""

        for sales_person, sales_credit in self._totals_by_sales_person.items():
            single_line = self._get_result_line('TOTAL BY SALES PERSON',
                                                sales_person=sales_person,
                                                sales_credit=sales_credit)
            self._trade_results.append(single_line)

        for portfolio, sales_credit in self._totals_by_portfolio.items():
            single_line = self._get_result_line('TOTAL BY PORTFOLIO',
                                                portfolio=portfolio,
                                                sales_credit=sales_credit)
            self._trade_results.append(single_line)

        for portfolio, sc_data in (self._totals_by_portfolio_and_sales_person
                                   .items()):
            for sales_person, sales_credit in sc_data.items():
                single_line = self._get_result_line(('TOTAL BY PORTFOLIO'
                                                     '& SALES PERSON'),
                                                    portfolio=portfolio,
                                                    sales_person=sales_person,
                                                    sales_credit=sales_credit)
                self._trade_results.append(single_line)

        for ins_type, sc_data in (self._totals_by_ins_type_and_sales_person
                                  .items()):
            for sales_person, sales_credit in sc_data.items():
                single_line = self._get_result_line(('TOTAL BY INSTRUMENT TYPE'
                                                    ' & SALES PERSON'),
                                                    ins_type=ins_type,
                                                    sales_person=sales_person,
                                                    sales_credit=sales_credit)
                self._trade_results.append(single_line)

    def _get_result_line(self, trade_number, trade_creation_date=None,
                         trade_date=None, counterparty=None,
                         relationship_party=None, issuer_sector=None,
                         portfolio=None, instrument_id=None,
                         ins_type=None, nominal=None,
                         sales_person=None, sales_credit=None):
        """Create a trade result row for the result output file"""

        absolute_nominal = None
        if nominal:
            absolute_nominal = abs(nominal)

        return [trade_number, trade_creation_date, trade_date, counterparty,
                relationship_party, issuer_sector, portfolio, instrument_id,
                ins_type, nominal, absolute_nominal, sales_person,
                sales_credit]

    def _increment_value(self, dictionary, key, value):
        """ Retrieve value from dictionary and increment it.

        If the key attribute is a pair of values, assume that
        the first item is the key, the value is another dictionary
        and the second item is the key to the inner dictionary - the
        method then increments the value of the inner dictionary.

        """

        if type(key) is list:
            if len(key) == 2:
                grouping_key = key[0]
                if grouping_key not in dictionary:
                    dictionary[grouping_key] = {}
                return self._increment_value(dictionary[grouping_key],
                                             key[1], value)
            else:
                message = 'Wrong # of items specified in the key attribute'
                raise Exception(message)
        else:
            if key in dictionary:
                dictionary[key] += value
            else:
                dictionary[key] = value
            return dictionary[key]
