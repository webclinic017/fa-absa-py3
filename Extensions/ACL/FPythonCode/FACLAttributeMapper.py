""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLAttributeMapper.py"
from __future__ import print_function
import sys
import acm
import FACLMapping
import FOperationsUtils as Utils
from FACLParameters import PartyMapping, CustomerBranchMapping, InternalDepartmentMapping
from numbers import Number

context = acm.GetDefaultContext()

insTypeAttributesMap = {FACLMapping.BASIS_SWAP: 'FACLBasisSwapAttributes',
                        FACLMapping.BOND_OPTION: 'FACLBondOptionAttributes',
                        FACLMapping.BOND_FORWARD: 'FACLBondForwardAttributes',
                        FACLMapping.BOND_SPOT: 'FACLBondSpotAttributes',
                        FACLMapping.BOND_REPO: 'FACLBondRepoAttributes',
                        FACLMapping.CAP: 'FACLCapAttributes',
                        FACLMapping.CREDIT_DEFAULT_SWAP: 'FACLCreditDefaultSwapAttributes',
                        FACLMapping.CURRENCY_SWAP: 'FACLCurrencySwapAttributes',
                        FACLMapping.EQUITY_OPTION: 'FACLEquityOptionAttributes',
                        FACLMapping.EQUITY_FORWARD: 'FACLEquityForwardAttributes',
                        FACLMapping.EQUITY_SPOT: 'FACLEquitySpotAttributes',
                        FACLMapping.EQUITY_SWAP: 'FACLEquitySwapAttributes',
                        FACLMapping.EQUITY_REPO: 'FACLEquityRepoAttributes',
                        FACLMapping.FRA: 'FACLFRAAttributes',
                        FACLMapping.FLOOR: 'FACLFloorAttributes',
                        FACLMapping.FX_BARRIER_OPTION: 'FACLFXBarrierOptionAttributes',
                        FACLMapping.FX_BINARY_OPTION: 'FACLFXBinaryOptionAttributes',
                        FACLMapping.FX_FORWARD: 'FACLFXForwardAttributes',
                        FACLMapping.FX_OPTION: 'FACLFXOptionAttributes',
                        FACLMapping.FX_CASH: 'FACLFXSpotAttributes',
                        FACLMapping.FX_SWAP: 'FACLFXSwapAttributes',
                        FACLMapping.INTEREST_DERIVATIVE: 'FACLInterestDerivativeAttributes',
                        FACLMapping.SWAP: 'FACLInterestRateSwapAttributes',
                        FACLMapping.MM_LOAN_DEPOSIT: 'FACLMMLoanDepositAttributes',
                        FACLMapping.DEMAND_LOAN_DEPOSIT: 'FACLDemandLoanDepositAttributes',
                        FACLMapping.BOND_DERIVATIVE: 'FACLOtherBondDerivativeAttributes',
                        FACLMapping.EQUITY_DERIVATIVE: 'FACLOtherEquityDerivativeAttributes',
                        FACLMapping.FX_DERIVATIVE: 'FACLOtherFXDerivativeAttributes',
                        FACLMapping.OVERNIGHT_INDEX_SWAP: 'FACLOvernightIndexSwapAttributes',
                        FACLMapping.ODF: 'FACLFXForwardAttributes',
                        FACLMapping.SECURITIES_BORROW_LEND: 'FACLSecuritiesBorrowLendAttributes',
                        FACLMapping.SWAPTION: 'FACLSwaptionAttributes',
                        FACLMapping.TOTAL_RETURN_SWAP: 'FACLTotalReturnSwapAttributes',
                        FACLMapping.UNKNOWN: 'FACLAllAttributes',
                        }


class FACLAllAttributes(object):
    
    def __init__(self, sheet, bType):
        self.columns = [column for column in
                        context.GetAllExtensions(
                        'FColumnDefinition', sheet,
                        True, True, 'acl', bType)]

    def Columns(self):
        return self.columns

    def ColumnValue(self, name):
        return None

class FACLTradeAttributesBase(object):

    MANDATORY_COLUMN_NAMES = []

    def __init__(self):
        self.columns = [context.GetExtension('FColumnDefinition',
                        'FTradeSheet', columnName).Value()
                        for columnName in
                        self.__class__.MANDATORY_COLUMN_NAMES]

    def Columns(self):
        return self.columns

    def ColumnValue(self, name):
        return None


class FACLFXSpotAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Sell Amount',
                            'FACL Booking Branch',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Exchange Rate',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Buy Amount',
                            'FACL Settlement Date',
                            'FACL Sell Currency',
                            'FACL Buy Currency']


class FACLDemandLoanDepositAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Notice Term (Days)',
                            'FACL Dealer ID',
                            'FACL Loan or Deposit',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Effective Date',
                            'FACL Amortisation']

    def ColumnValue(self, name):
        if 'Notice Term (Days)' in name: 
            return '0'
        return None


class FACLBondSpotAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Trade Date',
                            'FACL Bond Notional',
                            'FACL Settlement Date',
                            'FACL Deal Price',
                            'FACL Security',
                            'FACL Amortisation']

class FACLBondOptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Deferred Premium',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Strike Price',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Bond Notional',
                            'FACL Option Type',
                            'FACL Premium Payment Date',
                            'FACL Expiry Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date',
                            'FACL Security']

class FACLBondForwardAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Bond Notional',
                            'FACL Deal Price',
                            'FACL Settlement Date',
                            'FACL Security']

class FACLBondRepoAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Reference',
                            'FACL Booking Branch',
                            'FACL Clearing Type',
                            'FACL Maturity Date',
                            'FACL Underlying Bond',
                            'FACL Bond Maturity Date',
                            'FACL Repo/Reverse',
                            'FACL Cash Amount',
                            'FACL Counterparty',
                            'FACL Cash Currency',
                            'FACL Dealer ID',
                            'FACL Collateral Amount',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Collateral Currency',
                            'FACL Amortisation']


class FACLCapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Principal',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Buy Sell',
                            'FACL Payment Interval',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Cap Rate',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Premium Payment Date',
                            'FACL Premium Currency',
                            'FACL Amortisation']


class FACLInterestRateSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Pay Rate Type',
                            'FACL Booking Branch',
                            'FACL Principal',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Swap Rate',
                            'FACL Amortisation']


class FACLCreditDefaultSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Trade Date',
                            'FACL Notional Amount',
                            'FACL Underlying',
                            'FACL Amortisation']


class FACLCurrencySwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Pay Rate Type',
                            'FACL Booking Branch',
                            'FACL Clearing Type',
                            'FACL Receive Currency',
                            'FACL Pay Currency',
                            'FACL Counterparty',
                            'FACL Principal Exchange',
                            'FACL Dealer ID',
                            'FACL Receive Principal',
                            'FACL Pay Principal',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Amortisation']


class FACLSwaptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Principal',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Settlement Style',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Swap Maturity Date',
                            'FACL Product',
                            'FACL Option Expiry Date',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Payer Receiver',
                            'FACL Premium Payment Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date',
                            'FACL Swap Rate',
                            'FACL Amortisation']

class FACLEquityOptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Option Style',
                            'FACL Strike Price',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Equity',
                            'FACL Option Type',
                            'FACL Units',
                            'FACL Premium Payment Date',
                            'FACL Expiry Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date']


class FACLFXOptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Option Style',
                            'FACL Strike Price',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Underlying Amount',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Underlying Currency',
                            'FACL Option Type',
                            'FACL Premium Payment Date',
                            'FACL Expiry Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date']
    def ColumnValue(self, name):
        if 'Premium Amount' in name:
            return '0'
        return None

class FACLFXBinaryOptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Cash Payoff',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Payoff Currency',
                            'FACL Counterparty',
                            'FACL Strike Price',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Underlying Currency',
                            'FACL Option Type',
                            'FACL Premium Payment Date',
                            'FACL Expiry Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date']


class FACLFXBarrierOptionAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Option Style',
                            'FACL Strike Price',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Underlying Amount',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Underlying Currency',
                            'FACL Option Type',
                            'FACL Premium Payment Date',
                            'FACL Expiry Date',
                            'FACL Premium Currency',
                            'FACL Settlement Date']


class FACLFXForwardAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Sell Amount',
                            'FACL Booking Branch',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Exchange Rate',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Buy Amount',
                            'FACL Settlement Date',
                            'FACL Sell Currency',
                            'FACL Buy Currency']


class FACLFXSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Booking Branch',
                            'FACL Clearing Type',
                            'FACL Near Buy Amount',
                            'FACL Far Sell Amount',
                            'FACL Counterparty',
                            'FACL Reference',
                            'FACL Near Settlement Date',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Far Side Exchange Rate',
                            'FACL Trade Date',
                            'FACL Near Buy/Far Sell Currency',
                            'FACL Far Settlement Date',
                            'FACL Near Sell Amount',
                            'FACL Far Buy Amount',
                            'FACL Near Side Exchange Rate',
                            'FACL Near Sell/Far Buy Currency']


class FACLFRAAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Principal',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Settlement Date',
                            'FACL Borrower Lender',
                            'FACL Amortisation']


