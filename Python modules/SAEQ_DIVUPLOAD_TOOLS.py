'''
#Purpose:    Part of the dividend upload process for FA
#              Added in trade filter MO_Divs_IndexArbitrage and excluded any stream with names ending with _SOB in del_est()
#        Copy historic dividends from stock (ZAR/XYZ) to stock (ZAR/XYZ_Breakable) if ZAR/XYZ_Breakable exists
#               Add trade filter MO_Divs_Prime ARM to the list of filters
#Department:    MO, PCG, PCG, PCG, MO
#Requester:     Francois Henrion, Tendo Kiribakka, Tendo Kiribakka, Tendo Kiribakka, Imtiyaaz Domingo
#Developer:     Zaakirah Kajee, Jaysen Naicker, Jaysen Naicker, Jaysen Naicker, Zaakirah
#CR Number:     204846, 493648, 497011, 563757, 625708, 697769,


HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-08-24 746813       Zaakirah           Changed impact analysis reports for upgrade
2013-03-19 885308       Babalo Edwana         Updated Script to use exclusion list when uploading Divs.
2013-03-26 902944       Babalo Edwana         Updated module to use consistent stream name for exclusion list between Front Arena and Upload Spreadsheet.
-----------------------------------------------------------------------
'''



# ==================================================
#       SAEQ DIVUPLOAD TOOLS
#       Part of the dividend upload process for FA
#                                     Zaakirah Kajee
# ===================================================



import ael, acm, csv, time, string, SAEQ_DIV_PORT_COMPARE, FWorksheetReport, platform
from xml.etree.ElementTree import parse
import SAEQ_DIV_EXTRACT
import re
import FReportAPI

# ==============================
#       VARIABLES
# ==============================

month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

L0 = []
L = []
ERRORS = []
RATES = [['STOCK', 'STOCK_CURR', 'DIV_CURR', 'DIVIDEND', 'PAY_DAY', 'SPOT_RATE', 'FORWARD_RATE', 'CALC_DIV']]
DIVIDENDS = [['Process', 'Instrument', 'Ex_Div', 'Rec_Date', 'Pay_Date', 'Amount', 'Currency', 'Description']]
U_INS = []

ExclusionList = []

class DivUploadReport:

    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        ts = acm.FTradingSheetTemplate['MO_Div_Impact']
        pts = acm.FArray()
        pts.Add(ts)

        temp = acm.FArray()
        temp.AddAll([acm.FTradeSelection['MO_Divs_Arbitrage'], acm.FTradeSelection['MO_Divs_Delta_One'],\
        acm.FTradeSelection['MO_Divs_Index'], acm.FTradeSelection['MO_Divs_Linear_Trading'],\
        acm.FTradeSelection['MO_Divs_SNP'], acm.FTradeSelection['MO_Divs_ST'],\
        acm.FTradeSelection['MO_Divs_SS FC Short Term'], acm.FTradeSelection['MO_Divs_SS FC Long Term'],\
        acm.FTradeSelection['MO_Divs_SS RT Short Term'], acm.FTradeSelection['MO_Divs_SS RT Long Term'],\
        acm.FTradeSelection['MO_Divs_SS Baskets'], acm.FTradeSelection['MO_Divs_Small_Cap_Prop'],\
        acm.FTradeSelection['MO_Divs_NS Risk'], acm.FTradeSelection['MO_Divs_IndexArbitrage'],\
        acm.FTradeSelection['MO_Divs_Small_Cap_Client'], acm.FTradeSelection['MO_Divs_Prime ARM']])
        self.template = pts
        self.tradeFilters = temp

    def _setDefaultparams( self, report):

        report.ambAddress = ''
        report.ambSender = ''
        report.ambSubject = ''
        report.ambXmlMessage = True
        report.clearSheetContent = True
        report.compressXmlOutput = False
        report.createDirectoryWithDate = False
        report.dateFormat = None
        report.expiredPositions = False
        report.fileDateFormat = None
        report.fileDateBeginning = False
        report.fileName = self.filename
        report.filePath = self.filepath
        report.function = None
        report.gcInterval = 5000
        report.gridOutput = False
        report.gridUseLoopbackGridClient = False
        report.gridRowPartitionCbArg = None
        report.gridRowPartitionCbClass = None
        report.gridExcludeRowCbClass = "FReportGridCallbacks.ExcludeRowManager"
        report.gridAggregateXmlCbClass = None
        report.gridTimeout = None
        report.gridRowSet = None
        report.grouping = []
        report.htmlToFile = True
        report.htmlToPrinter = False
        report.htmlToScreen = False
        report.includeDefaultData = True
        report.includeFormattedData = True
        report.includeFullData = True
        report.includeRawData = True
        report.includeColorInformation = True
        report.instrumentParts = False
        report.instrumentRows = True
        report.maxNrOfFilesInDir = 1000
        report.multiThread = False
        report.numberOfReports = 1
        report.orders = None
        report.overridePortfolioSheetSettings = False
        report.overrideTimeSheetSettings = False
        report.overrideTradeSheetSettings = False
        report.overwriteIfFileExists = True
        report.param = None
        report.performanceStrategy = 'Periodic full GC to save memory'
        report.portfolioReportName = ''
        report.portfolioRowOnly = True
        report.portfolios = None
        report.preProcessXml = None
        report.printStyleSheet = 'FStandardCSS'
        report.printTemplate = 'FStandardTemplate'
        report.reportName = ''
        report.secondaryFileExtension = '.xls'
        report.secondaryOutput = False
        report.secondaryTemplate = 'FTABTemplate'
        report.sheetSettings = {}
        report.snapshot = True
        report.storedASQLQueries = None
        report.template= self.template
        report.tradeFilters = self.tradeFilters
        report.tradeRowsOnly = False
        report.trades = None
        report.updateInterval = 60
        report.workbook = None
        report.xmlToAmb = False
        report.xmlToFile = True
        report.zeroPositions = False
        report.guiParams = None
        report.reportApiObject = None

    def CreateReport(self):
        DefaultReport = FReportAPI.FWorksheetReportApiParameters()
        self._setDefaultparams( DefaultReport)
        DefaultReport.RunScript()

