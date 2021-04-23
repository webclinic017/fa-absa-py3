""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingCalculations.py"
import acm

# accounting
from FAccountingEnums import DebitOrCredit, JournalType
from FAccountingCompare import BelongsToDebitSide


#-------------------------------------------------------------------------
def IsAmountZero(amount):
    return acm.Math.AlmostZero(amount, 10e-5)

#-------------------------------------------------------------------------
def IsJournalAmountZero(journal):
    assert journal, 'No journal given'

    return IsAmountZero(journal.Amount())

#-------------------------------------------------------------------------
def IsJournalBaseAmountZero(journal):
    assert journal, 'No journal given'

    return IsAmountZero(journal.BaseAmount())

#-------------------------------------------------------------------------
def IncrementalBaseAmountUpdate(newJournal, prevJournal):
    if newJournal and prevJournal:

        assert newJournal.Currency() == prevJournal.Currency(), \
            'ERROR: New journal and previous journal with oid {} have different currency'.\
             format(prevJournal.Oid())

        assert newJournal.BaseCurrency() == prevJournal.BaseCurrency(), \
            'ERROR: New journal and previous journal with oid {} have different base currency'.\
             format(prevJournal.Oid())

        assert not newJournal.IsExchangeRateMissing(), \
            'ERROR: Missing FX rate for {} - {}, journals with eventdate {} will be generated with BaseAmount 0'.\
             format(newJournal.Currency().Name(), newJournal.BaseCurrency().Name(), newJournal.EventDate())

        assert not prevJournal.IsExchangeRateMissing(), \
            'ERROR: Previous journals with eventdate {} has missing FX Rate, journals with eventdate {} will be generated with BaseAmount 0'.\
             format(prevJournal.EventDate(), newJournal.EventDate())

        assert not newJournal.IsCalculationAmountFailed(), \
            'ERROR: Journals created with eventdate {} has amount calculation failed, journals will be generated with BaseAmount 0'.\
             format(newJournal.EventDate(), newJournal.EventDate())

        assert not prevJournal.IsCalculationAmountFailed(), \
            'ERROR: Previous journals with eventdate {} has amount calculation failed, journals with eventdate {} will be generated with BaseAmount 0'.\
             format(prevJournal.EventDate(), newJournal.EventDate())

        assert not prevJournal.IsBaseAmountCalculationFailed(), \
            'ERROR: Previous journals with eventdate {} has base amount calculation failed, journals with eventdate {} will be generated with BaseAmount 0'.\
             format(prevJournal.EventDate(), newJournal.EventDate())

        if (prevJournal.Amount() != 0 or prevJournal.BaseAmount() != 0):

            newJournal.BaseAmount(prevJournal.BaseAmount() + __CalculateBaseAmountDifference(newJournal, prevJournal))


#-------------------------------------------------------------------------
def __CalculateBaseAmountDifference(journal1, journal2):
    diff = journal1.Amount() - journal2.Amount()

    return acm.Accounting.GetRoundedAmount(diff * journal1.StoredFxRate(), journal1.BaseCurrency())

#-------------------------------------------------------------------------
def CalculateDebitCreditDelta(journals):
    debitLocal = 0.0
    creditLocal = 0.0
    baseDebit = 0.0
    baseCredit = 0.0

    for journal in journals:
        if journal.DebitOrCredit() == DebitOrCredit.DEBIT:
            debitLocal = debitLocal + journal.Amount()
            baseDebit = baseDebit + journal.BaseAmount()
        elif journal.DebitOrCredit() == DebitOrCredit.CREDIT:
            creditLocal = creditLocal + journal.Amount()
            baseCredit = baseCredit + journal.BaseAmount()

    return (creditLocal + debitLocal), (baseCredit + baseDebit)

#-------------------------------------------------------------------------
def CalculateFXRevaluationAmount(amount, baseAmount, templateJournal, date):
    assert templateJournal, 'ERROR: No templateJournal given for revaluation calculation'

    revaluationAmount = 0.0
    book = templateJournal.Book()
    localCurrency = templateJournal.Currency()
    baseCurrency = templateJournal.BaseCurrency()

    assert book, 'ERROR: No book given for revaluation calculation'
    assert localCurrency, 'ERROR: No currency given for revaluation calculation'
    assert baseCurrency, 'ERROR: No base currency given for revaluation calculation'

    market = book.FxConversionMarket()

    exchangeRate = acm.Accounting().GetFxRate(baseCurrency, localCurrency, date, market)

    if exchangeRate:
        revaluationAmount = acm.Accounting().GetRoundedAmount((amount * exchangeRate - baseAmount), baseCurrency)

    return revaluationAmount

#-------------------------------------------------------------------------
def CalculateFXRevaluationAmountXPL(date, templateJournal, journals, amount, baseAmount, fxUplRevals = None):
    baseCurrency = templateJournal.BaseCurrency()
    localCurrency = templateJournal.Currency()
    book = templateJournal.Book()
    market = book.FxConversionMarket() if book else None
    exchangeRate = acm.Accounting().GetFxRate(baseCurrency, localCurrency, date, market)
    if not exchangeRate:
        return 0, 0

    openBaseAmount = baseAmount
    if journals:
        openBaseAmount = CalculateFXRevaluationRplAmount(amount, baseAmount, journals, fxUplRevals)
    else:
        pass

    rplAmount = acm.Accounting().GetRoundedAmount((openBaseAmount - baseAmount), baseCurrency)
    uplAmount = acm.Accounting().GetRoundedAmount((amount * exchangeRate - openBaseAmount), baseCurrency)
    return uplAmount, rplAmount

#-------------------------------------------------------------------------
def CalculateDebitAndCreditSums(journals):
    debitSum, creditSum = [0, 0], [0, 0]
    periodic = False
    for j in journals:
        rightSideSum = debitSum if BelongsToDebitSide(j) else creditSum
        rightSideSum[0] += j.Amount()
        rightSideSum[1] += j.BaseAmount()
        periodic = True if (periodic or j.AccountingInstruction() and j.AccountingInstruction().IsPeriodic()) else False
    return debitSum, creditSum, periodic

#-------------------------------------------------------------------------
def CalculateFXRevaluationRplAmount(totalAmount, totalBaseAmount, journals, totalUpl):
    dr, cr, hasPeriodicJournals = CalculateDebitAndCreditSums(journals)

    previousTotalAmount = totalAmount - dr[0] - cr[0]
    previousTotalBaseAmount = totalBaseAmount - dr[1] - cr[1]

    openBaseAmount = previousTotalBaseAmount - totalUpl

    drFirst = previousTotalAmount < 0 if hasPeriodicJournals else previousTotalAmount > 0

    for amount, baseAmount in ( dr, cr ) if drFirst else ( cr, dr ):
        if amount == 0.0:
            pass
        elif previousTotalAmount * amount >= 0.0:
            openBaseAmount += baseAmount
        elif abs(previousTotalAmount) > abs(amount):
            openBaseAmount = openBaseAmount * ( 1 + amount / previousTotalAmount)
        else:
            openBaseAmount = baseAmount * ( 1 + previousTotalAmount / amount)
        previousTotalAmount += amount

    return openBaseAmount + totalUpl

#-------------------------------------------------------------------------
def CalculateAmountAndBaseAmount(journals):
    amount = 0
    baseAmount = 0

    for journal in journals:
        amount += journal.Amount()
        baseAmount += journal.BaseAmount()

    return amount, baseAmount