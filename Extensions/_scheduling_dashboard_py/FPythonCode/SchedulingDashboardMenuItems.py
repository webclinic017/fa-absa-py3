""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SchedulingDashboard/etc/SchedulingDashboardMenuItems.py"
""" Menu Items class for Scheduling Dashboard application """

import acm
import FUxCore

class menuItems(FUxCore.MenuItem):
    def __init__(self):
        self.application = None

    def Invoke(self, cd):
        commandName = cd.Definition().GetName().Text()
        if commandName == 'TaskManagement':
            acm.UX().SessionManager().StartApplication('Task Management', None)
        elif commandName == 'DeleteGroup':
            self.application.DeleteGroup()
        else: 
            pass
            
    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

    def SetApplication(self, application):
        self.application = application

class TaskMenuItems(FUxCore.MenuItem):
    def __init__(self):
        self.panel = None

    def Invoke(self, cd):
        commandName = cd.Definition().GetName().Text()
        if commandName == 'deleteDependency':
            self.panel.DeleteDependency()
        elif commandName == 'deleteSchedule':
            self.panel.DeleteSchedule()
        else: 
            pass

    def Applicable(self):
        return True

    def Enabled(self):
        return True

    def Checked(self):
        return False

    def SetPanel(self, panel):
        self.panel = panel