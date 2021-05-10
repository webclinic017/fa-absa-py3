""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendCorpActionHandler.py"

"""----------------------------------------------------------------------------
MODULE
    FSecLendCorpActionHandler

DESCRIPTION

Corporate Action Election Handler for Security Loans
----------------------------------------------------------------------------"""
import acm
from FCorpActionElectionHandler import IHandler
import FCorpActionRounding


class SecurityLoanHandler(IHandler):
    
    def __init__(self, context):
        self._context = context
        self._mainTrd = None
        
    def Instrument(self):
        return acm.FBusinessLogicDecorator.WrapObject(self.MainTrade().Instrument())
        
    def FirstLeg(self):
        return self.Instrument().Legs().First()

    def MainTrade(self):
        if self._mainTrd is None:
            self._mainTrd = self._context.Position().Trades().First().Contract()
        return self._mainTrd
        
    def GenerateCashFlows(self, instrument):
        for leg in instrument.Legs():
            leg.GenerateCashFlows(0)
        
    def AdjustTrade(self):
        import FSecLendDealUtils
        mainTrdWrapper = FSecLendDealUtils.SecurityLoanWrapper.Wrap(self.MainTrade())
        adjustTrdWrapper = mainTrdWrapper.CreateTradeActionTrade(self._context.Quantity(), 
                                                            self._context.ValueDay(), 
                                                            self._context.TradeTime(),
                                                            'Simulated')
        adjustTrade = adjustTrdWrapper.Trade().DecoratedObject()
        adjustTrade.Type('Corporate Action')
        self.GenerateCashFlows(adjustTrade.Instrument())
        return adjustTrade
        
    def ClosePosition(self, result):
        adjustTrade = self.AdjustTrade()
        result.append(adjustTrade) 

    def AdjustPosition(self, result):
        adjustTrade = self.AdjustTrade()
        result.append(adjustTrade)

    def OpenPosition(self, result):
        import FSecLendDealUtils
        insAttributes = {'underlying': self._context.NewInstrument(),
                        'rollingPeriod': self.FirstLeg().RollingPeriod(),
                        'openEnd': self.Instrument().OpenEnd(),
                        'noticePeriod': self.Instrument().NoticePeriod(),
                        'dayCountMethod': self.FirstLeg().DayCountMethod(),
                        'legStartPeriod': self.Instrument().LegStartPeriod(),
                        'legEndPeriod': self.Instrument().LegEndPeriod(),
                        'nominalFactor': self.FirstLeg().NominalFactor(),
                        'dividendFactor': self.Instrument().DividendFactor(),
                        'spotDays': self.Instrument().SpotBankingDaysOffset(),
                        'fixedPrice': True if self.FirstLeg().NominalScaling() == 'Initial Price' else False,
                        'currency': self.Instrument().Currency()}
        
        tradeAttributes = {'quantity': FCorpActionRounding.RoundQuantity(self._context.Quantity(), 0),
                          'acquirer': self.MainTrade().Acquirer(),
                          'portfolio': self.MainTrade().Portfolio(),
                          'counterparty': self.MainTrade().Counterparty(),
                          'source': self.MainTrade().Market()}

        slc = FSecLendDealUtils.SecurityLoanCreator()
        ins = slc.CreateInstrument(**insAttributes)
        trade = slc.CreateTrade(ins, **tradeAttributes)
        tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(trade)
        tradeDecorator.TradeTime(self._context.TradeTime())
        tradeDecorator.ValueDay(self._context.ValueDay())
        tradeDecorator.Type('Corporate Action')
        result.append(ins)
        result.append(trade)

