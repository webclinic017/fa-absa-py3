""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationSpecification.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationSpecification

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import FReconciliationIdentification
import FAssetManagementUtils
import FReconciliationReaderFactory
import FBusinessDataImportHook

logger = FAssetManagementUtils.GetLogger()


def GetReconciliationSpecificationNames(isUpload=False):
    modules = acm.GetDefaultContext().GetAllExtensions('FParameters', 'FObject', True, True)
    names = list()
    for m in modules:
        if m.GetString('Identification Rules'):
            if isUpload and m.GetString('Upload') == 'True':
                names.append(m.Name())
            elif not isUpload and m.GetString('Upload') != 'True':
                names.append(m.Name())
    return names
    
def GetReconciliationSpecification(reconciliationItem, upload = False, relaxValidation = False):
    ''' Return a reconciliation specification '''
    reconciliationName = reconciliationItem.ReconciliationDocument().ReconciliationName()
    try:
        return FReconciliationSpecification(reconciliationName, upload, relaxValidation)
    except ValueError as e:
        logger.error('Failed to load %s specification "%s" for reconciliation item %d: %s',
                      'reconciliation' if upload else 'data upload', reconciliationName, reconciliationItem.Oid(), e)
        raise
    return None
    

class FReconciliationSpecification(object):
    """Class defining all parameters necessary for processing a reconciliation document."""

    _FPARAMETER_ATTRIBUTES = (
        # FParameter attribute, class attribute, mandatory field
        ('Object Type', '_objectType', True),
        ('Sub Type', '_subType', False),
        ('FX Recon', '_isFxReconciliation', False),        
        ('File Format', '_readerType', False),
        ('State Chart', '_stateChartName', True),
        ('Store Reconciled Items', '_storeReconciledItems', False),
        ('External Attribute Map', '_externalAttributeMapName', True),
        ('Identification Rules', '_identificationRules', True),
        ('Compared Values Map', '_valueMappingName', True),
        ('External Data Type Map', '_dataTypeMappingName', True),
        ('Sheet Template', '_sheetTemplateName', False),
        ('Business Process Sheet Template', '_businessProcessSheetTemplateName', False),
        ('Universe Queries', '_universeQueries', False),
        ('Parser Hook', '_parserFunc', False),
        ('External Values Hook', '_externalValuesFunc', False),
        ('Identification Values Hook', '_identificationValuesFunc', False),
        ('Identify Item Hook', '_identifyItemFunc', False),
        ('Pre Commit Hook', '_precommitFunc', False),
        ('Post Processing Hook', '_postprocessingFunc', False),
        ('Comparison Type', '_comparisonType', False),
        ('Upload', '_upload', False),
        ('Max Nbr Of Items Missing in Document', '_maxUniverseQueries', False),
        ('Max Nbr Of Unclosed Recon Items', '_maxNbrOfUnclosedReconItems', False),
        ('Create column definitions on save', '_createColumnDefinitions', False),
    )

    def __init__(self, name, upload = False, relaxValidation = False, onLoad = True):
        ''' 
            Create a recon spec instance from the reconciliation document name.
            Observe that this class is used for both upload and reconciliation.
            Moreover, an optional input argument relaxes validation procedures,
            e.g. when full validation is not needed (outside of recon processing).
        '''
        assert name, 'No unique name identifying this reconciliation was specified!'
        # Set default values
        self._name = name
        self._readerType = None
        self._parserFunc = None
        self._externalValuesFunc = None
        self._objectType = None
        self._subType = None
        self._isFxReconciliation = False        
        self._stateChartName = 'Reconciliation' if not upload else 'Data Upload'
        self._storeReconciledItems = False
        self._externalAttributeMapName = None
        self._identificationRules = None
        self._valueMappingName = None
        self._dataTypeMappingName = None
        self._sheetTemplateName = None
        self._businessProcessSheetTemplateName = None
        self._universeQueries = list()
        self._identificationValuesFunc = None
        self._identifyItemFunc = None
        self._precommitFunc = None
        self._postprocessingFunc = None
        self._comparisonType = None
        self._upload = upload
        self._maxUniverseQueries = None
        self._maxNbrOfUnclosedReconItems = None
        self._createColumnDefinitions = None
        try:
            if self._ReconSpecInContext():
                # Load values from specification
                self._LoadFromExtension(relaxValidation, onLoad)
                if relaxValidation is False:                
                    # Validation relaxation is enforced for backwards compatability reasons
                    self._Validate()
        except Exception:
            logger.error('Invalid Reconciliation Specification "%s"' % self._name)
            raise

    def Name(self):
        """The unique name identifying this reconciliation."""
        return self._name

    def ReaderType(self):
        """The type of reader"""
        return self._readerType

    def ParseDocument(self, fp):
        """Parse a reconciliation document using the specified file parser generator
        function. Given a file object, this function must yield reconciliation item attributes
        as keyValuePairs dicts."""
        return self._parserFunc(fp)

    def HasExternalValuesHook(self):
        """Return True is this specification has an external values hook defined."""
        return bool(self._externalValuesFunc)

    def GetExternalValues(self, docDict):
        """Perform custom transformations of the dictionary produced by the parser.
        Return a transformed dictionary, or the original in case no external values hook has been defined."""
        if self._externalValuesFunc:
            return self._externalValuesFunc(docDict)
        else:
            return docDict

    def GetIdentificationValues(self, externalValues):
        """Given reconciliation item external values (as a name-value pair dictionary), return
        the values to be used for identification purposes.

        This function provides the opportunity to modify values set in the reconciliation
        document to match those defined in Front Arena. If no customisation of these
        values is necessary, simply return the passed externalValues.

        """
        if self._identificationValuesFunc:
            return self._identificationValuesFunc(externalValues)
        return externalValues

    def IdentifyReconciliationItem(self, matchedObjects, reconciliationItem):
        """Identify and return a Front Arena object corresponding to a reconciliation item.

        This function is only called if the normal method for locating reconciliation items
        (through identification rules and queries) fails to find an object, allowing
        for the possibility to locate the object through a customized method.
        Return the located ACM object, or None if one could not be found.

        """
        if self._identifyItemFunc:
            return self._identifyItemFunc(matchedObjects, reconciliationItem)
        return None

    def ExternalAttributeMapName(self):
        """The name of the FParameter extension mapping external attribute names
        to Front Arena attributes."""
        return self._externalAttributeMapName

    def ExternalAttributeMap(self):
        """Returns an FExternalAttributeMap (a dictionary-like object) mapping
        external attribute names to Front Arena attributes."""
        return FReconciliationIdentification.FExternalAttributeMap(self.ExternalAttributeMapName())

    def IdentificationRulesName(self):
        """The name of the FParameter extension defining the rules by which to
        identify Front Arena objects from reconciliation objects OR the trade query
        that represents the position spec used instead. Can be a list of queries"""
        return self._identificationRules

    def IdentificationRules(self):
        """Returns an FIdentificationRules objects used in identifying Front Arena
        objects from their reconciliation object counterparts."""
        #Note that comma separated method chains are no longer used but instead pos specs
        return FReconciliationIdentification.FIdentificationRules(self.IdentificationRulesName())

    def ReconciliationObjectType(self):
        """Returns the type of objects being reconciled."""
        return self._objectType
    
    def ReconciliationSubType(self):
        """Returns the sub type of objects being reconciled."""
        return self._subType

    def SheetTemplateName(self):
        """The name of the trading sheet template used in displaying reconciliation objects."""
        return self._sheetTemplateName

    def SheetTemplate(self):
        """Returns the trading sheet template object used in displaying reconciliation objects."""
        templateName = self.SheetTemplateName()
        return acm.FTradingSheetTemplate[templateName] if templateName else None

    def SheetType(self):
        """Returns the type of trading sheet used in representing the reconciled object type."""
        sheetTypeMap = {
            'Position': 'FPortfolioSheet',
            'Trade': 'FTradeSheet',
            'Settlement': 'FSettlementSheet',
            'Instrument': 'FDealSheet',
            'Journal': 'FJournalSheet'
        }
        sheetType = sheetTypeMap.get(self.ReconciliationObjectType(), None)
        if not sheetType:
            sheetTemplate = self.SheetTemplate()
            if sheetTemplate:
                sheetType = sheetTemplate.TradingSheetDefinition().SheetClass().Name()
        return sheetType
        
    def IsFXReconciliation(self):
        return self._isFxReconciliation

    def BusinessProcessSheetTemplateName(self):
        """The name of the trading sheet template used in displaying business processes tracking
        reconciliation items."""
        return self._businessProcessSheetTemplateName

    def BusinessProcessSheetTemplate(self):
        """Returns the trading sheet template used in displaying business processes tracking
        reconciliation items."""
        templateName = self.BusinessProcessSheetTemplateName()
        return acm.FTradingSheetTemplate[templateName] if templateName else None

    def UniverseQueries(self):
        """The name of the acm queries or query that defines all trades that should be reconciled."""
        return self._universeQueries

    def MaxUniverseQueries(self):
        """The maximum amount of universe queries to be generated from a two-way reconciliation."""
        return self._maxUniverseQueries
        
    def MaxNbrOfUnclosedReconItems(self):
        ''' Maximum number of unclosed recon items and business processes in a single reconciliation trial '''
        return self._maxNbrOfUnclosedReconItems

    def CreateColumnDefinitions(self):
        """If the column definitions should be created on save"""
        if self._createColumnDefinitions is not None:
            return self._createColumnDefinitions == 'True'
        else:
            return True
            
    def ReconciliationSpecification(self):
        return acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self._name)

    def StateChartName(self):
        """The name of the state chart defining the business process reconciliation workflow."""
        return self._stateChartName

    def StateChart(self):
        """Returns the state chart object defining the business process reconciliation workflow."""
        return acm.FStateChart[self.StateChartName()]

    def StoreReconciledItems(self, storeRecomciledItems=None):
        """Returns true if successfully reconciled items are to be persisted."""
        if storeRecomciledItems is None:
            return self._storeReconciledItems
        else:
            self._storeReconciledItems = storeRecomciledItems

    def Upload(self):
        return self._upload

    def ComparisonType(self):
        """Returns if comparsion columns should be absolute, relative or not added to the trading sheet."""
        return self._comparisonType

    def ValueMappingName(self):
        """The name of the FParameter extension mapping external attribute names
        to Front Arena columns for value comparison."""
        return self._valueMappingName

    def ValueMapping(self):
        """Returns a dictionary mapping external attribute names to Front Arena columns for
        value comparison."""
        if not self.ValueMappingName():
            return None
        extension = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self.ValueMappingName())
        return extension.Value() if extension else None

    def DataTypeMappingName(self):
        """The name of the FParameter extension mapping external attribute names to their data types."""
        return self._dataTypeMappingName
  
    def DataTypeMapping(self):
        """Returns a dictionary mapping external attribute names to their data types."""
        if not self.DataTypeMappingName():
            return None        
        extension = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self.DataTypeMappingName())
        return extension.Value() if extension else None

    def PreCommit(self, businessObject, externalValues):
        editedObject = businessObject
        if self._precommitFunc:
            editedObject = self._precommitFunc(businessObject, externalValues)
        return editedObject
    
    def PostProcessing(self, FUploadEngineInstance):
        outputValue = None 
        if self._postprocessingFunc:
            recoDoc = FUploadEngineInstance.ReconciliationInstance().ReconciliationDocument()
            outputValue = self._postprocessingFunc(self, recoDoc)
        return outputValue
    
    def _ReconSpecInContext(self):
        reconSpec = self.ReconciliationSpecification()
        return bool(reconSpec)
        
    def _ReconSpecKeys(self):
        return [str(key) for key in self.ReconciliationSpecification().Value().Keys()]

    def _LoadFromExtension(self, relaxValidation, onLoad):
        mode = 'Loading' if onLoad is True else 'Saving'
        if relaxValidation is False:                
            logger.info('%s %s specification %s...' % (mode, 'reconciliation' if not self.Upload() else 'data upload', self.Name()))    
        extension = self.ReconciliationSpecification()
        if not extension:
            raise ValueError('Failed to load FParameter extension "%s"' % self._name)
        extensionParams = extension.Value()

        for parameter, attribute, mandatory in self._FPARAMETER_ATTRIBUTES:
            attributeType = type(getattr(self, attribute))
            if attributeType == list:
                value = [str(symbol) for symbol in extensionParams.GetArray(parameter)]
            elif attributeType == bool:
                value = extensionParams.GetBool(parameter)
            else:
                # Type cast to integers if possible
                value = extensionParams.GetString(parameter)                
                try:
                    value = int(value)
                except ValueError:
                    pass           
                assert value is not None
            if value is not None:
                setattr(self, attribute, value)
            elif mandatory:
                raise ValueError('Mandatory attribute "%s" has not been defined' % parameter)
        
        # For backwards compatibility, make sure the reader type is set.
        # If the parser hook is set, the type will be 'Custom' and 'CSV' otherwise.
        if not self._readerType:
            if self._parserFunc and type(self._parserFunc) is str:
                self._readerType = 'Custom'
            else:
                self._readerType = 'CSV'
        if self._identificationValuesFunc:
            self._identificationValuesFunc = FBusinessDataImportHook.FBusinessDataImportHook(self._identificationValuesFunc)
        if self._identifyItemFunc:
            self._identifyItemFunc = FBusinessDataImportHook.FBusinessDataImportHook(self._identifyItemFunc)
        self._parserFunc = FReconciliationReaderFactory.GetReconciliationDocumentReader(self.ReaderType(), self._parserFunc)
        if self._externalValuesFunc:
            self._externalValuesFunc = FBusinessDataImportHook.FBusinessDataImportHook(self._externalValuesFunc)
        if self._precommitFunc:
            self._precommitFunc = FBusinessDataImportHook.FBusinessDataImportHook(self._precommitFunc)
        if self._postprocessingFunc:
            self._postprocessingFunc = FBusinessDataImportHook.FBusinessDataImportHook(self._postprocessingFunc)
            
    @staticmethod
    def _ValidateIntegerConversion(attr, method):
        value = method()
        if value is not None:
            castedValue = None
            try:
                castedValue = int(value)
            except ValueError:
                raise ValueError(attr + ' could not be converted to an integer.')
            if castedValue < 0:
                raise ValueError(attr + ' must not be less than zero.')
        else:
            raise ValueError('Invalid reconciliation specification %s: attribute %s has not been assigned a value' % (self.Name(), attr))
            
    def _ValidateAttribute(self, attr, method):
        if not attr in self._ReconSpecKeys():
            raise ValueError('Required attribute %s is not available in the reconciliation specification %s' % (attr, self.Name()))
        self._ValidateIntegerConversion(attr, method)
        
    def _Validate(self):
        try:
            # Forward compatability
            acm.EnumFromString('ReconciliationObjectType', self._objectType)
        except RuntimeError:
            if not self._objectType == 'Order': 
                raise ValueError(str(self._objectType) + ' is not a valid ReconciliationObjectType enumeration')
        if not self.StateChart():
            raise ValueError('Failed to load FStateChart "%s"' % self.StateChartName())
        if not self.ExternalAttributeMap():
            raise ValueError('Failed to load external attribute map "%s"' % self.ExternalAttributeMapName())
        if not self.IdentificationRules():
            raise ValueError('Failed to load identification rules "%s". Must point to parameter or queries.' % self.IdentificationRulesName())
        if not self.ValueMapping():
            raise ValueError('Failed to load values map "%s"' % self.ValueMappingName())
        if not self.DataTypeMapping():
            raise ValueError('Failed to load data type map "%s"' % self.DataTypeMappingName())
        if not self._parserFunc and self.ReaderType() == 'Custom':
            raise ValueError('Custom file format requires a file format hook')
        if not self.Upload():  
            self._ValidateAttribute('Max Nbr Of Items Missing in Document', self.MaxUniverseQueries)
            self._ValidateAttribute('Max Nbr Of Unclosed Recon Items', self.MaxNbrOfUnclosedReconItems)