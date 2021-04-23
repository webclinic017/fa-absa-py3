import acm, csv, string, FRunScriptGUI, FBDPCommon, at_time, MR_MainFunctions
from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger()

#Constants for output
BAS_FLAG = 'BAS'
HEADER_NAME = 'Position'
OBJECT = 'PositionSPEC'
TYPE = 'Position'
POSITION_UNITS_CAL = ''
POSITION_UNITS_DAYC = ''
POSITION_UNITS_FUNC = ''
POSITION_UNITS_PERD = ''
POSITION_UNITS_STRG = ''
SETTLEMENT_ACCNT_XREF = ''
SETTLEMENT_PROC_FUNC = ''
COUNTERPARTY_STRG = ''
TRADER_NAME = ''
POSITION_UNITS_UNIT = ''
INSTRUEMNT_TYPE = 'Cash'

#File names that is needed for the execution of this script
FILE_NAMES = ['MR_CASH_INSTRUMENT_ACS', 'MR_CASH_INSTRUMENT_ACS_FF',
                'MR_CASH_INSTRUMENT_GT', 'MR_CASH_INSTRUMENT_GT_FF',
                'MR_CASH_INSTRUMENT_PMB', 'MR_CASH_INSTRUMENT_PMB_FF',
                'MR_CASH_INSTRUMENT_SMB', 'MR_CASH_INSTRUMENT_SMB_FF',
                'MR_CASH_INSTRUMENT_SMT', 'MR_CASH_INSTRUMENT_SMT_FF',
                'MR_CASH_INSTRUMENT_TO', 'MR_CASH_INSTRUMENT_TO_FF']

global FILE_NAMES_STRING
FILE_NAMES_STRING = None

def setFileNamesToString():
    global FILE_NAMES_STRING
    for fileName in FILE_NAMES:
        if FILE_NAMES_STRING == None:
            FILE_NAMES_STRING = fileName
        else:
            FILE_NAMES_STRING = '%s,%s' %(FILE_NAMES_STRING, fileName)
setFileNamesToString()

#Variables that need to be set
FILE_COLUMN_NAMES_DICT = {}
CASH_PER_PORTFOLIO_PER_CURRENCY = {}

def getIdentifier(currName, portfolioName):
    return currName + '_Cash_' + portfolioName

def getInstrumentXREF(currName):
    return currName + '_Cash'

def getPortfolioXREF(portfolioName):
    acmPortfolio = acm.FPhysicalPortfolio[portfolioName]
    if acmPortfolio:
        return 'prfnbr_%i' %acmPortfolio.Oid()
    else:
        return 'prfnbr_0'

def setFileComumnNames(firstLineOfFile):
    counter = 1
    while counter <= len(firstLineOfFile) - 2:
        FILE_COLUMN_NAMES_DICT[counter] = firstLineOfFile[counter]
        counter = counter + 1

def setCashPerPortfolioPerDictionary(lineFromFile):
    portfolioName = lineFromFile[0]
    
    counter = 1
    while counter <= len(lineFromFile) - 2:
        currName = FILE_COLUMN_NAMES_DICT[counter]
        currValue = lineFromFile[counter]
        key = (currName, portfolioName)
        if key in CASH_PER_PORTFOLIO_PER_CURRENCY.keys():
            CASH_PER_PORTFOLIO_PER_CURRENCY[key] = CASH_PER_PORTFOLIO_PER_CURRENCY[key] + float(currValue)
        else:
            CASH_PER_PORTFOLIO_PER_CURRENCY[key] =  + float(currValue)
            
        counter = counter + 1

def writePositionData(outfilePath, outFileName):
    outFullFileName = outfilePath + outFileName
    
    try:
        outfile = open(outFullFileName, 'w')
    except Exception, e:
        LOGGER.exception('Could not create the output file %s with the following error message %s' %(outFullFileName, str(e)))
        LOGGER.critical('The output file could not be created. Nothing will be processed further.')
        return
        
    for outputKey in sorted(CASH_PER_PORTFOLIO_PER_CURRENCY):
        positionUnitsVAL = CASH_PER_PORTFOLIO_PER_CURRENCY[outputKey]
        currName = outputKey[0]
        instrumentXREF = getInstrumentXREF(currName)
        portfolioName = outputKey[1]
        portfolioXREF = getPortfolioXREF(portfolioName)
        identifier = getIdentifier(currName, portfolioName)
        
        if abs(positionUnitsVAL) == 0:
            continue
        
        try:
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BAS_FLAG, HEADER_NAME, OBJECT, TYPE, identifier, POSITION_UNITS_CAL, \
                        POSITION_UNITS_DAYC, POSITION_UNITS_FUNC, POSITION_UNITS_PERD, POSITION_UNITS_STRG, POSITION_UNITS_UNIT, \
                        positionUnitsVAL, instrumentXREF, portfolioXREF, SETTLEMENT_ACCNT_XREF, SETTLEMENT_PROC_FUNC, COUNTERPARTY_STRG,\
                        TRADER_NAME, portfolioName, INSTRUEMNT_TYPE, identifier))
        except Exception, e:
            LOGGER.warning('Could not write the following information to the file %s - %s' %(outputKey, positionUnitsVAL))
            LOGGER.warning('THe script will continue...')
    outfile.close()

