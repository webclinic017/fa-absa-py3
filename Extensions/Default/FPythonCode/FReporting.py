"""-------------------------------------------------------------------------------------------------------
MODULE
    FReporting - Produce a report for a workbook or a sheet template
    containing Portfolio sheets or Trade sheets.
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import FReportOutput
import acm
import re


def addColumnCreators(reportGrid, columnIDs, context):
    gridBuilder = reportGrid.GridBuilder()
    reportColumnCreators = gridBuilder.ColumnCreators()
    columnCreators = acm.GetColumnCreators(columnIDs, context)
    for i in range(columnCreators.Size()):
        columnCreator = columnCreators.At(i)
        reportColumnCreators.Add(columnCreator)
        
    return reportColumnCreators
    
def applySheetSettings(sheetSettingsDict, reportGrid):
    for columnID in sheetSettingsDict.keys():
        value = sheetSettingsDict[columnID]
        simSucceded = reportGrid.SimulateGlobalValue(columnID, value)
        if not simSucceded:
            raise Exception, "Could not set Sheet Setting " + \
                    columnID + " to " + str(value)


def getColumns(templateName, tag):
    template = acm.FTradingSheetTemplate.Select01('name = ' + templateName, '')
    sheet = template.TradingSheet()
    createContext = acm.FColumnCreatorCreateContext(tag)
    columns = sheet.ColumnCollection(createContext)
    dict = {}
    for col in columns:
        dict[str(col.ColumnId())] = col
    return dict


def generateXMLString(reportName, sheets, portfolios, grouper, sheetSettings, includeExpired,
                      includeInactive, includeFormattedData, includeRawData, buildChildren, showSingleRows,
                      buildInstrumentParts, snapshot, context, matchPerPortfolio = 0):
    outputs = []
    for sheetDict in sheets:
        output = acm.FXmlReportOutput('')
        output.EnableWhitespace(False)
        type = sheetDict['Type']
        reportGrid = acm.Report.CreateReport(reportName, output)
        sheetInstance = acm.Create(sheetDict['Type'])
        try:
            reportGrid.OpenSheet(sheetInstance)
            applySheetSettings(sheetSettings, reportGrid)
        except Exception as msg:
            extendedMsg = "Failed to create report: " + str(msg)
            raise Exception(extendedMsg)
        addColumnCreators(reportGrid, sheetDict['ColumnIDs'], context)
        output.IncludeFormattedData(includeFormattedData)
        output.IncludeRawData(includeRawData)
        builder = reportGrid.GridBuilder()
        reportGrid.SimulateGlobalValue('Portfolio Trade Filter Match Choice', 'Match Per Physical Portfolio')
        for prf in portfolios:
            n = builder.AddPortfolio(prf, grouper, None, buildChildren, buildInstrumentParts, includeInactive,\
            True, includeExpired, showSingleRows)
        reportGrid.Generate()
        outputs.append(output.AsString())
    return outputs

def getGrouperDictionary():
    grouperDict1 = acm.Risk().GetAllPortfolioGroupers()
    grouperDict = {}
    for k in grouperDict1.Keys():
        grouperDict[str(k)] = grouperDict1[k]
    grouperDict['Default'] = acm.FDefaultGrouper()
    grouperDict['Subportfolio'] = acm.FSubportfolioGrouper()
    grouperDict['Portfolio Level']= acm.FDefaultGrouper()
    return grouperDict

def parseBucketGrouper(stringTuple):
    """ Attempt to convert string s to timebucketgrouper  return 0 on failure"""
    if not stringTuple : return None
    s = ''
    for part in stringTuple:
        s += part + ','
    g = re.compile(r"""
            .*timebucket\(                          # match timebucket(
            [\s]*(expiry|cashflow)[\s]*             # match expiry or cashflow
            ((?:[\s]*,[\s]*(?:[\d]+(?:m|y|d)))*)    # match ,11m,2d,3y...
            [\s]*\)                                 # match  ) """
            , re.I+re.VERBOSE).search(s)
    if g:
        bucktype, dates = g.groups()
        newbuckets = acm.FTimeBuckets(bucktype.lower())
        dates = re.compile(r"""
                    ([\d]+(?:m|y|d))                # match 11m """
                    , re.I+re.VERBOSE).findall(dates)
        for date in dates:
            newbuckets.AddBucket(date, date)
        return acm.FTimeBucketGrouper(newbuckets)
    return None


def getAttributeGrouper(groupName):
    """
    Returns None or the FAttributeGrouper object for the string group name.
    """

    grouper = None
    try:
        grouper = acm.FAttributeGrouper(groupName)
    except:
        pass

    return grouper


