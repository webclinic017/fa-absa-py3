import acm
from QuoteRequestDefaultBase import QuoteRequestDefaultBase
from DealPackageDevKit import DealPackageUserException, Action
from CustomTextImportExport import ToClipboard

'''##############################################################################################
#
# This Python module can be used to customize the Quote Request dialog
#
##############################################################################################'''

class QuoteRequestCustomDefinition(QuoteRequestDefaultBase):

    '''**********************************************************************************************
    * Called when an instance of the class is created
    **********************************************************************************************'''
    def OnInit(self, **kwargs):
        super(QuoteRequestCustomDefinition, self).OnInit(**kwargs)
        
    '''**********************************************************************************************
    * Add custom attributes to the Quote Request dialog here
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
        return super(QuoteRequestCustomDefinition, self).Instrument()

    '''**********************************************************************************************
    * Method to access the Trade
    **********************************************************************************************'''
    def OriginalTrade(self):
        return super(QuoteRequestCustomDefinition, self).OriginalTrade()
        
    '''**********************************************************************************************
    * Method to access the Deal Package, only applicable when creating a Deal Package quote request
    **********************************************************************************************'''
    def DealPackage(self):
        return super(QuoteRequestCustomDefinition, self).DealPackage()
        
    '''**********************************************************************************************
    * Method to access the QuoteRequestInfo object for the customer quote request
    **********************************************************************************************'''
    def CustomerQuoteRequestInfo(self):
        return super(QuoteRequestCustomDefinition, self).CustomerQuoteRequestInfo()
        
    '''**********************************************************************************************
    * Method to access the QuoteRequestInfo object for the trading quote request
    **********************************************************************************************'''
    def TradingQuoteRequestInfo(self):
        return super(QuoteRequestCustomDefinition, self).TradingQuoteRequestInfo()

    '''**********************************************************************************************
    * Called when a Quote Request Dialog is opened from an already existing Quote Request
    **********************************************************************************************'''
    def CustomInitiateFromQuoteRequestInfos(self, *args):
        return super(QuoteRequestCustomDefinition, self).CustomInitiateFromQuoteRequestInfos()
  
    '''**********************************************************************************************
    * Return the default sales portfolio, the dialog will be populated with this sales portfolio when started
    **********************************************************************************************'''
    def DefaultSalesPortfolio(self):
        return super(QuoteRequestCustomDefinition, self).DefaultSalesPortfolio()

    '''**********************************************************************************************
    * Return the default trader, the dialog will be populated with this trader when started
    **********************************************************************************************'''
    def DefaultTrader(self):
        return super(QuoteRequestCustomDefinition, self).DefaultTrader()

    '''**********************************************************************************************
    * Called when a quote request is created
    **********************************************************************************************'''
    def OnCreateQuoteRequest(self, quoteRequest, componentName, customDict, *args):
        super(QuoteRequestCustomDefinition, self).OnCreateQuoteRequest(quoteRequest, componentName, customDict)

    '''**********************************************************************************************
    * Method to dictate how the Customer Price should be proposed (Firm or as Stream), when Stream from Trader. 
    *  Also dictates how to handle the Customer Price when Trader provides a Firm Stream price update. 
    *  Return an integer below.
    *       1 = Firm Stream price to the Customer. 
    *           Price updates from Trader results in a need to repropose the all-in price to the Customer.
    *       2 - Firm price to the Customer.
    *           Price updates from Trader results in a change of the Sales Margin, while keeping the Firm customer price fixed.
    **********************************************************************************************'''
    def CustomerPriceAsFirmOrStream(self, *args):
        return super(QuoteRequestCustomDefinition, self).CustomerPriceAsFirmOrStream()
        
    '''**********************************************************************************************
    * Return a list of counterparties specifying the quote request receivers
    **********************************************************************************************'''
    def QuoteRequestCounterparties(self, *args):
        return super(QuoteRequestCustomDefinition, self).QuoteRequestCounterparties()
        
    '''**********************************************************************************************
    * Called when a quote is either hit or lifted from the RFQ sales dialog
    **********************************************************************************************'''
    def OnAcceptQuote(self, order, quoteRequest, *args):
        super(QuoteRequestCustomDefinition, self).OnAcceptQuote(order, quoteRequest) 
        
    '''**********************************************************************************************
    * Called when a quote request answer is created and sent to the client
    * To add Extended Data to the Client Quote Request:
    *
    *    extendedData = acm.FQuoteExtendedData()
    *    extendedData.FairnessOfPrice(123.56)
    *    quoteRequestAnswer.ExtendedData(extendedData)
    *
    **********************************************************************************************'''
    def OnSendQuoteRequestAnswerToClient(self, quoteRequestInfo, quoteRequestAnswer, *args):
        super(QuoteRequestCustomDefinition, self).OnSendQuoteRequestAnswerToClient(quoteRequestInfo, quoteRequestAnswer) 
            
    '''**********************************************************************************************
    * Return the suggested name for the Customer Request
    **********************************************************************************************'''
    def SuggestCustomerRequestName(self, client, *args): 
        return super(QuoteRequestCustomDefinition, self).SuggestCustomerRequestName(client) 
            
    '''**********************************************************************************************
    * If the quick buttons are added to the dialog, this method should be used to return an array 
    * of length 6 with tuples specifying the labels and values of the nominal increment/decrement buttons
    **********************************************************************************************'''
    def NominalIncrements(self, *args):
        return super(QuoteRequestCustomDefinition, self).NominalIncrements() 
		
    '''**********************************************************************************************
    * Validate that the instrument is valid for RFQ, raise to pop-up dialog
    *   raise DealPackageUserException('Instrumenet is not valid to send quote request')
    **********************************************************************************************'''
    def CheckInstrumentIsValidToSendQuoteRequest(self, requestedNominal, client, *args):
        super(QuoteRequestCustomDefinition, self).CheckInstrumentIsValidToSendQuoteRequest(requestedNominal, client) 

    '''**********************************************************************************************
    * Return a text string that can be copied to the copy buffer on the command Copy Propsal
    **********************************************************************************************'''
    def CopyProposalText(self, summaryDict, *args):
        return super(QuoteRequestCustomDefinition, self).CopyProposalText(summaryDict)

    '''**********************************************************************************************
    * Return a text string that will be presented in the Quote Request Summary
    **********************************************************************************************'''
    def SummaryText(self, summaryDict, *args):
        return super(QuoteRequestCustomDefinition, self).SummaryText(summaryDict)
        
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
    *                                {'rfq_request_salesPortfolio'       : dict(visible=True)}
    *                                )
    *
    **********************************************************************************************'''
    @staticmethod
    def CustomAttributeOverrides(overrideAccumulator):
        pass
