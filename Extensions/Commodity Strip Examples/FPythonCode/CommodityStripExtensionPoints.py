
from CommodityStripExtensionPointsBase import *
from CommodityStripExtensionPointsBase import CustomAttributes as CustomAttributesBase
from DealPackageDevKit import NoOverride, DealPackageUserException
from CommodityStripExamplesUtils import GetContractSizeForQuotedInHours, IsQuotedInHoursPerPeriod, GetSuggestedPriceAsian, StandardLinearAsianStripName, MondayBeforeThirdWednesday, IsAgricultural, GetFirstFuture, IsStandardMonthStrip
import math

import acm

'''
    Use cases:
        - Set contract size for electricity instruments
        - Set suggested strip price
'''
def OnInstrumentsUpdated(dealPackage, deal=None):    
    if deal:
        # - Set contract size for electricity instruments
        baseUnderlying = deal.GetAttribute('baseUnderlying')
        if IsQuotedInHoursPerPeriod( baseUnderlying ):
            contrSize = GetContractSizeForQuotedInHours(deal)
        else:
            contrSize = 1.0 
        deal.Instruments().First().ContractSizeInQuotation( contrSize )

    # - Set suggested strip price
    #   NOTE: This example has only been implemented for Asian forward strips. Because
    #         no suggested price is implemented for other strip types, the extension point
    #         SetDefaultValuesOnChange has been used to set price to 0 when chaning to other
    #         strip types.
    if dealPackage.GetAttribute('stripType') == 'Asian':
        theorStrip = GetSuggestedPriceAsian(dealPackage)
        if not math.isnan(theorStrip):
            dealPackage.SetAttribute("price", round(theorStrip, 2))

'''
    Use case:
        - Custom name for strip
'''
def SuggestInstrumentPackageName( dealPackage ):
    type = dealPackage.GetAttribute('stripType')
    if type == 'Asian':
        if IsStandardMonthStrip(dealPackage):
            return StandardLinearAsianStripName( dealPackage, type )
        else:
            pass # Proprietary suggest name logic currentyly only implemented for standard, full-month strips
    else:
        pass # Proprietary suggest name logic currentyly only implemented for linear, Asian strips


'''
    Use case:
        - Set default expiry for standard bullets
'''
def CustomGetBulletExpiryDate(underlying, month, year, useCurrentFuture):
    if not useCurrentFuture and underlying.UnderlyingOrSelf().Name() == 'LME - COPPER':
        expiryDateOnly = MondayBeforeThirdWednesday(year, month)
        # Set expiry time to 22:59
        dateAsTime = acm.Time.DateTimeToTime(expiryDateOnly)
        return acm.Time.DateTimeFromTime(dateAsTime + 82740)
    return None


'''
    Use cases:
        - Limit the choices available for drop down lists (currency, fx source and fixing source)
        - Limit underlying choices based commodity or commodity type
'''
def CustomChoiceListPopulator(dp, attributeName):
    if attributeName == 'currency':
        currencyNames = ['CHF', 'DKK', 'EUR', 'GBP', 'NOK', 'SEK', 'USD']
        return [acm.FCurrency[c] for c in currencyNames]
    if attributeName == 'fxSource':
        markets = ['BFIX', 'ECB', 'WM', 'internal']
        return [acm.FMTMMarket[m] for m in markets]
    if attributeName == 'fixingSource':
        markets = ['internal', 'LBMA PM', 'LME MID', 'LME OFFER']
        return [acm.FMTMMarket[m] for m in markets]
    if attributeName == 'underlying':
        if dp.GetAttribute('stripType') == 'Asian':
            # Use case: Only allow the commodity itself as reference instrument for a certain instrument group
            if dp.GetAttribute('instrumentGroup') and dp.GetAttribute('instrumentGroup').Name() == 'Precious Metals':
                return [dp.GetAttribute('baseUnderlying')]
            else:
                # Use case: Only allow rolling schedules as ref instruments for a certain commodity
                from CommodityStripPopulators import UnderlyingPopulator
                underlyingChoices = UnderlyingPopulator(dp)
                if dp.GetAttribute('baseUnderlying').Name() == 'ICE - BRENT CRUDE OIL':
                    allRollingSchedules = [und for und in underlyingChoices if und.InsType() == 'Rolling Schedule']
                    if allRollingSchedules == []:
                        pass
                        #print ('WARNING: No rolling schedules available for %s' % (dp.GetAttribute('baseUnderlying').Name()))
                    return allRollingSchedules
                return underlyingChoices
    return None

