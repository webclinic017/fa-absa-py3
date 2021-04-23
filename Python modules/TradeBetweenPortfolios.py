import acm, csv, ael, FRunScriptGUI
'''
Date                    : 2010-04-13
Purpose                 : Reads a datafile, then automatically books the specified trades between the portfolios, successful trades will be removed from the datafiles
Department and Desk     : FO Eq Arb Trader
Requester               : Lulama Wakaba
Developer               : Rohan van der Walt
CR Number               : 283212
'''
fileSelection = FRunScriptGUI.InputFileSelection()
fileSelection.FileFilter('CSV Files (*.csv)|*.csv')

ael_variables = [['fileLocation', 'Batch Operation File Location', fileSelection, None, fileSelection, 0, 1, None, None, 1]]

ael_gui_parameters = {  'hideExtraControls':True,
                        'windowCaption':'Automatic Mirror Trades From File'}

def ael_main(dict):
    doTradesBetweenPortfolios(dict['fileLocation'])

def createMirrorTrade(originalTrade, toPortfolio):
    mirrorTrade = originalTrade.Clone()
    mirrorTrade.Portfolio( toPortfolio )
    mirrorTrade.Acquirer( originalTrade.Counterparty() )
    mirrorTrade.Counterparty( originalTrade.Acquirer() )
    mirrorTrade.Quantity( -originalTrade.Quantity() )
    mirrorTrade.Premium( -originalTrade.Premium() )
    return mirrorTrade
    
def doTradesBetweenPortfolios(dataFile):
    successfulTrades = []
    file = open(str(dataFile))
    reader = csv.DictReader(file)
    trade, mirrorTrade = None, None
    for row in reader:
        try:
            acm.BeginTransaction()
            trade = acm.FTrade()
            trade.Instrument( row['InstrumentID'] )
            trade.Price( row['Price'] )
            trade.Portfolio( row['ToPortfolio'] )
            trade.Acquirer( row['ToAcquirer'] )
            trade.Counterparty( acm.FParty[row['FromAcquirer']] )
            trade.Quantity( float(row['Quantity']) )
            trade.Premium( -trade.Quantity() * trade.Price() * trade.Instrument().Quotation().QuotationFactor())
            trade.ValueDay( acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.FDateTime(), 5) )
            trade.AcquireDay( acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.FDateTime(), 5) )
            trade.TradeTime( acm.FDateTime() )
            trade.Currency( trade.Instrument().Currency() )
            trade.Status( row['Status'] )
            trade.Trader( acm.User() )
            trade.Commit()
            mirrorTrade = createMirrorTrade( trade, row['FromPortfolio'] )
            mirrorTrade.Commit()
            acm.CommitTransaction()
            mirrorTrade.MirrorTrade( trade.Name() )
            mirrorTrade.Commit()
            trade.MirrorTrade( mirrorTrade.Name() )
            trade.Commit()
            print '=-'*10
            print '%s ---- %s ----> %s' % ( row['FromPortfolio'], row['InstrumentID'], row['ToPortfolio'] )
            print 'Trade Nr: %s' % (trade.Name())
            print 'Trade Nr: %s' % (mirrorTrade.Name())
            print '-='*10
            successfulTrades.append(row)
        except Exception, e:
            print "Exception: " + e.message
            acm.AbortTransaction()
    file.close()
    removeSuccessfulTradesFromFile(dataFile, successfulTrades)
    
def removeSuccessfulTradesFromFile(dataFile, successfulTrades):
    fieldnames = ['InstrumentID', 'Price', 'Quantity', 'FromPortfolio', 'FromAcquirer', 'ToPortfolio', 'ToAcquirer', 'Status']
    file = open(str(dataFile))
    reader = csv.DictReader(file)
    newSet = []
    newSet.append(fieldnames)
    for old in reader:
        if old not in successfulTrades:
            newSet.append([old[x] for x in fieldnames])
            ael.log("TradeBetweenPortfolios: FAILED - " + str(old))
    file.close()
    f = open(str(dataFile), 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(newSet)
    f.close()
