import acm
from DealPackageDevKit import DealPackageUserException, Action
from QuoteRequestReplyDefaultBase import QuoteRequestReplyDefaultBase
from QuoteRequestReplyUtil import ToClipboard

'''##############################################################################################
#
# This Python module can be used to customize the Quote Reply dialog
#
##############################################################################################'''
    
class QuoteRequestReplyCustomDefinition(QuoteRequestReplyDefaultBase):

    '''**********************************************************************************************
    * Called when an instance of the class is created
    **********************************************************************************************'''
    def OnInit(self, **kwargs):
        super(QuoteRequestReplyCustomDefinition, self).OnInit(**kwargs)


    '''**********************************************************************************************
    * Add custom attributes to the Quote Reply dialog here
    **********************************************************************************************'''
    def Attributes(self):
        attributes = {'copyIsin':              Action( label='Copy ISIN',
                                                        action=self.UniqueCallback('@CopyIsin')),
                     }
        return attributes
        
    '''**********************************************************************************************
    * Method to access the Instrument
    **********************************************************************************************'''
    def Instrument(self):
        return super(QuoteRequestReplyCustomDefinition, self).Instrument()

    '''**********************************************************************************************
    * Method to access the Original Trade, only applicable when replying to quote request with an added trade 
    **********************************************************************************************'''
    def OriginalTrade(self):
        return super(QuoteRequestReplyCustomDefinition, self).OriginalTrade()

    '''**********************************************************************************************
    * Method to access the Deal Package, only applicable when replying to a Deal Package quote request
    **********************************************************************************************'''
    def DealPackage(self):
        return super(QuoteRequestReplyCustomDefinition, self).DealPackage()
    
    '''**********************************************************************************************
    * Method to access the QuoteController object
    **********************************************************************************************'''
    def QuoteController(self):
        return super(QuoteRequestReplyCustomDefinition, self).QuoteController()
    
    '''**********************************************************************************************
    * Method where custom actions can be added, will appear in the top right menu (Button with '>')
    **********************************************************************************************'''
    def TopPanelActions(self):
        return [self.PrefixedName('copyIsin')]
    
    '''**********************************************************************************************
    * Implementation of the CopyIsin Action
    **********************************************************************************************'''
    def CopyIsin(self, *args):
        ToClipboard(self.Instrument().Isin())
    
    '''**********************************************************************************************
    * Return the custom attribute layout using hbox and vbox
    **********************************************************************************************'''
    def GetLayout(self):
        return self.UniqueLayout("")

    '''**********************************************************************************************
    * This method can be used to override the standard behaviour of the built in attributes (e.g. visibility, enabled). 
    * It can also be used to add additional callbacks when a value is changed, like in the example below.
    *
    * To find the names for the different fields in the dialog, enable the Log Category "gui - custom layouts" and
    *  start the dialog. The tooltips will be replaced with the full name of the field.
    *
    *            overrideAccumulator(
    *                                {'qrr_currency'       : dict(visible=False)}
    *                                )
    *
    **********************************************************************************************'''
    @staticmethod
    def CustomAttributeOverrides(overrideAccumulator):
        pass
