
import acm
import FUxUtils
import FUxCore

from BucketShiftSubDialog import BucketShiftSubDialog

def GetCriteriaTopOnly( parameters ):
    if parameters.HasKey( AsSymbol( 'topOnly' ) ):
        return parameters[ AsSymbol( 'topOnly' ) ]
    return False
    
def GetCriteria( parameters ):
    if parameters[ AsSymbol( 'Criteria' ) ]:
        return parameters[ AsSymbol( 'Criteria' ) ].Query()
    return acm.FObject

def GetNiceName( name, parameters ):
    displayName = name
    if parameters[ AsSymbol( 'Criteria' ) ]:
        displayName += ' (' + parameters[ AsSymbol( 'Criteria' ) ].Name() +  ')'
    return displayName

def AsSymbol( va ):
    return acm.FSymbol( va )

def OnShiftsClicked( self, cd ):
    tb = self.GetParameter( 'Time Buckets' )
    shifts = self.GetParameter( 'Shifts' )
    customDlg = BucketShiftSubDialog( tb, shifts, self.ShiftLabels() )
    res = acm.UX().Dialogs().ShowCustomDialogModal( self.m_fuxDlg.Shell(), customDlg.CreateLayout(), customDlg ) 
    if res:
        self.AddParameter( 'Shifts', res )

def OnCriteriaButtonClicked( self, cd ):
    crit = acm.UX().Dialogs().SelectStoredASQLQuery( self.m_fuxDlg.Shell(), self.CriteriaClass(), self.GetParameter('Criteria'))
    if crit:
        self.AddParameter('Criteria', crit)
        self.m_criteriaText.SetData( crit )
    self.UpdateControls()
    
def OnTimeBucketsClicked(self, cd):
    timeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_fuxDlg.Shell(), self.GetParameter('Stored Time Buckets'))
    if timeBuckets:
        self.OnTimeBucketsSelected( timeBuckets )
        self.AddParameter('Stored Time Buckets', timeBuckets)
        self.AddParameter('Time Buckets', timeBuckets.TimeBuckets())
        self.m_timeBucketsText.SetData( timeBuckets.Name() )
    self.UpdateControls()
     
class BucketShiftBaseDialog (FUxCore.LayoutDialog):

    # Implemented in subclasses
    def ShiftLabels(self):
        return None

    def CriteriaClass( self ):
        return None
        
    def CreateToolTip(self):
        timeBucketsToolTip = 'Define the time buckets for which the shifts should be applied.'
        self.m_timeBucketsText.ToolTip( timeBucketsToolTip )
        self.m_timeBucketsBtn.ToolTip( timeBucketsToolTip )
        self.m_shiftsBtn.ToolTip('View/edit the shifts')        

    def OnTimeBucketsSelected( self, timeBuckets ):
        oldStoredTb = self.GetParameter( 'Stored Time Buckets' )
        if oldStoredTb != timeBuckets:
            self.AddParameter( 'Shifts', None )

    def __init__(self):
        self.m_parameters = None
        self.m_timeBucketsBtn = None
        self.m_timeBucketsText = None
        self.m_criteriaBtn = None
        self.m_criteriaText = None
        self.m_shiftsBtn = None
        self.m_okBtn = None

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg       
        self.m_timeBucketsBtn = layout.GetControl( "timeBuckets" )
        self.m_timeBucketsText = layout.GetControl( "timeBucketsText" )
        stb = self.GetParameter('Stored Time Buckets')
        self.m_timeBucketsText.SetData( stb and stb.Name() or "")
        self.m_timeBucketsBtn.AddCallback( "Activate", OnTimeBucketsClicked, self )
        self.m_timeBucketsText.Editable( False )
        if self.CriteriaClass():
            self.m_topOnlyCtrl = layout.GetControl( "topOnly" )
            topOnly = self.GetParameter( 'topOnly' )
            self.m_topOnlyCtrl.Checked( topOnly )
            self.m_criteriaBtn = layout.GetControl( "criteria" )
            self.m_criteriaText = layout.GetControl( "criteriaText" )
            criteria = self.GetParameter( 'Criteria' )
            self.m_criteriaText.SetData( criteria or "" )
            self.m_criteriaBtn.AddCallback( "Activate", OnCriteriaButtonClicked, self )
            self.m_criteriaText.Editable( False )
        self.m_shiftsBtn = layout.GetControl( "shifts" )
        self.m_shiftsBtn.AddCallback( "Activate", OnShiftsClicked, self )
        self.m_okBtn = layout.GetControl("ok")
        self.UpdateControls()
        self.CreateToolTip()

    def UpdateControls(self):
        self.m_timeBucketsText.Visible( True )
        self.m_timeBucketsBtn.Visible( True )
        if self.GetParameter('Time Buckets'):
            self.m_okBtn.Enabled(True)
            self.m_shiftsBtn.Enabled( True )
        else:
            self.m_okBtn.Enabled(False)
            self.m_shiftsBtn.Enabled( False )

    def HandleApply( self ):
        if self.ValidateControls():
            if self.CriteriaClass():
                self.AddParameter( 'topOnly', self.m_topOnlyCtrl.Checked() )
            return self.m_parameters;
        return None

    def ValidateControls(self):
        return True

    def AddParameters(self, initData):
        self.m_parameters = initData
        
    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.BeginVertBox('Invisible')
        builder.        BeginHorzBox('None')
        builder.                AddInput('timeBucketsText', 'Time Buckets:', 20, -1, 40, "Default", False)
        builder.                AddButton('timeBuckets', '...', False, True)
        builder.        EndBox()
        self.CreateLayoutImpl( builder )
        builder.        BeginHorzBox('None')
        builder.                AddFill()
        builder.                AddButton('shifts', 'Shifts')
        builder.        EndBox()
        builder.EndBox()
        if self.CriteriaClass():
            builder.BeginVertBox('EtchedIn', 'Filter')
            builder.    AddCheckbox('topOnly', "Top Only")
            builder.    BeginHorzBox('None')
            builder.        AddInput('criteriaText', 'Query:', 20, -1, 49, "Default", False)
            builder.        AddButton('criteria', '...', False, True)
            builder.    EndBox()
            builder.EndBox()
        builder.        AddSpace(5)
        builder.        BeginHorzBox('None')
        builder.                AddFill()
        builder.                AddButton('ok', 'OK')
        builder.                AddButton('cancel', 'Cancel')
        builder.        EndBox()
        builder.EndBox()
        return builder
       
    def AddParameter(self, key, value):
        if not self.m_parameters:
            self.m_parameters = acm.FDictionary()
        self.m_parameters.AtPut( AsSymbol( key ), value )

    def GetParameter(self, key):
        if self.m_parameters and self.m_parameters.HasKey( AsSymbol( key ) ):
            return self.m_parameters.At( AsSymbol( key ) )
        return None
