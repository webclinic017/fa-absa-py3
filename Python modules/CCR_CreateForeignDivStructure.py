"""-----------------------------------------------------------------------
MODULE
    CCR_CreateForeignDivStructure

DESCRIPTION
    Procedure to create foreign dividend structure

    Date                : 2015-03-20
    Purpose             : Creates Dual Lised Dividend Context, foreign dividend streams, stock mappings and foreign dividend estimates.
    Department and Desk : Market Risk
    Developer           : Ryan Warne

HISTORY

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm, ael
import traceback
import collections
import csv
import FBDPGui
from  FBDPCurrentContext import Logme, CreateLog, Summary
import FBDPCommon
import time
import ArenaFunctionBridge
from at_time import *
import datetime
import ast

global FOREIGNDIVIDENDINS
FOREIGNDIVIDENDINS = {}

TODAY = acm.Time().DateToday()

_Dividend = collections.namedtuple('_Dividend',
    ['exDate', 'recDate', 'payDate', 'amount', 'curr', 'type'])

CONFIG = {}

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

# Get values from FParameter by name"""
def get_parameter_dict(name):
    
    values = {}
    p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', name)
    try:
        template = p.Value()
    except AttributeError, e:
        logger.ELOG( "Error getting parameters ( %s ): %s", name, str( e ) )
    for k in template.Keys():
        k = str(k)
        value = str( template.At(k) )
        value = None if value == "" else value
        values[ str(k) ] = value
    return values

# Error Message Construct
def error_message_construct(ex):

    errorSeverity = "ERROR"

    if ('Duplicate' in ex.args[0]) or 'Invalid field value' in ex.args[0]:
        errorSeverity = "WARN"

    template = "An exception of type {0} occured. Message:{1!r}"
    message = template.format(type(ex).__name__, ex.args[0])
    
    return message, errorSeverity

# Dividend Growth Function
def grow_divs(strm, gfac, endYear, testmode = True):

    growth = (1+(gfac/100.0))
    
    valid_estimates = [i for i in strm.Dividends() if i.Description() != 'Special']
    sort = sorted(valid_estimates, key = lambda div : div.RecordDay())

    for div in sort[-strm.DividendsPerYear():]:
        
        last_day = ael_date(div.RecordDay())
        amount = div.Amount()

        while last_day <= ael_date(endYear):
        
            last_day = last_day.add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')
        
            new = acm.FDividendEstimate()
            new.RecordDay = last_day
            new.DividendStream = strm
            new.ExDivDay = ael_date(new.RecordDay()).add_banking_day(ael.Instrument['ZAR'], -4)
            new.PayDay = ael_date(new.RecordDay()).add_banking_day(ael.Instrument['ZAR'], 1)
            new.Amount = amount * growth
            new.Currency = div.Currency()
            new.TaxFactor = 1
            new.Description = 'Simulated'
            log_div(new, testmode)
        
# Create dividend stream
def create_foreign_div_streams(testmode):

    Logme()("Creating Foreign Dividend Streams...")
    Logme()("="*100)
    
    for stock in FOREIGNDIVIDENDINS.keys():
        newStream = acm.FDividendStream()
        newStream.Instrument = acm.FInstrument[stock]
        newStream.DividendsPerYear = 2
        newStream.AdjustmentFactor = 1
        newStream.Name = (FOREIGNDIVIDENDINS[stock])[1]
        
        if not testmode:
        
            try:
                newStream.Commit()
                Summary().ok(acm.FDividendStream(), Summary().CREATE, None, 1)
                
            except Exception as ex:
            
                message, errorSeverity = error_message_construct(ex)
                print "Stream " + (FOREIGNDIVIDENDINS[stock])[1] +":" + message
                
                if errorSeverity == "WARN":
                    Summary().ignore(acm.FDividendStream(), Summary().CREATE, "Duplicate dividend stream found", (FOREIGNDIVIDENDINS[stock])[1])
                else:
                    Summary().fail(acm.FDividendStream(), Summary().CREATE, "Failed to create dividend stream for %s" %stock, "")
                
        else:
            Summary().ok(acm.FDividendStream(), Summary().CREATE, None, 1)
                
