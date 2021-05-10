
import acm
import FUxUtils
import VegaDynamicStrikeBucketsBase
from VegaDynamicStrikeBucketsBase import VegaDynamicStrikeBucketsDialogBase

class VegaDynamicStrikeBucketsDialogPortfolioSheet (VegaDynamicStrikeBucketsDialogBase):

    def __init__(self):
        VegaDynamicStrikeBucketsDialogBase.__init__( self )

    def HandleCreate( self, dlg, layout):
        VegaDynamicStrikeBucketsDialogBase.HandleCreate( self, dlg, layout )
        self.m_includeAdditionalDimension.Visible( False )
        self.m_additionalTimeBucketsEdit.Visible( False )
        self.m_additionalTimeBucketsBtn.Visible( False )
        self.m_additionalTimeBucketIdx.Visible( False )
        self.m_additionalTimeBucket.Visible( False )
        self.UpdateVolatilityDependentControls(False, '')
        self.m_useOneSidedShift.Visible( True )
        self.m_strikeLadderType.Populate(VegaDynamicStrikeBucketsBase.connectedStrikeTypes)

    def PopulateVolStructs(self):
        volatilityStructures = acm.FVolatilityStructure.Select('strikeType="Absolute"')
        volatilityStructures = volatilityStructures.SortByProperty('Name')
        self.m_volStructControl.Populate(volatilityStructures)

    def OnVolatilityStructureChanged(self, cd, ud):
        self.m_volStruct = acm.FVolatilityStructure[self.m_volStructControl.GetData()]
        if self.m_volStruct:
            self.m_referenceInstrument = self.m_volStruct.ReferenceInstrument()
            self.UpdateVolatilityDependentControls(True, self.m_referenceInstrument.Name() if self.m_referenceInstrument else '')
            self.UpdateStrikeTypeSelection()
        else:
            self.UpdateVolatilityDependentControls(False, '')
        self.m_groupingSensitive.Enabled( self.m_volStruct == None )
        self.Generate()

    def UpdateVolatilityDependentControls(self, enabled, referenceInstrument):
        self.m_useVolStructStrikes.Enabled(enabled)
        self.m_strikeLadderType.Enabled(enabled)
        self.m_strikeBucketsCount.Enabled(enabled)
        self.m_firstStrike.Enabled(enabled)
        self.m_strikeBucketsInterval.Enabled(enabled)
        self.m_includeRestBucket.Enabled(enabled)
        self.m_strikeBucketsString.Enabled(enabled)
        self.m_referenceInstrumentControl.SetData(referenceInstrument)
        self.m_strikeLadderType.Populate(VegaDynamicStrikeBucketsBase.connectedStrikeTypes if referenceInstrument else [acm.FSymbol('Absolute')])
        self.UpdateStrikeGenerationChoices()

    def UpdateStrikeTypeSelection(self):
        if not self.m_strikeLadderType.GetData():
            self.m_strikeLadderType.SetData(acm.FSymbol('Absolute'))

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
        volatilityStructure = dialogData.At(acm.FSymbol('volatilityStructure'))
        if volatilityStructure:
            label = volatilityStructure.StringKey()
    return label
