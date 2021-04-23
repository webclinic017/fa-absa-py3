""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/test/cunit/test_FIPFCalculations.py"
"""
#owner:Prime-OMS
#email:FrontArena.ProductSolutions.Dev@fisglobal.com
#AMF #WSOBankDebt
"""

import unittest

from FWSOUnitTests import MockImporter

if MockImporter.IsAvailable():
    import mock


class Mocks(object):
    
    CONTRACTS_DICT_MOCK = {
        '23456': {
            'Contract_ID': '23456',
            'Contract_Facility_ID': '123',
        },
        '23457': {
            'Contract_ID': '23457',
            'Contract_Facility_ID': '123',
        },
        '23458': {
            'Contract_ID': '23458',
            'Contract_Facility_ID': '124',
        }
    }

    CONTRACT_DETAILS_DICT_MOCK = {
        '567': {
            'ContractIPF_ID': '567',
            'Contract_ID': '23456',
            'ContractIPF_DateFrom': '2014-11-22T00:00:00+00:00',
            'ContractIPF_DateTo': '2015-01-22T00:00:00+00:00',
            'ContractIPF_Amount': '1000.0',
        },
        '568': {
            'ContractIPF_ID': '568',
            'Contract_ID': '23456',
            'ContractIPF_DateFrom': '2015-01-22T00:00:00+00:00',
            'ContractIPF_DateTo': '2015-02-23T00:00:00+00:00',
            'ContractIPF_Amount': '3000.0',
        }
    }

    CONTRACTID_CONTRACTDETAILS_SUBDICTS = {
        '47354': {
            '65311': {
                'Contract_Name': '', 
                'EndDateInRange': '2015-02-18T00:00:00+00:00', 'Contract_CurrencyType_ID': '1', 'Contract_MaturityDate': '2015-03-31T00:00:00+01:00', 'EarnedInterest': '3521.4769', 'ContractIPF_Account_ID': '9354', 'ContractIPF_ContractIPFrac': '', 'EarnedInterestFXConvRC': '3521.4769', 'ContractIP_ReceiveDate': '2015-03-31T00:00:00+01:00', 
                'ContractIPF_ID_4': {'ContractIPF_DateFrom': '2015-01-30', 'ContractIPF_DateTo': '2015-02-27'}, 'EarnedFeesRC': '0.0000', 
                'ContractIPF_ID_2': {'ContractIPF_DateFrom': '2015-01-20', 'ContractIPF_DateTo': '2015-01-21'}, 'EarnedInterestRC': '3521.4769', 
                'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2014-12-31', 'ContractIPF_DateTo': '2015-01-20'}, 'DaysInRange': '50', 'ContractIP_ID': '48827', 'Contract_ID': '47354', 'ContractIPF_DateFrom': '2014-12-31T00:00:00+00:00', 'ContractIPF_ID': '65311', 'ContractIPF_AllInRate': '0.0425', 'Contract_Frequency': '4', 'Position_ID': '9354', 'ContractTypeDescription': 'Term Funded', 'ContractIPF_Notes': '', 'ContractIPF_LastChangeID': 'nilnil', 'ContractIPF_Facility_ID': '1472', 'ContractIPF_Interest': '6338.6584', 'ContractIPF_BankDeal_ID': '252', 'YearCountName': '360', 'ContractIPF_LastChangeDate': '2014-12-30T15:38:44.083+00:00', 'ContractIPF_YearCount_ID': '2', 'ContractIPF_MonthCount_ID': '1', 'ContractIPF_CauseCode': '917804', 'Contract_FacilityOption_ID': '9192', 'EarnedInterestFXGainRC': '0.0000', 'ContractIPF_GlobalAmount': '374999999.9999', 'ContractIPF_AddID': 'nilnil', 'ContractIPF_DateTo': '2015-03-31T00:00:00+01:00', 'ContractIP_Received': '0', 'ContractIPF_AddDate': '2014-12-30T15:38:44.083+00:00', 'ContractIPF_Spread': '0.0325', 'Contract_FacilityOption_Name': 'LIBOR', 'ContractIPF_Issuer_ID': '236', 'ContractIPF_Cause_ID': '181492', 'ContractIPF_Portfolio_ID': '225', 'ContractIPF_ContractIP_ID': '48827', 'EarnedFeesFXConvRC': '0.0000', 'MonthCountName': 'ACT', 'Position_StopAccrualEndDate': '9999-09-09T00:00:00+01:00', 'EarnedFees': '0.0000', 'Contract_StartDate': '2014-12-31T00:00:00+00:00', 'EarnedFeesFXGainRC': '0.0000', 'ContractBehaviorDescription': 'LIBOR', 
                'ContractIPF_ID_5': {'ContractIPF_DateFrom': '2015-02-27', 'ContractIPF_DateTo': '2015-03-31'}, 'StartDateInRange': '2014-12-31T00:00:00+00:00', 'ContractIPF_Amount': '596579.6149', 'ContractIPF_BaseRate': '0.01', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1', 
                'ContractIPF_ID_3': {'ContractIPF_DateFrom': '2015-01-21', 'ContractIPF_DateTo': '2015-01-30'}}}, 
        '47608': {
            '65738': {'Contract_Name': '', 'EndDateInRange': '2015-02-18T00:00:00+00:00', 'Contract_CurrencyType_ID': '1', 'Contract_MaturityDate': '2015-03-31T00:00:00+01:00', 'EarnedInterest': '10238.0716', 'ContractIPF_Account_ID': '9353', 'ContractIPF_ContractIPFrac': '', 'EarnedInterestFXConvRC': '10238.0716', 'ContractIP_ReceiveDate': '2015-03-31T00:00:00+01:00', 'EarnedFeesRC': '0.0000', 
                'ContractIPF_ID_2': {'ContractIPF_DateFrom': '2015-01-30', 'ContractIPF_DateTo': '2015-02-27'}, 'EarnedInterestRC': '10238.0716', 
                'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2015-01-21', 'ContractIPF_DateTo': '2015-01-30'}, 'DaysInRange': '29', 'ContractIP_ID': '49108', 'Contract_ID': '47608', 'ContractIPF_DateFrom': '2015-01-21T00:00:00+00:00', 'ContractIPF_ID': '65738', 'ContractIPF_AllInRate': '0.0425', 'Contract_Frequency': '4', 'Position_ID': '9353', 'ContractTypeDescription': 'Term Funded', 'ContractIPF_Notes': '', 'ContractIPF_LastChangeID': 'nilnil', 'ContractIPF_Facility_ID': '1472', 'ContractIPF_Interest': '24359.5496', 'ContractIPF_BankDeal_ID': '252', 'YearCountName': '360', 'ContractIPF_LastChangeDate': '2015-01-20T08:11:56.797+00:00', 'ContractIPF_YearCount_ID': '2', 'ContractIPF_MonthCount_ID': '1', 'ContractIPF_CauseCode': '914904', 'Contract_FacilityOption_ID': '9192', 'EarnedInterestFXGainRC': '0.0000', 'ContractIPF_GlobalAmount': '374999999.9999', 'ContractIPF_AddID': 'nilnil', 'ContractIPF_DateTo': '2015-03-31T00:00:00+01:00', 'ContractIP_Received': '0', 'ContractIPF_AddDate': '2015-01-20T08:11:56.797+00:00', 'ContractIPF_Spread': '0.0325', 'Contract_FacilityOption_Name': 'LIBOR', 'ContractIPF_Issuer_ID': '236', 'ContractIPF_Cause_ID': '182723', 'ContractIPF_Portfolio_ID': '208', 'ContractIPF_ContractIP_ID': '49108', 'EarnedFeesFXConvRC': '0.0000', 'MonthCountName': 'ACT', 'Position_StopAccrualEndDate': '9999-09-09T00:00:00+01:00', 'EarnedFees': '0.0000', 'Contract_StartDate': '2015-01-20T00:00:00+00:00', 'EarnedFeesFXGainRC': '0.0000', 'ContractBehaviorDescription': 'LIBOR', 'StartDateInRange': '2015-01-21T00:00:00+00:00', 'ContractIPF_Amount': '2990430.6451', 'ContractIPF_BaseRate': '0.01', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1', 
                'ContractIPF_ID_3': {'ContractIPF_DateFrom': '2015-02-27', 'ContractIPF_DateTo': '2015-03-31'}}, 
            '65734': {'Contract_Name': '', 'EndDateInRange': '2015-01-20T00:00:00+00:00', 'Contract_CurrencyType_ID': '1', 'Contract_MaturityDate': '2015-03-31T00:00:00+01:00', 'EarnedInterest': '117.6790', 'ContractIPF_Account_ID': '9353', 'ContractIPF_ContractIPFrac': '', 'EarnedInterestFXConvRC': '117.6790', 'ContractIP_ReceiveDate': '2015-03-31T00:00:00+01:00', 'EarnedFeesRC': '0.0000', 'EarnedInterestRC': '117.6790', 
                'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2015-01-20', 'ContractIPF_DateTo': '2015-01-21'}, 'DaysInRange': '1', 'ContractIP_ID': '49108', 'Contract_ID': '47608', 'ContractIPF_DateFrom': '2015-01-20T00:00:00+00:00', 'ContractIPF_ID': '65734', 'ContractIPF_AllInRate': '0.0425', 'Contract_Frequency': '4', 'Position_ID': '9353', 'ContractTypeDescription': 'Term Funded', 'ContractIPF_Notes': '', 'ContractIPF_LastChangeID': 'nilnil', 'ContractIPF_Facility_ID': '1472', 'ContractIPF_Interest': '117.6790', 'ContractIPF_BankDeal_ID': '252', 'YearCountName': '360', 'ContractIPF_LastChangeDate': '2015-01-20T08:11:43.6+00:00', 'ContractIPF_YearCount_ID': '2', 'ContractIPF_MonthCount_ID': '1', 'ContractIPF_CauseCode': '914904', 'Contract_FacilityOption_ID': '9192', 'EarnedInterestFXGainRC': '0.0000', 'ContractIPF_GlobalAmount': '374999999.9999', 'ContractIPF_AddID': 'nilnil', 'ContractIPF_DateTo': '2015-01-21T00:00:00+00:00', 'ContractIP_Received': '0', 'ContractIPF_AddDate': '2015-01-20T07:44:06.697+00:00', 'ContractIPF_Spread': '0.0325', 'Contract_FacilityOption_Name': 'LIBOR', 'ContractIPF_Issuer_ID': '236', 'ContractIPF_Cause_ID': '182721', 'ContractIPF_Portfolio_ID': '208', 'ContractIPF_ContractIP_ID': '49108', 'EarnedFeesFXConvRC': '0.0000', 'MonthCountName': 'ACT', 'Position_StopAccrualEndDate': '9999-09-09T00:00:00+01:00', 'EarnedFees': '0.0000', 'Contract_StartDate': '2015-01-20T00:00:00+00:00', 'EarnedFeesFXGainRC': '0.0000', 'ContractBehaviorDescription': 'LIBOR', 'StartDateInRange': '2015-01-20T00:00:00+00:00', 'ContractIPF_Amount': '996810.2157', 'ContractIPF_BaseRate': '0.01', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1'}}, '47678': {'65840': {'Contract_Name': '', 'EndDateInRange': '2015-02-18T00:00:00+00:00', 'Contract_CurrencyType_ID': '1', 'Contract_MaturityDate': '2015-02-27T00:00:00+00:00', 'EarnedInterest': '5639.0583', 'ContractIPF_Account_ID': '9354', 'ContractIPF_ContractIPFrac': '', 'EarnedInterestFXConvRC': '5639.0583', 'ContractIP_ReceiveDate': '2015-02-27T00:00:00+00:00', 'EarnedFeesRC': '0.0000', 'EarnedInterestRC': '5639.0583', 
                'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2015-01-30', 'ContractIPF_DateTo': '2015-02-27'}, 'DaysInRange': '20', 'ContractIP_ID': '49178', 'Contract_ID': '47678', 'ContractIPF_DateFrom': '2015-01-30T00:00:00+00:00', 'ContractIPF_ID': '65840', 'ContractIPF_AllInRate': '0.0425', 'Contract_Frequency': '12', 'Position_ID': '9354', 'ContractTypeDescription': 'Term Funded', 'ContractIPF_Notes': '', 'ContractIPF_LastChangeID': 'nilnil', 'ContractIPF_Facility_ID': '1472', 'ContractIPF_Interest': '7894.6816', 'ContractIPF_BankDeal_ID': '252', 'YearCountName': '360', 'ContractIPF_LastChangeDate': '2015-01-29T11:21:43.533+00:00', 'ContractIPF_YearCount_ID': '2', 'ContractIPF_MonthCount_ID': '1', 'ContractIPF_CauseCode': '917804', 'Contract_FacilityOption_ID': '9192', 'EarnedInterestFXGainRC': '0.0000', 'ContractIPF_GlobalAmount': '1501250000.0003', 'ContractIPF_AddID': 'nilnil', 'ContractIPF_DateTo': '2015-02-27T00:00:00+00:00', 'ContractIP_Received': '0', 'ContractIPF_AddDate': '2015-01-29T11:21:43.533+00:00', 'ContractIPF_Spread': '0.0325', 'Contract_FacilityOption_Name': 'LIBOR', 'ContractIPF_Issuer_ID': '236', 'ContractIPF_Cause_ID': '183481', 'ContractIPF_Portfolio_ID': '225', 'ContractIPF_ContractIP_ID': '49178', 'EarnedFeesFXConvRC': '0.0000', 'MonthCountName': 'ACT', 'Position_StopAccrualEndDate': '9999-09-09T00:00:00+01:00', 'EarnedFees': '0.0000', 'Contract_StartDate': '2015-01-30T00:00:00+00:00', 'EarnedFeesFXGainRC': '0.0000', 'ContractBehaviorDescription': 'LIBOR', 'StartDateInRange': '2015-01-30T00:00:00+00:00', 'ContractIPF_Amount': '2388307.0350', 'ContractIPF_BaseRate': '0.01', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1'}}, '47679': {'65841': {'Contract_Name': '', 'EndDateInRange': '2015-02-18T00:00:00+00:00', 'Contract_CurrencyType_ID': '1', 'Contract_MaturityDate': '2015-02-27T00:00:00+00:00', 'EarnedInterest': '28266.4916', 'ContractIPF_Account_ID': '9353', 'ContractIPF_ContractIPFrac': '', 'EarnedInterestFXConvRC': '28266.4916', 'ContractIP_ReceiveDate': '2015-02-27T00:00:00+00:00', 'EarnedFeesRC': '0.0000', 'EarnedInterestRC': '28266.4916', 
                'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2015-01-30', 'ContractIPF_DateTo': '2015-02-27'}, 'DaysInRange': '20', 'ContractIP_ID': '49179', 'Contract_ID': '47679', 'ContractIPF_DateFrom': '2015-01-30T00:00:00+00:00', 'ContractIPF_ID': '65841', 'ContractIPF_AllInRate': '0.0425', 'Contract_Frequency': '12', 'Position_ID': '9353', 'ContractTypeDescription': 'Term Funded', 'ContractIPF_Notes': '', 'ContractIPF_LastChangeID': 'nilnil', 'ContractIPF_Facility_ID': '1472', 'ContractIPF_Interest': '39573.0883', 'ContractIPF_BankDeal_ID': '252', 'YearCountName': '360', 'ContractIPF_LastChangeDate': '2015-01-29T11:21:43.73+00:00', 'ContractIPF_YearCount_ID': '2', 'ContractIPF_MonthCount_ID': '1', 'ContractIPF_CauseCode': '917804', 'Contract_FacilityOption_ID': '9192', 'EarnedInterestFXGainRC': '0.0000', 'ContractIPF_GlobalAmount': '1501250000.0003', 'ContractIPF_AddID': 'nilnil', 'ContractIPF_DateTo': '2015-02-27T00:00:00+00:00', 'ContractIP_Received': '0', 'ContractIPF_AddDate': '2015-01-29T11:21:43.73+00:00', 'ContractIPF_Spread': '0.0325', 'Contract_FacilityOption_Name': 'LIBOR', 'ContractIPF_Issuer_ID': '236', 'ContractIPF_Cause_ID': '183482', 'ContractIPF_Portfolio_ID': '208', 'ContractIPF_ContractIP_ID': '49179', 'EarnedFeesFXConvRC': '0.0000', 'MonthCountName': 'ACT', 'Position_StopAccrualEndDate': '9999-09-09T00:00:00+01:00', 'EarnedFees': '0.0000', 'Contract_StartDate': '2015-01-30T00:00:00+00:00', 'EarnedFeesFXGainRC': '0.0000', 'ContractBehaviorDescription': 'LIBOR', 'StartDateInRange': '2015-01-30T00:00:00+00:00', 'ContractIPF_Amount': '11971690.5649', 'ContractIPF_BaseRate': '0.01', 'ContractType': '38', 'Contract_FacilityOption_Behavior': '1'}
        }
    }

    IPF_SUB_DICT = {
        'ContractIPF_DateFrom': '2015-01-30', 
        'ContractIPF_DateTo': '2015-02-27'
    }
    
    def ContractDetailDict(self):
        return self.ContractDetailsDict().get('567')
    
    def ContractDetailsDict(self):
        return self.CONTRACT_DETAILS_DICT_MOCK
    
    def Contract(self):
        return self.CONTRACTS_DICT_MOCK
    
    def ContractId(self):
        return '47608'
    
    def ContractIdContractDetailsSubDicts(self):
        return self.CONTRACTID_CONTRACTDETAILS_SUBDICTS
    
    def ContractDetailId(self):
        return '65738'
        
    def IpfSubDict(self):
        return self.IPF_SUB_DICT
        
    def IpfSubId(self):
        return 'ContractIPF_ID_2'


