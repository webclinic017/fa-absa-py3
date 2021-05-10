""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FTimeStampsCustomDialog.py"
import acm
import FUxCore
import time
from time import strftime

class TimeStampsCustomDialog(FUxCore.LayoutDialog):

    def __init__(self, shell, fObject):

        #Main dialog
        self.m_fuxDlg = 0
        self.binder   = None
        self.shell    = shell
        self.fObject  = fObject

    def StartDialog(self):
        self.result= acm.UX().Dialogs().ShowCustomDialog(self.shell, self.CreateLayout(), self)

    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.  BeginHorzBox('Invisible')
        builder.    BeginVertBox('None')
        builder.      AddLabel('create_user_lbl', 'Created by:')
        builder.      AddLabel('create_time_lbl', 'Time of creation:')
        builder.      AddLabel('update_user_lbl', 'Updated by:')
        builder.      AddLabel('update_time_lbl', 'Time of update:')
        builder.    EndBox()
        builder.    BeginVertBox('None')
        builder.      AddInput('create_user', '', 21)
        builder.      AddInput('create_time', '', 21)
        builder.      AddInput('update_user', '', 21)
        builder.      AddInput('update_time', '', 21)
        builder.    EndBox()
        builder.  EndBox()
        builder.  BeginHorzBox('None')
        builder.    AddFill()
        builder.    AddButton('cancel', 'Close', True, False)
        builder.  EndBox()
        builder.EndBox()
        return builder

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Time Stamps')
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)
        self.binder.AddLayout(layout)

        self.create_user = layout.GetControl("create_user")
        self.create_time = layout.GetControl("create_time")
        self.update_user = layout.GetControl("update_user")
        self.update_time = layout.GetControl("update_time")

        self.UpdateControls()
        self.PopulateData()

    def UpdateControls(self):
        """set visibility of controls and action when clicked 'More >>'"""
        self.create_user.Enabled(0)
        self.create_time.Enabled(0)
        self.update_user.Enabled(0)
        self.update_time.Enabled(0)

    def PopulateData(self):
        timeStamps = self.GetTimeStamps()
        self.create_user.SetData(timeStamps[0])
        self.update_user.SetData(timeStamps[1])
        self.create_time.SetData(timeStamps[2])
        self.update_time.SetData(timeStamps[3])

    def GetTimeStamps(self):
        """returns time stamps and user info"""
        create_user = ""
        update_user = ""
        create_time = ""
        update_time = ""
        if self.fObject:
            if self.fObject.CreateUser():
                create_user = self.fObject.CreateUser().Name()
            if self.fObject.UpdateUser():
                update_user = self.fObject.UpdateUser().Name()
            if self.fObject.CreateTime():
                create_time = self.fObject.CreateTime()
                create_time = strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(create_time))
            if self.fObject.UpdateTime():
                update_time = self.fObject.UpdateTime()
                update_time = strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(update_time))
        return create_user, update_user, create_time, update_time

def StartDialog(shell, fObject):
    """sets time stamps in time stamps dialog"""
    customDlg = TimeStampsCustomDialog(shell, fObject)
    customDlg.StartDialog()
