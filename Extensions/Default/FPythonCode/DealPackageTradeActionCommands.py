import acm
from DealPackageCommandActionUtils import CommandActionBase
from DealPackageUtil import ValidateDealPackageToBeMirrored


def AsFArray(obj):
    array = acm.FArray()
    array.Add(obj)
    return array
    
class CorrectCommand(CommandActionBase):
    DISPLAY_NAME = 'Correct'
    
    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator('TradeActionCorrect', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        enabled = False
        try:
            enabled = acm.DealPackageActions.ValidateDealPackageToBeCorrected(self.DealPackage())
        except Exception as e:
            return False
        return enabled
        

class CloseCommand(CommandActionBase):
    DISPLAY_NAME = 'Close'
    
    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('TradeActionClose', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        try:
            enabled = acm.DealPackageActions.ValidateDealPackageToBeClosed(self.DealPackage())
        except Exception as e:
            return False
        return enabled

class NovateCommand(CommandActionBase):
    DISPLAY_NAME = 'Novate'
    
    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('TradeActionNovate', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        try:
            enabled = acm.DealPackageActions.ValidateDealPackageToBeNovated(self.DealPackage())
        except Exception as e:
            return False
        return enabled

class MirrorCommand(CommandActionBase):
    DISPLAY_NAME = 'Mirror'
    
    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator('TradeActionMirror', self.DealPackage().GUI(), self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        try:
            enabled = ValidateDealPackageToBeMirrored(self.DealPackage())
        except Exception as e:
            return False
        return enabled
