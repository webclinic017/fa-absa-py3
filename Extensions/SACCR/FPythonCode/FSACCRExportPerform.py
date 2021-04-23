""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/FSACCRExportPerform.py"
"""----------------------------------------------------------------------------
MODULE
    FSACCRExportPerform - Module which exports the SACCR Deals XML file and the 
    Market Data file on the instrument.

DESCRIPTION
----------------------------------------------------------------------------"""

import platform
if platform.system() == 'Windows':
    import os
    import acm
    from FBDPCurrentContext import Summary
    from FBDPCurrentContext import Logme

    def perform(execParam):
        Logme()('SACCR Export 4.27.1')
        r = _SACCRExport()
        r.perform(execParam)
        Summary().log(execParam)
        Logme()(None, 'FINISH')
        del r

    def createCreditBalanceQuery(insList):
        q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        op = q.AddOpNode('OR')
        for ins in insList:
            if not ins.IsKindOf(acm.FCreditBalance):
                ignMsg = ('Ignore non Credit Balance instrument "{0}" of type '
                        '"{1}"'.format(ins.Name(), ins.InsType()))
                Logme()(ignMsg, 'WARNING')
                Summary().ignore(ins, 'ExportAAP', ignMsg, ins.Name())
            else:
                op.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())
        return q

    class _SACCRExport(object):

        def __init__(self):
            self._strPackedDateToday = acm.Time.DateToday().replace('-', '')

        def _acquireInstruments(self, execParam):
            self.Testmode = execParam['Testmode']
            if 'Instruments' in execParam and execParam['Instruments']:
                return execParam['Instruments']
            elif 'InstrumentsQuery' in execParam and execParam['InstrumentsQuery']:
                settmp = acm.FIdentitySet()
                objs = execParam['InstrumentsQuery']
                for obj in objs:
                   if (obj.IsKindOf(acm.FStoredASQLQuery) and
                            obj.SubType() == 'FInstrument'):
                        settmp.AddAll(obj.Query().Select())
                return settmp
            errMsg = ('Instruments must be selected.')
            raise Exception(errMsg)

        def _acquireRunParameter(self, execParam):
            insList = self._acquireInstruments(execParam)
            dealsExportDirPath = self._acquireRunParameterExportPath(execParam, 'DealsExportPath', 'AppendDateToDealsXMLDir')
            marketDataExportDirPath = self._acquireRunParameterExportPath(execParam, 'MarketDataExportPath', 'AppendDateToMarketDataXmlDir')
            ratefixingsExportDirPath = self._acquireRunParameterExportPath(execParam, 'RateFixingsExportPath', 'AppendDateToMarketDataXmlDir')
            distributedCalculations = execParam['distributedCalculations']
            return insList, dealsExportDirPath, marketDataExportDirPath, ratefixingsExportDirPath, distributedCalculations

        def _acquireRunParameterExportPath(self, execParam, dealsOrMarketData, createDirWithDate):
            exportPath = execParam[dealsOrMarketData]
            if not os.path.exists(exportPath):
                Logme()('The given export path "{0}" does not '
                        'exist.'.format(exportPath), 'ERROR')
                return None
            if not os.path.isdir(exportPath):
                Logme()('The given export path "{0}" is not '
                        'a directory.'.format(exportPath), 'ERROR')
                return None
            if not os.access(exportPath, os.W_OK):
                Logme()('The given export path "{0}" is not '
                        'writable.'.format(exportPath), 'ERROR')
                return None
            absExportPath = os.path.abspath(exportPath)
            if execParam[createDirWithDate]:
                absExportPath = os.path.join(absExportPath, acm.Time().DateToday())
                if not os.path.exists(absExportPath):
                    os.makedirs(absExportPath)
            return absExportPath
    
        def _writeToFile(self, filePath, content):
            errMsg = None
            if not self.Testmode:
                with open(filePath, 'w') as f:
                    f.write(content)
            return errMsg

        def _process(self, insList, dealsExportDirPath, marketDataExportDirPath, ratefixingsExportDirPath, distributedCalculations):
            Logme()('Exporting deals files to directory "{0}".'.format(dealsExportDirPath), 'DEBUG')
            Logme()('Exporting market data files to directory "{0}".'.format(marketDataExportDirPath), 'DEBUG')
            Logme()('Exporting rate fixings files to directory "{0}".'.format(ratefixingsExportDirPath), 'DEBUG')

            calcSpaceMngr = _PortfolioSheetCalcSpaceManager(distributedCalculations)
            insDealsXMLDict = calcSpaceMngr._getSACCRInputXMLs(insList, 'SACCR DEAL XML')
            for insName, inputXML in insDealsXMLDict.iteritems():
                aapFileName = makeValidFileName('{0}_{1}.aap'.format('Deals', insName, self._strPackedDateToday))
                aapFileFullPath = os.path.join(dealsExportDirPath, aapFileName)
                Logme()('    Exporting "{0}"...'.format(aapFileFullPath), 'DEBUG')
                self._writeToFile(filePath=aapFileFullPath, content=inputXML)
                ins = acm.FInstrument[insName]
                Summary().ok(ins, 'ExportedAAP', ins.Oid())

            insMarketDataXMLDict = calcSpaceMngr._getSACCRInputXMLs(insList, 'SACCR MarketData XML')
            for insName, inputXML in insMarketDataXMLDict.iteritems():
                datFileName = makeValidFileName('{0}_{1}.dat'.format('MarketData', insName, self._strPackedDateToday))
                datFileFullPath = os.path.join(marketDataExportDirPath, datFileName)
                Logme()('    Exporting "{0}"...'.format(datFileFullPath), 'DEBUG')
                self._writeToFile(filePath=datFileFullPath, content=inputXML)
                ins = acm.FInstrument[insName]
                Summary().ok(ins, 'ExportedMarketData', ins.Oid())
            Logme()('Done Exporting', 'DEBUG')
    
            insRateFixingDict = calcSpaceMngr._getSACCRInputXMLs(insList, 'SACCR RateFixing Str')
            for insName, inputXML in insRateFixingDict.iteritems():
                arfFileName = makeValidFileName('{0}_{1}.arf'.format('RateFixings', insName, self._strPackedDateToday))
                arfFileFullPath = os.path.join(ratefixingsExportDirPath, arfFileName)
                Logme()('    Exporting "{0}"...'.format(arfFileFullPath), 'DEBUG')
                self._writeToFile(filePath=arfFileFullPath, content=inputXML)
                ins = acm.FInstrument[insName]
                Summary().ok(ins, 'ExportedRateFixings', ins.Oid())
            Logme()('Done Exporting', 'DEBUG')
    
        def perform(self, execParam):
            Logme()('Acquiring run parameters...', 'INFO')
            insList, dealsExportDirPath, marketDataExportDirPath, ratefixingsExportDirPath, distributedCalculations = self._acquireRunParameter(execParam)
            if not dealsExportDirPath or not marketDataExportDirPath or not ratefixingsExportDirPath:
                return
            self._process(insList, dealsExportDirPath, marketDataExportDirPath, ratefixingsExportDirPath, distributedCalculations)
            return


    # #############################################################################
    # Portfolio Sheet Calculation Space Management
    # #############################################################################
    
    
    _CREDIT_ENTITY_GROUPER_NAME = 'Credit Entity'
    
    
    class _PortfolioSheetCalcSpaceManager(object):
    
        SHEET_TYPE = 'FPortfolioSheet'
    
        REFRESH_THRESHOLD_COUNT = 1000
    
        def __init__(self, distributedCalculations):

            self.__count = 0
            self.__calcSpace = self.__initCalcSpace(distributedCalculations)
            self._creditEntityGrouper = self._getBuiltInCreditEntityGrouper()
    
        def _getBuiltInCreditEntityGrouper(self):
    
            allBuiltInPortfolioGroupers = acm.Risk.GetAllBuiltInPortfolioGroupers()
            creditEntityGrouper = allBuiltInPortfolioGroupers.At(
                    _CREDIT_ENTITY_GROUPER_NAME)
            return creditEntityGrouper
    
        def __initCalcSpace(self, distributedCalculations):

            spaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            calcSpace = spaceCollection.GetSpace(
                            acm.FPortfolioSheet,
                            acm.GetDefaultContext().Name(),
                            None, 
                            distributedCalculations)

            return calcSpace

        def _getSACCRInputXMLs(self, insList, collumn):
            insInputXMLDict = {}
            node = self.__calcSpace.InsertItem(createCreditBalanceQuery(insList))
            self.__calcSpace.Refresh()
            nodeIterator = node.Iterator()
            if not nodeIterator.HasChildren():
                insNames = ''
                for ins in insList:
                    insNames = insNames + ins.Name() + ','
                raise Exception('Unable to obtain SACCR XML of these '
                            'instruments "{0}"'.format(insNames))

            it = nodeIterator.FirstChild()
            calculations = []
            while it:
                insName = it.Tree().Item().StringKey()
                calc = self.__calcSpace.CreateCalculation(it.Tree(), collumn)
                calculations.append((insName, calc))
                it = it.NextSibling()
            self.__calcSpace.Refresh()
            for insName, calc in calculations:
                insInputXMLDict[insName] = calc.FormattedValue()

            return insInputXMLDict


        def __checkCalcSpaceUsage(self):
    
            self.__count += 1
            if self.__count % self.REFRESH_THRESHOLD_COUNT:
                return
            self.__calcSpace.Clear()
            acm.Calculations().ResetEvaluatorBuilders()
            self.__calcSpace = self.__initCalcSpace()
            acm.Memory().GcWorldStoppedCollect()
    
        def __checkCalculatedValue(self, value):
    
            if value.IsKindOf(acm.FException):
                Logme()(str(value), 'WARNING')
    
    
    # #############################################################################
    # Filename manipulation
    # #############################################################################
    
    
    VALID_FILE_NAME_CHAR_WHITESPACE = ' '
    VALID_FILE_NAME_CHAR_UNDERSCORE = '_'
    VALID_FILE_NAME_CHAR_DASH = '-'
    VALID_FILE_NAME_CHAR_DOT = '.'
    
    
    def _isValidFileNameChar(char):
    
        isValid = (str.isupper(char) or str.islower(char) or str.isdigit(char)
                or char in (VALID_FILE_NAME_CHAR_WHITESPACE,
                        VALID_FILE_NAME_CHAR_UNDERSCORE,
                        VALID_FILE_NAME_CHAR_DASH,
                        VALID_FILE_NAME_CHAR_DOT))
        return isValid
    
    
    def makeValidFileName(origName):
    
        if not isinstance(origName, str):
            raise ValueError('The given original name must be a string, but "{0}" '
                    'of type "{1}" is given.'.format(origName, type(origName)))
        validFileNameBytes = []
        for char in origName:
            if _isValidFileNameChar(char):
                validFileNameBytes.append(char)
            else:
                twoLetterHexNum = hex(ord(char)).upper().replace('X', '')[-2:]
                validFileNameBytes.append('%{0}'.format(twoLetterHexNum))
        return ''.join(validFileNameBytes)