# Create Context Links
def create_new_context_and_links(contextName, testmode):
        
    # Create New Context
    Logme()("Creating Dual Listed Dividend Context...")
    Logme()("="*100)
    
    newContext = acm.FContext()
    newContext.Name = contextName

    if not testmode:
    
        try:
            newContext.Commit()
            Summary().ok(acm.FContext(), Summary().CREATE, None, 1)
            
        except Exception as ex:
        
            message, errorSeverity = error_message_construct(ex)
            print "Context " +contextName+ ":"+ message
        
            if errorSeverity == "WARN":
                Summary().ignore(acm.FContext(), Summary().CREATE, "Duplicate context found", contextName)
            else:
                Summary().fail(acm.FContext(), Summary().CREATE, "Failed to create new context: %s" %contextName, "")
        
    else: 
        Summary().ok(acm.FContext(), Summary().CREATE, None, 1)

    #Create Context Links    
    for stock in FOREIGNDIVIDENDINS.keys():
    
        Logme()("Creating %s Context Link..." %((FOREIGNDIVIDENDINS[stock])[1]))
        Logme()("="*100)
        contextLink = acm.FContextLink()
        contextLink.Context = newContext
        contextLink.MappingType = "Instrument"
        contextLink.Instrument = acm.FInstrument[stock]
        contextLink.Name = (FOREIGNDIVIDENDINS[stock])[1]
        contextLink.Type = "Dividend Stream"
    
        if not testmode:
        
            try:
                contextLink.Commit()
                Summary().ok(acm.FContextLink(), Summary().CREATE, None, 1)
                
            except Exception as ex:
            
                message, errorSeverity = error_message_construct(ex)
                print "Context Link " +(FOREIGNDIVIDENDINS[stock])[1]+ ":"+ message
            
                if errorSeverity == "WARN":
                    Summary().ignore(acm.FContextLink(), Summary().CREATE, "Duplicate context link found", stock)
                else:
                    Summary().fail(acm.FContextLink(), Summary().CREATE, "Failed to create context link for %s" %stock, "")
                
        else:
            Summary().ok(acm.FContextLink(), Summary().CREATE, None, 1)

# Deletes dividend estimates
def delete_est(stream, testmode):

    acm.BeginTransaction()
    
    Logme()("")
    Logme()("Deleting %s estimate(s) in stream" % len(stream.Dividends()), 'INFO')
    
    for e in stream.Dividends():
    
        if not testmode:
    
            try: 
                e.Delete()
                Summary().ok(acm.FDividendEstimate(), Summary().DELETE, None, 1)
                
            except:
                print "ERROR: Dividend estimate deletion failed!"
                Summary().fail(acm.FDividendEstimate(), Summary().DELETE, "Div. estimate deletion failed for stream %s" %stream.Name(), e.Oid())
                
        else:
           Summary().ok(acm.FDividendEstimate(), Summary().DELETE, None, 1)
    
    acm.CommitTransaction()
 
# Logged creation of dividend estimates 
def log_div(div, testmode):

    Logme()("")
    Logme()("Creating Dividend Estimate:", 'INFO')
    Logme()("Ex Div Day: %s" % div.ExDivDay(), 'INFO')
    Logme()("Record Day: %s" %div.RecordDay(), 'INFO')
    Logme()("Pay Day: %s" % div.PayDay(), 'INFO')
    Logme()("Amount: %s" % div.Amount(), 'INFO')
    Logme()("Currency: %s" % div.Currency().Name(), 'INFO')
    Logme()("Tax factor: %s" % div.TaxFactor(), 'INFO')
    Logme()("Description: %s" % div.Description(), 'INFO')
    
    if not testmode:
        
        try:
            div.Commit()
            Summary().ok(acm.FDividendEstimate(), Summary().CREATE, None, 1)

        except:
            print "ERROR: Dividend estimate creation failed!"
            Summary().fail(acm.FDividendEstimate(), Summary().CREATE, "Div. estimate creation failed for Ex. Div. Day:%s" %div.ExDivDay(), div.Instrument().Name())
    
    else:
        Summary().ok(acm.FDividendEstimate(), Summary().CREATE, None, 1)

