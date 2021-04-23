
import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageException, ParseSuffixedFloat, Object, InstrumentPart, Delegate
from CommodityStripUtils import StripMonth, GetMonth, StripPriceFormatter, GetBulletExpiryDate
from CompositeAttributesLib import BuySell

class CommodityStripDates(CompositeAttributeDefinition):

    def Attributes(self):
        return {

                'startDate' :   Object (objMapping = InstrumentPart(self._objectMappingStart),
                                        label = 'Start Date',
                                        defaultValue = '1M',
                                        formatter = self.UniqueCallback('@StartDateFormatter'),
                                        transform = self.UniqueCallback('@TransformToStartMonth'),
                                        onChanged=self.UniqueCallback('@OnStartDateChanged')),

                'endDate' :     Object (objMapping = InstrumentPart(self._objectMappingEnd),
                                        label = 'End Date',
                                        defaultValue = '0M',
                                        formatter = self.UniqueCallback('@EndDateFormatter'),
                                        transform = self.UniqueCallback('@TransformToEndMonth'))

                }

    def OnInit(self, objectMappingStart, objectMappingEnd):
        self._objectMappingStart = objectMappingStart
        self._objectMappingEnd = objectMappingEnd

    def StartDateMonthAndYear(self):
        return (self.Owner().expiryType in ('Standard') or
                (self.Owner().expiryType in ('Custom') and self.Owner().stripType in ('Bullet')))

    def StartDateFormatter(self, *args):
        formatter = 'MonthAndYear' if self.StartDateMonthAndYear() else 'DateOnly'
        return acm.Get('formats/%s' % formatter)

    def EndDateFormatter(self, *args):
        formatter = 'MonthAndYear' if self.Owner().expiryType in ('Standard', 'Custom Settlement') else 'DateOnly'
        return acm.Get('formats/%s' % formatter)

    def MonthFromString(self, value):
        mapping = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}
        return mapping.get(value.upper(), None)

    def ParseMonthAndYear(self, value, now):
        monthString = value[:3]
        yearString = value[3:]
        current = acm.Time.DateToYMD(now)
        month = self.MonthFromString(monthString)
        year = None
        if len(yearString) == 2:
            year = str(current[0])[:2] + yearString
        elif len(yearString) == 4:
            year = yearString
        elif month:
            if month > current[1]:
                year = current[0]
            else:
                year = current[0] + 1
        elif isinstance(value, str) and len(value.split('-')) == 2:
            year, month = value.split('-')
        return month, year
    
    def StripMonth(self, date):
        ymd = acm.Time.DateToYMD(date)
        return StripMonth(ymd[1], ymd[0])
        
    def TransformToStartMonth(self, attrName, value, *rest):
        dateFromPeriod = acm.Time().PeriodSymbolToDate(value)
        if dateFromPeriod:
            return self.StripMonth(dateFromPeriod).FirstDayOfMonth()
        
        month, year = self.ParseMonthAndYear(value, acm.Time.DateNow())
        if month and year:
            return acm.Time.DateFromYMD(year, month, 1)
        
        if self.Owner().expiryType == 'Standard':
            return self.StripMonth(value).FirstDayOfMonth()
        return value

    def TransformToEndMonth(self, attrName, value, *rest):
        startDate = self.TransformToStartMonth(attrName, self.startDate) if self.startDate else acm.Time().PeriodSymbolToDate('1M')
        if acm.Time.IsValidDateTime(startDate):
            if acm.Time().PeriodSymbolToDate(value):
                endDate = acm.Time.DateAdjustPeriod(startDate, value)
                if self.Owner().stripType == 'Bullet':
                    stripMonth = self.StripMonth(endDate)
                    if self.Owner().useCurrentFuture is True:
                        return GetBulletExpiryDate(self.Owner().baseUnderlying, stripMonth.Month(), stripMonth.Year(), False)
                    else:
                        return GetBulletExpiryDate(self.Owner().underlying, stripMonth.Month(), stripMonth.Year(), False)
                return self.StripMonth(endDate).LastDayOfMonth()
            else:
                month, year = self.ParseMonthAndYear(value, startDate)
                if month and year:
                    if self.Owner().stripType == 'Bullet':
                        if self.Owner().useCurrentFuture is True:
                            return GetBulletExpiryDate(self.Owner().baseUnderlying, month, year, False)
                        else:
                            return GetBulletExpiryDate(self.Owner().underlying, month, year, False)
                    else:
                        day = acm.Time.DaysInMonth(acm.Time.DateFromYMD(year, month, 1))
                        return acm.Time.DateFromYMD(year, month, day)
                elif self.Owner().expiryType == 'Standard' and self.Owner().stripType == 'Bullet':
                    stripMonth = self.StripMonth(value)
                    return GetBulletExpiryDate(self.Owner().underlying, stripMonth.Month(), stripMonth.Year(), False)
                elif self.Owner().expiryType in ('Standard', 'Custom Settlement'):
                    return self.StripMonth(value).LastDayOfMonth()
        return value
        
    def OnStartDateChanged(self, *args):
        if self.endDate < self.startDate:
            self.endDate = '0M'

    def GetLayout(self):
        return self.UniqueLayout(
               """
                hbox(;
                    startDate;
                    endDate;
                    );
                """)


