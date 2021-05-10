import acm, ael
import ABSAPortfolioSwapUtil
'''
Date                    : 2011-01-27
Purpose                 : Custom Methods on FInstrument
Developer               : Rohan van der Walt
CR Number               : 581108
'''


def StrikeCurrencyCustom(self):
    # Logic for FCustomMethod StrikeCurrencyCustom
    if self.IsKindOf(acm.FOption):
        return self.StrikeCurrency()
    else:
        return None


def UsedPrice(self, date, curr='ZAR', market='SPOT'):
    '''
    Retrieves price for given date, curr and market.
    Market defaults to "SPOT"
    Currency defaults to "ZAR"

    This ACM function calls ael function used_price.
    '''

    aelIns = ael.Instrument[self.Name()]
    try:
        return aelIns.used_price(ael.date(date), curr, '', 0, market)
    except Exception, e:
        print "EXCEPTION: Could not find used price for", self.Name(), "in market", market
        print e
        return 0

def get_isin_undisin_name(self):
    """ Returns one of the following values, if the previous does not exist:
        1. ISIN
        2. UND ISIN
        3. Instrument name
    """
    if self.Isin() != '':
        return self.Isin()[0:12]
    if self.Underlying() and self.Underlying().Isin() != '':
        return self.Underlying().Isin()[0:12]
    return self.Name()

def get_is_settled(self, date):
    """ Returns true if the instrument is settled
        Repo/Reverse - start date
        Bonds - value date
    """
    if self.InsType() == 'Repo/Reverse':
        return self.StartDate() > date
    if self.InsType() == 'Bond':
        return self.StartDate() > date

def is_dividend_leg(leg):
    """Return true if the leg is a dividend leg. The leg is fixed and pay"""
    if leg.LegType() == 'Fixed' and leg.PayLeg():
        return True
    
    return False


def get_pswap_leg_description(leg):
    if ABSAPortfolioSwapUtil.LegIsMtm(leg, False):
        return "Mtm"
    if ABSAPortfolioSwapUtil.LegIsCallDeposit(leg, False):
        return "Acount"
    if ABSAPortfolioSwapUtil.LegIsDividend(leg, False):
        return "Dividend"
    
    #TODO this is defined in the task PS_Generate_*_SERVER
    returnLegIsPayLeg = True
    if ABSAPortfolioSwapUtil.LegIsMargin(leg, returnLegIsPayLeg, False):
        return "Margin"
    if ABSAPortfolioSwapUtil.LegIsExecutionFee(leg, not returnLegIsPayLeg, False):
        return "Execution Premium"
    
    if ABSAPortfolioSwapUtil.LegIsRepo(leg, returnLegIsPayLeg, False):
        return "Short Premium"
    
    # TODO this one is not defined
    if leg.LegType()=='Float':
        return "Financing leg"
    #if ABSAPortfolioSwapUtil.LegIsRepo(leg, not returnLegIsPayLeg, False):
    #    return "Overnight Premium"
    
    return "Unknown (Type: {0}, PayLeg: {1})".format(leg.LegType(), leg.PayLeg())

def CreateDividendLegs(pswap, returnLeg, financingLeg):
    """Creates the dividend leg """
    for leg in pswap.Legs():
        if is_dividend_leg(leg) and leg.IndexRef() == returnLeg.IndexRef():
            return [leg]
        
    leg = pswap.CreateLeg(True)  # dividend leg
    leg.PayLeg(True)  # not being set in the factory method
    leg.LegType('Fixed')
    leg.StartDate(pswap.StartDate())
    leg.EndDate(pswap.EndDate())
    leg.DayCountMethod('Act/365')
    leg.FixedRate(0)
    leg.PayCalendar(pswap.Currency().Calendar())
    leg.RollingPeriodBase(pswap.StartDate())
    leg.IndexRef(returnLeg.IndexRef())
    leg.CreditRef(returnLeg.IndexRef())
    leg.NominalScaling = "Dividend Position Total"
        
    leg.Commit()

    return [leg]


def instrument_expiry_comparator(left_ins, right_ins):
    """DynamicVectorPerRowObjectOrderingComparator for vector column."""
    left_expiry = left_ins.ExpiryDate()
    right_expiry = right_ins.ExpiryDate()
    if left_expiry < right_expiry:
        return -1
    if left_expiry > right_expiry:
        return 1
    return 0

