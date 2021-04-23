import acm
import FOrderFlowController
import FOrderFlowPlayer
import FUxCore
import time

recordingColor = acm.UX().Colors().Create(255, 0, 0)
timer = acm.GetFunction('timer', 0)()
recorderHandlers = {}

"""--------------------------------------------------
 OrderFlowRecorderHandler - Wrapper class for 
 FOrderFlowRecorder used for starting/stopping
 recorder at specific times.
--------------------------------------------------"""
class OrderFlowRecorderHandler():
    def __init__(self, recorder):
        self.recorder = recorder
        self.startEvent = None
        self.stopEvent = None
        addRecorderHandler(self)
    
    def Start(self, time = None):
        if time == None:
            if self.startEvent:
                timer.RemoveTimerEvent(self.startEvent)
                self.startEvent = None
            self.Recorder().Start()
        else:
            self.startEvent = timer.CreateTimerEventAt(time, onStartHandler, self)
            if self.startEvent.IsExpired():
                self.Start()
        
    def Stop(self, time = None):
        if time == None:
            if self.startEvent:
                timer.RemoveTimerEvent(self.startEvent)
                self.startEvent = None
            if self.stopEvent:
                timer.RemoveTimerEvent(self.stopEvent)
                self.stopEvent = None
            self.Recorder().Stop()
        else:
            self.stopEvent = timer.CreateTimerEventAt(time, onStopHandler, self)
            if self.stopEvent.IsExpired():
                self.Stop()
            
    def Recorder(self):
        return self.recorder
        
    def OrderFlow(self):
        return self.Recorder().OrderFlow()
        
    def Status(self):
        if self.startEvent != None:
                return 'Scheduled Start'
        elif self.Recorder().StartTime() == None:
            return 'Not Started'
        elif self.Recorder().IsRecording():
            return 'Recording'
        return 'Stopped'
        
    def IsStarted(self):
        if self.startEvent != None:
            return True
        return self.Recorder().IsRecording()
                
