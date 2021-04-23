"""
 FRiskMatrix ver 1.9.1 (compatible with PRIME 2.6.x and 2.7.x)

 This Module contains functions to create Risk Matrix Reports.
 Parameters are set up in an AEL variables window.
 Documentation on the parameters can be found in PRIME Help

 There are two ways of running the report:

 * Run the AEL script FRiskMatrix from the AEL Module Editor.
 
 * Start it from the AEL Task Manager.

"""
  

import ael2, ael
starString = '//*********************************************************************************************************//\n'
separatorString = '-------------------------------------------------------------------------------------------------------------\n'


class underlyingRiskObject:
    def __init__(this, obj):

        this.RiskObject = obj
        this.Instruments = []
        this.PriceObjects = []
        this.VolaObjects = []
        this.ZeroPositions = 0

# Is obj matrix or array?
def isMatrix(obj):
    if (str(type(obj[0])) == "<type 'FVariantArray'>"):
        return 1
    return 0

#  Transform matrix depending on how "reportMatrixValues" are set
def formatMatrixValues(matrixValueType, matrix, portVal):
    def formatValue(matrixValueType, cellVal, portVal):
        if not ((cellVal == None) or (not portVal)):
            if (matrixValueType == 'Changes'):
                cellVal -= portVal
            elif (matrixValueType == 'Percent'):
                cellVal = ((cellVal*1.0)/(portVal * 1.0) - 1.0) * 100 #times 1.0 to ensure that we have a float
        return cellVal

    if not matrix:
        return matrix
    elif isMatrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = formatValue(matrixValueType, matrix[i][j], portVal)
    else:
        for i in range(len(matrix)):
            matrix[i] = formatValue(matrixValueType, matrix[i], portVal)
    return matrix


def shiftFunc(shiftString):
    if (shiftString == 'Percent') or (shiftString =='BetaPercent'):
        return '*'
    if shiftString == 'Absolute':
        return '+'


def shiftValue(shiftString, shiftArray):
    modShiftArray = []
    for shiftVal in shiftArray:
        if (shiftString == 'Percent') or (shiftString =='BetaPercent'):
            modShiftArray.append(1+(shiftVal/100))
        else:
            modShiftArray.append(shiftVal)
    return modShiftArray


# The beta value of an instrument array
def getBetaArray(instrs, contextName):
    betaArray = []
    for instr in instrs:
        betaArray.append(server.GetCalculatedValueFromString(instr, contextName, 'betaValue', uniqueVal).Value())
    return betaArray

# Returns the shifted matrix
def riskMatrix(evaluator, priceShiftArray, priceShiftType, priceObjects, volaShiftArray, volaShiftType, volaObjects, matrixValueType, portVal, server, contextName):
    #x-shift
    priceTargets = evaluator.FindAdHoc('price', priceObjects).AsArray()
    if priceShiftType == 'BetaPercent':
        xShift = server.CreateShiftEvaluator(evaluator, priceTargets, shiftFunc(priceShiftType), shiftValue(priceShiftType, priceShiftArray), '*', getBetaArray(priceObjects, contextName))
    else:
        xShift = server.CreateShiftEvaluator(evaluator, priceTargets, shiftFunc(priceShiftType), shiftValue(priceShiftType, priceShiftArray))

    #If we don't have any volatilities in the tree, return x-Shift
    if not volaObjects:
        return formatMatrixValues(matrixValueType, xShift.Value(), portVal)

    #y-shift
    volaTargets = evaluator.FindAdHoc('volatilityInPerCent', volaObjects).AsArray()
    yShift = server.CreateShiftEvaluator(xShift, volaTargets, shiftFunc(volaShiftType), shiftValue(volaShiftType, volaShiftArray))
    return formatMatrixValues(matrixValueType, yShift.Value(), portVal)


