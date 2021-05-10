""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecurityLoanDealCustom/etc/FSecLendDealTradeActionCommands.py"
import acm
from DealTradeActionCommands import DealCloseCommand, AsFArray
from DealPackageCommandActionUtils import CommandActionBase
from DealPackageUtil import SetNew


class ReturnCommand(DealCloseCommand):
    DISPLAY_NAME = 'Return'

    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionReturn',
            self.DealPackage().GUI(), 
            self.KeyWordArguments())
        return AsFArray(newDp)


class RecallCommand(ReturnCommand):
    DISPLAY_NAME = 'Recall'

    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionRecall',
            self.DealPackage().GUI(), 
            self.KeyWordArguments())
        return AsFArray(newDp)


class IncreaseCommand(DealCloseCommand):
    DISPLAY_NAME = 'Increase'

    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionIncrease',
            self.DealPackage().GUI(), 
            self.KeyWordArguments())
        return AsFArray(newDp)
        
class LinkTradeCommand(DealCloseCommand):
    DISPLAY_NAME = 'Link Trade'

    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionLink', 
            self.DealPackage().GUI(),
            self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        return not self.DealPackage().Trades().First().Originator().IsInfant()


class RerateCommand(CommandActionBase):
    DISPLAY_NAME = 'Rerate'

    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionRerate', 
            self.DealPackage().GUI(),
            self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        trade = self.DealPackage().Trades().First()
        isInfant = trade.Originator().IsInfant()
        allowedStatus = False if trade.Status() == 'Simulated' else True
        return not isInfant and allowedStatus

    def Buttons(self):
        return 'NoButtons'


class ExtendCommand(CommandActionBase):
    DISPLAY_NAME = 'Extend'

    def Invoke(self,*args):
        newDp = acm.DealPackage.NewAsDecorator(
            'SecurityLoanTradeActionExtend', 
            self.DealPackage().GUI(),
            self.KeyWordArguments())
        return AsFArray(newDp)
    
    def Enabled(self):
        trade = self.DealPackage().Trades().First()
        isInfant = trade.Originator().IsInfant()
        allowedStatus = False if trade.Status() == 'Simulated' else True
        return not isInfant and allowedStatus

    def Buttons(self):
        return 'NoButtons'
