
from DealPackageDevKit import CompositeAttributeDefinition, Action, SetNew, DealPackageException
import acm
 
def CustomChoiceListPopulator(dp, attributeName):
    ''' 
    Override the logic for populating choice lists. The returned order will be the order shown in list.
        
    Parameters:
        dp - The deal package
        attributeName - the name of the attribute that the choice list is attached to
    Return:
        - Return None to use default logic
        - Return a list to override default behaviour.
        NOTE: If the items in the list that is being returned represent ACM entities, they should be
              returned as a list of ACM entities and not as a list of strings. Returning strings will
              still populate the list but the setting of default values will not work.
    
    Example:
        def CustomerChoiceListPopulator(dp, attributeName):
            # Limit the available currencies
            if attributeName == 'currency':
                currencyNames = ['CHF', 'DKK', 'EUR', 'GBP', 'NOK', 'SEK', 'USD']
                return [acm.FCurrency[c] for c in currencyNames]
            else:
                return None

            # Limit the available underlyings / reference instruments based
            # either the commodity group or a specific commodity
            if attributeName == 'underlying':
                if dp.GetAttribute('instrumentGroup').Name() == 'Precious Metals':
                    return [dp.GetAttribute('baseUnderlying')]
                else:
                    from CommodityStripPopulators import UnderlyingPopulator
                    underlyingChoices = UnderlyingPopulator(dp)
                    if dp.GetAttribute('baseUnderlying').Name() == 'ICE - BRENT CRUDE OIL':
                        return [und for und in underlyingChoices if und.InsType() == 'Rolling Schedule']
                    return underlyingChoices
    '''
    
    return None

def CustomAttributeOverrides(self, overrideAccumulator):
    '''
    Override labels, tooltips, onChanged etc on Deal Package (strip) level.
    
    paramters:
        self - An instance of the deal package
        overrideAccumulator - the override accumulator available in the AttributeOverrides method.
                              For more information on the override accumualtor and the method
                              AttributeOverrides, please referr to the Deal Package documentation.

    Usage:
        - Add attribute overrides to the overrideAccumulator variable.
        - Note that there is a dedicated hook for setting default values, do not use this hook for that
          purpose.

    Example:
        overrideAccumulator({'payType':dict(label='Pay Type')})
        
    '''
    pass

def CustomDealAttributeOverrides(self, overrideAccumulator):
    '''
    Override labels, tooltips, onChanged etc on Deal (instrument / trade) level.
    
    paramters:
        self - An instance of the deal package
        overrideAccumulator - the override accumulator available in the AttributeOverrides method.
                              For more information on the override accumualtor and the method
                              AttributeOverrides, please referr to the Deal Package documentation.

    Usage:
        - Add attribute overrides to the overrideAccumulator variable.
        
    '''
    pass

# Implement custom logix for setting expiry date on 
# a bullet future based on month and year.
# return None to use default logic.
def CustomGetBulletExpiryDate(underlying, month, year, useCurrentFuture):
    '''
    Custom logic for setting expiry date on bullet futures. By default,
    the expiry date of bullet futures part of the strip will always be
    set to the last banking day of the month.
    
    Parameters:
        underlying - the underlying / reference instrument
        month - the expiry month
        year - the expiry year
        useCurrentFuture - is each strip component using the equivalent future as reference instrument
    
    Return value:
        The expiry date. To use the default logic, return None.
        
    '''
    return None

def LiveTradesOrAll(dealPackage):
    '''
        Override the definition of what should be considered live trades. Used by the mapping
        between the strip and the individual trades when setting and updating trade status.
        
        An example of when this hook should be used is if there can be trade payments with a 
        pay date after instrument expiry date
        
        Parameters:
            dealPackage - the deal package
        
        Return value:
            Return a list of trade entities
        
    '''
    return [trade for trade in dealPackage.Trades() if dealPackage.DealPackage().IsLiveTrade(trade)]

def PageGroup(dealPackage):
    '''
        It is possible to add an additional layer of grouping in the application by using pages.
        When specifying a page with sub pages through this extension point, an additional drop down
        list will automatically appear above the Commodity field in the application. The values
        available in the commodities drop down list will be filtered based on the instruments available
        in the selected sub page.
        
        For information on how the pages should be set up please see the example in FCA 4862.
        
        If None is returned from this function, the additional drop down list will not be visible
        and all commodities set up in the system will be available to chose from in one drop down list.
        
        Example:
        def PageGroup(dealPackage):
            return acm.FPageGroup['CommodityGroups']
    '''
    return None

