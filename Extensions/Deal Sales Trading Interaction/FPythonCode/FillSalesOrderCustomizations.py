import acm
from FillSalesOrderDefaultBase import FillSalesOrderDefaultBase
from DealPackageDevKit import DealPackageUserException, Action
from CustomTextImportExport import ToClipboard

'''##############################################################################################
#
# This Python module can be used to customize the Fill Sales Order dialog
#
##############################################################################################'''

class FillSalesOrderCustomDefinition(FillSalesOrderDefaultBase):

    '''**********************************************************************************************
    * Called when an instance of the class is created
    **********************************************************************************************'''
    def OnInit(self, **kwargs):
        super(FillSalesOrderCustomDefinition, self).OnInit(**kwargs)
      
    '''**********************************************************************************************
    * Add custom attributes to the Fill Sales Order dialog here
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
        return super(FillSalesOrderCustomDefinition, self).Instrument()
        
    '''**********************************************************************************************
    *  Method to access the Deal Package, only applicable when filling a Deal Package sales order
    **********************************************************************************************'''
    def DealPackage(self):
        return super(FillSalesOrderCustomDefinition, self).DealPackage()
        
    '''**********************************************************************************************
    * Method to access the Deal Package, only applicable when replying to a Deal Package quote request
    **********************************************************************************************'''
    def OrderHandler(self):
        return super(FillSalesOrderCustomDefinition, self).OrderHandler()

    '''**********************************************************************************************
    * Return the portfolio used for the trades created when filling a sales orders
    **********************************************************************************************'''
    def DefaultSalesOrderTradingPortfolioName(self):
        return super(FillSalesOrderCustomDefinition, self).DefaultSalesOrderTradingPortfolioName()


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
    *                                {'fillSalesOrder_fillQuantity'       : dict(enabled=False)}
    *                                )
    *
    **********************************************************************************************'''
    @staticmethod
    def CustomAttributeOverrides(overrideAccumulator):
        pass
