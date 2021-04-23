""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FPFEExportPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FPFEExport - Module which exports the PFE XML column and the output AAJ file on the instrument.

DESCRIPTION
----------------------------------------------------------------------------"""

import platform
if platform.system() == 'Windows':
    import os
    import re
    import acm
    import FBDPPerform
    import FBDPWorld
    import AAImport
    from xml.dom.minidom import parseString
    import SunGard.Adaptiv.Analytics.Framework

    try:
        import clr
    except:
        print("Could not import module clr")
    clr.AddReference("System")
    clr.AddReference("System.Xml")
    try:
        import System.IO
        import System.Xml
    except:
        print("Could not import System.IO or System.Xml")

    BUFFER_SIZE_FOR_OUTPUT_XML = 50*1024*1024

    def perform(world, execParam):
        r = _PFEExport(world)
        r.perform(execParam)
        r.end()
        del r


    def updateInputXml(input_xml, percentiles):
        doc = parseString(input_xml)
        calc = doc.getElementsByTagName('Calc')
        calculation = calc[0].getElementsByTagName('Calculation')        
        textData = calculation.item(0).childNodes[0].data
        p = re.compile(r'Percentiles=[0-9]*\.?[0-9]', re.U)
        textData = p.sub(u"Percentiles=" + unicode(percentiles, "ascii"), textData)
        calculation.item(0).childNodes[0].replaceWholeText(textData)
        return doc.toxml()


    class _PFEExport(FBDPPerform.FBDPPerform):

        def __init__(self, world):

            FBDPPerform.FBDPPerform.__init__(self, world)
            self._strPackedDateToday = acm.Time.DateToday().replace('-', '')
    
        def _validateMode(self):
    
            if acm.ArchivedMode():
                errMsg = 'This script must not be run in the Archived mode.'
                self._logError(errMsg)
            return

        def _acquireInstruments(self, execParam):
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
            """
            The ACQUIRING RUN PARAMETER phase of the perform()
            """
            insList = self._acquireInstruments(execParam)
            generateInputData = execParam['GenerateInputData']
            inputExportDirPath = ''
            if generateInputData:
                inputExportDirPath = self._acquireRunParameterExportPath(execParam, 'InputExportPath', 'AppendDateToInputDataDir')
            generateOutputData = execParam['GenerateOutputData']
            outputExportDirPath = ''
            if generateOutputData:
                outputExportDirPath = self._acquireRunParameterExportPath(execParam, 'OutputExportPath', 'AppendDateToOutputDataDir')
            profileData = [execParam['GenerateCashflowProfile'], execParam['CashflowProfileCurrencyOptions'], execParam['GenerateCollateralProfile'], 'No', execParam['CollateralProfilePartitionByDeal']]
            includeCollateralInCalculations = execParam['IncludeCollateralInCalculations']
            percentiles = execParam['Percentiles']
            distributedCalculations = execParam['distributedCalculations']

            return insList, inputExportDirPath, generateInputData, outputExportDirPath, generateOutputData, profileData, includeCollateralInCalculations, percentiles, distributedCalculations
    
        def _acquireRunParameterExportPath(self, execParam, inputOrOutput, createDirWithDate):
    
            exportPath = execParam[inputOrOutput]
            if not os.path.exists(exportPath):
                self._logError('The given export path "{0}" does not '
                        'exist.'.format(exportPath))
                return None
            if not os.path.isdir(exportPath):
                self._logError('The given export path "{0}" is not '
                        'a directory.'.format(exportPath))
                return None
            if not os.access(exportPath, os.W_OK):
                self._logError('The given export path "{0}" is not '
                        'writable.'.format(exportPath))
                return None
            absExportPath = os.path.abspath(exportPath)
            if execParam[createDirWithDate]:
                absExportPath = os.path.join(absExportPath, acm.Time().DateToday())
                if not os.path.exists(absExportPath):
                    os.makedirs(absExportPath)
            return absExportPath
    
        def _writeToFile(self, filePath, content):
    
            errMsg = None
            if not self._isInTestMode():
                with open(filePath, 'w') as f:
                    f.write(content)
            return errMsg

        def _process(self, insList, inputExportDirPath, generateInputData, outputExportDirPath, generateOutputData, profileData, includeCollateralInCalculations, percentiles, distributedCalculations):
            
            if generateInputData:
                self._logDebug('Exporting AAJ input files to directory "{0}".'.format(inputExportDirPath))
            if generateOutputData:
                self._logDebug('Exporting AAJ output files to directory "{0}".'.format(outputExportDirPath))
            
            calcSpaceMngr = _PortfolioSheetCalcSpaceManager(self._getWorldRef(), distributedCalculations)
            insInputXMLDict = calcSpaceMngr._getPFEInputXMLs(insList, profileData, includeCollateralInCalculations)
            for insName, inputXML in insInputXMLDict.iteritems():
                if generateInputData:
                    aajFileName = makeValidFileName('{0}_{1}.aaj'.format('InputAAJ', insName, self._strPackedDateToday))
                    aajFileFullPath = os.path.join(inputExportDirPath, aajFileName)
                    self._logDebug('    Exporting "{0}"...'.format(aajFileFullPath))
                
                if generateOutputData:
                    aajOutputFileName = makeValidFileName('{0}_{1}.aaj'.format('OutputAAJ', insName, self._strPackedDateToday))
                    aajOutputFileFullPath = os.path.join(outputExportDirPath, aajOutputFileName)
                    self._logDebug('    Exporting "{0}"...'.format(aajOutputFileFullPath))
                
                errMsg = None
                try:
                    if percentiles:
                        if ',' in percentiles:
                            percentiles = '[' + percentiles + ']'
                        inputXML = updateInputXml(inputXML, percentiles)

                    if generateInputData:
                        self._writeToFile(filePath=aajFileFullPath, content=inputXML)
                    if generateOutputData:
                        self._getPFEOutputXML(inputXML, aajOutputFileFullPath)
                except Exception as e:
                    errMsg = str(e)
                ins = acm.FInstrument[insName]
                if errMsg:
                    self._logError(errMsg)
                    self._summaryAddFail('Instrument', ins.Oid(), 'ExportedAAJ',
                            reasons=[errMsg])
                else:
                    self._summaryAddOk('Instrument', ins.Oid(), 'ExportedAAJ')
            self._logDebug('Done Exporting')

        def _getPFEOutputXML(self, inputXML, aajOutputFileFullPath):
            try:
                settings = System.Xml.XmlWriterSettings(False)
                fStream = System.IO.File.Create(aajOutputFileFullPath, BUFFER_SIZE_FOR_OUTPUT_XML)
                writer = System.Xml.XmlWriter.Create(fStream, settings)
                funcSignature = AAImport.ea.Process.__doc__
                newSignature = "Void Process(SunGard.Adaptiv.Analytics.Framework.Request, Int32, Boolean, System.Xml.XmlWriter)"
                if newSignature in funcSignature:
                    request = SunGard.Adaptiv.Analytics.Framework.Request()
                    request.set_Text(inputXML)
                    AAImport.ea.Process(request, 1, True, writer)
                else:
                    AAImport.ea.Process(inputXML, 1, True, writer)
            except Exception as e:
                self._logError(str(e))
            finally:
                writer.Close()
                fStream.Dispose()
    
        def perform(self, execParam):
    
            # VALIDATE phase
            self._logInfo('Validating environment and parameters...')
            self._validateMode()
            if self._hasAnyErrorMessage():
                self._listTopWarningMessages()
                self._listTopErrorMessages()
                return
            # ACQUIRING PARAMETER phase
            self._logInfo('Acquiring run parameters...')
            insList, inputExportDirPath, generateInputData, outputExportDirPath, generateOutputData, profileData, includeCollateralInCalculations, percentiles, distributedCalculations = self._acquireRunParameter(execParam)
            if self._hasAnyErrorMessage():
                self._listTopWarningMessages()
                self._listTopErrorMessages()
                return
            # INSPECTION phase (Nil)
            # PROCESS phase
            self._process(insList, inputExportDirPath, generateInputData, outputExportDirPath, generateOutputData, profileData, includeCollateralInCalculations, percentiles, distributedCalculations)
            # Finalise
            self._listTopWarningMessages()
            self._listTopErrorMessages()
            return
    
        def end(self):
    
            FBDPPerform.FBDPPerform._end(self)
    
    
    # #############################################################################
    # Portfolio Sheet Calculation Space Management
    # #############################################################################
    
    
    _CREDIT_ENTITY_GROUPER_NAME = 'Credit Entity'
    
    
    class _PortfolioSheetCalcSpaceManager(FBDPWorld.WorldInterface):
    
        SHEET_TYPE = 'FPortfolioSheet'
    
        REFRESH_THRESHOLD_COUNT = 1000
    
        def __init__(self, world, distributedCalculations):
    
            FBDPWorld.WorldInterface.__init__(self, world)
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

        def _getPFEInputXMLs(self, insList, profileData, includeCollateralInCalculations):
            insInputXMLDict = {}
            node = self.__calcSpace.InsertItem(self.__createCreditBalanceQuery(insList))
            self.__calcSpace.Refresh()
            nodeIterator = node.Iterator()
            if not nodeIterator.HasChildren():
                insNames = ''
                for ins in insList:
                    insNames = insNames + ins.Name() + ','
                raise Exception('Unable to obtain PFE XML of these '
                            'instruments "{0}"'.format(insNames))
            try:
                self.__calcSpace.SimulateGlobalValue('PFE Profile Setting Values', profileData)
            except Exception as e:
                errMsg = ('Error while simulating profile parameters in column "PFE Profile Setting Values".')
                raise Exception(errMsg)
            try:
                self.__calcSpace.SimulateGlobalValue('CVA and PFE Include Collateral', includeCollateralInCalculations)
            except Exception as e:
                errMsg = ('Error while simulating profile parameters in column "CVA and PFE Include Collateral".')
                raise Exception(errMsg)

            it = nodeIterator.FirstChild()
            calculations = []
            while it:
                insName = it.Tree().Item().StringKey()
                calc = self.__calcSpace.CreateCalculation(it.Tree(), 'PFE XML')
                calculations.append((insName, calc))
                it = it.NextSibling()
            self.__calcSpace.Refresh()
            for insName, calc in calculations:
                insInputXMLDict[insName] = calc.FormattedValue()

            self.__calcSpace.RemoveGlobalSimulation('PFE Profile Setting Values')
            self.__calcSpace.RemoveGlobalSimulation('CVA and PFE Include Collateral')
            return insInputXMLDict

        def __createCreditBalanceQuery(self, insList):
            q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
            op = q.AddOpNode('OR')
            for ins in insList:
                if not ins.IsKindOf(acm.FCreditBalance):
            	    ignMsg = ('Ignore non Credit Balance instrument "{0}" of type '
            		        '"{1}"'.format(ins.Name(), ins.InsType()))
            	    self._logWarning(ignMsg)
            	    self._summaryAddIgnore('Instrument', ins.Oid(), 'ExportAAJ',
                        reasons=[ignMsg])
            	    print(ignMsg)
                else:
            	    op.AddAttrNode('Instrument.Name', 'EQUAL', ins.Name())
            return q

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
                self._logWarning(str(value))
    
    
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
