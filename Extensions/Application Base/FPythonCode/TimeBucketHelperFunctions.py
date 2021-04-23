
import acm
import FUxCore

def GetDefaultCalendar():
    try:
        calendar = acm.UsedValuationParameters().AccountingCurrency().Calendar()
    except Exception:
        calendar = acm.FCalendar['Target']
    return calendar

def CreateIMMOrCDSTimeBucketDefinitions(startDate, numOfBuckets, businessDayMethod):
    buckets = acm.FArray()
    calendar = GetDefaultCalendar()
    firstDayInQ = startDate
    
    i = 0
    while i < numOfBuckets:
        firstDayInQ = acm.Time().FirstDayOfQuarter( firstDayInQ )
        modifiedDate = calendar.ModifyDate( None, None, firstDayInQ, businessDayMethod )
        if acm.Time.DateDifference(modifiedDate, startDate) >= 0:
            bucketDef = acm.FFixedDateTimeBucketDefinition()
            bucketDef.FixedDate( modifiedDate )
            bucketDef.Adjust( False )
            buckets.Add(bucketDef)
            i = i + 1
        firstDayInQ = acm.Time().DateAddDelta(firstDayInQ, 0, 3, 0)

    if buckets.Size():
        return buckets
    else:
        return None

def CreateMonthlyIMMTimeBucketDefinitions(startDate, numOfBuckets, businessDayMethod):
    buckets = acm.FArray()
    calendar = GetDefaultCalendar()
    firstDayInM = startDate
    
    i = 0
    while i < numOfBuckets:
        firstDayInM = acm.Time().FirstDayOfMonth( firstDayInM )
        modifiedDate = calendar.ModifyDate( None, None, firstDayInM, businessDayMethod )
        if acm.Time.DateDifference(modifiedDate, startDate) >= 0:
            bucketDef = acm.FFixedDateTimeBucketDefinition()
            bucketDef.FixedDate( modifiedDate )
            bucketDef.Adjust( False )
            buckets.Add(bucketDef)
            i = i + 1
        firstDayInM = acm.Time().DateAddDelta(firstDayInM, 0, 1, 0)

    if buckets.Size():
        return buckets
    else:
        return None

def ShowCreateBucketsFromCDSOrIMMDialog(shell, parameters, caption) :
    dlg = CDSOrIMMDialog(parameters, caption)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg )    

class CDSOrIMMDialog (FUxCore.LayoutDialog):

    def __init__(self, parameters, caption):

        self.m_okBtn = 0
        self.m_numberOfBucketInput = 0
        self.m_bindings = 0
        self.m_parameters = parameters.At('initialData')
        self.m_caption = caption
        self.InitControls()

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass

    

    def HandleApply( self ):

        params = acm.FDictionary()
        number = self.m_numberOfBucketInput.GetValue()
        number = int(number)
        
        params.AtPut('buckets', number)
        
        return params

    def HandleCreate( self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_bindings.AddLayout(layout)

        if self.m_parameters.Size() > 0 :
            
            self.m_numberOfBucketInput.SetValue(self.m_parameters.At('buckets'))
            
        self.UpdateControls()

    def UpdateControls( self ):
        pass

    def InitControls(self):

        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        formatter = acm.FNumFormatter('myFormatter')
        formatter.NumDecimals(0)
        self.m_numberOfBucketInput = self.m_bindings.AddBinder('numberOfBucketInput', acm.GetDomain('int'), formatter)
        
    def CreateLayout( self ):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        
        self.m_numberOfBucketInput.BuildLayoutPart(b, 'Number of buckets')
        
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()
        

        return b
