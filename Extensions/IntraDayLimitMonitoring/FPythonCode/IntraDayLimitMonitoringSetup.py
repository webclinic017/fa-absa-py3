
import ael
import acm
import IntraDayLimitMonitoring as limits

log = limits.log

def createChoiceList(choiceListName, list):
    log('Creating Choice List')    
    choiceList = acm.FChoiceList[choiceListName]
    if choiceList:
        log("Choice List %s already exists" % (choiceListName))
    else: 
        choiceList = acm.FChoiceList()
        choiceList.Name = choiceListName
        choiceList.List = list
        choiceList.Commit()
        log("Choice List %s created" % (choiceList.Name()))
 
def createTimeSeriesSpec():
    log('Creating Time Series Specification')    
    spec = acm.FTimeSeriesDvSpec[limits.timeSeriesSpecName]
    if spec:
        log("Time Series Spec %s already exists" % (limits.timeSeriesSpecName))
    else:
        spec = acm.FTimeSeriesDvSpec()
        spec.FieldName = limits.timeSeriesSpecName
        spec.Description = limits.timeSeriesSpecDescription
        spec.RecordType1 = 'Portfolio'
        spec.RecordType2 = 'ChoiceList'
        spec.Commit()
        log("Time Series Spec %s created" % (spec.FieldName()))

def createTextObject():
    to = limits.getTextObject()
    if to:
        log("Text Object %s already exists" % (to.name))
    else:
        to = ael.TextObject.new()
        to.name = limits.textObjectName
        to.subtype = limits.textObjectName
        to.type = 'Customizable'
        to.commit()
        log("Text Object %s created" % (to.name))
    return to
    
def importTextObject(file_name):
    log("Importing TextObject from %s " % (file_name))    
    f = open(file_name, 'r')
    txt = f.read()
    f.close()    
    to = createTextObject()    
    to_clone = to.clone()        
    to_clone.set_text(txt)
    to_clone.commit()    
    log("Done Importing TextObject")

def exportTextObject(file_name):
    log("Exporting TextObject to %s " % (file_name))
    ael.poll()
    txt = limits.getTextObject().get_text()    
    f = open(file_name, 'w')
    f.write(txt)
    f.close()     
    log("Done Exporting TextObject")
    
def cleanup():
    
    spec = acm.FTimeSeriesDvSpec[limits.timeSeriesSpecName]
    if spec: 
        log('Deleting Time Series Spec %s' % limits.timeSeriesSpecName)       
        tss = acm.FTimeSeriesDv.Select("timeSeriesDvSpecification = '%s'" % spec.FieldName()).AsList()
        for ts in tss:        
            ts.Delete()
            
        spec.Delete()
    else: 
        log('Time Series Spec %s does not exist' % limits.timeSeriesSpecName)
    
    choiceList = acm.FChoiceList[limits.choiceListName]
    if choiceList: 
        log('Deleting ChoiceList %s' % limits.choiceListName)
        for c in choiceList.Choices().AsList():
            log('Deleting Choice %s' % c.Name())
            c.Delete()
            
        ael.poll()
        choiceList.Delete()
    else:
        log('ChoiceList %s does not exist' % limits.choiceListName)       

    to = ael.TextObject.read("type = 'Customizable' and name = '%s'" % limits.textObjectName)
    if to:
        log("Deleting TextObject %s" % to.name)
        to.delete()
    else:
        log('TextObject %s does not exist' % limits.textObjectName)
        

def importDesks(filename):
    file = open(filename, 'r')
    data = limits.getData()
    desks = data.desks
    
    dict = {}
    missing_port = []
    for line in file.readlines():
        line = line.replace('\n', '')
        desk, port = line.split(',')
        port = port.strip()
        exist = acm.FPhysicalPortfolio[port]
        if exist:
            dict.setdefault(desk, []).append(port)
        else:
            missing_port.append(port)
    
    print dict

    for desk_name in dict:
        if desk_name not in desks:
            desk = limits.Desk(desk_name, dict[desk_name])
            print 'Added desk     ', desk_name, dict[desk_name]
            data.desks[desk_name] = desk
        else:
            
            #to_add = dict[desk_name]
            new_list = dict[desk_name]
            existing_desk = desks[desk_name]
            existing_desk.portfolio_names=new_list
            print 'Existed, updated   ', desk_name, dict[desk_name], new_list
            #existing_ports = existing_desk.portfolio_names
            #for new_item in to_add:
            #    if new_item not in existing_ports:
            #        existing_ports.append(new_item)
            #        print '---------Added' , new_item, '-----', desk_name
    file.close()
    print 'missing_port', missing_port

    limits.persistData(data)

def exportDesks(filename):
    file = open(filename, 'w')
    data = limits.getData()
    desks = data.desks
    for desk in desks:
        if desks[desk].portfolio_names:
            for portfolio in desks[desk].portfolio_names:
                line =  '%s,%s\n' % (desk, portfolio)
                print line
                file.write(line)
    file.close()
    



