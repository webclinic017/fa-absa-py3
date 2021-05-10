
"""
MODULE
  SaveNonZARDealTicket

DESCRIPTION
  The functions in this module is called from the [AbsaSpecific]FTradingSheet:SaveDealTicket column.
  This module then calls the function in the NonZAR_Deal_Ticket_PDF module that creates the PDF deal ticket and saves it to the shared drive.

ENDDESCRIPTION

"""

import ael
import acm
import NonZAR_Deal_Ticket_PDF


def ButtonCreate(invokationInfo):
    return True

    
def ButtonPush(invokationInfo):
    sheet = invokationInfo.ExtensionObject().ActiveSheet()
    button = invokationInfo.Parameter("ClickedButton")
    #Put in check that only the Non ZAR Desk can print the deal ticket
    if button:
        BusObject = button.BusinessObject()
    
        if BusObject.Class() == acm.FTradeRow:
            t = BusObject.Trade()
            if t.add_info('NonZAR_Status') != 'Saved':
                NonZAR_Deal_Ticket_PDF.main(t.Oid())

        elif BusObject.Class() == acm.FPortfolioInstrumentAndTrades:
            for t in BusObject.Portfolio().Trades():
               if t.add_info('NonZAR_Status') != 'Saved':
                  NonZAR_Deal_Ticket_PDF.main(t.Oid())
                   