class FACLFloorAttributes(FACLTradeAttributesBase):
    MANDATORY_COLUMN_NAMES = ['FACL Deferred Premium',
                            'FACL Reference',
                            'FACL Maturity Date',
                            'FACL Floor Rate',
                            'FACL Principal',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Buy Sell',
                            'FACL Payment Interval',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Premium Amount',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Premium Payment Date',
                            'FACL Premium Currency',
                            'FACL Amortisation']


class FACLEquityForwardAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Booking Branch',
                            'FACL Reference',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Trade Date',
                            'FACL Equity',
                            'FACL Units',
                            'FACL Settlement Date',
                            'FACL Deal Price']


class FACLEquitySpotAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Booking Branch',
                            'FACL Reference',
                            'FACL Currency',
                            'FACL Clearing Type',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Trade Date',
                            'FACL Equity',
                            'FACL Units',
                            'FACL Settlement Date',
                            'FACL Deal Price']


class FACLEquitySwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Counterparty',
                            'FACL Swap Type',
                            'FACL Pay/Receive Equity 1',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL IR/Equity 2 Currency',
                            'FACL IR/Equity 2 Principal']


class FACLEquityRepoAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Repo/Reverse',
                            'FACL Cash Amount',
                            'FACL Counterparty',
                            'FACL Cash Currency',
                            'FACL Dealer ID',
                            'FACL Collateral Amount',
                            'FACL Product',
                            'FACL Trade Date',
                            'FACL Collateral Currency',
                            'FACL Amortisation']


class FACLMMLoanDepositAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Amount',
                            'FACL Reference',
                            'FACL Maturity Date',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Rollover',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Loan or Deposit',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Effective Date',
                            'FACL Amortisation']


class FACLSecuritiesBorrowLendAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Cash Amount',
                            'FACL Counterparty',
                            'FACL Cash Currency',
                            'FACL Dealer ID',
                            'FACL Collateral Amount',
                            'FACL Underlying Security',
                            'FACL Lend/Borrow',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Collateral Currency',
                            'FACL Amortisation']


class FACLTotalReturnSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Book',
                            'FACL Buy Sell',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Notional Amount',
                            'FACL Underlying',
                            'FACL Initial Price',
                            'FACL Amortisation']


class FACLBasisSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Pay Rate Type',
                            'FACL Principal',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Amortisation']


class FACLOvernightIndexSwapAttributes(FACLTradeAttributesBase):

    MANDATORY_COLUMN_NAMES = ['FACL Maturity Date',
                            'FACL Reference',
                            'FACL Pay Rate Type',
                            'FACL Principal',
                            'FACL Booking Branch',
                            'FACL Currency',
                            'FACL Counterparty',
                            'FACL Dealer ID',
                            'FACL Product',
                            'FACL Replacement Value',
                            'FACL Trade Date',
                            'FACL Amortisation']


class FACLAttributeMapper:

    def MapAttributes(self, businessObject):
        if businessObject.IsKindOf(acm.FTrade):
            calculationSpaceTradeSheet = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
            return self._DoMapAttributes(businessObject, 'trade', 'FTradeSheet', calculationSpaceTradeSheet)
        elif businessObject.IsKindOf(acm.FInstrument):
            calculationSpaceDealSheet = acm.Calculations().CreateCalculationSpace(context, 'FDealSheet')
            return self._DoMapAttributes(businessObject, 'security', 'FDealSheet', calculationSpaceDealSheet)
        elif businessObject.IsKindOf(acm.FParty):
            return self._DoMapCpy(businessObject, businessObject.FACLgetMappingProperties())
        else:
            return None
    
    def _DoMapCpy(self, cpy, map):
        dictonary = {}

        for key in map.Keys():
            methodName = map[key]
            value = callMethodByName(cpy, methodName)
            dictonary[key] = value if value else ''
            
        return dictonary

    def _DoMapAttributes(self, businessObject, bType, sheet, calculationSpace):
        attributeDict = {}
        attributeCls = None
        if businessObject.IsKindOf(acm.FInstrument):
            attributeCls = FACLAllAttributes(sheet, bType)
        else:
            insType = FACLMapping.getFACLProduct(businessObject)
            try:
                attributeCls = getattr(sys.modules[__name__],
                                insTypeAttributesMap[insType])()
            except:
                attributeCls = FACLAllAttributes(sheet, bType)

        columns = attributeCls.Columns()
        for column in columns:
            columnId = str(column.Name())
            calculatedValue = calculationSpace.CalculateValue(businessObject, columnId)
            columnName = str(column.At('Name'))

            hint = str(column.At('Description'))
            value = self._UnpackValue(calculatedValue, hint)
            if value:
                attributeDict[columnName] = value
                Utils.LogVerbose('%s set to %s' % (columnId, value))
            elif bType == 'trade':
                if hint == 'amortisation':
                    attributeDict[columnName] = ''
                elif columnName not in attributeDict:
                    value = attributeCls.ColumnValue(columnName)
                    if value:
                        attributeDict[columnName] = value
        return attributeDict

    def _HandleReplacementValue(self, v):
        return {'SingleValue': str(v[0]), 'AssetCode' : str(v[1]), 'CalculatedDate' : str(v[2])}

    def _HandleAmortisation(self, amortisations):
        # Format: '2010-10-10=10000.0\2011-11-11=11000.0' etc
        dateAmounts = [(a[0], self._FloatToACRFormat(a[1])) for a in amortisations]
        return '\\'.join(('%s=%s' % (da[0], da[1])) for da in dateAmounts)

    def _HandleBreakClause(self, breaks):
        return '\\'.join(breaks)
    
    def _FloatToACRFormat(self, f):
        return '{0:f}'.format(f)
        
    def _UnpackValue(self, value, hint):
        if value:

            if (isinstance(value, str)):
                return value
            elif (isinstance(value, float)):
                return self._FloatToACRFormat(value)
            elif (isinstance(value, Number)):
                return str(value)
            elif value.IsKindOf(acm.FVariantArray):
                if hint == 'riskvalue':
                    return self._HandleReplacementValue(value)
                elif hint == 'amortisation':
                    return self._HandleAmortisation(value)
            elif value.IsKindOf(acm.FDenominatedValue):
                return self._FloatToACRFormat(value.Number())
            elif value.IsKindOf(acm.FArray):
                if hint == 'breakclause':
                    return self._HandleBreakClause(value)
            else:
                print('Cannot unpack value of type ', value.ClassName(), ' : ', value)

        return None


