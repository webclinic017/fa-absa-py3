""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/NotificationApplication.py"

import acm, ael
import FUxCore
import FSheetUtils
from ACMPyUtils import Transaction
from FParameterSettings import ParameterSettingsCreator
from FPanel import Panel
from FIntegratedWorkbenchUtils import GetAttributeInModule 

_SETTINGS = ParameterSettingsCreator.FromRootParameter('AlertNotificationView')

class NotificationApplication(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.tabs = list()
        self.pages = dict()
        self._subscription = None
        self._incomingAlerts = set()
        self._tabs = _SETTINGS.DockWindows()
        
    def HandleRegisterCommands(self, builder):
        builder.RegisterCommands([], [])
    
    def HandleCreate(self, createContext):
        self.tabControl = createContext.AddTabControlPane('tabPanel')
        for cls in self._tabs:
            attrpath = cls.Module()
            attr = GetAttributeInModule(attrpath)
            page = attr(self)
            self.pages[page.__class__.__name__] = page
            layout = self.tabControl.AddLayoutPage(page.CreateLayout(), page.TAB_NAME)
            page.InitControls(layout)
        self.InitSubscriptions()
        self.EnableOnIdleCallback(True)
      
      
    #Subscibe to the alert table
    def AlertTableCB(self, _object, ael_entity, _arg, event):
        if event in ['insert', 'update']:
            alert = acm.FAlert[ael_entity.seqnbr]
            self._incomingAlerts.add(alert)

    def InitSubscriptions(self):
        self._subscription = self._bindFunction(self.AlertTableCB)
        ael.Alert.subscribe(self._subscription, None)
        
    def _bindFunction(self, function):
        def inner(*args, **kwargs):
            return function(*args, **kwargs)
        return inner
  
    def HandleDestroy(self):
        ael.Alert.unsubscribe(self._subscription, None)
      
    def HandleOnIdle(self):
        while self._incomingAlerts:
            alert = self._incomingAlerts.pop()
            for page in self.pages.values():
                if hasattr(page, 'ProcessAlert'):
                    page.ProcessAlert(alert)
      


def CreateApplicationInstance():
    return NotificationApplication()
    
    
def StartOrActivateNotificationApplication(eii):
    for a in acm.ApplicationList():
        if a.Name() == "Notification Viewer":
            a.Restore()
            a.Activate()
            return
    acm.StartApplication('Notification Viewer', None)




