import acm
from DealPackageDevKit import Action
from SalesOrderDefaultBase import SalesOrderDefaultBase
from CustomTextImportExport import ToClipboard

'''##############################################################################################
#
# This Python module can be used to customize the Sales Order dialog
#
##############################################################################################'''

class SalesOrderCustomDefinition(SalesOrderDefaultBase):

    '''**********************************************************************************************
    * Called when an instance of the class is created
    **********************************************************************************************'''
    def OnInit(self, **kwargs):
        super(SalesOrderCustomDefinition, self).OnInit(**kwargs)

    '''**********************************************************************************************
    * Add custom attributes to the Sales Order dialog here
    **********************************************************************************************'''
    def Attributes(self):
        attributes = {'copyIsin' : Action( label='Copy ISIN',
                                           action=self.UniqueCallback('@CopyIsin'))
                     }
        return attributes

    '''**********************************************************************************************
    * Method to access the Instrument
    **********************************************************************************************'''
    def Instrument(self):
        return super(SalesOrderCustomDefinition, self).Instrument()

    '''**********************************************************************************************
    * Method to access the Deal Package, only applicable when creating a Deal Package sales order
    **********************************************************************************************'''
    def DealPackage(self):
        return super(SalesOrderCustomDefinition, self).DealPackage()

    '''**********************************************************************************************
    * Method to access the OrderHandler object
    **********************************************************************************************'''
    def OrderHandler(self):
        return super(SalesOrderCustomDefinition, self).OrderHandler()

    '''**********************************************************************************************
    * Return the default sales portfolio, the dialog will be populated with this sales portfolio when started
    **********************************************************************************************'''
    def DefaultSalesPortfolio(self):
        return super(SalesOrderCustomDefinition, self).DefaultSalesPortfolio()
     
    '''**********************************************************************************************
    * Called before the SalesOrder is Sent
    **********************************************************************************************'''
    def OnCreateSalesOrder(self, componentName, customDict, *args):
        super(SalesOrderCustomDefinition, self).OnCreateSalesOrder(componentName, customDict)
        
    '''**********************************************************************************************
    * Validate that instrument is valid for sales order
    **********************************************************************************************'''
    def CheckInstrumentIsValidToSendOrder(self, buyOrSell, quantity, client, portfolio):
        return super(SalesOrderCustomDefinition, self).CheckInstrumentIsValidToSendOrder(buyOrSell, quantity, client, portfolio)

    '''**********************************************************************************************
    * Return the suggested name for the Customer Request
    **********************************************************************************************'''
    def SuggestCustomerRequestName(self, client):
        return super(SalesOrderCustomDefinition, self).SuggestCustomerRequestName(client)

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
    *                                {'salesOrder_portfolio'       : dict(enabled=False)}
    *                                )
    *
    **********************************************************************************************'''
    @staticmethod
    def CustomAttributeOverrides(overrideAccumulator):
        pass
