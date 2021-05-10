import acm
import csv
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

HEADER_LIST = ['Stock', 'Direction', 'ABS()Vol', 'Ave Price', 'Trade date', 'Settlement Date']

ael_variables.add(
    'trade_filter',
    label='Trade Filter Name',
    cls='FTradeSelection',
    default='A2X_new_deals'
)

ael_variables.add(
    'output_file',
    label='Output File',
    default='/services/frontnt/Task/A2X_Postions.csv'
)


def write_csv_file(output_file_location, results_list, header_list):
    """
    Create a file to store all results
    """
    with open(output_file_location, 'wb') as reconBreaksFile:
        recon_writer = csv.writer(reconBreaksFile, quoting=csv.QUOTE_ALL)
        recon_writer.writerow(header_list)
        for item_in_list in results_list:
            recon_writer.writerow(item_in_list)


def source_data(trade_filter):
    """
        returns negative and postive position per instrument
    """
    results_data = []
    for instrument in trade_filter.Instruments():
        ins_name = instrument.Name()
        positive_position = 0
        negative_position = 0
        negative_price = 0
        positive_price = 0
        for trade in instrument.Trades():
            if trade in trade_filter.Trades():

                trade_position = trade.Position()
                if trade_position >= 0:
                    positive_position = positive_position + trade.Position()
                    positive_price = positive_price + trade.Position() * trade.Price()
                else:
                    negative_position = negative_position + trade.Position()
                    negative_price = negative_price + trade.Position() * trade.Price()

        settlement_date = trade.ValueDay()
        execution_time = trade.ExecutionTime()

        try:
            average_pos = positive_price / positive_position
        except ZeroDivisionError:
            average_pos = 0
        try:
            average_neg = negative_price / negative_position
        except ZeroDivisionError:
            average_neg = 0

        if float(abs(negative_position)) != 0.00:
            results_data.append(
                [ins_name, 'S', abs(negative_position), abs(average_neg), execution_time, settlement_date])
        if float(positive_position) != 0.00:
            results_data.append([ins_name, 'B', positive_position, average_pos, execution_time, settlement_date])

    return results_data


def ael_main(ael_dict):
    trade_filter_note = ael_dict['trade_filter']
    output_file_location = ael_dict['output_file']
    results_data = source_data(trade_filter_note)
    write_csv_file(output_file_location, results_data, HEADER_LIST)