#Populate Static Exclusion list to avoid parameter passing for every function that
#needs to use Exclusion List - read list once from config.
def populateExclusions(el):
    for exclusion in el:
        ExclusionList.append(exclusion)
# ==============================
#       GENERIC
# ==============================


def log(text, log_file):

    now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    line=('%s %s' % (now, string.join(text, ',  ')))
    o=open(log_file, 'a')
    o.write(line+'\n')
    o.close()


def write_file(name, data):
    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()


def read_file(name):
    f = open(name, 'rt')
    t = []
    reader = csv.reader(f)
    headers = reader.next()

    try:
        reader = csv.DictReader(f, fieldnames=headers)
        for row in reader:
            #Strip blanks from csv file, no need for blanks explicit function.
            if [True for v in row.values() if v.strip()]:
                t.append([row['Stock'], row['Ex-Date'], row['Rec-Date'], row['Pay-Date'], row['Amount'], row['Curr'], row['Type'] ])
    finally:
        f.close()
    return t

def get_config(filename):

    file = open(filename, "r")
    tree = parse(file)
    elem = tree.getroot()
    config = {'Server':'', 'Username': '', 'Password':'', 'Address': [], 'Stream':[], 'Data':'', 'DivGrowth':'', 'Growth':'', 'GrowUntil':'', 'FileName':'', 'Dir':''}
    for i in elem.getiterator():
        if i.tag in config.keys():
            if i.tag in ('Address', 'Stream'):
                config[i.tag].append(i.text)
            elif i.tag == 'Data':
                config['FileName']= i.attrib['FileName']
                config['Dir']= i.attrib['Dir']
            elif i.tag == 'DivGrowth':
                config[i.tag] = i.attrib['GrowDivs']
            else:
                config[i.tag] = i.text
    file.close()
    return config

def current(l):
    if l[1] == today:
        return 1
    else:
        return 0

def estimate(l):
    if l[1] > today:
        return 1
    else:
        return 0

def format_data(index, object):
    stock = (object[0].replace('J.J', '')).replace('Jn.J', '')
    amount = float(object[4])
    des = object[6]
    ex = ael.date(object[1])
    rec = ael.date(object[2])
    pay = ael.date(object[3])
    curr = object[5]
    typ =object[6]
    temp = [stock, ex, rec, pay, amount, curr, typ]
    for lo in L:
        if lo[0] == temp[0] and lo[1] == temp[1] and lo[6] == temp[6]:
            if ex >= today:
                es = ['WARNING: duplicate data', str(stock), str(ex), str(typ)]
                log(es, log_file)

            return 0

    #Exclude streams in the exclusion list
    if stock not in ExclusionList:
        L.append(temp)

    return 1


