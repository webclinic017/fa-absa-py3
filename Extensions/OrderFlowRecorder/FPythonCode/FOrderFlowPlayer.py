import acm
import FOrderFlowController

fileExtension = '.fof'
fileFilter = 'Order Flow Files (*.fof)|*.fof|Compressed Order Flow Files (*.cfof)|*.cfof'

class OrderFlowPlayer(FOrderFlowController.OrderFlowController):
    def __init__(self, orderFlow, owner):
        FOrderFlowController.OrderFlowController.__init__(self, orderFlow)
        self.dlg = None
        self.orderBooksCtrl = None
        self.addBtn = None
        self.removeBtn = None
        self.clearBtn = None
        self.owner = owner
        
    def InitLayout(self, dlg, layout):
        self.dlg = dlg
        self.orderBooksCtrl = layout.GetControl('orderBooks')
        self.addBtn = layout.GetControl('add')
        self.removeBtn = layout.GetControl('remove')
        self.clearBtn = layout.GetControl('clear')
        
        self.orderBooksCtrl.AddCallback('SelectionChanged', onSelectedOrderBookChanged, self)
        self.addBtn.AddCallback( 'Activate', onAddOrderBooks, self )
        self.removeBtn.AddCallback( 'Activate', onRemoveOrderBook, self )
        self.clearBtn.AddCallback( 'Activate', onClearOrderBooks, self )
             
    def BuildLayoutPart(self, builder):
        builder.BeginHorzBox('EtchedIn', 'Target Order Books')
        builder.  AddList('orderBooks', 5)
        builder.  BeginVertBox('None')
        builder.    AddButton('add', 'A&&dd...')
        builder.    AddButton('remove', 'Re&&move')
        builder.    AddButton('clear', 'C&&lear')
        builder.  EndBox()
        builder.EndBox()
    
    def Play(self, play):
        if play:
            self.Start()
        else:
            self.Stop()
                    
    def OnOrderFlowEvent(self, orderFlowEvent):
        FOrderFlowController.OrderFlowController.OnOrderFlowEvent(self, orderFlowEvent)
        self.owner.OnOrderFlowEvent(orderFlowEvent)
                
    def UpdateControls(self):
        self.clearBtn.Enabled(self.orderBooksCtrl.ItemCount() > 0)
        self.removeBtn.Enabled(self.orderBooksCtrl.GetData() != None)        
    
    def SelectOrderBooks(self):
        orderBooks = acm.UX().Dialogs().SelectObjectsInsertItems(self.dlg.Shell(), acm.FOrderBookInterface, True)
        if orderBooks != None:
            self.AddOrderBooks(orderBooks)
    
    def SelectedOrderBook(self):
        return self.orderBooksCtrl.GetData()
        
    def AddOrderBooks(self, orderBooks):
        FOrderFlowController.OrderFlowController.AddOrderBooks(self, orderBooks)
        self.orderBooksCtrl.Populate(self.OrderBooks())
        self.UpdateControls()
        
    def RemoveOrderBook(self, orderBook):
        FOrderFlowController.OrderFlowController.RemoveOrderBook(self, orderBook)
        self.orderBooksCtrl.Populate(self.OrderBooks())
        self.UpdateControls()
        
    def ClearOrderBooks(self):
        FOrderFlowController.OrderFlowController.ClearOrderBooks(self)
        self.orderBooksCtrl.Clear()
        self.UpdateControls()


def onAddOrderBooks(self, cd):
    self.SelectOrderBooks()
    
def onRemoveOrderBook(self, cd):
    ob = self.SelectedOrderBook()
    if ob != None:
        self.RemoveOrderBook(ob)
    
def onClearOrderBooks(self, cd):
    self.ClearOrderBooks()
    
def onSelectedOrderBookChanged(self, cd):
    self.UpdateControls()

def showErrorDialog(shell, message):
    return acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Error', message)
