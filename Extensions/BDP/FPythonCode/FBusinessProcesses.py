""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_processes/etc/FBusinessProcesses.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""---------------------------------------------------------------------------
MODULE
    FBusinessProcess - Business processes tasks GUI base implementation

DESCRIPTION

NOTE

ENDDESCRIPTION
---------------------------------------------------------------------------"""
import sys

import acm

import FBDPCustomSingleDlg
import FBDPGui

global ael_vars
ael_vars = None

def init(script_name, ael_variables_to_prepend):
    #Setup GUI with default parameters
    FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters(
        'FBDPParameters', script_name
    )
    ael_v = Gui(
        script_name=script_name,
        ael_variables_to_prepend=ael_variables_to_prepend
    )
    setattr(sys.modules[__name__], 'ael_vars', ael_v)
    return ael_v

class Gui(FBDPGui.TestVariables):
    def __init__(self, script_name, ael_variables_to_prepend):
        #Setup intended AEL variables
        if isinstance(ael_variables_to_prepend, (list, set)):
            ael_variables_to_prepend = tuple(ael_variables_to_prepend)

        assert isinstance(ael_variables_to_prepend, tuple)
        self.script_name = None
        self.state_chart = None

        #Tooltips
        ttDate = (
            'Action will be performed on processes '
            'that have remained in the same state since this date'
        )
        ttStateChart = 'Filter business process based on it\'s state chart.'
        ttStates = (
            'Perform task on business processes currently in one of '
            'these states'
        )

        days = [
            acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year'
        ]

        variables = ael_variables_to_prepend + (
            #[VariableName,
            #    DisplayName,
            #    Type, CandidateValues, Default,
            #    Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
            ['Date',
                    'Not changed since',
                    'string', days, 'Today',
                    1, False, ttDate, None, True, None],
            ['StateChart',
                    'State chart',
                    acm.FStateChart, None, None,
                    1, False, ttStateChart, self.stateChartCb, True, None],
            ['States',
                    'States',
                    'string', None, None,
                    0, True, ttStates, None, False, self.customStatesDialog]
        )
        super(Gui, self).__init__(*variables)
        self.script_name = script_name

    def stateChartCb(self, index, field_values):
        ttStatesDisabled = 'Select a valid state chart to enable'
        state_chart_id = field_values[index]
        self.state_chart = acm.FStateChart[state_chart_id]
        states_var = getattr(self, 'States')
        states_var.enable(bool(self.state_chart), ttStatesDisabled)
        if not self.state_chart:
            field_values[states_var.sequenceNumber] = None

        return field_values

    def customStatesDialog(self, shell, params):
        cb = lambda: [s.Name() for s in self.state_chart.States()]
        customDlg = FBDPCustomSingleDlg.SelectItemCustomDialog(
            shell=shell, params=params, selectionName='state chart states',
            getObjectChoicesCb=cb
        )
        return customDlg.Create()

def aelMain(performer_module, params):
    params['ScriptName'] = ael_vars.script_name
    states = dict((s.Name(), s) for s in params['StateChart'].States())
    params['States'] = [states[s] for s in params['States']]

    #Import Front modules
    import FBDPCommon
    import FBDPCurrentContext

    #Create logger
    FBDPCurrentContext.CreateLog(
        ScriptName=ael_vars.script_name,
        LogMode=params['Logmode'],
        LogToConsole=params['LogToConsole'],
        LogToFile=params['LogToFile'],
        Logfile=params['Logfile'],
        SendReportByMail=params['SendReportByMail'],
        MailList=params['MailList'],
        ReportMessageType=params['ReportMessageType']
    )
    #Execute relevant perform script
    FBDPCommon.execute_script(performer_module.perform, params)
