import acm
import FUxCore

GREENCOLOR = acm.UX().Colors().Create(30, 170, 30)
BLUECOLOR = acm.UX().Colors().Create(222, 235, 255)

class UpdateZarPrimeSpread(FUxCore.LayoutDialog):
    """The GUI-managing class."""
    
    def __init__(self, underlying):
        # prepare the layout
        self.underlying = underlying
        self.CreateLayout()
      
    def _update_spread(self, *args):  
        spread = self.mm_spread.GetData()
        underlying = self.mm_underlying.GetData()
        textobj = acm.FCustomTextObject[underlying]
        msg = 'Failed to update spread'
        if not textobj:
            textobj = acm.FCustomTextObject()
            textobj.Name(underlying)
            textobj.RegisterInStorage()
        textobj.Text(spread)
        textobj.Commit()
        msg = 'Succesfully updated %s spread to %s'% (textobj.Name(), str(spread))
        print '*** ', msg
        self.mm_spread_result.Populate([msg])  

    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''
        self.fux_dialog = dlg
        self.fux_dialog.Caption('Update Access Note Spread')             
        self.mm_spread = layout.GetControl('spread')
        self.mm_underlying = layout.GetControl('underlying') 
        underlying = acm.FChoiceList['AccessNoteSpreadUnderlyingIndex']
        underlying_indices = [i.Name() for i in underlying.Choices()]
        self.mm_underlying.Populate(underlying_indices)
        self.mm_spread_update = layout.GetControl("update_spread")
        self.mm_spread_update.AddCallback("Activate", self._update_spread, None)
        self.mm_spread_result = layout.GetControl('new_spread')
        self.mm_spread_result.ShowGridLines()
        self.mm_spread_result.ShowColumnHeaders()
        self.mm_spread_result.EnableMultiSelect(True)
        self.mm_spread_result.AddColumn('Update Status')        
        self.mm_spread_result.Editable(True)
        self.mm_spread_result.SetColor("Foreground", BLUECOLOR)
        self.mm_spread_result.SetColor("Text", GREENCOLOR)
        self.mm_spread_result.SetStandardFont("Bold")
            
    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""
        b = acm.FUxLayoutBuilder()
        b. BeginVertBox('None')        
        b. BeginVertBox('EtchedIn', label='Residual')    
        b. AddOption('underlying', 'Underlying Index', 30, 30)
        b. AddInput('spread', 'Spread over Underlying', 30, 30)
        b. EndBox()      
        b. AddSpace(10)       
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('update_spread', 'Update')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.  BeginVertBox('EtchedIn', 'Result Console')
        b.    AddList('new_spread', 5, -1, 75, -1)
        b.  EndBox()
        b.EndBox()
        self.layout = b


def start_dialog(eii, *rest):
    """Starts the dialog for comment adding."""
    
    underlying = eii.ExtensionObject().CurrentObject()    
    
    shell = eii.ExtensionObject().Shell()
    customDlg = UpdateZarPrimeSpread(underlying)
    acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                 customDlg.layout,
                                                 customDlg)
