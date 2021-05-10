import acm
from MakeInstrument import MakeInstrument


def CustomMakeInstrumentItems():
    return []
    
    
"""
# MakeInstrument is a base class for creating make instrument actions. 
# To add a new make instrument action, the following steps should be performed
# 1. Create a new class for the action which inherits from MakeInstrument
# 2. Implement the interface methods Label, Applicable and Invoke
# 3. Add an instance of the class in the array that is returned in CustomMakeInstrumentItems

class MakeInstrument():

    # Interface methods. MUST be implemented. 
    
    def Label(self):
        # Return the label that will be displayed in the Make Instrument menu.
        # If the name matches an allready existing make instrument action, the existing
        # action will be replaced by the new action
        
    def Applicable(self, instrumentOrTrade):
        # Return True if the action can be performed for the current instrument or trade
        
    def Invoke(self, instrumentOrTrade):
        # Called when selecting the action from the menu. This method should start an 
        # instrument definition window with the new instrument/trade
    
        
    # Utility methods. These are helper methods that can be used when implementing the 
    # interface methods.
    
    def Instrument(self, instrumentOrTrade):
        # Returns the instrument from which the action was invoked
        
    def Trade(self, instrumentOrTrade):
        # Returns the trade from which the action was invoked (if any)
        
    def IsApplicationInProfile(self):
        # Returns True if there is an application component in the user profile 
        # with the same name as the make instrument action.
        # Can be used in the Applicable method if an application component has
        # been created for the action.
        
Example:

class MakeFlipFlopSwap(MakeInstrument):
    
    def Label(self):
        return 'Make Flip Flop Swap'
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        return ins and 'Bond' == ins.InsType()
 
    def Invoke(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        insDecorator = acm.FBusinessLogicDecorator.WrapObject(ins)
        swap = acm.DealCapturing().CreateNewInstrument('Swap')
        decorator = acm.FBusinessLogicDecorator.WrapObject(swap)
        decorator.LegStartDate = insDecorator.LegStartDate()
        decorator.LegEndDate = insDecorator.LegEndDate()
        decorator.Currency = insDecorator.Currency()
        decorator.FirstEditLeg().RollingPeriod = '5w'
        decorator.SecondEditLeg().RollingPeriod = '6w'
        
        trade = self.Trade(instrumentOrTrade)
        swapTrade = None
        if trade:
            swapTrade = trade.StorageNew()
            swapTrade.Instrument = swap
            swapTrade.InitializeUniqueIdentifiers()
        acm.StartApplication('Instrument Definition', swapTrade if swapTrade else swap)
        
def CustomMakeInstrumentItems():
    return [MakeFlipFlopSwap()]
        
"""        