# Dividend estimate creation method       
def add_dividend_est(stream, data_list, testmode):

    acm.BeginTransaction()

    for data in data_list:
        newe = acm.FDividendEstimate()
        newe.DividendStream = stream
        newe.ExDivDay = data.exDate
        newe.RecordDay = data.recDate
        newe.PayDay = data.payDate
        newe.Amount = data.amount
        newe.Currency = acm.FCurrency[data.curr]
        newe.TaxFactor = 1
        newe.Description = data.type
        log_div(newe, testmode)
        
    acm.CommitTransaction()

# Creates foreign dividend estimates       
def create_foreign_div_stream_estimates(dividendDict, config):

    # Create Foreign Dividend Stream
    for stock in FOREIGNDIVIDENDINS.keys():
    
        domesticDivStreamName = (FOREIGNDIVIDENDINS[stock])[0]
        foreignDivStreamName = (FOREIGNDIVIDENDINS[stock])[1]

        Logme()("")
        Logme()("Processing foreign dividend stream %s" % foreignDivStreamName)
        Logme()("="*100)
       
        foreignDivStream = acm.FDividendStream[foreignDivStreamName]
        domesticDivStream = acm.FDividendStream[domesticDivStreamName]
        
        #Delete all domestic dividend estimates
        delete_est(domesticDivStream, config['Testmode'])
        
        if foreignDivStream == None:
            print "ERROR: Stock, %s, has no dividend stream setup" %stock
            Summary().fail(acm.FDividendStream(), Summary().PROCESS, "Stock, %s, has no dividend stream setup" %stock, foreignDivStreamName)
        
        else:
        
            #Delete existing estimates (transaction needed here to ensure proper delete)
            delete_est(foreignDivStream, config['Testmode'])
       
            #Add new dividend estimates
            add_dividend_est(foreignDivStream, dividendDict[domesticDivStreamName], config['Testmode'])
        
            #Additional Dividends using growth function
            if config['DivGrowth']:
                acm.BeginTransaction()
                grow_divs(foreignDivStream, float(config['Growth'])*100.0, config['GrowUntil'], testmode = config['Testmode'])
                acm.CommitTransaction()
        

# Creates dictionary containing information for dual listed stocks
def create_foreign_stock_dictionary(foreignStockList, dividendDict, foreignDividendInsParam):
    
    for stock in foreignStockList:
        strippedStockName = stock.Name().replace("ZAR/", '')
    
        if not stock.Name() in foreignDividendInsParam.keys():
            Summary().warning(acm.FStock(), Summary().PROCESS, "Stock is not in the 'foreignDividendIns' FParameter list and wont be subscribed to.", stock.Name())
    
        try:
            divCurr = dividendDict[strippedStockName][0].curr
            FOREIGNDIVIDENDINS[stock.Name()] = [strippedStockName, strippedStockName+'_'+divCurr, divCurr]
        
        except:
            Logme()('Stock, ' + stock.Name() + ', does not exist in upload file.', 'ERROR')
            Summary().fail(acm.FStock(), Summary().PROCESS, "Stock has no dividend stream setup", stock.Name())
    
def convert_date(inputDate):

    return datetime.datetime.strptime(inputDate, '%d/%m/%Y').strftime('%Y-%m-%d')
    
