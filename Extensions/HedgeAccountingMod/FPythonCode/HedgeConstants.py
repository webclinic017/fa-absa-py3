'''
===================================================================================================
PURPOSE: Module to contain all generic constants used in the Hedge Effectiveness Testing Package
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016      FIS Team                Initial implementation
28-08-2018      Jaysen Naicker          Set STR_HYPO_VAL_GROUP = 'AC_GLOBAL' and STR_HYPO_FLOAT_RATE = 'ZAR/Hypo_Spread_3mJibar'
23-10-2020      Qaqamba Ntshobane       Set STR_HYPO_FLOAT_RATE = 'ZAR/Hypo_Prime_NACQ'
===================================================================================================
'''

import acm
import FLogger

LOGGER = FLogger.FLogger(__name__)
EVGetter = acm.GetDefaultContext().GetExtension

# Log Verbosity (1=Normal,2=Debug,3=Warning,4=Error)
LOG_VERBOSITY = 4

# Booleans
BLN_CAN_DEDESIGNATE = False
BLN_MODIFY_TRADES = True
BLN_MODIFY_DATES = True
BLN_MODIFY_SETTINGS = True

# Colours
if acm.FACMServer().ClassName().Text() == 'FTmServer':
    try:
        CLR_WHITE = acm.UX().Colors().Create(255, 255, 255)
        CLR_LIGHT_ORANGE = acm.UX().Colors().Create(255, 177, 100)
        CLR_LIGHT_GRAY = acm.UX().Colors().Create(192, 192, 192)
        CLR_LIGHT_GRAY2 = acm.UX().Colors().Create(224, 224, 224)
        CLR_LIGHT_RED = acm.UX().Colors().Create(255, 128, 128)
        CLR_LIGHT_GREEN = acm.UX().Colors().Create(125, 255, 128)
    except Exception as ex:
        LOGGER.ELOG('Error loading acm.UX components. %s' % ex)

# Dates
DAT_TODAY = acm.Time().DateNow()

# Doubles
# Warnings are default values, but may be overridden in the GUI
DBL_PRO_DO_LO_LIMIT = 0.8
DBL_PRO_DO_LO_WARNING = 0.9
DBL_PRO_DO_HI_LIMIT = 1.25
DBL_PRO_DO_HI_WARNING = 1.1
DBL_PRO_REG_LO_B_LIMIT = -1.25
DBL_PRO_REG_LO_B_WARNING = -1.1
DBL_PRO_REG_HI_B_LIMIT = -0.8
DBL_PRO_REG_HI_B_WARNING = -0.9
DBL_PRO_REG_R2_LIMIT = 0.8
DBL_PRO_REG_R2_WARNING = 0.9
DBL_PRO_REG_P_LIMIT = 0.05
DBL_PRO_REG_P_WARNING = 0.04
DBL_PRO_VRM_LIMIT = 0.8
DBL_PRO_VRM_WARNING = 0.8
DBL_RETRO_DO_LO_LIMIT = 0.8
DBL_RETRO_DO_LO_WARNING = 0.9
DBL_RETRO_DO_HI_LIMIT = 1.25
DBL_RETRO_DO_HI_WARNING = 1.1
DBL_RETRO_VRM_LIMIT = 0.8
DBL_RETRO_VRM_WARNING = 0.9

# Integers
INT_BACKDATE_DAYS = 10000       # Number of permissible days for backdating
INT_LEN_BACKDATE_REASON = 6     # Backdating reasons must be at least this length
INT_DEFAULT_DISTANCE = 100      # Number of days to look back for a substitute price if a mtm price
# is not found on the exact date
INT_DATA_POINTS = 33            # Number of data points used in tests

# Lists
LST_DP_DEFAULT_COLUMNS = ['Trade Instrument', 'Portfolio Theoretical Value', 'Price Theor',
                          'Trade Quantity', 'Trade Price', 'Trade Portfolio', 'Trade Counterparty',
                          'Trade Currency', 'Trade Acquire Day', 'Trade Trader', 'Trade Status',
                          'Portfolio Currency']

