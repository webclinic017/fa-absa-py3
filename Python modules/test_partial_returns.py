"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  Unit tests for SL partial return process
DEPATMENT AND DESK      :  N/A
REQUESTER               :  N/A
DEVELOPER               :  Paul Jacot-Guillarmod and Francois Truter
CR NUMBER               :  494829
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    PJG & FT           Initial implementation
"""


import ael, acm
import unittest
from test_helper_trades import TradeHelper
from test_helper_instruments import InstrumentHelper
from test_helper_general import PortfolioHelper
import sl_partial_returns, sl_functions
import test_partial_returns

calendar = acm.FCalendar['ZAR Johannesburg']
today = acm.Time().DateNow()
tomorrow = calendar.AdjustBankingDays(today, 1)
yesterday = calendar.AdjustBankingDays(today, -1)

class TestTerminateTradeToday(unittest.TestCase):
    ''' Test terminating a trade today (returning the full amount)
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        sl_partial_returns.partial_return(self.parentTrade, today, 100)
        acm.PollDbEvents()
        
    def testTerminateTrade(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'Instrument Open End expected to be Terminated')
        self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'Trade status expected to be BO Confirmed')
        self.assertEqual(self.parentInstrument.EndDate(), today, 'End date expected to be equal to ' + str(today))


class TestTerminateTradeTomorrow(unittest.TestCase):
    ''' Test terminating a trade today (returning the full amount)
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        sl_partial_returns.partial_return(self.parentTrade, tomorrow, 100)
        acm.PollDbEvents()
        
    def testTerminateTrade(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'Instrument Open End expected to be Terminated')
        self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'Trade status expected to be BO Confirmed')
        self.assertEqual(self.parentInstrument.EndDate(), tomorrow, 'End date expected to be equal to ' + str(tomorrow))

class TestSameDayTermination(unittest.TestCase):
    
    def setUp(self):
        self.startDate = today
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        sl_partial_returns.partial_return(self.parentTrade, today, self.parentQuantity)
    
    def testTermination(self):
        self.assertEqual(self.parentInstrument.StartDate(), self.parentInstrument.EndDate(), 'ParentInstrument Start and End date expected to be equal')
        parentLeg = self.parentInstrument.Legs().At(0)
        self.assertEqual(len(parentLeg.CashFlows()), 0, 'ParentInstrument should have no cashflows')
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')

class TestCFDSameDayTermination(unittest.TestCase):
    
    def setUp(self):
        self.startDate = today
        self.endDate = tomorrow
        
        self.parentQuantity = 100
        self.parentTrade = TradeHelper.BookCFDSecurityLoanAndTrade(self.startDate, self.endDate, 'BO Confirmed', self.parentQuantity)
        self.parentInstrument = self.parentTrade.Instrument()
        
        self.returnDate = today
        self.returnQuantity = 100
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, self.returnDate, self.returnQuantity)
    
    def testTermination(self):
        self.assertEqual(self.parentInstrument.StartDate(), self.parentInstrument.EndDate(), 'ParentInstrument Start and End date expected to be equal')
        parentLeg = self.parentInstrument.Legs().At(0)
        self.assertEqual(len(parentLeg.CashFlows()), 0, 'ParentInstrument should have no cashflows')
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')

class TestSameDayReturn(unittest.TestCase):
    
    def setUp(self):
        self.startDate = today
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.returnQuantity = 50
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, today, self.returnQuantity)
        self.childInstrument = self.childTrade.Instrument()
    
    def testSameDayDates(self):
        self.assertEqual(self.parentInstrument.StartDate(), self.parentInstrument.EndDate(), 'ParentInstrument start and end date expected to be equal')
        self.assertEqual(self.parentInstrument.EndDate(), self.childInstrument.StartDate(), 'ParentInstrument end date and ChildInstrument start date expected to be equal')
        
    def testSameDayCashFlows(self):
        parentLeg = self.parentInstrument.Legs().At(0)
        self.assertEqual(len(parentLeg.CashFlows()), 0, 'ParentInstrument should have no cashflows')
        
    def testSameDayStatuses(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument.OpenEnd(), 'Open End', 'ChildInstrument Open End expected to be Open End')
        self.assertEqual(self.childTrade.Status(), 'FO Confirmed', 'ChildTrade status expected to be FO Confirmed')
        

class TestSinglePartialReturnToday(unittest.TestCase):
    ''' Testing a single partial return made today.
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        
        self.returnQuantity = 50
        self.returnDate = today
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, self.returnDate, self.returnQuantity)
        self.childInstrument = self.childTrade.Instrument()
    
    def testSinglePartialReturnStatuses(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument.OpenEnd(), 'Open End', 'ChildInstrument Open End expected to be Open End')
        self.assertEqual(self.childTrade.Status(), 'FO Confirmed', 'ChildTrade status expected to be FO Confirmed')
        
    def testSinglePartialReturnDates(self):
        self.assertEqual(self.parentInstrument.EndDate(), self.returnDate, 'ParentInstrument End date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.StartDate(), self.returnDate, 'ChildInstrument Start date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.EndDate(), tomorrow, 'ChildInstrument Start date expected to be ' + str(tomorrow))
        
    def testSinglePartialReturnQuantities(self):
        quantityChild = self.parentQuantity - self.returnQuantity
        self.assertEqual(sl_functions.underlying_quantity(self.parentTrade.Quantity(), self.parentInstrument), self.parentQuantity, 'Parent Trades underlying quantity should be ' + str(self.parentQuantity))
        self.assertEqual(sl_functions.underlying_quantity(self.childTrade.Quantity(), self.childInstrument), quantityChild, 'Child trades underling quantity should be ' + str(quantityChild))
        
    def testSinglePartialReturnPointers(self):
        self.assertEqual(self.parentTrade.ConnectedTrade().Oid(), self.childTrade.Oid(), 'Parent trades ConnectedTrdnbr should point to child trade')
        self.assertEqual(self.childTrade.Contract().Oid(), self.parentTrade.Oid(), 'Child trades ContractTrdnbr should point to the parent trade')
        self.assertEqual(self.childTrade.TrxTrade().Oid(), self.parentTrade.Oid(), 'Child trades Trans Ref should point to the parent trade')

class TestSinglePartialReturnPast(unittest.TestCase):
    ''' Testing a single partial return made in the past.
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        
        self.returnQuantity = 50
        self.returnDate = acm.Time().DateFromYMD(2010, 8, 18)
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, self.returnDate, self.returnQuantity)
        self.childInstrument = self.childTrade.Instrument()
    
    def testSinglePartialReturnStatuses(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument.OpenEnd(), 'Open End', 'ChildInstrument Open End expected to be Open End')
        self.assertEqual(self.childTrade.Status(), 'FO Confirmed', 'ChildTrade status expected to be FO Confirmed')
        
    def testSinglePartialReturnDates(self):
        self.assertEqual(self.parentInstrument.EndDate(), self.returnDate, 'ParentInstrument End date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.StartDate(), self.returnDate, 'ChildInstrument Start date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.EndDate(), tomorrow, 'ChildInstrument Start date expected to be ' + str(tomorrow))
        
    def testSinglePartialReturnQuantities(self):
        quantityChild = self.parentQuantity - self.returnQuantity
        self.assertEqual(sl_functions.underlying_quantity(self.parentTrade.Quantity(), self.parentInstrument), self.parentQuantity, 'Parent Trades underlying quantity should be ' + str(self.parentQuantity))
        self.assertEqual(sl_functions.underlying_quantity(self.childTrade.Quantity(), self.childInstrument), quantityChild, 'Child trades underling quantity should be ' + str(quantityChild))
        
    def testSinglePartialReturnPointers(self):
        self.assertEqual(self.parentTrade.ConnectedTrade().Oid(), self.childTrade.Oid(), 'Parent trades ConnectedTrdnbr should point to child trade')
        self.assertEqual(self.childTrade.Contract().Oid(), self.parentTrade.Oid(), 'Child trades ContractTrdnbr should point to the parent trade')
        self.assertEqual(self.childTrade.TrxTrade().Oid(), self.parentTrade.Oid(), 'Child trades Trans Ref should point to the parent trade')
        

class TestSinglePartialReturnFuture(unittest.TestCase):
    ''' Testing a single partial return made in the future.
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        
        self.returnQuantity = 50
        self.returnDate = calendar.AdjustBankingDays(self.endDate, 3)
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, self.returnDate, self.returnQuantity)
        self.childInstrument = self.childTrade.Instrument()
    
    def testSinglePartialReturnStatuses(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument.OpenEnd(), 'Open End', 'ChildInstrument Open End expected to be Open End')
        self.assertEqual(self.childTrade.Status(), 'FO Confirmed', 'ChildTrade status expected to be FO Confirmed')
        
    def testSinglePartialReturnDates(self):
        expectedChildEndDate = calendar.AdjustBankingDays(self.returnDate, 1)
        self.assertEqual(self.parentInstrument.EndDate(), self.returnDate, 'ParentInstrument End date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.StartDate(), self.returnDate, 'ChildInstrument Start date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.EndDate(), expectedChildEndDate, 'ChildInstrument Start date expected to be ' + str(expectedChildEndDate))
        
    def testSinglePartialReturnQuantities(self):
        quantityChild = self.parentQuantity - self.returnQuantity
        self.assertEqual(sl_functions.underlying_quantity(self.parentTrade.Quantity(), self.parentInstrument), self.parentQuantity, 'Parent Trades underlying quantity should be ' + str(self.parentQuantity))
        self.assertEqual(sl_functions.underlying_quantity(self.childTrade.Quantity(), self.childInstrument), quantityChild, 'Child trades underling quantity should be ' + str(quantityChild))
        
    def testSinglePartialReturnPointers(self):
        self.assertEqual(self.parentTrade.ConnectedTrade().Oid(), self.childTrade.Oid(), 'Parent trades ConnectedTrdnbr should point to child trade')
        self.assertEqual(self.childTrade.Contract().Oid(), self.parentTrade.Oid(), 'Child trades ContractTrdnbr should point to the parent trade')
        self.assertEqual(self.childTrade.TrxTrade().Oid(), self.parentTrade.Oid(), 'Child trades Trans Ref should point to the parent trade')
        

class TestDoublePartialReturn(unittest.TestCase):
    ''' Testing partial return on a partial return.  First return today, next one tomorrow.
    '''
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        
        self.returnQuantity1 = 50
        self.childTrade1 = sl_partial_returns.partial_return(self.parentTrade, today, self.returnQuantity1)
        self.childTrade1.Status('BO Confirmed')
        self.childTrade1.Commit()
        self.childInstrument1 = self.childTrade1.Instrument()
        
        self.returnQuantity2 = 25
        self.endDate2 = calendar.AdjustBankingDays(self.endDate, 3)
        self.childTrade2 = sl_partial_returns.partial_return(self.childTrade1, self.endDate2, self.returnQuantity2)
        self.childInstrument2 = self.childTrade2.Instrument()
    
    def testDoublePartialReturnPointers(self):
        ''' Testing that all the pointers are correct on the parent trade and first and second returns.
        '''
        self.assertEqual(self.parentTrade.ConnectedTrade().Oid(), self.childTrade1.Oid(), 'ParentTrade ConnectedTrdnbr should point to childTrade1')
        self.assertEqual(self.childTrade1.Contract().Oid(), self.parentTrade.Oid(), 'ChildTrade1 ContractTrdnbr should point to parentTrade')
        self.assertEqual(self.childTrade1.TrxTrade().Oid(), self.parentTrade.Oid(), 'ChildTrade1 Trans Ref should point to parentTrade')
        self.assertEqual(self.childTrade1.ConnectedTrade().Oid(), self.childTrade2.Oid(), 'ChildTrade1 ConnectedTrdnbr should point to childTrade2')
        self.assertEqual(self.childTrade2.Contract().Oid(), self.parentTrade.Oid(), 'ChildTrade2 ContractTrdnbr should point to parentTrade')
        self.assertEqual(self.childTrade2.TrxTrade().Oid(), self.childTrade1.Oid(), 'ChildTrade2 Trans Ref should point to childTrade1')
    
    def testDoublePartialReturnStatuses(self):
        ''' Testing that all the Open End statuses and trade statuses are correct on the parent and first and second returns.
        '''
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument1.OpenEnd(), 'Terminated', 'ChildInstrument1 Open End expected to be Terminated')
        #self.assertEqual(self.childTrade1.Status(), 'BO Confirmed', 'ChildTrade1 status expected to be BO Confirmed')
        self.assertEqual(self.childTrade1.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument2.OpenEnd(), 'Open End', 'ChildInstrument2 Open End expected to be Open End')
        self.assertEqual(self.childTrade2.Status(), 'FO Confirmed', 'ChildTrade2 status expected to be FO Confirmed')
    
    def testDoublePartialReturnDates(self):
        ''' Testing that the start and end dates are correct on the parent and first and second returns.
        '''
        self.assertEqual(self.parentInstrument.EndDate(), today, 'ParentInstrument End date expected to be ' + str(today))
        self.assertEqual(self.childInstrument1.StartDate(), today, 'ChildInstrument1 Start date expected to be ' + str(today))
        self.assertEqual(self.childInstrument1.EndDate(), self.endDate2, 'ChildInstrument1 Start date expected to be ' + str(self.endDate2))
        self.assertEqual(self.childInstrument2.StartDate(), self.endDate2, 'ChildInstrument2 Start date expected to be ' + str(self.endDate2))
        
    def testDoublePartialReturnQuantities(self):
        ''' Testing that the quantities are correct on the parent and first and second returns.
        '''
        quantityParent = sl_functions.underlying_quantity(self.parentTrade.Quantity(), self.parentInstrument)
        quantityChildTrade1 = sl_functions.underlying_quantity(self.childTrade1.Quantity(), self.childInstrument1)
        quantityChildTrade2 = sl_functions.underlying_quantity(self.childTrade2.Quantity(), self.childInstrument2)
        expectedQuantity1 = self.parentQuantity - self.returnQuantity1
        expectedQuantity2 = self.parentQuantity - self.returnQuantity1 - self.returnQuantity2
        self.assertEqual(quantityParent, self.parentQuantity, 'parentTrade should have underlying quantity of ' + str(self.parentQuantity))
        self.assertEqual(quantityChildTrade1, expectedQuantity1, 'childTrade1 should have underlying quantity of ' + str(expectedQuantity1))
        self.assertEqual(quantityChildTrade2, expectedQuantity2, 'childTrade2 should have underlying quantity of ' + str(expectedQuantity2))
        
class TestPartialReturnsAddInfos(unittest.TestCase):
    
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.endDate2 = calendar.AdjustBankingDays(self.endDate, 3)
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
        
        sl_functions.set_additional_info(self.parentInstrument, 'SL_Dividend_Factor', 1.3)
        sl_functions.set_additional_info(self.parentInstrument, 'SL_ExternalInternal', 'Internal')
        sl_functions.set_additional_info(self.parentInstrument, 'SL_Minimum_Fee', 0.5)
        sl_functions.set_additional_info(self.parentInstrument, 'SL_RecallDate', '2010-06-10')
        sl_functions.set_additional_info(self.parentInstrument, 'SL_Trading_Capacity', 'Agent')
        sl_functions.set_additional_info(self.parentInstrument, 'SL_VAT', 'False')
        sl_functions.set_additional_info(self.parentInstrument, 'SL_CFD', 'True')
        
        self.childTrade1 = sl_partial_returns.partial_return(self.parentTrade, self.endDate, 50)
        self.childTrade1.Status('BO Confirmed')
        self.childTrade1.Commit()
        self.childInstrument1 = self.childTrade1.Instrument()
        
        self.childTrade2 = sl_partial_returns.partial_return(self.childTrade1, self.endDate2, 25)
        self.childInstrument2 = self.childTrade2.Instrument()
        
    def testAddInfosFirstReturn(self):
        ''' Testing that all additional infos are correctly copied to the first return.
        '''
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_Dividend_Factor(), 1.3, 'SL_Dividend_Factor was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_ExternalInternal(), 'Internal', 'SL_ExternalInternal was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_Minimum_Fee(), 0.5, 'SL_Minimum_Fee was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_RecallDate(), '2010-06-10', 'SL_RecallDate was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_Trading_Capacity(), 'Agent', 'SL_TradingCapacity was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_VAT(), False, 'SL_VAT was not copied correctly to childInstrument1')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_CFD(), True, 'SL_CFD was not copied correctly to childInstrument1')
    
    def testAddInfosSecondReturn(self):
        ''' Testing that all additional infos are correctly copied to the second return.
        '''
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_Dividend_Factor(), 1.3, 'SL_Dividend_Factor was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_ExternalInternal(), 'Internal', 'SL_ExternalInternal was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_Minimum_Fee(), 0.5, 'SL_Minimum_Fee was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_RecallDate(), '2010-06-10', 'SL_RecallDate was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_Trading_Capacity(), 'Agent', 'SL_TradingCapacity was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument2.AdditionalInfo().SL_VAT(), False, 'SL_VAT was not copied correctly to childInstrument2')
        self.assertEqual(self.childInstrument1.AdditionalInfo().SL_CFD(), True, 'SL_CFD was not copied correctly to childInstrument2')

class TestDataValidation(unittest.TestCase):
    
    def setUp(self):
        self.startDate = acm.Time().DateFromYMD(2010, 6, 1)
        self.endDate = tomorrow
        self.parentQuantity = 100
        self.parentInstrument = InstrumentHelper.CreatePersistantOpenEndedSecurityLoan(self.startDate, self.endDate)
        self.parentTrade = TradeHelper.BookSecurityLoan(self.parentInstrument, 'BO Confirmed', self.startDate, self.parentQuantity)
    
    def testTradeQuantity(self):
        self.assertRaises(sl_partial_returns.ReturnQuantityError, sl_partial_returns.partial_return, self.parentTrade, self.endDate, 1000)
    
    def testReturnDate(self):
        returnDate = acm.Time().DateFromYMD(2010, 5, 1)
        self.assertRaises(sl_partial_returns.ReturnDateError, sl_partial_returns.partial_return, self.parentTrade, returnDate, 50)

class TestCFDSinglePartialReturn(unittest.TestCase):
    
    def setUp(self):
        self.startDate = calendar.AdjustBankingDays(today, -10)
        self.endDate = tomorrow
        
        self.parentQuantity = 100
        self.parentTrade = TradeHelper.BookCFDSecurityLoanAndTrade(self.startDate, self.endDate, 'BO Confirmed', self.parentQuantity)
        self.parentInstrument = self.parentTrade.Instrument()
        
        self.returnDate = today
        self.returnQuantity = 50
        self.childTrade = sl_partial_returns.partial_return(self.parentTrade, self.returnDate, self.returnQuantity)
        self.childInstrument = self.childTrade.Instrument()
        
    def testNumberOfParentCashFlows(self):
        expectedNumParentCashflows = len(list(sl_functions.DateGenerator(self.startDate, self.returnDate))) - 1
        cashFlows = self.parentInstrument.Legs().At(0).CashFlows()
        self.assertEqual(len(cashFlows), expectedNumParentCashflows, 'ParentInstrument expected to have ' + str(expectedNumParentCashflows) + ' cashflows.')
    
    def testNumberOfChildCashflows(self):
        cashFlows = self.childInstrument.Legs().At(0).CashFlows()
        self.assertEqual(len(cashFlows), 1, 'ChildInstrument expected to have 1 cashflow.')
    
    def testSinglePartialReturnStatuses(self):
        self.assertEqual(self.parentInstrument.OpenEnd(), 'Terminated', 'ParentInstrument Open End expected to be Terminated')
        #self.assertEqual(self.parentTrade.Status(), 'BO Confirmed', 'ParentTrade status expected to be BO Confirmed')
        self.assertEqual(self.parentTrade.Status(), 'Terminated', 'ParentTrade status expected to be Terminated')
        self.assertEqual(self.childInstrument.OpenEnd(), 'Open End', 'ChildInstrument Open End expected to be Open End')
        self.assertEqual(self.childTrade.Status(), 'FO Confirmed', 'ChildTrade status expected to be FO Confirmed')
        
    def testSinglePartialReturnDates(self):
        expectedChildEndDate = calendar.AdjustBankingDays(self.returnDate, 1)
        self.assertEqual(self.parentInstrument.EndDate(), self.returnDate, 'ParentInstrument End date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.StartDate(), self.returnDate, 'ChildInstrument Start date expected to be ' + str(self.returnDate))
        self.assertEqual(self.childInstrument.EndDate(), expectedChildEndDate, 'ChildInstrument Start date expected to be ' + str(expectedChildEndDate))
        
    def testSinglePartialReturnQuantities(self):
        quantityChild = self.parentQuantity - self.returnQuantity
        self.assertEqual(sl_functions.underlying_quantity(self.parentTrade.Quantity(), self.parentInstrument), self.parentQuantity, 'Parent Trades underlying quantity should be ' + str(self.parentQuantity))
        self.assertEqual(sl_functions.underlying_quantity(self.childTrade.Quantity(), self.childInstrument), quantityChild, 'Child trades underling quantity should be ' + str(quantityChild))
        
    def testSinglePartialReturnPointers(self):
        self.assertEqual(self.parentTrade.ConnectedTrade().Oid(), self.childTrade.Oid(), 'Parent trades ConnectedTrdnbr should point to child trade')
        self.assertEqual(self.childTrade.Contract().Oid(), self.parentTrade.Oid(), 'Child trades ContractTrdnbr should point to the parent trade')
        self.assertEqual(self.childTrade.TrxTrade().Oid(), self.parentTrade.Oid(), 'Child trades Trans Ref should point to the parent trade')
        
        
class TestRevertReturn(unittest.TestCase):

    def setUp(self):
        self.portfolio = PortfolioHelper.CreatePersistantPortfolio()
        self.stock = InstrumentHelper.CreatePersistantStock()
        
    def boConfirm(self, trade):
        trade.Status('BO Confirmed')
        trade.Commit()
        
    def assertTradeVoided(self, trade, message):
        self.assertEqual('Void', trade.Status(), '%s: Expected trade to be voided, got %s' % (message, trade.Status()))
        self.assertTrue(trade.SLPartialReturnNextTrade() == None, '%s: Expected voided trade not to have a next trade.' % message)
        self.assertTrue(trade.SLPartialReturnPrevTrade() == None, '%s: Expected voided trade not to have a previous trade.' % message)
        self.assertFalse(trade.SLPartialReturned(), '%s: Expected voided trade not to be partially returned.' % message)
        
    def assertRevertedTrade(self, trade, message):
        instrument = trade.Instrument()
        self.assertEqual('Open End', instrument.OpenEnd(), 'Expected Open End, got %s' % instrument.OpenEnd())
        self.assertEqual('BO Confirmed', trade.Status(), 'Expected BO Confirmed, got %s' % trade.Status())
        
    def testRevertNotSecurityLoan(self):
        trade = TradeHelper.BookTrade(self.portfolio, self.stock, today, 100)
        try:
            sl_partial_returns.revert_return(trade)
        except Exception as ex:
            expected = 'Cannot revert trade on instrument type Stock. Only SecurityLoan trades can be reverted.'
            actual = str(ex)
            self.assertEqual(expected, actual, 'Exception message not as expected. Expected [%s], got [%s]' % (expected, actual))
        else:
            self.fail('Expected an exception')
    
    def testRevertNotTerminated(self):
        loan = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.stock, 200, 300.67, 0.08, 'Internal', yesterday, 'BO Confirmed')
        instrument = loan.Instrument()
        instrument.OpenEnd('Open End')
        instrument.Commit()
        
        try:
            sl_partial_returns.revert_return(loan)
        except Exception as ex:
            expected = 'Cannot revert return on trade %i, only Terminated loans can be reverted: Open End' % loan.Oid()
            actual = str(ex)
            self.assertEqual(expected, actual, 'Exception message not as expected. Expected [%s], got [%s]' % (expected, actual))
        else:
            self.fail('Expected an exception')
            
    def testRevertSingleTrade(self):
        loan = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.stock, 300, 100.50, 0.05, 'Internal', yesterday, 'Terminated')
        instrument = loan.Instrument()
        instrument.OpenEnd('Terminated')
        instrument.Commit()
        
        self.assertEqual('Terminated', instrument.OpenEnd(), 'Expected Terminated, got %s' % instrument.OpenEnd())
        self.assertEqual('Terminated', loan.Status(), 'Expected Terminated status, got %s' % loan.Status())
        sl_partial_returns.revert_return(loan)
        self.assertEqual('Open End', instrument.OpenEnd(), 'Expected Open End, got %s' % instrument.OpenEnd())
        self.assertEqual('BO Confirmed', loan.Status(), 'Expected BO Confirmed, got %s' % loan.Status())
        
    def testRevertPartiallyReturnedTrade(self):
        loan1 = TradeHelper.BookSecurityLoanFromUnderlying(self.portfolio, self.stock, 1000000, 3000, 0.05, 'Internal', acm.Time().DateFromYMD(2010, 8, 2), 'BO Confirmed')
        loan2 = sl_partial_returns.partial_return(loan1, acm.Time().DateFromYMD(2010, 8, 10), 250000)
        self.boConfirm(loan2)
        loan3 = sl_partial_returns.partial_return(loan2, acm.Time().DateFromYMD(2010, 8, 16), 150000)
        self.boConfirm(loan3)
        loan4 = sl_partial_returns.partial_return(loan3, acm.Time().DateFromYMD(2010, 8, 25), 100000)
        sl_partial_returns.revert_return(loan2)
        loan1OpenEnd = loan1.Instrument().OpenEnd()
        self.assertEqual('Terminated', loan1OpenEnd, 'Expected loan1 to be terminated, got %s' % loan1OpenEnd)
        self.assertTrue(loan1.SLPartialReturned(), 'Expected loan1 to be partially returned')
        self.assertFalse(loan2.SLPartialReturned(), 'Expected loan2 not to be partially returned')
        self.assertEqual(loan2, loan1.SLPartialReturnNextTrade(), 'Expected loan1 to point to loan2')
        self.assertEqual(loan1, loan2.SLPartialReturnPrevTrade(), 'Expected loan2 to point to loan1')
        self.assertRevertedTrade(loan2, 'loan2')
        self.assertTradeVoided(loan3, 'loan3')
        self.assertTradeVoided(loan3, 'loan4')
        
def _run_tests():        
    suite = unittest.TestLoader().loadTestsFromModule(test_partial_returns)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestRevertReturn)
    unittest.TextTestRunner(verbosity=2).run(suite)

