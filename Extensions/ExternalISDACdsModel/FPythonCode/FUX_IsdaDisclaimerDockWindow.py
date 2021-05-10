
import acm
import FUxCore

class IsdaDisclaimerLayoutPanel (FUxCore.LayoutPanel):
    def __init__(self):
        self.m_underlying = None
        self.m_cdsDisclaimer = None
        self.m_cdsDisclaimerText = 'This application is based on the ISDA CDS Standard Model (version 1.8.2), \n developed and supported in collaboration with Markit Group Ltd.'

    def HandleCreate( self ):
        layout = self.SetLayout( self.CreateLayout() )
        self.m_cdsDisclaimer = layout.GetControl('cdsDisclaimer')
	self.m_cdsDisclaimer.SetData( self.m_cdsDisclaimerText )
	self.m_cdsDisclaimer.Editable( False )
        self.Owner().AddDependent(self)
        
    def CreateLayout( self):
        b = acm.FUxLayoutBuilder()
        b.  BeginVertBox();
        b.      AddDescriptionField('cdsDisclaimer', 700, 35, 700, 500)
        b.  EndBox()
        return b

def OnCDSCreate(eii):
    basicApp = eii.ExtensionObject()
    isdaDisclaimerPanel = IsdaDisclaimerLayoutPanel()
    basicApp.CreateCustomDockWindow(isdaDisclaimerPanel, 'customInsdefPane', '', 'Bottom', '', False, True, False, False)