LST_HR_TEMPLATE_STATUSES = ['New', 'Final']
LST_REPORT_TYPES = ['Prospective', 'Retrospective']
LST_TEST_TYPES = ['DollarOffset', 'Prospective', 'Retrospective', 'CriticalTerms']

# Strings
STR_ADS_USERNAME = 'ARENASYS'
STR_ASSESS_OF_EFFECT = EVGetter('FExtensionValue', 'FObject', 'AssesmentOfEffectiveness').Value()
STR_CHILD_TRADE_ACQUIRER = 'GROUP TREASURY'
STR_CHILD_TRADE_COUNTERPARTY = 'GROUP TREASURY'
STR_CHILD_TRADE_PORTFOLIO = 'Simulate_GT Hypo Primary'
STR_CHILD_COUNTERPARTY_PORTFOLIO = 'Simulate_GT Hypo Control'
STR_CHILD_TRADE_STATUS = 'FO Confirmed'
STR_CLR_REFERENCE = 'System.Windows.Forms.DataVisualization'
STR_CRITICAL_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'CriticalInformation').Value()
STR_CRITICAL_VALUE = 'Critical Value'
STR_DEALPACKAGE_NAME_PREFIX = 'HR/'
STR_DEALPACKAGE_NAME_SEPERATOR = '/'
STR_DEALPACKAGE_BASENAME_PATTERN = 'HR\/[0-9]{1,9}$'
STR_DEALPACKAGE_FULLNAME_PATTERN = 'HR\/[0-9]{1,9}/[0-9]{1,2}$'
STR_DEAL_SHEET = 'FDealSheet'
STR_DEFAULT_DATE_PATTERN = '^((19|20)\d\d)-([0][1-9]){1}|([1][012]){1}-([012][0-9]){1}|([3][01]){1}$'
STR_DEFAULT_FWD_BUCKETS = 'HE_prospective_dates'
STR_DEFAULT_TIME_BUCKETS = 'HE_historic_dates'
STR_DOLLAR_OFFSET = 'Dollar-Offset'
STR_GLOBAL_DATE_METHOD = ''
STR_GLOBAL_TIMEBUCKET = ''
STR_HEDGE_AUDIT = 'Hedge Effectiveness Audit'
STR_HEDGE_PORTFOLIO = 'Hedge_Child_Trades'
STR_HEDGE_RISK_TYPES = 'Hedge Effectiveness Risk Types'
STR_HEDGE_SUB_TYPES = 'Hedge Effectiveness Hedge Sub Types'
STR_HEDGE_TITLE = 'HedgeEffectiveness'
STR_HEDGE_TEMPLATE = 'Hedge Effectiveness Template Editor'
STR_HEDGE_TEST_SUITE = 'Hedge Effectiveness Test Suite'
STR_HEDGE_TYPES = 'Hedge Effectiveness Hedge Types'
STR_HYPO_VAL_GROUP = 'AC_OIS_ZAR'
STR_HYPO_FLOAT_RATE = 'ZAR/Hypo_Prime_NACQ'
STR_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'HedgeInformation').Value()
STR_HELP_FILE = EVGetter('FExtensionValue', 'FObject', 'HedgeDefaultHelp').Value()

STR_HELP_STRAT_1 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy1').Value()
STR_HELP_STRAT_2 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy2').Value()
STR_HELP_STRAT_3 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy3').Value()
STR_HELP_STRAT_4 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy4').Value()
STR_HELP_STRAT_5 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy5').Value()
STR_HELP_STRAT_6 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy6').Value()
STR_HELP_STRAT_7 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy7').Value()
STR_HELP_STRAT_8 = EVGetter('FExtensionValue', 'FObject', 'HedgeStrategy8').Value()

# Last price market used to store live prices for benchmarks
STR_LAST_PRICE_MARKET = 'SPOT'
STR_MTM_PRICE = 'SPOT_MID'

# Name of MTM market used to store historic prices for benchmarks
STR_MTM_PRICE_MARKET = 'internal'

# Name of market created for HE Testing to store prices for simulations where there is not 
# enough historical prices on a curve for a good representative simulation.
STR_HE_Market = 'HEDGE_TEST'
 
