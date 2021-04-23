import acm
from DealPackageDevKit import DealPackageDefinition, Text, Int, Settings
from inspect import cleandoc

@Settings(SheetApplicable=False)
class DealPackageGraph(DealPackageDefinition):
    """
    Enter values in 
     * Minimum X value
     * Maximum X value
     * Gradient
    to see the graph change.
    """

    minX        = Int(  defaultValue=0,
                        tick=True,
                        label='Minimum X value')
                       
    maxX        = Int(  defaultValue=10,
                        tick=True,
                        label='Maximum X value')
                       
    gradient    = Int(  defaultValue=1,
                        tick=2,
                        label='Gradient')
 
    doc         = Text( defaultValue=cleandoc(__doc__),
                        editable=False,
                        width=150,
                        height=120)

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def CustomPanes(self):
        return [ 
                    {'General' : """
                                minX;
                                maxX;
                                gradient;
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ] 

    def GraphYValues(self, xValues):
        yValues = [self.gradient*x for x in xValues]
        return yValues
        
    def GraphXValues(self):
        step = int((self.maxX-self.minX)/10)
        step = max(1, step)
        r = list(range(self.minX, self.maxX+step, step))
        return r

    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')
