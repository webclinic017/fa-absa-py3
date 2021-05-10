'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Creates SWIFT MT940 messages and places them on AMB
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               :  Francois Truter
CR NUMBER               :  695005
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date                CR                  Developer                 Description
--------------------------------------------------------------------------------
2011-03-25          686159              Francois Truter           Initial Implementation
2011-06-25          695005              Francois Truter           Calculating values from cashflows
2011-07-12          710394              Rohan van der Walt        Backend Date conversion fix
2015-09-02          CHNG0003153228      Lawrence Mucheka          Added WriteCallAccountMt940ToQueue method
2015-11-06          CHNG0003242578      Lawrence Mucheka          Strip off the Gateway wrapper
2016-02-05          CHNG0003427057      Gabriel Marko             Get MT940 recipient from MT940Recipient BIC Party Alias
2016-02-29          CHNG0003480353      Gabriel Marko             Fix of the balance calculation for loan account; Refactoring
2016-10-31          CHNG0004075040      Gabriel Marko             Fix 28C tag logic - increment daily.
'''

import ael
import acm

'''========================== SWIFT MT940 MESSAGE ==========================='''

from gen_swift_mt_blocks import Body
from gen_swift_mt_fields import *
from gen_swift_mt_messages import MtMessageBase

from gen_absa_xml_config_settings import AmbaType
from gen_absa_xml_config_settings import AmbaXmlConfig
from gen_amb_helper import AmbHelper
from at_timeSeries import (
    add_time_series_value,
    get_time_series_values
)

MANDATORY = True
OPTIONAL = False

MESSAGE_TYPE = 'MT940'
MT940BICALIAS = "MT940RecipientBIC"
MT940_STATEMENT_NUMBER_SPEC = 'MT940_StatementNum'
AMBA_NODE = 'MarketsMessageGatewayAmba'


class Mt940(MtMessageBase):

    def __init__(self):
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 940
        self.MT940BicAlias = MT940BICALIAS

        self._body = Body([
            MtField20('TransactionReferenceNumber', MANDATORY),
            MtField21('RelatedReference', OPTIONAL),
            MtField25('AccountIdentification', MANDATORY),
            MtField28C('StatementNumber', MANDATORY),
            MtField60F('OpeningBalance', MANDATORY),
            RepetitiveSequence(
                'StatementLine',
                [
                    MtField61('Detail', OPTIONAL),
                    MtField86('AccountOwnerInformation', OPTIONAL)
                ],
                OPTIONAL
            ),
            MtField62F('ClosingBalance', MANDATORY),
            MtField64('ClosingAvailableBalance', OPTIONAL),
            RepetitiveSequence(
                'ForwardAvailableBalance',
                [
                    MtField65('Value', OPTIONAL)
                ],
                OPTIONAL
            ),
            MtField86('AccountOwnerInformation', OPTIONAL)
        ])

    def SetRecipientFromAlias(self, party):
        try:
            self.ApplicationHeader.Address.BicCode = party.Alias(self.MT940BicAlias)
        except TypeError:
            raise Exception("Missing MT940Recipient alias for %s." % party.Name())


'''======================= CREATE MT940 FROM CALL ACCOUNT ==================='''

from gen_swift_gateway_message import FrontGatewayMessage
from gen_swift_gateway_message import GatewayMessageFormat
from gen_swift_gateway_message import GatewayMessageType
from gen_swift_mt_messages import GetTransactionReferenceFromRunDate

INTEREST_TYPES = [
    'Call Fixed Rate Adjustable',
    'Call Fixed Rate',
    'Call Float Rate',
    'Fixed Rate Adjustable'
]


def _debitOrCredit(amount):
    return 'D' if amount < 0 else 'C'


class CashTransaction(object):

    def __init__(self, cashFlow, amount, reference=None):
        self._cashFlow = cashFlow
        self._amount = round(amount, 2)
        self._reference = reference if reference else cashFlow.Oid()

    def __str__(self):
        return '%10s %10s %3s %1s %15f %s' % (
            self.ValueDate,
            self.EntryDate,
            self.TransactionType,
            self.DebitOrCredit,
            self.Amount,
            self.Description
        )

    @property
    def CashFlow(self):
        return self._cashFlow

    @property
    def Amount(self):
        return self._amount

    @Amount.setter
    def Amount(self, value):
        self._amount = value

    @property
    def ValueDate(self):
        return self._cashFlow.PayDate()

    @staticmethod
    def _AELTimeToACMDate(time):
        dateString = time.to_string('%Y%m%d')
        return acm.Time().DateFromYMD(dateString[:4], dateString[4:6], dateString[6:8])

    @property
    def EntryDate(self):
        createDate = CashTransaction._AELTimeToACMDate(ael.date_from_time(self._cashFlow.CreateTime()))
        if self._cashFlow.CashFlowType() in INTEREST_TYPES:
            if self._cashFlow.PayDate() < createDate:
                return createDate
            else:
                return self._cashFlow.PayDate()
        else:
            return createDate

    @property
    def TransactionType(self):
        LOOKUP = {
            'None': None,
            'Fixed Amount': 'MSC',
            'Fixed Rate': 'MSC',
            'Float Rate': 'MSC',
            'Caplet': 'MSC',
            'Floorlet': 'MSC',
            'Digital Caplet': 'MSC',
            'Digital Floorlet': 'MSC',
            'Total Return': 'MSC',
            'Credit Default': 'MSC',
            'Call Fixed Rate': 'INT',
            'Call Float Rate': 'INT',
            'Redemption Amount': None,
            'Zero Coupon Fixed': 'MSC',
            'Return': 'RTI',
            'Dividend': 'DIV',
            'Fixed Rate Adjustable': 'INT',
            'Interest Reinvestment': 'INT',
            'Call Fixed Rate Adjustable': 'INT',
            'Fixed Rate Accretive': 'MSC',
            'Position Total Return': 'MSC'
        }

        for interest_type in INTEREST_TYPES:
            LOOKUP[interest_type] = 'INT'

        cashflow_type = self._cashFlow.CashFlowType()

        if cashflow_type in LOOKUP:
            return LOOKUP[cashflow_type]
        else:
            raise Exception('Cashflow type [%s] not mapped to MT940 on FDeposit [%s]' % (cashflow_type, self._cashFlow.Leg().Instrument().Name()))

    @property
    def Description(self):
        LOOKUP = {
            'Interest Reinvestment': 'Interest Reinvested'
        }

        for interest_type in INTEREST_TYPES:
            LOOKUP[interest_type] = 'Interest'

        cashflow_type = self._cashFlow.CashFlowType()
        if cashflow_type in LOOKUP:
            description = LOOKUP[cashflow_type]
            if description == 'Interest':
                if self._amount >= 0:
                    description += ' Received'
                else:
                    description += ' Withdrawn'
            return description
        else:
            if self._amount >= 0:
                return 'Transfer In'
            else:
                return 'Transfer Out'

    @property
    def DebitOrCredit(self):
        return _debitOrCredit(self._amount)

    @property
    def Reference(self):
        return self._reference


class CashAccount(object):
    @staticmethod
    def _selectAllCashFlows(account):
        query = acm.CreateFASQLQuery('FCashFlow', 'AND')
        op = query.AddOpNode('AND')
        op.AddAttrNode('Leg.Instrument.Oid', 'EQUAL', account.Oid())

        return list(query.Select())

    @staticmethod
    def _is_loan_account(account):
        if len(account.Trades()) != 1:
            raise ValueError("Invalid account: The account has to have 1 trade.")
        return account.Trades()[0].Quantity() == -1.0

    @staticmethod
    def _getTransactions(account):
        """Get MT940 relevant transaction from deposit."""
        cashFlows = CashAccount._selectAllCashFlows(account)
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

        interestPayments = []
        interestReinvestments = []
        validTransactions = []

        for cashFlow in cashFlows:
            transaction = CashTransaction(
                cashFlow,
                cashFlow.Calculation().Projected(calcSpace, None).Number()
            )

            if not transaction.TransactionType:
                continue

            if cashFlow.CashFlowType() in INTEREST_TYPES:
                interestPayments.append(transaction)
            elif cashFlow.CashFlowType() == 'Interest Reinvestment':
                interestReinvestments.append(transaction)
            else:
                validTransactions.append(transaction)

        if interestPayments:
            interestPayments.sort(key=lambda transaction: (
                transaction.CashFlow.PayDate(),
                transaction.CashFlow.StartDate(),
                transaction.CashFlow.EndDate())
            )
            interestPayments.pop()

        for reinvestment in interestReinvestments:
            for payment in interestPayments:
                if round(reinvestment.Amount, 2) == round(payment.Amount, 2) * -1.00 \
                and reinvestment.CashFlow.PayDate() == payment.CashFlow.PayDate():
                    interestPayments.remove(payment)
                    break

        validTransactions.extend(interestReinvestments)
        validTransactions.extend(interestPayments)

        for transaction in interestPayments:
            validTransactions.append(
                CashTransaction(
                    transaction.CashFlow,
                    transaction.Amount * -1,
                    str(transaction.CashFlow.Oid()) + 'B'
                )
            )

        if CashAccount._is_loan_account(account):
            for transaction in validTransactions:
                transaction.Amount *= -1

        return sorted(validTransactions,
                      key=lambda transaction: (
                          transaction.CashFlow.PayDate(),
                          transaction.CashFlow.StartDate(),
                          transaction.CashFlow.EndDate()))

    def __init__(self, fDeposit):
        self._transactions = CashAccount._getTransactions(fDeposit)
        self._currency = fDeposit.Currency().Name()

    @property
    def Currency(self):
        return self._currency

    def Transactions(self, startDate, endDate):
        return [transaction
                for transaction in self._transactions
                if startDate <= transaction.ValueDate <= endDate]

    def BookBalance(self, balanceDate):
        balance = sum(transaction.Amount
                      for transaction in self._transactions
                      if transaction.ValueDate <= balanceDate)
        return balance

    def AvailableBalance(self, statementDate, balanceDate):
        balance = sum(transaction.Amount
                      for transaction in self._transactions
                      if (transaction.EntryDate <= statementDate
                          and transaction.ValueDate <= balanceDate))

        return balance

    def ForwardBalances(self, statementDate):
        balances = {}

        for transaction in self._transactions:
            if (transaction.EntryDate <= statementDate < transaction.ValueDate
                and transaction.ValueDate not in balances):
                balances[transaction.ValueDate] = 0

        for balanceDate in balances:
            balances[balanceDate] = self.AvailableBalance(statementDate, balanceDate)

        return balances


def _getMt940FromCallAccount(account, statementNumber, startDate, endDate, onlyIfTransactions):

    if not startDate:
        startDate = endDate

    cashAccount = CashAccount(account)
    transactions = cashAccount.Transactions(startDate, endDate)

    if onlyIfTransactions and not transactions:
        return None

    dayBeforeStartDate = acm.Time().DateAddDelta(startDate, 0, 0, -1)
    accountOwner = account.TradeCounterparty()

    message = Mt940()
    message.SetRecipientFromAlias(accountOwner)
    message.SetMeridianBusinessEntityFromParty(accountOwner)

    message.Body.TransactionReferenceNumber = GetTransactionReferenceFromRunDate(account, endDate)
    message.Body.AccountIdentification = (account.Name()[0:35]).replace('#', '')
    message.Body.StatementNumber.Value = statementNumber

    openingBalance = cashAccount.BookBalance(dayBeforeStartDate)
    message.Body.OpeningBalance.DebitCredit = _debitOrCredit(openingBalance)
    message.Body.OpeningBalance.Date = startDate
    message.Body.OpeningBalance.Amount.Currency = cashAccount.Currency
    message.Body.OpeningBalance.Amount.Value = openingBalance

    for transaction in transactions:
        line = message.Body.StatementLine.AddSequence()
        line.Detail.ValueDate = transaction.ValueDate
        line.Detail.EntryDate = transaction.EntryDate
        line.Detail.DebitCredit = transaction.DebitOrCredit
        line.Detail.Amount.Currency = cashAccount.Currency
        line.Detail.Amount.Value = transaction.Amount
        line.Detail.TransactionType = 'N'
        line.Detail.TransactionIdentificationCode = transaction.TransactionType
        line.Detail.AccountOwnerReference = 'NONREF'
        line.Detail.InstitutionReference = transaction.Reference
        line.Detail.SupplementaryDetails = transaction.Description

    closingBalance = cashAccount.BookBalance(endDate)
    message.Body.ClosingBalance.DebitCredit = _debitOrCredit(closingBalance)
    message.Body.ClosingBalance.Date = endDate
    message.Body.ClosingBalance.Amount.Currency = cashAccount.Currency
    message.Body.ClosingBalance.Amount.Value = closingBalance

    closingAvailableBalance = cashAccount.AvailableBalance(endDate, endDate)
    message.Body.ClosingAvailableBalance.DebitCredit = _debitOrCredit(closingAvailableBalance)
    message.Body.ClosingAvailableBalance.Date = endDate
    message.Body.ClosingAvailableBalance.Amount.Currency = cashAccount.Currency
    message.Body.ClosingAvailableBalance.Amount.Value = closingAvailableBalance

    forwardBalances = cashAccount.ForwardBalances(endDate)
    for forwardDate in forwardBalances:
        forwardBalance = forwardBalances[forwardDate]
        forwardAvailableBalance = message.Body.ForwardAvailableBalance.AddSequence()
        forwardAvailableBalance.Value.DebitCredit = _debitOrCredit(forwardBalance)
        forwardAvailableBalance.Value.Date = forwardDate
        forwardAvailableBalance.Value.Amount.Currency = cashAccount.Currency
        forwardAvailableBalance.Value.Amount.Value = forwardBalance

    return message


def get_next_statement_number(account, date):
    numbers = acm.FTimeSeries.Select(
        "timeSeriesSpec = '%(spec)s' and recaddr = %(rec)i and day >= '%(day)s'" %
        {
            'spec': MT940_STATEMENT_NUMBER_SPEC,
            'rec': account.Oid(),
            'day': acm.Time().FirstDayOfYear(date)
        }
    )

    if not numbers:
        return None

    return max(int(number.TimeValue()) for number in numbers)


def _get_statement_number_new_run_no(spec_name, obj, date):
    timeSeries = acm.FTimeSeries.Select(
        "timeSeriesSpec = '%(spec)s' and recaddr = %(rec)i and day >= '%(day)s'" %
        {
            'spec': spec_name,
            'rec': obj.Oid(),
            'day': acm.Time().FirstDayOfYear(date)
        }
    )

    if not timeSeries:
        return 0

    last_run_no = max(i.RunNo() for i in timeSeries)

    return last_run_no + 1


def set_next_statement_number(account, date, value=1):
    runNo = _get_statement_number_new_run_no(
        MT940_STATEMENT_NUMBER_SPEC,
        account,
        acm.Time().FirstDayOfYear(date)
    )

    # add_time_series_value(ts_name, recaddr, value, date, run_number=None):
    add_time_series_value(
        MT940_STATEMENT_NUMBER_SPEC,
        account.Oid(),
        value,
        acm.Time().FirstDayOfYear(date),
        run_number=runNo
    )


def GetGatewayMessage(account, startDate, endDate, onlyIfTransactions):

    statementNumber = get_next_statement_number(account, endDate)

    mt940_message = _getMt940FromCallAccount(
        account,
        statementNumber,
        startDate,
        endDate,
        onlyIfTransactions
    )

    if not mt940_message:
        return None

    recipient = mt940_message.ApplicationHeader.Address

    gatewayMessage = FrontGatewayMessage(
        recipient,
        mt940_message.Body.TransactionReferenceNumber,
        str(account.Oid()),
        MESSAGE_TYPE,
        GatewayMessageType.New,
        GatewayMessageFormat.Swift,
        str(mt940_message)
    )

    return (statementNumber, gatewayMessage)


def GetRawMessage(account, start_date, end_date, statement_number=None, only_if_transactions=False):

    if statement_number is None:
        statement_number = get_next_statement_number(account, end_date) or 1

    mt940 = _getMt940FromCallAccount(
        account,
        statement_number,
        start_date,
        end_date,
        only_if_transactions
    )

    if not mt940:
        return None

    return (statement_number, str(mt940))


def WriteCallAccountMt940ToAmb(account, startDate, endDate, onlyIfTransactions):

    result = GetGatewayMessage(
        account,
        startDate,
        endDate,
        onlyIfTransactions
    )

    if not result:
        return False

    ambaConfig = AmbaXmlConfig(AMBA_NODE, AmbaType.Sender)
    AmbHelper.WriteSwiftMtMessageWithStatementToQueue(
        ambaConfig,
        MESSAGE_TYPE,
        str(result[1]),
        account.Oid(),
        result[0],
        endDate
    )

    return True
