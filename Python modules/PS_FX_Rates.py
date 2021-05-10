import string

import acm

from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator
from at_logging import getLogger
from HedgeConstants import STR_LAST_PRICE_MARKET
from PS_FormUtils import DateField

LOGGER = getLogger(__name__)
DATES = DateField.get_captions([
    'PrevBusDay',
    'Now',
    'Custom Date'])


def add_date_to_path(output_file, date):
    """Return the file path with date paremeter."""
    file_path_template = string.Template(output_file)
    file_path = file_path_template.substitute(DATE=date.replace("-", ""))
    return file_path


def custom_date_hook(selected_variable):
    """Enable/Disable Custom Date base on Date value."""
    start_date = ael_variables.get('date')
    start_date_custom = ael_variables.get('date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add(
    'currency_pairs',
    mandatory=True,
    label='Currency Pairs',
    cls='FStoredASQLQuery',
    collection=acm.FStoredASQLQuery.Select("subType='FCurrencyPair'"),
    alt='A query folder of Currencies for FX market to be included in the report'
)
ael_variables.add(
    "date",
    label="Date",
    default="Now",
    collection=DATES,
    hook=custom_date_hook
)
ael_variables.add(
    "date_custom",
    label="Date Custom",
    default=acm.Time().DateToday(),
    enabled=False
)
ael_variables.add(
    'filename',
    label='File Name',
    cls='string',
    default='PS_FX_Rates_$DATE',
    mandatory=True,
    multiple=False,
    alt='Name of the output file'
)
ael_variables.add_directory(
    'directory',
    label='Directory',
    alt='Output file path'
)


def get_fx_rate(curr_pair, input_date):
    if input_date == acm.Time().DateToday():
        price_table = curr_pair.Currency1().Prices()
    else:
        price_table = curr_pair.Currency1().HistoricalPrices()

    prices = price_table.Filter(
        lambda price:
            price.Currency().Name() == curr_pair.Currency2().Name() and
            price.Market().Name() == STR_LAST_PRICE_MARKET and
            price.Day() == input_date
    )

    if prices:
        return prices[0].Settle()
    else:
        LOGGER.warning(
            "Could not find fx rate for {} on {}".format(
                curr_pair.Name(), input_date))


class FxRatesReport(CSVReportCreator):
    def __init__(self, file_path, file_name, date, currency_pairs):
        self.report_date = date
        self.currency_pairs = currency_pairs
        super(FxRatesReport, self).__init__(file_name, 'csv', file_path)

    def _collect_data(self):
        for curr_pair in self.currency_pairs:
            rate = get_fx_rate(curr_pair, self.report_date)
            if rate:
                row = [
                    self.report_date,
                    curr_pair.Name(),
                    get_fx_rate(curr_pair, self.report_date)
                ]
                LOGGER.info(row)
                self.content.append(row)

    def _header(self):
        header = [
            "Date",
            "Currency Pair",
            "Rate",
        ]
        return header


def ael_main(ael_dict):
    if ael_dict['date'] == 'Custom Date':
        date = ael_dict['date_custom']
    else:
        date = DateField.read_date(ael_dict['date'])

    fx_report = FxRatesReport(
        str(ael_dict['directory'].SelectedDirectory()),
        add_date_to_path(ael_dict['filename'], date),
        date,
        ael_dict['currency_pairs'].Query().Select()
    )
    fx_report.create_report()
    LOGGER.info("Secondary output wrote to %s", fx_report._get_full_path())
    LOGGER.info("Completed successfully")
