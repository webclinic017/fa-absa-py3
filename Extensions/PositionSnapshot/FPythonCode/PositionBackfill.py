import acm
import PositionSnapshotCorrectCreateTask

type_tt = "The type of value sessions to be created."
disposition_tt = "The data disposition for which the value sessions will be created."
calcEnv_tt = 'When running backfill tasks, only the default calculation environment can be used.'
calendar_tt = 'Business day calendar used to decides backfill dates. If left empty, the calendar of the accounting currency will be used.'
fromDate_tt = 'Start of date range for which backfill snapshots are to be created.'
toDate_tt = 'End of date range for which backfill snapshots are to be created.'

def StartPositionBackfill(eii):
    acm.RunModuleWithParameters("PositionBackfill", acm.GetDefaultContext()) 

def DefinitionFromAelVariables( aelVariables ):
    definition = acm.FDictionary()
    definition.AtPut(acm.FSymbol('disposition'), aelVariables['disposition'])
    definition.AtPut(acm.FSymbol('sessionType'), aelVariables['sessionType'].StringKey())
    definition.AtPut(acm.FSymbol('calendar'), aelVariables['calendar'])
    definition.AtPut(acm.FSymbol('fromDate'), aelVariables['fromDate'])
    definition.AtPut(acm.FSymbol('toDate'), aelVariables['toDate'])
    return definition

dispositions = acm.FPositionDataDisposition.Select('').SortByProperty('Name', True)
sessionTypes = acm.FValueSessionType.Select('').SortByProperty('Name', True)
calculationEnvironments = acm.FStoredCalculationEnvironment.Select('').SortByProperty('Name', True)
calendars = acm.FCalendar.Select('').SortByProperty('Name', True)

ael_variables = [
[       'disposition',  'Data Disposition',  'FPositionDataDisposition', dispositions, None, 1, 0, disposition_tt, None, True],
[       'sessionType',  'Value Session Type',  'FValueSessionType',      sessionTypes, None, 1, 0, type_tt, None, True],
[       'calculationEnvironment', 'Calculation Environment', 'string', None, '<Default Calculation Environment>', 0, 0, calcEnv_tt, None, False],
[       'calendar', 'Calendar', acm.FCalendar, calendars, None, 0, 0, calendar_tt, None, True],
[       'fromDate', 'Start Date', 'date', None, None, 1, 0, fromDate_tt, None, True],
[       'toDate', 'End Date', 'date', None, None, 1, 0, toDate_tt, None, True]
]
    
def ael_main(vars):
    definition = DefinitionFromAelVariables(vars)
    return PositionSnapshotCorrectCreateTask.CreateActivity(definition)
