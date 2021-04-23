"""
-------------------------------------------------------------------------------
MODULE
    safex_positions

DESCRIPTION
    Date                : 2014-04-07
    Purpose             : This module contains an implementation of generating
                          safex positions report.
    Department and Desk : Risk Mid
    Requester           : Patrick Ngoie
    Developer           : Jakub Tomaga
    CR Number           : CHNG0001865852

HISTORY
===============================================================================
Date            CR number   Developer       Description
-------------------------------------------------------------------------------
24-04-2014      1919888     Jakub Tomaga    Quote marks around non-numeric
                                            values removed, ClosingAIP column
                                            added back - both modifictaions
                                            in the previous version of the
                                            script caused failures during
                                            subsequent Intellimatch feed.
-------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
import at_report


class PositionsReport(at_report.CSVReportCreator):
    """Creates the report."""
    def __init__(self, name, suffix, path, trade_filter, start_date, end_date):
        super(PositionsReport, self).__init__(file_name=name,
            file_suffix=suffix, path=path,
            csv_writer_parameters={'delimiter': ','}) # No quote marks!

        self.trade_filter = trade_filter
        self.start_date = start_date
        self.end_date = end_date

    def _collect_data(self):
        """Collect all required data relevant for the report."""
        self._log('Started')

        calc_space = acm.Calculations().CreateCalculationSpace(
           acm.GetDefaultContext(), 'FPortfolioSheet')

        trade_selection = acm.FTradeSelection[self.trade_filter]
        top_node = calc_space.InsertItem(trade_selection)

        grouper = acm.FStoredPortfolioGrouper.Select(
           'name=Portfolio')[0].Grouper()
        top_node.ApplyGrouper(grouper)

        # Portfolio sheet settings (variables)
        pnl_start_date_var = 'Standard Calculations Profit And Loss Start Date'
        pnl_end_date_var = 'Standard Calculations Profit And Loss End Date'
        valuation_date_var = 'Valuation Date'

        calc_space.SimulateGlobalValue(pnl_start_date_var, self.start_date)
        calc_space.SimulateGlobalValue(pnl_end_date_var, self.end_date)
        calc_space.SimulateGlobalValue(valuation_date_var, self.end_date)

        calc_space.Refresh()

        # Extract data
        if top_node.NumberOfChildren():
            # Iterate over a node tree structure in the calculation sheet
            # Note: Iterators need to be cloned - otherwise deeper levels won't
            #       be handled properly!
            portfolio_iter = top_node.Iterator().Clone().FirstChild()
            while portfolio_iter:
                count = 1
                number_of_children = portfolio_iter.Tree().NumberOfChildren()
                ins_iter = portfolio_iter.Clone().FirstChild()
                portfolio_name = portfolio_iter.Tree().Item().StringKey()
                while ins_iter:
                    self._log('Processing {0}/{1} ({2})'.format(count,
                        number_of_children, portfolio_name))
                    count += 1
                    self.content.append(self._line(calc_space, ins_iter,
                        portfolio_name))
                    ins_iter = ins_iter.NextSibling()
                portfolio_iter = portfolio_iter.NextSibling()

        # Remove simulations
        calc_space.RemoveGlobalSimulation(pnl_start_date_var)
        calc_space.RemoveGlobalSimulation(pnl_end_date_var)
        calc_space.RemoveGlobalSimulation(valuation_date_var)

        self._log('Finished')

    def _line(self, calc_space, iterator, portfolio_name):
        """Return a line to be appended to the csv file.

        iterator.Item() should return object of FInstrumentAndTrades
        """

        # Input values
        period_start = self.start_date
        period_end = self.end_date

        # Directly extracted values from data structures
        ins = iterator.Tree().Item().Instruments()[0]
        ins_name = ins.Name()
        currency = ins.Currency().Name()
        contract_size = ins.ContractSize()
        ins_type = ins.InsType()
        expiry = ins.ExpiryDate()
        quote_type = ins.QuoteType()
        quotation_factor = ins.Quotation().QuotationFactor()

        if ins.InsType() == 'Option':
            ins_option_type = 'Call' if ins.IsCallOption() else 'Put'
            ins_strike_price = ins.StrikePrice()
        else:
            # Not applicable when instrument's type is other than option.
            ins_option_type = ins_strike_price = ''

        # Directly extracted vales for underlying instrument (if any)
        u_ins = ins.Underlying()
        if u_ins:
            u_contract_size = u_ins.ContractSize()
            u_ins_name = u_ins.Name()
            u_ins_type = u_ins.InsType()

            # Normalised instrument name
            u_normalised_ins = self._normalised_instrument_name(u_ins)

        else:
            # Not applicable when underlying instrument doesn't exist
            u_contract_size = u_ins_name = u_ins_type = u_normalised_ins = ''

        # Values from calculation space
        value_start = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Value Start').FormattedValue())

        value_end = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Value End').FormattedValue())

        used_price_start = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Profit Loss Price Start Date').FormattedValue())

        used_price_end = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Profit Loss Price End Date').FormattedValue())

        pl_position_start = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Profit Loss Position Start').FormattedValue())

        pl_position_end = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Profit Loss Position End').FormattedValue())

        total_pl = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Total Profit and Loss').FormattedValue())

        total_pl_daily = self._str_to_float(
            calc_space.CreateCalculation(iterator.Tree(),
            'Portfolio Total Profit and Loss Daily').FormattedValue())

        # Dependent values
        if ins_type == 'Future/Forward' and quote_type == 'Per Contract':
            normalised_used_price_start = (used_price_start *
                quotation_factor / contract_size)
            normalised_used_price_end = (used_price_end *
                quotation_factor / contract_size)
        else:
            normalised_used_price_start = pl_position_start * quotation_factor
            normalised_used_price_end = pl_position_end * quotation_factor

        if ins_option_type:
            opening_front_notional = (pl_position_start *
                normalised_used_price_start)
            closing_front_notional = (pl_position_end *
                normalised_used_price_end)
        else:
            opening_front_notional = (pl_position_start *
                normalised_used_price_start * contract_size)
            closing_front_notional = (pl_position_end *
                normalised_used_price_end * contract_size)
        
        portfolio_nbr = ''
        physical_port = acm.FPhysicalPortfolio[portfolio_name]
        if physical_port:
            portfolio_nbr = physical_port.Oid()

        # Once the report is generated, it is used for feed into Intellimatch
        # which depends on column positioning. That's why the column needs to
        # stay in it's original position. Default value 0 - no specification.
        closing_aip = 0

        # Construct output line out of extracted data
        line = (
            portfolio_name,
            portfolio_nbr,
            u_contract_size,
            ins_name,
            value_start,
            value_end,
            currency,
            pl_position_end,
            contract_size,
            period_start,
            period_end,
            total_pl,
            used_price_start,
            used_price_end,
            ins_type,
            u_ins_name,
            u_ins_type,
            ins_option_type,
            ins_strike_price,
            expiry,
            quote_type,
            closing_aip,
            total_pl_daily,
            pl_position_start,
            quotation_factor,
            u_normalised_ins,
            normalised_used_price_start,
            normalised_used_price_end,
            opening_front_notional,
            closing_front_notional
        )

        return line

    @staticmethod
    def _normalised_instrument_name(instrument):
        """Return normalised instrument name."""
        name = instrument.Name()

        if name.lower().startswith('zar/'):
            if instrument.InsType() in ('Commodity', 'Future/Forward'):
                name = name.split('/')[1]
            elif instrument.InsType() == 'EquityIndex':
                if name.lower().__contains__('_divfut_underlying'):
                    name = name.split('/', 1)[1]
                else:
                    name = name.split('/', 1)[1].split('_')[0]
            elif instrument.InsType() in ('Stock', 'ETF'):
                name = name.split('/', 1)[1].split('_')[0]

        return name

    @staticmethod
    def _str_to_float(val):
        """
        Convert string to float while ignoring the commas
        within the number.
        """
        if type(val) == float:
            return val
        else:
            try:
                return float(val.replace(',', '')) if val != '' else 0
            except ValueError:
                return 0

    def _header(self):
        """Return columns of the header."""
        header = [
            'Portfolio',
            'PortfolioID',
            'Underlying.ContractSize',
            'Instrument',
            'Val Start',
            'Val End',
            'Currency',
            'PLPosEnd',
            'Contract Size',
            'Period Start',
            'Period End',
            'TPL',
            'Used Price Start',
            'Used Price End',
            'InstrumentType',
            'UnderlyingInstrument',
            'UnderlyingInstruentType',
            'Call/Put',
            'Strike Price',
            'Expiry',
            'QuoteType',
            'ClosingAIP',
            'TPLD',
            'PLPosStart',
            'QuotationFactor',
            'NormalisedUnderlyingInstrument',
            'NormalisedUsedPriceStart',
            'NormalisedUsedPriceEnd',
            'OpeningFrontNotional',
            'ClosingFrontNotional'
        ]

        return header

    @staticmethod
    def _log(message):
        """Basic console logging with time stamp prefix."""
        print("{0}: {1}".format(acm.Time.TimeNow(), message))


_CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVIOUS_BUSINESS_DAY = _CALENDAR.AdjustBankingDays(TODAY, -1)

START_DATE_DICT = {
    'Previous Business Day': PREVIOUS_BUSINESS_DAY,
    'Custom Date': PREVIOUS_BUSINESS_DAY
}
START_DATE_KEYS = START_DATE_DICT.keys()
START_DATE_KEYS.sort()

END_DATE_DICT = {
    'Today': TODAY,
    'Custom Date': TODAY
}
END_DATE_KEYS = END_DATE_DICT.keys()
END_DATE_KEYS.sort()


def custom_start_date_hook(selected_variable):
    """Enable/Disable Custom Start Date based on Start Date value."""
    start_date_custom = selected_variable.handler.get('start_date_custom')

    if selected_variable.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


def custom_end_date_hook(selected_variable):
    """Enable/Disable Custom End Date based on End Date value."""
    end_date_custom = selected_variable.handler.get('end_date_custom')

    if selected_variable.value == 'Custom Date':
        end_date_custom.enabled = True
    else:
        end_date_custom.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add('trade_filter', label='Trade filter',
    default='SI_safex_futures', alt='Trade filter')

ael_variables.add('filename', label='Filename',
    default='FrontArena_Safex_Positions', alt='Filename')

ael_variables.add('path', label='Path', default=r'F:/', alt='Path')

ael_variables.add('start_date', label='Start Date',
    default='Previous Business Day', collection=START_DATE_KEYS,
    alt='Start date', hook=custom_start_date_hook)

ael_variables.add('start_date_custom', label='Start Date Custom',
    default=PREVIOUS_BUSINESS_DAY, alt='Custom start date', enabled=False)

ael_variables.add('end_date', label='End Date',
    default='Today', collection=END_DATE_KEYS,
    alt='End date', hook=custom_end_date_hook)

ael_variables.add('end_date_custom', label='End Date Custom',
    default=TODAY, alt='Custom end date', enabled=False)


def ael_main(config):
    """The main entry point of the Run Script window."""
    # Get start date
    if config['start_date'] == 'Custom Date':
        start_date = config['start_date_custom']
    else:
        start_date = START_DATE_DICT[config['start_date']]

    # Get end date
    if config['end_date'] == 'Custom Date':
        end_date = config['end_date_custom']
    else:
        end_date = END_DATE_DICT[config['end_date']]

    # Generate the report
    report = PositionsReport(name=config['filename'], suffix='csv',
        path=config['path'], trade_filter=config['trade_filter'],
        start_date=start_date, end_date=end_date)
    report.create_report()