class Patches(object):

    mocks = Mocks()
    
    def ContractsDict(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.Contract', return_value=self.mocks.Contract())
    
    def ContractDetailsDict(self):
        return mock.patch('FWSODictAccessor.WSODictAccessor.ContractDetail', return_value=self.mocks.ContractDetailsDict())
    

class TestContractDetail(unittest.TestCase):

    mocks = Mocks()
    patch = Patches()
        
    def setUp(self):
        from FWSOIPFCalculations import ContractDetail
        self.contractDetail = ContractDetail(self.mocks.ContractDetailDict())

    def test_ConstructIPFSubPeriodDictionaryFromOriginalContractDetailDict(self):
        ipfSubDict = self.contractDetail.ConstructIPFSubPeriodDictionaryFromOriginalContractDetailDict('2014-11-22', '2015-01-22')
        self.assertEqual(ipfSubDict['ContractIPF_DateFrom'], '2014-11-22')
        self.assertEqual(ipfSubDict['ContractIPF_DateTo'], '2015-01-22')

    def test_ConstructIPFSubPeriodDictionaries(self):
        contractDetailPrefix = 'ContractIPF_ID_'
        ipfSubPeriodDictExpected = {'ContractIPF_ID_1': {'ContractIPF_DateFrom': '2014-11-22', 'ContractIPF_DateTo': '2015-01-22'}}
        ipfPeriods = [['2014-11-22', '2015-01-22'], ['2015-01-22', '2015-02-23']]
        ipfSubPeriodDict = self.contractDetail.ConstructIPFSubPeriodDictionaries(contractDetailPrefix, ipfPeriods)
        self.assertEqual(ipfSubPeriodDict, ipfSubPeriodDictExpected)

    def test_AddContractAmountForIPFPeriod(self):
        contractAmountForPeriodExpected = 1000.0
        ipfSubDict = {
            'ContractIPF_DateFrom': '2014-11-22', 
            'ContractIPF_DateTo': '2015-01-22',
        }
        from FWSOIPFCalculations import ContractDetail
        ipfSub = ContractDetail(ipfSubDict)
        contractAmountForPeriod = ipfSub.AddContractAmountForIPFPeriod(self.mocks.ContractDetailsDict())
        self.assertEqual(contractAmountForPeriod, contractAmountForPeriodExpected)
        

class TestIPFNominalCalculatorRealIPFs(unittest.TestCase):

    mocks = Mocks()

    def setUp(self):
        from FWSOIPFCalculations import WSOIPFCalculations
        self.calculator = WSOIPFCalculations()
        
    def test_ComputeIPFNominalFactor(self):
        ipfNominalFactorExpected = 0.166625582852
        ipfNominalFactor = self.calculator.ComputeIPFNominalFactor(self.mocks.ContractId(), self.mocks.ContractDetailId(), self.mocks.IpfSubId(), self.mocks.IpfSubDict(), self.mocks.ContractIdContractDetailsSubDicts())
        self.assertAlmostEqual(ipfNominalFactor, ipfNominalFactorExpected)

    def test_ComputeGlobalIPFNominalAmountForPeriod(self):
        totalContractDetailIPFAmountExpected = 17947007.8599
        totalContractDetailIPFAmount = self.calculator._ComputeGlobalIPFNominalAmountForPeriod(self.mocks.ContractId(), self.mocks.ContractDetailId(), self.mocks.IpfSubId(), self.mocks.IpfSubDict(), self.mocks.ContractIdContractDetailsSubDicts())
        self.assertAlmostEqual(totalContractDetailIPFAmount, totalContractDetailIPFAmountExpected)


'''
testClassesToRun = [TestIPFCalculations, TestIPFNominalCalculator, TestIPFNominalCalculatorRealIPFs]
testSuite = unittest.TestSuite()
for testClass in testClassesToRun:
    testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testClass))

runner = unittest.TextTestRunner()
runner.run(testSuite)
'''
