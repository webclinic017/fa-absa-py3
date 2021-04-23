""" This module is the unit testing module for the Fvalidation module

Purpose               :  Only users in FO PSSecLend Trader group can deleted SecLoan cashflows. None other person with FO Call Trades in their profile
                         can deleted cashfflows.
                         Unit tests to check that zero-rate validation works correctly
Department and Desk   :  Money Market Desk
Requester             :  Venessa Kennel, Jansen Van Vuuren, Correy, Jan Sinkora
Developer             :  Heinrich Cronje, Rohan vd Walt, Jan Sinkora, Jan Sinkora
CR Number             :  616426,651043,586166,1024176

2014-08-31 Vojtech Sidorin  CHNG0002210109 Update imports to be compatible with new FValidation
2014-10-01 Dmitry Kovalenko CHNG0002328679 Removed usage of FValidation_depr_Helper
2016-03-11 Lawrence Mucheka ABITFA-4161    Remove call to validate_mm_instrument_update as rules FV93 and FV94-1 have been removed
"""

from FValidation_UnitTestHelper import *
import random, unittest
from FValidation_depr_General import *
import FValidation_depr_General as FValidation_General
from FValidation_depr_MoneyMarket import *
import FValidation_depr

from FValidation_core import DataValidationError, show_validation_warning


def AssertRaisesExp(self, callable,excClass, expectedMessage, *args):
    """ This function will result in a test case failure unless a specific exception with the correct exception message is raised when callable is invoked
         Arguments:

        Test Case
        Callable function
        Exception Class
        Exception message
        callable function arguments
    """

    try:
        callable(*args)
    except excClass, ex:
        if str(ex) != expectedMessage and expectedMessage != False:
            raise self.failureException, 'Exception message not as expected. Expected "%s", got "%s"' % (expectedMessage, ex)
    except Exception, ex:
        raise self.failureException, 'Raised %s (%s), expected %s' %(Exception.__name__, ex.message, excClass.__name__)
    else:
        raise self.failureException, '%s not raised.' %excClass.__name__

def AssertNoException(self, callable, *args):
    """ This function will result in a test case failure unless no exception is raised when callable is invoked
         Arguments:

        Test Case
        Callable function
        callable function arguments
    """
    try:
        callable(*args)
    except Exception, ex:
        raise self.failureException, '%s raised.' %str(ex)

class TestTradeInsert(unittest.TestCase):



    def testZeroTrade(self):
        """ No deposits booked at zero price"""
        instrument = InstrumentHelper.CreateFixedDepositInstrument()
        TradeDataDict = {"insaddr":instrument, "price":0}
        self.trade1 = TradeHelper.CreateMMTrade(TradeDataDict, isPersistant = False)
        TradeDataDict = {"insaddr":instrument, "price":5}
        self.trade2 = TradeHelper.CreateMMTrade(TradeDataDict)
        self.trade2.price = -1
        self.trade3 = TradeHelper.CreateTrade(TradeDataDict = {"price":0}, isPersistant = False)

        AssertRaisesExp(self, validate_trade_insert, DataValidationError, "Please enter a valid price that is greater than 0.", self.trade1, 'Insert')
        AssertRaisesExp(self, validate_trade_insert, DataValidationError, "Please enter a valid price that is greater than 0.", self.trade2, 'Update')
        AssertNoException(self, validate_trade_insert, self.trade3, 'Insert')

    def testCPRef(self):
        """ On Insert of Trade Clear out CP Ref"""
        self.CPRefTrd1 = TradeHelper.CreateTrade(TradeDataDict = {"your_ref": "TweedleDee"})
        self.CPRefTrd2 = TradeHelper.CreateTrade()
        trd2_clone = self.CPRefTrd2.clone()
        trd2_clone.your_ref = 'TweedleDum'
        trd2_clone.commit()
        self.assertEqual(self.CPRefTrd1.your_ref, '', 'CP Ref value not cleared on Insert of Trade')
        self.assertEqual(trd2_clone.your_ref, 'TweedleDum', 'CP Ref value cleared on Update of Trade')