# Returns array with Extreme Value and it's location
def getExtremeValue(matrix, priceShiftArray, volaShiftArray, objName, timeShift, portVal):
    if not matrix:
        return matrix
    elif isMatrix(matrix):
        resMat = [matrix[0][0], priceShiftArray[0], volaShiftArray[0], objName, timeShift, portVal]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if (matrix[i][j] < resMat[0]):
                    resMat = [matrix[i][j], priceShiftArray[j], volaShiftArray[i], objName, timeShift, portVal]
    else:
        resMat = [matrix[0], priceShiftArray[0], None, objName, timeShift, portVal]
        for i in range(len(matrix)):
            if (matrix[i] < resMat[0]):
                resMat = [matrix[i], priceShiftArray[i], None, objName, timeShift, portVal]

    return resMat
    

# Returns matrix with [Delta Gamma Theta Vega Rho] as columns
def greekRiskMatrix(evalGreeks, priceShiftArray, priceShiftType, priceObjects, volaShiftArray, volaShiftType, volaObjects, matrixValueType, timeShift, portVal, objName, server, contextName):
    resMatrix=[]
    for evaluator in evalGreeks:
        try:
            greekVal = evaluator.Value()
        except:
            resMatrix.append(None)
            break
        rm = riskMatrix(evaluator, priceShiftArray, priceShiftType, priceObjects, volaShiftArray, volaShiftType, volaObjects, matrixValueType, greekVal, server, contextName)
        resMatrix.append(rm)
    return [resMatrix, timeShift, portVal, objName]
    

# Expands the portfolio tree and returns it as two flat lists
def buildPortfolioTree(portfolio):
    listCompound = []
    listPhysical = []
    if (portfolio.Category() == 'CompoundPortfolio'):
        listCompound = [portfolio]
        subs = portfolio.SubPortfolios()
        for sub in subs:
            temp = buildPortfolioTree(sub)
            listCompound.extend(temp[0])
            listPhysical.extend(temp[1])
    else:
        listPhysical = [portfolio]
    return [listCompound, listPhysical]


# Which portfolios are to be printed?
def portfoliosToPrint(portfolio, choice):
    if (choice == 'Top'):
        return [portfolio]      
    portTree = buildPortfolioTree(portfolio)
    if (choice == 'All'):
        portTree[0].extend(portTree[1])
        return portTree[0]
    if (choice == 'Compound'):
        return portTree[0]
    if (choice == 'Physical'):
        return portTree[1]

        
