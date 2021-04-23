
import acm
from DealPackageDevKit import DealPackageDefinition, CompositeAttributeDefinition, Settings, Object, Text
from inspect import cleandoc

class SimpleTradeCompositeAttribute(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #  

    def OnInit(self, labelPrefix, tradeMapping, defaultStatus):
        self._labelPrefix = labelPrefix
        self._defaultStatus = defaultStatus
        self._tradeMapping = tradeMapping
        
    def Attributes(self):
        """
        -----------------------------------
        self.UniqueCallback('<NameOfMethod>')
        -----------------------------------
        Calling UniqueCallback with the name of the method has two purposes.
        
        1. It adds the method to the parent (deal package), with a prefixed name of myCompAttr_NameOfMethod,
           assuming that the composite attribute is defined as:
               myCompAttr = SimpleTradeCompositeAttribute(<args>)
           on the parent (deal package).
           
        2. UniqueCallback returns a prefixed name, so that the mapping becomes correct. For example:
                toolTip=self.UniqueCallback('@ToolTipMethod') -> toolTip='@myCompAttr_ToolTipMethod'
           This enables the attribute to find the method myCompAttr_NameOfMethod found on the parent.
        
        """
        attributes = {
            'counterparty'  : Object( label=self._labelPrefix +' Cpty',
                                      objMapping=self._tradeMapping + '.Counterparty',
                                      toolTip=self.UniqueCallback('@ToolTipMethod') ),
                                      
            'portfolio'     : Object( label=self._labelPrefix +' Prf',
                                      objMapping=self._tradeMapping + '.Portfolio' ),
            
            'acquirer'      : Object( label=self._labelPrefix +' Acq',
                                      objMapping=self._tradeMapping + '.Acquirer' ),
            
            'status'        : Object( label=self._labelPrefix +' Status',
                                      defaultValue=self._defaultStatus,
                                      objMapping=self._tradeMapping + '.Status' )
            }
        
        """
        -----------------------------------
        self.GetMethod('<MethodName>')
        -----------------------------------
        GetMethod will return an attribute/method on the parent (deal package) with the name <MethodName>.
        This can be needed as the CompositeAttributeDevKit-API does not contain all methods that might be needed.
        For example; if you need to set an "RegisterCallbackOnAttributeChanged", you would do as below:
            self.GetMethod('RegisterCallbackOnAttributeChanged')(self.CompositeAttributeMethod)
        where the method "RegisterCallbackOnAttributeChanged" is found on the parent deal package.
        Note: As we are actually passing in the bound method reference we do not need to use "UniqueCallback".
        """
        self.GetMethod('RegisterCallbackOnAttributeChanged')(self.PrintTheChange)
            
        return attributes 
    
    def GetLayout(self):
        """
        -----------------------------------
        self.UniqueLayout(''' layout ''')
        -----------------------------------
        UniqueLayout will replace all the attributes with the prefixed name. For example:
            self.UniqueLayout('''portfolio''') -> myCompAttr_portfolio
        """
        return self.UniqueLayout(
            '''
            vbox(;
                counterparty;
                portfolio;
                acquirer;
                status;
            );
            '''
            )

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def ToolTipMethod(self, attributeName):
        return ('The counterparty of the trade from method ' 
                + self._tradeMapping + '. '
                +'The name of this ToolTipMethod is: ' 
                + self.UniqueCallback('ToolTipMethod'))

    def PrintTheChange(self, attributeName, oldValue, newValue, userInput):
        print('PrintTheChange-Method on %s called as %s has changed' % (self.UniqueCallback('')[:-1], attributeName))


@Settings(GraphApplicable=False)
class DealPackageCompositeAttributes(DealPackageDefinition):
    """
    Example showing how to create composite attributes programmatically. 
    For more information on the CompositeAttribute API, see python module
    CompositeAttributeDevKit found in the "Deal Package"-module.
    """
    
    ipName      = Object(   label='Name',
                            objMapping='InstrumentPackage.Name') 
    
    myCompAttr1 = SimpleTradeCompositeAttribute(labelPrefix='First',
                                                tradeMapping='Trade1',
                                                defaultStatus='Simulated')
                                                
    myCompAttr2 = SimpleTradeCompositeAttribute(labelPrefix='Second',
                                                tradeMapping='Trade2',
                                                defaultStatus='FO Confirmed')
    
    doc         = Text(     defaultValue=cleandoc(__doc__),
                            editable=False,
                            height=80)

    # ####################### #
    #   Interface Overrides   #
    # ####################### #  

    def CustomPanes(self):
        """
        The 'myCompAttr1' and 'myCompAttr2' strings in the layout will at a later stage be replaced by
        the string returned by the GetLayout-method of the composite attributes. For example:
        
            myCompAttr1
        
        is replaced by:
        
            vbox(;
                myCompAttr1_counterparty;
                myCompAttr1_portfolio;
                myCompAttr1_acquirer;
                myCompAttr1_status;
            );
        """
    
        return [ 
                    {'General' : """
                                ipName;
                                hbox(;
                                    myCompAttr1;
                                    myCompAttr2;
                                );
                                fill;
                                hbox{DESCRIPTION;
                                    doc;
                                );
                                """
                    }
                ] 

    def AssemblePackage(self):
        self.DealPackage().CreateTrade('Option', 'option1')
        self.DealPackage().CreateTrade('Option', 'option2')

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def Trade1(self):
        return self.TradeAt('option1')
        
    def Trade2(self):
        return self.TradeAt('option2')
