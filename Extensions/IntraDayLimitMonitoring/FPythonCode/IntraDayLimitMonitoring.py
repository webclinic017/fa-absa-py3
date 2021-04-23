from time import time
from datetime import datetime, timedelta
import acm
import ael
import string
import smtplib
import StringIO
import json
import operator

debug = True
date_format = '%Y-%m-%d %H:%M:%S'
timeSeriesSpecName = 'LimitMonitoring'
timeSeriesSpecDescription = 'IntraDayLimitMonitoring'
choiceListName = 'IntraDayLimitMonitoringColumns' 
textObjectName = 'IntraDayLimitMonitoring'

def log(message):
    if debug:
        date_string = datetime.strftime(datetime.now(), date_format)
        message = "%s %s" % (date_string, message)  
        print message

def error(message):
    date_string = datetime.strftime(datetime.now(), date_format)
    message = "ERROR: %s %s" % (date_string, message)  
    print message
    ael.log(message)
    raise Exception(message)

def send_mail(TO, SUBJECT, MSG):
    log("Sending email")
    HOST = 'SMTPRELAY.barcapint.com'
    FROM = "IntraDayTriggerMonitoring"
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", MSG), "\r\n")
    try:
        server = smtplib.SMTP(HOST)
        server.set_debuglevel(1)
        server.sendmail(FROM, TO.split(','), BODY)
        server.quit()
    except Exception, e:
        print e  
    

class PersistentData(object): 
     
    def __init__(self, columns, desks):
        self.columns = convert(columns)
        self.desks = convert(desks)

class Desk(object):          
    def __init__(self, desk_name, portfolio_names, limits={}):
        self.desk_name = str(desk_name)
        self.portfolio_names = convert(portfolio_names)
        self.limits = convert(limits)        
        
class Limit(object):          
    def __init__(self, column_name, limit_value):
        self.column_name = str(column_name)
        self.limit_value = float(limit_value)

class CalculationResult(object): 
     
    def __init__(self, column_name, denominated_value, date_time):
        self.column_name = column_name
        self.denominated_value = denominated_value
        self.date_time = date_time

class Column(object): 
     
    def __init__(self, column_name, column_id, column_label, report_order, active):
        self.column_name = str(column_name)
        self.column_id = str(column_id)
        self.column_label = str(column_label)
        self.report_order = int(report_order)
        self.active = str(active)

class StandardColumn(Column): 
     
    def __init__(self, column_name, column_id, column_label, report_order, active):
        Column.__init__(self, column_name, column_id, column_label, report_order, active)

    def __repr__(self):
        return '%s' % (self.column_name)

class TimeBucketColumn(Column): 
     
    def __init__(self, column_name, column_id, column_label, report_order, active, bucket):
        Column.__init__(self, column_name, column_id, column_label, report_order, active)
        self.bucket = str(bucket)
        
    def __repr__(self):
        return '%s %s' % (self.column_name, self.bucket)

class VectorColumn(Column): 
     
    def __init__(self, column_name, column_id, column_label, report_order, active, vector_type, vector_value):
        Column.__init__(self, column_name, column_id, column_label, report_order, active)
        self.vector_type = str(vector_type)
        self.vector_value = str(vector_value)
        
    def __repr__(self):
        return '%s %s %s' % (self.column_name, self.vector_type, self.vector_value)


class JsonEncoder(json.JSONEncoder):    
    def default(self, obj):
        d = { '__class__': obj.__class__.__name__,
              '__module__': obj.__module__,
              }
        d.update(obj.__dict__)
        return d
   
