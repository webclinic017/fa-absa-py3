import acm
from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate

import csv

trueFalse = ['True', 'False']

AUTH_GROUP_MAPPING = {'Authorization stage 1': 'Risk',
                      'Authorization stage 2': 'Compliance',
                      'Authorization stage 3': 'Product Control',
                      'Authorization stage 4': 'Product Supervisor'}
STATE_CHART_NAME = 'GenericMandatesAuthorization_v3'
PATH = "C:\Temp\Mandate_AuditTrail.csv"


def GetFirstDayOfYear():
    today = acm.Time.DateToday()
    #return acm.Time.DateAddDelta(today, 0, -1, 0)
    return acm.Time.FirstDayOfYear(today)


def GetLastDayOfYear():
    today = acm.Time.DateToday()
    firstDayOfYear = acm.Time.FirstDayOfYear(today)
    lastDayOfYear = acm.Time.DateAddDelta(firstDayOfYear, 1, 0, -1)
    return lastDayOfYear


def AllowReportDatesEdit(index, fieldValues):
    enableDates = 0 if fieldValues[0] == 'True' else 1
    ael_variables[1][9] = enableDates
    ael_variables[2][9] = enableDates
    return fieldValues


ael_variables = [
    ['editReportDates', 'Use the default report dates.', 'string', trueFalse, 'True', 1, 0, 'Change the default report dates.', AllowReportDatesEdit, 1],
    ['startDate', 'Start Date', 'date', None, GetFirstDayOfYear(), 1, 0, 'Start date of report', None, 1],
    ['endDate', 'End Date', 'date', None, GetLastDayOfYear(), 1, 0, 'End date of report', None, 1],
    ["exportPath", "Export File Location", "string", None, PATH, 1, 0, "Location of output file"],
]


def ael_main(ael_variables):
    getLogger().info('Mandate - Exporting Audit Trail information')
    getLogger().info('Report starting..')

    if ael_variables['editReportDates'] == 'True':
        startDate = GetFirstDayOfYear()
        endDate = GetLastDayOfYear()
    else:
        startDate = ael_variables['startDate']
        endDate = ael_variables['endDate']
    
    path = ael_variables['exportPath']
    getLogger().info('Exporting events captured between %s and %s' % (startDate, endDate))

    # Select business processes linked to TextObjects of type 39
    getLogger().info('Selecting data from the database.')
    bps = acm.FBusinessProcess.Select('subject_type="TextObject" subject_subtype=39')

    with open(path, 'wb') as csvFile:
        getLogger().info('Processing data')
        fileWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Create CSV file headings
        row = ['Mandate Id', 'Mandate Name', 'BP Step Oid', 'State', 'Event', 'Update Time', 'Update User ID',
               'Update User Name', 'Mandate Type', 'Active', 'Query Folders', 'Reason for Amendment', 'Authorizer Group', 'Blocking',
               'Entity', 'Authorizer']
        fileWriter.writerow(row)

        for bp in bps:
            if bp.StateChart().Name() == STATE_CHART_NAME:

                mandateName = "Mandate Deleted"
                mandateId = bp.Subject().Name()
                limit = acm.FLimit[mandateId]
                if limit:
                    mandate = Mandate(limit)
                    if mandate and mandate.Name():
                        mandateName = mandate.Name()

                steps = bp.Steps()
                for step in steps:
                    params = step.DiaryEntry().Parameters()

                    if params['Authorizer Group'] in AUTH_GROUP_MAPPING.keys():
                        authGroup = AUTH_GROUP_MAPPING[params['Authorizer Group']]
                    else:
                        authGroup = params['Authorizer Group']
                    updateTime = acm.Time.DateFromTime(step.UpdateTime())

                    # Check if StartDate <= today <= EndDate
                    if acm.Time.DateDifference(updateTime, startDate) >= 0 and \
                       acm.Time.DateDifference(endDate, updateTime) >= 0:
                       
                        authFullName = ''
                        if params['Authorizer']:
                            authorizer = acm.FUser[params['Authorizer']]
                            if authorizer:
                                authFullName = authorizer.FullName() if authorizer.FullName() else ''
                            
                        row = [mandateId, mandateName, step.Oid(), step.State().Name(), step.Event().Name(), updateTime,
                               step.UpdateUser().Name(), step.UpdateUser().FullName(), params['Mandate type'], params['Mandate Active'],
                               params['Mandate query folders'], params['Mandate Change Reason'], authGroup,
                               params['Mandate blocking type'], params['Mandate target'], params['Authorizer'], authFullName]
                        fileWriter.writerow(row)

    getLogger().info("RunScript has completed executing.")
    
    # Required for RTB 
    acm.Log("Wrote secondary output to {0}".format(path))
    acm.Log("Completed successfully")
    

def StartRunScript(eii):
    del eii
    acm.RunModuleWithParameters("GenericMandatesRunScriptAuditTrail", acm.GetDefaultContext())
