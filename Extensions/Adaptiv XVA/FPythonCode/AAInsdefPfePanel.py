""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAInsdefPfePanel.py"
import acm
import FUxCore

class AAInsdefPfePanel(FUxCore.LayoutPanel):
    
    def __init__(self, logic):
        self._uxIPFEResult = None
        self._uxBeforePFEResult = None
        self._uxAfterPFEResult = None
        self._uxSendRequest = None
        self._uxStatus = None
        self._logic = logic
    
    def HandleApply( self, *args ):
        return True
    
    def SetResult(self, msgDic):
        for key in list(msgDic.keys()):
            if key == 'IncPFE':    
                self._uxIPFEResult.SetData(msgDic[key])
            elif key == 'PFE':
                self._uxBeforePFEResult.SetData(msgDic[key])
            elif key == 'AfterPFE':
                self._uxAfterPFEResult.SetData(msgDic[key])
    
    def SetStatus(self, msg):
        self._uxStatus.SetData(msg)
    
    def EnableCalcButton(self, enabled):
        self._uxSendRequest.Enabled(enabled)

    def EnableGraphButton(self, enabled):
        self._uxShowGraph.Enabled(enabled)

    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        
        self._uxIPFEResult = layout.GetControl('incrementalPFE')
        self._uxIPFEResult.Editable(False)
        
        self._uxBeforePFEResult = layout.GetControl('beforePFE')
        self._uxBeforePFEResult.Editable(False)

        self._uxAfterPFEResult = layout.GetControl('afterPFE')
        self._uxAfterPFEResult.Editable(False)
        
        self._uxStatus = layout.GetControl('status')
        self._uxStatus.Editable(False)
        
        self._uxSendRequest = layout.GetControl('sendRequest')
        self._uxSendRequest.AddCallback( "Activate", self._OnSendIPFERequestClicked, None )
        
        self._uxShowGraph = layout.GetControl('showGraph')
        self._uxShowGraph.AddCallback( "Activate", self._OnShowGraphClicked, None )
        self._uxShowGraph.Enabled(False)
         
        self._logic._InitDependents()
    
    def _OnSendIPFERequestClicked(self, *args):
        self._logic._CreateTask()
        
    def _OnShowGraphClicked(self, *args):
        self._logic._showGraph()
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('Invisible')
        b.  BeginHorzBox()
        b.    AddInput('incrementalPFE', 'Inc PFE')
        b.    AddButton('sendRequest', 'Calc')
        b.    AddButton('showGraph', 'Graph')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('beforePFE', 'Before PFE')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('afterPFE', 'After PFE')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('status', 'Status')
        b.  EndBox()
        b.EndBox()
        return b