def convert(input):
    if isinstance(input, dict):
        return dict([(convert(key), convert(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
   
class JsonDecoder(json.JSONDecoder):    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items())
            inst = class_(**args)
        else:
            inst = d
        return inst


def getTextObject():
    to = ael.TextObject.read("type = 'Customizable' and name = '%s'" % textObjectName)
    return to

def persistData(data):
    to = getTextObject()
    if to:
        json = JsonEncoder().encode(data)
        to_clone = to.clone()        
        to_clone.set_text(json)
        to_clone.commit()

def getData():
    to = getTextObject()
    if to:
        txt = to.get_text()
        if txt:
            data = JsonDecoder().decode(txt)
            return data


def getColumnList():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FColumnDefinition', 'FPortfolioSheet', True, True, 'sheet columns', 'portfoliosheet').Sort() 
    return extensions

def create_timebuckets(bucket_labels, add_rest_bucket):
    today = acm.Time().DateToday()
    buckets_definition = []
    for label in bucket_labels:
        bucket_definition = acm.FDatePeriodTimeBucketDefinition()
        bucket_definition.DatePeriod(label)
        buckets_definition.append(bucket_definition)
        if add_rest_bucket:
            buckets_definition.append(acm.FRestTimeBucketDefinition())
        definition = acm.TimeBuckets().CreateTimeBucketsDefinition(today,
        buckets_definition, False, False, False, False, False)
        def_and_conf = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
    return acm.TimeBuckets().CreateTimeBuckets(def_and_conf)

def create_named_param(vector, name, obj):
    param = acm.FNamedParameters();
    param.AddParameter(name, obj)
    vector.Add(param)

def create_currency_vector(items):
    vector = acm.FArray()
    for i in items:
        create_named_param(vector, 'currency', acm.FCurrency[ i.strip() ])        
    return vector
    
def getTimeSeriesSpec():
    spec = acm.FTimeSeriesDvSpec[timeSeriesSpecName]
    return spec 
    
def runCalc(context, sheet_type, global_values, portfolio):
    results = []                
    log("Setting up calculation space")
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
            
    try:
        for key in global_values:
            calc_space.SimulateGlobalValue(key, global_values[key])
            
        log("Inserting portfolio in calculation space")
        top_node = calc_space.InsertItem(portfolio)
        
        log("Refreshing calculation space")         
        calc_space.Refresh()        
 
        log("Starting calculation") 
        columns = getData().columns
        for c in columns:
            column = columns[c]
            #log("Calculating '%s'" % (column.column_name))         
            calculation = None
             
            if isinstance(column, StandardColumn):
                calculation = calc_space.CreateCalculation(top_node, column.column_id)            
                results.append(CalculationResult(column.column_name, calculation.ValueOrException(), datetime.now()))

            if isinstance(column, TimeBucketColumn):
                time_buckets = None
                if '-' in column.bucket:
                    split = column.bucket.split('-')
                    time_buckets = create_timebuckets(split, False)
                else:
                    time_buckets = create_timebuckets([column.bucket], False)
                column_config = acm.Sheet.Column().ConfigurationFromTimeBuckets(time_buckets)
                calculation = calc_space.CreateCalculation(top_node, column.column_id, column_config)
                if '-' in column.bucket:
                    results.append(CalculationResult(column.column_name, calculation.ValueOrException()[1], datetime.now()))
                else:
                    results.append(CalculationResult(column.column_name, calculation.ValueOrException(), datetime.now()))
                 
            if isinstance(column, VectorColumn):
                if column.vector_type == 'Currency':
                    vector = create_currency_vector([column.vector_value])
                    column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
                    calculation = calc_space.CreateCalculation(top_node, column.column_id, column_config)                    
                    results.append(CalculationResult(column.column_name, calculation.ValueOrException(), datetime.now()))
                elif column.vector_type == 'YieldCurve':
                    yc = acm.FYieldCurve[column.vector_value]
                    param = acm.FNamedParameters();
                    param.AddParameter('yieldCurve', yc)                                  
                    column_config = acm.Sheet.Column().ConfigurationFromVectorItem(param)
                    calculation = calc_space.CreateCalculation(top_node, column.column_id, column_config)
                    results.append(CalculationResult(column.column_name, calculation.ValueOrException(), datetime.now()))
                else:
                    error("Unsupported Vector Type %s" % column.vector_type)
    finally:        
        log("Removing global simulation")         
        for g in global_values:            
            calc_space.RemoveGlobalSimulation(g)    

    log("Calculation complete")         
    return results


def get_task(portfolio):
    intraday_tasks = acm.FAelTask.Select('')
    tasks=[]
    for task in intraday_tasks:     
        if task.ModuleName() =='IntraDayLimitMonitoringTask' and task.Name().find('IntraDayLimitMon') <>-1:
            txt = task.ParametersText()
            txt = txt.replace('portfolios=', '')
            txt = txt.replace(';', '')
            if portfolio in txt.split(','):
                tasks.append(task.Name())
    return tasks


def runReport(desk_names, outputfile_csv, email_address, date):
    log('Running Report')
    env = '%s %s' % (acm.FDhDatabase['ADM'].ADSNameAndPort().lower(), acm.ADSAddress())
    log('Environment: %s' %env)
    #date = acm.Time.DateNow()
    print desk_names
    breaches = {}
    missing = {}
    
    spec = acm.FTimeSeriesDvSpec['LimitMonitoring']
    output = StringIO.StringIO()
    summary = StringIO.StringIO()
    summary_file = StringIO.StringIO()
    portfolio_detail = StringIO.StringIO()
    
    output.write('Desk Detail\n')            
    portfolio_detail.write("\n\nPortfolio Detail\n")
    portfolio_detail.write("StorageDate,Portfolio,Column,Value,Currency,Date,UpdateTime,UpdateUser\n")
    data = getData()
    columns = None
    sorted_columns = None   
    tasks_with_missing_values=[]
    missing_entities = []
    if data:        
        for desk_name in desk_names:
            try:
                desk = data.desks[desk_name]
            except KeyError:
                log('Error: desk "%s" does not exist' % desk_name)
                missing_entities.append('desk %s' % desk_name)
                continue

            if not columns:
                columns = data.columns
                sorted_columns = (sorted(columns.values(), key=operator.attrgetter('report_order')))
                output.write('Desk,') 
                for idx, column in enumerate(sorted_columns):
                    output.write(column.column_label)  
                    output.write(',')
                    output.write('Limit,')  
                    output.write('Breached,')  
                output.write('\n')  
            aggregation = {}
            for c in columns:
                column = columns[c]
                aggregation[column.column_name] = 0.0
            for portfolio_name in desk.portfolio_names:
                #print portfolio_name
                portfolio = acm.FPhysicalPortfolio[portfolio_name]
                
                if portfolio is None:
                    log('Error: portfolio "%s" does not exist' % portfolio_name)
                    missing_entities.append('Portfolio %s:%s' % (desk_name, portfolio_name))
                    continue
                
                for idx, column in enumerate(sorted_columns):
                    choiceList = acm.FChoiceList.Select("name = '%s' and list = '%s'" % (column.column_name, choiceListName))[0]                
                    ts = getTimeSeries(spec, date, portfolio, choiceList)
                    if ts:            
                        currentValue = aggregation[column.column_name]
                        aggregation[column.column_name] = currentValue + ts.DvValue()
                        portfolio_detail.write(ts.StorageDate())
                        portfolio_detail.write(',')
                        portfolio_detail.write(portfolio.Name())
                        portfolio_detail.write(',')
                        portfolio_detail.write(column.column_name)
                        portfolio_detail.write(',')
                        portfolio_detail.write(ts.DvValue())
                        portfolio_detail.write(',')
                        curr_ = ts.DvCurrency().Name() if ts.DvCurrency() else ''
                        portfolio_detail.write(curr_)
                        portfolio_detail.write(',')
                        portfolio_detail.write(ts.DvDate())
                        portfolio_detail.write(',')
                        portfolio_detail.write(acm.Time.DateTimeFromTime(ts.UpdateTime()))
                        portfolio_detail.write(',')
                        portfolio_detail.write(ts.UpdateUser().Name())
                        portfolio_detail.write('\n')
                    else:
                        missing_list = None
                        if desk_name in missing:
                            missing_list = missing[desk_name]
                        else:
                            missing_list = []
                            missing[desk_name] = missing_list
                        missing_list.append([portfolio.Name(), column.column_name]) 

                        tasks = get_task(portfolio.Name())
                        for task in tasks:
                            tasks_with_missing_values.append(task)
                   
        
            output.write(desk_name)
            output.write(',')
            for idx, column in enumerate(sorted_columns):
                output.write(aggregation[column.column_name])
                output.write(',')
                if column.column_name in desk.limits:
                    limit = desk.limits[column.column_name]
                    output.write(limit.limit_value)                
                    output.write(',')
                    if (abs(float(aggregation[column.column_name])) > float(limit.limit_value)):            
                        output.write('TRUE')            
                        output.write(',')
                        breach_list = None
                        if desk_name in breaches:
                            breach_list = breaches[desk_name]
                        else:
                            breach_list = []
                            breaches[desk_name] = breach_list
                        breach_list.append([column.column_name, str(aggregation[column.column_name]), str(limit.limit_value)])
                            
                    else:
                        output.write('FALSE')            
                        output.write(',')
                else:
                    output.write(',')
                    output.write(',')
                                            
            output.write('\n')   

     
    tasks_with_missing_values = list(set(tasks_with_missing_values))
    
    newline='\t\n'
    summary.write('Number of desks with a breach: %s%s'%(len(breaches.keys()), newline))
    summary_file.write('Number of desks with a breach: %s%s'%(len(breaches.keys()), newline))
    for desk_name in desk_names:
        if desk_name in breaches:    
            summary.write('%-60s%-20s%s' %(desk_name, len(breaches[desk_name]), newline))
            summary_file.write('%s,%s%s' %(desk_name, len(breaches[desk_name]), newline))
    summary.write(newline+newline)
    summary_file.write(newline+newline)
    
    summary.write('Number of desks with missing values: %s%s'%(len(missing.keys()), newline))
    summary_file.write('Number of desks with missing values: %s%s'%(len(missing.keys()), newline))
    for desk_name in desk_names:
        if desk_name in missing:  
            summary.write('%-60s%-20s%s' %(desk_name, len(missing[desk_name]), newline))
            summary_file.write('%s,%s%s' %(desk_name, len(missing[desk_name]), newline))
            
    summary.write('%sTasks with missing values: %s' % (newline, str(tasks_with_missing_values))) 
    summary_file.write('%sTasks with missing values: %s' %(newline, str(tasks_with_missing_values))) 
    
    summary.write(newline+newline) 
    summary_file.write(newline+newline) 
    
    summary.write('Breach Summary%s'%newline)
    summary_file.write('Breach Summary%s'%newline)
    summary.write('%-60s%-20s%-20s%-20s%s' %('Desk', 'Column', 'Value', 'Limit', newline))
    summary_file.write('%s,%s,%s,%s%s' %('Desk', 'Column', 'Value', 'Limit', newline))
    for desk_name in desk_names:
        if desk_name in breaches:    
            for b in breaches[desk_name]:
                summary.write('%-60s%-20s%-20s%-20s%s' %(desk_name, b[0], b[1], b[2], newline))
                summary_file.write('%s,%s,%s,%s%s' %(desk_name, b[0], b[1], b[2], newline))
    summary.write(newline+newline+'Environment: '+env)
    
    portfolio_detail.write('\n\nMissing Detail\n')
    portfolio_detail.write('Desk\tPortfolio\tColumn\n')
    for desk_name in desk_names:
        if desk_name in missing:    
            for m in missing[desk_name]:
                portfolio_detail.write(desk_name)
                portfolio_detail.write(',')
                portfolio_detail.write(','.join(m))
                portfolio_detail.write('\n')            
    portfolio_detail.write('\n\n')

    
    summary_message = summary.getvalue()
    
    log("Writing report to %s" % outputfile_csv)
    f = open(outputfile_csv, 'w')    
    f.write(summary_file.getvalue()) 
    f.write(output.getvalue()) 
    f.write(portfolio_detail.getvalue()) 
    f.write('\n\nEnvironment: %s' %env) 
    
    f.close() 
    output.close()          
    summary.close()          
    portfolio_detail.close()
        
    
    if email_address:
        #message = "\n\nSee the file %s for details\n\n" % outputfile_csv
        #message = message + summary_message
        message = summary_message
        #acmtoday =  acm.Time.DateToday()
        acmtoday=date
        rtb_location = 'Y:\Jhb\FAReports\AtlasEndOfDay\TradingManager\%s\IntraDayTriggerMon_Report_All_Desks_%s.csv ' %(acmtoday, datetime.strptime(acmtoday, '%Y-%m-%d').strftime('%y%m%d')   )
        #message = message + "\n\nSee the file %s for details\n\n" % outputfile_csv
        message = message + "\n\nSee the file %s for details\n\n" % rtb_location
        if missing_entities:
            message += '\n\nMissing entities:\n'
            message += '; '.join(missing_entities)
        print message
        send_mail(email_address, "IntraDayTriggerMonitoring: Trigger Exception", message)
        print 'Done sending mail'





def addDeltaToTime(date, deltaStr):
    deltaStr = deltaStr.replace(' ', '')
    last = deltaStr[len(deltaStr)-1]
    delta = int(deltaStr[0:len(deltaStr)-1])
    if last.upper() == 'D':
        diff = timedelta(days=delta)
    elif last.upper() == 'W':
        diff = timedelta(weeks=delta)
    elif last.upper() == 'Y':
        diff = timedelta(years=delta)
    else:
        msg = "Invalid delta string '%s'" % (deltaStr)
        raise Exception(msg)
    day = date + diff
    return day.strftime('%Y-%m-%d')
    
    
def deleteTimeSeries(deleteDate, max_delete):
    print "\nDeleting TimeSeries older than %s. Max to delete: %i" % (deleteDate, max_delete)

    query = """
    select tsdv.seqnbr
    from time_series_dv tsdv,time_series_dv_spec tsdvs
    where tsdv.ts_dv_specnbr = tsdvs.specnbr
    and tsdvs.field_name = '%s'
    and tsdv.date <='%s'
    """ % (
        timeSeriesSpecName, deleteDate
    )
    
    res = ael.dbsql(query)[0]
    found = len(res)
    
    to_delete = res[:max_delete]
    
    deleteCount = 0
    

    for seqnbr in to_delete:
        #print seqnbr
        ts = ael.TimeSeriesDv[seqnbr[0]]
        if ts:
            ts.delete()
            deleteCount = deleteCount + 1 

    print "Removed %s TimeSeries records (found %s)\n" % (deleteCount, found)
    
    
    
def runTask(portfolios):
    for portfolio in portfolios:
        if portfolio.IsKindOf(acm.FCompoundPortfolio):
            runTask(portfolio.AllPhysicalPortfolios())            
        
        trades = portfolio.Trades()
        trade_count = len(trades) 
        last_trade = 0
        if trade_count > 0:
            last_trade = max(trade.Oid() for trade in trades)   
        
        log("Portfolio '%s' contains %s trades" % (portfolio.Name(), trade_count))

    
        context = 'Standard'
        sheet_type = 'FPortfolioSheet'
        global_values = {'Portfolio Profit Loss Start Date':'Inception', 'Portfolio Profit Loss End Date':'Now', 'Position Currency Choice':'Accounting Cur'}

        start_time = time()
        calculation_results = runCalc(context, sheet_type, global_values, portfolio)
        end_time = time()

        st = datetime.fromtimestamp(start_time)
        et = datetime.fromtimestamp(end_time)
        duration = et - st
                
        log("Calculated %s results in %s" % (len(calculation_results), duration)) 

        log("Writing Results")  
        now = acm.Time.DateNow()
        for calculation_result in calculation_results:
            try:
                writeResult(now, portfolio, calculation_result.column_name, calculation_result.denominated_value)
            except Exception, e:
                print e  
            
        ccy = acm.FCurrency['ZAR']
        writeResult(now, portfolio, 'Calculation_Last_Trade', acm.DenominatedValue(last_trade, ccy, now))
        writeResult(now, portfolio, 'Calculation_Trade_Count', acm.DenominatedValue(trade_count, ccy, now))
        writeResult(now, portfolio, 'Calculation_Start_Time', acm.DenominatedValue(start_time, ccy, now))
        writeResult(now, portfolio, 'Calculation_End_Time', acm.DenominatedValue(end_time, ccy, now))

        log("Done!")  


def getTimeSeries(spec, date, portfolio, choiceList):
    query = "timeSeriesDvSpecification = '%s' and storageDate = '%s' and recordAddress1 = %s and recordAddress2 = %s" % (spec.FieldName(), date, portfolio.Oid(), choiceList.Oid())
    ts = acm.FTimeSeriesDv.Select(query)
    if ts:    
        return ts[0]
    
def writeResult(date, portfolio, column_name, denominatedValue):
    spec = acm.FTimeSeriesDvSpec['LimitMonitoring']
    choiceList = acm.FChoiceList.Select("name = '%s' and list = '%s'" % (column_name, choiceListName))[0]

    ts = getTimeSeries(spec, date, portfolio, choiceList)
 
    if ts:
        pass
    else:
        ts = acm.FTimeSeriesDv()
        ts.TimeSeriesDvSpecification(spec)
        
    if (isinstance(denominatedValue, float) or isinstance(denominatedValue, int)):
        ts.DvValue(denominatedValue)
    else:
        try:
            is_dv = denominatedValue.IsKindOf(acm.FDenominatedValue)
        except:
            print 'Calculated value is not a DV or float', type(denominatedValue), denominatedValue
            is_dv = False
        
        if is_dv:        
            try:
                ts.DvValue(denominatedValue.Number())
                ts.DvCurrency(denominatedValue.Unit())
                ts.DvDate(denominatedValue.DateTime())
            except:
                print 'denominatedValue', denominatedValue
                raise
                
    ts.RecordAddress1(portfolio.Oid())    
    ts.RecordAddress2(choiceList.Oid())    

    ts.StorageDate(date)
    ts.Commit()
