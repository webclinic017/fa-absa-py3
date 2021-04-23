import acm
from at import TP_SWAP_NEAR_LEG, TP_SWAP_FAR_LEG
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

class AutoRollBooking:
    def __init__(self, acquirer, counter_party, portfolio, mirror_port, status, amount, currency, currency_pair, value_date, far_val_date, rollBackSpec = None):
        self.acquirer = acquirer
        self.counter_party = counter_party
        self.portfolio = portfolio
        self.mirror_port = mirror_port
        self.status = status
        self.amount = amount
        self.currency_pair = currency_pair
        self.value_date = value_date or {}
        self.far_val_date = far_val_date
        self.currency = currency

    def get_forward_rate(self, currencyPair, forwardDate):
        curr1 = currencyPair.Currency1()
        curr2 = currencyPair.Currency2()
        spaceCollection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        forwardRate = curr1.Calculation().FXRate(spaceCollection, curr2, forwardDate) 
        return forwardRate.Number()

    def create_swap_roll_trade(self):
        if abs(round(self.amount, 2)) <= 0.00:
            Logme()('INFO: Received currency %s with an amount of %s. Will not book this trade' %(self.currency, self.amount), 'INFO')
            return
        
        near = acm.FTrade()
        near.RegisterInStorage()
        near.TradeTime(acm.Time.TimeNow())
        near.AcquireDay(self.value_date)
        near.ValueDay(near.AcquireDay())
        near.Instrument(self.currency_pair.Currency1())
        near.Currency(self.currency_pair.Currency2())
        near.Acquirer(self.acquirer)
        near.Counterparty(self.counter_party)
        near.Portfolio(self.portfolio)
        near.Price(self.get_forward_rate(self.currency_pair, self.value_date))
        
        if abs(round(near.Price(), 2)) == 0.00:
            Logme()('INFO: Retrieved a price of 0. Will not book this trade.', 'INFO')
            return
        
        near.ReferencePrice(self.get_forward_rate(self.currency_pair, self.currency_pair.SpotDate(acm.Time.DateNow())))
        if acm.User().Name() == 'ATS':
            near.Trader(acm.FUser['HEWITTEN'])
        else:
            near.Trader(acm.User())
        
        if self.currency in self.currency_pair.Currency1().Name():
            near.Quantity(self.amount)
            if abs(round(near.Quantity() * near.Price(), 2)) <= 0.00:
                Logme()('INFO: Currency %s with amount %s will result in a FX amount of %s. Will not book this trade.' %(self.currency, self.amount, near.Quantity() * near.Price()), 'INFO')
                return
        else:
            near.Premium(self.amount)
            near.QuantityIsDerived(True)
            if abs(round(near.Premium() / near.Price(), 2)) <= 0.00:
                Logme()('INFO: Currency %s with amount %s will result in a FX amount of %s. Will not book this trade.' %(self.currency, self.amount, near.Premium() / near.Price()), 'INFO')
                return
        
        near.UpdatePremium(True)
        near.TradeProcess(TP_SWAP_NEAR_LEG)
        near.Status(self.status)
        near.Type("Spot Roll")
        near.DiscountingType('CCYBasis')
        near.MirrorPortfolio(self.mirror_port)

        #--------------------------------------------------------------------

        far = acm.FTrade()
        far.RegisterInStorage()
        far.TradeTime(acm.Time.TimeNow())
        far.AcquireDay(self.far_val_date)                                 
        far.ValueDay(far.AcquireDay())
        far.Instrument(near.Instrument())
        far.Currency(near.Currency())
        far.Acquirer(near.Acquirer())
        far.Counterparty(near.Counterparty())
        far.Portfolio(near.Portfolio())
        far.Price(self.get_forward_rate(self.currency_pair, self.far_val_date))
        far.ReferencePrice(self.get_forward_rate(self.currency_pair, self.currency_pair.SpotDate(acm.Time.DateNow())))
        far.Trader(near.Trader())
        if self.currency in self.currency_pair.Currency1().Name():
            far.Quantity(-near.Quantity())
        else:
            far.Premium(-near.Premium())
            far.QuantityIsDerived(True)
        far.UpdatePremium(True)
        far.TradeProcess(TP_SWAP_FAR_LEG)
        far.Status(self.status)
        far.Type("Spot Roll")
        far.DiscountingType('CCYBasis')
        far.MirrorPortfolio(self.mirror_port)

        #--------------------------------------------------------------------

        far.ConnectedTrade(near)
        near.FxSwapFarLeg()         
        near.ConnectedTrade(far)

        #--------------------------------------------------------------------

        def commit_in_transaction(self, near, far):
            acm.BeginTransaction()
            try:
                near.Commit()
                far.Commit()
                acm.CommitTransaction()
                Summary().ok(near, Summary().CREATE, near.Oid())
                Summary().ok(near.TrueMirror(), Summary().CREATE, near.TrueMirror().Oid())
                Summary().ok(far, Summary().CREATE, far.Oid())
                Summary().ok(far.TrueMirror(), Summary().CREATE, far.TrueMirror().Oid())
            except Exception, e:
                Logme()('ERROR: Abort Transaction %s' %str(e), 'ERROR')
                acm.AbortTransaction()

        commit_in_transaction(self, near, far)
        Logme()('INFO: Near Trade: %s \t Far Trade: %s' %(near.Oid(), far.Oid()), 'INFO')
        Logme()('INFO: Near Mirror Trade: %s \t Far Mirror Trade: %s' %(near.TrueMirror().Oid(), far.TrueMirror().Oid()), 'INFO')

#from FX_AUTOROLL_PARAMETERS import AUTOROLL_PARAMETERS
#param = AUTOROLL_PARAMETERS('FX_AUTOROLL_ACX')
#create_trade = AutoRollBooking("ABSA CAPITAL", "TEST", "RND", "FWT", "FO Confirmed", 115000.26, 'INR', acm.FCurrencyPair['USD/INR'], '2017-11-08', '2017-11-09')
#print create_trade.get_forward_rate(acm.FCurrencyPair['USD/ZAR'], '2017-10-18')
#create_trade.create_swap_roll_trade()