def importLimits(filename):

    created=[]
    
    def addLimit(data, desk_name, column_name, value):
        desks = data.desks
        if desk_name in desks:
            desk = desks[desk_name]
        
            columns = data.columns
            if column_name in columns:        
                print "Setting limit for column %s" % column_name
                limit = limits.Limit(column_name, value)
                desk.limits[column_name] = limit
            else:
                print '-----Missing column def %s ' %column_name
                
        else:
            desk = limits.Desk(desk_name, [])
            created.append(desk_name)
        
        
    def remove_limit(data, desk_name, column_name):
        desks = data.desks
        if desk_name in desks:
            desk = desks[desk_name]
            columns = data.columns
            if column_name in columns:  
                if column_name in desk.limits:
                    del desk.limits[column_name]
        
        
    file = open(filename, 'r')
    header = file.readline()
    header = header.replace('\n', '')
    columns = header.split(',')
    
    data = limits.getData()
    
    #print 'Header',header
    for line in file.readlines():
        print '\n\n'
        line = line.replace('\n', '')
        items = line.split(',')
        
        print items
        if items[0] == '':
            continue
            
        counter = 0
        for item in items:
            
            if counter ==0 :
                desk = item
                counter+=1
                continue
                
            if item <> '':
                print desk, columns[counter], '--->', item
                addLimit(data, desk, columns[counter], item)
                
            else:
                print 'CLEAN', columns[counter]
                remove_limit(data, desk, columns[counter])
            counter+=1
        
    file.close()
    limits.persistData(data)
    
    print 'created', created

def exportLimits(filename):
    file = open(filename, 'w')
    data = limits.getData()
    desks = data.desks
    all_columns=[]
    for desk in desks:
        desk_limits = desks[desk].limits
        for limit in  desk_limits:
            all_columns.append(desk_limits[limit].column_name)
            
    print all_columns
    all_columns = sorted(list(set(all_columns)))
    header = 'DESK,%s\n' % ','.join(all_columns)
    file.write(header)
    
    for desk in desks:
        desk_limits = desks[desk].limits
        line='%s,'%desk
        for column in sorted(all_columns):
            found=False
            for limit in  desk_limits:
                if desk_limits[limit].column_name == column:
                    line = '%s%s,' %(line, desk_limits[limit].limit_value)
                    found=True
                    break
            if not found:
                line = '%s,' %(line)
    
        line = '%s\n' %(line)
            
        print line,
        file.write(line)
    file.close()
    
    
def checkTasksVsDesks():
    print 'Sanity Check Running...'


    def get_task_portfolio_dict():
        duplicates=[]
        intraday_tasks = acm.FAelTask.Select('')
        portfolios = {}
        all_calcd=[]
        for task in intraday_tasks:     
            if task.ModuleName() =='IntraDayLimitMonitoringTask' and task.Name().find('IntraDayLimitMon') <>-1:
                txt = task.ParametersText()
                txt = txt.replace('portfolios=', '')
                txt = txt.replace(';', '')
                for item in txt.split(','):
                    if not (item == '' or item == ';'):
                        portfolios.setdefault(task.Name(), []).append(item)
                        if item in all_calcd:
                            duplicates.append((task.Name(), item))
                        all_calcd.append(item)
                        
        return portfolios, all_calcd, duplicates               
            
     
    print '\nScript to check which portfolios are used in Desks (IntraDayLimitMonitoring GUI) and that is not being \
    calculated in (IntraDayLimitMon? tasks) or portfolios that are calculated but not used in a Desk.\n\n'
           
    task_port_dict, all_calcd, duplicates = get_task_portfolio_dict()       

    data = limits.getData()
    desks = data.desks
    portfolios_in_desks=[]
    for desk in desks:
        portfolio_names = desks[desk].portfolio_names
        for portfolio_name in portfolio_names:
            portfolios_in_desks.append(portfolio_name)

    print 'Not Calculated in a task:'
    for portfolio in portfolios_in_desks:
        if portfolio not in all_calcd:
            for desk in desks:
                if portfolio in desks[desk].portfolio_names:
                    print '  %-80s%-20s' %(desk, portfolio)
            
    print '\n\nCalculated but not used:'
    for portfolio in all_calcd:
        if portfolio not in portfolios_in_desks: 
            for task in task_port_dict:
                if portfolio in task_port_dict[task]:
                    print '  %-80s%-50s' % (task, portfolio)
                    
    
            
    print '\n\nDuplicates:'
    for item in duplicates:
        print item
    print '\nSanity check done.'

    