class TestTradeGeneric(unittest.TestCase):


    def testTradeCPFICA(self):

        """ Test that a trade has a counterparty and that the counterparty is Fica Complaint"""

        a = {'FICA_Compliant': 'No'}
        nonFicaCP = PartyHelper.CreateCounterparty(AddInfoDict = a)
        self.FicaTrd1 = TradeHelper.CreateTrade(TradeDataDict = {"counterparty_ptynbr":nonFicaCP}, isPersistant = False)
        self.FicaTrd2 = TradeHelper.CreateTrade()
        self.FicaTrd2.counterparty_ptynbr = nonFicaCP
        self.FicaTrd3 = TradeHelper.CreateTrade(TradeDataDict = {"counterparty_ptynbr":None}, isPersistant = False)

        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "The Counterparty that you have selected to trade with is not FICA Compliant.", self.FicaTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "The Counterparty that you have selected to trade with is not FICA Compliant.", self.FicaTrd2, 'Update')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "Please select a Counterparty", self.FicaTrd3, 'Insert')



    def testTradeAcqFICA(self):

        """ Test that a trade has an acquirer and that the acquirer is Fica Complaint"""

        a = {'FICA_Compliant': 'No'}
        nonFicaAcq = PartyHelper.CreateAcquirer(AddInfoDict = a)
        self.FicaAcqTrd1 = TradeHelper.CreateTrade(TradeDataDict = {"acquirer_ptynbr":nonFicaAcq}, isPersistant = False)
        self.FicaAcqTrd2 = TradeHelper.CreateTrade()
        self.FicaAcqTrd2.acquirer_ptynbr = nonFicaAcq
        self.FicaAcqTrd3 = TradeHelper.CreateTrade(TradeDataDict = {"acquirer_ptynbr":None}, isPersistant = False)
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "The Acquirer that you have selected to trade with is not FICA Compliant.", self.FicaAcqTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "The Acquirer that you have selected to trade with is not FICA Compliant.", self.FicaAcqTrd2, 'Update')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "Please select an Acquirer", self.FicaAcqTrd3, 'Insert')


    def testTradeCPBesa(self):

        """ Test that BSB, Bonds and Repos not allowed against CP without Besa Member Agreement """

        nonBesaCP = PartyHelper.CreateCounterparty(AddInfoDict = {'BESA_Member_Agree': 'No', 'FICA_Compliant': 'Yes'})
        self.BesaBSBTrd1 = TradeHelper.CreateBSBTrade(TradeDataDict = {'counterparty_ptynbr':nonBesaCP}, isPersistant = False)
        self.BesaBSBTrd2 = TradeHelper.CreateBSBTrade()
        self.BesaBSBTrd2.counterparty_ptynbr = nonBesaCP
        nonBesaIntern = PartyHelper.CreateAcquirer(AddInfoDict = {'BESA_Member_Agree': 'No', 'FICA_Compliant': 'Yes'})
        self.BesaBSBTrd3 = TradeHelper.CreateBSBTrade(TradeDataDict = {'counterparty_ptynbr':nonBesaIntern}, isPersistant = False)


        bond = ael.Instrument['ZAR/R186']
        p = bond.used_price()
        self.BesaBondTrd1 = TradeHelper.CreateTrade(TradeDataDict = {'counterparty_ptynbr':nonBesaCP,'insaddr': bond, 'price':p}, isPersistant = False)
        self.BesaBondTrd2 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': bond, 'price':p})
        self.BesaBondTrd2.counterparty_ptynbr = nonBesaCP

        repo = InstrumentHelper.CreateRepoInstrument()
        self.BesaRepoTrd1 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': repo, 'counterparty_ptynbr':nonBesaCP}, isPersistant = False)
        self.BesaRepoTrd2 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': repo})
        self.BesaRepoTrd2.counterparty_ptynbr = nonBesaCP

        err = "The party that you selected to trade with does not have a BESA Client agreement set up"
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaBSBTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaBSBTrd2, 'Update')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaBondTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaBondTrd2, 'Update')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaRepoTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.BesaRepoTrd2, 'Update')
        AssertNoException(self, validate_trade_gen, self.BesaBSBTrd3, 'Insert')

    def testTradeCPBSB(self):

        """ Test that no BSB can only be booked with specific counterparties """
        self.BSBCPTrd1 = TradeHelper.CreateBSBTrade(isPersistant = False)
        self.BSBCPTrd2 = TradeHelper.CreateBSBTrade(isPersistant = False)
        self.BSBCPTrd2.counterparty_ptynbr = BSB_COUNTERPARTIES[0]

        AssertNoException(self, validate_trade_gen, self.BSBCPTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, "Please book a Repo not a BSB with this counterparty", self.BSBCPTrd2, 'Insert')

    def testIRDSimulatedPort(self):

        """ Only simulated trades allowed in portfolio IRD_SIMULATED"""
        irdsim = ael.Portfolio['IRD_SIMULATED']

        self.IRDSimTrd1 = TradeHelper.CreateTrade(TradeDataDict = {'prfnbr': irdsim}, isPersistant = False)
        self.IRDSimTrd2 = TradeHelper.CreateTrade()
        self.IRDSimTrd2.prfnbr = irdsim
        self.IRDSimTrd3 = TradeHelper.CreateTrade(TradeDataDict = {'prfnbr': irdsim, 'status':'Simulated'}, isPersistant = False )

        err = "Unable to commit the trade because only simulated trades are allowed in the IRD_SIMULATED Portfolio"
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.IRDSimTrd1, 'Insert')
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.IRDSimTrd2, 'Update')
        AssertNoException(self, validate_trade_gen, self.IRDSimTrd3, 'Insert')


    def testMentisPort(self):

        """ Trades in Mentis Portfolios must have Mentis Project Number add info"""
        mentisAdd = {'Mentis Project Num': '123456'}
        mentisPort = ael.Portfolio[MENTIS_PORTS[0]]
        self.MentisTrd1 = TradeHelper.CreateTrade(TradeDataDict = {'prfnbr':mentisPort}, isPersistant = False)
        self.MentisTrd2 = TradeHelper.CreateTrade(TradeDataDict = {'prfnbr':mentisPort}, AddInfoDict = mentisAdd, isPersistant = False)

        err = "Traders not allowed to capture trade without Mentis Project Num"
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.MentisTrd1, 'Insert')
        AssertNoException(self, validate_trade_gen, self.MentisTrd2, 'Insert')



class TestTradeUpdate(unittest.TestCase):

    def testAggAndArchive(self):
        """Test that no updates allowed on Aggregate and Archived Trade"""
        self.AATrd1 = TradeHelper.CreateTrade(TradeDataDict = {"archive_status":1}, isPersistant = False)
        self.AATrd1.price = 10
        self.AATrd2 = TradeHelper.CreateTrade(TradeDataDict = {"aggregate":1}, isPersistant = False)
        self.AATrd2.price = 10
        AssertRaisesExp(self, validate_trade_update, DataValidationError, "No changes allowed to Archived trades", self.AATrd1, 'Update')
        AssertRaisesExp(self, validate_trade_update, DataValidationError, "No changes allowed to Aggregate trades", self.AATrd2, 'Update')


