import acm
import FUxCore
import time


def Show(shell, caption, searchableItems, updateSearchItemCB):
    customDlg = CreateSearchableItemsProgressDialog(caption, searchableItems, updateSearchItemCB)

    builder = customDlg.CreateLayout()
    
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
    
class CreateSearchableItemsProgressDialog(FUxCore.LayoutDialog):
    def __init__(self, caption, searchableItems, updateSearchItemCB):
        self.m_caption = caption
        self.m_cancelButton = 0
        self.m_progressCtrl = 0
        self.m_updateSearchItemCB = updateSearchItemCB
        self.m_searchableItems = searchableItems
        
        self.m_currentPosition = 0
        self.m_numberOfNodes = len(self.m_searchableItems)
        self.m_delta = self.m_numberOfNodes / 100

    def OnTimer(self, ud):

        start = time.time()

        while (time.time() - start) < 0.5 and self.m_currentPosition < self.m_numberOfNodes:
            self.m_updateSearchItemCB(self.m_searchableItems[self.m_currentPosition])
            self.m_currentPosition += 1

        self.UpdateControls()
    
    def UpdateControls(self):
        if self.m_delta:
            self.m_progressCtrl.SetData(self.m_currentPosition / self.m_delta + 1)
        else :
            self.m_progressCtrl.SetData(100)

        if self.m_currentPosition >= self.m_numberOfNodes :
            self.m_fuxDlg.CloseDialogOK()
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)

        self.m_fuxDlg.RegisterTimer( self.OnTimer, 200) 

        self.m_cancelButton = layout.GetControl("stop")
        self.m_cancelButton.AddCallback('Activate', self.OnStopButton, None)
        self.m_progressCtrl = layout.GetControl("creationProgress")
        
        self.UpdateControls()

    def OnStopButton(self, ud, cd) :
        self.m_fuxDlg.CloseDialogCancel()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddProgress('creationProgress', 300, 12, -1, 12)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('stop', 'Cancel')
        b.      AddFill()
        b.  EndBox()
        b.EndBox()
        return b
    