def blanks(object):
    if object[4] == '':
        object[4] = '0.0'

    try:
        object.index('')
        es = ['WARNING: blank elements', str(object[0]), str(object[1]), str(object[2]), str(object[3]), str(object[4]), str(object[5]), str(object[6])]
        log(es, log_file)
        print 'ERRROR: blank elements', object

    except ValueError:
        L0.append(object)
        return object


def delete_est(stream):
    try:
        ael.begin_transaction()

        s_c = stream.clone()
        for e in s_c.estimates():
            try:
                e.delete()
            except:
                es = ['ERRROR: Estimate not deleted: ', stream.name, str(e.ex_div_day), e.description]
                log(es, log_file)
        try:
            s_c.commit()
        except:
            print 'ERRROR: stream not updated', stream.name
        ael.commit_transaction()
        ael.poll()
        return 1
    except:
        ael.abort_transaction()
        return 0


def create_dict(l):
    dict = {}
    for  d in l:
        if d[0] in dict.keys():
            dict[d[0]].append(d)
        else:
            dict[d[0]] = [d]
    return dict


# ==============================
#       DIV ESTIMATES FUNCS
# ==============================

def add_dividend_est(stream, data_list, spec):
    try:
        ael.begin_transaction()
        s_c = stream.clone()

        for data in data_list:
            if data[6] != 'Special' or spec == 1:
                newe = ael.DividendEstimate.new(s_c)
                newe.ex_div_day = data[1]
                newe.day = data[2]
                newe.pay_day = data[3]
                newe.dividend = fx_conv(stream.insaddr, data[5], data[3], data[4], stream.name)
                newe.curr = stream.insaddr.curr
                newe.tax_factor = 1
                newe.description = data[6]

                try:
                    newe.commit()
                except:
                    es = ['ERRROR: Estimate not added', stream.name, str(newe.ex_div_day), newe.description]
                    log(es, log_file)

        try:
            s_c.commit()

        except:
            es = ['ERRROR: stream not updated', stream.name]
            log(es, log_file)
            print 'ERRROR: stream not updated', stream.name
        ael.commit_transaction()
        ael.poll()
        return 1
    except:
        ael.abort_transaction()
        return 0

def get_estimates():
    lst = [['Stream', 'Instrument', 'Ex_Div', 'Rec_Date', 'Pay_Date', 'Amount', 'Description'] ]
    streams = ael.DividendStream.select()
    for strm in streams.members():
        stream = strm.name
        ins = strm.insaddr.insid
        for est in strm.estimates():
            lst.append([stream, ins, est.ex_div_day, est.day, est.pay_day, est.dividend, est.description])
    return lst

def del_est():
    streams = ael.DividendStream.select()
    for strm in streams.members():
        stream = strm.name
        if re.search('_SOB$', stream) == None:
            #Do not delete stream in exclusion list
            if stream:
                if stream not in ExclusionList:
                    delete_est(strm)
                else:
                    es = ['INFO: Will not delete Excluded Dividend Stream ', (stream)]
                    log(es, log_file)
            
def upload_est(ins):
    for i in ins.keys():
        if ael.DividendStream[i]:
            s = ael.DividendStream[i]
            add_dividend_est(s, ins[i], 0)
            if s.insaddr.insid not in U_INS:
                U_INS.append(s.insaddr.insid)
        if ael.DividendStream[(i+'1')]:
            add_dividend_est(ael.DividendStream[(i+'1')], ins[i], 1)
        else:
            es = ['WARNING: Missing Dividend Stream ', (i+'1')]
            log(es, log_file)


# ==============================
#       DIVIDEND FUNCS
# ==============================


def add_dividends(stock, data_list, des):
    try:
        ael.begin_transaction()
        s_c = stock.clone()

        for data in data_list:

            newe = ael.Dividend.new(s_c)

            newe.ex_div_day = data[1]
            newe.day = data[2]
            newe.pay_day = data[3]
            newe.dividend = fx_conv(stock, data[5], data[3], data[4], stock.insid)
            newe.curr = stock.curr
            newe.tax_factor = 1
            newe.description = data[6]

            try:
                newe.commit()

                DIVIDENDS.append([des, stock.insid, data[1], data[2], data[3], newe.dividend, stock.curr.insid, data[6]])
            except:
                es = ['ERRROR: Dividend could not be added', stock.insid, str(data[1]), str(data[6]), str(val)]
                log(es, log_file)
                print 'ERRROR: couldnt add dividend', data
        try:
            s_c.commit()
        except:
            es = ['ERRROR: Instrument not updated', stock.insid]
            log(es, log_file)
            print 'ERROR: Instrument not updated', stock.insid
        ael.commit_transaction()
        ael.poll()
        return 1
    except:
        ael.abort_transaction()
        return 0


