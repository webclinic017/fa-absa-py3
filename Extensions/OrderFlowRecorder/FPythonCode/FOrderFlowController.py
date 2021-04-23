import acm
import FOrderFlow
import zipfile


class OrderFlowController():
    def __init__(self, orderFlow):
        self.orderBooks = acm.FArray()
        self.orderFlow = orderFlow
        self.startIndex = -1
    
    def NextEvent(self, time):
        self.startIndex = self.orderFlow.FindNextEventIndex(time)
        self.Reset()
            
    def Start(self):
        self.orderFlow.Start(onOrderFlowEvent, self)
        
    def Stop(self):
        self.orderFlow.Stop()
        
    def Reset(self):
        if self.startIndex != -1:
            self.orderFlow.NextEvent(self.startIndex)
        else:
            self.orderFlow.Reset()
    
    def OnOrderFlowEvent(self, orderFlowEvent):
        if not self.orderBooks.IsEmpty():
            FOrderFlow.handleOrderFlowEvent(orderFlowEvent, self.orderBooks)

    def OrderBooks(self):
        return self.orderBooks
        
    def AddOrderBooks(self, orderBooks):
        self.orderBooks.AddAll(orderBooks)
        
    def RemoveOrderBook(self, orderBook):
        self.orderBooks.Remove(orderBook)
        
    def ClearOrderBooks(self):
        self.orderBooks.Clear()


def onOrderFlowEvent(orderFlowEvent, receiver):
    receiver.OnOrderFlowEvent(orderFlowEvent)

def convertToNewFormat(fileName):
    s = acm.FXmlSerializer()
    orderFlow = s.Import(fileName)
    exportOrderFlow(orderFlow, fileName + '.fof')
    
def importOrderFlow(fileName):
    orderFlow = None
    if fileName.endswith('.fof'):
        file = open(fileName, 'r')
        fileContent = file.read()
        file.close()
        orderFlow = acm.Trading.ImportOrderFlow(fileContent)
    elif fileName.endswith('.cfof'):
        file = open(fileName, 'r')
        fileContent = file.read()
        file.close()
        archive = acm.FXmlArchive()
        archive.Load(fileContent)
        of = archive.Get('orderFlow')
        
        if isinstance(of, type('')):
            orderFlow = acm.Trading.ImportOrderFlow(of)
        elif of.IsKindOf(acm.FOrderFlow):
            orderFlow = of
        
    if orderFlow != None:
        orderFlow.Name(fileName)
    return orderFlow

def exportOrderFlow(orderFlow, fileName):    
    if fileName.endswith('.fof'):
        fileStream = acm.FCharacterOutputFileStream(fileName)
        orderFlow.Output(fileStream)
        fileStream.Close()
    else:
        if not fileName.endswith('.cfof'):
            fileName = fileName + '.cfof'
        stringStream = acm.FCharacterOutputStringStream()
        orderFlow.Output(stringStream)
        archive = acm.FXmlArchive()
        archive.Add('orderFlow', stringStream.AsString())
        file = open(fileName, 'w')
        file.write(archive.Compressed())
        file.close()
