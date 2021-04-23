'''
#Purpose:       Part of the dividend upload process for FA. 
                The EXCEL Tool FrontDividendDataRetriever is responsible of 
                getting dividends from Markit, Peregrine and other Dividends 
                and joins them to one CSV file. This CSV file will be used as 
                an input. Furthermore one can select dividend streams which 
                will then be deleted and rewritten. 
        
#Department:    MO, PCG, PCG, PCG, MO
#Requester:     Irfaan Karim
#Developer:     Marc-Stephan Maenner (marc-stephan.maenner@d-fine.de)
'''



import collections
import csv
import acm
import ael
import time
import ArenaFunctionBridge
import FBDPGui
from  FBDPCurrentContext import Logme, CreateLog
import FBDPCommon

_Dividend = collections.namedtuple('_Dividend',
    ['exDate', 'recDate', 'payDate', 'amount', 'curr', 'type'])
    
space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

CONFIG = {}

def grow_divs(strm, gfac, endYear,el, testmode = True):
    growth = (1+(gfac/100.0))
    
    valid_estimates = [i for i in strm.estimates() if i.description != 'Special']
    sort = sorted(valid_estimates, key = lambda div : div.day)

  
    for div in sort[-strm.div_per_year:]:
        
        last_day = div.day
        amount = div.dividend

        
        while last_day <= endYear:
            last_day = last_day.add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')
        
            new = ael.DividendEstimate.new(strm)
            new.day = last_day
            new.ex_div_day = new.day.add_banking_day(ael.Instrument['ZAR'], -4)
            new.pay_day = new.day.add_banking_day(ael.Instrument['ZAR'], 1)
            new.dividend = amount * growth
            new.curr =div.curr
            new.tax_factor = 1
            new.description = 'Simulated'
            log_div(new, testmode)


def _fx_rate(from_currency, to_currency, date):
   
    calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    from_curr = acm.FCurrency[from_currency]
    to_curr = acm.FCurrency[to_currency]
    return from_curr.Calculation().FXRate(space, to_curr, date).Number()
     
def _hook_called_before_dividend_is_added_to_stream(div):
    from_curr = div.curr.insid
    to_curr = div.stream_seqnbr.insaddr.curr.insid
        
    if not CONFIG['FxConversion'] == 'No FX conversion' and from_curr <> to_curr:
        from_curr = div.curr.insid
        to_curr = div.stream_seqnbr.insaddr.curr.insid
        if CONFIG['FxConversion'] == 'Use Spot FX rate (deprecated)':
            day = acm.FCurrency[to_curr].Calendar().AdjustBankingDays(acm.Time().DateNow(), 2)
        else:
            day = acm.Time().AsDate(str(div.pay_day)) 
        forward = _fx_rate(from_curr, to_curr, day)
        
        Logme()("")
        Logme()("Calculating Fx Rate %s-%s-%s:%s" %(from_curr, to_curr, day, forward), 'INFO')
    
    
        div.curr = to_curr
        div.dividend = div.dividend * forward
            
def add_dividend_est(stream, data_list, testmode):
    for data in data_list:
        newe = ael.DividendEstimate.new(stream)
        newe.ex_div_day = data.exDate
        newe.day = data.recDate
        newe.pay_day = data.payDate
        newe.dividend = data.amount
        newe.curr = data.curr
        newe.tax_factor = 1
        newe.description = data.type
        _hook_called_before_dividend_is_added_to_stream(newe)
        log_div(newe, testmode)

def log_div(div, testmode):
    Logme()("")
    Logme()("Creating Dividend Estimate", 'INFO')
    Logme()("Ex Div Day: %s" % div.ex_div_day, 'INFO')
    Logme()("Record Day: %s" %div.day, 'INFO')
    Logme()("Pay Day: %s" % div.pay_day, 'INFO')
    Logme()("Amount: %s" % div.dividend, 'INFO')
    Logme()("Currency: %s" % div.curr.insid, 'INFO')
    Logme()("Tax factor: %s" % div.tax_factor, 'INFO')
    Logme()("Description: %s" % div.description, 'INFO')
    if not testmode:
        div.commit()    
            
def delete_est(stream, testmode):
    Logme()("")
    Logme()("Delete %s estimates in stream" % len(stream.estimates()), 'INFO')
    for e in stream.estimates():
        e.delete()

def get_dividends_dictionary(filename, today = ael.date_today()):
    dictionary = {}
    Logme()("Reading file %s " % filename, 'INFO')
    for row in csv.DictReader(open(filename), delimiter = ','):
        stock = stock = (row['Stock'].replace('J.J', '')).replace('Jn.J', '')
        stock1 = stock+'1'
        if not stock in dictionary:
            dictionary[stock] = []
            dictionary[stock1] = []

        if  not (row['Source'] == "Markit" and row['Amount'] == ""):
            amount = float(row['Amount'] if row['Amount'] else 0)
            div = _Dividend(
                exDate = ael.date(row['Ex-Date']),
                amount = amount,
                recDate = ael.date(row['Rec-Date']),
                payDate = ael.date(row['Pay-Date']),
                curr = row['Curr'],
                type = row['Type']
            )
            if ael.date(row['Ex-Date']) > today:
                dictionary[stock] += [div]
                if div.type != 'Special':
                    dictionary[stock1] += [div]
        else:
            Logme()("%s is empty" % row, 'WARNING')
    return dictionary
    
def insertDividendStreams():
    q = acm.CreateFASQLQuery(acm.FDividendStream, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    #op = q.AddOpNode('AND')
    return q
    
ael_variables = FBDPGui.TestVariables(
    # [VariableName,
    #   DisplayName,
    #   Type, CandidateValues, Default,
    #   Mandatory, Multiple, Description, InputHook, Enables]
    ['sourceFile', 'Source File', 'string'],
    ['divStreams', 'Dividend Streams', 'FDividendStream', insertDividendStreams(), None, 1, 1],
    ['FxConversion', 'Fx Conversion', 'string', 
        ['No FX conversion', 'Use Spot FX rate (deprecated)', 'Use Forward FX rate at pay day'],
    'No FX conversion'],
    ['DivGrowth', 'DivGrowth', 'int', [0, 1]],
    ['Growth', 'Growth', 'double', 0, 0],
    ['GrowUntil', 'GrowUntil', 'string', '']
)
    
def ael_main(config):
    
    CreateLog('DividendUploaderTask', config['Logmode'], 
            config['LogToConsole'], config['LogToFile'], config['Logfile'],
            config['SendReportByMail'], config['MailList'], config['ReportMessageType'])
    Logme()(None, 'START')      
    
    try:
        global CONFIG
        CONFIG = config
        div_dictionary =  get_dividends_dictionary(config['sourceFile'])

        for stream in config['divStreams']:
            
            name = stream.Name()
            Logme()("Processing dividend stream %s" % name)
            Logme()("="*100)
            ael.begin_transaction()
            stream = ael.DividendStream[name].clone()
            if name in div_dictionary:
                delete_est(stream, config['Testmode'])
                add_dividend_est(stream, div_dictionary[name], config['Testmode'])
                
                if config['DivGrowth']:
                    grow_divs(stream, float(config['Growth'])*100.0, ael.date(config['GrowUntil']), stream, testmode = config['Testmode'])
            else:
                Logme()("This dividend stream is not set-up in the output file")
            ael.commit_transaction()
    except:
        Logme()(FBDPCommon.get_exception(), 'ERROR')
        import traceback, sys
        traceback.print_exc(file=sys.stdout)
       