class TestCallTrade(unittest.TestCase):

    CALL_REGION = "INST GAUTENG"

    def testCallRegion(self):
        """Ensure that the additional info field Call Region is filled in for Funding Desk Call Trades"""

        acq = PartyHelper.CreateAcquirer()
        ad = {"Funding Instype":"Call Deposit DTI", 'Account_Name': str(uuid.uuid4())}
        self.RegionTrd1 = TradeHelper.CreateCallTrade(AddInfoDict =ad, isPersistant = False)
        self.RegionTrd2 = TradeHelper.CreateCallTrade()
        to_del = None
        for a in self.RegionTrd2.additional_infos():
            if a.addinf_specnbr.field_name == 'Call_Region':
                to_del = a
                break
        to_del.delete()
        self.RegionTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': acq}, AddInfoDict = ad, isPersistant = False)

        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please select a region for the Call Account', self.RegionTrd1, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please select a region for the Call Account', self.RegionTrd2, 'Update')
        AssertNoException(self, validate_call_trade, self.RegionTrd3, 'Insert')

    def testAccName(self):
        """Ensure that the additional info field Account Name is filled in for Funding Desk Call Trades"""

        ad = {"Funding Instype":"Call Deposit DTI", "Call_Region":self.CALL_REGION}
        self.AccNameTrd1 = TradeHelper.CreateCallTrade(AddInfoDict =ad, isPersistant = False)
        self.AccNameTrd2 = TradeHelper.CreateCallTrade()
        to_del = None
        for a in self.AccNameTrd2.additional_infos():
            if a.addinf_specnbr.field_name == 'Account_Name':
                to_del = a
                break
        to_del.delete()
        self.AccNameTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': PS_DESK}, AddInfoDict = ad, isPersistant = False)
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please add an Account Name.', self.AccNameTrd1, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please add an Account Name.', self.AccNameTrd2, 'Update')
        AssertNoException(self, validate_call_trade, self.AccNameTrd3, 'Insert')

    def testFundingType(self):
        """Ensure that the additional info field Funding Instype is filled in correctly Funding Desk Call Trades"""

        acq = PartyHelper.CreateAcquirer()
        ad = {"Funding Instype":"CD", "Call_Region":self.CALL_REGION, 'Account_Name': str(uuid.uuid4())}
        self.FundingTrd1 = TradeHelper.CreateCallTrade(AddInfoDict =ad, isPersistant = False)
        self.FundingTrd2 = TradeHelper.CreateCallTrade()
        for a in self.FundingTrd2.additional_infos():
            if a.addinf_specnbr.field_name == 'Funding Instype':
                a.value = "CD"
        self.FundingTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': acq}, AddInfoDict = ad, isPersistant = False)


        self.FundingTrd4 = TradeHelper.CreateNonZARCallTrade(AddInfoDict = {}, isPersistant = False)
        self.FundingTrd5 = TradeHelper.CreateNonZARCallTrade()
        for ai in self.FundingTrd5.additional_infos():
            if ai.addinf_specnbr.field_name == 'Funding Instype':
                ai.value = "CD"

        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please change the Funding Instype', self.FundingTrd1, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'Please change the Funding Instype', self.FundingTrd2, 'Update')
        AssertNoException(self, validate_call_trade, self.FundingTrd3, 'Insert')

    def testCallPortfolio(self):
        """Ensure that a Funding Desk Call Trade is booked into a Call_ portfolio"""

        acq = PartyHelper.CreateAcquirer()
        port = PortfolioHelper.CreatePhysicalPortfolio()
        self.CallPortTrd1 = TradeHelper.CreateCallTrade(TradeDataDict ={'prfnbr': port}, isPersistant = False)
        self.CallPortTrd2 = TradeHelper.CreateCallTrade()
        self.CallPortTrd2.prfnbr = port
        self.CallPortTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': acq}, isPersistant = False)

        err = 'Unable to commit the trade. Please pick a Call portfolio'
        AssertRaisesExp(self, validate_call_trade, DataValidationError, err, self.CallPortTrd1, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, err, self.CallPortTrd2, 'Update')
        AssertNoException(self, validate_call_trade, self.CallPortTrd3, 'Insert')

    def testCallFixedPeriod(self):
        """Ensure that a Funding Desk Call Trade Instrument has the Fixed Period ticked on."""

        acq = PartyHelper.CreateAcquirer()
        leg = {'fixed_coupon': 0}
        ins = InstrumentHelper.CreateCallAccountInstrument(LegDataDict = leg)
        self.CallFixedPeriodTrd1 = TradeHelper.CreateCallTrade(TradeDataDict ={'insaddr': ins}, isPersistant = False)
        self.CallFixedPeriodTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'insaddr':ins,'acquirer_ptynbr': acq}, isPersistant = False)
        err = 'Please select the Fixed Period.'
        AssertRaisesExp(self, validate_call_trade, DataValidationError, err, self.CallFixedPeriodTrd1, 'Insert')
        AssertNoException(self, validate_call_trade, self.CallFixedPeriodTrd3, 'Insert')


    def testCallDayCount(self):
        """Ensure that a Funding Desk Call Trade Instrument has the correct day count method"""

        acq = PartyHelper.CreateAcquirer()
        leg = {'daycount_method': 'Act/360'}
        ins = InstrumentHelper.CreateCallAccountInstrument(LegDataDict = leg)
        self.CallDCTrd1 = TradeHelper.CreateCallTrade(TradeDataDict ={'insaddr': ins}, isPersistant = False)
        self.CallDCTrd2 = TradeHelper.CreateCallTrade(TradeDataDict = {'insaddr':ins,'acquirer_ptynbr': acq}, isPersistant = False)

        USD = ael.Instrument['USD']
        leg = {'curr': USD, 'daycount_method': 'Act/365' , 'reinvest':1}
        ins = InstrumentHelper.CreateCallAccountInstrument(InsDataDict = {'curr': USD}, LegDataDict = leg)
        self.CallDCTrd3 = TradeHelper.CreateNonZARCallTrade(TradeDataDict = {'insaddr':ins}, isPersistant= False)


        ins1 = InstrumentHelper.CreateCallAccountInstrument(InsDataDict = {'curr': USD}, LegDataDict = leg)
        self.CallDCTrd4 = TradeHelper.CreateNonZARCallTrade(TradeDataDict = {'insaddr':ins1, 'acquirer_ptynbr': acq})
        self.CallDCTrd4.acquirer_ptynbr = NON_ZAR_CFC

        err = 'The daycount method is not Act/365.'
        AssertRaisesExp(self, validate_call_trade, DataValidationError, err, self.CallDCTrd1, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'The daycount method for the USD currency should be Act/360', self.CallDCTrd3, 'Insert')
        AssertRaisesExp(self, validate_call_trade, DataValidationError, 'The daycount method for the USD currency should be Act/360', self.CallDCTrd4, 'Update')
        AssertNoException(self, validate_call_trade, self.CallDCTrd2, 'Insert')