def getListOfGroupersFromNames(groupNames):
    """
    Returns the only grouper or a chained grouper for the list of group name
    strings.
    """

    # If there is only one grouper and it is an FStorePortfolioGrouper or an FGrouper, 
    # return it immediately.
    if len(groupNames) == 1:
        try: 
            if groupNames[0].IsKindOf(acm.FStoredPortfolioGrouper): 
                return groupNames[0].Grouper()
            elif groupNames[0].IsKindOf(acm.FGrouper): 
                return groupNames[0]
        except: 
            pass 

    # If the groupNames refers to a single time bucket grouper, return the time
    # bucket grouper.
    timebuckGrouper = parseBucketGrouper(groupNames)
    if timebuckGrouper:
        return timebuckGrouper

    # Find out the current groupers available in the system.
    grouperDict = getGrouperDictionary()

    # Find the grouper for each group name in the list.  Throw error if there
    # isn't a grouper for a group name.
    groupers = []
    for groupName in groupNames:

        foundGrouper = None
        if grouperDict.has_key(groupName):
            foundGrouper = grouperDict[groupName]
            # GetAllPortfolioGroupers returns FStoredPortfolioGrouper
            # instances for the groupers in the database
            if foundGrouper and foundGrouper.IsKindOf(acm.FStoredPortfolioGrouper):
                foundGrouper = foundGrouper.Grouper()
        else:
            foundGrouper = getAttributeGrouper(groupName)

        if not foundGrouper:
            raise RuntimeError('No such grouper %s' % groupName)

        if foundGrouper.IsKindOf(acm.FChainedGrouper):
            for g in foundGrouper.Groupers():
                groupers.append(g)
        else:
            groupers.append(foundGrouper)

    # Return None, the only grouper, or the chained grouper of all groupers.
    grouper = None
    if groupers:
        if len(groupers) > 1:
            grouper = acm.CreateWithParameter('FChainedGrouper', groupers)
        else:
            grouper = groupers[0]
    return grouper


def fileNameFromPortfolioList(portfolioList, fileName=None):
    if fileName == None:
        fileName = 'portfolio_report' + '_' + portfolioList[0].Name().replace('/', '')
        if len(portfolioList)>1:
            fileName += '_etc'
    return fileName

def getXMLString(columnIDs, portfolios, sheetSettings, grouperNames, context, name,\
                 showSingleRows, includeExpired, includeInactive, includeFormattedData,\
                 includeRawData, buildInstrumentParts, snapshot=1, matchPerPortfolio = 0):
    if not grouperNames:
        grouper = acm.FDefaultGrouper()
    else:
        grouper = getListOfGroupersFromNames(grouperNames)
    sheetDict = {}
    sheetDict['ColumnIDs'] = columnIDs
    sheetDict['Name'] = name
    sheetDict['Type'] = 'FPortfolioSheet'
    sheets = [sheetDict]
    return generateXMLString(name, sheets, portfolios, grouper, sheetSettings, includeExpired,
                      includeInactive, includeFormattedData, includeRawData, 1, showSingleRows, 
                      buildInstrumentParts, snapshot, context, matchPerPortfolio)[0]

def createPortfolioReport(columnIDs, portfolios, grouperNames=None, context=None, name="PortfolioReport",\
                          filePath=None, fileName=None, createDateDirectory=None, showSingleRows=1, includeExpired=0,\
                          includeInactive=0, xmlToFile=None, htmlToFile=None, includeFormattedData=1,\
                          includeRawData=1, sheetSettings={}, snapshot=1, matchPerPortfolio = 0):
    trueFalse = ['False', 'True']
    if not context:
        context = acm.GetDefaultContext()
    fileName = fileNameFromPortfolioList(portfolios, fileName)
    reportOutput = FReportOutput.getAelVariables()
    outputDict = {'HTML to Screen':trueFalse[False]}
    if filePath != None:
        outputDict['File Path'] = filePath
    if xmlToFile != None:
        outputDict['XML to File'] = trueFalse[xmlToFile]
    if htmlToFile != None:
        outputDict['HTML to File'] = trueFalse[htmlToFile]
    if createDateDirectory != None:
        outputDict['Create directory with date'] = trueFalse[createDateDirectory]
    dict = {}
    for row in reportOutput:
        key = row[0]
        value = row[4]
        if outputDict.has_key(key):
            dict[key] = outputDict[key]
        else:
            dict[key] = value
    XML = getXMLString(columnIDs, portfolios, sheetSettings, grouperNames, context,\
                            name, showSingleRows, includeExpired, includeInactive,\
                            includeFormattedData, includeRawData, 1, snapshot, matchPerPortfolio)
    FReportOutput.produceOutput(XML, fileName, dict)
