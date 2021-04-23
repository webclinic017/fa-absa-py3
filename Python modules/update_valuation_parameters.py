import acm

def update_valuation_parameters(valuation_parameters, parameter_name, parameter_value):
    for valuation_parameter in valuation_parameters:
        obj = valuation_parameter.GetPropertyObject(parameter_name)
        
        if obj and not obj.IsReadOnly():
            try:
                obj.Set(parameter_value)
            except Exception, e:
                print(e)
        
        
ael_variables = [
    ['valuation_parameters', 'Valuation Parameters', 'FValuationParameters', None, '', 1, 1, 'Valuation Parameter to be updated.', None, 1],
    ['parameter_name', 'Parameter Name', 'string', None, '', 1, 1, 'Valuation Parameter to be updated.', None, 1],
    ['parameter_value', 'Parameter Value', 'string', None, '', 1, 1, 'Valuation Parameter to be updated.', None, 1]
]

def ael_main(parameters):
    update_valuation_parameters(
        parameters['valuation_parameters'],
        parameters['parameter_name'],
        parameters['parameter_value']
    )
