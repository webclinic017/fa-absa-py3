import FUxCore
class MenuCommandHandler(FUxCore.MenuItem):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB = None):
        self.m_ApplicationObject = p_ParentApplication
        self.m_CommandName = p_CommandName
        self.m_CommandCB   = p_CommandCB

    def Invoke(self, cd):
        pass

    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

    def Instance(self):
        return self

class OpenPanelCommandsHandler(MenuCommandHandler):
    def __init__(self, p_ParentApplication, p_CommandName, p_CommandCB):
        MenuCommandHandler.__init__(self, p_ParentApplication, p_CommandName, p_CommandCB)

    def Invoke(self, cd):
        self.m_CommandCB(self.m_ApplicationObject, None)

    def Enabled(self):
        return True

class ListItem(FUxCore.MenuItem):
    def __init__(self, package_dialog):
        self.m_package_dialog = package_dialog
        pass

    def Invoke(self, cd):
        if cd.Definition().GetName().AsString() == 'Remove':
            self.m_package_dialog.RemoveObject()
        elif cd.Definition().GetName().AsString() == 'Open':
            self.m_package_dialog.OpenListObject()
        elif cd.Definition().GetName().AsString() == 'Properties':
            self.m_package_dialog.InspectListObject()
        
    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False
        
class IncludeExcludeItem(FUxCore.MenuItem):
    def __init__(self, package_dialog):
        self.m_package_dialog = package_dialog
        pass
        
    def Invoke(self, cd):
        if cd.Definition().GetName().AsString() == 'Include':
            self.m_package_dialog.IncludeSpecificObject()
        elif cd.Definition().GetName().AsString() == 'Remove':
            self.m_package_dialog.RemoveSpecificObject()
        elif cd.Definition().GetName().AsString() == 'Remove All of Class':
            self.m_package_dialog.RemoveAllSpecificObject()
        elif cd.Definition().GetName().AsString() == 'Include All of Class':
            self.m_package_dialog.IncludeAllSpecificObject()
        elif cd.Definition().GetName().AsString() == 'Open':
            self.m_package_dialog.OpenObject()
        elif cd.Definition().GetName().AsString() == 'Properties':
            self.m_package_dialog.InspectObject()
        
    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

