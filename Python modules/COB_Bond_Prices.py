import csv
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


DEAL_SHEET_CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
TRADE_SHEET_CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
RESULTS_HEADERS = ['Date', 'Instrument', 'Yield', 'Price', 'Spread', 'Benchmark Delta']
DATE_TODAY = acm.Time().DateToday()
LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()

ael_variables.add('Outpath',
    label='Output Path',
    default='/services/frontnt/Task/')

ael_variables.add('result_output_filename',
                      label='Result file name',
                      default='CAP_MARKET_CD_CorpCDS_basis.csv')
                      
ael_variables.add('Curve',
    label='Yield Curve',
    cls='FYieldCurve',
    default='USD-CORPBONDS-SPREADS',
    multiple=False)
    

def write_csv_file(output_file_location, results_list, header_list):
    with open(output_file_location, 'wb') as cob_bond_price_report:
        file_writer = csv.writer(cob_bond_price_report, quoting=csv.QUOTE_ALL)
        file_writer.writerow(header_list)
        for item in results_list:
            file_writer.writerow(item)


def ael_main(ael_dict):
    yield_curve = ael_dict['Curve']
    ins_spreads = yield_curve.InstrumentSpreads()    
    results_list = []    
    
    for ins_spread in ins_spreads:
        ins_name = ins_spread.Instrument().Name()
        spread = ins_spread.Spread()
        ins = acm.FInstrument[ins_name]
        
        yield_price = DEAL_SHEET_CALC_SPACE.CreateCalculation(ins, 'Theoretical Price YTM Adjusted').Value()
        if yield_price:
            yield_price = yield_price.Number()
        else:
            yield_price = 0.0
        
        price = DEAL_SHEET_CALC_SPACE.CreateCalculation(ins, 'Theoretical Price Clean').Value().Number()
        bdelta = TRADE_SHEET_CALC_SPACE.CreateCalculation(ins, 'Benchmark Delta').Value().Number()
                
        results_list.append([DATE_TODAY, ins_name, yield_price, price, spread, bdelta])

    output_file_location = str(ael_dict['Outpath']) + str(ael_dict['result_output_filename'])
    
    try:
        write_csv_file(output_file_location, results_list, RESULTS_HEADERS)
        LOGGER.info("Completed successfully.")
    except Exception as exc:
        LOGGER.exception("Error writing to file: %s", exc)
    
