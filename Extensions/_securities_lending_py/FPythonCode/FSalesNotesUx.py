""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSalesNotesUx.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesNotesUx

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm, FUxCore
import FSecLendUtils


class SalesActivityDiaryPane():

    GREY = None

    def __init__(self, security):
        self.diaryCtrl = None
        self.historyCtrl = None
        self.diary = None
        self.getDiary(security)

    def getDiary(self, m_security):
        self.m_master = FSecLendUtils.GetMasterSecurityLoan(m_security)
        diary = acm.FSalesActivityDiary['SalesNotes_{0}'.format(self.m_master.Oid())]
        if diary:
            self.diary = diary.StorageImage()

    def CreateLayout(self, b):
        b.  BeginVertBox('None')
        b.    AddText('history', 350, 250)
        b.    AddText('diary', 350, 125)
        b.  EndBox()
        return b

    def HandleCreate(self, layout):
        self.historyCtrl = layout.GetControl('history')
        self.historyCtrl.Editable(False)
        self.historyCtrl.SetColor('BackgroundReadonly', self.Grey())
        self.diaryCtrl = layout.GetControl('diary')
        self.diaryCtrl.Editable(True)
        self.diaryCtrl.SetFocus()
        self.UpdateDiary()

    def UpdateDiary(self):
        self.ClearDiary()
        if self.diary and self.diary.Text() and self.historyCtrl:
            self.historyCtrl.SetData(self.diary.Text())

    def SetNewDiary(self, diaryText):
        if self.diary is None:
            self.diary = acm.FSalesActivityDiary()
            self.diary.Name('SalesNotes_{0}'.format(self.m_master.Oid()))
        self.diary.Text(diaryText)
        self.diary.Commit()

    def Header(self):
        timeNow = acm.Time.RealTimeNow()
        return '{0} {1}\n'.format('[' + acm.UserName() + ']', timeNow[:-4])

    def AddToDiary(self):
        newEntry = ''.join((
            self.Header(),
            self.diaryCtrl.GetData(), 2*'\n',
            self.historyCtrl.GetData()))
        return newEntry

    def OnDiaryChanged(self, cd, params):
        self.SetNewDiary(self.AddToDiary())

    def OnHistoryChanged(self, cd, params):
        self.SetNewDiary(self.historyCtrl.GetData())

    def ClearDiary(self):
        try:
            self.historyCtrl.Clear()
            self.diaryCtrl.Clear()
        except AttributeError:
            pass

    def Save(self):
        if self.diaryCtrl.GetData():
            self.SetNewDiary(self.AddToDiary())
            self.UpdateDiary()

    @classmethod
    def Grey(cls):
        if cls.GREY is None:
            cls.GREY = acm.GetDefaultContext().GetExtension(
                'FColor', 'FObject', 'BkgEvalClone').Value()
        return cls.GREY


class FSalesNotesUx(FUxCore.LayoutDialog):

    def __init__(self, security, eii):
        self.diaryPane = None
        self.m_security = security
        self.m_SaveLoans = None
        self.m_SaveCloseLoans = None
        self.m_fuxDlg = None
        self.eii = eii
        self.diaryPane = SalesActivityDiaryPane(security)

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Sales Notes:  {}'.format(self.m_security.Name()))
        self.m_SaveLoans = layout.GetControl('Save')
        self.m_SaveLoans.AddCallback('Activate', self.OnSaveLoansButtonClicked, self)
        self.m_SaveCloseLoans = layout.GetControl('SaveClose')
        self.m_SaveCloseLoans.AddCallback('Activate', self.OnSaveCloseLoansButtonClicked, self)
        self.diaryPane.HandleCreate(layout)

    def OnSaveLoansButtonClicked(self, *args):
        self.diaryPane.Save()
        cell = self.eii.Parameter('sheet').Selection().SelectedCell()

    def OnSaveCloseLoansButtonClicked(self, *args):
        self.diaryPane.Save()
        self.m_fuxDlg.CloseDialogOK()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        self.diaryPane.CreateLayout(b)
        b.BeginHorzBox('None')
        b.AddSpace(10)
        b.AddFill()
        b.AddButton('SaveClose', 'Save and Close')
        b.AddButton('Save', 'Save')
        b.AddButton('cancel', 'Close')
        b.EndBox()
        b.EndBox()
        return b


def CreateFSalesNotesUxInstance(eii, security):
    dlg = FSalesNotesUx(security, eii)
    acm.UX().Dialogs().ShowCustomDialog(eii.ExtensionObject().Shell(), dlg.CreateLayout(), dlg)