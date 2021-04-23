""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FProtectionCustomDialog.py"
import acm
import FUxCore
import FPriceLinkSpecificationUtils as Utils

class ProtectionCustomDialog(FUxCore.LayoutDialog):

    def __init__(self, shell, owner, protection):

        #Main dialog
        self.m_fuxDlg = 0
        self.binder = None
        self.shell = shell
        self.owner = owner
        self.protection = protection

    def StartDialog(self):
        self.result= acm.UX().Dialogs().ShowCustomDialogModal(self.shell, self.CreateLayout(), self)

    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox('None')
        builder.  BeginVertBox('Invisible')
        builder.    AddOption('owner', 'Owner', 25, -1, 'Default')
        builder.    AddOption('owner_rights', 'Owner rights', 25, -1, 'Default')
        builder.    AddOption('group_rights', 'Group rights', 25, -1, 'Default')
        builder.    AddOption('org_rights', 'Org. rights', 25, -1, 'Default')
        builder.    AddOption('world_rights', 'World rights', 25, -1, 'Default')
        builder.  EndBox()
        builder.  BeginHorzBox('None')
        builder.    AddFill()
        builder.    AddButton('ok', 'OK', True, False)
        builder.  EndBox()
        builder.EndBox()

        return builder

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Protection')
        self.binder = acm.FUxDataBindings()
        self.binder.AddDependent(self)
        self.binder.AddLayout(layout)

        self.owner_ctrl =  layout.GetControl("owner")
        self.owner_rights =  layout.GetControl("owner_rights")
        self.group_rights =  layout.GetControl("group_rights")
        self.org_rights =  layout.GetControl("org_rights")
        self.world_rights =  layout.GetControl("world_rights")

        self.PopulateData()

    def PopulateData(self):
        """populates the default data in GUI fields"""
        # set focus on the owner field
        self.owner_ctrl.Populate(acm.FUser.Select(''))
        for rights in ["Read/Write/Delete", "Read/Write", "Read", "None"]:
            self.owner_rights.AddItem(rights)
            self.group_rights.AddItem(rights)
            self.org_rights.AddItem(rights)
            self.world_rights.AddItem(rights)

        self.DefaultData()

    def DefaultData(self):
        """Provide default data in GUI"""
        params = self.FormatProtection()
        self.owner_ctrl.SetData(self.owner)
        self.owner_rights.SetData(params[0])
        self.group_rights.SetData(params[1])
        self.org_rights.SetData(params[2])
        self.world_rights.SetData(params[3])

    def FormatProtection(self):
        """returns owner, group, organisation and world rights"""
        prot_params_list = []
        if self.protection or self.protection == 0:
            world_rt_lst = []
            org_rt_lst = []
            group_rt_lst = []
            owner_rt_lst = []
            pLis = ["Read ", "Write ", "Delete "]
            gLis = ["Owner: ", "Group: ", "Org: ", "World: "]
            prot=gLis[0]
            level=""
            bit = 1
            for n in range(12):
                if level != gLis[n/4]:
                    level = gLis[n/4]
                if n and not (n)%3:
                    prot += gLis[n/4+1]
                if not bit<<n & self.protection:
                    prot += pLis[n%3]

            world_rt_lst = prot.rsplit("World: ")
            org_rt_lst = world_rt_lst[0].rsplit("Org: ")
            group_rt_lst = org_rt_lst[0].rsplit("Group: ")
            owner_rt_lst = group_rt_lst[0].rsplit("Owner: ")
            owner_rts = self.return_rights(owner_rt_lst[1])
            group_rts = self.return_rights(group_rt_lst[1])
            org_rts = self.return_rights(org_rt_lst[1])
            world_rts = self.return_rights(world_rt_lst[1])

        return owner_rts, group_rts, org_rts, world_rts

    def return_rights(self, val):
        """return rights in proper format"""
        if not val:
            return "None"
        return val.replace(' ', "/").rstrip("/")

    def HandleApply(self):
        try:
            self.owner = self.owner_ctrl.GetData()
            self.protection = self.GetProtection()
            return 0
        except ValueError as e:
            acm.UX().Dialogs().MessageBox(self.shell, 'Error', str(e), 'OK', None, None, 'Button1', 'Button2')


    def GetProtection(self):
        """return a binary string based on Protection Parameters values"""
        self.owner_rt_pd = self.owner_rights.GetData()
        self.group_rt_pd = self.group_rights.GetData()
        self.org_rt_pd = self.org_rights.GetData()
        self.world_rt_pd = self.world_rights.GetData()

        rights_dict={"Read/Write/Delete":"000",
                    "Read/Write":"100",
                    "Read":"110",
                    "None":"111"}
        binary = ""
        pLis = ["Delete", "Write", "Read"]
        prev_rts = ""
        for rts in [self.world_rt_pd, self.org_rt_pd, self.group_rt_pd, self.owner_rt_pd]:
            if prev_rts:
                if rights_dict[rts] > rights_dict[prev_rts]:
                    raise ValueError('Please select valid Protection rights')
            binary += rights_dict[rts]
            prev_rts = rts

        return Utils.BinaryToDecimal(binary)

def StartDialog(shell, owner, protection):
    """sets protection parameters in protection dialog"""
    Dlg = ProtectionCustomDialog(shell, owner, protection)
    Dlg.StartDialog()
    return Dlg.owner, Dlg.protection