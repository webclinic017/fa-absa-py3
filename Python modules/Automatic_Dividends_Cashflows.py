import acm
import csv
import FRunScriptGUI
import FUxCore
from at_logging import getLogger
from DividendCashFlow import GenerateDividendCashFlow
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
ael_variables.add('query_folder',
                  label='Query folder',
                  cls=acm.FStoredASQLQuery,
                  collection=sorted(acm.FStoredASQLQuery.Select("subType='FInstrument'")),
                  default=acm.FStoredASQLQuery['TRS_Dividends'])

ael_variables.add('output_folder',
                  label='Output Folder',
                  mandatory=True,
                  default="Y:\Jhb\PCG\Middle Office\Projects\DIVIDENDS_CASH_FLOWS")


def write_instruments_to_csv(output_location, results_list):
    with open(output_location, 'wb') as output_file:
        output_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        output_writer.writerows(results_list)


def ael_main(ael_dict):
    results_list = []
    instruments = ael_dict['query_folder'].Query().Select()
    today = acm.Time.DateToday()
    two_days_back = acm.Time.DateAddDelta(today, 0, 0, -2)
    for instrument in instruments:
        div = GenerateDividendCashFlow(instrument, two_days_back, today)
        if not div.cash_flow_exists():
            div.generate_dividend_cash_flow()
            results_list.append([instrument.Name()])

    output_location = str(ael_dict['output_folder']) + 'Automatic_Dividends_Cashflows.csv'
    write_instruments_to_csv(output_location, results_list)