def SumForContractSize(quotation):
    ''' Return True for contract sizes in quotations that should be summed, for example MWh.

        Parameters:
            quotation - The name (note: not the nice name) of the quotation

        Example:
            def SumForContractSize(quotation):
                return quotation in ('MWh')
            
    '''
    return False

def DefaultStripType():
    '''
        Set the default strip type for when the application is started
    '''
    return 'Asian'
    
def StripDealTypeMapping():
    '''
        Return a mapping between the names of different strip types available in the application
        and the corresponding Deal definitions.
        
        Note 1: This extension point should only be used if custom deal definitions are used.
        
        Note 2: If a custom deal definition is used, it is necessary to also use the hooks
        CustomStripTypeFromInstruments, CustomExpiryTypeFromInstruments and 
        CustomStructureTypeFromInstruments.
    '''
    return {'Asian': 'CommodityStripDealAsian',
            'Bullet': 'CommodityStripDealBullet',
            'BulletOption': 'CommodityStripDealBulletOption' }

def CustomStripTypeFromInstruments(instruments):
    '''
        Specify how to determine the value of the deal package field stripType
        based on a a set of instruments.
        
        Return value:
            If no custom deal definitions are used, return None.
            The return value must be one of the dictionary keys returned by StripDealTypeMapping.
    '''
    return None
    
def CustomExpiryTypeFromInstruments(instruments):
    '''
        Specify how to determine the value of the deal package field expiryType
        based on a a set of instruments.
        
        Return value:
            If no custom deal definitions are used, return None.
    '''
    return None
    
def CustomStructureTypeFromInstruments(instruments):
    '''
        Specify how to determine the value of the deal package field structureType
        based on a a set of instruments.
        
        Return value:
            If no custom deal definitions are used, return None.
    '''
    return None

def SuggestInstrumentPackageName(dealPackage):
    '''
        Customize the suggested name of the instrument package. The hook will be
        called when <Suggest> button in the application is clicked as well as when
        an instrument package is saved for the first time if the Name field is empty.
        
        Tip: If the suggested name of a not yet saved instrument package should be updated 
             automatically when various input fields are updated and/or the strip components
             are updated, add the following line in the OnInstrumentsUpdated extension point:
             dealPackage.GetAttribute('suggestNameButton')()

    '''
    return ''
    
def OnInstrumentsUpdated(dealPackage, deal=None):
    '''
        Hook called after input that:
            - Resulted in a re-generation of the strip components
            - One or more components were removed from the strip
            - One or more Deal attributes were updated
        
        Note: If a Deal attribute is updated the hook is called for each affected deal.
        
        Parameters:
            dealPackage - the strip deal package
            deal - The deal if an attribute on the deal (strip component) has been updated.
    '''


    pass
    
def DealPackageDefaultValues(dealPackage):
    ''' 
    Set default values for the deal package attributes. Called from OnNew when the deal package is 
    infant (i.e. even if the instrument package is not infant, the hook will be called).
    
    Note: For instrument package attributes, use extension point InstrumentpackageDefaultValues.

    Parameters:
        dealPackage - the infant deal package
    Return format:
        A dictionary where each key-value pair corresponds to attribute name - default value
    
    Preferred return format of the actual default value is: 
        if attribute has a choice list, then return in the same domain as the choice list callback returns.
    For example: 
        If choice list callback returns a list of strings (for example names of instruments), then set detault value to a string
        If choice list callback returns a list of FObjects (for example instruments), then set detault value to an FObject

    Example:
        def DealPackageDefaultValues(dealPackage):
            default = {}
            default['portfolio'] = acm.FPhysicalPortfolio['Com Sales Prf']
            default['acquirer'] = acm.FParty['MyInstitution']
            return default
    '''
    return {}

def InstrumentPackageDefaultValues(dealPackage):
    ''' 
    Set default values for the instrument package attributes. Called from OnNew.
    
    Note: For deal package attributes, use extension point InstrumentpackageDefaultValues.

    Parameters:
        dealPackage - the infant deal package
    Return format:
        A dictionary where each key-value pair corresponds to attribute name - default value

    Preferred return format of the actual default value is: 
        if attribute has a choice list, then return in the same domain as the choice list callback returns.
    For example: 
        If choice list callback returns a list of strings (for example names of instruments), then set detault value to a string
        If choice list callback returns a list of FObjects (for example instruments), then set detault value to an FObject

    Example:
        def InstrumentPackageDefaultValues(dealPackage):
            default = {}
            default['stripDates_endDate'] = '6m'
            default['baseUnderlying'] = acm.FInstrument['ICE - BRENT CRUDE OIL']
            return default

    '''
    return {}

def GetConfig(dealPackage):
    return None

