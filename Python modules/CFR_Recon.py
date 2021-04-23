import acm, string, ael, FLogger, at_time
import xlrd, csv
import pyodbc as odbc
from shutil import copyfile

global date
date = ael.date_today()
global datetime
datetime = date.to_string() + ' 00:00:00'
global midasDealDate
midasDealDate = date.to_string('%Y-%m-%d')
global midasData
midasData = []
global logger
logger = None
global SQLConnection
SQLConnection = None

midasFileReconChoiseList = ['CLIENT', 'SHADOW', 'BOTH']

def establishSQLConnection():
    global SQLConnection
    if SQLConnection == None:
        logger.info('Connecting to Midas DB for 4Front trade reconciliation...')
        dataSource='JHBPCM05015V05A\FXB_MAIN1_LIVE'
        #dataSource='JHBPSM05017\FXB_MAIN1_UAT'
        initialCatalog='MMG_FXF'
        connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (dataSource, initialCatalog) 
        sqlConnection = odbc.connect(connectionString, autocommit=True) 
        SQLConnection = sqlConnection.cursor() 

    return SQLConnection

def closeSQLConnection():
    global SQLConnection
    SQLConnection.close()

def executeSQLQuery(query):
    global SQLConnection
    sql = query
    
    result = SQLConnection.execute(sql).fetchall() 
    return result

def copyAFile(source, desctination):
    copyfile(source, desctination)

def setFileName(index, fieldValues):
    global date, datetime, midasDealDate
    date = ael.date(fieldValues[0])
    datetime = date.to_string() + ' 00:00:00'
    midasDealDate = date.to_string('%Y-%m-%d')
    
    fieldValues[4] = ael_variables[4][4] + 'Trueup ' + date.to_string('%Y%m%d') + '.tab'
    fieldValues[5] = ael_variables[5][4] + 'Trueup ' + date.to_string('%Y%m%d') + '.tab'
    fieldValues[6] = ael_variables[6][4] + 'Trueup sh ' + date.to_string('%Y%m%d') + '.tab'
    fieldValues[7] = ael_variables[7][4] + 'Trueup sh' + date.to_string('%Y%m%d') + '.tab'
    return fieldValues

def loadMidasData(locationAndFile):
    global midasData
    file = open(locationAndFile, 'r')

    line = file.readline()
    line = file.readline()
    
    while line:
        line = string.split(line, "\t")
        midasData.append(line)
        
        line = file.readline()
    
    del midasData[-1]
    del midasData[-1]
    del midasData[-1]
    
    file.close()

def getTrades(portfolio):
    global date, logger
    
    tradeQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    tradeQuery.AddAttrNode('Portfolio.Oid', 'EQUAL', portfolio.Oid())
    tradeQuery.AddAttrNode('ValueDay', 'GREATER_EQUAL', date.to_string('%Y-%m-%d'))

    trades = tradeQuery.Select()
    
    logger.info('Total Number of Front Arena Trades in portfolio %s: %i\n' %(portfolio.Name(), len(trades)))
    
    return trades

def buildFrontArenaTradeDictionary(trades):
    tradeDictionary = dict()
    for trade in trades:
        if trade.OptionalKey().__contains__('VOID'):
            tradeDictionary[trade.OptionalKey()[5:]] = trade
        else:
            tradeDictionary[trade.OptionalKey()] = trade
    return tradeDictionary

def buildMidasTradeDictionary(midas_portfolio):
    global midasData
    
    midasTradeDictionary = {}
    
    for midasTrade in midasData:
        dealDate = midasTrade[9]
        midasPortfolio = midasTrade[23]
        midasBrokerCode = midasTrade[0]
        
        if midasPortfolio == midas_portfolio:
            dealNo = str(int(float(midasTrade[1])))
            shadowDealNo = str(int(float(midasTrade[22])))
            midasKey = ael.date_from_string(dealDate, '%Y-%m-%d').to_string('%Y%m%d') + '_' + dealNo + '_' + shadowDealNo
            midasTradeDictionary[midasKey] = midasTrade[24]
    return midasTradeDictionary