def setup():
    createTextObject()

    createTimeSeriesSpec()
    createChoiceList(limits.choiceListName, 'MASTER')

    data = limits.getData()
    columns = data.columns
    for column in columns:
        createChoiceList(column, limits.choiceListName)

    createChoiceList('Calculation_Last_Trade', limits.choiceListName)
    createChoiceList('Calculation_Trade_Count', limits.choiceListName)    
    createChoiceList('Calculation_Start_Time', limits.choiceListName)
    createChoiceList('Calculation_End_Time', limits.choiceListName)
    
'''
    #createChoiceList('Portfolio Position', limits.choiceListName)
    #createChoiceList('Portfolio Theoretical Value', limits.choiceListName)
    #createChoiceList('Portfolio Total Profit and Loss', limits.choiceListName)
    #createChoiceList('Interest Rate Yield Delta Bucket 1Y', limits.choiceListName)
    #createChoiceList('Interest Rate Yield Delta Bucket 2Y', limits.choiceListName)

    #createChoiceList('Portfolio Cash Vector EUR', limits.choiceListName)
    #createChoiceList('Portfolio Cash Vector USD', limits.choiceListName)
    #createChoiceList('Portfolio Cash Vector ZAR', limits.choiceListName)
    createChoiceList('Benchmark Delta 3m-2Y', limits.choiceListName)
    createChoiceList('Equity Delta Cash', limits.choiceListName)
    createChoiceList('Cash Per Currency EUR', limits.choiceListName)
    createChoiceList('Cash Per Currency USD', limits.choiceListName)
'''    
 
'''
    columns = {}
    column = limits.StandardColumn('Portfolio Position', 'Portfolio Position', 'Pos')
    columns[column.column_name] = column
    column = limits.StandardColumn('Portfolio Theoretical Value', 'Portfolio Theoretical Value', 'ThVal')
    columns[column.column_name] = column
    column = limits.StandardColumn('Portfolio Total Profit and Loss', 'Portfolio Total Profit and Loss', 'TPL')
    columns[column.column_name] = column
    column = limits.TimeBucketColumn('Interest Rate Yield Delta Bucket 1Y', 'Interest Rate Yield Delta Bucket', 'YDelta 1Y', '1Y')
    columns[column.column_name] = column
    column = limits.TimeBucketColumn('Interest Rate Yield Delta Bucket 2Y', 'Interest Rate Yield Delta Bucket', 'YDelta 2Y', '2Y')
    columns[column.column_name] = column
    column = limits.VectorColumn('Portfolio Cash Vector EUR', 'Portfolio Cash Vector', 'Cash/CCY EUR', 'Currency', 'EUR')
    columns[column.column_name] = column
    column = limits.VectorColumn('Portfolio Cash Vector USD', 'Portfolio Cash Vector', 'Cash/CCY USD', 'Currency', 'USD')
    columns[column.column_name] = column
    column = limits.VectorColumn('Portfolio Cash Vector ZAR', 'Portfolio Cash Vector', 'Cash/CCY ZAR', 'Currency', 'ZAR')
    columns[column.column_name] = column
    column = limits.TimeBucketColumn('Benchmark Delta 3m-2Y', 'Benchmark Delta', 'PV01 3m-2Y', '3m-2Y')
    columns[column.column_name] = column

    
    desks = {}
    data = limits.PersistentData(columns, desks)
    
    limits.persistData(data)
'''   

def run001():
    print 'run001'
    data = limits.getData()
    columns = data.columns
    report_order = 1500
    currencies = ['AED', 'AOA', 'AUD', 'BRL', 'BWP', 'CAD', 'CHF', 'CNH', 'CNY', 'CZK', 'DKK', 'EGP', 'EUR', 'GBP', 'GHC', 'GHS', 'HKD', 'HUF', 'ILS', 'INR', 'JPY', 'KES', 'KMF', 'KWD', 'LSL', 'MAD', 'MAL', 'MCU', 'MNI', 'MPB', 'MSN', 'MUR', 'MWK', 'MXN', 'MYR', 'MZM', 'MZN', 'NAD', 'NGN', 'NOK', 'NZD', 'PKR', 'PLN', 'QAR', 'RUB', 'SAR', 'SCR', 'SEK', 'SGD', 'SZL', 'THB', 'TND', 'TRY', 'TZS', 'UGX', 'USD', 'XAF', 'XAG', 'XAU', 'XOF', 'XPD', 'XPT', 'XRH', 'XZN', 'ZMK', 'ZMW', 'ZWD']
    for ccy in currencies:        
        column = limits.VectorColumn('Proj Payments %s'%ccy, 'Portfolio Projected Payments Discounted Base Currency Equivalent Per Currency', 'Proj Payments %s'%ccy, report_order, True, 'Currency', ccy)
        columns[column.column_name] = column
        report_order = report_order + 100
        createChoiceList('Proj Payments %s'%ccy, limits.choiceListName)

    limits.persistData(data)

