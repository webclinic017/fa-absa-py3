
import acm
from DealPackageDevKit import DealPackageDefinition, Object, Settings, InstrumentPart, Text, CounterpartyChoices, AcquirerChoices, TradeActions, CorrectCommand
from inspect import cleandoc

def UnderlyingChoices():
    return acm.FStock.Instances()

def FindAnyStockWithPrice():
    for stock in UnderlyingChoices():
        if stock.Prices():
            return stock
    return None



@TradeActions( correct = CorrectCommand(statusAttr='status', newStatus='FO Confirmed') )
@Settings(LogMode='Verbose',
          MultiTradingEnabled=True,
          SheetDefaultColumns=['Price Theor', 'Portfolio Underlying Price', 'Portfolio Underlying Forward Price', 
                               'Portfolio Volatility', 'Portfolio Carry Cost', 'Instrument Delta', 'Strike Price'])
class ProgrammaticInterface(DealPackageDefinition):
    """
    Example illustrating how to work with the Programmatic Python interface
    
    Basic Get/Set methods
        - GetAttributes
        - GetAttribute/SetAttribute
        - GetAttributeMetaData
        
    Save/Save New
        - How to use the FDealPackageSaveConfiguration
        
    Delete
        - How to delete a Deal Package or Instrument Package
        
    Python example available in Extension Manager
        - FPythonCode Module: ProgrammaticInterface_DPE
        
    The Python Method: BasicProgrammaticInterface
        - Basic Creation/SetAttribute/GetAttribute/Save/Update/Delete

    The Python Method: TradeActionsProgrammaticInterface
        - Deal Package Correction from Python
    """
    
    stockWithPrice = FindAnyStockWithPrice()
    
    name         = Object(  label='Name',
                            objMapping='InstrumentPackage.Name')
    
    underlying   = Object(  defaultValue=stockWithPrice,
                            label='Underlying',
                            objMapping=InstrumentPart('Option.Underlying'),
                            choiceListSource=UnderlyingChoices(),
                            onChanged='@SetCurrencyFromUnderlying')     

    currency     = Object(  defaultValue=stockWithPrice.Currency(),
                            label='Currency',
                            objMapping=InstrumentPart('Option.Currency').\
                                       DealPart('Trade.Currency') )

    optionType   = Object(  defaultValue='Call',
                            label='Type',
                            objMapping=InstrumentPart('Option.OptionType'),
                            choiceListSource=['Call', 'Put'])
    
    expiryDate   = Object(  defaultValue='3m',
                            label='Expiry',
                            objMapping=InstrumentPart('Option.ExpiryDate'),
                            transform='@TransformExpPeriodToDate')

    strike       = Object(  label='Strike',
                            objMapping=InstrumentPart('Option.StrikePrice'))

    quantity     = Object(  defaultValue=100,
                            label='Quantity',
                            objMapping='Trade.Quantity')
                           
    price        = Object(  label='Price',
                            objMapping='Trade.Price')
              
    premium      = Object(  label='Premium',
                            objMapping='Trade.Premium')
         
         
    acquirer     = Object(  label='Acquirer',
                            objMapping='Trade.Acquirer',
                            choiceListSource=AcquirerChoices()) 
                            
    counterparty = Object(  label='Counterparty',
                            objMapping='Trade.Counterparty',
                            choiceListSource=CounterpartyChoices()) 
         
    status       = Object(  label='Status',
                            objMapping='Trade.Status')
                           
    doc          = Text(    defaultValue=cleandoc(__doc__),
                            editable=False,
                            height=300,
                            width=400)  
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
  
    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Option', 'opt')
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_ProgrammaticInterface_DPE')
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
    
    def TransformExpPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Option().ExpiryDateFromPeriod(newDate)
        return newDate
    
    def SetCurrencyFromUnderlying(self, *args):
        self.currency = self.underlying.Currency()
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Option(self):
        return self.InstrumentAt('opt')
     
    def Trade(self):
        return self.TradeAt('opt')

'''******************************************************************************
* Examples on how to programmatically interact with the Deal Package framemwork
******************************************************************************'''
def CreateNewDealPackage():
    # Create a new instance of a Deal Package
    newDealPackage = acm.DealPackage().NewAsDecorator('ProgrammaticInterface')
    return newDealPackage
    
def BasicGetSetAttributes(newDealPackage):
    # Print all the attributes on the Deal Package instance
    for attribute in newDealPackage.GetAttributes():
        print (attribute)

    # Get the value of all the attributes
    for attribute in newDealPackage.GetAttributes():
        print (attribute, newDealPackage.GetAttribute(attribute))

    # Set the value of the attribute strike, and print the updated value
    newDealPackage.SetAttribute('strike', 12)    
    print (newDealPackage.GetAttribute('strike'))

    #Access the meta data, e.g. label, describing the expiryDate attribute
    print (newDealPackage.GetAttributeMetaData('expiryDate', 'label')())

def SaveNewInstrumentAndDealPackage(newDealPackage):
    # The FDealPackageSaveConfiguration is used to parameterize what parts should be saved
    saveConfig = acm.FDealPackageSaveConfiguration()
    saveConfig.InstrumentPackage = 'SaveNew'
    saveConfig.DealPackage = 'SaveNew'

    savedDealPackage = newDealPackage.Save(saveConfig).First()
    return savedDealPackage
    
def InstrumentPackageNameFromDealPackage(savedDealPackage):
    # Access the Instrument Package from a Deal Package
    instrumentPackage = savedDealPackage.InstrumentPackage()
    return instrumentPackage.Name()
    