class CommodityStripOptionData(CompositeAttributeDefinition):
    def Attributes(self):
        return {

                'optionType':  Delegate(   attributeMapping = self.UniqueCallback('Deals') + '.optionType',
                                            label = 'C/P',
                                            toolTip = 'Call or Put',
                                            choiceListSource = ['Call', 'Put'],
                                            visible = self.UniqueCallback('@IsVisible')),

                'strikePrice': Delegate(   attributeMapping = self.UniqueCallback('Deals') + '.strikePrice',
                                            label = 'Strike',
                                            toolTip = 'Option strike price',
                                            visible = self.UniqueCallback('@IsVisible')),
                
                'quantity_value': Delegate( attributeMapping = self.UniqueCallback('Deals') + '.quantity_value',
                                            validateMapping=False,
                                            toolTip='@QuantityTooltip',
                                            visible = self.UniqueCallback('@IsVisible')),

                'quantity_buySell': Delegate( attributeMapping = self.UniqueCallback('Deals') + '.quantity_buySell',
                                            toolTip='Buy or Sell',
                                            validateMapping=False,
                                            visible = self.UniqueCallback('@IsVisible')),

                'b2bMargin':   Delegate(   attributeMapping = self.UniqueCallback('Deals') + '.b2bMargin',
                                            validateMapping=False,
                                            toolTip='@b2BMarginTooltip',
                                            formatter=StripPriceFormatter,
                                            visible = self.UniqueCallback('@IsVisibleAndB2B')),

                'b2bPrice':   Delegate(    attributeMapping = self.UniqueCallback('Deals') + '.b2bPrice',
                                            validateMapping=False,
                                            toolTip='@b2BPriceTooltip',
                                            formatter=StripPriceFormatter,
                                            visible = self.UniqueCallback('@IsVisibleAndB2B')),

                'price':       Delegate(   attributeMapping = self.UniqueCallback('Deals') + '.price',
                                            formatter=StripPriceFormatter,
                                            toolTip='@PriceTooltip',
                                            validateMapping = False,
                                            visible = self.UniqueCallback('@IsVisible')),

                'totalQuantity': Object (    objMapping = self.UniqueCallback('TotalQuantity'),
                                            visible = self.UniqueCallback('@IsVisible'),
                                            toolTip='@TotalQuantityTooltip',
                                            label = 'Total Qty'),
                                            
                'uti': Delegate(   attributeMapping = self.UniqueCallback('Deals') + '.uti',
                                            domain = 'string',
                                            label = 'UTI',
                                            validateMapping = False,
                                            visible = self.UniqueCallback('@IsVisible')),
                }

    def AttributeOverrides(self, overrideAccumulator):
        if self._nbr == 1:
            overrideAccumulator({'quantity_value':dict(label='Quantity'),
                                 'quantity_buySell':dict(label='B/S')})
        else:
            overrideAccumulator({'optionType': dict(label=''),
                                 'strikePrice': dict(label=''),
                                 'quantity_value': dict(label=''),
                                 'quantity_buySell': dict(label=''),
                                 'b2bMargin': dict(label=''),
                                 'b2bPrice': dict(label=''),
                                 'price': dict(label=''),
                                 'totalQuantity': dict(label=''),
                                 'uti': dict(label=''),})

    def Deals(self):
        return [deals[min(self._nbr, len(deals))-1] for deals in self.Owner().DealsPerMonth().values()]
    
    def TotalQuantity(self, value='NoValue'):
        if value == 'NoValue':
            return sum(deal.GetAttribute('quantity_value') for deal in self.Deals())
        else:
            numDeals = float(len(self.Deals()))
            for deal in self.Deals():
                deal.SetAttribute('quantity_value', float(value)/numDeals) 

    def OnInit(self, nbr):
        self._nbr = nbr
        
    def IsVisible(self, *args):
        return self.Owner().IsOptionStrip(None) and self._nbr <= self.Owner().GetAttribute('contractsPerPeriod')

    def IsB2B(self, *args):
        return self.Owner().IsB2B(None)
    
    def IsVisibleAndB2B(self, *args):
        return self.IsVisible() and self.IsB2B()
        
    def GetLayout(self):
        return self.UniqueLayout(
               """
                vbox(;
                    optionType;
                    strikePrice;
                    quantity_buySell;
                    quantity_value;
                    b2bPrice;
                    b2bMargin;
                    price;
                    totalQuantity;
                    uti;
                    );
                """)



