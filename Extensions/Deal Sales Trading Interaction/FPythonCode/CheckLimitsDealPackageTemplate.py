
import acm
from DealPackageDevKit import Action, Text, NoButtonAttributeDialog, NoTradeActions, Settings, DealPackageDefinition, DealPackageException, DealPackageUserException
from DealPackageUtil import UnpackPaneInfo

@NoTradeActions
@Settings( GraphApplicable=False,
           SheetApplicable=False )
class CheckLimits(DealPackageDefinition):        
    
    result                       = Action(      action='@ConfirmResult',
                                                dialog=NoButtonAttributeDialog( label='Limit Check Result', 
                                                                                customPanes='@DialogPanes')
                                         ) # Omit the 'dialog' metadata if only the action should be called
                                         
    infoText                    = Text(         defaultValue = 'All limits passed.',
                                                width=300,
                                                height=100)
                                                                        
    ok                          = Action(       action='@Ok',
                                                label='OK',
                                                visible='@OkVisible')
    
    ignore                      = Action(       action='@Ignore',
                                                label='Ignore',
                                                visible='@IgnoreVisible')
    
    cancel                      = Action(       action='@Cancel',
                                                label='Cancel',
                                                visible='@CancelVisible')
    
    def OnInit(self, *args, **kwargs):
        self._tradeToCheck = None
        self._dealPackageToCheck = None
        self._okToSendRequest = True
        
    def AssemblePackage(self, arguments):    
        self._tradeToCheck = arguments[0]
        self._dealPackageToCheck = arguments[1]
        
    def OnNew(self, *args):
        self.PerformChecks()
    
    '''********************************************************************
    * Perform Limit Checks 
    ********************************************************************'''   
    def PerformChecks(self):
        if self._tradeToCheck.Quantity() > 1000:
            self._okToSendRequest = False
            self.infoText = 'Limit breached: Trade quantity is larger than 1000.'
    
    '''********************************************************************
    * ConfirmResult - Return False to disallow Quote Request/Sales Order continuation
                      Called after PerformChecks. If a dialog metadata is specifed on the
                      'result' attribute, ConfirmResult is called when the dialog closes.
    ********************************************************************'''  
    def ConfirmResult(self, *args):
        return self._okToSendRequest
    
    '''********************************************************************
    * Button Action Callbacks
    ********************************************************************''' 
    def Ok(self, *args):
        self.CloseDialog()
    
    def Ignore(self, *args):
        self._okToSendRequest = True
        self.CloseDialog()
    
    def Cancel(self, *args):
        self.CloseDialog()
    
    '''********************************************************************
    * Visible Callbacks
    ********************************************************************''' 
    def OkVisible(self, *args):
        return self._okToSendRequest
        
    def IgnoreVisible(self, *args):
        return not self._okToSendRequest
        
    def CancelVisible(self, *args):
        return not self._okToSendRequest
        
    '''********************************************************************
    * Dialog Layout
    ********************************************************************''' 
    def DialogPanes(self, *args):
        return [
                    {'Result' : '''
                                vbox(;
                                    infoText;
                                    hbox(;
                                        fill;
                                        ok;
                                        ignore;
                                        cancel;
                                    );
                                );
                                '''
                    }
                ]
