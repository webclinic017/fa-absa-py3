'''
Used to combine the files created by ASQL Deriv_Cashflw_Rec and task Deriv_Cashflw_Rec_Cash_End_SERVER

Department     Requester              Developer              CR Number              Purpose
PCG            Nick Bance             Willie van der Bank    131939 12/04/2012      [Initial deployment]
PCG            Martin Kariuki         Willie van der Bank    181642 10/05/2012      [Added additional column information to the Amendments]
PCG            Martin Kariuki         Willie van der Bank    238154 2012-06-07      [Added additional manual exclusion from ASQL]
PCG            Martin Kariuki         Willie van der Bank    303927 2012-07-05      [Updated calculation on amendments]
PCG            Martin Kariuki         Willie van der Bank    354288 2012-07-27      [Updated ASQL amendments section]
PCG            Martin Kariuki         Willie van der Bank    759700 2013-02-07      [Added section to deal with Voids]
PCG            Chantel Nicholsen      Willie van der Bank    1770313 2014-03-04     [Added error handling for trades returning string values as TM cash value (like # errors]
PCG            Tammy Bourgstein       Willie van der Bank    2014-04-15 1887605     [Amended Voids section. Cash End trading manager file now includes an additional column 
                                                                                     showing the trade status and this will be used to identify voided trades]
PCG            Production Issue       Fancy Dire             2014-04-13 1957518     [Added a .rstrip() method to the status column as it contained a new line character and 
                                                                                     could not work properly in the backend]
PCG            Xolani Zondi           Fancy Dire             2014-06-09             [Added a condition to exclude all payments where the portfolio is like 'PB_REPOBOND%_CR' 
                                                                                     or 'PB_GOVIBOND%_CR' or 'PB_CORPBOND%_CR' when the difference is the sum of all the payments]
PCG            Xolani Zondi           Bhavik Mistry          CHNG0002979912         [Added funtionality to create an addition aggregated file based on Portfolio, instype, paydate]
PCG            Lai Bjorn              Bhavik Mistry          CHNG0003011030         [Added rounding to aggregate rows, as IMATCH cannot handle exponential numbers]
PCG			   Ameet Lalloo			  Faize Adams			 						[Excludes payments of type "Commitment Fee""]
'''

import ael, acm, string, os
from itertools import groupby
from operator import itemgetter

global exclusionSection

calcSpaceObj = acm.FCalculationSpaceCollection().GetSpace("FTradeSheet", "Standard")

# Function to aggregate amended Deriv_Cashflw_Rec_DATE_InclAmends file
def aggregate_file(input_file, output_file):
    file_rows = []
    agg_cashflow_rows = []
    amount = 0
    nominal = 0

    with open(input_file, 'rb') as file:
        for row in file:
            file_rows.append(row.rstrip('\n').split('|'))


    agg_cashflow_rows.append('|'.join(file_rows.pop(0)) + '\n')
    sorted_input = sorted(file_rows, key=itemgetter(16, 11, 6, 4)) #sorted by portfolio, instype, counterparty, paydate
    groups = groupby(sorted_input, key=itemgetter(16, 11, 6, 4))   #grouped by portfolio, instype, counterparty, paydate

    for key, rows in groups:
        cashflows = list(rows)
        if key[0].startswith('PB') and key[0].endswith('CR'):
            for cf in cashflows:
                try:
                    amount += float(cf[7])
                except ValueError:
                    print cf[3], 'No ammount'
                try:
                    nominal += float(cf[12])
                except ValueError:
                    print cf[3], 'No nominal'

            amount = round(amount, 4)
            nominal = round(amount, 4)
            
            agg_cashflow_rows.append('|'.join([cashflows[0][0],  #FromRepDate
                                               cashflows[0][1],  #ToRepDate
                                               '',               #TrdStatus
                                               '',               #Trdnbr
                                               cashflows[0][4],  #PayDate
                                               cashflows[0][5],  #InsExpiry
                                               cashflows[0][6],  #Counterparty
                                               str(amount),      #Amount
                                               '',               #BS
                                               '',               #TrdCurrency
                                               '',               #insid
                                               cashflows[0][11], #instype
                                               str(nominal),     #Nominal
                                               '',               #CFType
                                               '',               #CptyRef
                                               '',               #SettlementID
                                               cashflows[0][16], #prfid
                                               cashflows[0][17], #prfnbr
                                               '',               #Acquirer
                                               '',               #CptyType
                                               '',               #cfwnbr
                                               '',               #TransRef
                                               '']) + '\n')      #MirrorRef
            amount = 0
            nominal = 0
        else:
            for cf in cashflows:
                agg_cashflow_rows.append('|'.join(cf) + '\n')

    #Write to aggregated ouput file
    fhandle = open(output_file, 'w')
    for row in agg_cashflow_rows:
        fhandle.write(row)

    fhandle.close()
    
    return 'Aggregated file "' + output_file + '" created.'
    
