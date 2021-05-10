
import FUxUtils
import acm
import VegaDynamicStrikeBucketsBase
from VegaDynamicStrikeBucketsBase import VegaDynamicStrikeBucketsDialogBase

strikeTypeEnums = acm.FEnumeration['enum(StrikeType)'].Enumerators()
strikeTypes = []
for index in range(1, len(strikeTypeEnums)):
    strikeTypes.append(acm.FSymbol(strikeTypeEnums[index]))

class VegaDynamicStrikeBucketsDialog (VegaDynamicStrikeBucketsDialogBase):

    def __init__(self):
        VegaDynamicStrikeBucketsDialogBase.__init__( self )

    def HandleCreate( self, dlg, layout):
        VegaDynamicStrikeBucketsDialogBase.HandleCreate( self, dlg, layout )
        self.m_strikeLadderType.Populate(strikeTypes)

def ael_custom_dialog_show(shell, parameters):
    dialog = VegaDynamicStrikeBucketsDialog()
    initData = FUxUtils.UnpackInitialData(parameters)
    if initData:
        dialog.m_initialData = initData.At('dialogData')
    dialog.InitControls()
    dialogData = acm.UX().Dialogs().ShowCustomDialogModal(shell, 
        dialog.CreateLayout(), dialog)
    if dialogData:
        resultDict = acm.FDictionary()
        resultDict.AtPut('dialogData', dialogData)
        return resultDict
    return None

def RefactorOldParameters( parameters ):
    newParams = acm.FDictionary()
    for key in parameters.Keys():
        key = key.AsString()
        k1 = key.replace(' ', '')
        newKey = acm.FSymbol( ''.join([k1[0].lower(), k1[1:len(k1)]]))
        newParams.AtPut( newKey, parameters.At( key ) )
    return newParams

def ael_custom_dialog_main(parameters, dictExtra):
    resultVector = []
    dialogData = parameters.At('dialogData')
    if not dialogData:
        dialogData = RefactorOldParameters( parameters )
    return VegaDynamicStrikeBucketsBase.GenerateStrikeBuckets( dialogData )

def ael_custom_label(parameters, dictExtra):
    dialogData =  parameters.At('dialogData')
    lbl = None
    if not dialogData:
        dialogData = RefactorOldParameters( parameters )
    if dialogData:
        vol =  dialogData.At(acm.FSymbol('volatilityStructure'))
        if vol:
            lbl = vol.StringKey()
        if dialogData.At(acm.FSymbol('includeAdditionalDimension')):
            timeBuckets = dialogData.At(acm.FSymbol('additionalTimeBuckets'))
            idx = int(dialogData.At(acm.FSymbol('additionalTimeBucketIdx')))
            if timeBuckets:
                timeBucket = timeBuckets[idx - 1]
                if timeBucket:
                    lbl = lbl + " - Maturity: " + timeBucket.StringKey()     
    return lbl
