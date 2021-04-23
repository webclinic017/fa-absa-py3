

import acm
import FUxCore

def ReallyStartDialog(shell, object):
    builder           = CreateLayout()
    customDlg         = myCustomDialog(object)
    
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg)

def StartDialog(eii):
    shell  = eii.ExtensionObject().Shell()
    object  = eii.ExtensionObject().CurrentObject()
    ReallyStartDialog(shell, object);

def OnSaveClicked(self, cd):
    volStruct    = acm.FVolatilityStructure[self.m_parentObject.Name()]
    volStructClone = volStruct.Clone()
    originalKappa = volStructClone.Kappa()
    try:
        kappa  = float(self.m_kappa.GetData())
        if kappa < 0.0:
            raise Exception('Kappa: The kappa value must be greater or equal to zero, reverting to original value.')
        volStructClone.Kappa(kappa)
        volStruct.Apply(volStructClone)
        volStruct.Commit()
    except ValueError:
        print ('Kappa: Wrong format for kappa, reverting to original value.')
        self.m_kappa.SetData(originalKappa)
    except Exception as e:
        print (e)
        self.m_kappa.SetData(originalKappa)
          
class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self, object):
        self.m_fuxDlg       = 0
        self.m_kappa       = 0.3
        self.m_parentObject = object
    
    def PopulateData(self):
        
        self.m_kappa.SetData(self.m_parentObject.Kappa())  
        self.m_kappa.Visible(1) 
      
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption("Hull White Utils")

        self.m_saveBtn = layout.GetControl("save")
                
        self.m_kappa       = layout.GetControl("kappa")        
        
        self.m_saveBtn.AddCallback( "Activate", OnSaveClicked, self )
        
        self.PopulateData()
        
def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')   
    b.  BeginVertBox('Invisible')
    b.    AddInput('kappa', 'Kappa' )
    b.  EndBox()
    b.  BeginHorzBox('Invisible')
    b.    AddFill()
    b.    AddButton('save', 'Save')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    
    return b