def buildTempTables(Seperator, filename, TrdColumn, ValColumn, StusColumn, SkipLine, CashEndMin1d):
    tempTable = {}

    fhandle = open(filename)

    fline = fhandle.readline()
    while SkipLine > 0:
        fline = fhandle.readline()
        SkipLine = SkipLine - 1
    while fline:
        #try:
        line = string.split(fline, Seperator)
        if len(line) > 1:
            trd = line[TrdColumn]
            try:
                val = float(line[ValColumn])
            except:
                print 'Cash float conversion issue on trade', trd
                val = float(0)
            #If a trade already exists in the cash file, the total will be summed
            if tempTable.has_key(trd):
                val = tempTable[trd][1] + val
            #As from 2014-03-13 the Cash End file will contain the trade status as an extra column            
            #tempTable[trd] = [trd,val]
            
            #2014-05-08 Fancy Dire
            #Added the .rstrip() method to remove any white space at the end of the string, to enable correct evaluation of the Status column
            status = line[StusColumn].rstrip()                          #Exclude new line character at end of row
            tempTable[trd] = [trd, val, status]

            fline = fhandle.readline()
        else:
            break

    fhandle.close()

    return tempTable

def buildFile(filename, newfilepath, newfilename):
    if not os.path.exists(newfilepath):
        os.mkdir(newfilepath)

    tmpfile = file(newfilename, 'w')
    fhandle = open(filename)
    fline = fhandle.readline()
    tmpfile.write(fline)        #Headers

    fline = fhandle.readline()
    fline = fhandle.readline()
    
    while fline:
            try:
                if fline == '\n':
                    break
                else:
                    if '|' in fline:                        
                        tradeOid = fline.split('|')[3]
                        if not isMidasSettled(tradeOid):
                            if not isCommitmentFee(tradeOid):
                                tmpfile.write(fline)
                            else:
                                print 'Excuding cashflow for trade {0}. Trade is commitment fee'.format(tradeOid)    
                        else:
                            print 'Excuding cashflow for trade {0}. Trade is Midas settled'.format(tradeOid)
                        fline = fhandle.readline()
            except:
                break
        

    fhandle.close()
    tmpfile.close()
    return 'File "' + newfilename + '" created.'

def isCommitmentFee(tradeOid):
    trade = acm.FTrade[tradeOid]
    payments = trade.Payments()
    
    for payment in payments:
        if payment.Type() == "Commitment Fee":
            return True
    return False

def isMidasSettled(tradeOid):
    midasSettleYesNo = calcSpaceObj.CreateCalculation(acm.FTrade[tradeOid], 'midasSettlement').FormattedValue()

    if midasSettleYesNo in ('Yes', 'true'):
        return True
    else:
        return False

def writeFileMacro(i, strCash, Local, tmpfile, runDate):
    specific_portfolios = ['PB_REPOBOND', 'PB_GOVIBOND', 'PB_CORPBOND']
    paymentTotal = 0
    myTrade = checkTradeValid(i)
    if len(myTrade) == 1:
        #Get trade detail
        myAcmTrade = acm.FTrade[i]
        payments = myAcmTrade.Payments()
        
        for p in payments:
            paymentTotal = paymentTotal + round(p.Amount(), 2)
        
        strPaymentTotal = str(paymentTotal)
        Cpty = myAcmTrade.Counterparty().Name()
        InsID = myTrade[0][6]
        InsType = myTrade[0][5]
        PrfID = myAcmTrade.Portfolio().Name()
        PrfNBR = str(myAcmTrade.Portfolio().Oid())
        Acquirer = myTrade[0][3]
        Status = myAcmTrade.Status()
        TransRef = '0'
        if myAcmTrade.TrxTrade():
            TransRef = str(myAcmTrade.TrxTrade().Oid())
        CptyType = myAcmTrade.Counterparty().Type()
        
        space = ''
        line = [runDate, runDate, Status, str(i), runDate, space, Cpty, strCash, space, space, InsID, InsType, space, Local, space, '0', PrfID, PrfNBR, Acquirer, CptyType, '0', TransRef]
        wline = string.join(line, '|')
        
        if True in map(PrfID.startswith, specific_portfolios) and (PrfID.endswith('_CR')) and (strPaymentTotal == strCash):
            return
        else:
            tmpfile.write(wline + '\n')