def writeCurrencyFile(currencyNameDictionary, outFileDirectory, fileName):
    outFullFileName = outFileDirectory + fileName
    
    try:
        outfile = open(outFullFileName, 'w')
    except Exception, e:
        LOGGER.exception('Could not create the output file %s with the following error message %s' %(outFullFileName, str(e)))
        LOGGER.critical('The output file could not be created. Nothing will be processed further.')
        return
    
    for position in currencyNameDictionary.keys():
        currName = currencyNameDictionary[position]
        fCurrency = acm.FCurrency[currName]
        BASFLAG = 'BAS'
        HeaderName ='Cash Instrument'
        OBJECT = 'Cash InstrumentSPEC'
        TYPE = 'Cash Instrument'
        NAME = currName + '_Cash'
        IDENTIFIER = currName + '_Cash'
        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = currName
        BorrowCurveXREF = MR_MainFunctions.NameFix(fCurrency.MappedRepoLink(fCurrency).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        LendingCurveXREF = MR_MainFunctions.NameFix(fCurrency.MappedRepoLink(fCurrency).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        DiscountCurveXREF = MR_MainFunctions.NameFix(fCurrency.MappedMoneyMarketLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
        TheoModelXREF = 'ZAR Cash Account'
        MarketModelXREF = 'ZAR Cash Account'
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, BorrowCurveXREF, LendingCurveXREF, DiscountCurveXREF, TheoModelXREF, MarketModelXREF))
    
    zarName = 'ZAR'
    zarCash = 'ZAR_Cash'
    fCurrencyZAR = acm.FCurrency[zarName]
    curveXREFZAR = MR_MainFunctions.NameFix(fCurrencyZAR.MappedRepoLink(fCurrencyZAR).Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
    discountCurveXREFZAR = MR_MainFunctions.NameFix(fCurrencyZAR.MappedMoneyMarketLink().Link().AsString().rsplit(',')[0].lstrip("'").rstrip("'"))
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, zarCash, zarCash, CurrencyCAL, CurrencyDAYC, CurrencyPERD, zarName, curveXREFZAR, curveXREFZAR, discountCurveXREFZAR, TheoModelXREF, MarketModelXREF))

    outfile.close()

def read_file(fullFileName):
    try:
        with open(fullFileName, 'r') as file:
            data = [row for row in csv.reader(file.read().splitlines())]
        return data
    except Exception, e:
        LOGGER.error('Could not open file %s. The error message is: %s' %(fullFileName, str(e)))
        return None
    
def get_ael_variables():
    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory(r'F:\\')
    variables = AelVariableHandler()
    variables.add('inputFileDirectory',
                label = 'Input File Directory',
                default = directory_selection,
                cls = directory_selection,
                multiple = True,
                alt = 'Directory from where the input files will be uploaded from.')
    variables.add('inputFileNames',
                label = 'File Names',
                multiple = True,
                collection = FILE_NAMES,
                default = FILE_NAMES_STRING,
                alt = 'List of the files that needs to be concatenate.')
    variables.add('outputFileDirectory',
                label = 'Output File Directory',
                default = directory_selection,
                cls = directory_selection,
                multiple = True,
                alt = 'Directory to where the output files will be placed.')
    variables.add('outFileName',
                label = 'OutFile Name',
                default = 'MR_Cash_Instrument_Position',
                alt = 'The filename of the output file that will contain the positions.')
    variables.add('outFileNameCurrFile',
                label = 'Currency OutFile Name',
                default = 'MR_Cash_Instrument',
                alt = 'The filename of the output file that will contain the currencies.')
    variables.add('reportDate',
                label = 'Report Date',
                default = 'Today',
                cls = 'string',
                alt = 'The date for which the reports will be picked up and concatenated.')
    return variables
    
ael_variables = get_ael_variables()

def ael_main(dictionary):
    fileDirectory = dictionary['inputFileDirectory'].SelectedDirectory().Text()
    fileNames = dictionary['inputFileNames']
    date = dictionary['reportDate'] and FBDPCommon.toDate(dictionary['reportDate'])
    fileCounter = 1
    totalNumberOfFiles = len(fileNames)
    directoryDate = at_time.date_from_string(date).strftime('%Y-%m-%d')
    fileDate = at_time.date_from_string(date).strftime('%y%m%d')
    exitscript = False
    
    for fileName in fileNames:
        fullFileName = '%s%s/%s' %(fileDirectory, directoryDate, '%s_%s.csv' %(fileName, fileDate))

        LOGGER.info('Processing file %s, %i of %i' %(fullFileName, fileCounter, totalNumberOfFiles))
        data = read_file(fullFileName)
        if not data:
            LOGGER.critical('Stopping the entire process. Please ensure that file %s is avaialble in the specified location, %s.' %(fullFileName, fileDirectory))
            LOGGER.warning('The file is generated by n Front Arena Task with the name %s' %fileName[:len(fileName)-4])
            exitscript = True
            break
            
        setFileComumnNames(data[0]) #This will be a dictionary where the position of the column will represent a currency.
        rowCounter = 2 #The first line contains the currency header and the second line contains the portfolio row totals which are not needed.
        lenFile = len(data)

        while rowCounter <= lenFile - 1:
            setCashPerPortfolioPerDictionary(data[rowCounter]) #Cash is bucketed based on portfolio and currency.
            rowCounter = rowCounter + 1
        fileCounter = fileCounter + 1

    if exitscript == False:
        outFileDirectory = dictionary['outputFileDirectory'].SelectedDirectory().Text()
        outFileName = dictionary['outFileName']
        currencyOutFileName = dictionary['outFileNameCurrFile']
        
        writePositionData(outFileDirectory, '%s.csv' %(outFileName))
        
        writeCurrencyFile(FILE_COLUMN_NAMES_DICT, outFileDirectory, '%s.csv' %(currencyOutFileName))
        
        LOGGER.info('The script completed successfully')
    else:
        LOGGER.critical('The script encountered issues but is completed it run.')
