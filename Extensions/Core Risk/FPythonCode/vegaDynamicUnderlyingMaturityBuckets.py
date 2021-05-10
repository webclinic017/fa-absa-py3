
import acm
import FUxUtils
import FUxCore

shiftDateFunction = acm.GetFunction("shiftVolatilityStructureDate", 2)

def OnSelectTimeBuckets(self, cd ):
    timeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_fuxDlg.Shell(), self.m_storedTimeBuckets)
    if timeBuckets:
        self.m_storedTimeBuckets = timeBuckets
        self.m_timeBuckets = timeBuckets.TimeBuckets()
    self.UpdateControls()

class vegaunderlyingMaturityDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_initialData = None
        self.m_shiftAllStructures = None
        self.m_volatilityStructures = None
        self.m_storedTimeBuckets = None
        self.m_timeBuckets = None
        self.m_timeBucketsEdit = None
        self.m_timeBucketsBtn = None
        self.m_okBtn = None

    def HandleApply( self ):
        if not self.m_bindings.Validate(True):
            return None
        dictResult = self.m_bindings.GetValuesByName()
        dictResult.AtPut('timeBuckets', self.m_timeBuckets )
        return dictResult

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()

    def UpdateControls(self):
        if self.m_timeBuckets:
            self.m_timeBucketsEdit.SetData(self.m_timeBuckets.StringKey() )
        else:
            self.m_timeBucketsEdit.SetData('')
        shiftAllStructures = self.m_bindings.GetValuesByName().At('shiftAllStructures')
        self.m_volatilityStructures.Enabled(not shiftAllStructures)
        ok = False
        if self.m_bindings.Validate(False):
            vol = self.m_bindings.GetValuesByName().At('volatilityStructure')
            if (self.m_timeBuckets != None) and ((vol != None) or shiftAllStructures): 
                ok = True
        self.m_okBtn.Editable( ok )

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_timeBucketsEdit = layout.GetControl('timeBuckets')
        self.m_timeBucketsBtn = layout.GetControl('timeBucketsBtn')
        self.m_fuxDlg.Caption('Vega Buckets' )
        self.m_okBtn = layout.GetControl('ok')
        self.m_bindings.AddLayout(layout)
        self.m_timeBucketsEdit.Editable(False)
        self.m_timeBucketsBtn.AddCallback('Activate', OnSelectTimeBuckets, self)
        self.m_shiftAllStructures.SetValue(True)
        if self.m_initialData :
            self.m_bindings.SetValuesByName(self.m_initialData)
            self.m_timeBuckets = self.m_initialData.At('timeBuckets')
        self.UpdateControls()

    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_shiftAllStructures = self.m_bindings.AddBinder('shiftAllStructures', acm.GetDomain('bool'), None)
        self.m_volatilityStructures = self.m_bindings.AddBinder('volatilityStructure', acm.GetDomain('FVolatilityStructure'), None)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        self.m_shiftAllStructures.BuildLayoutPart(b, 'Shift All Volatility Structures')
        self.m_volatilityStructures.BuildLayoutPart(b, 'Volatility Structure')
        b.    BeginHorzBox('None')
        b.      AddInput('timeBuckets', 'Time Buckets' )
        b.      AddButton('timeBucketsBtn', '...', False, True )
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

def ael_custom_dialog_show(shell, parameters):
    vegaUMDlg = vegaunderlyingMaturityDialog()
    initData = FUxUtils.UnpackInitialData(parameters)
    dialogData = None
    if initData:
        dialogData = initData.At('dialogData')
    vegaUMDlg.InitControls()
    vegaUMDlg.m_initialData = dialogData

    dialogData = acm.UX().Dialogs().ShowCustomDialogModal(shell, vegaUMDlg.CreateLayout(), vegaUMDlg)
    if dialogData:
        resultDict = acm.FDictionary()
        resultDict.AtPut('dialogData', dialogData)
        return resultDict    
    return None

def ael_custom_dialog_main(parameters, dictExtra):
    dialogData = parameters.At('dialogData')
    shiftAllStructures = dialogData.At('shiftAllStructures')
    shiftFilter = acm.FObject
    if not shiftAllStructures:
        shiftToDate = 0
        if acm.IsHistoricalMode():
            shiftToDate = acm.Time().DateToday()
        shiftFilter = shiftDateFunction(
                        dialogData.At('volatilityStructure'),
                        shiftToDate)
    resultVector = []
    for timeBucket in dialogData.At('timeBuckets'):
        np = acm.FNamedParameters()
        np.Name(timeBucket.Name())
        np.UniqueTag(timeBucket.Spec())
        np.AddParameter('timeBucket', timeBucket)
        np.AddParameter('shiftFilter', shiftFilter)
        resultVector.append(np)
    return resultVector