class TestCallInstrument(unittest.TestCase):


    def testInsDayCount(self):
        """Ensure that the daycount method is correct on a call account"""
        acq = PartyHelper.CreateAcquirer()
        self.CallDCTrd1 = TradeHelper.CreateCallTrade()
        ins_c = self.CallDCTrd1.insaddr.clone()
        lc = ins_c.legs()[0]
        lc.daycount_method = 'Act/360'

        self.CallDCTrd2 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': acq})
        ins1_c = self.CallDCTrd2.insaddr.clone()
        lc1 = ins1_c.legs()[0]
        lc1.daycount_method = 'Act/360'

        self.CallDCTrd3 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': PS_DESK})
        ps_ins_c = self.CallDCTrd3.insaddr.clone()
        lc3 = ps_ins_c.legs()[0]
        lc3.daycount_method = 'Act/360'

        USD = ael.Instrument['USD']
        leg = {'curr': USD, 'daycount_method': 'Act/360' , 'reinvest':1}
        addinf = {'Funding Instype':'Non Zar CFC I/Div'}
        ins = InstrumentHelper.CreateCallAccountInstrument(InsDataDict = {'curr': USD}, LegDataDict = leg)
        self.CallDCTrd4 = TradeHelper.CreateCallTrade(TradeDataDict = {'insaddr': ins,'acquirer_ptynbr': NON_ZAR_CFC, 'curr':USD}, AddInfoDict = addinf)
        ael.poll()
        non_zar_ins_c = self.CallDCTrd4.insaddr.clone()
        lc4 = non_zar_ins_c.legs()[0]
        lc4.daycount_method = 'Act/365'

        err = 'The daycount method is not Act/365.'
        AssertRaisesExp(self, validate_call_instrument, DataValidationError, err, ins_c, 'Update')
        err = 'The daycount method for the ZAR currency should be Act/365'
        AssertRaisesExp(self, validate_call_instrument, DataValidationError, err, ps_ins_c, 'Update')
        AssertRaisesExp(self, validate_call_instrument, DataValidationError, err, ps_ins_c, 'Update')
        AssertRaisesExp(self, validate_call_instrument, DataValidationError, 'The daycount method for the USD currency should be Act/360', non_zar_ins_c, 'Update')
        AssertNoException(self, validate_call_instrument, ins1_c, 'Insert')

    def testInsFixedPeriod(self):
        """Ensure that the Fixed period is correct on a funding desk instrument"""
        acq = PartyHelper.CreateAcquirer()
        self.CallInsFixedPeriodTrd1 = TradeHelper.CreateCallTrade()
        ins_c = self.CallInsFixedPeriodTrd1.insaddr.clone()
        lc = ins_c.legs()[0]
        lc.fixed_coupon = 0

        self.CallInsFixedPeriodTrd2 = TradeHelper.CreateCallTrade(TradeDataDict = {'acquirer_ptynbr': acq})
        ins1_c = self.CallInsFixedPeriodTrd2.insaddr.clone()
        lc1 = ins1_c.legs()[0]
        lc1.fixed_coupon = 0

        err = 'Please select the Fixed Period.'
        AssertRaisesExp(self, validate_call_instrument, DataValidationError, err, ins_c, 'Update')
        AssertNoException(self, validate_call_instrument, ins1_c, 'Update')


class TestCommTrade(unittest.TestCase):

    def testCommodityValueDay(self):
        """ Comm Trades with an external ID beginning with SFX2_ and instrument name HOLDER, have value and acq day set to First Business Day of Next Month"""
        holderIns = ael.Instrument['ZAR/WMAZ/HOLDER']
        optkey = 'SFX2_' + str(uuid.uuid4())[0:24]
        self.ComValTrd1 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': holderIns, 'optional_key': optkey})

        self.ComValTrd2 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': holderIns}, isPersistant = False)
        origValueDay = self.ComValTrd2.value_day
        self.ComValTrd2.commit()

        self.assertEqual(self.ComValTrd1.value_day, FIRSTDAYOFNEXTMONTH, 'Value day is not equal to first business day of next month')
        self.assertEqual(self.ComValTrd2.value_day, origValueDay, 'Value day does not remain unchanged for non Safex trade.')

    def testCommodityAfriStatus(self):
        """Commodities booked against the Agri Desk must have an AgriStatus"""
        commodity = ael.Instrument['ZAR/WMAZ/PhysWM1']
        addinf = {'AgriStatus': 'Physical'}
        d = {'insaddr': commodity, 'acquirer_ptynbr': AGRI_DESK}
        self.ComAgriStatusTrd1 = TradeHelper.CreateTrade(TradeDataDict = d, isPersistant = False)
        self.ComAgriStatusTrd2 = TradeHelper.CreateTrade(TradeDataDict = d, AddInfoDict = addinf, isPersistant = False)
        self.ComAgriStatusTrd3 = TradeHelper.CreateTrade(TradeDataDict = {'insaddr': commodity}, isPersistant = False)

        err = 'Please select Physical in the AgriStatus AddInfo field'
        AssertRaisesExp(self, validate_trade_gen, DataValidationError, err, self.ComAgriStatusTrd1, 'Insert')
        AssertNoException(self, validate_trade_gen, self.ComAgriStatusTrd2, 'Insert')
        AssertNoException(self, validate_trade_gen, self.ComAgriStatusTrd3, 'Insert')

