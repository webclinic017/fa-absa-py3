from __future__ import print_function
import acm
import sys
import Contracts_LookupServices_Attributes_Messages_QueryAttributes as ContractMessages
import LookupServicePluginBase

def GetExtensionValue(extensionValue):
    extension = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'LookupServiceSettings')
    if extension:
        consParams = extension.Value()
        params = {str(key): str(consParams[key]) for key in consParams.Keys()}

        if extensionValue in params:
            return params[extensionValue]
    return None

def EnableDebug():
    debug = GetExtensionValue("ConservatoryDebug")
    if debug and debug == "True":
        return True
    return False

s_debugEnabled = EnableDebug()

def globalimport(module_name):
    globals()[module_name] = __import__(module_name)


class AttributeColumnEnum:
    MethodName = 0
    IsIndexed = 1
    ValueType = 2
    
s_conservatoryAttributes = \
    {\
        'Isin':                        ['Isin', True, LookupServicePluginBase.AssignString], \
        'isin':                        ['Isin', True, LookupServicePluginBase.AssignString], \
        'Source':                      ['Source', False, LookupServicePluginBase.AssignString], \
        'TradingVenueMic':             ['TradingVenueMic', False, LookupServicePluginBase.AssignString], \
        'LargeInScale':                ['PreLargeInScale', False, LookupServicePluginBase.AssignDouble], \
        'StandardMarketSize':          ['StandardMarketSize', False, LookupServicePluginBase.AssignDouble], \
        'SizeSpecificToInstrument':    ['PreTradeSizeSpecificToIns', False, LookupServicePluginBase.AssignDouble], \
        'HasTradingObligation':        ['HasTradingObligation', False, LookupServicePluginBase.AssignBool], \
        'IsLiquid':                    ['IsLiquid', False, LookupServicePluginBase.AssignBool], \
        'IsSystematicInternaliser':    ['IsSystematicInternaliser', False, LookupServicePluginBase.AssignBool], \
        'LiquidityBand':               ['LiquidityBand', False, LookupServicePluginBase.AssignInt32], \
        'TickSize':                    ['TickSize', False, LookupServicePluginBase.AssignDouble], \
        'CfiCode':                     ['CfiCode', False, LookupServicePluginBase.AssignString], \
        'ClearingIsMandatory':         ['ClearingIsMandatory', False, LookupServicePluginBase.AssignBool], \
        'InstypeRTS28':                ['MiFIDIIRTS28InsType', False, LookupServicePluginBase.AssignString], \
        'PrimaryMarketMic':            ['PrimaryMarketMic', False, LookupServicePluginBase.AssignString], \
        'MaterialMarketMic':           ['MaterialMarketMic', False, LookupServicePluginBase.AssignString], \
        'DarkCapStatus':               ['DarkCapStatus', False, LookupServicePluginBase.AssignString], \
        'DoubleVolumeCapStatus':       ['DoubleVolumeCapStatus', False, LookupServicePluginBase.AssignString], \
        'DarkCapMic':                  ['DarkCapMic', False, LookupServicePluginBase.AssignString], \
        'AverageDailyTurnover':        ['AverageDailyTurnover', False, LookupServicePluginBase.AssignDouble], \
        'IsMiFIDTransparent':          ['IsMiFIDTransparent', False, LookupServicePluginBase.AssignBool], \
    }


