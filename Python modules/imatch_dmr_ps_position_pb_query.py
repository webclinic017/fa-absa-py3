"""

This script is used to produce the iMatch  extract for settled trades for Prime Brokerage Trading.

Date: 2014-10-20
Requester: Thulsie Gasant
Developer: Manan Ghosh

"""

import acm
import time
import FRunScriptGUI
import os
import csv
import re
from types import *

acm_time = acm.Time()
TODAY = acm_time.DateToday()


dates = {
   'Today': TODAY,
   'Previous Business Day': acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(TODAY, -1),
   'Yesterday': acm_time.DateAddDelta(TODAY, 0, 0, -1),
   'Two Days Ago':  acm_time.DateAddDelta(TODAY, 0, 0, -2),
   'First Day of the Week': acm_time.FirstDayOfWeek(TODAY),
   'First Day of the Month': acm_time.FirstDayOfMonth(TODAY),
   'Custom Date': TODAY
}

tradeFilterKey = 'TRADE_FILTER'

outputDirectoryKey = 'OUTPUT_DIRECTORY'
outputSelection = FRunScriptGUI.DirectorySelection()

outputFileKey = 'OUTPUT_FILE'

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

ael_gui_parameters = {
    'windowCaption' : 'iMatch PB Position File'
}

columndefs =   [['Type', 'Instrument Type'],
                ['UnderlyingOrSelf', 'UnderlyingOrSelf'],
                ['Trade Portfolio', 'Trade Portfolio'],
                ['Counterparty', 'Cash Equity Counterparty'],
                ['Val End', 'Portfolio Value End'],
                ['Cash End', 'Portfolio Cash End'],
                ['Daily Execution Fee', 'Daily Execution Fee'],
                ['Fees', 'Portfolio Fees'],
                ['Div', 'Portfolio Dividends'],
                ['PLPosEnd', 'Portfolio Profit Loss Position End'],
                ['PLPeriodStart', 'PLPeriodStart'],
                ['PLPeriodEnd', 'PLPeriodEnd'],
                ['ZAR Cash in ZAR', 'Cash Per Currency - ZAR'],
                ['SAFEX Clearing Fee Excl VAT', 'SAFEX Clearing Fee Excl VAT'],
                ['SAFEX Exchange Fee Excl VAT', 'SAFEX Exchange Fee Excl VAT'],
                ['SAFEX Commission Fee Excl VAT', 'SAFEX Commission Fee Excl VAT'],
                ['SAFEX Total Fee Incl VAT', 'SAFEX Total Fee Incl VAT'],
                ['ISIN', 'ISIN'],
				['Acquire Day', 'Trade Acquire Day']]

def _raiseError(message):
    """ Function to raise and error. """

    func = acm.GetFunction('msgBox', 3)
    func('Error', message, 0)


def getColumn( node, calc_space , column_name, results, type=None):
    """ 
    Get the value of the column from 
    calculation space.
    """

    if not results:
        results = {}    

    if type == "datetime":
        datevalue = dt.datetime.fromtimestamp(calc_space.CalculateValue(node, column_name))
        result = datevalue.strftime("%Y-%m-%d %H:%M:%S")
    elif type == "objectname":        
        result = formatValues(calc_space.CalculateValue(node, column_name).Name())
    else:
        result = formatValues(calc_space.CalculateValue(node, column_name))

    results[node.Item().StringKey()][column_name] = cleanValues(result)

    return results

def getInstrumentISIN(instrument):
    """ 
    Get the ISIN of the non MTM instrument or 
	the non MTM underlying instrument if the 
	ISIN is not available on the MTM instrument.
    """

    ins = acm.FInstrument[instrument]
    ISIN = ins and ins.Isin() or None
    und = ins.Underlying()  	


    if not ISIN:
    	instr = re.sub("/MTM", "", instrument or "" )
        ins = acm.FInstrument[instr]	
        ISIN = ins and ins.Isin()

    if not ISIN:
        ISIN = und and und.Isin() or None

    if not ISIN:
        undinstr = und and und.Name() or None
        undinstr = re.sub("/MTM", "", undinstr or "")
        und = acm.FInstrument[undinstr]

        ISIN = und and und.Isin() or None

    return ISIN

def cleanValues(d):
    """ Clean the value of the column.    """

    return str(d).replace("[]", "")

def formatValues(d):
    """ Format the value of the column.    """

    if type(d) == FloatType:
        return '%0.2f' % (d)

    if type(d) == IntType:
        return '%d' % (d)        

    if type(d) == StringType:
        d = d.replace("'", "")
        return d

    if d.IsKindOf(acm.FDenominatedValue):
        d = d.Number()    
        return '%0.2f' % (d)

    return d

def create_named_param(vector, currency):
    """Simple function that add FNamedParameters
    to passed vector.

    Arguments:
    vector - FArray
    currency - FCurrency
    """
    param = acm.FNamedParameters()
    param.AddParameter('currency', currency)
    vector.Add(param)    