def upload_divs(ins, des):
    for i in ins.keys():

        if ael.Instrument[('ZAR/' + i)]:
            inst = ael.Instrument[('ZAR/' + i)]
            numb = str(inst.insaddr)

            acm.FDividend.Select("exDivDay = '%s' and instrument = '%s'" %(dateS, numb)).Delete()
            add_dividends(ael.Instrument[('ZAR/' + i)], ins[i], des)
            if inst.insid not in U_INS:
                U_INS.append(inst.insid)
        if ael.Instrument[('ZAR/'+ i+'3')]:
            inst = ael.Instrument[('ZAR/'+ i+'3')]
            numb = str(inst.insaddr)
            acm.FDividend.Select("exDivDay = '%s' and instrument = '%s'" %(dateS, numb)).Delete()
            add_dividends(ael.Instrument[('ZAR/' + i + '3')], ins[i], des)

        if ael.Instrument[('ZAR/'+ i+'_Breakable')]:
            inst = ael.Instrument[('ZAR/'+ i+'_Breakable')]
            numb = str(inst.insaddr)
            acm.FDividend.Select("exDivDay = '%s' and instrument = '%s'" %(dateS, numb)).Delete()
            add_dividends(ael.Instrument[('ZAR/' + i + '_Breakable')], ins[i], des)
# ==============================
#       OTHER FUNCS
# ==============================

def ABSA_get_ircurveinfo(yc, ins):
    valday = acm.Time.DateToday()
    if yc.Category() not in ('AttributeSpreadCurve', 'InstrumentSpreadCurve', 'InstrumentSpreadCurveBidAsk'):
        return yc.IrCurveInformation(valday)
    elif yc.Category() == 'AttributeSpreadCurve':
        if not ins:
            return
        if yc.AttributeType() == 'Currency':
            if ins.Category() == 'Currency':
                curr = ins
            else:
                curr = ins.Currency()
            ycatt = yc.YCAttribute(curr, curr)

        if ycatt.UnderlyingCurve():
            und = ycatt.UnderlyingCurve()
        else:
            und = yc.UnderlyingCurve()
        return ycatt.IrCurveInformation(ABSA_get_ircurveinfo(und, ins), valday)

        return None

def ABSA_get_ircurveinfo(yc, ins):
    valday = acm.Time.DateToday()
    if yc.Category() not in ('AttributeSpreadCurve', 'InstrumentSpreadCurve', 'InstrumentSpreadCurveBidAsk'):
        return yc.IrCurveInformation(valday)
    elif yc.Category() == 'AttributeSpreadCurve':
        if not ins:
            return
        if yc.AttributeType() == 'Currency':
            if ins.Category() == 'Currency':
                curr = ins
            else:
                curr = ins.Currency()
            ycatt = yc.YCAttribute(curr, curr)

        if ycatt.UnderlyingCurve():
            und = ycatt.UnderlyingCurve()
        else:
            und = yc.UnderlyingCurve()
        return ycatt.IrCurveInformation(ABSA_get_ircurveinfo(und, ins), valday)

        return None

def fx_conv(stock, quoted_curr, pay_day, div, scode):
    if stock.curr.insid != quoted_curr:

        Curve = {'ZAR':'ZAR-BASIS','USD':'USD-SWAP','GBP':'GBP-BASIS','EUR':'EUR-BASIS','CHF':'CHF-BASIS'}
        DayC = 'ACT/365'

        ycf_ins = acm.FYieldCurve[Curve[stock.curr.insid]]
        ycf_quote = acm.FYieldCurve[Curve[quoted_curr]]
        ins = acm.FInstrument[stock.insid]
        today =  ins.Currency().Calendar().AdjustBankingDays(acm.Time().DateNow(), 2)
        ymd = pay_day.to_ymd()
        apay_day = acm.Time.DateFromYMD(ymd[0], ymd[1], ymd[2])
        curr = acm.FInstrument[quoted_curr]
        I_Discount = ABSA_get_ircurveinfo(ycf_ins, ins).Rate(today, apay_day, 'Discount', 'ACT/365', 'Discount', None, 0)
        Q_Discount = ABSA_get_ircurveinfo(ycf_quote, curr).Rate(today, apay_day, 'Discount', 'ACT/365', 'Discount', None, 0)

        FXSpot = ael.Instrument[quoted_curr].used_price(ael.date_today(), stock.curr.insid)
        FXForward = FXSpot * (Q_Discount/I_Discount)
        convert = div * FXForward
        RATES.append([scode, stock.curr.insid, quoted_curr, div, pay_day, FXSpot, FXForward, convert])
        return convert
    else:

        RATES.append([scode, stock.curr.insid, quoted_curr, div, pay_day, 1, 1, div])
        return div