def amendFileMacro(i, CashFile, EndCashDiff, tmpfile, runDate):

    Local = ''

    if CashFile.has_key(i):
        #Diff between EndCash and CashFlow file
        CashFileDiff = EndCashDiff - round(CashFile[i][1], 2)
        if abs(CashFileDiff) > 5:
            Local = 'Amendment of trade in file'
            strCash = str(CashFileDiff)
    elif abs(EndCashDiff) > 5:
        #If trade does not exist in cash file
        Local = 'Amendment of trade not in file'
        strCash = str(EndCashDiff)

    if Local != '':
        writeFileMacro(i, strCash, Local, tmpfile, runDate)

def amendFile(OrigNewFile, CashEnd0d, CashEndMin1d, CashFile, runDate):

    tmpfile = file(OrigNewFile, 'a')
    if len(CashEnd0d.values()[0]) >= 3 and len(CashEndMin1d.values()[0]) >= 3: #This is required for backward compatibility of Void solution, but can be removed at a later stage
        NewCashFile = True
    else:
        NewCashFile = False
    for i in CashEnd0d:
        #Voids
        #-------
        #As from 2014-03-13 the Cash End file contains the trade status as an extra column
        #aelTrade = ael.Trade[int(i)]
        #if aelTrade.status == 'Void':
        #if ael.date_from_time(aelTrade.updat_time) == ael.date(runDate):
		
        if CashEnd0d[i][2] == 'Void':
            if CashEndMin1d.has_key(i):
                if CashEndMin1d[i][2] != 'Void':
                    print '%s Reversal Generated' % i 
                    Local = 'Reversal of void'
                    try:
                        Cash = round(CashEndMin1d[i][1], 2)
                    except:
                        Cash = 0
                        
                    if abs(Cash) > 0:
                        writeFileMacro(i, str(-1 * Cash), Local, tmpfile, runDate)
        else:
            if CashEndMin1d.has_key(i):
                #Diff between EndCash files
                EndCashDiff = round(CashEnd0d[i][1], 2) - round(CashEndMin1d[i][1], 2)
            else:
                #If trade only appears in latest CashEnd file
                EndCashDiff = round(CashEnd0d[i][1], 2)
            amendFileMacro(i, CashFile, EndCashDiff, tmpfile, runDate)

    tmpfile.close()
    return 'Amend done and saved to ' + OrigNewFile + ' .'

def buildASQL():

    global exclusionSection

    asql = acm.FSQL['Deriv_Cashflw_Rec']
    text = asql.Text()
    lines = text.splitlines()

    exclusionSection = """select
        t.trdnbr,
        add_info(t,'Funding Instype')  'Funding_Instype',
        add_info(t,'MM_Instype')  'MM_Instype',
        display_id(t,'acquirer_ptynbr') 'Acquirer',
        t.insaddr,
        display_id(t,'prfnbr')  'prfid',
        t.prfnbr
    into trades
    from
        trade t
    where
            t.trdnbr in (@TradeNbr)
        /*and t.status ~= 'Void'*/
    select
        tt.trdnbr,
        tt.Funding_Instype,
        tt.MM_Instype,
        tt.Acquirer,
        tt.prfid,
        i.instype,
        i.insid,
        tt.insaddr
    into tempTrades
    from
        trades tt,
        instrument i
    where
            i.insaddr = tt.insaddr"""

    section = 'False'
    for lineNumber, line in enumerate(lines):
        if "/* **Query specific exclusions begin** */" in line:
            section = 'True'
        if section == 'True':
            exclusionSection = exclusionSection + '\n' + line
        if "/* **Query specific exclusions end** */" in line:
            section = 'False'

    # ######## Additional manual exclusion from ASQL ########
    exclusionSection = exclusionSection + '\n' + \
        """select
            t.trdnbr,
            t.Funding_Instype,
            t.MM_Instype,
            t.Acquirer,
            t.prfid,
            t.instype,
            t.insid
        into finalTrades
        from
            tempTrades t,
            leg l
        where
            t.instype = 'Deposit'
            and t.insaddr = l.insaddr
            and not (l.type = 'Fixed'
                    and not (t.Acquirer = 'STRUCT NOTES DESK'))

        select
            t.trdnbr,
            t.Funding_Instype,
            t.MM_Instype,
            t.Acquirer,
            t.prfid,
            t.instype,
            t.insid
        into finalTrades
        from
            tempTrades t
        where
            t.instype ~= 'Deposit'
        select
            t.*
        from
            finalTrades t"""

    #print exclusionSection
    return exclusionSection