'''
    Use case:
        - Introduce a page group in order to create an extra grouping/filter in the application
'''    
def PageGroup(dealPackage):
    return acm.FPageGroup['CommodityGroups']


'''
    Use cases:
        - Set default values (e.g. portfolio) based on the selected commodity group
        - Set default underlying (e.g. first future) based on selected commodity
        - Set default values (e.g. pay day offset) based on selected commodity
'''
def SetDefaultValuesOnChange(dealPackage, updatedAttributes):
    # Set default portfolio based on commodity group
    if 'instrumentGroup' in updatedAttributes:
        if dealPackage.GetAttribute('instrumentGroup').Name() == 'Metals':
            dealPackage.SetAttribute('portfolio', 'Commodities')

    # Set default underlying future based on the selected commodity
    if 'baseUnderlying' in updatedAttributes and dealPackage.GetAttribute('stripType') == 'Asian':
        commodity = dealPackage.GetAttribute('baseUnderlying')
        if IsAgricultural( commodity ):
            f = GetFirstFuture( dealPackage, dealPackage.GetAttribute('stripDates_endDate') )
            if f:
                dealPackage.SetAttribute('underlying', f)

    # Set default pay day offset based on the commodity
    if 'baseUnderlying' in updatedAttributes:
        if IsAgricultural( dealPackage.GetAttribute('baseUnderlying') ):
            dealPackage.SetAttribute('payDayOffset', 5)
        else:
            dealPackage.SetAttribute('payDayOffset', 2)

    # Set suggested price to 0 when chaning strip type. The extension point
    # OnInstrumentsUpdated has an example for Asian forward strips on how
    # to set the suggested price based on teh theoretical value of the strip.
    if 'stripType' in updatedAttributes or 'isOptionStrip' in updatedAttributes:
        dealPackage.SetAttribute('price', 0)

'''
    Use case:
        - Set instrument package default values when starting application
'''
def InstrumentPackageDefaultValues(dealPackage):

    defaultInstrumentGroup = 'Energy'
    defaultBaseUnderlying = 'ICE - BRENT CRUDE OIL'
    defaultUnderlying = 'BRENT FRONT MONTH'
    default = {}
    
    # Set default instrument group
    # ----------------------------
    instrumentGroup = acm.FPhysInstrGroup[defaultInstrumentGroup]
    pageGroup = PageGroup(None)
    # Only set the instrument group if a page group has been defined and if it is a valid instrument group
    setInstrumentGroup = pageGroup and instrumentGroup and instrumentGroup.SuperGroup() == pageGroup
    if setInstrumentGroup:
        default['instrumentGroup'] = instrumentGroup

    # Set default base underlying
    # ---------------------------
    baseUnderlying = acm.FCommodity[defaultBaseUnderlying]
    if baseUnderlying and setInstrumentGroup and (not baseUnderlying in instrumentGroup.Instruments()):
        #print ('WARNING: Cannot set %s as default base underlying, not part of group %s' % (defaultBaseUnderlying, defaultInstrumentGroup))
        if instrumentGroup.Instruments():
            baseUnderlying = instrumentGroup.Instruments().First()
    # Only set base underlying if it is a valid commodity
    if baseUnderlying:
        default['baseUnderlying'] = baseUnderlying

    # Set default underlying (i.e. reference instrument)
    # --------------------------------------------------
    underlying = acm.FInstrument[defaultUnderlying]
    # Only set underlying if it is a valid instrument and a valid selection based on default
    # instrument group and default base underlying.
    setUnd = underlying and ((baseUnderlying and underlying.UnderlyingOrSelf() == baseUnderlying) or
                              (setInstrumentGroup and underlying.UnderlyingOrSelf() in instrumentGroup.Instruments()) or
                              (not (baseUnderlying or setInstrumentGroup)))
    if setUnd:
        default['underlying'] = underlying
    else:
        pass
        #print ('WARNING: %s is not a valid default reference instrument according to the default instrument group or default base underlying' % defaultUnderlying)

    return default

'''
    Use case:
        - Set deal package default values when starting application
'''
def DealPackageDefaultValues(dealPackage):
    default = {}
    counterparty = acm.FParty['Sandvik AB']
    if counterparty:
        default['counterParty'] = counterparty

    portfolio = acm.FPhysicalPortfolio['CommoditySales']
    if portfolio:
        default['portfolio'] = portfolio

    acquirer = acm.FParty['Commodity Desk']
    if acquirer:
        default['acquirer'] = acquirer

    return default