class TestDeleteCashFlows(unittest.TestCase):

    def testFOCallTrader(self):
        """Any user with FO Call Trader linked to their profile should not be able to delete a cash flow"""
        accessProfileList = ['FO Call Trader']
        err = 'You have FO Call Trader in your profile. You are not allowed to delete cashflows.'

        """Default test. Remove FO Call Trader from access profile"""
        ProfileHelper.RemoveAccessProfileFromGroup(accessProfileList)
        cashFlowList = []

        """Case 1: Default Test - do not have FO Call Trader. Book a Call Account and delete a cashflow."""
        callTrade1 = TradeHelper.CreateCallTrade()
        cashFlowList.append(callTrade1.insaddr.legs()[0].cash_flows()[0])
        AssertNoException(self, validate_cashFlow_delete, cashFlowList[0], 'Delete')

        """Add FO Call Trader to access profile"""
        ProfileHelper.AddAccessProfileToGroup(accessProfileList)

        """Case 2: FO Call Trader is added to profile. Book a Call Account and delete a cashflow."""
        callTrade2 = TradeHelper.CreateCallTrade()
        cashFlowList[0] = callTrade2.insaddr.legs()[0].cash_flows()[0]
        AssertRaisesExp(self, validate_cashFlow_delete, DataValidationError, err, cashFlowList[0], 'Delete')

        """Move user to FO PSSecLend Trader group."""
        self.OriginalUserGroup = acm.FUser[ael.user().userid].UserGroup().Name()
        ProfileHelper.MoveUserToDifferentUserGroup('FO PSSecLend Trader')

        """Case 3: Book a Call Account and delete a cashflow."""
        callTrade3 = TradeHelper.CreateCallTrade()
        cashFlowList[0] = callTrade3.insaddr.legs()[0].cash_flows()[0]
        AssertRaisesExp(self, validate_cashFlow_delete, DataValidationError, err, cashFlowList[0], 'Delete')

        """Case 4: Book a Security Loan and delete a cashflow."""
        securityLoan1 = InstrumentHelper.CreateSecLoanInstrument()
        cashFlowList[0] = securityLoan1.legs()[0].cash_flows()[0]
        AssertNoException(self, validate_cashFlow_delete, cashFlowList[0], 'Delete')

        """Move user to original user group."""
        ProfileHelper.MoveUserToDifferentUserGroup(self.OriginalUserGroup)

class TestMMTrade(unittest.TestCase):
    def testNonZeroRateFundingDeskCheck(self):
        """ Checks that trade with acquirer Funding Desk doesn't have zero rate, excludes FRN and Bill ins types """

        err = 'Trades With Zero Rate Not Allowed On Funding Desk'

        self.frnTrade = TradeHelper.CreateFRNTrade(TradeDataDict = {'acquirer_ptynbr' : ael.Party['Funding Desk']}, isPersistant = False)
        self.billTrade = TradeHelper.CreateBillTrade( TradeDataDict = {'acquirer_ptynbr' : ael.Party['Funding Desk']}, isPersistant = False)
        self.bsbTrade = TradeHelper.CreateBSBTrade( TradeDataDict = {'acquirer_ptynbr' : ael.Party['Funding Desk']}, isPersistant = False)
        AssertNoException(self, validate_mm_trade, self.frnTrade, 'Insert')
        AssertNoException(self, validate_mm_trade, self.billTrade, 'Insert')
        AssertNoException(self, validate_mm_trade, self.bsbTrade, 'Insert')

        self.callIns = InstrumentHelper.CreateCallAccountInstrument(LegDataDict = {'fixed_rate':0}, isPersistant = False)
        self.callTrade = TradeHelper.CreateCallTrade( TradeDataDict = {'insaddr': self.callIns, 'acquirer_ptynbr' : ael.Party['Funding Desk']}, isPersistant = False)
        AssertRaisesExp(self, validate_mm_trade, DataValidationError, err, self.callTrade, 'Insert')
        AssertRaisesExp(self, validate_mm_trade, DataValidationError, err, self.callTrade, 'Update')

        self.callIns2 = InstrumentHelper.CreateCallAccountInstrument(LegDataDict = {'fixed_rate':10}, isPersistant = True)
        self.callTrade2 = TradeHelper.CreateCallTrade( TradeDataDict = {'insaddr': self.callIns2, 'acquirer_ptynbr' : ael.Party['Funding Desk']}, isPersistant = True)
        clonedIns = self.callIns2.clone()
        clonedIns.legs()[0].fixed_rate = 0
        ael.poll()

    def testBackdatedPremium(self):
        """ Checks that the premium is updated on backdated mm trades - ABITFA-973"""
        LASTYEAR = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -365)
        self.callIns = InstrumentHelper.CreateFixedDepositInstrument(LegDataDict = {'fixed_rate':10, 'start_day' : LASTYEAR}, isPersistant = True)
        self.callTrade = TradeHelper.CreateMMTrade( TradeDataDict = {'insaddr': self.callIns, 'acquirer_ptynbr' : ael.Party['Funding Desk'], 'value_day' : LASTYEAR, 'acquire_day' : LASTYEAR}, isPersistant = True)

        self.assertNotEqual(self.callTrade.premium, 0, 'Premium is zero')
        self.assertEqual(self.callTrade.premium, self.callTrade.quantity * self.callTrade.insaddr.contr_size * -1, 'Premium calc not consistent')