def reconcileMidasToFrontArena(frontArenaTradeDictionary, midasTradeDictionary):
    global logger
    
    frontArenaCopy = dict(frontArenaTradeDictionary)
    midasCopy = dict(midasTradeDictionary)
    
    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    for frontTrade in frontArenaTradeDictionary.keys():
        for midasTrade in midasTradeDictionary.keys():
            if frontTrade == midasTrade:
                if (midasCopy[midasTrade] == 'REV' and frontArenaCopy[frontTrade].Status() != 'Void') or (midasCopy[midasTrade] != 'REV' and frontArenaCopy[frontTrade].Status() == 'Void'):
                    logger.info('Midas trade %s has Period %s but its corresponding trade in Front Arena, %i, has status %s.' %(midasTrade, midasCopy[midasTrade], frontArenaCopy[frontTrade].Oid(), frontArenaCopy[frontTrade].Status()))
                    continue

                del frontArenaCopy[frontTrade]
                del midasCopy[midasTrade]
    
    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    logger.info('\n')
    return frontArenaCopy, midasCopy

def reconcileMidasToFrontArenaForeFrontStreetFacing(frontArenaTradeDictionary, midasTradeDictionary, foreFrontTrades):
    global logger
    
    frontArenaCopy = dict(frontArenaTradeDictionary)
    midasCopy = dict(midasTradeDictionary)
    
    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    for tradeLine in foreFrontTrades:
        midasDealNo = tradeLine[1]
        dealDate = ael.date_from_string(tradeLine[5][:10], '%Y-%m-%d').to_string('%Y%m%d')
        frontTradeNumber = tradeLine[3]
        
        uniqueKey = '%s_%i_0' %(dealDate, midasDealNo)
        
        if uniqueKey in midasTradeDictionary.keys() and uniqueKey in frontArenaTradeDictionary.keys():
            if (midasCopy[uniqueKey] == 'REV' and frontArenaCopy[uniqueKey].Status() != 'Void') or (midasCopy[uniqueKey] != 'REV' and frontArenaCopy[uniqueKey].Status() == 'Void'):
                logger.info('Midas trade %s has Period %s but its corresponding trade in Front Arena, %i, has status %s.' %(uniqueKey, midasCopy[uniqueKey], frontArenaCopy[uniqueKey].Oid(), frontArenaCopy[uniqueKey].Status()))
                continue

            del frontArenaCopy[uniqueKey]
            del midasCopy[uniqueKey]

    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    logger.info('\n')
    return frontArenaCopy, midasCopy

def reconcileMidasToFrontArenaForeFrontShadow(frontArenaTradeDictionary, midasTradeDictionary, foreFrontTrades):
    global logger
    
    frontArenaCopy = dict(frontArenaTradeDictionary)
    midasCopy = dict(midasTradeDictionary)
    
    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    for tradeLine in foreFrontTrades:
        midasDealNo = tradeLine[0]
        midasShadowDealNo = tradeLine[1]
        dealDate = ael.date_from_string(tradeLine[3][:10], '%Y-%m-%d').to_string('%Y%m%d')
        frontTradeNumber = tradeLine[2]
        
        uniqueKey = '%s_%i_%i' %(dealDate, midasDealNo, midasShadowDealNo)
        
        if uniqueKey in midasTradeDictionary.keys() and uniqueKey in frontArenaTradeDictionary.keys():
            if (midasCopy[uniqueKey] == 'REV' and frontArenaCopy[uniqueKey].Status() != 'Void') or (midasCopy[uniqueKey] != 'REV' and frontArenaCopy[uniqueKey].Status() == 'Void'):
                logger.info('Midas trade %s has Period %s but its corresponding trade in Front Arena, %i, has status %s.' %(uniqueKey, midasCopy[uniqueKey], frontArenaCopy[uniqueKey].Oid(), frontArenaCopy[uniqueKey].Status()))
                continue

            del frontArenaCopy[uniqueKey]
            del midasCopy[uniqueKey]

    logger.info('Number of outstanding Front Arena Trades: %i' %len(frontArenaCopy.keys()))
    logger.info('Number of outstanding Midas Trades: %i' %len(midasCopy.keys()))
    
    logger.info('\n')
    return frontArenaCopy, midasCopy

def getFrontArenaTradeNumbers(frontArenaTradeList):
    frontArenaTradeNumberTuple = ()
    for trade in frontArenaTradeList:
        frontArenaTradeNumberTuple = frontArenaTradeNumberTuple + (trade.Oid(),)
    return frontArenaTradeNumberTuple

