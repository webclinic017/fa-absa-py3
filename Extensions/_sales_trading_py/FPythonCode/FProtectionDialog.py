""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FProtectionDialog.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FProtectionDialog

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FUxCore

class ProtectionDialog(FUxCore.LayoutDialog):

    CAPTION = 'Protection'
    PROTECTION = {
        'World': {'Read': 9, 'Write': 10, 'Delete': 11},
        'Org.': {'Read': 6, 'Write': 7,  'Delete': 8},
        'Group': {'Read': 3, 'Write': 4,  'Delete': 5},
        'Owner': {'Read': 0, 'Write': 1,  'Delete': 2},
        }

    def __init__(self, businessObj, commitOnApply=False):
        self._businessObj = businessObj
        self._ownerCtrl = None
        self._rightCtrls = []
        self._commitOnApply = commitOnApply
        assert self._businessObj and self._businessObj.IsKindOf(acm.FBusinessObject)

    def PopulateOwnerCtrl(self):
        self._ownerCtrl.Populate([u for u in acm.FUser.Select(None).SortByProperty('Name')])
        self._ownerCtrl.SetData(acm.UserName())

    def PopulateProtectionCtrls(self):
        for ctrl in self._rightCtrls:
            for prot in ('Read/Write/Delete', 'Read/Write', 'Read', 'None'):
                ctrl.AddItem(prot)

    def InitOwnerControl(self):
        self.PopulateOwnerCtrl()
        self._ownerCtrl.SetData(self._businessObj.Owner())

    def RegisterRightCtrls(self, ctrl):
        if ctrl not in self._rightCtrls:
            self._rightCtrls.append(ctrl)
        return ctrl

    @staticmethod
    def GetBit(byteval, idx):
        return ((byteval & (1 << idx))!=0)

    @staticmethod
    def SetBit(idx):
        return 1 << idx

    def SetRights(self, ctrl, protection):
        level = ctrl.Label().split(' ')[0]
        data = ''.join(('%s/'%right for right in self.PROTECTION.get(level)
            if not self.GetBit(protection, self.PROTECTION[level][right])))
        ctrl.SetData(data[:-1] or 'None')

    def InitProtectionControls(self):
        self.PopulateProtectionCtrls()
        for ctrl in self._rightCtrls:
            self.SetRights(ctrl, self._businessObj.Protection())

    def RegisterControls(self, layout):
        self._ownerCtrl = layout.GetControl('owner')
        self.RegisterRightCtrls(layout.GetControl('ownerRights'))
        self.RegisterRightCtrls(layout.GetControl('groupRights'))
        self.RegisterRightCtrls(layout.GetControl('orgRights'))
        self.RegisterRightCtrls(layout.GetControl('worldRights'))

    def HandleCreate(self, dialog, layout):
        dialog.Caption(self.CAPTION)
        self.RegisterControls(layout)
        self.InitOwnerControl()
        self.InitProtectionControls()

    def Rights(self, ctrl):
        level = ctrl.Label().split(' ')[0]
        protection = 0
        for right in self.PROTECTION.get(level):
            if right not in ctrl.GetData():
                protection += self.SetBit(self.PROTECTION[level][right])
        return protection

    def HandleApply(self):
        protection = 0
        for ctrl in self._rightCtrls:
            protection += self.Rights(ctrl)
        owner = self._ownerCtrl.GetData()

        if protection != self._businessObj.Protection():
            self._businessObj.Protection(protection)
        if owner != self._businessObj.Owner():
            self._businessObj.Owner(owner)

        if self._commitOnApply and self._businessObj.IsModified():
            self._businessObj.Commit()
        return True

    def CreateLayout(self):
        # pylint: disable-msg=R0201
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn')
        b.   AddPopuplist('owner', 'Owner')
        b.   AddOption('ownerRights', 'Owner rights')
        b.   AddOption('groupRights', 'Group rights', 20)
        b.   AddOption('orgRights', 'Org. rights', 20)
        b.   AddOption('worldRights', 'World rights', 20)
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b



def ViewProtection(businessObj, shell, commitOnApply=False):
    dlg = ProtectionDialog(businessObj, commitOnApply)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

def CreateProtectionMenuItem(eii):
    isInSheet = hasattr(eii, 'ActiveSheet')
    return FunctionMappedMenuItem(eii,
        invokeFunc=lambda l: ViewProtection(l, eii.Shell(), commitOnApply=isInSheet))



class FunctionMappedMenuItem(FUxCore.MenuItem):

    def __init__(self, extObj, invokeFunc=None, enabledFunc=None,
                    validateFunc=None, intendedApplication=None, applicableFunc=None):
        self._frame = extObj
        self._invokeFunc = invokeFunc
        self._enabledFunc = enabledFunc
        self._validateFunc = validateFunc
        self._applicableFunc = applicableFunc

    def Applicable(self):
        if callable(self._applicableFunc):
            return self._applicableFunc(self._frame)
        return False

    def Enabled(self):
        if callable(self._enabledFunc):
            return self._enabledFunc(self._SelectedObject())
        return bool(self._SelectedObject())

    def Invoke(self, _eii):
        if callable(self._invokeFunc):
            self._invokeFunc(self._SelectedObject())

    def _SelectedObject(self):
        if hasattr(self._frame, 'CustomLayoutApplication'):
            obj = self._frame.CustomLayoutApplication().EditObject()
            return obj
        return None