class TestOptionsWithUnderlyingFixedRates(unittest.TestCase):
    """Test for options that have an und instrument with a fixed rate.

    The Option and the instrument must have the same fixed rates if a trade is to be
    booked. Once a non-voided trade is assigned to an instrument, both the rates must
    be forbidden from changing.

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_swap_fixed_leg(self, und):
        """
        Gets the fixed leg for the swap.
        """
        return filter(lambda l: l.type == 'Fixed', und.legs())[0].clone()


    def test_correct_swaption_rates(self):
        """
        A swaption where the option has strike price equal to the
        swap's fixed leg's rate should be booked correctly.

        """
        ins_name = 'UNITTEST/OPTION/SWAP/#1'

        ins = InstrumentHelper.get_or_create_swaption_instrument(ins_name)
        ins = ins.clone()

        ins.strike_price = 1.0
        ins.commit()
        ins = InstrumentHelper.get_or_create_swaption_instrument(ins_name)

        ael.poll()

        und = ael.Instrument[ins.und_insaddr.insid]

        # get the fixed swap leg
        fixed_leg = self.get_swap_fixed_leg(und)

        # set the same rate as the strike price
        fixed_leg.fixed_rate = 1.0
        fixed_leg.commit()

        trade = TradeHelper.create_swaption_trade(trade_data_dict={'insaddr': ins}, is_persistent=False)

        # the test itself
        AssertNoException(self, validate_swap_or_fra_option_trade_rates, trade, "Insert")

    def test_incorrect_swaption_rates(self):
        """
        A swaption where the option has strike price different from the swap's
        fixed leg's rate should not be booked.
        """
        ins_name = 'UNITTEST/OPTION/SWAP/#2'

        ins = InstrumentHelper.get_or_create_swaption_instrument(ins_name)
        ins = ins.clone()

        ins.strike_price = 1.1
        ins.commit()

        ael.poll()

        und = ael.Instrument[ins.und_insaddr.insid]

        # get the fixed swap leg
        fixed_leg = self.get_swap_fixed_leg(und)

        # set the rate to a different value than the strike price
        fixed_leg.fixed_rate = 1.0
        fixed_leg.commit()


        trade = TradeHelper.create_swaption_trade(trade_data_dict={'insaddr': ins}, is_persistent=False)

        # the test itself
        # uncomment if the validations only show information
        #AssertRaisesExp(self, validate_swap_or_fra_option_trade_rates, DataValidationError, "Warning: booking an Option trade while the strike price is different from the underlying fixed rate.", trade, "Insert")
        AssertRaisesExp(self, validate_swap_or_fra_option_trade_rates, DataValidationError, "Booking an Option trade while the strike price is different from the underlying fixed rate.", trade, "Insert")

    def test_swaption_successfull_rate_change(self):
        """
        The rates can change if there aren't any referencing trades
        """
        ins_name = 'UNITTEST/OPTION/SWAP/#3'

        # create a swaption instrument
        ins = InstrumentHelper.get_or_create_swaption_instrument(ins_name)
        ins = ins.clone()
        und = ins.und_insaddr

        ins.strike_price = 1.0
        AssertNoException(self, validate_swap_or_fra_option_instrument_change, ins, 'Update')

        ins.commit()

        # get the fixed swap leg
        fixed_leg = self.get_swap_fixed_leg(und)
        fixed_leg.fixed_rate = 2.0
        AssertNoException(self, validate_fixed_leg_change, fixed_leg, 'Update')

    def test_swaption_rate_change_with_booked_trades(self):
        """
        When there are trades booked, an info should be displayed.
        """
        ins_name = 'UNITTEST/OPTION/SWAP/#4'

        # create a swaption instrument
        ins = InstrumentHelper.get_or_create_swaption_instrument(ins_name)
        ins = ins.clone()

        # set the rates to the same value
        ins.strike_price = 1.0
        ins.commit()
        ins = ins.clone()

        ael.poll()

        und = ael.Instrument[ins.und_insaddr.insid]

        # get the fixed swap leg
        fixed_leg = self.get_swap_fixed_leg(und)
        fixed_leg.fixed_rate = 1.0
        fixed_leg.commit()
        fixed_leg = fixed_leg.clone()

        trade = TradeHelper.create_swaption_trade(trade_data_dict={'insaddr': ins})

        ael.poll()

        ins.strike_price = 2.0
        # uncomment if the validations only show information
        AssertRaisesExp(self, validate_swap_or_fra_option_instrument_change, DataValidationError, "Warning: Changing the strike price while there are trades booked for this option.", ins, "Update")
        #AssertRaisesExp(self, validate_swap_or_fra_option_instrument_change, DataValidationError, "Changing the strike price while there are trades booked for this option.", ins, "Update")

        fixed_leg.fixed_rate = 3.0
        # uncomment if the validations only show information
        AssertRaisesExp(self, validate_fixed_leg_change, DataValidationError, "Warning: Changing the fixed rate when there are trades booked for overlying options: {0}.".format(ins_name), fixed_leg, "Update")
        #AssertRaisesExp(self, validate_fixed_leg_change, DataValidationError, "Changing the fixed rate when there are trades booked for overlying options: {0}.".format(ins_name), fixed_leg, "Update")

    def get_fra_fixed_leg(self, ins):
        """
        Gets the FRA fixed leg (which is the only leg that there is).
        """
        return ins.legs()[0].clone()

    def test_correct_FRA_option_rates(self):
        """
        A FRA-based option should be booked correctly if the strike
        price and the underlying fixed rate are the same.

        """
        ins_name = 'UNITTEST/OPTION/FRA/#1'

        ins = InstrumentHelper.get_or_create_fra_option_instrument(ins_name)
        ins = ins.clone()
        und = ins.und_insaddr

        # the empty FRA instrument has its fixed rate set to 0.0, set this to the same value
        ins.strike_price = 0.0
        ins.commit()

        trade = TradeHelper.create_fra_option_trade(trade_data_dict={'insaddr': ins}, is_persistent=False)

        # the test
        AssertNoException(self, validate_swap_or_fra_option_trade_rates, trade, "Insert")

    def test_incorrect_FRA_option_rates(self):
        """
        A FRA-based option should NOT be booked correctly if the strike
        price and the underlying fixed rate differ.

        """
        ins_name = 'UNITTEST/OPTION/FRA/#2'

        ins = InstrumentHelper.get_or_create_fra_option_instrument(ins_name)
        ins = ins.clone()
        und = ins.und_insaddr

        # set this to another value to 0.0
        ins.strike_price = 0.1
        ins.commit()

        trade = TradeHelper.create_fra_option_trade(trade_data_dict={'insaddr': ins}, is_persistent=False)

        # the test itself
        # uncomment if the validations only show information
        #AssertRaisesExp(self, validate_swap_or_fra_option_trade_rates, DataValidationError, "Warning: booking an Option trade while the strike price is different from the underlying fixed rate.", trade, "Insert")
        AssertRaisesExp(self, validate_swap_or_fra_option_trade_rates, DataValidationError, "Booking an Option trade while the strike price is different from the underlying fixed rate.", trade, "Insert")

    def test_fra_option_successfull_rate_change(self):
        """
        The rates can change if there aren't any referencing trades.
        """
        ins_name = 'UNITTEST/OPTION/FRA/#3'

        # create a swaption instrument
        ins = InstrumentHelper.get_or_create_fra_option_instrument(ins_name)
        ins = ins.clone()
        und = ins.und_insaddr

        ins.strike_price = 1.0
        AssertNoException(self, validate_swap_or_fra_option_instrument_change, ins, 'Update')

        ins.commit()

        # get the fixed swap leg
        fixed_leg = self.get_fra_fixed_leg(und)
        fixed_leg.fixed_rate = 2.0
        AssertNoException(self, validate_fixed_leg_change, fixed_leg, 'Update')

    def test_fra_option_rate_change_with_booked_trades(self):
        """
        When there are trades booked, an info should be displayed.
        """
        ins_name = 'UNITTEST/OPTION/FRA/#4'

        # create a swaption instrument
        ins = InstrumentHelper.get_or_create_fra_option_instrument(ins_name)
        ins = ins.clone()

        # set the rates to the same value
        ins.strike_price = 1.0
        ins.commit()
        ins = ins.clone()

        ael.poll()

        und = ael.Instrument[ins.und_insaddr.insid]

        # get the fixed swap leg
        fixed_leg = self.get_fra_fixed_leg(und)
        fixed_leg.fixed_rate = 1.0
        fixed_leg.commit()
        fixed_leg = fixed_leg.clone()

        TradeHelper.create_fra_option_trade(trade_data_dict={'insaddr': ins})

        ael.poll()

        ins.strike_price = 2.0
        # uncomment if the validations only show information
        AssertRaisesExp(self, validate_swap_or_fra_option_instrument_change, DataValidationError, "Warning: Changing the strike price while there are trades booked for this option.", ins, "Update")
        #AssertRaisesExp(self, validate_swap_or_fra_option_instrument_change, DataValidationError, "Changing the strike price while there are trades booked for this option.", ins, "Update")

        fixed_leg.fixed_rate = 3.0
        # uncomment if the validations only show information
        AssertRaisesExp(self, validate_fixed_leg_change, DataValidationError, "Warning: Changing the fixed rate when there are trades booked for overlying options: {0}.".format(ins_name), fixed_leg, "Update")
        #AssertRaisesExp(self, validate_fixed_leg_change, DataValidationError, "Changing the fixed rate when there are trades booked for overlying options: {0}.".format(ins_name), fixed_leg, "Update")

class TestTRSIndexRefdInstrumentChange(unittest.TestCase):
    def component_allowed(self, flag):
        self.mocked_components[(self.component, self.component_type)] = flag

    def setUp(self):
        self.mocked_components = {}
        self.component = 'Modify FO Part'
        self.component_type = 'Operation'

        self.original_func = FValidation_General.user_is_allowed
        def user_is_allowed(user, component, component_type):
            if (component, component_type) in self.mocked_components:
                return self.mocked_components[(component, component_type)]
            else:
                return self.original_func(user, component, component_type)
        FValidation_General.user_is_allowed = user_is_allowed

        def validate_transaction(transaction_list, *rest):
            return transaction_list

        self.original_validation = FValidation.validate_transaction
        FValidation.validate_transaction = validate_transaction

    def tearDown(self):
        FValidation_General.user_is_allowed = self.original_func
        FValidation.validate_transaction = self.original_validation

    def test_trs_with_no_trades(self):
        insid = 'UNITTEST/TRS/EQIndex/#1'
        und_insid = 'UNITTEST/TRS/EQIndex/REF/#1'
        trs = InstrumentHelper.get_or_create_trs_eqi_instrument(insid, und_insid)

        eqi = trs.legs()[1].index_ref
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')
        self.component_allowed(False)
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')

    def test_trs_with_trades_without_component(self):
        insid = 'UNITTEST/TRS/EQIndex/#4'
        und_insid = 'UNITTEST/TRS/EQIndex/REF/#4'
        trs = InstrumentHelper.get_or_create_trs_eqi_instrument(insid, und_insid)

        if not trs.trades():
            TradeHelper.create_trs_trade(trs)
            ael.poll()
        t = trs.trades()[0].clone()
        t.status = 'Void'
        t.commit()
        ael.poll()
        t = trs.trades()[0].clone()
        t.status = 'FO Confirmed'
        t.commit()
        ael.poll()

        eqi = trs.legs()[1].index_ref
        self.component_allowed(True)
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')
        self.component_allowed(False)
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')

        t = trs.trades()[0].clone()
        t.status = 'BO Confirmed'
        t.commit()
        ael.poll()
        self.component_allowed(True)
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')
        self.component_allowed(False)
        AssertRaisesExp(self, validate_trs_index_ref_change, DataValidationError, False, eqi, 'Update')

        t = trs.trades()[0].clone()
        t.status = 'BO-BO Confirmed'
        t.commit()
        ael.poll()
        self.component_allowed(True)
        AssertNoException(self, validate_trs_index_ref_change, eqi, 'Update')
        self.component_allowed(False)
        AssertRaisesExp(self, validate_trs_index_ref_change, DataValidationError, False, eqi, 'Update')


class TestAggregationCashPostingLock(unittest.TestCase):
    def setUp(self):
        """Prepare the trade."""
        insid = 'UNITTEST/STOCK/#1'

        i = InstrumentHelper.get_or_create_stock_instrument(insid)

        p = ael.Portfolio['Call_2474']

        t = ael.Trade.new(i)
        t.quantity = 10
        t.prfnbr = p
        t.acquirer_ptynbr = 'FMAINTENANCE'
        t.counterparty_ptynbr = 'FMAINTENANCE'
        t.commit()
        self.owner = t.owner_usrnbr

        self.t = t

    def test_non_locked_trade(self):
        t = self.t.clone()
        t.type = 'Normal'
        t.owner_usrnbr = self.owner
        t.text1 = ''
        t.commit()
        t = t.clone()
        t.quantity = 100

        AssertNoException(self, validate_cash_posting_trade_lock, t, 'Update')

    def test_locked_trade(self):
        t = self.t.clone()
        t.type = 'Cash posting'
        t.owner_usrnbr = 'FMAINTENANCE'
        t.text1 = LOCKED_TRADE_TEXT
        t.commit()
        ael.poll()
        t = ael.Trade[t.trdnbr].clone()
        t.quantity = 200


        AssertRaisesExp(self, validate_cash_posting_trade_lock, DataValidationError, False, t, 'Update')

blgd = acm.FBusinessLogicGUIDefault() 

class TestTradesFromPaceFXO(unittest.TestCase):
    """Unit tests for Pace-FXO trades."""
    def _create_trade(self, ins_args = {}, trd_args = {}):
        usd = ael.Instrument['USD']
        zar = ael.Instrument['ZAR']
        def_ins_args = { 'und_insaddr': zar, 'curr': usd, 'strike_curr': usd, 
            'strike_price': 9.7571, 'contr_size': 1.0, 'exp_day': ael.date('2013-08-02') }
        def_ins_args.update(ins_args)
        
        opt = InstrumentHelper.create_option_instrument(def_ins_args)
        
        def_trade_args = {
            'insaddr': opt, 
            'premium': -56330.0, 
            'price': 0.0,
            'quantity': 1000000.0, 
            'value_day': ael.date('2013-07-30'), 
            'acquire_day': ael.date('2013-07-30'), 
            'optional_key': 'PFXO_{0}'.format(random.randint(99000000, 100000000)),
            'curr': zar, 
            'time': ael.date('2013-07-25').to_time(),
            'optkey4_chlnbr': ael.ChoiceList.read('list="TradeKey4" and entry="USD/ZAR"') }
        def_trade_args.update(trd_args)
        
        trade = TradeHelper.CreateTrade(def_trade_args)
        return trade
        
    def test_price_is_set_for_pfxo_option_trade(self):
        """Trade price should be set in FValidation for PFXO options."""
        trade = self._create_trade()
        
        if trade.trdnbr < 0: # for some reason CreateTrade does not throw exception when validation fails
            raise Exception("Trade was not committed.")
        
        if trade.price == 0:
            raise Exception('Trade price is not set.')
    
    def test_price_is_not_set_for_nonpfxo_option_trade(self):
        """Trade price should NOT be set in FValidation for non-PFXO options."""
        trade = self._create_trade(trd_args = { 'optional_key': '' })
        
        if trade.trdnbr < 0: # for some reason CreateTrade does not throw exception when validation fails
            raise Exception("Trade was not committed.")
        
        if trade.price != 0:
            raise Exception('Trade price is set.')
    
    def test_disable_non_zar_premium_currency(self):
        """FValidation should reject non-zar premium currency."""
        usd = ael.Instrument['USD']
        trade = self._create_trade(trd_args = { 'curr': usd })
        
        if trade.trdnbr > 0: # for some reason CreateTrade does not throw exception when validation fails
            raise Exception("Trade was committed.")
    
    def test_sets_deliverydate_for_usdzar(self):
        """FValidation should override delivery date for USD/ZAR options."""
        values = { '2013-11-08': '2013-11-12',  # November 11 - Veteran's day
            '2013-08-30': '2013-09-03', # September 02 - also USA holiday
            '2013-08-08': '2013-08-13', # August 09 - SA holiday
            '2014-09-16': '2014-09-18' } # no holidays
        
        for exp_day, deli_day in values.iteritems():
            ael_trade = self._create_trade(ins_args = { 'exp_day': ael.date(exp_day), 'exp_time': ael.date(exp_day).to_time() })
            acm_trade = acm.FTrade[ael_trade.trdnbr]
            ael.poll() # Important!
            insdec = acm.FOptionDecorator(acm_trade.Instrument(), blgd)
            if ael.date(insdec.DeliveryDate()) != ael.date(deli_day):
                raise Exception("Delivery day test fails for exp day {0}. Expected {1}, got {2}. Insid {3}.".format(exp_day, deli_day, insdec.DeliveryDate(), acm_trade.Instrument().Name()))

def _run_tests():
    import FValidation_UnitTest

    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTradeInsert)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTradeGeneric)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestCallTrade)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestCallInstrument)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestCommTrade)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestDeleteCashFlows)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestMMTrade)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestOptionsWithUnderlyingFixedRates)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTRSIndexRefdInstrumentChange)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAggregationCashPostingLock)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTradesFromPaceFXO)
    #If you want to run the whole test suite, uncomment lines below
    suite = unittest.TestLoader().loadTestsFromModule(FValidation_UnitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    pass

# Patch TradeService users for the sake for unit tests
import FValidation_depr_PaceFXO
if ael.user().userid not in FValidation_PaceFXO.TRADESERVICE_USERS:
    FValidation_PaceFXO.TRADESERVICE_USERS.append(ael.user().userid)

try:
    _run_tests()
finally:
    # Remove the user from TRADESERVICE_USERS.
    FValidation_PaceFXO.TRADESERVICE_USERS.remove(ael.user().userid)