def checkTradeValid(trdnbr):

    global exclusionSection

    selectASQL = exclusionSection

    Trades = ael.asql(selectASQL, 0, ['@TradeNbr'], ["'" + trdnbr + "'"])[1][0]

    return Trades

ael_variables = [('OrigCashFile', 'Cash file path:', 'string', '', 'Y:/Jhb/FAReports/AtlasEndOfDay/'),
                ('OrigCashEndMin1d', 'Previous cash end file path:', 'string', '', 'Y:/Jhb/FAReports/AtlasEndOfDay/TradingManager/'),
                ('OrigCashEnd0d', 'Today cash end file path:', 'string', '', 'Y:/Jhb/FAReports/AtlasEndOfDay/TradingManager/'),
                ('OrigNewFile', 'New cash file path:', 'string', '', 'F:/'),
                ('RunDate', 'Date', 'string', '', '', 0, 0, 'Leave blank to run for todays date')]

def ael_main(dict):

    if dict['RunDate'] == '':
        runDate = ael.date_today()
    else:
        runDate = ael.date(dict['RunDate'])

    PrevBuss = runDate.add_days(-1).adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')

    OrigCashFile = dict['OrigCashFile'] + runDate.to_string('%Y-%m-%d') + '/' + 'Deriv_Cashflw_Rec_' + runDate.to_string('%y%m%d') + '.csv'
    OrigCashEndMin1d = dict['OrigCashEndMin1d'] + PrevBuss.to_string('%Y-%m-%d') + '/' + 'Deriv_Cashflw_Rec_Cash_End_' + PrevBuss.to_string('%y%m%d') + '.csv'
    OrigCashEnd0d = dict['OrigCashEnd0d'] + runDate.to_string('%Y-%m-%d') + '/' + 'Deriv_Cashflw_Rec_Cash_End_' + runDate.to_string('%y%m%d') + '.csv'
    OrigNewPath = dict['OrigNewFile'] + runDate.to_string('%Y-%m-%d')
    OrigNewFile = OrigNewPath + '/' + 'Original_Deriv_Cashflw_Rec_' + runDate.to_string('%y%m%d') + '_InclAmends.csv'

    buildASQL()

    #Build ASQL text which contains additional trade exclusions

    #Create temp cash file
    TrdColumn = 3
    ValColumn = 7
    StusColumn = 2
    SkipLine = 2
    Seperator = '|'
    CashFile = buildTempTables(Seperator, OrigCashFile, TrdColumn, ValColumn, StusColumn, SkipLine, '')
    print 'Cash file:', OrigCashFile
    print 'Cash file size:', len(CashFile)

    TrdColumn = 0
    ValColumn = 1
    StusColumn = 2
    SkipLine = 1
    Seperator = ','

    #Create temp cash end -1d file
    CashEndMin1d = buildTempTables(Seperator, OrigCashEndMin1d, TrdColumn, ValColumn, StusColumn, SkipLine, '')
    print 'EndCash -1d file:', OrigCashEndMin1d
    print 'EndCash -1d file size:', len(CashEndMin1d)

    #Create temp cash end 0d file
    CashEnd0d = buildTempTables(Seperator, OrigCashEnd0d, TrdColumn, ValColumn, StusColumn, SkipLine, CashEndMin1d)
    print 'EndCash 0d file:', OrigCashEnd0d
    print 'EndCash 0d file size:', len(CashEnd0d)

    #Create new cash file (excl line count at end of back-end run files)
    print buildFile(OrigCashFile, OrigNewPath, OrigNewFile)

    #Add amendments to new file
    print amendFile(OrigNewFile, CashEnd0d, CashEndMin1d, CashFile, runDate.to_string('%Y-%m-%d'))
    ael.log('Wrote secondary output to:::' + OrigNewFile)
    
    #Aggregate new amendments file
    output_file = OrigNewPath + '/' + 'Deriv_Cashflw_Rec_' + runDate.to_string('%y%m%d') + '_InclAmends.csv'
    print aggregate_file(OrigNewFile, output_file)
    ael.log('Wrote secondary output to:::' + output_file)
