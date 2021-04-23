"""----------------------------------------------------------------------------
PROJECT                 :  SBL ACS Migration
PURPOSE                 :  Class for generating fixed length trade files to be
                           sent to Global One
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  500714

HISTORY
===============================================================================
Date       Change no Developer          Description
-------------------------------------------------------------------------------
2010-10-15 450056    Francois Truter    Initial Implementation
2010-10-19 468171    Francois Truter    Added WriteConfirmationReport
2010-10-19 500714    Francois Truter    Updates the file footer for the new
                                        Global One version 7.20
2011-04-21 634517    Rohan vd Walt      Check environment before calling msgBox
2013-05-09 999016    Peter Basista      Feed SL Dividend Factor to Global One.
----------------------------------------------------------------------------"""

import datetime
import shutil
import time

import acm
import ael

from gen_fixed_length_record import DatetimeField
from gen_fixed_length_record import ImpliedDecimalField
from gen_fixed_length_record import IntField
from gen_fixed_length_record import IntRangeField
from gen_fixed_length_record import ListField
from gen_fixed_length_record import Record
from gen_fixed_length_record import StringField
from gen_fixed_length_record import YesNoField
import sl_return_confirmation_summary

NEWLINE = '\n'

class GlobalOneStatus:
    New = 'N'
    Cancelled = 'C'
    Amended = 'A'
    Update = 'U'
    Authorise = 'T'
    PendingCancellation = 'D'
    AcceptPendingCancellation = 'E'
    RejectPendingCancellation = 'X'

class TransactionType:
    Trade = 'T'
    Return = 'R'
    ReAllocation = 'A'
    RaisePriority = 'P'
    CancelCrestInstruction = 'C'
    Split = 'S'
    Repo = 'M'
    RepoRollover = 'O'
    FullReturn = 'F'

class SecurityCodeType:
    Sedol = 'A'
    ISIN = 'B'
    Cusip = 'C'
    Quick = 'D'
    Ticker = 'E'
    InHouse = 'F'

class PostingType:
    Borrow = 'B'
    Loan = 'L'
    Hold = 'H'

class LenderModuleTrade:
    Automatic = '1'
    ManualValidation = '2'
    ManualNoValidation = '3'

class ReturnUpdateFlag:
    UseAllRecords = 'C'
    DefaultFromParent = 'U'

class G1UploadHeader(Record):

    def __init__(self):
        Record.__init__(self, 'Global One Upload Header', [
            IntField('RecordType', False, 1, 0),
            DatetimeField('RecordDate', '%Y%m%d', datetime.datetime.today()),
            YesNoField('MultipleAcceptanceRecords'),
            YesNoField('CreateInvalidSecurities'),
            StringField('Filler', 3781, '')])

class G1UploadFooter(Record):

    def __init__(self):
        Record.__init__(self, 'Global One Upload Footer', [
            IntField('RecordType', False, 1, 9),
            IntField('RecordCount', False, 10, 0),
            StringField('Filler', 3781, '')])