def grow_divs(gfac, endYear, el, log_file):
    growth = (1+(gfac/100.0))
    streams = ael.DividendStream.select()
    dates= []
    for strm in streams:
        if strm.name not in el:
            slist = []
            temp = []
            year = ael.date_today().to_ymd()[0]
            for i in strm.estimates():

                if i.description != 'Special':
                    slist.append([i.day, i.dividend])

            if slist:
                slist.sort()
                x= max(strm.div_per_year, 1)
                while x > 0:
                    temp.append([strm, slist[len(slist)-x][0], slist[len(slist)-x][1]])
                    x-=1
            if temp:
                dates.append(temp)


    for d in dates:
        cy =  d[0][1].add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')
        div = d[0][2]
        years = 1
        while cy <= endYear:

            for i in d:

                rec = i[1].add_years(years).adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')
                strm = i[0].clone()
                new = ael.DividendEstimate.new(strm)
                new.day = rec
                new.ex_div_day = rec.add_banking_day(ael.Instrument['ZAR'], -4)
                new.pay_day = rec.add_banking_day(ael.Instrument['ZAR'], 1)
                new.dividend = i[2]* pow(growth, years)
                new.curr = ael.Instrument['ZAR']
                new.tax_factor = 1
                new.description = 'Simulated'
                try:
                    new.commit()
                    strm.commit()

                except:
                    log(['ERROR:  Estimate not added to stream '+ strm.name], log_file)


            years +=1
            cy = cy.add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'], 'Following')


def impact(dir, filen, log_file):

    fpath = acm.FFileSelection()
    fpath.PickDirectory(True)
    fpath.SelectedDirectory(dir)

    divreport = DivUploadReport(filen, fpath)

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Impact Analysis start....'
    log(['INFO:  Impact Analysis start....'], log_file)
    divreport.CreateReport()
    log(['INFO:  Impact Analysis completed....'], log_file)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Impact Analysis completed....'
    return 1



def compare_reports(file1, file2, resultfile):

    diff_result = SAEQ_DIV_PORT_COMPARE.diff(file1, file2, "OutPut", 1, 10e-10)
    #print diff_result
    list1 = [['PORTFOLIO', 'INSTRUMENT', 'COLUMN', 'BEFORE', 'AFTER', 'ABS DIFFERENCE', 'DIFFERENCE', 'RELATIVE DIFF']]
    for (column, diff_lists) in diff_result.iteritems():
        for diff_list in diff_lists:

            l0 = []
            s0 = diff_list[0].split('^')
            l0.append(s0[0])
            if len(s0) > 1:
                l0.append(s0[1])
            else:
                l0.append('Portfolio Summary')
            l0.append(column)
            if diff_list[3] == 'None':
                diff_list[3] = 0.0

            if diff_list[4] == 'None':
                diff_list[4] = 0.0
            l0.append(diff_list[4])
            l0.append(diff_list[3])
            l0.append(diff_list[1])
            if not isinstance(diff_list[3], float) and not isinstance(diff_list[3], int):
                diff_list[3] = float(diff_list[3].replace(',', ''))
            if not isinstance(diff_list[4], float) and not isinstance(diff_list[4], int):
                diff_list[4] = float(diff_list[4].replace(',', ''))
            #l0.append(abs(diff_list[3]- diff_list[4]))
            l0.append(diff_list[3]- diff_list[4])
            l0.append(diff_list[2])
            list1.append(l0)


    write_file(resultfile, list1)

# ==============================
#       MAIN
# ==============================