def getFrontArenaTrades(front_portfolio, midas_portfolio):
    logger.info('Retreiving CFR Trades from Front Arena...')
    frontArenaCFRTrades = getTrades(front_portfolio)
    
    logger.info('Retrieving 4Front trades from Front Arena...')
    foreFrontPortfolio = acm.FPhysicalPortfolio[midas_portfolio]
    frontArena4FrontTrades = []
    if foreFrontPortfolio:
        frontArena4FrontTrades = getTrades(acm.FPhysicalPortfolio[midas_portfolio])
    
    logger.info('Total number of Front Arena Trades: %i' %(len(frontArenaCFRTrades) + len(frontArena4FrontTrades)))
    
    return frontArenaCFRTrades, frontArena4FrontTrades

def matchingFrontArenaTradesToMidasTrades(frontArena4FrontTrades, foreFrontTradesFromMidas, foreFrontTradesShadowFromMidas):
    global logger
    frontTrades = []
    for tradeLine in foreFrontTradesFromMidas:
        frontTrades.append(tradeLine[3])
    for tradeLine in foreFrontTradesShadowFromMidas:
        frontTrades.append(tradeLine[2])
    
    for trade in frontArena4FrontTrades:
        if trade.Oid() not in frontTrades:
            logger.info('The following Front Arena trade can not be found in Midas: %i with status %s' %(trade.Oid(), trade.Status()))

def removeVoidedAndReversedTrades(frontArenaTradeDictionary, midasReversedTrades):
    voidedMidasTrades = []
    for midasLine in midasReversedTrades:
        #print str(midasLine[5].replace('-','')), str(midasLine[2]), str(midasLine[3])
        #if '%s_%s_%s' %(str(midasLine[5].replace('-','')), str(midasLine[2]), str(midasLine[3])) == '20160810_134542_0':
        #    print '@@' * 200
        voidedMidasTrades.append('%s_%s_%s' %(str(midasLine[4].replace('-', '')), str(midasLine[2]), str(midasLine[3])))

    #print frontArenaTradeDictionary.keys()
    #print voidedMidasTrades
    for trade in voidedMidasTrades:
        if trade in frontArenaTradeDictionary.keys():
            del frontArenaTradeDictionary[trade]
            
    return frontArenaTradeDictionary

def reportFrontArenaSummary(frontArenaTradeDictionary):
    global logger, date
    logger.info('The following Front Arena trades could not be found in Midas:\n')
    for trade in frontArenaTradeDictionary:
        if ael.date(str(at_time.to_datetime(frontArenaTradeDictionary[trade].CreateTime()).date())) < date:
            logger.info('Trade Number: %i with Trade Status %s and creat time %s' %(frontArenaTradeDictionary[trade].Oid(), frontArenaTradeDictionary[trade].Status(), str(at_time.to_datetime(frontArenaTradeDictionary[trade].CreateTime()))))
    logger.info('\n')

def reportMidasSummary(midasTradeDictionary):
    global logger
    logger.info('The following Midas trades could not be found in Front Arena:\n')
    for trade in midasTradeDictionary:
        logger.info('Trade Number: %s with Trade Status %s' %(trade, midasTradeDictionary[trade]))
    logger.info('\n')
    
ael_variables = [
                    ['date', 'Report Date_General Information', 'date', None, date, 1, 0, 'The report date for which the recon should run.', setFileName, 1],
                    ['portfolio', 'Portfolio(s)_General Information', acm.FPhysicalPortfolio, None, '', 1, 1, 'Portoflio(s) that will be reconciled.', None, 1],
                    ['midasFileReconOption', 'Midas Recon Selection_General Information', 'string', midasFileReconChoiseList, 'BOTH', 1, 0, 'Which Midas recon should be run against Front Arena.', None, 1],
                    ['skipFileTransfer', 'Skip File Transfer_General Information', 'int', [0, 1], 0, 0, 0, 'Files should not be copied. Use this if files were already copied.', None, 1],
                    ['sourceMidasExcelFile', 'Source_Midas Client File Locations', 'string', None, 'Y:/Jhb/Internal Audit/Public/HeinrichC/', 1, 0, 'Source file location and file name of the Midas street facing trades in .xlsx format', None, 1],
                    ['destinationMidasCSVFile', 'Destination_Midas Client File Locations', 'string', None, 'F:/', 1, 0, 'Destination file location and name of the Midas street facing trades in CSF format.', None, 1],
                    ['sourceMidasShadowExcelFile', 'Source_Midas Shadow File Locations', 'string', None, 'Y:/Jhb/Internal Audit/Public/HeinrichC/', 1, 0, 'Source file location and file name of the Midas shadow trades in .xlsx format', None, 1],
                    ['destinationMidasShadowCSVFile', 'Destination_Midas Shadow File Locations', 'string', None, 'F:/', 1, 0, 'Destination file location and name of the Midas shadow trades in CSF format.', None, 1]
                ]

