import acm
from DealPackageDevKit import DealPackageDefinition, Float, Object, Settings, Text
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class SolveBetweenDoublesDefinition(DealPackageDefinition):
    """
    Basic example showing how to work with the attribute solver    
     - Input in the field Double will calculate and set the field Double Square to Double * Double
     - Input in the field Double Square will solve for the field Double if the value is between 0-10 or 20-30
    """

    aDouble       = Float( label='Double',
                           solverParameter=[{'minValue':0, 'maxValue':10}, {'minValue':20, 'maxValue':30}],
                           onChanged='@SetDoubleSquare',
                           toolTip='Entering a value here calculate and set \'Double Square\' to \'Double\' * \'Double\'')
    
    aDoubleSquare = Float( label='Double Square',
                           solverTopValue='aDouble',
                           toolTip='Entering a value here will solve for the field \'Double\' if value of the field is between 0-10 or 20-30')

    doc           = Text(  defaultValue=cleandoc(__doc__),
                           editable=False,
                           height=65) 
                                    
    # ####################### #
    #   Interface Overrides   #
    # ####################### # 
    
    def CustomPanes(self):
        return [ {'General' : """vbox[Solve Between Doubles;
                                   aDouble;
                                   aDoubleSquare;
                                   ];
                                 fill;
                                 hbox{DESCRIPTION;
                                   doc;
                                   );
                              """}]
                              
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can\'t be saved.')
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### # 
    
    def SetDoubleSquare(self, attributeName, oldValue, newValue, userInputAttributeName):
        self.SetAttribute('aDoubleSquare', newValue * newValue, silent=True)
