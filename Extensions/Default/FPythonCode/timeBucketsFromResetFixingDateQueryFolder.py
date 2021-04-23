import acm
import ael
import FUxCore

TOOL_TIP_FOR_QUERY_FOLDER = 'Select an Insert Item query that directly or implicitly (by having Insert Item "Find What:" set to Trade or Trade Filter) points out a set of cash flow instruments who\'s future reset dates (taken from any fixed or un-fixed reset) should be used to generate time buckets.'
TOOL_TIP_FOR_NUMBER_OF_BUCKETS = 'The maximum number of future time buckets that should be generated (including any bucket with today\'s date).'
TOOL_TIP_FOR_NO_BUCKETS_AFTER_DATE_PERIOD = 'No buckets are generated after the defined, non-calendar adjusted, period (calendar days, weeks, month or years).'
TOOL_TIP_FOR_ADVANCED_BTN = 'Advanced mode makes it possible to select which cash flow reset types time buckets should be generated from.'
TOOL_TIP_FOR_NORMAL_BTN = 'In normal mode all cash flow reset types applicable for Fixing Risk is used to generate time buckets (given that all checkboxes are left as selected).'


def ael_custom_label( parameters, dictExtra ):
    queryFolder =  parameters.At('queryFolder')
    if queryFolder:
       return '(' + queryFolder.StringKey() + ')'
    return None

def ael_custom_dialog_show(shell, params):
    dlg = ResetFixingDateBucketUI(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg )    

def ael_custom_dialog_main( parameters, dictExtra ):
    return CreateBuckets(parameters)
    
def addResetsDatesToDictRecursive( queryObject, dateDict, selectedResetTypes):
    if queryObject.IsKindOf("FTradeSelection"):
        for queryObj in queryObject.Trades():
            addResetsDatesToDictRecursive( queryObj, dateDict, selectedResetTypes)
    instrumentMethod = queryObject.Class().GetMethod( "Instrument", None )
    if instrumentMethod:
        cfInstrument = instrumentMethod.Call( [queryObject] )
        if cfInstrument.IsKindOf('FCashFlowInstrument'):
            for leg in cfInstrument.Legs():
                for cashFlow in leg.CashFlows():
                    for reset in cashFlow.Resets():
                        if reset.ResetType() in selectedResetTypes:
                            dateDict.AtPutStrings(reset.Day(), reset.Day())

def CreateBuckets( parameters ):
 
    queryFolder = parameters.At('queryFolder')
    numberOfBuckets = parameters.At('numberOfBuckets')
    noBucketsAfterDatePeriod = parameters.At('noBucketsAfterDatePeriod')
    selectedResetTypes = parameters.At('resetTypes')
    dateDict = acm.FDictionary()
   
    for queryObject in queryFolder.Query().Select():
        addResetsDatesToDictRecursive( queryObject, dateDict, selectedResetTypes)
    
    buckets = acm.FArray()
    noBucketsAfterDate = ael.date_today().add_period(noBucketsAfterDatePeriod)

    count = 0
    for dateKey in dateDict.Keys().Sort():
        date = dateDict.At(dateKey)
        if numberOfBuckets > count and acm.Time.DateDifference( ael.date_today(), date ) <= 0:
            if acm.Time.DateDifference( date, noBucketsAfterDate ) <= 0:
                bucketDef = acm.FFixedDateTimeBucketDefinition()
                bucketDef.FixedDate(date)      
                buckets.Add(bucketDef)
                count = count + 1

    return buckets;
    
def OnAdvancedResetTypesClicked(self, cd):

    self.m_advancedResetTypesModeEnabled = not self.m_advancedResetTypesModeEnabled
    self.UpdateControls()

def ToCamelCase(originalString):

    words = originalString.split(' ')
    result = words[0].lower()
    endWords = [word.title() for word in words[1:]]
    for w in endWords:
        result += w
    return result

