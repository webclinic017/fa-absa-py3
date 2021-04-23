""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/BDP/FCloseOpenSecurityLoanPerform.py"
"""----------------------------------------------------------------------------
MODULE
    FCloseOpenSecurityLoanPerform - Module which performs the bulk editing of Sec Loans

DESCRIPTION


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import ael
import acm
import FBDPCommon
import FBDPRollback
from FTransactionHandler import RollbackHandler
from FSecLendUtils import GetSecurityLoanRate, SetSecurityLoanRate

from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme

def perform(dictionary):
    Logme()('Security Loan Bulk Edit 4.33.1')
    day = FBDPCommon.toDate(dictionary['date'])
    Logme()('Security Loan Bulk Edit date:%s' % str(day))
    runner = FCloseOpenSecurityLoanPerform()
    runner.performProcess(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')

class FCloseOpenSecurityLoanPerform():
    
    def readArguments(self, args):
        self.date = FBDPCommon.toDate(args.get('date', acm.Time.DateToday()))
        self.trades = args.get('Trades', [])
        self.testmode = args.get('Testmode', 1)
        self.secloans = args.get('SecLoans', None)
        self.underlying = args.get('Underlying', None)
        self.divfactor = args.get('DivFactor', None)
        self.loanrate = args.get('LoanRate', None)
        self.term = args.get('Term', None)

    def performProcess(self, args):
        # Read GUI parameter selection
        self.readArguments(args)
        rollback = FBDPRollback.RollbackWrapper('CloseOpenSecLoan-' + str(self.date), 
                                bool(self.testmode))
        result = []
        for trade in self.trades:
            closeTrade = self.CloseSecLoan(trade)
            result.append(closeTrade)
            openTrade, openIns = self.OpenSecLoan(trade)
            result.append(openIns)
            result.append(openTrade)
        transHandler = RollbackHandler(rollback)
        with transHandler.Transaction():
            transHandler.AddAll(result)
        
    
    def OpenSecLoan(self, trade):
        Logme()('SecurityLoanHandler--OpenPosition', 'INFO')
        import FSecLendDealUtils
        underlying = trade.Instrument().Underlying()
        if self.underlying:
            underlying = self.underlying[0]
        divfactor = self.divfactor if self.divfactor else trade.Instrument().DividendFactor()
        loanrate = self.loanrate if self.loanrate else GetSecurityLoanRate(trade)
        firstleg = trade.Instrument().Legs().First()
        instrument = acm.FBusinessLogicDecorator.WrapObject(trade.Instrument())
        insAttributes = {'underlying': underlying,
                        'rollingPeriod': firstleg.RollingPeriod(),
                        'openEnd': instrument.OpenEnd(),
                        'noticePeriod': instrument.NoticePeriod(),
                        'dayCountMethod': firstleg.DayCountMethod(),
                        'legStartPeriod': instrument.LegStartPeriod(),
                        'legEndPeriod': instrument.LegEndPeriod(),
                        'nominalFactor': firstleg.NominalFactor(),
                        'dividendFactor': divfactor,
                        'spotDays': instrument.SpotBankingDaysOffset(),
                        'fixedPrice': True if firstleg.NominalScaling() == 'Initial Price' else False,
                        'currency': instrument.Currency()}
        
        tradeAttributes = {'quantity': trade.Quantity(),
                          'acquirer': trade.Acquirer(),
                          'portfolio': trade.Portfolio(),
                          'counterparty': trade.Counterparty(),
                          #'source': trade.Market(),
                          'slAccount' : trade.AdditionalInfo().SL_Account(),
                          'collateralAgreement' : trade.AdditionalInfo().CollateralAgreement()}

        slc = FSecLendDealUtils.SecurityLoanCreator()
        ins = slc.CreateInstrument(**insAttributes)
        newtrade = slc.CreateTrade(ins, **tradeAttributes)
        SetSecurityLoanRate(newtrade, loanrate)
        tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(newtrade)
        tradeDecorator.TradeTime(self.date)
        tradeDecorator.ValueDay(self.date)
        tradeDecorator.Type('Normal')
        tradeDecorator.Market(None)
        newtrade = self.UpdateSecLoanTrade(newtrade)
        newins = self.UpdateSecLoanInstrument(ins)
        return newtrade, newins
    
    def CloseSecLoan(self, trade):
        return self.AdjustTrade(trade, -1.0 * trade.Quantity(), 'Closing')
        
    def AdjustTrade(self, trade, quantity, tradeType):
        mainTrade = trade
        if mainTrade == None:
            print('Maintrade is None')
            return None
        
        import FSecLendDealUtils
        mainTrdWrapper = FSecLendDealUtils.SecurityLoanWrapper.Wrap(trade.Contract())
        print(mainTrdWrapper)
        adjustTrade = mainTrdWrapper.CreateAdjustTrade(quantity, 
                                                            self.date, 
                                                            self.date,
                                                            'Simulated')
        adjustTrade.Type(tradeType)
        adjustTrade.Market(None)
        self.GenerateCashFlows(adjustTrade.Instrument())
        return adjustTrade
    
    def GenerateCashFlows(self, instrument):
        for leg in instrument.Legs():
            leg.GenerateCashFlows(0)

    def UpdateSecLoanTrade(self, trade):
        #update further properties or additional infos here
        return trade
    
    def UpdateSecLoanInstrument(self, ins):
        #update further properties or additional infos here
        return ins 

