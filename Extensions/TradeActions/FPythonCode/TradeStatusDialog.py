import acm
import FUxCore

class TradeStatusDialog( FUxCore.LayoutDialog ):
    def __init__( self, superset, initialSet=None):
        self.initialSet = initialSet if initialSet else set()
        self.superset = superset
        self.checkboxes = {}
                
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Trade Status Selection')
        self.m_layout = layout
                        
        for e in self.superset:
            box = layout.GetControl(self.checkboxName(e))
            box.Checked(e in self.initialSet)
                
    def HandleApply(self):
        return self.Selection()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()

        b. BeginHorzBox()
        b.  BeginVertBox('Invisible')

        for e in self.superset:
            b.AddCheckbox(self.checkboxName(e), e)
            
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b.  EndBox()
        b. EndBox()

        b. AddSpace(3)
        b.EndBox()
        
        return b
    
    def checkboxName(self, e):
        if e not in self.checkboxes:
            name = 'checkbox' + str(len(self.checkboxes))
            self.checkboxes[e] = name
        
        return self.checkboxes[e]    
    
    def IsSelected(self, e):
        checkbox = self.m_layout.GetControl(self.checkboxName(e))
        return checkbox.Checked()
    
    def Selection(self):
        res = set()
        
        for e in self.superset:
            if self.IsSelected(e):
                res.add(e)
        
        return res
