import acm
import FVaRFileParsing

tt_file = 'The name or path to an external scenario file. If no path is given, the path fallbacks to the FCS_RISK_DIR environment variable first and then the current working directory. '    
tt_start_index = 'The starting column used in the external scenario file.'
tt_end_index = 'The ending column used in the external scenario file.'
tt_risk_type = 'The Risk Factor Type. Only Risk Factor Specifications with Risk Factor Group of this type will be shifted.' 

ael_variables = [
['file', 'Scenario File', 'string', 
    None, None, 1, 0, tt_file],
['start_index', 'Column Start', 'int', 
    None, None, 0, 0, tt_start_index],
['end_index', 'Column End', 'int', 
    None, None, 0, 0, tt_end_index],
['risk_type', 'Risk Type', 'EnumRiskFactorTypes', 
    acm.FEnumeration['EnumRiskFactorTypes'].Values(), 'Total', 1, 0, tt_risk_type]
]

def ael_main_ex(parameters, dict_extra):
    file = parameters['file']
    start_index = parameters['start_index']
    end_index = parameters['end_index']
    risk_type = parameters['risk_type']

    file_path = FVaRFileParsing.file_with_path(file)
    if not risk_type:
        risk_type = 'None'
    elif risk_type == 'Total':
        risk_type = 'None'
    if not start_index or start_index < 0:
        start_index = 0
    if not end_index or end_index < 0:
        end_index = 0

    if end_index < start_index:
        raise Exception('Column End < Column Start')

    valuationDate = acm.Time().DateToday()
    builder = acm.GetFunction("createRiskFactorScenarioBuilder", 0)()

    return builder.CreateScenario(file_path, start_index, end_index, risk_type, valuationDate)