# Prints the matrix (or array) to the file
def printToFile(file, matrix):
    def tryRound(val):
        try:
            ret = round(val, 2)
        except:
            ret = val
        return ret
        
    if not matrix:
        file.write('*** Not defined ***\n'.rjust(20))
    elif isMatrix(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                file.write((str(tryRound(matrix[i][j]))+';').rjust(20))
            file.write('\n')
    else:
        for i in range(len(matrix)):
            file.write((str(tryRound(matrix[i]))+';').rjust(20))
        file.write('\n')

# Returns an array containing the risk factors of an instrument
def riskFactors(instr):
    def underlyingIteration(instr, returnList):
        if instr.Category() == 'Combination':
            for instrMap in instr.InstrumentMaps():
                underlyingIteration(instrMap.Instrument(), returnList)
        elif instr.IsDerivative():
            underlyingIteration(instr.Underlying(), returnList)
        else:
            returnList.append(instr)

    returnList = []
    underlyingIteration(instr, returnList)
    return returnList

# Returns what sector an instrument belongs to
def belongsToSector(instr, sectorGroup):
    size = sectorGroup.SubGroups().Size()

    for s in range(size):
        sec = sectorGroup.SubGroups().At(s)
        if sec.Includes(instr):
            return sec   	
    return 0

# Creates a dictionary containing risk objects
def createUndDict(instrArray, contextName, priceObjects, volaObjects):
    undDict = {}

    for instr in instrArray:
        rfArray = riskFactors(instr)
        for rf in rfArray:
            rfName = rf.Name()
            if not undDict.has_key(rfName):
                newUndObj = underlyingRiskObject(rf)
                undDict[rfName] = newUndObj
            undDict[rfName].Instruments.append(instr)
            if instr in priceObjects:
                undDict[rfName].PriceObjects.append(instr)
            if instr in volaObjects:
                undDict[rfName].VolaObjects.append(instr)

    for instr in priceObjects:
    	if instr not in instrArray:
            rfArray = riskFactors(instr)
            for rf in rfArray:
                rfName = rf.Name()
                if not undDict.has_key(rfName):
                    break #Should not happen...
                undDict[rfName].PriceObjects.append(instr)

    for instr in volaObjects:
    	if instr not in instrArray:
            rfArray = riskFactors(instr)
            for rf in rfArray:
                rfName = rf.Name()
                if not undDict.has_key(rfName):
                    break #Should not happen...
                undDict[rfName].VolaObjects.append(instr)


    return undDict

# Sets a flag to be 1 on the risk object if they only contain zero positions
def findZeroPositions(undDict, port):
    for riskObj in undDict.values():
        foundNonZeroPos = 0
        
        for instr in riskObj.Instruments:
            if (instr.position(None, None, None, None, None, port, 1) != 0):
                foundNonZeroPos = 1
                break
            
        if not foundNonZeroPos:
            riskObj.ZeroPositions = 1

# Creates a dictionary with the key as the sector name and the value is an array containing both sector and risk objects connected.
def createSectorDict(undDict, sectorGroup):
    sectorDict = {}

    for riskObj in undDict.values():
        if not riskObj.ZeroPositions:
            sector = belongsToSector(riskObj.RiskObject, sectorGroup)
            if sector:
                sectorName = sector.Name()
            else:
                sectorName = 'No Sector'
            if sectorDict.has_key(sectorName):
                sectorDict[sectorName][1].append(riskObj)
            else:
                sectorDict[sectorName] = [sector, [riskObj]]

    return sectorDict


# The main function called with ADFL parameters set by user in Extension Manager
def createReports(portfolioList, priceShiftArray, priceShiftType, volaShiftArray, volaShiftType, \
                  timeShiftArray, printAllUnd, portTreeChoice, matrixValueType, printExtreme, \
                  printGreeks, afterExpiry, server, contextName, printSectors, filePath):

    import time
    uniqueVal = int(time.time())
    
    portPrintList = []
    for p in portfolioList:
        portPrintList.extend(portfoliosToPrint(p, portTreeChoice))
        
    if len(portPrintList) == 0:
        print 'No portfolio to print'
        return 0
    
    dateToday = time.strftime('%d%m%y', time.localtime(time.time()))

    if not filePath:
        filePath = "c:\\"
    if filePath and (filePath != '') and (filePath[len(filePath) - 1] != '\\'):
        filePath = filePath + '\\'
    fileName = filePath+'matrixReport_'+portPrintList[0].Name().replace('/', '')
    if len(portfolioList)>1:
        fileName = fileName+'_And_More.txt'
    else:
        fileName = fileName+'.txt'
    file = open(fileName, 'w')

    if afterExpiry == 'Change With Underlying':
        aftExpStr = ' Change with underlying after expiry.'
        aftExp = 1
    elif afterExpiry == 'Equity Equivalent':
        aftExpStr = ' Equity equivalent'
        aftExp = 2
    elif afterExpiry == 'Constant':
        aftExpStr = ' Constant Value.'
        aftExp = 3
    else:
        aftExpStr = ' No payoff after expiry.'
        aftExp = 0
        
    #Print Info
    file.write(starString)
    file.write('// PRIME Portfolio Risk Matrix Report'+'//\n'.rjust(73))
    file.write('// '+dateToday+'//\n'.rjust(101))
    file.write('//'+'//\n'.rjust(108))
    file.write('// Portfolio values:       '+str(matrixValueType).ljust(80)+'//\n')
    file.write('// Today prices and trades.'+'//\n'.rjust(83))
    file.write('//'+aftExpStr.ljust(105)+'//\n')
    file.write('//'+'//\n'.rjust(108))
    file.write('// Price Shift:            '+str(priceShiftArray).ljust(80)+'//\n')
    file.write('// Price Shift Type:       '+str(priceShiftType).ljust(80)+'//\n')
    file.write('// Vola Shift:             '+str(volaShiftArray).ljust(80)+'//\n')
    file.write('// Vola Shift Type:        '+str(volaShiftType).ljust(80)+'//\n')
    file.write('// Time Shift:             '+str(timeShiftArray).ljust(80)+'//\n')
    file.write('// Print Underlying:       '+str(printAllUnd).ljust(80)+'//\n')
#    file.write('// Print Sectors:          '+str(printSectors).ljust(80)+'//\n')
    file.write('// Portfolio Tree Choice:  '+str(portTreeChoice).ljust(80)+'//\n')
    file.write('//'+'//\n'.rjust(108))
    file.write('// Print Extreme Values:   '+str(printExtreme).ljust(80)+'//\n')
    file.write('// Print Greek Report:     '+str(printGreeks).ljust(80)+'//\n')
    file.write('//'+'//\n'.rjust(108))
    file.write(starString+'\n')

    extremeArray = []
    greekMatrixArray = []
    evalBuilder = server.GetEvaluatorBuilder(contextName, uniqueVal)
    aftExpEval= server.GetCalculatedValueFromString(0, contextName, 'whatAfterExpiry', uniqueVal)
    aftExpEval.Simulate(aftExp, 0)

    if printSectors:
        secName = server.GetCalculatedValue(0, contextName, 'poSectorGroups').Value()       
        selectString = 'name = "' + secName +'"'
        sectorGroup = server.GetClass('FPageGroup').Select01(selectString, '')

    for p in portPrintList:
        print 'Processing ', p.Name()

        portIAndT = p.InstrumentAndTrades()
        evaluator = server.GetCalculatedValueFromString(portIAndT, contextName, 'thVal', uniqueVal)
        evalGreeks = []
        if printGreeks:
            evalGreeks.append(server.GetCalculatedValueFromString(portIAndT, contextName, 'delta', uniqueVal))
            evalGreeks.append(server.GetCalculatedValueFromString(portIAndT, contextName, 'gamma', uniqueVal))
            evalGreeks.append(server.GetCalculatedValueFromString(portIAndT, contextName, 'theta', uniqueVal))
            evalGreeks.append(server.GetCalculatedValueFromString(portIAndT, contextName, 'vega', uniqueVal))
            evalGreeks.append(server.GetCalculatedValueFromString(portIAndT, contextName, 'rho', uniqueVal))
            
        file.write('Portfolio: '+p.Name()+'\n')
        pCurrName = server.GetCalculatedValue(p, contextName, 'portCurrName').Value()
        file.write('Matrix currency: '+pCurrName+'\n\n')

        # Get all the instruments returning a price (stocks, indices)
        priceObjects = evaluator.CollectKindOf('price', server.GetClass('FInstrument')).AsArray()
        
        # Get all the instruments returning a volatility (options)
        volaObjects = evaluator.CollectKindOf('volatilityInPerCent', server.GetClass('FInstrument')).AsArray()

        # Create dictionary with all underlying
        if printAllUnd or printSectors:
            instrArray = portIAndT.LiveInstruments()
            undDict = createUndDict(instrArray, contextName, priceObjects, volaObjects)
            findZeroPositions(undDict, p)
            if printSectors:
                sectorDict = createSectorDict(undDict, sectorGroup)

        # Get calcDateTime if it exist (in non-derivative portfolios it does not)
        timeTree = evaluator.CollectKindOf('calcDateTime', server.GetClass('FObject'))
        timeNodeAsArray = evaluator.FindAdHoc('calcDateTime', timeTree).AsArray()
        timeNode = 0
        
        if (len(timeNodeAsArray) > 0):
            timeNode = timeNodeAsArray[0]
            timeNow = timeNode.Value()
        
        for timeShift in timeShiftArray:
            if (timeNode and timeShift>0):
                newTime = timeNow+timeShift
                timeNode.Simulate(newTime, 0)
	    try:
            	portVal = evaluator.Value()
            except:
                errString = 'Portfolio '+p.Name()+' has no theoretical value! Aborting...'
                print errString
                file.write(errString+'\n')
                file.close()
                return 0
            file.write('Theoretical Value: '+str(round(portVal, 2))+'\n')
            
            if printAllUnd:
                for key in undDict.keys():
                    riskObj = undDict[key]
                    if not riskObj.ZeroPositions:
                        rm = riskMatrix(evaluator, priceShiftArray, priceShiftType, riskObj.PriceObjects, volaShiftArray, volaShiftType, riskObj.VolaObjects, matrixValueType, portVal, server, contextName)

                        if printExtreme: 
                            extremeArray.append(getExtremeValue(rm, priceShiftArray,  volaShiftArray, key, timeShift, portVal))
                        if printGreeks: 
                            greekMatrixArray.append(greekRiskMatrix(evalGreeks, priceShiftArray, priceShiftType, riskObj.PriceObjects, timeShift, portVal, key, server))

                        file.write('Time shift: '+str(timeShift)+'\n'+separatorString) 
                        file.write('Risk Object: '+key+'\n'+separatorString) 
                        printToFile(file, rm) 
                        file.write(separatorString+'\n') 
            
            rm = riskMatrix(evaluator, priceShiftArray, priceShiftType, priceObjects, volaShiftArray, volaShiftType, volaObjects, matrixValueType, portVal, server, contextName)
            if printExtreme:
                extremeArray.append(getExtremeValue(rm, priceShiftArray,  volaShiftArray, p.Name(), timeShift, portVal))
            if printGreeks:
                greekMatrixArray.append(greekRiskMatrix(evalGreeks, priceShiftArray, priceShiftType, priceObjects, volaShiftArray, volaShiftType, volaObjects, matrixValueType, timeShift, portVal, p.Name(), server, contextName))
            file.write('Time shift: '+str(timeShift)+'\n'+separatorString)
            file.write('Risk Object: '+p.Name()+'\n'+separatorString)
            printToFile(file, rm)
            file.write(separatorString+'\n')
            if (timeNode and timeShift>0):
                timeNode.RemoveSimulation()             
        evalBuilder.Reset()

    if printExtreme:
        file.write('\n\n'+starString)
        file.write('//'+'//\n'.rjust(108))
        file.write('// PRIME Portfolio Extreme Value Report'+'//\n'.rjust(71))
        file.write('//'+'//\n'.rjust(108))
        file.write(starString+'\n')
        for extreme in extremeArray:
            if not extreme:
                extreme = ['None', 'None', 'None', 'None', 'None', 0]
            file.write('Time Shift: '+str(extreme[4])+'\n'+separatorString)
            file.write('Risk Object'.ljust(20)+'Theoretical Value'.rjust(20)+'Highest Risk'.rjust(20)+'Price'.rjust(20)+'Volatility'.rjust(20)+'\n')
            file.write(separatorString)
            file.write(extreme[3].ljust(20)+str(round(extreme[5], 2)).rjust(20)+str(extreme[0]).rjust(20)+str(extreme[1]).rjust(20)+str(extreme[2]).rjust(20)+'\n')
            file.write(separatorString+'\n')        

    if printGreeks:
        file.write('\n\n'+starString)
        file.write('//'+'//\n'.rjust(108))
        file.write('// PRIME Portfolio Greek Value Report'+'//\n'.rjust(73))
        file.write('//'+'//\n'.rjust(108))
        file.write(starString+'\n')
        for greekArray in greekMatrixArray:
            file.write('Time Shift: '+str(greekArray[1])+'\n'+separatorString+'Risk Object: '+greekArray[3]+'\n')
            matrix = greekArray[0]
            file.write(separatorString)
            file.write('Delta:\n')
            printToFile(file, matrix[0])
            file.write('\n\nGamma:\n')
            printToFile(file, matrix[1])
            file.write('\n\nTheta:\n')
            printToFile(file, matrix[2])
            file.write('\n\nVega:\n')
            printToFile(file, matrix[3])
            file.write('\n\nRho:\n')
            printToFile(file, matrix[4])
            file.write(separatorString+'\n')
            

    aftExpEval.RemoveSimulation()    
    file.close()
    print 'Report written to file: ', fileName
            

priceShiftTypes = ['Absolute', 'Percent']
volaShiftTypes = ['Absolute', 'Percent']
matrixValType = ['Changes', 'Absolute', 'Percent']
afterExpType = ['Change With Underlying', 'Equity Equivalent', 'Constant']
treeChoiceType = ['All', 'Compound', 'Physical', 'Top']
trueFalse = ['True', 'False']

def pf():
    """List of all portfolios"""
    port = ael.Portfolio
    pf = []
    for p in port:
        pf.append(p.prfid)
    return pf

def tf():
    """List of all trade filters"""
    filt = ael.TradeFilter
    tf = []
    for t in filt:
        tf.append(t.fltid)
    return tf

def contextNames():
    retList = []
    contextClass = ael2.getServerObject().GetClass('FExtensionContext')
    contexts = contextClass.Select('')
    for context in contexts:
        retList.append(context.Name())
    return retList

pfs = pf()
tfs = tf()
contexts = contextNames()

ael_variables = [('priceShifts', 'Price Shifts', 'float', None, None, 1, 1), 
                ('priceShiftType', 'Price Shift Type', 'string', priceShiftTypes, 'Percent'),
                ('volaShifts', 'Volatility Shifts', 'float', None, None, 1, 1), 
                ('volaShiftType', 'Volatility Shift Type', 'string', volaShiftTypes, 'Absolute'),
                ('timeShifts', 'Time Shifts', 'float', None, None, 1, 1),
                ('printAllUnd', 'Print All Underlyings', 'string', trueFalse, 'False'),
                ('printExtreme', 'Print Extreme Values', 'string', trueFalse, 'False'),
                ('printGreeks', 'Print Greek Report', 'string', trueFalse, 'False'),
                ('matrixValueType', 'Matrix Value Type', 'string', matrixValType, 'Changes', 1),
                ('afterExpiry', 'After Expiry', 'string', afterExpType, 'Change With Underlying', 1),
                ('portTreeChoice', 'Portfolio Tree Choice', 'string', treeChoiceType, 'Top', 1),
                ('tf', 'Trade Filters', 'string', tfs, None, 0, 1),
                ('pf', 'Portfolios', 'string', pfs, None, 0, 1),#0=ej obligatorisk, 1=kan fylla i fler portf ljer
                ('contextName', 'Context', 'string', contexts, 'Standard'),
                ('filePath', 'File Path', 'string', None, 'c:\\', 1)] 


#('printSectors', 'Print All Sectors', 'string', trueFalse, 'False'),

def convertToInt(input):
    if (input == 'True'):
        return 1
    else:
        return 0 

def ael_main(dict):
    server = ael2.getServerObject()
    priceShiftArray = dict.get('priceShifts')
    priceShiftType = dict.get('priceShiftType') 
    volaShiftArray = dict.get('volaShifts')
    volaShiftType = dict.get('volaShiftType')
    timeShiftArray = dict.get('timeShifts')
    printAllUndString = dict.get('printAllUnd')
    printAllUnd = convertToInt(printAllUndString)
    printExtremeString = dict.get('printExtreme')
    printExtreme = convertToInt(printExtremeString)
    printGreeksString = dict.get('printGreeks')
    printGreeks = convertToInt(printGreeksString)
    matrixValueType = dict.get('matrixValueType')
    afterExpiry = dict.get('afterExpiry')
    portTreeChoice = dict.get('portTreeChoice')
    portfolioNames = dict.get('pf') 
    TradeFilterNames = dict.get('tf')
    contextName = dict.get('contextName')
    #printSectorsString = dict.get('printSectors')
    #printSectors = convertToInt(printSectorsString)
    filePath = dict.get('filePath')
    printSectors = 0
    
        
    portfolioList = []
    
    for portName in portfolioNames:
        selectString = 'name = "'+portName+'"'
        port = server.GetClass('FPhysicalPortfolio').Select01(selectString, '')
        if not port:
            port = server.GetClass('FCompoundPortfolio').Select01(selectString, '')
        portfolioList.append(port)

    for portName in TradeFilterNames:
        selectString = 'name = "'+portName+'"'
        portfolioList.append(server.GetClass('FTradeSelection').Select01(selectString, ''))

    createReports(portfolioList, priceShiftArray, priceShiftType, volaShiftArray, volaShiftType, \
                  timeShiftArray, printAllUnd, portTreeChoice, matrixValueType, printExtreme, \
                  printGreeks, afterExpiry, server, contextName, printSectors, filePath)


