
import acm
import FUxUtils
import VegaDynamicStrikeBucketsBase
from VegaDynamicStrikeBucketsBase import VegaDynamicStrikeBucketsDialogBase

class VegaDynamicStrikeBucketsDialogPortfolioSheet (VegaDynamicStrikeBucketsDialogBase):

    def __init__(self):
        VegaDynamicStrikeBucketsDialogBase.__init__( self )

    def HandleCreate( self, dlg, layout):
        VegaDynamicStrikeBucketsDialogBase.HandleCreate( self, dlg, layout )
        self.m_volStructControl.Visible( False )
        self.m_useVolStructStrikes.Visible( False )
        self.m_referenceInstrumentControl.Visible( False )
        self.m_includeAdditionalDimension.Visible( False )
        self.m_additionalTimeBucketsEdit.Visible( False )
        self.m_additionalTimeBucketsBtn.Visible( False )
        self.m_additionalTimeBucketIdx.Visible( False )
        self.m_additionalTimeBucket.Visible( False )
        self.m_groupingSensitive.Visible( True )
        self.m_useOneSidedShift.Visible( True )
        self.UpdateStrikeTypeSelection()

    def OnGroupingSensitiveChanged(self, cd, ud):
        self.UpdateStrikeTypeSelection()
        self.Generate()

    def UpdateStrikeTypeSelection(self):
        groupingSensitive = self.m_groupingSensitive.GetValue()
        currentData = acm.FSymbol(self.m_strikeLadderType.GetData())
        strikeTypes = VegaDynamicStrikeBucketsBase.connectedStrikeTypes if groupingSensitive else [acm.FSymbol('Absolute')]
        self.m_strikeLadderType.Populate(strikeTypes)
        if currentData and (currentData in strikeTypes):
            self.m_strikeLadderType.SetData(currentData)
        else:
            self.m_strikeLadderType.SetData(acm.FSymbol('Absolute'))
        VegaDynamicStrikeBucketsDialogBase.UpdateStrikeTypeSelection(self)

def ael_custom_dialog_show(shell, parameters):
    dialog = VegaDynamicStrikeBucketsDialogPortfolioSheet()
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

def ael_custom_dialog_main(parameters, dictExtra):
    dialogData = parameters.At('dialogData')
    return VegaDynamicStrikeBucketsBase.GenerateStrikeBuckets( dialogData )

def ael_custom_label(parameters, dictExtra):
    dialogData =  parameters.At('dialogData')
    label = None
    if dialogData:
        strikeType = dialogData.At(acm.FSymbol('strikeLadderType'))
        label = 'Ladder Type: ' + str(strikeType)
        groupingSensitive = dialogData.At(acm.FSymbol('groupingSensitive'))
        if groupingSensitive:
            label += ' - Grouping Sensitive: Yes'    
    return label
