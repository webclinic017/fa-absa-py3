"""
The purpose of PriceKeeper is to move SPOT prices to be available at the start of a business day.
PriceKeeper also copies SPOT prices to be SPOT_SOB along with spread copy for some Yield Curves.

Please update if required:
http://confluence.barcapint.com/display/ABCAPFA/PriceKeeper

Date              JIRA               Developer               Reporter
==========        ===========        =============           =================
2014-09-24        ABITFA-3061        Pavel Saparov           Anwar Banoo
2015-06-24        ABITFA-3061        Andrei Conicov           Anwar Banoo
"""
import ael
import acm

from itertools import ifilter
from at_ael_variables import AelVariableHandler
import datetime


class PriceKeeper(object):

    # logging information messages
    info = []

    # logging errors
    errors = []
    
    def __init__(self, dry_run=False, verbose=False, fix_spot_sob=False, yield_curves=[]):
        """Init method.

        Args:
            dry_run: A switch to indicate test run.
        """

        self.yield_curves = yield_curves
        self.dry_run = dry_run
        self.verbose = verbose
        self.fix_spot_sob = fix_spot_sob

        self.today = acm.Time.DateToday()
        self.yesterday = acm.Time.DateAdjustPeriod(self.today, '-1d')
        self.spot_market = acm.FParty['SPOT']
        self.spot_besa_market = acm.FParty['SPOT_BESA']
        calendar = acm.FCurrency['ZAR'].Calendar()
        self.prev_day = calendar.AdjustBankingDays(self.today, -1)

    @staticmethod
    def latest_spot_sob(instrument, currency):
        """Return SPOT_SOB price or None for given instrument and currency"""

        return next(ifilter(lambda p: p.Market().Name() == 'SPOT_SOB' and p.Currency() == currency,
            instrument.Prices()), None)

    @staticmethod
    def format_price(price):
        if price.Bid() == price.Ask() == price.Last() == price.Settle():
            return "Bid = Ask = Last = Settle: {0:.4f}".format(price.Settle())
        else:
            return "Bid = {0:.4f}, Ask = {1:.4f}, Last = {2:.4f}, Settle = {3:.4f}".format(
                price.Bid(), price.Ask(), price.Last(), price.Settle())

    def _process_error(self, msg):
        acm.Log(msg)
        self.errors.append(msg)

    def _process_info(self, msg):
        acm.Log(msg)
        self.info.append(msg)


    def copy_spot(self, instrument):
        """Method will always copy yesterday's SPOT prices to be
        today's SPOT for multiple currencies"""

        for price in instrument.Prices():
            if price.Market() and price.Market() == self.spot_market:

                # if SPOT price date is today, use yesterday's SPOT
                if price.Day() == self.today:
                    if self.verbose:
                        msg = "Warning: {0} {1} price with values {2} already exists".format(
                                instrument.Name(),
                                price.Market().Name(),
                                self.format_price(price))
                        self._process_info(msg)
                # update SPOT price with today's date
                elif price.Day() < self.today:
                    new_spot = price.Clone()
                    new_spot.Day(self.today)
                    self.update_price(price, new_spot)

    def copy_spot_sob(self, instrument):
        """Method will always copy previous business day
        SPOT price to be today's SPOT_SOB for multiple currencies"""
        
        prev_spot_prices = acm.FPrice.Select(
            'instrument = {0} and market = {1} and day = {2}'.format(
            instrument.Oid(), self.spot_market.Oid(), self.prev_day
        ))

        for prev_spot in prev_spot_prices:
            # if an instrument has SPOT_SOB prices update
            # them with previous business day SPOT
            spot_sob = self.latest_spot_sob(instrument, prev_spot.Currency())

            if spot_sob and spot_sob.Currency() != prev_spot.Currency():
                continue

            if spot_sob and spot_sob.Day() != self.today:
                prev_spot = ael.Price[prev_spot.Oid()]
                new_spot_sob = spot_sob.Clone()
                new_spot_sob.Ask(prev_spot.ask)
                new_spot_sob.Bid(prev_spot.bid)
                new_spot_sob.Last(prev_spot.last)
                new_spot_sob.Settle(prev_spot.settle)
                new_spot_sob.Day(self.today)
                self.update_price(spot_sob, new_spot_sob)

            # if an instrument doesn't have SPOT_SOB, create it
            elif spot_sob is None:
                new_spot_sob = acm.FPrice()
                new_spot_sob.Apply(prev_spot)
                new_spot_sob.Market('SPOT_SOB')
                new_spot_sob.Day(self.today)
                self.update_price(None, new_spot_sob)

    def copy_spot_besa(self, instrument):
        """Method will copy yesterday's SPOT_BESA prices to be same for today."""
        
        for price in instrument.Prices():
            if price.Market() and price.Market() == self.spot_besa_market:

                # create new SPOT_BESA price
                if price.Day() <= self.yesterday:
                    new_spot_besa = price.Clone()
                    new_spot_besa.Day(self.today)
                    self.update_price(price, new_spot_besa)

    def update_price(self, old_price, new_price):
        """Method will commit 'new_price' using 'old_price' as a reference.
        !Have to overwrite the old price, otherwise will not work.

        Arguments:
            old_price: original acm.FPrice object or None
            new_price: newly created or update acm.FPrice object ready for commit
        """
 
        if new_price.IsKindOf(acm.FPrice):
            try:
                instrument = new_price.Instrument()
                if old_price is None or not old_price.IsKindOf(acm.FPrice):
                    if not self.dry_run:
                        new_price.Commit()
                    if self.verbose:
                        msg = "INFO: {0} {1} price with values {2} created".format(
                                instrument.Name(),
                                new_price.Market().Name(),
                                self.format_price(new_price))
                        self._process_info(msg)
                else:
                    if old_price.Day() != self.today:
                        old_price.Apply(new_price)
                        
                        if not self.dry_run:
                            old_price.Commit()
                        if self.verbose:
                            msg = "INFO: {0} {1} price with values {2} updated".format(
                                    instrument.Name(),
                                    new_price.Market().Name(),
                                    self.format_price(new_price))
                            self._process_info(msg)
                    else:
                        if self.verbose:
                            msg = "INFO: {0} price for {1} already exists for today." \
                              "No update was done.".format(
                                    new_price.Market().Name(),
                                    instrument.Name())
                            self._process_info(msg)
                            
            except RuntimeError as e:
                msg = "ERROR: {0}".format(e)
                msg += "Unable to commit price update."
                self._process_error(msg)

    def copy_yield_curves(self):
        """Method will copy Yield Curve spreads to their equivalent SOB curve."""
        
        for yield_curve in self.yield_curves:
            spreads = {}
            sob_yield_curve = acm.FYieldCurve['{0}-SOB'.format(yield_curve.Name())]

            # populate 'spreads' dict where key is a date period and value is a spread
            for pt in yield_curve.Points():
                period = pt.DatePeriod()
                spread = acm.FYCSpread.Select01("point = '{0}'".format(pt.Oid()),
                                                "multiple found")
                if spread:
                    spreads[period] = spread.Spread()

            # updated spreads for SOB Yield Curve
            for pt in sob_yield_curve.Points():
                period = pt.DatePeriod()
                spread = acm.FYCSpread.Select01("point = '{0}'".format(pt.Oid()),
                                                "multiple found")
                try:
                    if (spread is not None and period in spreads):
                        spread.Spread(spreads[period])
                        if not self.dry_run:
                            spread.Commit()
                        if self.verbose:
                            msg = "INFO: Updated {0} curve for a '{1}' period".format(
                                sob_yield_curve.Name(), period)
                            self._process_info(msg)
                except RuntimeError as e:
                    msg = "ERROR: {0}".format(e)
                    msg += "Unable to update {0} curve for a '{1}' period".format(
                                sob_yield_curve.Name(), period)
                    self._process_error(msg)

    def update_matured_spot_sob(self, instrument):
        """ Make sure that the the maturity SPOT_SOB price is the same as the SPOT price"""

        spot_market = acm.FParty['SPOT']
        day = instrument.maturity_date()
        prev_spot_prices = acm.FPrice.Select(
            'instrument = {0} and market = {1} and day = {2}'.format(
            instrument.Oid(), spot_market.Oid(), day
        ))

        for prev_spot in prev_spot_prices:
            # if an instrument has SPOT_SOB prices update
            # them with previous business day SPOT
            spot_sob = self.latest_spot_sob(instrument, prev_spot.Currency())

            if (not spot_sob
                or (spot_sob and spot_sob.Currency() != prev_spot.Currency())
                or spot_sob.Day() != day):
                continue

            if (prev_spot.Ask() != spot_sob.Ask()
                or prev_spot.Bid() != spot_sob.Bid()
                or prev_spot.Last() != spot_sob.Last()
                or prev_spot.Settle() != spot_sob.Settle()):

                msg = ("Warning: {0} has matured but the SPOT_SOB price does not match the SPOT price and will be updated '{1}'. ").format(
                                instrument.Name(), instrument.maturity_date())
                self._process_info(msg)

                prev_spot = ael.Price[prev_spot.Oid()]
                new_spot_sob = spot_sob.Clone()
                new_spot_sob.Ask(prev_spot.ask)
                new_spot_sob.Bid(prev_spot.bid)
                new_spot_sob.Last(prev_spot.last)
                new_spot_sob.Settle(prev_spot.settle)
                new_spot_sob.Day(day)
                self.update_price(spot_sob, new_spot_sob)
    
    def run(self):
        """Copy prices and yield curve spreads."""

        acm.Log("Starting PriceKeeper")
        if self.dry_run:
            acm.Log("Info: !Running in dry mode")

        query = acm.CreateFASQLQuery('FInstrument', 'OR')
        query.AddAttrNode('generic', 'Equal', True)
        query.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', self.today)
        query.AddAttrNode('ExpiryDate', 'EQUAL', acm.Time().AsDate('2007-01-01'))
        query.AddAttrNode('ExpiryDate', 'EQUAL', acm.Time().AsDate('9999-12-31'))
        query.AddAttrNode('ExpiryDate', 'EQUAL', None)
        query.AddAttrNode('ExpiryDate', 'LESS_EQUAL', acm.Time().AsDate('0001-01-01')) # searching for items with date 0000-01-01

        instruments = query.Select()
        
        for instrument in instruments:
            
            ignore_expiry_date = acm.Time.AsDate(instrument.ExpiryDate()) in ('0000-01-01', '9999-12-31', '2007-01-01')
            if ignore_expiry_date:
                msg = "Warning: {0} has a strange expiry date '{1}'. ".format(
                            instrument.Name(), instrument.maturity_date())
                self._process_info(msg)
            # the expiry date is not always the maturity date, it depends on the instrument type
            if instrument.maturity_date() >= self.today or ignore_expiry_date:
                
                # Checking PS_IntFut_PK_ex() is time consuming and I could not find any entry in the add_info table for specnbr 991
                self.copy_spot(instrument)
                self.copy_spot_sob(instrument)
                self.copy_spot_besa(instrument)
            else:
                if self.fix_spot_sob or instrument.maturity_date() == self.yesterday:
                    self.update_matured_spot_sob(instrument)
                msg = ("Warning: {0} has already matured '{1}'. "
                       "The SPOT, SPOT_SOB and SPOT_BESA prices are not copied.").format(
                            instrument.Name(), instrument.maturity_date())
                self._process_info(msg)

        self.copy_yield_curves()

        if len(self.errors) > 0:
            acm.Log("Completed with errors:")
        else:
            acm.Log("Completed successfully")


ael_variables = AelVariableHandler()

ael_variables.add_bool(
    "dry_run",
    label="Dry run",
    alt="Prices won't be published to Price Entry. For testing purposes only."
)

ael_variables.add_bool(
    "verbose",
    label="Verbose",
    alt="Information message will be output to log."
)

ael_variables.add_bool(
    "fix_spot_sob",
    label="Fix SPOT-SOB at maturity",
    alt="Fix SPOT_SOB prices to match SPOT prices at maturity .",
    default=False
)

ael_variables.add(
    "yield_curves",
    label="Yield Curves",
    alt="Copy selected Yield Curves to -SOB",
    cls=acm.FYieldCurve,
    multiple=True
)


def ael_main(params):
    """Main loop"""

    price_keeper = PriceKeeper(**params)
    print("Verbose: {0}".format(price_keeper.verbose))
    price_keeper.run()

