""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FParametricVolStruct.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FParametricVolStruct- Module which calculates volatility structures

DESCRIPTION
    This is the start-script for the procedure to calculate and store
    volatility strucutres. It mainly contains the parameter GUI. 
    The script FParametricVolStructPerform then takes
    over the execution of the procedure.
----------------------------------------------------------------------------"""


import FBDPGui
reload(FBDPGui)

ScriptName = 'FParametricVolStruct'
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', 
        ScriptName)

qVolatilities = FBDPGui.insertVolatilities()

# Tool Tips

ttUpdateATMRef = ('Update the ATM references of skews according '
            'to the forward prices of the underlying instrument.')
ttVolStructures = 'Recalculate these Volatility Structures.'
ttMoveTo = 'Choose to move the points/skew to Mid, Last or Call/Put.'

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['UpdateATMRef',
                'Update ATM References',
                'int', ['0', '1'], None,
                0, 0, ttUpdateATMRef],
        ['VolStructures',
                'Volatility Structures',
                'FVolatilityStructure', None, qVolatilities,
                None, 1, ttVolStructures, None, None],
        ['MoveTo',
                'Move To',
                'string', ['Mid', 'Call/Put', 'Last'], None,
                0, 0, ttMoveTo, None, None],
)


def ael_main(dictionary):

    import FBDPCommon
    reload(FBDPCommon)
    import FBDPCurrentContext
    import FParametricVolStructPerform
    reload(FParametricVolStructPerform)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['ScriptName'] = 'Calculate Volatility Structures'
    FBDPCommon.execute_script(FParametricVolStructPerform.perform, dictionary)