def InitTrade(trade):
    ''' 
    Use this hook to reset data on trade when instruments are regenerated, 
    or trades are copied to create new trades.

    Parameters:
        trade - the new (copied) trade
        
    Note: This method contains logic by default. If this extension point is used to add rather than override
          this default behaviour, make sure that the default bahviour is still being run.
    '''
    
    # Remove Payments
    for p in trade.Payments():
        p.Unsimulate() 

"""
    Import and export to excel
    --------------------------
    Use EXCEL_SEPARATOR and EXCEL_NEW_LINE to specify what characters to use
    for import and export to excel.
    
    Use the methods ExportHook and ImportHook to specify transplation between excel columns
    and attributes on the strip components.
    
    
    Note: The export and import buttons are disabled by default. If implementing logic
          in the excel extension points below it is necessary to also enable the buttons
          using the method CustomAttributeOverrides
    
"""
EXCEL_SEPARATOR = '\t'
EXCEL_NEW_LINE = '\n'

def ExportHook(dealPackage):
    ''' 
    Use this hook to transfer data from the strip components to the clip board

    Parameters:
        the deal package
    
    Return value:
        A matrix (python list of python lists) containing the rows that will be available to
        paste into excel.

    Example:
        dataAsMatrix = []
        stripComponents = dealPackage.GetAttribute('stripComponents')
        for component in stripComponents:
            dataRow = []
            dataRow.append(component.GetAttribute('quantity_buySell'))
            dataRow.append(component.GetAttribute('quantity_value'))
            dataRow.append(component.GetAttribute('endDate'))
            dataAsMatrix.append(dataRow)
        return dataAsMatrix
    '''
    pass
    
def ImportHook(dealPackage, data):
    ''' 
    Use this hook to transfer data from the clip board to the strip components.

    Parameters:
        dealPackage - the deal package
        data        - the clip board data copied from excel
    
    Example:
        stripComponents = dealPackage.GetAttribute('stripComponents')
        for (row,component) in zip(data,stripComponents):
            component.SetAttribute('price',row[0])
    '''
    pass
    
class CustomAttributes(CompositeAttributeDefinition):
    # Use this class to specify additional, customer specific attributes/fields to be 
    # shown in the Commodity Strip GUI.
    
    def OnInit(self, **kwargs):
        self._tradesMethod      = kwargs['tradesMethod']
        self._instrumentsMethod = kwargs['instrumentsMethod']
        self._stripComponents   = kwargs['stripComponents']
        self._templateModel     = kwargs['templateModel']
        
    def Trades(self):
        return self.GetMethod(self._tradesMethod)()
    
    def Instruments(self):
        return self.GetMethod(self._instrumentsMethod)()
    
    def StripComponents(self):
        return self.GetMethod(self._stripComponents)()

    def TemplateModel(self):
        return self.GetMethod(self._templateModel)()

    def Attributes(self):
        return {
                }
    
    def GetLayout(self):
        # Use this if the custom attributes defined in this class should 
        # automatically be added to the UI without updating the layout 
        # extension value
        return self.UniqueLayout("")

    def ModifyLayout(self, layout):
        # Use this to customize layout further, and return modified layout
        # For example:
        #    layout.insert(1, {'Details': """myAttribute"""})
        return layout

class CustomDealAttributes(CompositeAttributeDefinition):
    # Use this class to specify additional, customer specific attributes/fields on '
    # the Deal level.

    def Attributes(self):
        return {
                }

    def OnInit(self, **kwargs):
        self._tradeMethod      = kwargs['tradeMethod']
        self._instrumentMethod = kwargs['instrumentMethod']

    def Trade(self):
        return self.GetMethod(self._tradeMethod)()
    
    def Instrument(self):
        return self.GetMethod(self._instrumentMethod)()

class CustomDealBulletAttributes(CustomDealAttributes):
    # Use this class to specify additional, customer specific attributes/fields on '
    # the Bullet Deal level.
    def Attributes(self):
        baseAttributes = super(CustomDealBulletAttributes, self).Attributes()
        return baseAttributes

class CustomDealAsianAttributes(CustomDealAttributes):
    # Use this class to specify additional, customer specific attributes/fields on '
    # the Asian Deal level.
    def Attributes(self):
        baseAttributes = super(CustomDealAsianAttributes, self).Attributes()
        return baseAttributes
        