"""--------------------------------------------------
 OrderFlowRecorderDialog - Dialog used for controlling
 an order flow recorder
--------------------------------------------------"""
class OrderFlowRecorderDialog (FUxCore.LayoutDialog):
    def __init__(self, orderBook, recorder):
        self.recorderHandler = None
        if recorder:
            self.recorderHandler = recorder
        else:
            self.recorderHandler = OrderFlowRecorderHandler(acm.FOrderFlowRecorder(orderBook))
        self.fuxDlg = None
        self.bindings = None
        self.orderFlowPlayer = FOrderFlowPlayer.OrderFlowPlayer(self.recorderHandler.OrderFlow(), self)
        self.bindings = acm.FUxDataBindings()
        self.orderBookCtrl = self.bindings.AddBinder( 'orderBookCtrl', acm.GetDomain('FOrderBookInterface'), None )
        self.startTimeCtrl = self.bindings.AddBinder( 'startTimeCtrl', acm.GetDomain('datetime'), None )
        self.stopTimeCtrl = self.bindings.AddBinder( 'stopTimeCtrl', acm.GetDomain('datetime'), None )
        self.statusCtrl = self.bindings.AddBinder( 'statusCtrl', acm.GetDomain('string'), None )
        self.statusColor = None
        self.latestEventCtrl = self.bindings.AddBinder( 'latestEventCtrl', acm.GetDomain('string'), None )
        self.recordBtn = None
        self.stopBtn = None
        self.saveBtn = None
        
    def HandleApply(self):
        return 1
    
    def HandleCreate( self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('Order Flow Recorder' )
        self.bindings.AddLayout(layout)
        
        self.recordBtn = layout.GetControl('record')
        self.stopBtn = layout.GetControl('stop')
        self.saveBtn = layout.GetControl('save')
        self.statusColor = layout.GetControl('statusCtrl')
        
        self.recordBtn.AddCallback( 'Activate', onStartRecording, self )
        self.stopBtn.AddCallback( 'Activate', onStopRecording, self )
        self.saveBtn.AddCallback( 'Activate', onSaveOrderFlow, self )

        self.orderBookCtrl.SetValue(self.Recorder().TradingInterface(), False)
        self.orderBookCtrl.Editable(False)
        self.statusCtrl.Editable(False)
        self.latestEventCtrl.Editable(False)
        self.orderFlowPlayer.InitLayout(dlg, layout)

        self.bindings.AddDependent( self )
        self.Recorder().AddDependent( self )
        self.UpdateControls()
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()
    
    def UpdateControls(self):
        started = self.recorderHandler.IsStarted()
        self.recordBtn.Enabled(not started)
        self.stopBtn.Enabled(started)
        self.saveBtn.Enabled(not started and not self.OrderFlow().IsEmpty())
        self.startTimeCtrl.Editable(not started)
        self.stopTimeCtrl.Editable(not started)
        
        self.statusCtrl.SetValue(self.recorderHandler.Status(), False)
        
        if self.Recorder().IsRecording():
            self.statusColor.SetColor('Text', recordingColor)
        else:
            self.statusColor.SetColor('Text', None)
            
        self.orderFlowPlayer.UpdateControls()
                                   
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        
        b.  BeginVertBox('EtchedIn', 'Source')
        self.orderBookCtrl.BuildLayoutPart(b, 'Order Book')
        self.startTimeCtrl.BuildLayoutPart(b, 'Start Time')
        self.stopTimeCtrl.BuildLayoutPart(b, 'Stop Time')
        self.statusCtrl.BuildLayoutPart(b, 'Status')
        self.latestEventCtrl.BuildLayoutPart(b, 'Last Event')
        b.  EndBox()
        
        b.  BeginVertBox('EtchedIn', 'Replay Order Flow')
        self.orderFlowPlayer.BuildLayoutPart(b)
        b.  EndBox()
        
        b.  BeginHorzBox('None')
        b.    AddSpace(5)
        b.    AddFill()
        b.    AddButton('record', '&&Rec')
        b.    AddButton('stop', 'S&&top')
        b.    AddButton('save', '&&Save')
        b.  EndBox()
        
        b.EndBox()
        return b
    
    def Recorder(self):
        return self.recorderHandler.Recorder()
    
    def OrderFlow(self):
        return self.Recorder().OrderFlow()
        
    def Record(self, rec):
        if rec:
            self.recorderHandler.Start(self.startTimeCtrl.GetValue())
            stopTime = self.stopTimeCtrl.GetValue()
            if stopTime != None:
                self.recorderHandler.Stop(stopTime)
        else:
            self.recorderHandler.Stop()
        self.orderFlowPlayer.Play(rec)
        self.UpdateControls()
            
    def Save(self):
        selectedFile = self.Recorder().TradingInterface().StringKey() + time.strftime('%y%m%d')
        fileSelection = acm.FFileSelection()
        fileSelection.FileFilter(FOrderFlowPlayer.fileFilter)
        fileSelection.SelectedFile(selectedFile)
        fileSelection.PickExistingFile(False)
        
        try:
            if acm.UX().Dialogs().BrowseForFile(self.fuxDlg.Shell(), fileSelection):
                selectedFile = fileSelection.SelectedFile().StringKey()
                FOrderFlowController.exportOrderFlow(self.OrderFlow(), selectedFile)
        except Exception as e:
            FOrderFlowPlayer.showErrorDialog(self.fuxDlg.Shell(), 'Failed to save Order Flow' + str(e))

    def OnOrderFlowEvent(self, orderFlowEvent):
        self.latestEventCtrl.SetValue(orderFlowEvent.AsString(), False)

"""-------------------------------------------------------------
 Callbacks
-------------------------------------------------------------"""
def onStartRecording(self, cd):
    self.Record(True)

def onStopRecording(self, cd):
    self.Record(False)

def onSaveOrderFlow(self, cd):
    self.Save()    

def onStartHandler(recorderHandler):
    recorderHandler.Start()
    
def onStopHandler(recorderHandler):
    recorderHandler.Stop()

# Add recorder handler
def addRecorderHandler(recorderHandler):
    recorderHandlers[recorderHandler.Recorder()] = recorderHandler

# Return recorder handler for order book    
def getRecorderHandler(orderBook):
    recorder = acm.Trading().OrderFlowRecorder(orderBook)
    if recorder != None:
        if recorder in recorderHandlers:
            return recorderHandlers[recorder]
        else:
            handler = OrderFlowRecorderHandler(recorder)
            addRecorderHandler(handler)
            return handler
    return None

# Show recorder dialog    
def onShowDlg(invokationInfo):
    shell = invokationInfo.Parameter('shell')   
    orderBooks = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedTradingInterfaces()
    
    for ob in orderBooks:
        handler = getRecorderHandler(ob)
        customDlg = OrderFlowRecorderDialog(ob, handler)
        acm.UX().Dialogs().ShowCustomDialog(shell, customDlg.CreateLayout(), customDlg )

# Stop recorders for selected order books
def onStopRecorders(invokationInfo):
    orderBooks = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedTradingInterfaces()
    
    for ob in orderBooks:
        handler = getRecorderHandler(ob)
        if handler:
            handler.Stop()
            handler.Recorder().OrderFlow().Stop()