# Specify which price from the MTM price entry: Settle/Bid/Ask
STR_MTM_PRICE_POSITION = 'Settle'
STR_NO_RESULT = 'Test Not Run'
STR_OBJECTIVE_AND_STAT = EVGetter('FExtensionValue', 'FObject', 'ObjectiveAndStrategy').Value()
STR_OVERALLRESULT = 'Overall_Result'
STR_PARENT_CHANGE_REPORT = 'Parent Change Report'
STR_PDO_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'ProDollarOffsetInformation').Value()
STR_PROCVVALUENAME = 'Prospective_Critical Value_Value'
STR_PROCVRESULTNAME = 'Prospective_Critical Value_Result'
STR_PRODOVALUENAME = 'Prospective_Dollar-Offset_Value'
STR_PRODORESULTNAME = 'Prospective_Dollar-Offset_Result'
STR_PROREGVALUENAME = 'Prospective_Regression_Value'
STR_PROREGRESULTNAME = 'Prospective_Regression_Result'
STR_PROREGALPHA = 'Prospective_Regression_alpha'
STR_PROREGBETA = 'Prospective_Regression_beta'
STR_PROREGCORRELATION = 'Prospective_Regression_correlation'
STR_PROREGR2 = 'Prospective_Regression_R2'
STR_PROREGPVALUE = 'Prospective_Regression_p-value'
STR_PROSPECTIVE = 'Prospective'
STR_PROTPOINTBASE = 'Prospective_Point T_'
STR_PROVRMVALUENAME = 'Prospective_Variable Reduction_Value'
STR_PROVRMRESULTNAME = 'Prospective_Variable Reduction_Result'
STR_PROVRMPARCOUPONNAME = 'Prospective_VR_Par_Coupon'
STR_PROXPOINTBASE = 'Prospective_Point X_'
STR_PROYPOINTBASE = 'Prospective_Point Y_'
STR_PVRM_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'ProVRMInformation').Value()
STR_RDO_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'RetroDollarOffsetInformation').Value()
STR_REG_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'RegressionInformation').Value()
STR_REGRESSION = 'Regression'
STR_REPORT_FOLDER = 'c:\reports'
STR_RETDOVALUENAME = 'Retrospective_Dollar-Offset_Value'
STR_RETDORESULTNAME = 'Retrospective_Dollar-Offset_Result'
STR_RETROSPECTIVE = 'Retrospective'
STR_RETTPOINTBASE = 'Retrospective_Point T_'
STR_RETVRMVALUENAME = 'Retrospective_Variable Reduction_Value'
STR_RETVRMRESULTNAME = 'Retrospective_Variable Reduction_Result'
STR_RETVRMPARCOUPONNAME = 'Retrospective_VR_Par_Coupon'
STR_RETXPOINTBASE = 'Retrospective_Point X_'
STR_RETYPOINTBASE = 'Retrospective_Point Y_'
STR_RISK_BEING_HEDGED = EVGetter('FExtensionValue', 'FObject', 'RiskBeingHedge').Value()
STR_RVRM_INFORMATION = EVGetter('FExtensionValue', 'FObject', 'RetroVRMInformation').Value()
STR_SPREAD_BASE_CURVE = 'ZAR-SWAP'
STR_SPREAD_ATTR_CURVE = 'ZAR_Hypo_Prime'
STR_SUPER_USER_PROFILE = 'ALL_COMPONENTS'
STR_TEST_INFORMANTION = EVGetter('FExtensionValue', 'FObject', 'HedgeTestString').Value()
STR_TIMESERIESSPECNAME = 'HedgeResult'
STR_TRADE_SHEET = 'FTradeSheet'
STR_TSTIMESERIESSPECNAME = 'HedgeResultVector'
STR_VARIABLE_REDUCTION = 'Variable Reduction'
STR_XPOINTBASE = 'Point X_'
STR_YPOINTBASE = 'Point Y_'

STR_NumPySciPyLocalLoadPath = r'C:\temp\CommonLib\NumpyAndScipy'
STR_NumPySciPyServerLoadPath = r'\\Intranet.barcapint.com\dfs-emea\Group/Jhb\Arena\CommonLib\2018\binary\64bit\PythonLib27'