def SetDefaultValuesOnChange(dealPackage, updatedAttributes):
    '''
    This extension point is called from the Deal Package Refresh method whenever 
    one or more attributes have been updated. Use this method to update values or set 
    default based on these attribute changes.
    
    Parameters:
        dealPackage - the deal package
        updatedAttributes - a list of all attributes that have changed since the method 
                            was called the last time
    

    Example:
        def SetDefaultValuesOnChange(dealPackage, updatedAttributes):
            if 'instrumentGroup' in updatedAttributes:
                if dealPackage.GetAttribute('instrumentGroup').Name() == 'Metals':
                    dealPackage.SetAttribute('portfolio', 'Metals Prf')
    '''
    pass

def SelectMonthFuture(allMonthFutures):
    '''
    Select current future for a certain month
    
    Parameters:
        allMonthFutures - a sorted python list containing all futures with the same expiry month.
                          The list is sorted on expiry date
    
    Return Format:
        Return the future that should be used as underlying in the strip for the month.
    
    Default:
        Returns the future with the latest expiry date
    '''
    return allMonthFutures[len(allMonthFutures) - 1]

def CommodityCanUseCurrentFuture(commodity):
    '''
    Specify if the functionality "Use Current Future" should
    be available for a certain commodity or not.
    
    Parameters:
        commodity - an FCommodity object
    
    Return Format:
        Return a boolean
            - True:  Use current future is available if at least
                     2 futures are available within the entered period
            - False: Use current future should not be available for this
                     commodity
    '''
    return True

def IsValid(self, exceptionAccumulator, aspect):
    '''
    Custom validation of a strip. Called from the Commodity Strip Deal Package method IsValid.
    For information on how to use the IsValid method and its parameters see Deal Package documentation.
    '''
    return True
    
def OnSave(self, config):
    '''
    Possibility to customize the OnSave behavious. Called from the Commodity Strip Deal Package method OnSave.
    For information on how to use the OnSave method and its parameters see Deal Package documentation.
    
    Note: This method contains logic by default. If this extension point is used to add rather than override
          this default behaviour, make sure that the default bahviour is still being run.
    
    '''

    # Help Methods
    def _InsPackageInstrumentsModified():
        if _InfantInstrumentsInPersistedDealStructures():
            return True
        newInstruments = self.Instruments()     
        originalLinks = self.DealPackage().InstrumentPackage().Originator().InstrumentLinks()
        originalInstruments = acm.FArray()
        for inslink in originalLinks:
            originalInstruments.Add(inslink.Instrument().Originator().StorageId())
        for ins in newInstruments:
            if ins.Originator().StorageId() not in originalInstruments:
                return True
        if len(newInstruments) != len(originalInstruments):
                return True
        return False
    
    def _ContainsPersistentDealPackage(dealPackages):
        if _InfantInstrumentsInPersistedDealStructures():
            return True
        else:
            if dealPackages:
                for dealpackage in dealPackages:
                    for trade in dealpackage.Trades():
                        tradeOriginator = trade.Originator()
                        if not tradeOriginator.IsClone() and not tradeOriginator.IsInfant():
                            return True            
        return False
    
    def _InfantInstrumentsInPersistedDealStructures():
        dealPackage = self.DealPackage().Originator()
        insPackage = dealPackage.InstrumentPackage().Originator()   
        if dealPackage.Oid() > 0 and insPackage.Oid() > 0:
            for ins in self.Instruments():
                if ins.Originator().IsInfant():
                    return True    
        return False
    
    def _ReplaceExistingInstrumentPackage(config):
        insPackage = self.DealPackage().InstrumentPackage()
        if insPackage.IsInfant() or config.InstrumentPackage() == "SaveNew":
            existingInsPackage = acm.FInstrumentPackage[insPackage.Name()]
            if existingInsPackage:
                config.InstrumentPackage('Exclude')
                existingInsPackage = existingInsPackage.StorageImage()
                currentInsPackage = self.DealPackage().InstrumentPackage()
                self.DealPackage().InstrumentPackage(existingInsPackage)

    def _ValidateInstrumentPackageName():
        return self.insPackageName == self.DealPackage().InstrumentPackage().Originator().Name()
            
    # Implementation
    if config.DealPackage() == "SaveNew":
        config.InstrumentPackage("SaveNew")
        self.DealPackage().Name('')
        saveAsNewTrades = self.Trades()
        SetNew(saveAsNewTrades)
    if config.InstrumentPackage() == 'Save' and not self.DealPackage().InstrumentPackage().IsInfant()\
        and _ContainsPersistentDealPackage(self.InstrumentPackage().Originator().DealPackages())\
            and (_InsPackageInstrumentsModified() or not _ValidateInstrumentPackageName()):
        raise DealPackageException('Cannot save instrument package when current instrument package holds deal packages.')
    _ReplaceExistingInstrumentPackage(config)

    
