""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FUpdateExportBP.py"
import acm
import FUxCore
import FChangeTradeStatus

def ButtonClicked(self, cd ):
    if isinstance(self._object.CurrentObject(), type(acm.FTrade())):
        trade = self._object.CurrentObject()
        change = FChangeTradeStatus.FChangeCurrentState(trade, trade.Status())
        change.Execute()


class CustomInsdefLayoutPanel (FUxCore.LayoutPanel):
    def __init__(self, object):
        self._object = object
        self._transitionbtn = None

    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        self._transitionbtn = layout.GetControl('Amend')
        self._transitionbtn.AddCallback( "Activate", ButtonClicked, self )
    
    def HandleCancel(self):
        return 1
        
    def CreateLayout( self):
        b = acm.FUxLayoutBuilder()
        b.  BeginHorzBox();
        b.    AddButton('Amend', 'Update Export BP', False, True)
        b.    AddFill()
        b.  EndBox()
        return b


def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    myPanel = CustomInsdefLayoutPanel(basicApp)
    basicApp.CreateCustomDockWindow(myPanel, 'UpdateExportBPPane', 'Trade State Transition', 'Bottom')