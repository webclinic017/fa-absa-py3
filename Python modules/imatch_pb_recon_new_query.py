"""

This script is used to produce the iMatch  extract for new trades for Commodities Trading.

Date: 2014-10-16
Requester: Thulsie Gasant
Developer: Manan Ghosh

History
=======

Date            CR                          Developer               Description
====            ======                      ================        =============
2015-07-30      CHNG0003003874              Lawrence Mucheka        Fix the ZAR Cash column
'''

"""
import acm
import time
import FRunScriptGUI
import os
import csv
from types import *
import datetime as dt
import at_time


tradeFilterKey = 'TRADE_FILTER'


outputDirectoryKey = 'OUTPUT_DIRECTORY'
outputSelection = FRunScriptGUI.DirectorySelection()

outputFileKey = 'OUTPUT_FILE'

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

ael_gui_parameters = {
    'windowCaption' : 'iMatch PB Recon File'
}

            
headers = {'Instrument': 'Trade Instrument',
           'Value Day': 'Trade Value Day',
           'Price': 'Trade Price',
           'Quantity': 'Trade Quantity',
           'ZAR Cash': 'Cash Per Currency - ZAR',
           'Fees': 'Portfolio Fees',
           'Execution Time': 'Trade Execution Time',
           'Portfolio': 'Trade Portfolio',
           'B/S': 'Bought or Sold'}


def _raiseError(message):
    """ Function to raise and error. """
	
    func = acm.GetFunction('msgBox', 3)
    func('Error', message, 0)


def getColumn(node, calc_space , column_name, results, ttype=None):
    """ 
	Get the value of the column from 
    calculation space.
	"""
	
    if not results:
        results = {}

    calcValue = calc_space.CalculateValue(node, column_name)
    
    if ttype == "datetime":
        datetimeValue = at_time.datetime_from_string(calcValue)
        results[node.Item().StringKey()][column_name] = datetimeValue.strftime("%Y-%m-%d %H:%M:%S")
    elif ttype == "objectname":
        results[node.Item().StringKey()][column_name] = formatValues(calcValue.Name())
    else:
        results[node.Item().StringKey()][column_name] = formatValues(calcValue)

    return results

    
def formatValues(d):
    """ Format the value of the column.	"""

    if type(d) == FloatType or type(d) == IntType:
        return '%0.2f' % (d)
 
    if type(d) == StringType :
        d = d.replace("'", "")
        d = d.replace("ZAR/", "")
        return d
   

    if d.IsKindOf(acm.FDenominatedValue):
        d = d.Number()    
        return '%0.2f' % (d)

    d = str(d)        
    d = d.replace("'", "")
    d = d.replace("ZAR/", "")

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
    """ Get the results for the trade filter .	"""
	
    context = acm.GetDefaultContext()
    sheet_type = 'FTradeSheet'


    calcSpace = acm.Calculations().CreateCalculationSpace(context, sheet_type)    

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

        while childiter :
            tradeNo = childiter.Tree().Item().StringKey()
            trade = acm.FTrade[tradeNo]

            results[tradeNo] = {}

            results = getColumn(childiter.Tree(), calcSpace, 'Trade Instrument', results )
            results = getColumn(childiter.Tree(), calcSpace, 'Trade Value Day', results )

            results = getColumn(childiter.Tree(), calcSpace, 'Trade Price', results )
            results = getColumn(childiter.Tree(), calcSpace, 'Trade Quantity', results )
          
            results[tradeNo]['Cash Per Currency - ZAR'] = formatValues(-trade.Premium())
            results = getColumn(childiter.Tree(), calcSpace, 'Portfolio Fees', results )
            results = getColumn(childiter.Tree(), calcSpace, 'Trade Execution Time', results, "datetime" )
            results = getColumn(childiter.Tree(), calcSpace, 'Trade Portfolio', results, "objectname" )
            results = getColumn(childiter.Tree(), calcSpace, 'Bought or Sold', results )
            
            childiter = childiter.NextSibling()

                        
        return results
        
def WriteToFile(filepath, results):
    """  Write the results into the output file.	"""
	
    csvFile = open(filepath, 'w')

    columns = ['si_JSE new trades',
	           'Instrument',
			   'Value Day',
			   'Price',
			   'Quantity',
			   'ZAR Cash',
			   'Fees',
			   'Execution Time',
			   'Portfolio',
			   'B/S']

    writer = csv.writer(csvFile, lineterminator = '\n')
    writer.writerow(columns)

    for result in results.keys():
        row = [results[result][headers[col]] for col in columns if headers.has_key(col) and results[result].has_key(headers[col]) ]
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
