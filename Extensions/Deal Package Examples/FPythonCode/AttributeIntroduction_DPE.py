
import acm
from DealPackageDevKit import DealPackageDefinition, Date, Settings, Text
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=False)
class AttributeIntroductionDefinition(DealPackageDefinition):
    """This Example introduces a date attribute, and meta data"""
    
    startDate         = Date(   defaultValue='0d',
                                label='Start Date',
                                validate='@StartDateValidate',
                                transform='@PeriodToDateTransform',
                                toolTip='@GenericToolTip',
                                onChanged='@Print1|Print2' )

    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=80)   

    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def CustomPanes(self):
        print ('CustomPanes')
        return [ 
                    {'General' : """
                                startDate;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );	
                                """
                    }
                ] 
                
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def Print1(self, attributeName, old, new, userInputAttributeName):
        print ('This is printed from "Print1"')
        print ('  Attribute name:', attributeName)
        print ('  Old value:', old)
        print ('  New value:', new)
        print ('  User input attribute name:', userInputAttributeName)

    def Print2(self, attributeName, old, new, userInputAttributeName):
        print ('This is printed from "Print2"')

    def GenericToolTip(self, attributeName):
        return 'This parameter has name ' + attributeName

    def PeriodToDateTransform(self, attributeName, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = acm.Time().PeriodSymbolToDate(newDate)
        print ('TransformStartPeriodToDate', newDate, date)
        return date
 
    def StartDateValidate(self, attributeName, value):
        # raise exception here to prevent value from beeing applied to attribute
        print ('ValidateStartDate')