'''
    Use case:
        - Enable exort to and import from Excel
        - NOTE: This example includes:
            - Global setting EXCEL_SEPARATOR
            - Global setting EXCEL_NEW_LINE
            - Method ExportHook
            - Method ImportHook
            - Setting meta data enabled to True for the import and export
              buttons using the method CustomAttributeOverrides.
'''

EXCEL_SEPARATOR = '\t'
EXCEL_NEW_LINE = '\n'

def ExportHook(dealPackage):
    dataAsMatrix = []
    stripComponents = dealPackage.GetAttribute('stripComponents')
    for component in stripComponents:
        dataRow = []
        dataRow.append(component.Instruments().First().Name())
        dataRow.append(component.GetAttribute('quantity_buySell'))
        dataRow.append(component.GetAttribute('quantity_value'))
        dataRow.append(component.GetAttribute('endDate'))
        dataAsMatrix.append(dataRow)
    return dataAsMatrix
    
def ImportHook(dealPackage, data):
    numberOfAttributes = 4
    stripComponents = dealPackage.GetAttribute('stripComponents')

    if len(data) != len(stripComponents):
        raise DealPackageUserException('Number of rows to import does not correspont to the number of strip components')
    if len(data[0]) != numberOfAttributes:
        raise DealPackageUserException('Expected exactly ' + numberOfAttributes + ' number of columns (' + len(data[0]) + ' given)')
    
    stripComponents = dealPackage.GetAttribute('stripComponents')
    for (row, component) in zip(data, stripComponents):
        component.SetAttribute('quantity_buySell', row[0])
        component.SetAttribute('quantity_value', float(row[1]))
        component.SetAttribute('endDate', row[2])
        component.SetAttribute('price', row[3])

'''
    Use case:
        - Customizing when certain fields should be visible or enabled
        - NOTE: This example includes both CustomAttributeOverrides
                and CustomAttributes
            - Visibility depending on show mode (slim or detail)
            - Always hide a ceratin field
            - Show mode (slim or detail) depending the value of certain fields
            - Show mode (slim or detail) depending on the number of available choices
            - How to add custom visibility logic that should be combined with core
              visibility rules.
        - NOTE: When adding custom visibility rules, make sure that core visibility rules
                are not accidently overridden.
'''
def CustomAttributeOverrides(self, overrideAccumulator):
    overrideAccumulator({'quotation':dict(visible='@IsShowModeDetail'),
                         'underlying':dict(visible='@customAttributes_DetailIfOnlyOneIfDefault'),
                         'payOffsetMethod':dict(visible='@customAttributes_NeverShow'),
                         'payDayMethod':dict(visible='@customAttributes_NeverShow'),
                         'convType':dict(visible='@customAttributes_ShowConversionType'),
                         'importStripComponents':dict(enabled=True),
                         'exportStripComponents':dict(enabled=True)})

class CustomAttributes(CustomAttributesBase):

    def Attributes(self):
        self.UniqueCallback('DetailIfOnlyOne')
        self.UniqueCallback('DetailIfOnlyOneIfDefault')
        self.UniqueCallback('NeverShow')
        self.UniqueCallback('ShowConversionType')
        return {} 
    
    # Visibility depends on deal package data
    def DetailIfOnlyOne(self, attrName, *rest):
        if self.GetMethod('GetAttributeMetaData')(attrName, 'choiceListSource')().GetChoiceListSource().Size() == 1:
            return self.GetMethod('IsShowModeDetail')()
        return NoOverride

    # Visibility depends on deal package data and default logic
    def DetailIfOnlyOneIfDefault(self, attrName, *rest):
        defaultLogic = self.GetMethod('DealIsVisibleAndNotUseCurrentFuture')(attrName)
        customLogic = self.DetailIfOnlyOne(attrName)
        return defaultLogic and customLogic
    
    # Never show a certain field
    def NeverShow(self, attrName, *rest):
        return False

    # Combine custom and default logic for visibility
    def ShowConversionType(self, attrName, *rest):
        defaultLogic = self.GetMethod('DealIsVisible')('convType')
        convTypeValue = self.GetMethod('GetAttribute')('convType')
        customLogic = convTypeValue == 'Average then convert' or self.GetMethod('IsShowModeDetail')()
        return defaultLogic and customLogic
        
