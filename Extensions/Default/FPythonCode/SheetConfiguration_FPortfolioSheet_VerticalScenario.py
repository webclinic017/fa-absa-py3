
import acm
import FUxCore

def ael_custom_dialog_show(shell, params):
    result = None
    scenario = acm.UX().Dialogs().SelectScenario(shell)
    if scenario:
        result = acm.FDictionary()
        result.AtPut('scenario', scenario )
    return result;

def ael_custom_dialog_main( parameters, dictExtra ):
    scenario = parameters['scenario']
    extensionObject = dictExtra['customData'].ExtensionObject()
    extensionObject.VerticalScenario(scenario)
    return extensionObject