class ConservatoryLookupProvider(LookupServicePluginBase.LookupServicePluginProviderBase):
    def __init__(self, serviceAttributes, tableName):
        self.knownAttributes = serviceAttributes
        self.tableName = tableName

    def ReadConservatorySourceOrder(self):
        sourceOrder = GetExtensionValue("ConservatorySourceOrder")
        if sourceOrder:
            return sourceOrder.split(",")
        if s_debugEnabled:
            print ("<Debug> Source order not set.")
        return sourceOrder

    def GetRowBySourceOrder(self, rows):
        self.sourceOrder = self.ReadConservatorySourceOrder()
        index = 0
        usedIndex = 9999
        usedRow = None
        if self.sourceOrder:
            for i, row in enumerate(rows):
                src = row.Source().strip(" ")
                if src in self.sourceOrder:
                    index = self.sourceOrder.index(src)
                    if index < usedIndex:
                        usedIndex = index
                        usedRow = row
                else:
                    if s_debugEnabled:
                        print ("<Debug> Instrument source not in SourceOrder. ", src)

        if rows and usedRow is None:
            if s_debugEnabled:
                print ("<Debug> Using default source order.")
            usedRow = rows[0]
        return usedRow

    # ################# LookupService plugin Interface methods
    def GetTableName(self):
        return self.tableName
        
    def LookupTableObject(self, providedAttributes):
        row = None
        usedAttributeInfo = None
        
        for attributeTypeAndValue in providedAttributes:
            attributeInfo = self.knownAttributes.get(attributeTypeAndValue.type)
            
            if attributeInfo and attributeInfo[AttributeColumnEnum.IsIndexed]:
                if s_debugEnabled:
                    print ("<debug> Conservatory searching for attribute: ", attributeTypeAndValue.type, " = ", attributeTypeAndValue.value)

                value = attributeTypeAndValue.value

                instrList = Conservatory.GetInstrument(value)
                if instrList:
                    row = self.GetRowBySourceOrder(instrList)

                if row:
                    usedAttributeInfo = attributeTypeAndValue
                    break
        return row, usedAttributeInfo
    
    def BuildResult(self, definition, tableRow, usedAttribute):
        keyValues = []        

        resultKey = ContractMessages.ResultKey()
        resultKey.uniqueId.MergeFrom(usedAttribute)
        result = ContractMessages.Result()
        for requestedAttributeName in definition.requestedAttributeNames:
            attribute = None
            attributeInfo = self.knownAttributes.get(requestedAttributeName)

            resultValue = result.values.add() 
            resultValue.status = ContractMessages.Value().HAS_VALUE
            try:
                method = None
                if attributeInfo[AttributeColumnEnum.MethodName]:
                    methodName = attributeInfo[AttributeColumnEnum.MethodName]
                    method = getattr(tableRow, methodName)
                if method:
                    attribute = method()
                    if attribute and isinstance(attribute, acm._pyClass(acm.FChoiceList)):
                        attribute = attribute.Name()
                if attribute is not None:
                    LookupServicePluginBase.AssignVariantValue(resultValue.attributeValue, attribute, attributeInfo[AttributeColumnEnum.ValueType] )
                else:
                    resultValue.status = ContractMessages.Value().NOT_APPLICABLE

            except BaseException as err:
                resultValue.status = ContractMessages.Value().FAILURE
                resultValue.failureReason = LookupServicePluginBase.ToUnicode(str(err))

        keyValues.append( [resultKey, result] )
        return keyValues


s_supportedProviders = {ConservatoryLookupProvider(s_conservatoryAttributes, "instrument"), ConservatoryLookupProvider(s_conservatoryAttributes, "conservatory") }

class ConsrvatoryLookupServicePlugin(LookupServicePluginBase.LookupServicePluginBase):

    def GetPluginName(self):
        return "ConsrvatoryLookupServicePlugin"

    def InitializePlugin(self):
        self.conservatoryEnabled = self.EnableConservatory()

    def EnableConservatory(self):
        retValue = False
        conservatoryPath = GetExtensionValue("ConservatoryPath")
        if conservatoryPath:
            if not conservatoryPath in sys.path:
                sys.path.append(conservatoryPath)
            try:
                globalimport("Conservatory")
                if s_debugEnabled:
                    print ("<debug> Conservatory module loaded ok.")
                retValue = True
            except ImportError:
                if s_debugEnabled:
                    print ("<debug> Conservatory module failed to load.")
                    raise StandardError('ConsrvatoryLookupServicePlugin Failed to import Conservatory.')
        return retValue

    def GetProviders(self):
        return s_supportedProviders;




ael_variables = []

def ael_main_ex(parameters, dictExtra):
    print ("Loading LookupService : ConsrvatoryLookupServicePlugin")
    lookupPlugin = ConsrvatoryLookupServicePlugin()
    return lookupPlugin