def getCountryOfRisk(party):
    country = party.RiskCountry()
    if country:
        return country.Description()
    else:
        return None

def getCountryOfIncorporation(party):
    return getCountryOfRisk(party)

def getJurisdictionCountry(party):
    country = party.JurisdictionCountryCode()
    return country

def getActive(party):
    return 'Yes'

def getTrading(party):
    return 'Yes'

def getConsolidation(party):
    return 'Yes'

def getParent(party):
    if party.Type() == 'Intern Dept':
        return 'H1'
    elif party.Parent():
        return party.Parent().FACLgetIdentificationCode()
    else:
        return None
        

def getType(party):
    if party.Type() == 'Intern Dept':
        return 'Organisation\Legal Entity'
    elif party.Relation() and party.Relation().Name() == 'Branch':
        return 'Customer\Customer Branch'
    else:
        return 'Customer\Legal Entity'

def getCustomerType(party):
    # NOTE: this needs to be kept in sync with how trades are filtered by counterparty type (see FACLFilterQuery)
    if party:
        if party.Class() == acm.FCounterParty:
            return 'Counterparty'
        elif party.Class() == acm.FClient:
            return 'Client'
        elif party.Class() == acm.FIssuer:
            return 'Issuer'
        else:
            if party.Issuer() and party.Class() in [acm.FBroker, acm.FDepot, acm.FMarketPlace]:
                return 'Issuer'
            else:
                return None
                
    return None

def getMappingProperties(party):
    if party.Type() == 'Intern Dept':
        return InternalDepartmentMapping.properties
    elif party.Relation() and party.Relation().Name() == 'Branch':
        return CustomerBranchMapping.properties
    else:
        return PartyMapping.properties

def getPreviousName(party):
    name = party.Name()
    recordType = acm.GetDomain("enum(B92RecordType)").Enumeration(party.RecordType())

    query = acm.CreateFASQLQuery(acm.FTransactionHistory, 'AND')

    query.AddAttrNode('TransRecordType', 'EQUAL', recordType )
    query.AddAttrNode('RecordId', 'EQUAL', party.Oid() )
    query.AddAttrNode('Version', 'EQUAL', party.VersionId() - 1)
    
    result = query.Select()
    if  result:
        name = query.Select()[0].CreateCloneFromTransaction().Name()

    return name
def callMethodByName(callObj, methodName):
    method = callObj.Class().GetMethod(methodName, 0)
    if method:
        value = str(method.Call([callObj]))
    else:
        methodChain = acm.FMethodChain(methodName)
        value = str(methodChain.Call([callObj]))
    
    return value

def getIdentificationCode(party):
    props = party.FACLgetMappingProperties()
    methodName = props['Identification\Code']
    
    return callMethodByName(party, methodName)
    
def getIdentificationName(party):
    props = party.FACLgetMappingProperties()
    methodName = props['Identification\Name']
    
    return callMethodByName(party, methodName)

def getReference(party):
    props = party.FACLgetMappingProperties()
    methodName = props['Reference']
    
    return callMethodByName(party, methodName)