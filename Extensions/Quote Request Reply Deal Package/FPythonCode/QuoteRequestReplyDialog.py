
import acm
import FUxCore
from DealPackageAsDialog import DealPackageDialog
from DealPackageUtil import UnpackPaneInfo
from QuoteRequestReplyUtil import Misc
from QuoteRequestReplyDialogList import QuoteRequestReplyList

class QuoteRequestReplyDialog(DealPackageDialog):
    def __init__(self, shell, replyHandler, caption, applyMode):
        self._shell = shell
        self._dialogIsOpen = False
        self._selectedQuoteController = None
        self._replyHandler = replyHandler
        dealPackage = self.CreateInitialDealPackage(replyHandler)
        self._replyHandlerList = QuoteRequestReplyList(replyHandler.QuoteControllers(), self.QuoteControllerListSelectionChanged)
        DealPackageDialog.__init__(self, shell, dealPackage, caption, applyMode)
        
    def ReplyHandlerList(self):
        return self._replyHandlerList
        
    def Shell(self):
        return self._shell    
    
    def CreateInitialDealPackage(self, replyHandler):
        quoteController = self.GetActiveQuoteController(replyHandler)
        self._selectedQuoteController = quoteController
        return self.CreateDealPackage(quoteController)

    def CreateDealPackage(self, quoteController):
        gui = acm.FBusinessLogicGUIShell()
        gui.SetFUxShell(self.Shell())
        return acm.DealPackage().NewAsDecorator('Quote Request Reply', gui, [quoteController])
        
    def GetActiveQuoteController(self, replyHandler):
        forcedQuoteController = replyHandler.ForcedController()
        quoteControllers = replyHandler.QuoteControllers()
        return forcedQuoteController if forcedQuoteController else (quoteControllers.First() if quoteControllers.Size() > 0 else None)

    def UpdateSelectedQuoteContoller(self, replyHandler):
        quoteController = self.GetActiveQuoteController(replyHandler)
        self.QuoteControllerListSelectionChanged(quoteController)
        self.ReplyHandlerList().UpdateSelected(quoteController)

    def NeedToRebuildDialogLayout(self, quoteController):
        needRebuild = False
        if quoteController:
            fromType = Misc.IdentifyObjectTypeFromQuoteController(self._selectedQuoteController)
            toType = Misc.IdentifyObjectTypeFromQuoteController(quoteController)
            needRebuild = fromType != toType
        return needRebuild
        
    def CreateLayout(self):
        from DealPackageUxTraitsTabPane import TraitsPane       
        fUxLayoutBuilder = acm.FUxLayoutBuilder()
        self.m_GUIPanes = acm.FArray()
        self._GetCustomPaneInfos()
        paneInfo = self.m_paneInfos[0]
        paneName, customLayout = UnpackPaneInfo(paneInfo)
        customPane = TraitsPane(self, paneName)
        customPane.BuildPaneLayout(fUxLayoutBuilder, customLayout) 
        self._GUIPanes().Add(customPane)
        return fUxLayoutBuilder, customPane
    
    def RebuildLayout(self):
        fUxLayoutBuilder, customPane = self.CreateLayout()
        self._FuxTopLayout().SetLayout(fUxLayoutBuilder, 'RFQ')  
        customPane.AddLayoutToBindingsAndInitControls(self._FuxTopLayout())
        self._UpdateTraitsTabValues()
    
    def AlwaysOnTop(self, enable):
        self._FuxDialog().AlwaysOnTop(enable)
        
    def QuoteControllerListSelectionChanged(self, quoteController):
        if self.NeedToRebuildDialogLayout(quoteController):
            self.m_dealPackage = self.CreateDealPackage(quoteController)
            self.SetDealPackageUxCallbacks()
            self.RebuildLayout()
            self.m_refreshProxy._dp = self.DealPackage()
        else:
            self.DealPackage().GetAttribute('updateQuoteController')(quoteController)
            
        if quoteController:
            self._selectedQuoteController = quoteController

    def HandleCancel(self):
        self.QuoteControllerListSelectionChanged(None)
        self._replyHandler.ForcedController(None)
        self._dialogIsOpen = False
        return True
        
    def HasCustomBottomLayout(self):
        return False
        
    def HandleCreate( self, dialog, layout ):
        DealPackageDialog.HandleCreate(self, dialog, layout)
        self.ReplyHandlerList().InitControls(layout)
        self.ReplyHandlerList().UpdateSelected(self._selectedQuoteController)
        
    def CreateBottomLayout(self):
        return self.ReplyHandlerList().BuildLayout()
        
    def ShowDialog(self, shell, modalMode=True):
        fUxLayoutBuilder = self.CreateBottomLayout()
        acm.UX().Dialogs().ShowCustomDialog(shell, fUxLayoutBuilder, self, False, True)
              
    def Show(self, shell):
        try:
            if self._FuxDialog():
                self._FuxDialog().ShowDialog(True)
            else:
                self.ShowDialog(shell, False)
            self._dialogIsOpen = True
        except Exception as e:
            print ('QuoteRequestReplyDialog - Show', e)
            self._dialogIsOpen = False
            
    def _OnTimerTick(self, ud):
        if self._dialogIsOpen:
            self.RefreshProxy().Refresh()
            self.ReplyHandlerList().Update()
        

