import acm

def rf_spec_headers():
    return acm.FRiskFactorSpecHeader.Select("")

ael_variables = [
#   [e_Id, e_Name, e_Type, e_Choices, e_DefaultValue, e_Mandatory, e_MultiChoice,  
#    e_Description, e_InputHook, e_Enabled],

    ['filePath', 'External scenario file', 'string', None, None, 1, 0, '',
     None, True],
     
    ['rfSpecHeader', 'Risk Factor Specification header',
     'FRiskFactorSpecHeader', rf_spec_headers(), None, 1, 0, '', None, True],
     
    ['shiftForm', 'Shift form', 'string', ["Triangle", "Rectangle", "Smooth"],
     "Triangle", 1, 0, '', None, True]
]

def ael_main_ex( parameters, dict_extra ):
    file_path = parameters['filePath']
    rf_spec_header = parameters['rfSpecHeader']
    shift_form = parameters['shiftForm']
    
    # FExtensionInvokationInfo
    eii = dict_extra.At('customData')    
    
    # FParameterGUIDefinition
    definition = eii.Definition()
    
    return None
