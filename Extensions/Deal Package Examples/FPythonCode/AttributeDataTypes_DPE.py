
import acm
from DealPackageDevKit import DealPackageDefinition, DealPackageException, Date, Str, Float, Bool, Settings, Text
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class AttributeDataTypesDefinition(DealPackageDefinition):
    """Example showing Attribute of type Str, Bool, Float, Date"""
    
    string      = Str(   label='Underlying Type',
                         choiceListSource=['Bond', 'Commodity', 'Stock'])
    
    bool        = Bool(  label='@BoolLabel')

    float       = Float( label='',
                         backgroundColor='@FloatBackgroundColor',
                         onChanged='@PrintMessageFloatOnChanged')
    
    startDate   = Date(  defaultValue='0d',
                         label='@StartDateLabel',
                         validate='@StartDateValidate',
                         transform='@PeriodToDateTransform',
                         onChanged='@PrintMessageStartDateOnChanged' )   
                             
    endDate     = Date(  defaultValue='10d',
                         label='End Date',
                         validate='@EndDateValidate',
                         transform='@PeriodToDateTransform')

    doc         = Text(  defaultValue=cleandoc(__doc__),
                         editable=False,
                         height=80)       

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_AttributeDataTypes_DPE')
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def FloatBackgroundColor(self, attributeName):
        value = self.GetAttribute(attributeName)
        return 'BkgTickerOwnBuyTrade' if value >= 0 else 'BkgTickerOwnSellTrade'

    def StartDateLabel(self, attributeName):
        date = self.GetAttribute(attributeName)
        dateToday = acm.Time().DateToday()
        dateDiff = acm.Time().DateDifference(dateToday, date)
        if(dateDiff > 0):
            return 'Historic Date'
        elif(dateDiff < 0):
            return 'Future Date'
        else:
            return 'Date Today'
            
    def BoolLabel(self, attributeName):
        bool = self.GetAttribute(attributeName)
        return 'ON' if bool else 'OFF'

    def PrintMessageStartDateOnChanged(self, attrStartDateDate, oldDate, newDate, userInputAttributeName):
        print ('Start Date Changed, oldDate: %s, newDate: %s' %(oldDate, newDate))
    
    def PrintMessageFloatOnChanged(self, name, oldValue, newValue, userInputAttributeName):
        print ('Float Changed, oldValue: %s, newValue: %s' %(oldValue, newValue))

    def PeriodToDateTransform(self, name, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = acm.Time().PeriodSymbolToDate(newDate)
        return date

    def StartDateValidate(self, name, value):
        if not acm.Time().PeriodSymbolToDate(self.endDate):
            if acm.Time().DateDifference(value, self.endDate) > 0:
                raise DealPackageException('Start Date must be prior to End Date.')
        
    def EndDateValidate(self, name, value):
        if not acm.Time().PeriodSymbolToDate(self.startDate):
            if acm.Time().DateDifference(self.startDate, value) > 0:
                raise DealPackageException('Start Date must be prior to End Date.')