def user_components():
    user_profile_dict = {
        Hedge_User_Profiles.FrontOffice: (Hedge_Relation_Status.Simulated,
                                          Hedge_Relation_Status.Proposed),
        Hedge_User_Profiles.Control: tuple(Hedge_Relation_Status.get_all_as_list())
    }

    return user_profile_dict


class Hedge_Trade_Types:
    '''Class that defines and encapsulates the hedge relationship trade types
    '''
    Original = 'Original'
    Internal = 'Internal'
    Hypo = 'Hypo'
    External = 'External'
    ZeroBond = 'Zero Bond'

    @classmethod
    def get_all_as_list(cls):

        hedgeTypeList = []
        hedgeTypeList.append(cls.Original)
        hedgeTypeList.append(cls.Internal)
        hedgeTypeList.append(cls.Hypo)
        hedgeTypeList.append(cls.External)
        hedgeTypeList.append(cls.ZeroBond)

        return hedgeTypeList

    @classmethod
    def test_for_valid_hedge_type(cls, hedge_type_to_test):

        result = False

        if hedge_type_to_test == cls.Original:
            result = True
        elif hedge_type_to_test == cls.Internal:
            result = True
        elif hedge_type_to_test == cls.Hypo:
            result = True
        elif hedge_type_to_test == cls.External:
            result = True
        elif hedge_type_to_test == cls.ZeroBond:
            result = True

        return result


class Hedge_Relation_Status:
    '''Class that defines and encapsulates the hedge relation statuses
    '''
    Simulated = 'Simulated'
    Proposed = 'Proposed'
    Active = 'Active'
    Discard = 'Discard'
    DeDesignated = 'De-Designated'

    @classmethod
    def get_all_as_list(cls):
        _list = []
        _list.append(cls.Simulated)
        _list.append(cls.Proposed)
        _list.append(cls.Active)
        _list.append(cls.Discard)
        _list.append(cls.DeDesignated)

        return _list

    @classmethod
    def get_status_per_simulated(cls):
        _list = []
        _list.append(cls.Simulated)
        _list.append(cls.Proposed)
        _list.append(cls.Discard)

        return _list

    @classmethod
    def get_status_per_proposed(cls):
        _list = []
        _list.append(cls.Simulated)
        _list.append(cls.Proposed)
        _list.append(cls.Active)
        _list.append(cls.Discard)

        return _list

    @classmethod
    def get_status_per_active(cls):
        _list = []
        _list.append(cls.Active)
        _list.append(cls.Proposed)

        return _list

    @classmethod
    def get_status_per_deDesignated(cls):
        _list = []
        _list.append(cls.DeDesignated)

        return _list

    @classmethod
    def get_status_per_discard(cls):
        _list = []
        _list.append(cls.Discard)

        return _list


class Hedge_User_Profiles:
    '''Class that defines and encapsulates the hedge user profiles
    '''
    FrontOffice = 'HedgeEffFO'
    Control = 'HedgeEffControl'

    @classmethod
    def get_all_as_list(cls):
        _list = []
        _list.append(cls.FrontOffice)
        _list.append(cls.Control)

        return _list


class DedesignationReason:
    '''Class that defines and encapsulates the hedge de-designation reasons
    '''

    ExernalExpired = 'External Expired'
    ExternalSold = 'External Sold'
    ExternalTerminated = 'External Terminated'
    Ineffective = 'Ineffective'
    OriginalExpired = 'Original Expired'
    OriginalSold = 'Original Sold'
    OriginalTerminated = 'Original Terminated'
    PartialDedesignation = 'Partial de-designation'
    ReBalanced = 'Re-balanced'
    Voluntary = 'Voluntary'

    @classmethod
    def get_all_as_list(cls):
        _list = []
        _list.append(cls.ExernalExpired)
        _list.append(cls.ExternalTerminated)
        _list.append(cls.ExternalSold)
        _list.append(cls.Ineffective)
        _list.append(cls.OriginalExpired)
        _list.append(cls.OriginalSold)
        _list.append(cls.OriginalTerminated)
        _list.append(cls.PartialDedesignation)
        _list.append(cls.ReBalanced)
        _list.append(cls.Voluntary)

        return _list