def ael_main(dict):
    global date, midasData, midasDealDate, logger
    
    logger = FLogger.FLogger(logToConsole = False, logToFileAtSpecifiedPath = 'C:/temp/CFR_Recon_%s.txt' %date.to_string('%Y%m%d'))
    
    logger.info('Log File is available on: C:/temp/CFR_Recon_%s.txt' %date.to_string('%Y%m%d'))
    logger.info('Running Midas vs. Front Arena Reconcilliation...\n')
    logger.info('*' * 100)
    logger.info('Parameters...')
    logger.info('     Report Date:                    %s' %date)
    logger.info('     Portfolio(s):                   %s' %dict['portfolio'])
    logger.info('     Midas Recon Type:               %s' %dict['midasFileReconOption'])
    logger.info('     Source Midas Client File:       %s' %dict['sourceMidasExcelFile'])
    logger.info('     Source Midas Shadow File:       %s' %dict['sourceMidasShadowExcelFile'])
    logger.info('     Destination Midas Client File:  %s' %dict['destinationMidasCSVFile'])
    logger.info('     Destination Midas Client File:  %s' %dict['destinationMidasShadowCSVFile'])
    logger.info('*' * 100 + '\n')
    
    
    if dict['midasFileReconOption'] in ('CLIENT', 'BOTH'):
        if not dict['skipFileTransfer']:
            logger.info('Copying file %s...' %dict['sourceMidasExcelFile'])
            copyAFile(dict['sourceMidasExcelFile'], dict['destinationMidasCSVFile'])
        logger.info('Loading Midas Data: %s...' %dict['destinationMidasCSVFile'])
        loadMidasData(dict['destinationMidasCSVFile'])
        
    if dict['midasFileReconOption'] in ('SHADOW', 'BOTH'):
        if not dict['skipFileTransfer']:
            logger.info('Copying file %s...' %dict['sourceMidasShadowExcelFile'])
            copyAFile(dict['sourceMidasShadowExcelFile'], dict['destinationMidasShadowCSVFile'])
        logger.info('Loading Midas Shadow Data: %s...' %dict['destinationMidasShadowCSVFile'] + '\n')
        loadMidasData(dict['destinationMidasShadowCSVFile'])
    
    logger.info('Total Number of Midas Data: %i\n' %len(midasData))
    
    portfolioCounter = 0
    numberOfPortfolios = len(dict['portfolio'])
    
    establishSQLConnection()

    logger.info('Retrieving all Reversed Midas Trades...\n')
    midasReversedTrades = executeSQLQuery("SELECT * FROM OPENQUERY (MIDAS, 'select * from DEALSALLVW where RECI = ''R''')")

    for front_portfolio in dict['portfolio']:
        portfolioCounter = portfolioCounter + 1
        logger.info('*' * 20 + ' Portfolio %i of %i: %s '%(portfolioCounter, numberOfPortfolios, front_portfolio.Name()) + '*' * 20)
    
        midas_portfolio = front_portfolio.Name()[-3:]

        logger.info('Building Midas trade dictionary...\n')
        midasTradeDictionary = buildMidasTradeDictionary(midas_portfolio)

        frontArenaCFRTrades, frontArena4FrontTrades = getFrontArenaTrades(front_portfolio, midas_portfolio)
        
        logger.info('Building Front Arena trade dictionary...\n')
        frontArenaTradeDictionary = buildFrontArenaTradeDictionary(frontArenaCFRTrades)
        
        logger.info('Total number of Front Arena Trades after CFR selection: %i' %len(frontArenaTradeDictionary))
        
        logger.info('Formatting Front Arena 4Front Trade Numbers for Midas Selection...\n')
        frontArenaTradeNumberTuple = getFrontArenaTradeNumbers(frontArena4FrontTrades)
        
        logger.info('Retrieving 4Front street facing trades from Midas...\n')
        foreFrontTradesFromMidas = []
        foreFrontTradesShadowFromMidas = []
        if frontArena4FrontTrades:
            for i in range(0, len(frontArenaTradeNumberTuple), 100):
                chunk = frontArenaTradeNumberTuple[i:i+100]
                resultSet = executeSQLQuery("SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM FORTRESSPF WHERE FRONTDEALNO IN %s')" %chunk.__str__())
                for result in resultSet:
                    foreFrontTradesFromMidas.append(result)
        
            for trade in foreFrontTradesFromMidas:
                frontArenaTradeDictionary['%s_%i_0' %(ael.date_from_string(trade[5][:10], '%Y-%m-%d').to_string('%Y%m%d'), trade[1])] = acm.FTrade[trade[3]]

            logger.info('Total number of Front Arena Trades after 4Front Street Facing trade selection in Midas : %i' %len(frontArenaTradeDictionary))

            logger.info('Retrieving 4Front shadow trades from Midas...\n')
            for i in range(0, len(frontArenaTradeNumberTuple), 100):
                chunk = frontArenaTradeNumberTuple[i:i+100]
                resultSet = executeSQLQuery("SELECT * FROM OPENQUERY (MIDAS, 'SELECT sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO, MAX(p.DATETIMEADDED) AS DEALDATETIME FROM PFSHADOW4F sh LEFT JOIN FORTRESSPF p ON sh.MIDASDEALNO = p.MIDASDEALNO WHERE sh.FRONTINTERNALNO IN %s GROUP BY sh.MIDASDEALNO, sh.SHADOWDEALNO, sh.FRONTINTERNALNO')" %chunk.__str__())
                for result in resultSet:
                    foreFrontTradesShadowFromMidas.append(result)

            for trade in foreFrontTradesShadowFromMidas:
                frontArenaTradeDictionary['%s_%i_%s' %(ael.date_from_string(trade[3][:10], '%Y-%m-%d').to_string('%Y%m%d'), trade[0], int(trade[1]))] = acm.FTrade[int(trade[2])]

        logger.info('Total number of Front Arena Trades after 4Front Shadow trade selection in Midas: %i' %len(frontArenaTradeDictionary))

        logger.info('Number of trades in Front Arena that is missing in Midas based on integration key identification: %i' %(len(frontArenaCFRTrades) + len(frontArena4FrontTrades) - len(frontArenaTradeDictionary.keys())))
        logger.info('Identifying missing trades in Midas...\n')
        matchingFrontArenaTradesToMidasTrades(frontArena4FrontTrades, foreFrontTradesFromMidas, foreFrontTradesShadowFromMidas)

        logger.info('\n')
        logger.info('Reconciling Midas trades to Front Arena Trades...')
        frontArenaTradeDictionary, midasTradeDictionary = reconcileMidasToFrontArena(frontArenaTradeDictionary, midasTradeDictionary)
        
        logger.info('\n')
        logger.info('Reconciling Midas trades to Front Arena Trades 4Front Street facing trades...')
        frontArenaTradeDictionary, midasTradeDictionary = reconcileMidasToFrontArenaForeFrontStreetFacing(frontArenaTradeDictionary, midasTradeDictionary, foreFrontTradesFromMidas)
        
        logger.info('\n')
        logger.info('Reconciling Midas trades to Front Arena Trades 4Front Shadow trades...')
        frontArenaTradeDictionary, midasTradeDictionary = reconcileMidasToFrontArenaForeFrontShadow(frontArenaTradeDictionary, midasTradeDictionary, foreFrontTradesShadowFromMidas)

        logger.info('\n')
        logger.info('Removing trades that are Voided and Reversed in Front Arena and Midas respectively...')
        frontArenaTradeDictionary = removeVoidedAndReversedTrades(frontArenaTradeDictionary, midasReversedTrades)

        logger.info('-' * 20 + ' Summary of Front Arena breaks ' + '-' * 20)
        reportFrontArenaSummary(frontArenaTradeDictionary)
        
        logger.info('-' * 20 + ' Summary of Midas breaks ' + '-' * 20)
        reportMidasSummary(midasTradeDictionary)
    closeSQLConnection()