def OpenAndCreateEditableDealPackageCopyFromInstrumentPackageName(instrumentPackageName):
    instrumentPackage = acm.FInstrumentPackage[instrumentPackageName]
    
    # Create a new Deal Package from an existing Instrument Package
    newDealPackageInExistingInstrumentPackage = acm.DealPackage().NewAsDecoratorFromInstrumentPackage(instrumentPackage)

    return newDealPackageInExistingInstrumentPackage
    
def CreateEditableCopy(savedDealPackage):
    editableDealPackage = savedDealPackage.Edit()
    return editableDealPackage
    
def SaveNewDealPackageInExistingInstrumentPackage(editableDealPackage):
    # Parameterize to only save a new Deal Package
    saveConfig = acm.FDealPackageSaveConfiguration()
    saveConfig.InstrumentPackage = 'Exclude'
    saveConfig.DealPackage = 'SaveNew'
    
    savedDealPackage = editableDealPackage.Save(saveConfig).First()
    return savedDealPackage
    
def UpdateExistingDealPackageAndSave(editableDealPackage):
    # Set a Deal Package Attribute
    editableDealPackage.SetAttribute('strike', 13)
    
    # Parameterize to only save the existing Deal Package
    saveConfig = acm.FDealPackageSaveConfiguration()
    saveConfig.InstrumentPackage = 'Exclude'
    saveConfig.DealPackage = 'Save'
    updatedDealPackage = editableDealPackage.Save(saveConfig).First()

def GetAllDealPackagesFromInstrumentPackageName(instrumentPackageName):
    instrumentPackage = acm.FInstrumentPackage[instrumentPackageName]
    allDealPackages = instrumentPackage.DealPackages()
    return allDealPackages

def DeleteAllDealPackagesIncludingTrades(allDealPackages):
    for dealPackage in allDealPackages:
        dealPackage.Delete(True, True)
       
def DeleteInstrumentPackage(instrumentPackageName):
    instrumentPackage = acm.FInstrumentPackage[instrumentPackageName]
    # DELETE HERE

def SetDealPackageAttributes(newDealPackage):
    import ChoicesExprTrade
    newDealPackage.SetAttribute('quantity', 100)    
    newDealPackage.SetAttribute('price', 123)
    newDealPackage.SetAttribute('acquirer', ChoicesExprTrade.getAcquirers()[0])
    newDealPackage.SetAttribute('counterparty', ChoicesExprTrade.getCounterparties()[0])
    newDealPackage.SetAttribute('status', 'FO Confirmed')

def CreateCorrectionDealPackage(savedDealPackage):    
    correctAction = savedDealPackage.TradeActionAt('correct')
    correctionDealPackage = correctAction.Invoke().First()
    return correctionDealPackage 
    
def ModifyCorrectionDealPackage(correctionDealPackage):
    correctionDealPackage.SetAttribute('correct_price', 124)
    correctionDealPackage.SetAttribute('text1', 'Reason for amendment: wrong input')
    
def CommitCorrectionDealPackage(correctionDealPackage):
    # The FDealPackageSaveConfiguration is used to parameterize what parts should be saved
    saveConfig = acm.FDealPackageSaveConfiguration()
    saveConfig.InstrumentPackage = 'Exclude'
    saveConfig.DealPackage = 'SaveNew'
    correctionDealPackage.Save(saveConfig)
    
def BasicProgrammaticInterface():
    # Create a new Deal Package
    newDealPackage = CreateNewDealPackage()

    # Get/Set Deal Package attributes
    BasicGetSetAttributes(newDealPackage)

    # Save the Deal Package and the Instrument Package
    savedDealPackage = SaveNewInstrumentAndDealPackage(newDealPackage)

    # Get the Instrument Package name from a Deal Package
    instrumentPackageName = InstrumentPackageNameFromDealPackage(savedDealPackage)

    # Open an existing Instrument Package from name, and create a new Deal Pacakge
    newDealPackageInExistingInstrumentPackage = OpenAndCreateEditableDealPackageCopyFromInstrumentPackageName(instrumentPackageName)

    # Save a new Deal Package in the already existing Instrument Package
    savedDealPackage = SaveNewDealPackageInExistingInstrumentPackage(newDealPackageInExistingInstrumentPackage)

    # Create an editable copy of a Deal Package
    editableDealPackage = CreateEditableCopy(savedDealPackage)

    # Update an existing Deal Package and Save
    UpdateExistingDealPackageAndSave(editableDealPackage)

    # Find all Deal Pacakges from Instrument Package Name
    allDealPackages = GetAllDealPackagesFromInstrumentPackageName(instrumentPackageName)

    # Delete all the Deal Packages and the Trades
    DeleteAllDealPackagesIncludingTrades(allDealPackages)

    # Delete the Instrument Package and the Instruments
    DeleteInstrumentPackage(instrumentPackageName)

    return True

def TradeActionsProgrammaticInterface():
    # Create a new Deal Package
    newDealPackage = CreateNewDealPackage()

    # Set Deal Package Attributes 
    SetDealPackageAttributes(newDealPackage)

    # Save the Deal Package and the Instrument Package
    savedDealPackage = SaveNewInstrumentAndDealPackage(newDealPackage).Edit()

    # Create a Correction Deal Package instance
    correctionDealPackage = CreateCorrectionDealPackage(savedDealPackage)

    # Modify Deal Package Attributes
    ModifyCorrectionDealPackage(correctionDealPackage)

    # Commit Correction Deal Package
    CommitCorrectionDealPackage(correctionDealPackage)
    
    return True
