import acm
import FOrderFlowController
import FOrderFlowPlayer
import FUxCore
      
class OrderFlowPlayerDialog (FUxCore.LayoutDialog):
    def __init__(self, orderFlow, initialOrderBooks):
        self.orderFlow = orderFlow
        self.initialOrderBooks = initialOrderBooks
        self.orderFlowPlayer = FOrderFlowPlayer.OrderFlowPlayer(orderFlow, self)
        self.fuxDlg = None
        self.bindings = acm.FUxDataBindings()
        self.nameCtrl = self.bindings.AddBinder( 'nameCtrl', acm.GetDomain('string'), None )
        self.nextEventCtrl = self.bindings.AddBinder( 'nextEventCtrl', acm.GetDomain('string'), None )
        self.startTimeCtrl = self.bindings.AddBinder( 'startTimeCtrl', acm.GetDomain('datetime'), None )
        self.ignoreBeforeCtrl = self.bindings.AddBinder( 'ignoreBeforeCtrl', acm.GetDomain('datetime'), None )
        self.speedCtrl = self.bindings.AddBinder( 'speedCtrl', acm.GetDomain('double'), None )
        self.startBtn = None
        self.stopBtn = None
        self.resetBtn = None
    
    def HandleApply(self):
        return 1
        
    def HandleDestroy(self):
        self.orderFlowPlayer.Play(False)
        
    def HandleCreate( self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('Order Flow Player' )
        self.bindings.AddLayout(layout)
        
        self.startBtn = layout.GetControl('start')
        self.stopBtn = layout.GetControl('stop')
        self.resetBtn = layout.GetControl('reset')
        
        self.startBtn.AddCallback( 'Activate', onStartOrderFlow, self )
        self.stopBtn.AddCallback( 'Activate', onStopOrderFlow, self )
        self.resetBtn.AddCallback( 'Activate', onResetOrderFlow, self )

        self.nameCtrl.SetValue(self.orderFlow.Name(), False)
        self.startTimeCtrl.SetValue(self.orderFlow.StartTime(), False)
        self.speedCtrl.SetValue(self.orderFlow.Speed(), False)
        
        self.nameCtrl.Editable(False)
        self.nextEventCtrl.Editable(False)

        self.orderFlowPlayer.InitLayout(dlg, layout)
        self.orderFlowPlayer.AddOrderBooks(self.initialOrderBooks)
        self.bindings.AddDependent( self )
        self.UpdateControls()
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if parameter == self.startTimeCtrl:
            self.orderFlow.StartTime(self.startTimeCtrl.GetValue())
        elif parameter == self.ignoreBeforeCtrl:
            self.orderFlowPlayer.NextEvent(self.ignoreBeforeCtrl.GetValue())
        elif parameter == self.speedCtrl:
            self.orderFlow.Speed(self.speedCtrl.GetValue())
        self.UpdateControls()

    def UpdateControls(self):
        self.startTimeCtrl.Enabled(not self.orderFlow.IsStarted())
        self.ignoreBeforeCtrl.Enabled(not self.orderFlow.IsStarted())
        self.speedCtrl.Enabled(not self.orderFlow.IsStarted())
        self.startBtn.Enabled(not self.orderFlow.IsStarted())
        self.stopBtn.Enabled(self.orderFlow.IsStarted())
        self.resetBtn.Enabled(not self.orderFlow.IsStarted())
        self.orderFlowPlayer.UpdateControls()
        self.UpdateNextEvent()
    
    def UpdateNextEvent(self):
        text = ''
        nextEvent = self.orderFlow.NextEvent()
        if nextEvent != None:
            text = nextEvent.AsString()
        elif self.orderFlow.IsStarted():
            text = 'Done'
                
        self.nextEventCtrl.SetValue(text, False)
            
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        
        b.  BeginVertBox('EtchedIn', 'Order Flow')
        self.nameCtrl.BuildLayoutPart(b, 'File')
        self.nextEventCtrl.BuildLayoutPart(b, 'Next Event')
        self.startTimeCtrl.BuildLayoutPart(b, 'Start Time')
        self.ignoreBeforeCtrl.BuildLayoutPart(b, 'Ignore Events Before')
        self.speedCtrl.BuildLayoutPart(b, 'Speed')
        b.  EndBox()
        
        self.orderFlowPlayer.BuildLayoutPart(b)
        
        b.  BeginHorzBox('None')
        b.    AddSpace(5)
        b.    AddFill()
        b.    AddButton('start', '&&Start')
        b.    AddButton('stop', 'S&&top')
        b.    AddButton('reset', '&&Reset')
        b.  EndBox()
        
        b.EndBox()
        return b
        
    def Play(self, play):
        self.orderFlowPlayer.Play(play)
        self.UpdateNextEvent()
        self.UpdateControls()
    
    def Reset(self):
        self.orderFlowPlayer.Reset()
        self.UpdateNextEvent()
        self.UpdateControls()
        
    def OnOrderFlowEvent(self, orderFlowEvent):
        self.UpdateNextEvent()
        
 

def onStartOrderFlow(self, cd):
    self.Play(True)
    
def onStopOrderFlow(self, cd):
    self.Play(False)

def onResetOrderFlow(self, cd):
    self.Reset()

def selectStartedOrderFlow(shell):
    orderFlows = acm.FArray()
    all = acm.FOrderFlow.InstancesKindOf()

    for of in all:
        if of.IsStarted() and of.Name() != None:
            orderFlows.Add(of)
                   
    if orderFlows.IsEmpty():
        return None
    
    question = 'You have one or more Order Flows running. Do you want to open a running Order Flow?'
    if 'Button1' == acm.UX().Dialogs().MessageBoxYesNo(shell, 'Question', question):
        if orderFlows.Size() == 1:
            return orderFlows.First()
        return acm.UX().Dialogs().SelectObject(shell, 'Open', 'Order Flow', orderFlows, None)
    return None

def openOrderFlow(shell, orderFlow, orderBooks):
    customDlg = OrderFlowPlayerDialog(orderFlow, orderBooks)
    acm.UX().Dialogs().ShowCustomDialog(shell, customDlg.CreateLayout(), customDlg )

def onConvertToNewFormat(invokationInfo):
    shell = invokationInfo.Parameter('shell')
    fileSelection = acm.FFileSelection()
    fileSelection.FileFilter(FOrderFlowPlayer.fileFilter)
    fileSelection.PickExistingFile(True)
    
    if acm.UX().Dialogs().BrowseForFile(shell, fileSelection):
        try:
            FOrderFlowController.convertToNewFormat(fileSelection.SelectedFile().StringKey())
            acm.UX().Dialogs().MessageBoxInformation(shell, 'Order Flow converted!')
        except Exception as e:
            FOrderFlowPlayer.showErrorDialog(shell, 'Failed to convert Order Flow: ' + str(e))
            
def onShowDlg(invokationInfo):
    shell = invokationInfo.Parameter('shell')
    orderBooks = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedOrderBooks()
    orderFlow = selectStartedOrderFlow(shell)
       
    if orderFlow != None:
        openOrderFlow(shell, orderFlow, orderBooks)
    else:
        fileSelection = acm.FFileSelection()
        fileSelection.FileFilter(FOrderFlowPlayer.fileFilter)
        fileSelection.PickExistingFile(True)
    
        if acm.UX().Dialogs().BrowseForFile(shell, fileSelection):
            selectedFile = fileSelection.SelectedFile().StringKey()
            success = False
            
            try:
                serializer = acm.FXmlSerializer()
                orderFlow = FOrderFlowController.importOrderFlow(selectedFile)
                if orderFlow != None:
                    openOrderFlow(shell, orderFlow, orderBooks)
                    success = True
            except:
                pass
                
            if not success:
                result = FOrderFlowPlayer.showErrorDialog(shell, 'The selected file does not contain a valid Order Flow')
                if 'Button1' == result:
                    onShowDlg(invokationInfo)
