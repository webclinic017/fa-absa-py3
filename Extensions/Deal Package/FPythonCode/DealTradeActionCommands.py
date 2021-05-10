import acm
from DealPackageTradeActionCommands import CorrectCommand, CloseCommand, NovateCommand, MirrorCommand

def AsFArray(obj):
    array = acm.FArray()
    array.Add(obj)
    return array
    
class DealCorrectCommand(CorrectCommand):

    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator('DealTradeActionCorrect', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
        
class DealNovateCommand(NovateCommand):
    
    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('DealTradeActionNovate', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)

class DealCloseCommand(CloseCommand):
    
    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('DealTradeActionClose', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)

class DealMirrorCommand(MirrorCommand):

    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('DealTradeActionMirror', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
