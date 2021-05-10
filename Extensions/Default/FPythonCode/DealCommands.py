import acm
from DealPackageCommandActionUtils import CommandActionBase

class SwitchLegsCommand(CommandActionBase):
    DISPLAY_NAME = 'Switch Legs'
    PARENT = 'View'
    TOOL_TIP = 'Move all Pay leg data to the Receive leg and vice versa'
    
    def Invoke(self, cd=None):
        self.DealPackage().Instruments().First().SwitchLegs()
        rcc = self.DealPackage().GetAttribute('refreshCalcCounter')
        self.DealPackage().SetAttribute('refreshCalcCounter', rcc+1)
        
    def Applicable(self):
        return self.DealPackage().IsDeal() and self.DealPackage().Instruments().First().IsSwap()