def upload(dir,config,logf, *rest):

    ael.poll()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Upload Process Started.......'
    global log_file
    global dateS, today, dateT
    today = ael.date_today()
    dateS =  today.to_string('%Y-%m-%d')
    dateT = time.strftime('%Y-%m-%d_%Hh%Mh%Ss', time.localtime(time.time()))
    log_file = logf
    log(['INFO:  Upload Process Started.......' + dir ], log_file)
    print dir, config, logf
    log(['INFO:  Upload Process Started.......'], log_file)
    log(['INFO:  Connected to server: ' + str(config['Server'])], log_file)

    # Populate Exclusion List from Config
    populateExclusions(config['Stream'])
    # MOVE ESTIMATES
    list1 = []
    ex = acm.FDividendEstimate.Select("exDivDay = '%s'" %dateS)
    for i in ex:
        list1.append([i.DividendStream().AsString(), ael.date(i.ExDivDay()), ael.date(i.RecordDay()), ael.date(i.PayDay()), i.Amount(), i.Currency().Name(), i.Description()])
    dict = create_dict(list1)
    log(['INFO:  Moving Historical Dividends from Dividend Estimates'], log_file)

    upload_divs(dict, 'MOVE FROM ESTIMATE')
    log(['INFO:  Completed moving Historical Dividends from Dividend Estimates'], log_file)
    ael.poll()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Completed moving historical....'
    # DELETE UPLOAD

    data = read_file(config['FileName'])

    [blanks(object) for object in data]
    log(['INFO:  BLANKS'], log_file)
    [format_data(index, object) for index, object in enumerate(L0)]
    log(['INFO:  FORMAT DATA '], log_file)
    curr = [x for x in L if current(x)]
    log(['INFO:  CURRENT DIVIDENDS '], log_file)
    est = [x for x in L if estimate(x)]
    log(['INFO:  ESTIMATE DIVIDENDS '], log_file)
    log(['INFO:  Taking Snapshot of current dividend estimates'], log_file)
    write_file(dir + '\\ESTIMATES_BEFORE_' + dateT + '.csv', get_estimates())
    log(['INFO:  Begin Deleting Dividend Estimates'], log_file)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Begin deleting all estimates....'
    del_est()
    ael.poll()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Deleted all estimates....'
    log(['INFO:  Deleted Dividend Estimates'], log_file)

    ins = create_dict(est)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Begin uploading all estimates....'
    log(['INFO:  Begin Uploading new Estimates'], log_file)
    upload_est(ins)
    ael.poll()
    log(['INFO:  Completed Uploading new Estimates'], log_file)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Uploaded all estimates....'
    write_file(dir + '\\ESTIMATES_AFTER_' + dateT + '.csv', get_estimates())


    c = create_dict(curr)
    log(['INFO:  Begin Uploading historical dividends'], log_file)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Begin Uploading all historical dividends....'
    upload_divs(c, 'UPLOAD FROM DATA')
    ael.poll()
    log(['INFO:  Completed Uploading historical dividends'], log_file)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Uploaded all historical dividends....'

    write_file(dir + '\\RATES_' + dateT + '.csv', RATES)
    write_file(dir + '\\UPLOADED_DIVIDENDS_' + dateT + '.csv', DIVIDENDS)
    ael.poll()


    if config['DivGrowth'].lower() == 'yes':
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Grow Dividends Begin.......'
        log(['INFO:  Begin growing dividend estimates'], log_file)
        grow_divs(float(config['Growth'])*100.0, ael.date(config['GrowUntil']), config['Stream'], log_file)
        log(['INFO:  Completed growing dividend estimates'], log_file)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Grow Dividends Completed.......'
    ael.poll()

    log(['INFO:  Run script to create extracts'], log_file)
    SAEQ_DIV_EXTRACT.SaveSSDivsToFile(U_INS, dir + r"\\ssdivs" + dateT + ".txt")
    SAEQ_DIV_EXTRACT.SaveIndexDivsToFile(["ZAR/ALSI", "ZAR/SWIX"], dir + r"\indexdivs" + dateT + ".txt")
    file = open(r"C:\temp\DivExtract_Dates.txt", "w")
    try:
        file.write(dateT)
    finally:
        file.close()


    MyOutput = 'Dividends have been uploaded into Front Arena by the user: %s on %s, from the machine %s.' %(acm.UserName(), ael.date_today(), platform.node())
    MySubject = 'FRONT ARENA PRODUCTION DIVIDEND ALERT'

    for a in config['Address']:
        ael.sendmail(a, MySubject, MyOutput)

    log(['INFO:  Upload Process Completed.......'], log_file)
    ael.poll()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ':  Upload Process Completed.......'


def test():
    return 'TEST FUNCTION'
