import acm
from ExtensionPointUtil import DefaultValGroup
from DealPackageDevKit import CompositeAttributeDefinition, Object
INCREASED_PRECISION = 0
        
def DefaultFXInstrumentOverride(defaultInstrumentForeignCurrency, defaultInstrumentDomesticCurrency, defaultInstrumentExpiryDate):
    # use this method to override the Currency Pair and Expiry Date when creating a new FX Option
    foreignCurrency = defaultInstrumentForeignCurrency if defaultInstrumentForeignCurrency else 'EUR'
    domesticCurrency = defaultInstrumentDomesticCurrency if defaultInstrumentDomesticCurrency else 'USD'
    expiryDate = defaultInstrumentExpiryDate if acm.Time().DateDifference(acm.Time().DateToday(), defaultInstrumentExpiryDate) < 0 else '3m'
    
    return foreignCurrency, domesticCurrency, expiryDate

def DefaultPMInstrumentOverride(defaultInstrumentPreciousMetal, defaultInstrumentDomesticCurrency, defaultInstrumentExpiryDate):
    # use this method to override the Precious Metal Pair and Expiry Date when creating a new PM Option
    preciousMetal = defaultInstrumentPreciousMetal if defaultInstrumentPreciousMetal else 'XAU oz'
    domesticCurrency = defaultInstrumentDomesticCurrency if defaultInstrumentDomesticCurrency else 'USD'
    expiryDate = defaultInstrumentExpiryDate if acm.Time().DateDifference(acm.Time().DateToday(), defaultInstrumentExpiryDate) < 0 else '3m'
    
    return preciousMetal, domesticCurrency, expiryDate

def PreciousMetalChoiceList(pmOption):
    # Use this method to override the available Precious Metal Commodity Variants in the Drop Down list 
    return pmOption.DefaultPreciousMetals()

def ValuationGroupOverride(baseType):
    # Use this method to set override the Valuation Group on the Instrument. 
    # The method will be called when creating a new Option and when the Option Base Type is changed.
    # Return an intance of the class DefaultValGroup (as below) to override value, 
    # - return None -> disables the use of the override method
    # - return DefaultValGroup(None) - will set the Valuation Group on the Instrument to None 
    # - return DefaultValGroup('Vanna-Volga') - Will set the Valuation Group on the Instrument to 'Vanna-Volga'
    return None
    
def IgnoreCellsInTabOrder():
    # Use this method to list cells that will be ignored when tabbing through the UI grid
    return ['deliveryDate', 'intrinsicFwd']
    
def StartApplicationWithBidAskEnabled():
    # Use this method to specify if Bid/Ask valuation should be enabled as default
    return True
    
def TurnOffRealTimeUpdatesOnSimulation():
    # Use this method to specify if Real Time price and volatility updates should be disabled when simulating a calculated value
    return True


class CustomerAdditionalAttributes(CompositeAttributeDefinition):
    # Use this class to specify additional, customer specific attributes/fields to be 
    # shown in the Properties section in the GUI. An example of how to add OptKey1 field
    # is illustrated below. 
    
    def OnInit(self, tradeNames):
        self._tradeNames = tradeNames
        
    def Trades(self):
        return self._tradeNames
    
    def CustomerAttributes(self):
        # Define the attributes to be shown in the GUI.
        # Each attribute is defined as a key-value pair.
        # ------------------------------- Example ----------------------------------#
        # return { 'optTradeKey' :   Object( label='Optional Trade Key 1',
        #                                    objMapping=self.Trades()+'.OptKey1') }
        # --------------------------------------------------------------------------#
        
        return { }
                                                
    def GetLayout(self):
        # Define the layout of the attributes defined in 
        # CustomerAttributes. The order of the fields in
        # the GUI will be as specified here.
        #
        # -------------------- Example -----------------------#
        # return self.UniqueLayout(''' optTradeKey; ''')
        # ----------------------------------------------------#
        
        return self.UniqueLayout(''' ''')
        
    def Attributes(self):
        return dict(self.CustomerAttributes())
