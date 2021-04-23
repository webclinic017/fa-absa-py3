'''================================================================================================
================================================================================================'''
import acm
import time
import FUxCore
'''================================================================================================
================================================================================================'''
def get_status(user):
    if str(acm.ObjectServer().ClassName()) == 'FTmServer': 
        module = acm.FExtensionModule[user.Name()]
        extension = module.GetExtension('FParameters', 'FObject', 'FXUserParams')
        if extension == None: create_default_params(user, 'no') 
        params = extension.Value()
        return str(params.At('ltn_email'))
    else:
        return None
enabled = get_status(acm.User())
'''================================================================================================
================================================================================================'''
def create_default_params(user, on):
    extContext      = acm.FExtensionContext()
    module          = acm.FExtensionModule[user.Name()]
    extContext.AddModule(module)
    extAttrText = 'FObject:FXUserParams =' 
    extAttrText += '\nltn_email=' + on
    extContext.EditImport('FParameters', extAttrText)
    module.Commit()
    global enabled
    enabled = 1 if on == 'yes' else 0
    return module
'''================================================================================================
================================================================================================'''
def NotificationOFF(eii): return CreateLTNMenuItem(eii, 0)
def NotificationON(eii): return CreateLTNMenuItem(eii, 1)
'''================================================================================================
================================================================================================'''
class CreateLTNMenuItem(FUxCore.MenuItem):
   
    def __init__(self, extObj, onOff):
        self._onOff = onOff
        self._frame = extObj  
        
    def Invoke(self, eii):  # eii = 'FExtensionInvokationInfo' 
        if self._onOff == 1:
            acm.Log('Turning Large Trade Notification ON')
            print 'Turning Large Trade Notification ON'
            create_default_params(acm.User(), 'yes')
        else:
            acm.Log('Turning Large Trade Notification OFF')
            print 'Turning Large Trade Notification OFF'
            create_default_params(acm.User(), 'no')
        
    def Enabled(self):
        global enabled
        if enabled == 1:
            return True if self._onOff == 0 else False
        else:    
            return False if self._onOff == 0 else True
 
    def Checked(self): return False
    def Applicable(self): return True
'''================================================================================================
================================================================================================'''
