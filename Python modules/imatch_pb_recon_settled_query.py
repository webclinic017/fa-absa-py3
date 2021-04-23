"""

This script is used to produce the iMatch  extract for settled trades for Commodities Trading.

Date: 2014-10-16
Requester: Thulsie Gasant
Developer: Manan Ghosh

"""
import acm
import time
import FRunScriptGUI
import os
import csv
from types import *
import datetime as dt


tradeFilterKey = 'TRADE_FILTER'


outputDirectoryKey = 'OUTPUT_DIRECTORY'
outputSelection = FRunScriptGUI.DirectorySelection()

outputFileKey = 'OUTPUT_FILE'

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

ael_gui_parameters = {
    'windowCaption': 'iMatch PB Recon File'
}

headers = {'Used Price End': 'Portfolio Profit Loss Price End Date',
           'PLPosEnd': 'Portfolio Profit Loss Position End',
           'ZAR Cash': 'Cash Per Currency - ZAR',
           'Fees': 'Portfolio Fees',
           'Total Val End': 'Total Val End',
           'Cash End': 'Portfolio Cash End',
           'O/S_Cash': 'O/S_Cash',
           'Isin': 'ISIN',
           'TradePortfolio': 'Trade Portfolio',
           'Counterparty': 'Trade Counterparty',
           'InsValEnd': 'InsValEnd'}


def _raiseError(message):
    """ Function to raise and error. """
	
    func = acm.GetFunction('msgBox', 3)
    func('Error', message, 0)

def getColumn(key, node, calc_space, column_name, results, type= None):
    """ 
	Get the value of the column from 
    calculation space.
	"""
	
    if not results:
        results = {}

    calcValue = calc_space.CalculateValue(node, column_name)
    key = node.Item().StringKey()

    if type == "datetime":
        datetimeValue = dt.datetime.fromtimestamp(calcValue)
        results[key][column_name] = datetimeValue.strftime("%Y-%m-%d %H:%M:%S")
    elif type == "objectname":
        results[key][column_name] = formatValues(calcValue.Name())
    else:
        results[key][column_name] = formatValues(calcValue)

    return results


def formatValues(d):
    """ Format the value of the column.	"""

    if type(d) == FloatType:
        return '%0.2f' % (d)

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
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, None, 0, 1,
     'Trades Filter to be written to the recon file.', None, 1],
    [outputDirectoryKey, 'Output Directory', outputSelection,
     None, outputSelection, 1, 1,
     'Directory where the file will be created.', None, 1],
    [outputFileKey, 'Output File', 'string', None, None,
     1, 1, 'Name of the output file.',  None, 1]
]


def GetOutputResults(tradeFilter):
    """ Get the results for the trade filter .	"""
	
    context = acm.GetDefaultContext()
    sheet_type = 'FTradeSheet'

    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    tf = tradeFilter[0]

    if tf:
        topNode = calcSpace.InsertItem(tf)
        calcSpace.Refresh()

        filtiter = calcSpace.RowTreeIterator().FirstChild()
        childiter = filtiter.FirstChild()

        currencies = []
        ccy = acm.FCurrency['ZAR']
        currencies.append(ccy)

        vector = acm.FArray()
        for currency in currencies:
            create_named_param(vector, currency)

        cash_per_currency = acm.Sheet.Column().ConfigurationFromVector(vector)

        results = {}
        while childiter:
            key = childiter.Tree().Item().StringKey()
            key = key.replace("ZAR/", "")

            results[key] = {}

            results = getColumn(key, childiter.Tree(), calcSpace, 'Portfolio Profit Loss Price End Date', results )
            results = getColumn(key, childiter.Tree(), calcSpace, 'Portfolio Profit Loss Position End', results )
            results = getColumn(key, childiter.Tree(), calcSpace, 'Portfolio Fees', results )

            cpc_vector = calcSpace.CreateCalculation(childiter.Tree(), 'Portfolio Cash Vector', cash_per_currency).Value()   

            cpc_vector = cpc_vector.Number() 

            results[key]['Cash Per Currency - ZAR'] = formatValues(cpc_vector)
            results = getColumn(key, childiter.Tree(), calcSpace, 'Total Val End', results)
            results = getColumn(key, childiter.Tree(), calcSpace, 'Portfolio Cash End', results)
            results = getColumn(key, childiter.Tree(), calcSpace, 'O/S_Cash', results )
            results = getColumn(key, childiter.Tree(), calcSpace, 'ISIN', results )
            results = getColumn(key, childiter.Tree(), calcSpace, 'InsValEnd', results )
            results = getColumn(key, childiter.Tree(), calcSpace, 'Trade Portfolio', results, "objectname")
            results = getColumn(key, childiter.Tree(), calcSpace, 'Trade Counterparty', results, "objectname")

            childiter = childiter.NextSibling()

        return results


def WriteToFile(filepath, results):
    """  Write the results into the output file.	"""
	
    csvFile = open(filepath, 'w')

    columns = ['si_JSE_settled trades',
               'Isin',
               'Used Price End',
               'PLPosEnd',
               'ZAR Cash',
               'Fees',
               'Total Val End',
               'Cash End',
               'O/S_Cash',
               'TradePortfolio',
               'Counterparty',
               'InsValEnd']

    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerow(columns)

    for result in results.keys():

        row = [results[result][headers[col]]
               for col in columns if headers.has_key(col) and
               results[result].has_key(headers[col]) ]
        writer.writerow([result]+row)

    csvFile.close()


def ael_main(parameters):
    """Entry point for task execution."""
	
    try:

        tradeFilter = parameters[tradeFilterKey]
        if not tradeFilter:
            _raiseError('Please supply value for mandatory parameter Trade Filter.')
            return

        outputDirectory = parameters[outputDirectoryKey]
        outputFile = parameters[outputFileKey][0]

        fileDirectory = outputDirectory.SelectedDirectory().Text()
        filepath = _getFilepath(fileDirectory, outputFile)
        output = GetOutputResults(tradeFilter)
        WriteToFile(filepath, output)
        print('Wrote secondary output to:::' + filepath)

    except Exception, ex:
        print('Error while creating trade recon report', str(ex))