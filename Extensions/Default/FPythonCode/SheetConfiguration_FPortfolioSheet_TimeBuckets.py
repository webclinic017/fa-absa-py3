
import acm
import FUxCore

def ael_custom_dialog_show(shell, params):
    result = None
    stb = None
    if params:
        stb = params['timeBuckets']
    stb = acm.UX().Dialogs().SelectTimeBuckets(shell, stb )
    if stb:
        result = acm.FDictionary()
        result.AtPut('timeBuckets', stb )
    return result;

def ael_custom_dialog_main( parameters, dictExtra ):
    stb = parameters['timeBuckets']
    extensionObject = dictExtra['customData'].ExtensionObject()
    extensionObject.ColumnSetupExtensionAttribute('_defaultProjectedRiskColumns')
    extensionObject.TimeBucketsTemplate(stb.TimeBuckets())
    return extensionObject




