import acm
from DealPackageDevKit import DealPackageDefinition, Text, Object, Settings, ReturnDomainDecorator
from CompositeAttributes import SelectInstrumentsDialog
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class SelectInstrumentsControl(DealPackageDefinition):
    """
    Example showing the SelectInstrumentDialog composite attribute. 
    Click the "Select Instrument(s)..." button in order to 
    select instruments.
    """
    
    ipName              = Object( label='Name',
                                  objMapping='InstrumentPackage.Name')
                                  
    selectInstruments   = SelectInstrumentsDialog(label='Select Instrument(s)...',
                                                  objMapping='EqIndexInstruments',
                                                  sizeToFit=True)
    
    instruments         = Object( label="Instruments",
                                  objMapping='EqIndex.Instruments',
                                  columns=[{'methodChain': 'StringKey', 'label': 'Name'}])
    
    doc                 = Text(   defaultValue=cleandoc(__doc__),
                                  editable=False,
                                  height=170) 
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #  

    def CustomPanes(self):
        return [ 
                    {'General' : """
                                ipName;
                                instruments;
                                hbox(;
                                    fill;
                                    selectInstruments;
                                );
                                fill;
                                hbox{DESCRIPTION;
                                   doc;
                                   );
                                """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateInstrument('Equity Index', 'index')
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    @ReturnDomainDecorator('FArray(FInstrument)')
    def EqIndexInstruments(self, value='Reading'):
        if value == 'Reading':
            return self.EqIndex().Instruments()
        else:
            currentInstruments = self.EqIndex().Instruments()
            # Remove
            for ins in currentInstruments:
                if ins not in value:
                    self.EqIndex().Remove(ins)
            # Add
            for ins in value:
                if ins not in self.EqIndex().Instruments():
                    self.EqIndex().AddInstrument(ins, 1.0)
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def EqIndex(self):
        return self.InstrumentAt('index')
