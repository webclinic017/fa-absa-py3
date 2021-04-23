"""-----------------------------------------------------------------------
MODULE
    LimitMonitoring

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Monitors a trading manager limit column and send out an email if a limit is breached.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Marco Cerutti
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2011-08-22 744507    Herman Hoon        Updated the worksheetreport_dict to include Color Information for 2010.2

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael
import xml.etree.ElementTree
import FBDPGui
reload(FBDPGui)
import FWorksheetReport
import traceback
import os.path
import smtplib
from email.mime.text import MIMEText
from datetime import date
import re
import LimitUtils
reload (LimitUtils)

#-- SETUP GUI -----------------------------------------------------------------------
#------------------------------------------------------------------------------------
""" M.CERUTTI
    Idea here is to get the user to select the workbookreport and save params to a task, 
    then we determine all the limit monitoring related stuff by parsing the task, 
    and then the workbook, then executing our script
"""
ttWorkbook = 'The workbook to evaluate.'
ttSheetInactive = "A workbook has to be selected to use this field. "
ttDate = 'The date to evaluate the limit on.'
ttCustomDate = 'Insert your own custom date here'
ttEndDateInactive = "A custom date has to be selected to use this field. "
ttbreachColumnNames = "The Name of the Sheet Column that will be used to determine the breach criteria. "
ttbreachEmailTo = "The recipient(s) of the limit breach notification."
ttDirectory = 'The file path to the directory where the report should be saved.'
ttGrouper = 'Set the custom grouper if one is used in the underlying portfolio.'


LEFT_JUSTIFY_WIDTH = 16

worksheetreport_dict = {
'wbName': '',
'template': '',
'instrumentParts': 'False',
'snapshot': 'True',
'multiThread': 'True',
'numberOfReports': '5',
'updateInterval': '60',
'portfolios': [],
'tradeFilters': [],
'storedASQLQueries': [],
'trades': [],
'tradeRowsOnly': 'True',
'portfolioRowOnly': 'False',
'zeroPositions': 'False',
'expiredPositions': 'False',
'instrumentRows': 'True',
'clearSheetContent': 'False',
'grouping': [],
'HTML to File': 'False',
'HTML to Screen': 'False',
'HTML to Printer': 'False',
'File Path': 'C:\\temp',
'File Name': '',
'File date format': '%y%m%d%H%M%S',
'File date beginning': 'False',
'Create directory with date': 'False',
'Date format': '%d%m%y',
'Overwrite if file exists': 'True',
'Print template (XSL)': 'FStandardTemplate',
'Print style sheet (CSS)': 'FStandardCSS',
'Secondary output': 'True',
'Secondary template': 'FTABTemplate',
'Secondary file extension': '.xls',
'Include Raw Data': 'True',
'Include Full Data': 'False',
'Include Formatted Data': 'True',
'Include Default Data': 'False',
'Include Color Information':'False',
'XML to File': 'False',
'Compress Output': 'False',
'Send XML File to AMB': 'False',
'AMB XML Message': 'False',
'AMB Address': '',
'AMB Sender Name': '',
'AMB Subject': '',
'Performance Strategy': 'Periodic full GC to save memory',
'gridOutput': 'False',
'gridUseLoopbackGridClient': 'False',
'gridRowPartitionCbClass': 'FReportGridCallbacks.RowPartitionManager',
'gridRowPartitionCbArg': '',
'gridAggregateXmlCbClass': 'FReportGridCallbacks.AggregateXmlManager',
'gridTimeout': 60,
'preProcessXml': '',
'function': '',
'param': '',
'FPortfolioSheet_overrideSheetSettings': 'True',
'FPortfolioSheet_Portfolio Hide Expired Positions Choice': '',
'FPortfolioSheet_Portfolio Hide Zero Positions Choice': '',
'FPortfolioSheet_Portfolio Price Source': '',
'FPortfolioSheet_Credit Delta DayCount': '',
'FPortfolioSheet_Credit Delta Displayed Rate': '',
'FPortfolioSheet_Credit Delta RateType': '',
'FPortfolioSheet_Portfolio Profit Loss Start Date': '',
'FPortfolioSheet_Portfolio Profit Loss Start Date Custom': '',
'FPortfolioSheet_Portfolio Profit Loss End Date': 'Custom Date',
'FPortfolioSheet_Portfolio Profit Loss End Date Custom': '',
'FPortfolioSheet_Portfolio Profit Loss Use MtM Today': '',
'FPortfolioSheet_Portfolio Trade Filter Match Choice': '',
'FPortfolioSheet_Valuation Date': '',
'FTimeSheet_overrideSheetSettings': 'False',
'FTimeSheet_PL Valuation Date': '',
'FTimeSheet_PL Valuation Date Custom': '',
'FTradeSheet_overrideSheetSettings':'False',
'FTradeSheet_Portfolio Profit Loss Start Date': '',
'FTradeSheet_Portfolio Profit Loss Start Date Custom': '',
'FTradeSheet_Portfolio Profit Loss End Date': '',
'FTradeSheet_Portfolio Profit Loss End Date Custom': '',
'FTradeSheet_Portfolio Profit Loss Use MtM Today': ''
}

def DirectorySelection():
    dir_selection = acm.FFileSelection()
    dir_selection.PickDirectory(True)
    return dir_selection


def breachEmail(breached_items, wbName, report_date, breachColumn, breachColumnValue, sendTo=LimitUtils.SMTP_YOU[0]):
    """ Run the report on the worksheet if there was a breach """
    
    '''data is a list containing a list of items with indexes:
        0: worksheet name
        1: physical portfolio oid
        2: tuple of breached instrument names
        3: tuple of ordered grouper names
    '''
     
    data = [(k[0], k[1], v[0], v[1]) for (k, v) in breached_items.iteritems() if v]
    
    if data:
        ael_variables = []
        worksheetreport_dict['wbName'] = wbName
        worksheetreport_dict['File Name'] = wbName
        worksheetreport_dict['FPortfolioSheet_Portfolio Profit Loss End Date Custom'] = report_date
        
        FWorksheetReport.ael_main(worksheetreport_dict)

        reportfile = LimitUtils.YDRIVE
        
        #Now create the body of the email
        body = []
        for d in data:
            body.append(
'''\
--------------------------------------------
WorkSheet:   %s
Portfolio:   %s
Grouped by:  %s

Instruments with breaches in this portfolio:
%s
''' % ( d[0],                                                           
        acm.FPhysicalPortfolio[d[1]].Name(), \
        d[3], \
        "\n".join(LimitUtils.unique_sorted_sequence([t for t in d[2] if t])) \
        ))

        #Message headers and body. Here we only create a plain text email with no attachments

        msg = '''\
This email generated because a breach has occured:

Column:      %s 
Value:       %s 
Report file: %s 

BREACH DETAILS:
Workbook:    %s
%s
''' % ( breachColumn,
        breachColumnValue,
        reportfile, 
        worksheetreport_dict['wbName'], 
        "\n".join(body))
            
        #SMTP section -- generate and send the email
        #print msg
        msg = MIMEText(msg)
        
        smtp_mailserver = LimitUtils.SMTP_MAILSERVER
        smtp_me = LimitUtils.SMTP_ME
        smtp_you = sendTo

        
        msg['Subject'] = 'Limit Breach in workbook: %s' % worksheetreport_dict['wbName']
        msg['From'] = smtp_me
        msg['To'] = ";".join(smtp_you)
    
        print "Sending the email message to: ", msg['To']
        s = smtplib.SMTP(smtp_mailserver)
        s.sendmail(smtp_me, smtp_you, msg.as_string())
        s.quit()
 
    return "Breached"

def recurse_tree(node, calc_space, column_id, breached_nodes=[], breachValue="Breached"):
    """Recurse grid and compute values"""
    
    node_calc = calc_space.CreateCalculation(node, column_id)   #get value of node
    
    #print node_calc.FormattedValue().ljust(LEFT_JUSTIFY_WIDTH), node.Item().StringKey()
    
    if node_calc.FormattedValue() == breachValue:
        breached_nodes.append(node.Item().StringKey())
    
    #recurse tree
    if node.NumberOfChildren():
        child_iter = node.Iterator().FirstChild()
        while child_iter:
            recurse_tree(child_iter.Tree(), calc_space, column_id, breached_nodes, breachValue)
            child_iter = child_iter.NextSibling()
    
    return breached_nodes

def determineGroupers(sheets, default_grouper):
    """ This is very specific to the structure of the worksheet XML.
        No way around it as internal parser throws error saying it can't
        find FGuiTree node, which does in fact exist.
        
        This code finds the top level nodes of the worksheet, retrieves
        grouper information for them and returns it
    """
    oid = 0
    s = ''
    portfolio_groupers = []
    for s in sheets:

        tree = xml.etree.ElementTree.XML(s.Text())
        #print s.Text()

        nodeFPortfolioTreeBuilder = tree.findall(
             ".//FGuiTree/Element/FPortfolioTree/builder/FPortfolioTreeBuilder")

        for node in nodeFPortfolioTreeBuilder:

            oid = node.find('portfolio//StorageId/ptrint').text
            
            if default_grouper:
                portfolio_groupers.append((s.SheetName(), oid, default_grouper.Grouper(), str(default_grouper.Grouper().Groupers()[0].Method())))
            else:
                groupers = node.find('grouper')
                
                #check first for chained groupers
                names = [name.text for name in groupers.findall('FChainedGroupers/groupers/FArray/FAttributeGrouper/method/FSymbol/Text/string')]

                if not names:   #we checked first for chained groupers, if none we check for a single grouper  
                    names = [name.text for name in groupers.findall('.//label//string')]
                
                name = ''
                if names:
                    name = names[0]
                
                grouper = acm.Risk().GetGrouperFromName(name)   

                portfolio_groupers.append((s.SheetName(), oid, grouper, name))
    
    return portfolio_groupers

def scanForLimits(portfolio_groupers, report_date, sheetType='FPortfolioSheet', columnId=LimitUtils.DEFAULT_LIMIT_COLUMN_ID,
                    breachColumnValue="Breached", context=LimitUtils.EXTENSION_CONTEXT):
    """ Create a calculation space, and check for limit breaches for each portfolio
    """

    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
    result = {}

    msg = "Scanning for Limit Breaches:"
    #print msg, "\n", "-" * len(msg)

    try:
        # portfolio_groupers is defined as:
        #    (s.SheetName(), oid, (groupers))
        # and is sorted by sheet, then portfolio oid

        for row in portfolio_groupers:
            portfolio = acm.FPhysicalPortfolio[row[1]]

            if portfolio:
                topNode = calcSpace.InsertItem(portfolio)

                grouper = row[2]
                topNode.ApplyGrouper(grouper)
                try:
                    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', report_date)
                    calcSpace.Refresh()

                    #print "\nPortfolio:".ljust(LEFT_JUSTIFY_WIDTH), portfolio.Name()
                    #print "Grouper(s):".ljust(LEFT_JUSTIFY_WIDTH), ", ".join(row[2])

                    breached_nodes = recurse_tree(topNode, calcSpace, columnId, [], breachColumnValue)
                    if breached_nodes:
                        result[(row[0], row[1])] = (breached_nodes, row[3])

                finally:
                    calcSpace.Clear()
                    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')

    except Exception, e:
        pass
        acm.Log("Exception when scanning for limits: " + str(e))

    return result

def wb_cb(index, fieldValues):
    
    wb = acm.FWorkbook[fieldValues[index]]
    
    ael_variables.sheet_names.enable(wb, ttSheetInactive)
    
    if wb:
        #sheet names
        names = [s.SheetName() for s in wb.Sheets() if s.IsKindOf('FPortfolioSheet')]
        sheets = [s for s in wb.Sheets() if s.IsKindOf('FPortfolioSheet')]
        ael_variables.sheet_names[3] = names
        fieldValues[ael_variables.sheet_names.sequenceNumber] = ", ".join(names)
        
    else:
        fieldValues[ael_variables.sheet_names.sequenceNumber] = ""
        
    return fieldValues 

def date_cb(index, fieldValues):

    endDate = fieldValues[index]
    
    if endDate == 'Custom Date':
        ael_variables.endDateCustom.enable(endDate, ttCustomDate)
    else:
        ael_variables.endDateCustom.enable(None, ttEndDateInactive)
    
    fieldValues[ael_variables.endDateCustom.sequenceNumber] = LimitUtils.EndDateList[endDate]
        
    return fieldValues 


workbooks = [wb for wb in acm.FWorkbook.Select('createUser = ' + str(acm.FUser[acm.UserName()].Oid()))]
workbooks.sort()

ael_variables = FBDPGui.LogVariables(
    ['workbook', 'Workbook_Limit Check', 'FWorkbook', workbooks, None, 1, 0, ttWorkbook, wb_cb, 1],
    ['sheet_names', 'Portfolio Sheets_Limit Check', 'string', [], None, 0, 1, ttSheetInactive, None, 1],
    ['endDate', 'End Date_Limit Check', 'string', LimitUtils.EndDateListSortedKeys, 'Now', 1, 0, ttDate, date_cb, 1],
    ['endDateCustom', 'End Date Custom_Limit Check', 'string', None, LimitUtils.EndDateList['Now'], 1, 0, ttEndDateInactive, None, 0],
    ['breachEmailTo', 'Breach Email Recipients_Limit Check', 'string', LimitUtils.SMTPYouSortedKeys, LimitUtils.SMTPYouSortedKeys[0], 1, 1, ttbreachEmailTo, None, 1],
    ['breachColumn', 'Breach Column Name_Limit Check', 'string', LimitUtils.BreachColumnsSortedKeys, LimitUtils.BreachColumnsSortedKeys[0], 1, 0, ttbreachColumnNames, None, 1],
    ['filePath', 'File Path_Limit Check', DirectorySelection(), None, DirectorySelection(), 0, 1, ttDirectory, None, 1],
    ['grouping', 'Grouping_Limit Check', 'FStoredPortfolioGrouper', None, '', 0, 1, ttGrouper, None, 1]
    )

def ael_main(dictionary):
    wb = dictionary['workbook']
    sheets = [s for s in wb.Sheets() if s.IsKindOf('FPortfolioSheet')]
    
    if dictionary['grouping']:
        grouping = dictionary['grouping'][0]
    else:
        grouping = None
    
    portfolio_groupers = determineGroupers(sheets, grouping)
    
    
    if dictionary['endDate'] == 'Custom Date':
        report_date = dictionary['endDateCustom']
    else:
        report_date = LimitUtils.EndDateList[dictionary['endDate']]
    
    worksheetreport_dict['File Path'] = dictionary['filePath']
    
    breached_items = scanForLimits(     portfolio_groupers, 
                                        report_date,
                                        'FPortfolioSheet',
                                        dictionary['breachColumn'],
                                        LimitUtils.BREACH_COLUMNS[dictionary['breachColumn']]['value'],
                                        LimitUtils.BREACH_COLUMNS[dictionary['breachColumn']]['context'])
                                        
    breachEmail(breached_items, 
                wb.Name(), 
                report_date, 
                dictionary['breachColumn'],
                LimitUtils.BREACH_COLUMNS[dictionary['breachColumn']]['value'],
                dictionary['breachEmailTo'])