class ResetFixingDateBucketUI (FUxCore.LayoutDialog):

    def __init__(self, parameters):

        self.m_okBtn = 0
        self.m_queryFolder = 0
        self.m_numberOfBucketInput = 0
        self.m_noBucketsAfterDatePeriod = 0
        self.m_resetTypeBinders = acm.FDictionary()
        self.m_advancedResetTypesModeBtn = None
        self.m_advancedResetTypesModeEnabled = False
        self.m_bindings = 0
        self.m_parameters = parameters.At('initialData')
        self.m_supportedResetTypes = ['Single', 'Weighted', 'Unweighted', 'Compound', 'Flat Compound', \
                                      'Compound Spread Excluded', 'Weighted 1m Compound', 'Accretive', \
                                      'Total Weighted', 'Compound of Weighted', 'Compound Float Fctr Included']
        self.m_supportedResetTypes.sort()
        self.InitControls()

    def CreateToolTip(self):
        self.m_queryFolder.ToolTip(TOOL_TIP_FOR_QUERY_FOLDER)
        self.m_numberOfBucketInput.ToolTip(TOOL_TIP_FOR_NUMBER_OF_BUCKETS)
        self.m_noBucketsAfterDatePeriod.ToolTip(TOOL_TIP_FOR_NO_BUCKETS_AFTER_DATE_PERIOD)

    def AdvancedResetTypesModeEnabled(self):
        return self.m_advancedResetTypesModeEnabled

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass

    def HandleApply( self ):

        params = acm.FDictionary()
        queryFolder = self.m_queryFolder.GetValue()        
        numberOfBuckets = int(self.m_numberOfBucketInput.GetValue())
        noBucketsAfterDatePeriod = self.m_noBucketsAfterDatePeriod.GetValue()
        advancedResetTypesEnabled = self.m_advancedResetTypesModeEnabled
        
        resetTypes = [resetType for resetType in self.m_supportedResetTypes if self.m_resetTypeBinders.At(resetType).GetValue()]

        params.AtPut('queryFolder', queryFolder)
        params.AtPut('numberOfBuckets', numberOfBuckets)
        params.AtPut('noBucketsAfterDatePeriod', noBucketsAfterDatePeriod)
        params.AtPut('resetTypes', resetTypes)
        params.AtPut('advancedResetTypesEnabled', advancedResetTypesEnabled)
        
        return params

    def HandleCreate( self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption("Reset Fixing Date Bucket Description")
        self.m_bindings.AddLayout(layout)
        self.m_advancedResetTypesModeBtn = layout.GetControl("advancedResetTypesMode")
        self.m_advancedResetTypesModeBtn.AddCallback("Activate", OnAdvancedResetTypesClicked, self) 
        
        nbrBuckets = self.m_parameters.At('numberOfBuckets')
        if nbrBuckets == None:
            nbrBuckets = 15
        maxDatePeriod = self.m_parameters.At('noBucketsAfterDatePeriod')
        if maxDatePeriod == None:
            maxDatePeriod = '1y'
        query = self.m_parameters.At('queryFolder')
        
        selectedResetTypes = self.m_parameters.At('resetTypes')
        if selectedResetTypes == None:
            selectedResetTypes = self.m_supportedResetTypes
        for resetType in self.m_supportedResetTypes:
            self.m_resetTypeBinders[resetType].SetValue(resetType in selectedResetTypes)
            
        advancedResetTypesEnabled = self.m_parameters.At('advancedResetTypesEnabled')
        if advancedResetTypesEnabled == None:
            advancedResetTypesEnabled = False
        
        self.m_queryFolder.SetValue(query)
        self.m_numberOfBucketInput.SetValue(nbrBuckets)
        self.m_noBucketsAfterDatePeriod.SetValue(maxDatePeriod)
        self.m_advancedResetTypesModeEnabled = advancedResetTypesEnabled

        self.UpdateControls()
        self.CreateToolTip()

    def UpdateControls( self ):
    
        if self.AdvancedResetTypesModeEnabled():
            self.m_advancedResetTypesModeBtn.Label('Normal <<')
            self.m_advancedResetTypesModeBtn.ToolTip(TOOL_TIP_FOR_NORMAL_BTN)
        else:
            self.m_advancedResetTypesModeBtn.Label('Advanced >>')
            self.m_advancedResetTypesModeBtn.ToolTip(TOOL_TIP_FOR_ADVANCED_BTN)
        
        for resetType in self.m_supportedResetTypes:
            self.m_resetTypeBinders.At(resetType).Visible(self.AdvancedResetTypesModeEnabled())

    def InitControls(self):

        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        formatter = acm.FNumFormatter('myFormatter')
        formatter.NumDecimals(0)
        
        for resetType in self.m_supportedResetTypes:
            self.m_resetTypeBinders.AtPut(resetType, self.m_bindings.AddBinder(ToCamelCase(resetType), acm.GetDomain('bool')))
        
        self.m_numberOfBucketInput = self.m_bindings.AddBinder('numberOfBuckets', acm.GetDomain('int'), formatter)
        self.m_noBucketsAfterDatePeriod = self.m_bindings.AddBinder('noBucketsAfterDatePeriod', acm.GetDomain('dateperiod'))
        self.m_queryFolder = self.m_bindings.AddBinder('queryFolder', acm.GetDomain('FStoredASQLQuery'))
    
    def BuildLayoutPartsForResetTypes(self, builder):
        
        for resetType in self.m_supportedResetTypes:
            builder.  BeginHorzBox('None')
            self.       m_resetTypeBinders.At(resetType).BuildLayoutPart(builder, resetType)
            builder.  EndBox()
        
    def CreateLayout( self ):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        
        self. m_queryFolder.BuildLayoutPart(b, 'Query Folder')
        self. m_numberOfBucketInput.BuildLayoutPart(b, 'Max number of buckets')
        self. m_noBucketsAfterDatePeriod.BuildLayoutPart(b, 'No buckets after date period')
        
        b.    AddButton('advancedResetTypesMode', 'Advanced >>')
        b.    BeginVertBox('EtchedIn', 'Reset Types') 
        self.   BuildLayoutPartsForResetTypes(b)                    
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()
    
        return b
