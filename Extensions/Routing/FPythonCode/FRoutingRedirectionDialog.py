from __future__ import print_function
import acm
import FUxCore

def GroupRedirections(user):
    from itertools import groupby
    
    user_rr = acm.FRoutingRedirection.Select('fromUser = %d' % user.Oid())

    keyf = lambda x: (x.FromPortfolio(), x.FromAcquirer())
    user_rr = sorted(user_rr, key = keyf)
    grouped = groupby(user_rr, keyf)
    
    ut = lambda x: x.UpdateTime()

    return dict([k, sorted(list(g), key = ut, reverse = True)] for k, g in grouped)

def OnCheckboxClicked(self, cd):
    self.m_applyBtn.Enabled(True)
    self.UpdateControls()

def OnAllCheckboxClicked(self, cd):
    self.m_applyBtn.Enabled(True)
    for name, ctrl in self.m_RedirectionEnabledMap.iteritems():
        ctrl.Checked(self.m_allCheckbox.Checked())
        
    self.UpdateControls()

class RoutingRedirectionDialog(FUxCore.LayoutDialog):
    def __init__(self, redirections, shell):
        self.m_bindings = None
        self.m_Redirections = redirections
        self.m_RedirectionCtrlMap = {}    
        self.m_RedirectionControls = {}
        self.m_RedirectionEnabledMap = {}
        self.m_okBtn = None
        self.m_applyBtn = None
        self.m_allCheckbox = None
        self.m_shell = shell

    def ToCtrlName(self, prf_acq_tuple):
        return 'ctrl_%d_%d' % (prf_acq_tuple[0].Oid(), prf_acq_tuple[1].Oid())
    
    def ToLabel(self, prf_acq_tuple):
        return '%s / %s' % (prf_acq_tuple[0].Name(), prf_acq_tuple[1].Name())
    
    def ToOption(self, rr):
        return acm.FSymbol('%s / %s' % (rr.ToPortfolio().Name(), rr.ToAcquirer().Name()))

    
    def PrepareToPersist(self):
        to_persist = []
        for name, ctrl in self.m_RedirectionEnabledMap.iteritems():
            # For a given named ctrl, this maps the visible options to the underlying instance.
            # Each control holds one option <-> instance map.
            option_map = self.m_RedirectionCtrlMap[name]
            # This is the selected, visible option (string)
            combobox = self.m_RedirectionControls[name]
            selected = combobox.GetData()

            # Disable all 
            for rr in option_map.values():
                rr.Status('Disabled')
            
            # Then enable the selected one, if the corresponding checkbox is checked
            if ctrl.Checked() and selected and option_map.has_key(selected):
                rr = option_map[selected]
                rr.Status('Enabled')
                    
            to_persist.extend(option_map.values())
            
        return to_persist
    
    def HandleApply(self):
        to_persist = self.PrepareToPersist()

        if to_persist:
            acm.BeginTransaction()
            try:
                for rr in to_persist:
                    rr.Commit()
                acm.CommitTransaction()
            except Exception as e:
                print ('dir(e)', dir(e))
                print ('e.message()', e.message)
                acm.AbortTransaction()
                acm.UX().Dialogs().MessageBox(self.m_shell,# Shell
                                              'Error',     # Dialog Type
                                              str(e),   # Message
                                              'OK',        # Button 1 Label
                                              '',          # Button 2 Label
                                              '',          # Button 3 Label
                                              'Button1',   # Default Btn
                                              0)           # Cancel Btn
                raise
        
        self.m_applyBtn.Enabled(False)
        return 0
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        pass
    
    def UpdateControls(self):
        all_checked = True
        for name, ctrl in self.m_RedirectionEnabledMap.iteritems():
            self.m_RedirectionControls[name].Enabled(not ctrl.Checked())
            if not ctrl.Checked():
                all_checked = False
                
        if self.m_allCheckbox:
            self.m_allCheckbox.Checked(all_checked)
        
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Routing Redirection' )
        self.m_okBtn = layout.GetControl('ok')
        
        self.m_applyBtn = layout.GetControl('apply')
        self.m_applyBtn.Enabled(False)

        try:
            self.m_allCheckbox = layout.GetControl('allCb')
            self.m_allCheckbox.AddCallback('Activate', OnAllCheckboxClicked, self)
        except:
            # Not visible if there's only one selection to be made
            pass
        
        for k, redirections in self.m_Redirections.iteritems():
            ctrl_name = self.ToCtrlName(k)
            combobox = layout.GetControl(ctrl_name)
            
            self.m_RedirectionControls[ctrl_name] = combobox
            self.m_RedirectionCtrlMap[ctrl_name] = {}
            
            options = []
            selected = None
            for redirection in redirections:
                option = self.ToOption(redirection)
                self.m_RedirectionCtrlMap[ctrl_name][option] = redirection
                options.append(option)

                if redirection.Status() == 'Enabled':
                    selected = option

            checkbox = layout.GetControl(ctrl_name + '_cb')
            checkbox.AddCallback('Activate', OnCheckboxClicked, self)
            self.m_RedirectionEnabledMap[ctrl_name] = checkbox
            
            combobox.Populate(options)
            if selected:
                combobox.SetData(selected)
                checkbox.Checked(True)
            else:
                combobox.SetData(options[0])
        
        self.m_bindings.AddLayout(layout)
        self.UpdateControls()


    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')

        b.BeginHorzBox('None')
        b.  BeginVertBox('None')
        for k, v in self.m_Redirections.iteritems():
            ctrl_name = self.ToCtrlName(k)
            label = self.ToLabel(k)
            
            b.  BeginHorzBox('None')
            b.    AddCheckbox(ctrl_name + '_cb', label)
            b.    AddFill()
            b.  EndBox()
        b.  EndBox()

        b.  BeginVertBox('None')
        for k, v in self.m_Redirections.iteritems():
            ctrl_name = self.ToCtrlName(k)
            
            b.  BeginHorzBox('None')
            b.    AddOption(ctrl_name, None)
            b.  EndBox()
        b.  EndBox()
        b.EndBox()

        if len(self.m_Redirections) > 1:
            b.BeginHorzBox('None')
            b.  AddCheckbox('allCb', 'All')
            b.EndBox()

        b.  AddSeparator()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddSpace(150)
        b.    AddButton('ok', 'OK')
        b.    AddButton('apply', 'Apply')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()
        
        return b


def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    redirections = GroupRedirections(acm.User())    
    
    if redirections:
        customDlg = RoutingRedirectionDialog(redirections, shell)
        customDlg.InitControls()
        acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'There are no redirections set up.')