class GlUploadDetail(Record):

    def __init__(self):
        Record.__init__(self, 'Global One Upload Detail', [
            IntField('RecordType', False, 1, 1),
            ListField('Status', 1, ['N', 'C', 'A', 'U', 'T', 'D', 'E', 'X']),
            ListField('TransactionType', 1, ['T', 'R', 'A', 'P', 'C', 'S',
                'M', 'O', 'F']),
            StringField('PostingType', 3),
            StringField('CounterpartyCode', 6),
            StringField('CounterpartyCrossReference', 10),
            ListField('SecurityCodeType', 1, ['A', 'B', 'C', 'D', 'E', 'F']),
            StringField('Sedol', 12),
            StringField('IsinCode', 12),
            StringField('CusipCode', 12),
            StringField('QuickCode', 12),
            StringField('TickerCode', 12),
            StringField('InHouseCrossReference', 12),
            YesNoField('Callable'),
            ListField('CollateralType', 1, ['C', 'N', 'P'], 'N', True),
            IntField('Quantity', True, 11),
            StringField('Currency', 3),
            ImpliedDecimalField('LoanPrice', True, 9, 4),
            ImpliedDecimalField('LoanValue', True, 11, 2),
            ImpliedDecimalField('RequiredMargin', False, 3, 2),
            ImpliedDecimalField('InterestRate', True, 2, 6),
            DatetimeField('SecuritySettlementDueDate', '%Y%m%d'),
            StringField('SecuritySettlementMode', 6),
            DatetimeField('CashSettlementDueDate', '%Y%m%d'),
            StringField('CashSettlementMode', 6),
            YesNoField('Dvp'),
            DatetimeField('TradeDate', '%Y%m%d'),
            DatetimeField('TermDate', '%Y%m%d'),
            # Pushing the dividend percentage to Global One.
            ImpliedDecimalField('NetDividendPercentage', False, 3, 2),
            ImpliedDecimalField('OverseasTaxPercentage', False, 3, 2),
            ImpliedDecimalField('DomesticTaxPercentage', False, 3, 2),
            StringField('InterestType', 2),
            StringField('InternalComments', 20),
            StringField('ExternalComments', 50),
            StringField('TradeCategory', 3),
            StringField('LinkReference', 8),
            StringField('OwnContractReference', 16),
            StringField('GlobalOneTradeReference', 12),
            ImpliedDecimalField('MinimumFee', False, 12, 2),
            StringField('MinimumFeeCurrency', 3),
            StringField('FinderLocBankCode', 6),
            ImpliedDecimalField('FinderLocBankFee', False, 3, 6),
            StringField('EuroclearSharesType', 3),
            StringField('EuroclearReference', 16),
            ImpliedDecimalField('EuroclearPrice', False, 10, 4),
            IntField('EuroclearPriority', False, 1),
            StringField('EuroclearComments', 35),
            StringField('OwnShiftBicCode', 20),
            StringField('CashClearerCode', 10),
            StringField('CashClearSwiftBic', 25),
            StringField('CashClearerAccountNumber', 25),
            StringField('CashClearerSubAccount', 25),
            StringField('CashClearerAccountReference', 50),
            StringField('CashClearerContact', 30),
            StringField('CashClearerName', 50),
            StringField('SecurityClearerCode', 10),
            StringField('SecurityClearerSwiftBic', 25),
            StringField('SecurityClearerAccountNumber', 25),
            StringField('SecurityClearerSubAccount', 25),
            StringField('SecurityClearerAccountReference', 50),
            StringField('SecurityClearerContact', 30),
            StringField('SecurityClearerName', 50),
            StringField('ClCashClearerCode', 10),
            StringField('ClCashClearerSwiftBic', 25),
            StringField('ClCashClearerAccountNumber', 25),
            StringField('ClCashClearerSubAccount', 25),
            StringField('ClCashClearerAccountReference', 50),
            StringField('ClCashClearerContact', 30),
            StringField('ClCashClearerName', 50),
            StringField('ClSecurityClearerCode', 10),
            StringField('ClSecurityClearerSwiftBic', 25),
            StringField('ClSecurityClearerAccountNumber', 25),
            StringField('ClSecurityClearerSubAccount', 25),
            StringField('ClSecurityClearerAccountReference', 50),
            StringField('ClSecurityClearerContact', 30),
            StringField('ClSecurityClearerName', 50),
            YesNoField('RecalledIndicator'),
            StringField('FundCode', 6),
            StringField('FundCrossReference', 10),
            StringField('FundLocation', 3),
            StringField('FundLocationCrossReference', 10),
            YesNoField('AutoSettlement'),
            ImpliedDecimalField('NonCashCollateralHaircut', False, 3, 2),
            ImpliedDecimalField('CashPoolValue', True, 11, 2),
            ImpliedDecimalField('PrePayRate', True, 2, 6),
            StringField('CostCentre1Code', 3),
            IntField('CostCentre1Quantity', True, 11),
            ImpliedDecimalField('CostCentre1Value', True, 11, 2),
            StringField('CostCentre2Code', 3),
            IntField('CostCentre2Quantity', True, 11),
            ImpliedDecimalField('CostCentre2Value', True, 11, 2),
            StringField('CostCentre3Code', 3),
            IntField('CostCentre3Quantity', True, 11),
            ImpliedDecimalField('CostCentre3Value', True, 11, 2),
            StringField('CostCentre4Code', 3),
            IntField('CostCentre4Quantity', True, 11),
            ImpliedDecimalField('CostCentre4Value', True, 11, 2),
            StringField('CostCentre5Code', 3),
            IntField('CostCentre5Quantity', True, 11),
            ImpliedDecimalField('CostCentre5Value', True, 11, 2),
            StringField('CostCentre6Code', 3),
            IntField('CostCentre6Quantity', True, 11),
            ImpliedDecimalField('CostCentre6Value', True, 11, 2),
            StringField('CostCentre7Code', 3),
            IntField('CostCentre7Quantity', True, 11),
            ImpliedDecimalField('CostCentre7Value', True, 11, 2),
            StringField('CostCentre8Code', 3),
            IntField('CostCentre8Quantity', True, 11),
            ImpliedDecimalField('CostCentre8Value', True, 11, 2),
            StringField('CostCentre9Code', 3),
            IntField('CostCentre9Quantity', True, 11),
            ImpliedDecimalField('CostCentre9Value', True, 11, 2),
            StringField('CostCentre10Code', 3),
            IntField('CostCentre10Quantity', True, 11),
            ImpliedDecimalField('CostCentre10Value', True, 11, 2),
            YesNoField('MarketTradeIndicator'),
            StringField('DealerIdentifier', 8),
            YesNoField('MatchedInvestment'),
            DatetimeField('TradeTime', '%H:%M'),
            StringField('InternalCommentsSecondLine', 20),
            StringField('ExternalCommentsSecondLine', 50),
            ImpliedDecimalField('ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('ExtendedLoanPrice', True, 9, 7),
            ImpliedDecimalField('CostCentre1ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre2ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre3ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre4ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre5ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre6ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre7ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre8ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre9ExtendedQuantity', True, 11, 2),
            ImpliedDecimalField('CostCentre10ExtendedQuantity', True, 11, 2),
            ListField('ReturnUpdateFlag', 1, ['C', 'U']),
            YesNoField('CompareDividendTracking'),
            YesNoField('CompareMarkEligible'),
            ListField('LenderModuleTrade', 1, ['1', '2', '3']),
            StringField('FundCode1', 6),
            StringField('FundCrossReference1', 10),
            StringField('FundLocation1', 3),
            StringField('FundLocationCrossReference1', 10),
            ImpliedDecimalField('Fund1Quantity', True, 11, 2),
            ImpliedDecimalField('Fund1Value', True, 11, 2),
            StringField('FundCode2', 6),
            StringField('FundCrossReference2', 10),
            StringField('FundLocation2', 3),
            StringField('FundLocationCrossReference2', 10),
            ImpliedDecimalField('Fund2Quantity', True, 11, 2),
            ImpliedDecimalField('Fund2Value', True, 11, 2),
            StringField('FundCode3', 6),
            StringField('FundCrossReference3', 10),
            StringField('FundLocation3', 3),
            StringField('FundLocationCrossReference3', 10),
            ImpliedDecimalField('Fund3Quantity', True, 11, 2),
            ImpliedDecimalField('Fund3Value', True, 11, 2),
            StringField('FundCode4', 6),
            StringField('FundCrossReference4', 10),
            StringField('FundLocation4', 3),
            StringField('FundLocationCrossReference4', 10),
            ImpliedDecimalField('Fund4Quantity', True, 11, 2),
            ImpliedDecimalField('Fund4Value', True, 11, 2),
            StringField('FundCode5', 6),
            StringField('FundCrossReference5', 10),
            StringField('FundLocation5', 3),
            StringField('FundLocationCrossReference5', 10),
            ImpliedDecimalField('Fund5Quantity', True, 11, 2),
            ImpliedDecimalField('Fund5Value', True, 11, 2),
            StringField('FundCode6', 6),
            StringField('FundCrossReference6', 10),
            StringField('FundLocation6', 3),
            StringField('FundLocationCrossReference6', 10),
            ImpliedDecimalField('Fund6Quantity', True, 11, 2),
            ImpliedDecimalField('Fund6Value', True, 11, 2),
            StringField('FundCode7', 6),
            StringField('FundCrossReference7', 10),
            StringField('FundLocation7', 3),
            StringField('FundLocationCrossReference7', 10),
            ImpliedDecimalField('Fund7Quantity', True, 11, 2),
            ImpliedDecimalField('Fund7Value', True, 11, 2),
            StringField('FundCode8', 6),
            StringField('FundCrossReference8', 10),
            StringField('FundLocation8', 3),
            StringField('FundLocationCrossReference8', 10),
            ImpliedDecimalField('Fund8Quantity', True, 11, 2),
            ImpliedDecimalField('Fund8Value', True, 11, 2),
            StringField('FundCode9', 6),
            StringField('FundCrossReference9', 10),
            StringField('FundLocation9', 3),
            StringField('FundLocationCrossReference9', 10),
            ImpliedDecimalField('Fund9Quantity', True, 11, 2),
            ImpliedDecimalField('Fund9Value', True, 11, 2),
            StringField('FundCode10', 6),
            StringField('FundCrossReference10', 10),
            StringField('FundLocation10', 3),
            StringField('FundLocationCrossReference10', 10),
            ImpliedDecimalField('Fund10Quantity', True, 11, 2),
            ImpliedDecimalField('Fund10Value', True, 11, 2),
            DatetimeField('FundCostCentreReallocationDate', '%Y%m%d'),
            ListField('InterestRateSign', 1, ['-']),
            StringField('AgencyReference', 16),
            StringField('TransactionNarative', 20),
            YesNoField('AutoAuthorised'),
            YesNoField('SecurityBulking'),
            StringField('BulkingReference', 2),
            StringField('CollateralGroupingCode', 3),
            StringField('CashWashCurrency', 3),
            ImpliedDecimalField('CashWashValue', True, 11, 2),
            IntField('NoOfFundCostCentreAdditionalRecords', False, 5),
            IntField('NoOfUserDefinedFieldAdditionalRecords', False, 5),
            ListField('NonDollarRepoTrade', 1, ['1', '2']),
            ImpliedDecimalField('CouponInterest', False, 12, 2),
            ImpliedDecimalField('EndCouponInterest', False, 12, 2),
            ImpliedDecimalField('InvestmentRate', False, 3, 6),
            ImpliedDecimalField('AccrualValue', False, 12, 2),
            YesNoField('MonthlyBilled'),
            ImpliedDecimalField('CleanPrice', False, 9, 6),
            StringField('ReturnCashClearerCode', 10),
            StringField('ReturnCashClearerSwiftBic', 25),
            StringField('ReturnCashClearerAccountNumber', 25),
            StringField('ReturnCashClearerSubAccount', 25),
            StringField('ReturnCashClearerAccountReference', 50),
            StringField('ReturnCashClearerContact', 30),
            StringField('ReturnCashClearerName', 50),
            StringField('ReturnSecurityClearerCode', 10),
            StringField('ReturnSecurityClearerSwiftBic', 25),
            StringField('ReturnSecurityClearerAccountNumber', 25),
            StringField('ReturnSecurityClearerSubAccount', 25),
            StringField('ReturnSecurityClearerAccountReference', 50),
            StringField('ReturnSecurityClearerContact', 30),
            StringField('ReturnSecurityClearerName', 50),
            StringField('ClReturnCashClearerCode', 10),
            StringField('ClReturnCashClearerSwiftBic', 25),
            StringField('ClReturnCashClearerAccountNumber', 25),
            StringField('ClReturnCashClearerSubAccount', 25),
            StringField('ClReturnCashClearerAccountReference', 50),
            StringField('ClReturnCashClearerContact', 30),
            StringField('ClReturnCashClearerName', 50),
            StringField('ClReturnSecurityClearerCode', 10),
            StringField('ClReturnSecurityClearerSwiftBic', 25),
            StringField('ClReturnSecurityClearerAccountNumber', 25),
            StringField('ClReturnSecurityClearerSubAccount', 25),
            StringField('ClReturnSecurityClearerAccountReference', 50),
            StringField('ClReturnSecurityClearerContact', 30),
            StringField('ClReturnSecurityClearerName', 50),
            YesNoField('RollAccrualInterest'),
            IntRangeField('CrestPriority', 0, 90),
            ListField('CrestSystemOfOrigin', 1, ['S', 'T', 'I', 'L', 'O']),
            YesNoField('CrestNcCondition'),
            ListField('CrestCashMovementType', 1, ['A', 'C', 'O']),
            ListField('CrestAgentIndicator', 1, ['A', 'P', 'S', 'N']),
            ImpliedDecimalField('CrestDbvMargin', False, 4, 2),
            ImpliedDecimalField('CrestDbvConsideration', False, 14, 2),
            YesNoField('CrestConcentrationLimit'),
            YesNoField('CrestIncludeRate'),
            ImpliedDecimalField('CrestMatchingConsideration', False, 14, 2),
            YesNoField('CrestSuppressRevaluation'),
            YesNoField('CrestBargainConditions1'),
            YesNoField('CrestBargainConditions2'),
            YesNoField('CrestBargainConditions3'),
            YesNoField('CrestBargainConditions4'),
            YesNoField('CrestBargainConditions5'),
            YesNoField('CrestBargainConditions6'),
            YesNoField('CrestBargainConditions7'),
            YesNoField('CrestBargainConditions8'),
            YesNoField('CrestBargainConditions9'),
            YesNoField('CrestBargainConditions10'),
            YesNoField('CrestAutoRaisePriority'),
            IntRangeField('CrestNewPriority', 0, 90),
            IntField('NumberOfSplitRecords', False, 5),
            YesNoField('AmendmentUpdateFlag'),
            YesNoField('CancelPendingMark'),
            ListField('SuppressConfirmInstructions', 1, ['C', 'I', 'B']),
            YesNoField('MandatoryOwnContractReference', True, True),
            ListField('UsRepoAccrualType', 1, ['M', 'R', 'B']),
            YesNoField('TaxableFlag'),
            StringField('MatchedInvestmentDefaultCode', 6),
            ListField('AuthorisedSecurityCancels', 1, ['A', 'R']),
            ListField('MinimumFeeType', 1, ['B', 'F', 'V']),
            ImpliedDecimalField('MinimumFeeValue', False, 7, 2),
            StringField('MinimumFeeValueCurrency', 3),
            YesNoField('ProhibitDuplicateOwnContractRefs', True, True),
            StringField('DbvClassGroupCode', 3),
            StringField('LenderAllocationOverrideReasonCode', 3),
            StringField('BulkCashPoolExtendedReference', 3),
            ImpliedDecimalField('CollateralMargin', False, 3, 2),
            StringField('ExternalUserId', 10),
            YesNoField('InvalidClearerCodeOverrideIndicator'),
            YesNoField('WarningOverrideIndicator'),
            ImpliedDecimalField('MinimumQuantity', False, 12, 2),
            ImpliedDecimalField('RoundingQuantity', False, 12, 2),
            StringField('LenderSettlementID', 12),
            DatetimeField('OriginalTermDate', '%Y%m%d'),
            YesNoField('LenderSpecialLoanIndicator'),
            StringField('LenderCustodyBankCode', 3),
            StringField('LenderCustodyBankCrossReference', 10),
            StringField('LenderLocationCode', 3),
            StringField('LenderLocationCrossReference', 10),
            ListField('OriginalCurrentFaceIndicatorForMortageBackSecurities',
                1, ['O', 'C']),
            YesNoField('SecuritySettlementModeOverride'),
            YesNoField('CashSettlementModeOverride'),
            StringField('OwnCashAgencyCode', 6),
            StringField('OwnSecurityAgencyCode', 6),
            StringField('CounterpartyCashAgencyCode', 6),
            StringField('CounterpartySecurityAgencyCode', 6),
            StringField('RepoReturnOwnCashAgencyCode', 6),
            StringField('RepoReturnOwnSecurityAgencyCode', 6),
            StringField('RepoReturnCounterpartyCashAgencyCode', 6),
            StringField('RepoReturnCounterpartySecurityAgencyCode', 6),
            StringField('ProfitCentreCode', 1),
            StringField('CrestTransactionNumber', 16),
            ListField('SecurityBulkingLevel', 1, ['C', 'M', 'R']),
            YesNoField('FundMajorFlag'),
            StringField('DividendOverrideReasonCode', 3),
            StringField('DefaultDataCode', 6),
            ImpliedDecimalField('ExtendedNetDividendPercentage', False, 3, 6),
            ImpliedDecimalField('ExtendedOverseasTaxPercentage', False, 3, 6),
            ImpliedDecimalField('ExtendedDomesticTaxPercentage', False, 3, 6),
            ])

class GlUploadFile():

    def __init__(self):
        self._header = G1UploadHeader()
        self._footer = G1UploadFooter()
        self._records = {}

    @property
    def Header(self):
        return self._header

    @property
    def Footer(self):
        return self._footer

    @property
    def Filename(self):
        return 'TR' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.DAT'

    def CreateRecord(self, trade):
        _record = GlUploadDetail()
        if trade in self._records:
            self._records[trade].append(_record)
        else:
            self._records[trade] = [_record]
        return _record

    def WriteFile(self, filepath, backupPath = None, stampTrade = True):
        success = True

        if not self._records:
            if str(acm.Class()) == "FTmServer":
                func = acm.GetFunction('msgBox', 3)
                func('Warning', 'There are no records to write to the '
                    'Global One Upload File.\nNo file will be written.', 0)
            else:
                print ('There are no records to write to the Global One '
                    'Upload File.\nNo file will be written.')
            return success

        if backupPath:
            backup = True
        else:
            backup = False
            backupPath = filepath

        now = time.time()
        acm.BeginTransaction()
        try:
            with open(backupPath, 'w') as reportFile:
                with open(backupPath + '.err', 'w') as errFile:
                    reportFile.write(str(self._header))
                    counter = 0
                    formatting = ''
                    for trade in self._records:
                        try:
                            for _record in self._records[trade]:
                                recordStr = str(_record)
                                reportFile.write(NEWLINE + recordStr)
                                counter += 1
                        except Exception, ex:
                            line = "{0}Trade {1}: {2}".format(formatting, trade.Oid(), str(ex))
                            errFile.write(line)
                            formatting = NEWLINE
                            success = False
                        else:
                            if stampTrade:
                                trade.SLGlobalOneTimeStamp(now)

                    self._footer.RecordCount.Value(counter)
                    reportFile.write(NEWLINE + str(self._footer))
        except Exception, ex:
            acm.AbortTransaction()
            success = False
            raise ex
        else:
            if success:
                acm.CommitTransaction()
                if backup:
                    shutil.copy2(backupPath, filepath)
            else:
                acm.AbortTransaction()

        return success

    def WriteConfirmationReport(self, outputDirectory):
        trades = self._records.keys()
        returnedTrades = []
        for trade in trades:
            record = self._records[trade][0]
            if (record.TransactionType.GetValue() == TransactionType.Return
                and trade.SLPartialReturnIsPartOfChain()):
                 returnedTrades.append(trade.SLPartialReturnPrevTrade())
            elif (record.TransactionType.GetValue() ==
                TransactionType.FullReturn and
                trade.Instrument().OpenEnd() == 'Terminated'):
                returnedTrades.append(trade)

        if returnedTrades:
            excludeGlobalOneStampedTrades = False
            sl_return_confirmation_summary.WriteConfirmationSummary(
                outputDirectory, returnedTrades, excludeGlobalOneStampedTrades,
                False, None, None)
