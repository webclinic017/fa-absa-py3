import acm
from DealPackageDevKit import DealPackageDefinition, Str, Action, Box, Label, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class ButtonsDefinition(DealPackageDefinition):
    """
    Examples on how to work with Buttons and Actions attributes
    """
    
    lastButtonClicked = Str(      defaultValue='Click a button...')
    
    topPanel            = Box(    label='',
                                  vertical=False,
                                  backgroundColor='@TopPanelColor')
                                  
    topPanelText        = Label(  label='@TopPanelText',
                                  labelFont='@FontArial24',
                                  backgroundColor='@TopPanelColor',
                                  textColor='@TopPanelTextColor',
                                  width=400,
                                  maxWidth=400)
    
    firstAction         = Action( label='Button 1',
                                  action='@ButtonAction',
                                  textFont='@FontArial12Bold',
                                  textColor='@BlueColor',
                                  backgroundColor='@LightGreenColor')
    
    firstActionMenu     = Action( label='>',
                                  sizeToFit=True,
                                  actionList='@FirstActionList',
                                  textFont='@FontArial12Bold',
                                  textColor='@BlueColor',
                                  backgroundColor='@LightGreenColor')
                                  
    first_subMenu_1     = Action( label='Button 1 Menu 1',
                                  action='@ButtonAction')
                                  
    first_subMenu_2     = Action( label='Button 1 Menu 2',
                                  action='@ButtonAction')
                                  
    first_subMenu_3     = Action( label='Button 1 Menu 3',
                                  action='@ButtonAction')
    
    secondAction        = Action( label='Button 2',
                                  action='@ButtonAction',
                                  textFont='@FontArial12Bold',
                                  textColor='@WhiteColor',
                                  backgroundColor='@LightRedColor')
                                
    secondActionMenu    = Action( label='>',
                                  sizeToFit=True,
                                  actionList='@SecondActionList',
                                  textFont='@FontArial12Bold',
                                  textColor='@WhiteColor',
                                  backgroundColor='@LightRedColor')
                                  
    second_subMenu_1    = Action( label='Button 2 Menu 1',
                                  action='@ButtonAction')
                                  
    second_subMenu_2    = Action( label='Button 2 Menu 2',
                                  action='@ButtonAction')
                                  
    second_subMenu_3    = Action( label='Button 2 Menu 3',
                                  action='@ButtonAction')
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used to demonstrate button and actions and can not be saved.')

    # ####################### #
    #   Actions               #
    # ####################### #    
    def ButtonAction(self, attrName, *args):
        self.lastButtonClicked = self.GetAttributeMetaData(attrName, 'label')()
        
    def FirstActionList(self, *args):
        return ['first_subMenu_1', 'first_subMenu_2', 'first_subMenu_3']
   
    def SecondActionList(self, *args):
        return ['second_subMenu_1', 'second_subMenu_2', 'second_subMenu_3']
     
    # ####################### #
    #   Labels                #
    # ####################### #
    def TopPanelText(self, *args):
        return self.lastButtonClicked

    # ####################### #
    #   Fonts                 #
    # ####################### #
    def FontArial24(self, *args):
        return {'font':'Arial', 'bold':False, 'italic':False, 'size':24}

    def FontArial12Bold(self, *args):
        return {'font':'Arial', 'bold':True, 'italic':False, 'size':12}
    
    # ####################### #
    #   Colors                #
    # ####################### #
    def TopAreaColors(self):
        backColor = acm.Get('Colors/LightBlue')
        textColor = acm.Get('Colors/Gold')
        if 'Button 1' in str(self.lastButtonClicked):
            backColor = self.LightGreenColor()
            textColor = self.BlueColor()
        elif 'Button 2' in str(self.lastButtonClicked):
            backColor = self.LightRedColor()
            textColor = self.WhiteColor()
        return textColor, backColor
            
    def TopPanelColor(self, *args):
        textColor, backColor = self.TopAreaColors()
        return backColor
    
    def TopPanelTextColor(self, *args):
        textColor, backColor = self.TopAreaColors()
        return textColor
    
    def LightGreenColor(self, *args):
        return acm.Get('Colors/LightGreen')
        
    def LightRedColor(self, *args):
        return acm.Get('Colors/LightRed')

    def WhiteColor(self, *args):
        return acm.Get('Colors/White')
        
    def BlueColor(self, *args):
        return acm.Get('Colors/Blue')
            
    
    # ####################### #
    #   Layout                #
    # ####################### #
    def CustomPanes(self):
        return [ 
                    {'General' :    '''
                                    topPanel{;
                                        hbox(;
                                            topPanelText;
                                        );
                                    topPanel};
                                    hbox(;
                                        firstAction;
                                        firstActionMenu;
                                        secondAction;
                                        secondActionMenu;
                                    );
                                    '''
                    }
                ]
                
