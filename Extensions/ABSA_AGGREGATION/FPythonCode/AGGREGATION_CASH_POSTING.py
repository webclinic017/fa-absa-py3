'''----------------------------------------------------------------------
History:
Date       CR Number     Who                    What
2019-03-22 CHG1001539200 Tibor Reiss            Update and refactor to enable PS aggregation
----------------------------------------------------------------------'''
import acm
import at_addInfo
from FBDPCurrentContext import Logme
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS
from AGGREGATION_PARAMETERS import PARAMETERS


class CASH_POSTING():
    def __init__(self, fInstrument, fCounterparty, fAcquirer, fTrader, fPortfolio, status, date, fCurrency):
        self.__cashPostingTrade = None
        self.__instrument = fInstrument
        self.__counterparty = fCounterparty
        self.__acquirer = fAcquirer
        self.__trader = fTrader
        self.__portfolio = fPortfolio
        self.__quantity = 0
        self.__status = status
        self.__currency = fCurrency
        self.__date = date
        self.__type = 'Cash Posting'
        self.__aggregate = 2
        self.__helpers = GENERIC_HELPERS()
        self.__createCashPostingSuccess = False
        self.__createPaymentSuccess = False
        self.__payments = []
        
    def createTrade(self):
        if not self.__cashPostingTrade:
            self.__cashPostingTrade = acm.FTrade()
            self.__cashPostingTrade.Instrument(self.__instrument)
            self.__cashPostingTrade.Counterparty(self.__counterparty)
            self.__cashPostingTrade.Acquirer(self.__acquirer)
            self.__cashPostingTrade.Trader(self.__trader)
            self.__cashPostingTrade.Portfolio(self.__portfolio)
            self.__cashPostingTrade.Type(self.__type)
            self.__cashPostingTrade.Quantity(self.__quantity)
            self.__cashPostingTrade.Status(self.__status)
            self.__cashPostingTrade.Currency(self.__currency)
            self.__cashPostingTrade.TradeTime(self.__date)
            self.__cashPostingTrade.AcquireDay(self.__date)
            self.__cashPostingTrade.ValueDay(self.__date)
            self.__cashPostingTrade.Aggregate(self.__aggregate)

            #Setting additional info values
            for addInfo in PARAMETERS.tradeAdditionalInfos:
                addInfoPath = addInfo[0].split('.')
                addInfoName = addInfoPath[len(addInfoPath) - 1]
                addInfoValue = addInfo[1]
                if addInfoValue not in (None, ''):
                    self.__cashPostingTrade.AdditionalInfo().GetPropertyObject(addInfoName).Set(addInfoValue)
                    self.__helpers.addToSummary('Trade Additional Info', 'Create', 1)

            try:
                self.__cashPostingTrade.RegisterInStorage()
            except Exception as e:
                msg = 'Error during creating cash posting trade. {0}'.format(e)
                raise RuntimeError(msg)
        else:
            Logme()('WARNING: Cash Posting trade already exists: %i. '
                    'Did not create another cash posting trade.' %
                    self.__cashPostingTrade.Oid(), 'WARNING')

    def createTradeAddInfo(self, addInfoName, value):
        if self.__cashPostingTrade:
            try:
                at_addInfo.save(self.__cashPostingTrade, addInfoName, value)
                self.__helpers.addToSummary('Trade Additional Info', 'Create', 1)
            except Exception as e:
                Logme()('ERROR: Aborting Transaction: creating trade additional info '
                        '%s with value %s. %s' % (addInfoName, value, str(e)), 'ERROR')
        else:
            Logme()('WARNING: Cash Posting trade does not exists: '
                    'Did not create an additional info.', 'WARNING')
            
    def createPayment(self, payType, payAmount, payCurr, payDay, party=None):
        if self.__cashPostingTrade:
            payment = acm.FPayment()
            payment.Type(payType)
            payment.Trade(self.__cashPostingTrade)
            payment.Amount(payAmount)
            payment.Currency(acm.FCurrency[payCurr])
            payment.Party(party if party else self.__counterparty)
            payment.ValidFrom(payDay)
            payment.PayDay(payDay)
            try:
                payment.RegisterInStorage()
                self.__payments.append(payment)
            except Exception as e:
                Logme()('ERROR: Could not create payment %s %s %s %s: %s' %
                        (payType, payAmount, payCurr, payDay, str(e)), 'ERROR')
                raise e
        else:
            msg = 'Cash Posting trade does not exists, did not create payment.'
            raise RuntimeError(msg)

    def commit(self):
        acm.BeginTransaction()
        try:
            self.__cashPostingTrade.Commit()
            for p in self.__payments:
                p.Commit()
            acm.CommitTransaction()
            self.__helpers.addToSummary('Trade', 'Create', 1)
            self.__createCashPostingSuccess = True
            self.__helpers.addToSummary('Additional Payment', 'Create', len(self.__payments))
            self.__createPaymentSuccess = True
            Logme()('INFO: Created Cash Posting trade: %i.' % self.__cashPostingTrade.Oid(), 'INFO')
            return self.__cashPostingTrade.Oid()
        except Exception as e:
            acm.AbortTransaction()
            Logme()('ERROR: Aborting commit!')
            raise e

    def updateTrade(self, keyValuePairs):
        if self.__cashPostingTrade:
            for attribute in keyValuePairs.keys():
                self.__cashPostingTrade.SetProperty(attribute, keyValuePairs[attribute])
            try:
                self.__cashPostingTrade.Commit()
            except Exception as e:
                Logme()('ERROR: Aborting updating trade %s' % str(e), 'ERROR')
                raise e
        else:
            Logme()('WARNING: Cash Posting trade does not exists: Did not update any trade.', 'WARNING')

    def getCashPostingTrade(self):
        return self.__cashPostingTrade

    def getCreateCashPostingSuccess(self):
        return self.__createCashPostingSuccess
        
    def getCreatePaymentSuccess(self):
        return self.__createPaymentSuccess
