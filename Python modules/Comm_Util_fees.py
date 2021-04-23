import acm
from at_logging import getLogger
from DataAccessUtil import DataAccess
from at_ael_variables import AelVariableHandler
from FAFOUtils import WriteCSVFile

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()

ael_variables.add('output_path',
                  label='output path',
                  mandatory=True,
                  default='/services/frontnt/Task/',
                  tab="Task Inputs")
                  
def get_data_values(keys, data_dict):
    data_values = []
    for key in keys:
        if key in data_dict.keys():
            if key in ['PM_FacilityExpiry', 'PM_CommitFeeBase']:
                date = acm.Time.AsDate(data_dict[key])
                data_values.append(date)
            else:
                data_values.append(data_dict[key])
        else:
            data_values.append(None)
    return data_values
            
def get_trades():
    asql_query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    asql_query.AddAttrNode('Acquirer.Name', 'EQUAL', 'PRIMARY MARKETS')
    asql_query.AddAttrNodeString('Status', 'Simulated', 'NOT_EQUAL')
    asql_query.AddAttrNodeString('Status', 'Void', 'NOT_EQUAL')
    asql_query.AddAttrNodeString('Instrument.InsType', 'Curr', 'EQUAL')
    asql_query.AddAttrNodeString('AdditionalInfo.InsOverride', ['Commitment Fee', 'Utilisation Fee'], 'EQUAL')
    return asql_query.Select()

def get_util_rates(trade):
    rates = []
    record = DataAccess().Select(trade.Name())
    for key in record.keys():
        if 'From' in key:
            num = key.split('From')
            lb = record['RateFrom'+str(num[1])]
            ub = record['RateTo'+str(num[1])]
            rate = str(record['Rate'+str(num[1])])
            if lb and ub:
                rates.append([lb, ub, float(rate)])
    return rates

def get_generate_report(file_path, trades):
    today = acm.Time.DateToday() 
    keys = ['PM_FacilityMax', 'PM_FacilityExpiry', 'PM_CommitFeeBase', 'CommitPeriod', 'Rolling Convention', 'DayCount']
    commfee_trades = [trd for trd in trades if trd.AdditionalInfo().InsOverride() == 'Commitment Fee']
    utilfee_trades = [trd for trd in trades if trd.AdditionalInfo().InsOverride() == 'Utilisation Fee']
    headers = ['Trade Number', 'PM_FacilityCPY', 'PM_FacilityID', 'Calculate Utilization Fee',\
            'Facility Limit', 'Facility Expiry', 'PM_CommitFeeBase', 'Rolling Period',\
            'Rolling Convention', 'Day Count', '']
    utilisation_headers = ['PM_FacilityCPY', 'PM_FacilityID', 'LowerBound', 'UpperBound', 'Rate']
    if len(commfee_trades)>= 1:
        res = []
        file_name = 'CommFees'+'.csv'
        fee_type = 'CMF'
        util_fee_indicator = 'FALSE'
        for trade in commfee_trades:
            key = fee_type+str(trade.Name())
            record = DataAccess().Select(key)
            facility_cpty = trade.AdditionalInfo().PM_FacilityCPY()
            if facility_cpty <> None:
                facility_cpty  = facility_cpty.Name()
            facility_id = trade.AdditionalInfo().PM_FacilityID()
            if record <> None:
                res.append([trade.Name(), facility_cpty, facility_id, util_fee_indicator]+get_data_values(keys, record))
        WriteCSVFile(file_path, file_name, res, headers)
        LOGGER.info('Comm File generated successfully.')
    if len(utilfee_trades) >= 1:
        res = []
        util_table = []
        file_name = 'UtilFees'+'.csv'
        file_name2 = 'Utilstables'+'.csv'
        fee_type = 'UTF'
        util_fee_indicator = 'TRUE'
        for trade in utilfee_trades:
            key = fee_type+str(trade.Name())
            record = DataAccess().Select(key)
            facility_cpty = trade.AdditionalInfo().PM_FacilityCPY()
            if facility_cpty <> None:
                facility_cpty  = facility_cpty.Name()
            facility_id = trade.AdditionalInfo().PM_FacilityID()
            util_fee_indicator = 'TRUE'
            if record <> None:
                utils_rates = get_util_rates(trade)
                res.append([trade.Name(), facility_cpty, facility_id, util_fee_indicator]+get_data_values(keys, record))
                for rate_list in utils_rates:
                    util_table.append([facility_cpty, facility_id]+rate_list)
        WriteCSVFile(file_path, file_name, res, headers)
        LOGGER.info('Util File generated successfully.')
        WriteCSVFile(file_path, file_name2, util_table, utilisation_headers)
        LOGGER.info('Util tables file generated successfully.')

def ael_main(ael_dict):
    file_path = ael_dict['output_path']
    try:
        trades = get_trades()
        if len(trades) >= 1:
            get_generate_report(file_path, trades)
            LOGGER.info('Reports generated....')
        LOGGER.info('Task completed successfully.')
    except Exception as e:
        LOGGER.error('Task failed due to the following error {}.', format(e))


    


