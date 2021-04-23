'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Ad_Hoc_Message
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module will give the Front Arena user the ability to run Ad Hoc BoP Reports
                                on multiple trades, instruments and portfolios for different dates.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project - BOPCUS 3 Upgrade
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       CHNG0001209844
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2013-08-17      CHNG0001209844  Heinrich Cronje                 Initial Implementation
2013-10-14      XXXXXXXXXXXXXX  Heinrich Cronje                 Front Arena Upgrade 2013. Changed input variable types
                                                                to System types.
                                                                
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    When this module is run, mulitple trade, instrument or portfolio requests will be sent to the
    request service.
'''

import acm, ael, clr
import FOperationsUtils as Utils
import CBFETR_Parameters as Params
from CBFETR_Access_Check import CBFETR_Access_Check as Access

'''---------------------------------------------------------------------------------------
                                Register and Import DLL
---------------------------------------------------------------------------------------'''
clr.FindAssembly("System")
clr.AddReference("RequestHandlerClientProxy")

import System
import CIBWM.Markets.FA.Services.RequestHandler
from CIBWM.Markets.FA.Services.RequestHandler import RequestHandlerServiceWrapper

ael_variables = [
                ['trades', 'Trade Numbers_Trades', acm.FTrade, acm.FTrade, '', 0, 1, 'Trade Numbers to generate prtential BOP Reports.', None, 1],
                ['trdDate', 'Date_Trades', 'date', None, ael.date_today(), 1, 0, 'Date for which potential BOP Reports should be created for.', None, 1],
                
                ['instruments', 'Instrument Names_Instrument', acm.FInstrument, acm.FInstrument, '', 0, 1, 'Trades on the instrument to generate potential BOP Reports.', None, 1],
                ['insDate', 'Date_Instrument', 'date', None, ael.date_today(), 1, 0, 'Date for which potential BOP Reports should be created for.', None, 1],
                
                ['portfolios', 'Portfolio Names_Portfolio', acm.FPhysicalPortfolio, acm.FPhysicalPortfolio, '', 0, 1, 'Trades in the instrumens to generate potential BOP Reports.', None, 1],
                ['prfDate', 'Date_Portfolio', 'date', None, ael.date_today(), 1, 0, 'Date for which potential BOP Reports should be created for.', None, 1]
                ]

def aelDateBreakdown(aelDate):
    return (aelDate.to_string('%Y'), aelDate.to_string('%m'), aelDate.to_string('%d'))

def ael_main(dict):
    if Params.environment == 'P':
        adHocBoPAccess = Access()
        if adHocBoPAccess.check_BoP_AccessResult == False:
            Utils.Log(True, 'ERROR: You do not have access to run Ad Hoc BoP Reporting.')
            return
        
    requestHandlerClass = RequestHandlerServiceWrapper()
    
    Utils.Log(True, 'Request Handler Wrapper Set' )
    Utils.Log(True, 'RequestHandler: ' + str(RequestHandlerServiceWrapper) )
    if dict['trades']:
        for trade in dict['trades']:
            dateBreakdown = aelDateBreakdown(dict['trdDate'])
            convertedDate = System.DateTime(dateBreakdown[0], dateBreakdown[1], dateBreakdown[2])
            try:
                if requestHandlerClass.RegisterRequest(System.String(Params.requestServiceAddress), convertedDate, System.Int32(2), System.String(str(trade.Oid())), System.String('FA Ad Hoc Trade Reuqest %s' %Params.FAEnvironment), System.String('MMG_CBFETR')):
                    Utils.Log(True, 'SUCCESS: Sent trade %s to the Request Service.' %str(trade.Oid()))
                else:
                    Utils.Log(True, 'ERROR: Could not send trade %s to the Request Service. Received the following error : ' %(str(trade.Oid()), str(e)))
            except Exception, e:
                Utils.Log(True, 'ERROR: Could not send trade %s to the Request Service. Received the following error : ' %(str(trade.Oid()), str(e)))
    
    if dict['instruments']:
        for instrument in dict['instruments']:
            dateBreakdown = aelDateBreakdown(dict['insDate'])
            convertedDate = System.DateTime(dateBreakdown[0], dateBreakdown[1], dateBreakdown[2])
            try:
                if requestHandlerClass.RegisterRequest(System.String(Params.requestServiceAddress), convertedDate, System.Int32(1), System.String(instrument.Name()), System.String('FA Ad Hoc Instrument Reuqest %s' %Params.FAEnvironment), System.String('MMG_CBFETR')):
                    Utils.Log(True, 'SUCCESS: Sent instrument %s to the Request Service.' %str(instrument.Name()))
                else:
                    Utils.Log(True, 'ERROR: Could not send instrument %s to the Request Service. Received the following error : ' %(str(instrument.Name()), str(e)))
            except Exception, e:
                Utils.Log(True, 'ERROR: Could not send instrument %s to the Request Service. Received the following error : ' %(str(instrument.Name()), str(e)))
    
    if dict['portfolios']:
        for portfolio in dict['portfolios']:
            dateBreakdown = aelDateBreakdown(dict['prfDate'])
            convertedDate = System.DateTime(dateBreakdown[0], dateBreakdown[1], dateBreakdown[2])
            Utils.Log(True, 'Trying to Register Request')
            try:
                if requestHandlerClass.RegisterRequest(System.String(Params.requestServiceAddress), convertedDate, System.Int32(0), System.String(portfolio.Name()), System.String('FA Ad Hoc Portfolio Reuqest %s' %Params.FAEnvironment), System.String('MMG_CBFETR')):
                    Utils.Log(True, 'SUCCESS: Sent portfolio %s to the Request Service.' %str(portfolio.Name()))
                else:
                    Utils.Log(True, 'Register Request NULL' )
                    Utils.Log(True, 'ERROR: Could not send portfolio %s to the Request Service. Received the following error : ' %(str(portfolio.Name()), str(e)))
            except Exception, e:
                Utils.Log(True, 'Failed to Register Request' )
                Utils.Log(True, 'ERROR: Could not send portfolio %s to the Request Service. Received the following error : ' %(str(portfolio.Name()), str(e)))

def generate_Ad_Hoc_BoP_Report(self):
    acm.RunModuleWithParameters('CBFETR_Ad_Hoc_Message', 'Standard' )
