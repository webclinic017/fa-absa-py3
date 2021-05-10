import acm
import at
import FUxCore

YC_UPDATE_FREQUENCY = "UpdateFrequency"
YC_OWNER = "CurveOwner"

class FUxYCOwnerDialog(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, curve):
        # setup the data
        self.curve = curve
        # prepare the layout
        self.CreateLayout()


    def HandleApply(self):
        # runs when "ok" is clicked

        updateFrequency = self.fux_updateFrequency.GetData()
        curveOwner = self.fux_curveOwner.GetData()
        if self.curve:
            at.addInfo.save_or_delete(self.curve, YC_UPDATE_FREQUENCY, updateFrequency)
            at.addInfo.save_or_delete(self.curve, YC_OWNER, curveOwner)
        # return None => dialog stays open
        # return anything else => dialog closes
        return True
        
    def HandleCreate(self, dlg, layout):
        # runs when the gui is being created
        self.fux_dialog = dlg
        self.fux_dialog.Caption('Yield Curve Ownership')
        self.fux_updateFrequency = layout.GetControl('updateFrequency')
        self.fux_curveOwner = layout.GetControl('curveOwner')

        choiceList = at.choiceList.get('YCUpdateFrequency')
        choices = [c.Name() for c in choiceList.Choices()]
        choices.append('')        
        for choice in sorted(choices):
            self.fux_updateFrequency.AddItem(choice)  
        if self.curve:      
            self.fux_updateFrequency.SetData(at.addInfo.get_value(self.curve, YC_UPDATE_FREQUENCY))
        
        choiceList = at.choiceList.get('YCOwner')
        choices = [c.Name() for c in choiceList.Choices()]
        choices.append('')
        for choice in sorted(choices):
            self.fux_curveOwner.AddItem(choice)
        if self.curve:
            self.fux_curveOwner.SetData(at.addInfo.get_value(self.curve, YC_OWNER))


    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""
        curve_name= ""
        if self.curve:
            curve_name = self.curve.Name()
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', 'Yield Curve Ownership')
        b.AddSpace(5)
        b. BeginVertBox('EtchedIn', label=curve_name)
        b. AddOption('updateFrequency', 'Update Frequency:', 30, 30)
        b. AddSpace(10)
        b. AddOption('curveOwner', 'Curve Owner:', 30, 30)
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'OK')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b. EndBox()
        b.AddSpace(5)
        b.EndBox()
        self.layout = b

def StartDialog(eii, *rest):
    """Starts the dialog for ownership adding."""
    shell = eii.Parameter('shell')
    customDlg = FUxYCOwnerDialog(eii.ExtensionObject().CurrentObject())
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.layout, customDlg)
