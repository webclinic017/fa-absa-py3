
"""--------------------------------------------------------------------------
MODULE
    FileImporter

DESCRIPTION
    Module parses incoming files, creates dictionary with loan data and passes it
        to OrderCreator.
    Main class: FileImporter
        FileImporter.fileReadOK() parses the file and populate data dictionary
        FileImporter.process() finds underlying instrument and counterparty and
            calls OrderCreator
-----------------------------------------------------------------------------"""

import os
import datetime
import acm
from FSecLendRecordLookup import FInstrumentLookup, FPartyLookup
from FWorkflow import Logger
from FSecLendDealUtils import SecurityLoanCreator, GetStartingFee
import FPortfolioRouter
import FSecLendHooks


logger = Logger()

"""
the script looks for keywords below in the file
line 
      keyword value
will produce dictionary entry {keyword : value}
for 'indication of interest', 'return', 'confirm' the value is not relevant, just their existence

examples of file:
counterparty 22222222220004
SEDOL 5497102
quantity 5100
fee 2.75
settlement date 2018-06-29

"""
keywords = ['counterparty', 'quantity', 'fee', 'settlement date', 'isin', 'sedol', 'currency', 'indication of interest', 'return', 'trade id', 'confirm']

keywordsOutput = ['trade id', 'counterparty', 'quantity', 'fee', 'settlement date', 'isin', 'sedol', 'instrument', 'billing price', 'billing currency']

FInstrument = FInstrumentLookup(['ID_ISIN'])
FParty = FPartyLookup(['Id'])

SEC_LENDING_STATE_CHART = 'Securities Lending'            

def secLendBusinessProcess(trade):
    try:
        return acm.BusinessProcess.FindBySubjectAndStateChart(trade, SEC_LENDING_STATE_CHART)[0]
    except IndexError:
        return None


def createTrade(dataDict):
    """-----------------------------------------------------------------
    Uses FSecLendDealUtils.SecurityLoanCreator to create loan and trade
    -----------------------------------------------------------------"""

    instrument = dataDict['underlying']
    counterparty = dataDict.get('counterparty', None)
        
    insAttributes = {'underlying':instrument}

    if dataDict.has_key('fee'):
        insAttributes['fee'] = dataDict['fee']
    
    if dataDict.has_key('settlement date'):
        insAttributes['legStartDate'] = dataDict['settlement date'] 
            
    #if dataDict.has_key('dividendRate'):
    #    insAttributes['dividendFactor'] = float(dataDict['dividendRate']) / 100.0    
            
    if dataDict.has_key('currency'):
        insAttributes['currency'] = dataDict['currency']
    else:
        insAttributes['currency'] = instrument.Currency().Name()
        
    tradeAttributes = {    'acquirer' : FSecLendHooks.DefaultAcquirer(),
                            #'collateralAgreement' : None,
                            'status' : FSecLendHooks.DefaultTradeStatus(),
                            'source' : 'File'
                            }

    if counterparty:
        tradeAttributes['counterparty'] = counterparty

    if dataDict.has_key('quantity'):
        tradeAttributes['quantity'] = -1 * abs(float(dataDict['quantity']))
            
    loan = SecurityLoanCreator.CreateInstrument(**insAttributes)
        
    trade = SecurityLoanCreator.CreateTrade(loan, **tradeAttributes)

    trade.Portfolio(FPortfolioRouter.GetPortfolio(trade))

    if dataDict.has_key('indication of interest'):
        trade.AdditionalInfo().OrderType('IOI')
    elif dataDict.get('fee', None):
        trade.AdditionalInfo().OrderType('Limit')
    else:
        trade.AdditionalInfo().OrderType('Market')

    loan.Commit()
    trade.Commit()


