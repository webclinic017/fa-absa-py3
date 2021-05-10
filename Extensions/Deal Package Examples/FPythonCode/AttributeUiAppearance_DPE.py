import acm
from DealPackageDevKit import DealPackageDefinition, DealPackageException, Str, Text, Int, Bool, Label, Link, Settings, Box
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class AttributeUiAppearance(DealPackageDefinition):
    """
    UI Appearance attributes. 
     - Note that the initial focus is on the Width control
     - Entering positive/negative values in Font Size will change the color
     - The value entered in Font Size will set the font size
     - The Font Size field only accepts inputs in the range -50 to 50
     - Note that the font size fields have a non-standard font and are both bold and italic
     - Note that the black box around the font size label is a custom hbox
     - Click on the hyperlink to increase the font size
     - The Width field has a fixed width
     - The password field has masked password characters
     - Clicking in the Enable field will enable/disable the Enabled / Visible String field
     - Clicking in the Visible field will show/hide 
     - Clicking in the Editable field will make the Enabled / Visible String fields editable/uneditable
     - Clicking on Slim/Detail under Layout to toggle slim/detail mode
     - Tabbing from with will give focus to Enabled, and thereby skip the "No Tab Stop" control
     """

    size              = Int(    defaultValue=20,
                                label='Font Size',
                                backgroundColor='@SizeAttributeBackgroundColor',
                                validate='@SizeValidate',
                                labelColor='BkgFlash',
                                textColor='SyntaxPythonStringEOL',
                                textFont='@SizeFont',
                                labelFont='@SizeFont',
                                tick=True)
    
    customHbox        = Box(    label='',
                                vertical=False,
                                backgroundColor='SyntaxPythonDefault')
                            
    sizeLabel         = Label(  label='@SizeLabel',
                                labelColor='@SizeAttributeBackgroundColor',
                                backgroundColor='SyntaxPythonDefault',
                                labelFont='@SizeFont',
                                width=200)
    
    sizeLink          = Link(   label='@SizeLinkLabel',
                                action='@SizeLinkClicked',
                                width=300)
                                
    someChoices       = Str(    label='Choices',
                                choiceListSource=['A', 'B', 'C'],
                                textFont='@SizeFont',
                                labelFont='@SizeFont',
                                defaultValue='A')
    
    width             = Str(    label='Width',
                                initialFocus=True,
                                width=10,
                                maxWidth=10)
    
    password          = Str(    label='Password',
                                isPassword=True)
    
    tabSkip           = Str(    label='No Tab Stop',
                                tabStop=False,
                                toolTip='Skip this control when tabbing between controls')
    
    enabled           = Bool(   defaultValue=True,
                                label='Enable')
                                
    editable          = Bool(   defaultValue=True,
                                label='Editable')
    
    visible           = Bool(   defaultValue=True,
                                label='Visible')
    
    stringEnable      = Str(    label='Enabled / Visible String',
                                enabled='@StringEnabled',
                                visible='@StringVisible',
                                editable='@StringEditable')
                                
    textEnable        = Text(   defaultValue= 'Enter text here when enabled',
                                enabled='@StringEnabled',
                                visible='@StringVisible',
                                editable='@StringEditable',
                                height=100)
 
    onlyInDetail      = Str(    label='Only Shown In Detail',
                                visible='@IsShowModeDetail')
                                
    doc               = Text(   defaultValue=cleandoc(__doc__),
                                editable=False,
                                height=160)  

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_AttributeUiAppearance_DPE')
    
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used for demonstration and can not be saved.')
        
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def SizeValidate(self, name, value):
        if value < -50:
            raise DealPackageException('Value must be greater than -50.')
        if value > 50:
            raise DealPackageException('Value must be less than 50.')

    def StringEnabled(self, attributeName):
        return self.enabled
        
    def StringVisible(self, attributeName):
        return self.visible
    
    def StringEditable(self, attributeName):
        return self.editable
    
    def SizeAttributeBackgroundColor(self, attributeName):
        return 'BkgTickerOwnBuyTrade' if self.size > 0 else 'BkgTickerOwnSellTrade'
        
    def SizeFont(self, attributeName):
        return {'font':'Monotype Corsiva', 'bold':True, 'italic':True, 'size':self.size}
        
    def SizeLabel(self, *args):
        return 'Font Size = ' +  str(self.size)
        
    def SizeLinkLabel(self, *args):
        return 'Click to increase font size (current value is ' +  str(self.size) + ')'
        
    def SizeLinkClicked(self, attributeName):
        self.size += 1
