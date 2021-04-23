
import acm
import FUxUtils
import FUxCore

MAXROWSPERPAGE = 25

def OnPrevClicked( self, cd ):
    self.m_pageNo -= 1
    self.UpdateControls()
    
def OnNextClicked( self, cd ):
    self.m_pageNo += 1
    self.UpdateControls()

def AsSymbol( va ):
    return acm.FSymbol( va )

class BucketShiftSubDialog (FUxCore.LayoutDialog):
        
    def __init__(self, timeBuckets, shifts, labels):
        self.m_timeBuckets = timeBuckets
        self.m_shifts = shifts
        self.m_labels = labels
        self.m_pageNo = 1
        self.m_noOfPages = 1
        self.m_rowsPerPage = 0
        self.m_pageLbl = None
        self.m_prevCtrl = None
        self.m_nextCtrl = None
        self.m_okBtn = None

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_controls = []
        self.m_lblControls = []
        if self.m_noOfPages > 1:
            self.m_prevCtrl = layout.GetControl( 'prev' )
            self.m_prevCtrl.AddCallback( 'Activate', OnPrevClicked, self )
            self.m_nextCtrl = layout.GetControl( 'next' )
            self.m_nextCtrl.AddCallback( 'Activate', OnNextClicked, self )
            self.m_pageLbl = layout.GetControl( 'currPage' )
        ctrl = layout.GetControl( 'lbltb' )
        ctrl.Editable( False )
        ctrl.SetData( 'Time Buckets' )
        for idy, label in enumerate( self.m_labels ):
            ctrl = layout.GetControl( 'lbl' + str(idy) )
            ctrl.Editable( False )
            ctrl.SetData( label )
            
        for idx, tb in enumerate( self.m_timeBuckets ):
            #set labels
            ctrl = layout.GetControl( 'lbltb' + str(idx) )
            self.m_lblControls.append( ctrl )
            ctrl.Editable( False )
            ctrl.SetData( tb.Name() )
            ctrls = []
            for idy, label in enumerate( self.m_labels ):
                ctrl = layout.GetControl( 'shift' + str(idx) + str(idy) )
                ctrls.append( ctrl )
                if self.m_shifts and self.m_shifts.HasKey( AsSymbol( label ) ):
                    ctrl.SetData( self.m_shifts.At( AsSymbol( label ) ).At( tb.AsSymbol() ) )
            self.m_controls.append( ctrls )
        self.UpdateControls()

    def UpdateControls(self):
        if self.m_noOfPages > 1:
            self.m_pageLbl.SetData( "page " + str(self.m_pageNo) + " / " + str( self.m_noOfPages ) )
            self.m_prevCtrl.Enabled( self.m_pageNo > 1 )
            self.m_nextCtrl.Enabled( self.m_pageNo < self.m_noOfPages )
            visible = True
            for idx, tb in enumerate( self.m_timeBuckets ):
                visible = idx >= ( self.m_pageNo - 1 ) * self.m_rowsPerPage and idx < self.m_pageNo * self.m_rowsPerPage
                self.m_lblControls[idx].Visible( visible )
                for idy, label in enumerate( self.m_labels ):
                    self.m_controls[idx][idy].Visible( visible )
                
    def HandleApply( self ):
        if not self.m_shifts:
            self.m_shifts = acm.FDictionary()
        for label in self.m_labels:
            self.m_shifts.AtPut( AsSymbol( label ), acm.FDictionary() )
        try:
            for idx, tb in enumerate( self.m_timeBuckets ):
                for idy, label in enumerate( self.m_labels ):
                    value = self.m_controls[idx][idy].GetData() and float( self.m_controls[idx][idy].GetData() ) or 0.0
                    self.m_shifts.At( AsSymbol( label ) ).AtPut( tb.AsSymbol(), value )
        except ValueError as e:
            acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', str(e), 'OK', None, None,  'Button1', 'Button1')
            return None
        return self.m_shifts 

    def ValidateControls(self):
        ok = True
        return ok

    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        
        if self.m_timeBuckets.Size() > MAXROWSPERPAGE:
            builder.BeginHorzBox();
            builder.    AddSpace(8)
            builder.    AddButton("prev", "<", False, True);
            builder.    AddButton("next", ">", False, True);
            builder.    AddLabel("currPage", "");
            builder.EndBox();
            self.m_noOfPages = int(round( float(self.m_timeBuckets.Size()) / float(MAXROWSPERPAGE) ))
            self.m_rowsPerPage = int(round( float(self.m_timeBuckets.Size()) / float(self.m_noOfPages) ))
            
        builder.BeginHorzBox('Invisible')
        builder.        BeginVertBox('None')
        builder.                AddInput('lbltb', '', 10)
        for idx, tb in enumerate( self.m_timeBuckets ):
            builder.                AddInput('lbltb' + str(idx), '', 10)
        builder.        EndBox()
        for idy, label in enumerate( self.m_labels ):
            builder.        BeginVertBox('None')
            builder.                AddInput('lbl' + str(idy), '', 10)
            for idx, tb in enumerate( self.m_timeBuckets ):
                builder.                AddInput('shift' + str(idx) + str(idy), '', 10)
            builder.EndBox()
        builder.EndBox()
        builder.        BeginHorzBox('None')
        builder.                AddFill()
        builder.                AddButton('ok', 'OK')
        builder.                AddButton('cancel', 'Cancel')
        builder.        EndBox()
        builder.EndBox()
       
        builder.EndBox()
        return builder