class FileImporter():
    def __init__(self, filepath):
        self._filepath = filepath
        self._loanDict = {}
        

    def fileReadOK(self):        
        try:
            file = open(self._filepath, 'r')
            for line in file.readlines():
                for keyword in keywords:
                    if keyword in line.lower():
                        self._loanDict[keyword] = line[len(keyword):].strip()
            file.close()
            return True
        except:
            logger.error('Failed to process file {0}'.format(self._filepath))
            return False       
            
    def process(self):
        # find underlying instrument
        instruments = FInstrument([self._loanDict.get('isin', ''), self._loanDict.get('sedol', '')])
        if len(instruments) > 1:
            logger.info('More than one underlying found')
        if len(instruments) > 0:
            self._loanDict['underlying'] = instruments[0]
      
        # find counterparty
        counterparties = FParty([self._loanDict.get('counterparty', '')])
        if len(counterparties) > 1:
            logger.info('More than one counterparty found')
        if len(counterparties) > 0:
            self._loanDict['counterparty'] = counterparties[0]

        if self._loanDict.has_key('return'):
            self.createReturn()
        elif self._loanDict.has_key('confirm'):
            #if the file is a trade ticket and it is possible to find the trade
            self.bookTrade()
        else:
            createTrade(self._loanDict)
    
    
    def createReturn(self):
        tradeId = self._loanDict['trade id']
        quantity = abs(float(self._loanDict['quantity']))
        trade = acm.FTrade[int(tradeId)]
        if trade:
            newTrades = SecurityLoanCreator.CreateReturnTrades([trade], quantity)
            for newTrade in newTrades:
                newTrade.Commit()

        
    def bookTrade(self):
        # update securities lending business process
        tradeId = self._loanDict['trade id']
        if tradeId:
            trade = acm.FTrade[int(tradeId)]
            if trade:
                businessProcess = secLendBusinessProcess(trade)
                if businessProcess:
                    businessProcess.HandleEvent('Book')
                    businessProcess.Commit()
                    logger.info('Booked trade {0}'.format(tradeId))
                    return
        logger.info('Cannot find trade to book')


def getLoanDatafromTrade(trade):
    answerDict = {}
    answerDict['quantity'] = str(abs(trade.Quantity()))
    answerDict['trade id'] = str(trade.Oid())
    answerDict['counterparty'] = trade.Counterparty().Name()
    
    instrument = trade.Instrument()
    leg = instrument.PayLeg()
    answerDict['fee'] = str(GetStartingFee(leg))
    answerDict['dividend rate'] = str(instrument.DividendFactor()*100)
    answerDict['billing price'] = str(leg.InitialIndexValue())
    answerDict['billing currency'] = leg.Currency().Name()
        
    answerDict['trade date'] = trade.TradeTime()[0:10]
    answerDict['settlement date'] = trade.ValueDay()[0:10]
    
    answerDict['instrument'] = instrument.Underlying().Name()
    answerDict['isin'] = instrument.Underlying().AdditionalInfo().ID_ISIN()
    answerDict['sedol'] = instrument.Underlying().InstrumentAlias().SEDOL()
    
    return answerDict


def ExportTrade(trade, folder, msgType):
    loanData = getLoanDatafromTrade(trade)
    fileName = 'OUTPUT_{0}_{1}.TXT'.format(trade.Oid(), datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
    path = os.path.join(folder, fileName)
    file = open(path, 'w')
    file.write('{0}\n'.format(msgType))
    for keyword in keywordsOutput:
        if loanData.get(keyword, None):
            file.write('{0} {1}\n'.format(keyword, loanData[keyword]))
    file.close()

import zipfile
import ntpath

#pass optional timestamp format string as parameter if you wish to append to zip file name
def moveFileAndZip(sourcefile,destinationpath,timestampformat=None):
    #get file name from sourcepath
    zipFileName = ''
    if timestampformat:
        zipFileName = os.path.join(destinationpath, ntpath.basename(sourcefile))
        zipFileName = zipFileName + datetime.datetime.now().strftime(timestampformat) + '.zip'
    else:
        zipFileName = os.path.join(destinationpath, ntpath.basename(sourcefile)) + '.zip'
    #open zipfile for writing
    with zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(sourcefile, ntpath.basename(sourcefile))
    #rm unzipped file
    os.remove(sourcefile)
    return zipFileName