#Obtain dividend dictionary from file    
def get_dividends_dictionary(filename):

    dictionary = {}
    Logme()("Reading file %s " % filename, 'INFO')
    Logme()("="*100)
    for row in csv.DictReader(open(filename), delimiter = ','):
        stock = stock = (row['Stock'].replace('J.J', '')).replace('Jn.J', '')
        stock1 = stock+'1'

        if  not (row['Source'] == "Markit" and row['Amount'] == ""):
            amount = float(row['Amount'] if row['Amount'] else 0)
            
            div = _Dividend(
                exDate = convert_date(row['Ex-Date']),
                amount = amount,
                recDate = convert_date(row['Rec-Date']),
                payDate = convert_date(row['Pay-Date']),
                curr = row['Curr'],
                type = row['Type']
            )
            
            if ael_date(convert_date(row['Ex-Date'])) > ael.date_today():
            
                dictionary.setdefault(stock, []).append(div)
                
                if div.type != 'Special':
                   dictionary.setdefault(stock1, []).append(div)
                
        else:
            Logme()("%s is empty" % row, 'WARNING')
            
    return dictionary

#Stock list supplier for RunScript GUI
def insert_stocks():

    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    
    return q

#Hook for context name field
def context_name_hook(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] != '0')
    return fieldValues
    
#Hook for dividend growth fields
def dividend_growth_hook(index, fieldValues):
    ael_variables[6][9] = (fieldValues[5] != '0')
    ael_variables[7][9] = (fieldValues[5] != '0')
    ael_variables[6][3] = 0.0
    return fieldValues

tt_createStructure = "If selected will create context, context links and foreign dividend streams."
tt_contextName = "Name of context for dual listed dividends."
tt_foreignStockList = "List of stocks with foreign dividends."
tt_sourceFile = "Path and filename containing dividends."
tt_dividendGrowth = 'If selected will allow user to select dividend growth parameters'
tt_growth = "Growth factor (numeric number) for dividends."
tt_growthUntil = "Date up until which to grow dividends (yyyy-mm-dd)."

ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #   DisplayName,
    #   Type, CandidateValues, Default,
    #   Mandatory, Multiple, Description, InputHook, Enables]
    ['createStructure', 'Create Stream Structure', 'int', [0, 1], None, 0, 0, tt_createStructure, context_name_hook, 1],
    ['contextName', 'Context Name', 'string', None, None, 0, 0, tt_contextName, None, 0],
    ['foreignStockList', 'Foreign Stocks', 'FInstrument', insert_stocks(), None, 0, 1, tt_foreignStockList, None, 1],
    ['sourceFile', 'Source File', 'string', None, None, 1, 0, tt_sourceFile, None, 1],
    ['DivGrowth', 'DivGrowth', 'int', [0, 1], None, 0, 0, tt_dividendGrowth, dividend_growth_hook, 1],
    ['Growth', 'Growth', 'double', 0.0, None, 0, 0, tt_growth, None, 0],
    ['GrowUntil', 'GrowUntil', 'string', None, None, 0, 0, tt_growthUntil, None, 0]
)

def ael_main(config):
    
    CreateLog('ForeignDividendSetupTast', config['Logmode'], 
            config['LogToConsole'], config['LogToFile'], config['Logfile'],
            config['SendReportByMail'], config['MailList'], config['ReportMessageType'])
    Logme()(None, 'START')      
    Summary().setStartTime(time.time())
    
    global CONFIG
    CONFIG = config
    
    #Monitored Foreign Listed Stocks from FParameter
    foreignDividendInsParam = ast.literal_eval((get_parameter_dict("foreignDividendIns"))['stockDictionary'])
    
    #Create dictionary of dividends
    div_dictionary =  get_dividends_dictionary(config['sourceFile'])

    #Create foreign stock stream dictionary
    create_foreign_stock_dictionary(config['foreignStockList'], div_dictionary, foreignDividendInsParam)

    #Create dividend stream structure
    if config['createStructure'] and config['contextName']:
        
        #Create Foreign Dividend Stream
        create_foreign_div_streams(config['Testmode'])

        #Create Context
        create_new_context_and_links(config['contextName'], config['Testmode'])
        
    #Create Foreign Dividend Estimates
    create_foreign_div_stream_estimates(div_dictionary, config)
        
    Summary().commitEntries()
    Summary().log(config)
    







    

