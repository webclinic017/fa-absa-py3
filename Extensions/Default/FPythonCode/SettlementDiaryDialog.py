""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/gui/SettlementDiaryDialog.py"
import acm
import FUxCore

#---------------------------------------------------------------------------
class SettlementDiaryDialog (FUxCore.LayoutDialog):

    #---------------------------------------------------------------------------
    def __init__(self, settlement):
        self.m_fuxDlg = 0
        self.m_oldDiaryText = 0
        self.m_newDiaryText = 0

        self.m_settlement = settlement

    #---------------------------------------------------------------------------
    def HandleApply( self ):
        return self.m_newDiaryText.GetData()

    #---------------------------------------------------------------------------
    def PopulateData(self):
        self.m_oldDiaryText.SetData(self.m_settlement.Diary().TextWithUTCTimeStamp() if self.m_settlement and self.m_settlement.Diary() else '')

    #---------------------------------------------------------------------------
    def UpdateControls(self):
        self.m_oldDiaryText.Editable(False)

    #---------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Fill in diary')

        self.m_oldDiaryText = layout.GetControl("olDiaryText")
        self.m_newDiaryText = layout.GetControl("newDiaryText")

        self.PopulateData()
        self.UpdateControls()

        self.m_newDiaryText.SetFocus()

    #---------------------------------------------------------------------------
    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()

        b.  BeginVertBox('None')
        b.    AddText("olDiaryText", 200, 100, 1000, 1000)
        b.    AddText("newDiaryText", 200, 100, 1000, 1000)
        b.    BeginHorzBox()
        b.      AddFill()
        b.      AddButton('ok', '&&Save')
        b.    EndBox()
        b.  EndBox()
        return b