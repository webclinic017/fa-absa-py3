import ael, time
import acm
from FPLReport import *
import FRiskMatrix
import FPLReport
reload(FPLReport)

print "PLPrimeRun...."

def run(fobject, **settings):
    print "Run PLReport, using FPLReport"
    print settings['PLContext']
    print settings['PLReportType']
    apply(FPLReport.run_report, (fobject,), settings)
    return time.time()

###################################################
# Globals
###################################################

"""---------  Report File Type  ---------"""
RFT     = "Default"
RFT_TAB = "Tab" # Tab separated report to be used for example import to excel.

YES = "Yes"
NO  = "No"

ISO = 'ael.DATE_ISO'

FILE = 'c:/plreport/'

ACC = 'Accounting'

CONTEXT = 'Standard'
NOW = str(ael.date_today())


pfs       = FRiskMatrix.pf()
tfs       = FRiskMatrix.tf()
contexts  = FRiskMatrix.contextNames()
repTypes  = [PORTFOLIO, POSITION, TRADE]
Intervals = [WEEK, MONTH, YEAR, PERIOD]
Periods   = [DAY, WEEK]
RFTs      = [RFT, RFT_TAB]
YesOrNo   = [YES, NO]
ShowCurrs = [ACC, PORTFOLIO]
Calendars = [ACC]
Formats   = [ISO]
FileNames = [FILE]
Dates     = [NOW]
Columns   = "Position,RPL,UPL,TPL,Cash,MarketValue,Fees,Div"
AllColumns = [
'Position', 'RPL', 'nRPL', 'dRPL', 'UPL', 'nUPL', 'dUPL', 'TPL', 'nTPL', 'dTPL', 'MaUPL',
'nMaUPL', 'dMaUPL', 'MaTPL', 'nMaTPL', 'dMaTPL', 'Cash', 'nCash', 'dCash',
'MarketValue', 'nMarketValue', 'dMarketValue', 'Fees', 'nFees', 'dFees', 'Div',
'nDiv', 'dDiv', 'RPL-NewPL', 'Diff-Rpl', 'Position']
ael_variables = [\
('PLInterval',       'Interval',         'string', Intervals,  YEAR),
('PLShowEndDate',    'Show End Date',    'string', YesOrNo,    YES),
('PLShowPeriod',     'Show Period',      'string', YesOrNo,    YES),
('PLCalendar',       'Calendar',         'string', Calendars,  ACC),
('PLDateFormat',     'Date Format',      'string', Formats,    ISO),
('PLFileName',       'File Name',        'string', FileNames,  FILE),
('tf',               'Trade Filters',    'string', tfs,        None, 0),
('PLShowCurr',       'Show Curr',        'string', ShowCurrs,  ACC),
('PLReportType',     'Report Type',      'string', repTypes,   POSITION),
('pf',               'Portfolios',       'string', pfs,        'JENAHL01'),
('PLContext',        'Context',          'string', contexts,   CONTEXT),
('PLColumns',        'Columns',          'string', AllColumns, Columns, 0, 1),
('PLReportFileType', 'Report File Type', 'string', RFTs,       RFT),
('PLShowStartDate',  'Show Start Date',  'string', YesOrNo,    YES),
('PLIncludeExpired', 'Include Expired',  'string', YesOrNo,    YES),
('PLStartDate',      'Start Date',       'string', Dates,      None, 0),
('PLEndDate',        'End Date',         'string', Dates,      NOW),
('PLPeriodInterval', 'Period Interval',  'string', Intervals,  PERIOD)
]

def ael_main(dict):
    server        = acm.getServerObject()
    portfolioName = dict.get('pf')
    dict['PLFileName'] = "'" + dict['PLFileName'] + "PlPrime_'+settings["\
    "'PLReportType']+'_'+name_str+'_'+str(ael.date_today())+'%N.txt'"
    if portfolioName:
        selectString  = 'name = "' + portfolioName + '"'
    else:
        raise 'No Portfolio.'
    fobject       = server.GetClass('FPhysicalPortfolio').Select01(selectString, '')
    if not fobject:
        fobject = server.GetClass('FCompoundPortfolio').Select01(selectString, '')
    apply(run, (fobject,), dict)