def _getFilepath(directory, file):
    return os.path.join(directory, '%s_%s.csv' % (file[0:-4], time.strftime('%Y%m%d%H%M%S')))

ael_variables = [
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, None, 0, 1, 'Trades Filter to be written to the recon file.', None, 1],
    [outputDirectoryKey, 'Output Directory', outputSelection, None, outputSelection, 1, 1, 'Directory where the file will be created.', None, 1],
    [outputFileKey, 'Output File', 'string', None, None, 1, 1, 'Name of the output file.', None, 1]
]


def GetOutputResults(tradeFilter):
    """ Get the results for the trade filter .    """

    context = acm.GetDefaultContext()
    sheet_type = 'FTradeSheet'


    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheet_type)    

    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', dates['Previous Business Day'])    

    tf = tradeFilter[0]


    if tf:
        topNode = calcSpace.InsertItem(  tf )
        calcSpace.Refresh()

        filtiter = calcSpace.RowTreeIterator().FirstChild()
        childiter = filtiter.FirstChild()        

        itemName = filtiter.Tree().Item().StringKey() 

        currencies = []
        ccy = acm.FCurrency['ZAR']
        currencies.append(ccy)

        vector = acm.FArray()
        for currency in currencies:
            create_named_param(vector, currency)

        cash_per_currency = acm.Sheet.Column().ConfigurationFromVector(vector)         

        results = {}
        print 'Iterating trade filter ...'

        while childiter:
            results[childiter.Tree().Item().StringKey()] = {}

            tree = childiter.Tree()

            results = getColumn(tree, calcSpace, 'Instrument Type', results )

            underlying = calcSpace.CalculateValue(tree, 'Underlying Instrument')
            instrument = calcSpace.CalculateValue(tree, 'Instrument Name')

            
            results[childiter.Tree().Item().StringKey()]['UnderlyingOrSelf'] = underlying if underlying else instrument

            results = getColumn(tree, calcSpace, 'Trade Portfolio', results, "objectname")
            results = getColumn(tree, calcSpace, 'Cash Equity Counterparty', results, "objectname" )
            results = getColumn(tree, calcSpace, 'Portfolio Value End', results )

            results = getColumn(tree, calcSpace, 'Portfolio Cash End', results )

            results = getColumn(tree, calcSpace, 'Daily Execution Fee', results )
            results = getColumn(tree, calcSpace, 'Portfolio Fees', results )

            results = getColumn(tree, calcSpace, 'Portfolio Dividends', results )
            results = getColumn(tree, calcSpace, 'Portfolio Profit Loss Position End', results )
            results = getColumn(tree, calcSpace, 'PLPeriodStart', results )
            results = getColumn(tree, calcSpace, 'PLPeriodEnd', results )

            cpc_vector = calcSpace.CreateCalculation(tree, 'Portfolio Cash Vector', cash_per_currency).Value()   
            cpc_vector = cpc_vector.Number() 
            results[childiter.Tree().Item().StringKey()]['Cash Per Currency - ZAR'] = cpc_vector

            results = getColumn(tree, calcSpace, 'SAFEX Clearing Fee Excl VAT', results )            
            results = getColumn(tree, calcSpace, 'SAFEX Exchange Fee Excl VAT', results )            
            results = getColumn(tree, calcSpace, 'SAFEX Commission Fee Excl VAT', results )            
            results = getColumn(tree, calcSpace, 'SAFEX Total Fee Incl VAT', results )


            ISIN = getInstrumentISIN(instrument)
            results[childiter.Tree().Item().StringKey()]['ISIN'] = ISIN
            results = getColumn(tree, calcSpace, 'Trade Acquire Day', results )			

            childiter = childiter.NextSibling()

        return results

def WriteToFile(filepath, results):
    """  Write the results into the output file.    """

    csvFile = open(filepath, 'w')

    columns =  [column[0] for column in columndefs]
    headers = {}
    for col in columndefs:
        headers[col [0]] = col [1]


    writer = csv.writer(csvFile, lineterminator = '\n')
    writer.writerow(['si_JSE new trades']+columns)


    for result in results.keys():
        row = [results[result][headers[col]] if results[result].has_key(headers[col]) else '' for col in columns if headers.has_key(col) ]
        writer.writerow([result]+row)


    csvFile.close()

def ael_main(parameters):
    """Entry point for task execution."""

    try:
        trades = None

        tradeFilter = parameters[tradeFilterKey]
        if not tradeFilter:
            _raiseError('Please supply value for mandatory parameter Trade Filter.')
            return

        outputDirectory = parameters[outputDirectoryKey]            
        outputFile = parameters[outputFileKey][0]



        filepath = _getFilepath(outputDirectory.SelectedDirectory().Text(), outputFile)
        output = GetOutputResults(tradeFilter)
        WriteToFile(filepath, output)
        print 'Wrote secondary output to:::' + filepath


    except Exception, ex:
        print 'Error while creating trade recon report', str(ex)
