""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftParametersMetaDataCheck.py"

import FSwiftMTBase
import FOperationsUtils as Utils

metaDataOptions = FSwiftMTBase.METADATA_OPTIONS

def MetaDataCheck():
    print('\t\t\t\t Meta Data Check Started')
    VerifySwiftParametersModule()
    ValidateMessageTypeConfiguration()
    for messageType in metaDataOptions:
        ValidateFieldConfiguration(messageType)
        ValidateOptionConfiguration(messageType)
    print('\t\t\t\t Meta Data Check Done')

def VerifySwiftParametersModule():
    import FSwiftParameters as SwiftParams
    
    if SwiftParams.__name__ == "FSwiftParameters":
        Utils.VerifyParameterModule("FSwiftParametersTemplate", SwiftParams.__name__)

def ValidateMessageTypeConfiguration():
    missingMessageTypes = GetMissingMessageTypes()
    if missingMessageTypes:
        print('\t\t\t\t Error : Message type(s) %s missing in FSwiftParameters' % missingMessageTypes)
        raise LookupError

def ValidateFieldConfiguration(messageType):
    CheckMissingFields(messageType)
    CheckUnSupportedFields(messageType)

def ValidateOptionConfiguration(messageType):
    missingFields = GetMissingFields(messageType)
    for fieldName in metaDataOptions[messageType]:
        if fieldName not in missingFields:
            CheckOptionConfiguration(messageType, fieldName)

def CheckMissingFields(messageType):
    fieldsMissingInSwiftParams = GetMissingFields(messageType)
    if fieldsMissingInSwiftParams:
        for fieldName in fieldsMissingInSwiftParams:
            print('\t\t\t\t Field missing: %s in FSwiftParameters for Swift Message Type MT%s ' % (fieldName, str(messageType)))
        print('\t\t\t\t Warning: Field(s) missing in FSwiftParameters configuration.\n\t\t\t\t Ignore if above field(s) exluded intentionally\n\t\t\t\t Please Check SWIFT Standards/FCA 4437')

def CheckUnSupportedFields(messageType):
    fieldsUnSupportedInFA = GetUnSupportedFields(messageType)
    if fieldsUnSupportedInFA:
        for fieldName in fieldsUnSupportedInFA:
            print('\t\t\t\t Field not supported: %s for MT%s' % (fieldName, str(messageType)))
        print('\t\t\t\t Error(s): FSwiftParameters is not configured properly. \n\t\t\t\t Please Check SWIFT Standards/FCA 4437')

def CheckOptionConfiguration(messageType, fieldName):
    supportedOptions = GetSupportedOptions(messageType, fieldName)
    configuredOption = GetConfiguredOption(messageType, fieldName)
    if len(configuredOption) > 1:
        print('\t\t\t\t Error: Single supported option must be specified for field %s on MT%s' % (fieldName, str(messageType)))
    elif configuredOption not in supportedOptions:
        print('\t\t\t\t Error: Option not supported in FRONT ARENA: Option %s for %s Swift Message Type MT%s.' % (configuredOption, fieldName, messageType))
        print('\t\t\t\t FRONT ARENA Supported Options for %s: %s' % (fieldName, supportedOptions))

def GetMissingMessageTypes():
    import FSwiftParameters as SwiftParams

    configuredOptions = SwiftParams.OPTIONS

    supportedMTs = metaDataOptions.keys()
    configuredMTs = configuredOptions.keys()
    return list(set(supportedMTs) - set(configuredMTs))

def GetMissingFields(messageType):
    import FSwiftParameters as SwiftParams

    configuredOptions = SwiftParams.OPTIONS

    return list(set(metaDataOptions[messageType].keys()) - set(configuredOptions[messageType].keys()))

def GetUnSupportedFields(messageType):
    import FSwiftParameters as SwiftParams

    configuredOptions = SwiftParams.OPTIONS

    return list(set(configuredOptions[messageType].keys()) - set(metaDataOptions[messageType].keys()))

def GetSupportedOptions(messageType, fieldName):
    return metaDataOptions[messageType][fieldName]

def GetConfiguredOption(messageType, fieldName):
    import FSwiftParameters as SwiftParams

    configuredOptions = SwiftParams.OPTIONS

    return configuredOptions[messageType][fieldName].strip()

def run():
    MetaDataCheck()
