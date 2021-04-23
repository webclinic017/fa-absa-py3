
import acm
from QuoteRequestReplyDialog import QuoteRequestReplyDialog

class QuoteRequestReplyDialogHandler(object):
    def __init__(self, shell, replyHandler):
        self._shell = shell
        self._dialogCache = acm.FDictionary()
        replyHandler.AddDependent(self)
        
    def Shell(self):
        return self._shell
                
    def FromDialogCache(self, replyHandler):
        return self._dialogCache.At(replyHandler)
        
    def ToDialogCache(self, replyHandler, dealPackageDlg):
        self._dialogCache.AtPut(replyHandler, dealPackageDlg)
        
    def CreateDialogAndAddToCache(self, replyHandler):
        dealPackageDlg = QuoteRequestReplyDialog(self.Shell(), replyHandler, 'Quote Reply', 4)
        self.ToDialogCache(replyHandler, dealPackageDlg)
        dealPackageDlg._UpdateTraitsTabValues()
        return dealPackageDlg
    
    def StartDialog(self, replyHandler):
        dealPackageDlg = self.FromDialogCache(replyHandler)
        if dealPackageDlg:
            dealPackageDlg.UpdateSelectedQuoteContoller(replyHandler)
            dealPackageDlg.AlwaysOnTop(replyHandler.AlwaysOnTop())
        else:
            dealPackageDlg = self.CreateDialogAndAddToCache(replyHandler)
        dealPackageDlg.Show(self.Shell())
        return dealPackageDlg
      
    def OnReplyHandlerInclude(self, replyHandler):
        dealPackageDlg = self.StartDialog(replyHandler)
        
    def OnReplyHandlerForce(self, replyHandler):
        dealPackageDlg = self.StartDialog(replyHandler)
        
    def OnReplyHandlerExclude(self, replyHandler):
        dealPackageDlg = self.FromDialogCache(replyHandler)
        if dealPackageDlg:
            if replyHandler.QuoteControllers().Size() == 0:
                dealPackageDlg._FuxDialog().CloseDialogCancel()
            else:
                dealPackageDlg.UpdateSelectedQuoteContoller(replyHandler)

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        
        try:
            if str(aspectSymbol) == 'include':
                self.OnReplyHandlerInclude(sender)
            elif str(aspectSymbol) == 'force':
                self.OnReplyHandlerForce(sender)
            elif str(aspectSymbol) == 'exclude':
                self.OnReplyHandlerExclude(sender)
        except Exception as e:
            print ('QuoteRequestReplyDialogHandler ServerUpdate Failed', aspectSymbol,  e)
    
'''*****************************************************************************************************        
*
* This is the Electronic Trading Extension Point, registered as a FCustomMethod
*
******************************************************************************************************'''
def QuoteRequestReplyDialogOverride(invokationInfo):
    try:
        shell = invokationInfo.Parameter('shell')
        replyHandler = invokationInfo.Parameter('replyHandler')
        QuoteRequestReplyDialogHandler(shell, replyHandler)
    except Exception as e:
        print ('QuoteRequestReplyDialog failed', e)
