"""Confirmation report generator for bond trades.

This script is invoked by calling the homonymous ASQL query.
"""

# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    Aaeda Salejee    Ickin Vural            C000000697493, ABITFA-569
# Decommission platypus and move all existing reports using it to FOP

# OPS    Sipho Ndlalane   Lukas Paluzga          ABITFA-1269
# Refactored to use common base.

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS Sipho Ndlalane	Sanele Macanda		CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions



import os, time
import acm, ael

import at, SACM_Trade_Confirmation_PDF as stc
from zak_funcs import formcurr
from XMLReport import mkcaption, mkinfo, mkvalues
from SAGEN_IT_Functions import startFile


class ReturnConfirmationReport(stc.Report):
    def _clean(self):
        return self.instrument_ael.clean_from_yield(self.valday_ael, None, None, self.trade_ael.price)

    def _dirty(self):
        return self.instrument_ael.dirty_from_yield(self.valday_ael, None, None, self.trade_ael.price)
        
    def _stockDes(self):
        instrument = self.trade.Instrument()
        expiry_year = at.date_to_datetime(instrument.ExpiryDate()).year
        return '{0}   {1}%   {2}'.format(instrument.Name(), round(instrument.Legs()[0].FixedRate(), 3), expiry_year)

    def _cleanPrice(self):
        cp = self._clean() * (self.trade_ael.nominal_amount(self.valday_ael)) / 100
        return abs(cp)

    def _accInterest(self):
        accint = (self._dirty() - self._clean()) / 100 * self.trade_ael.nominal_amount(self.valday_ael)
        return abs(accint)

    def _noOfDays(self):
        days = 0

        leg = self.instrument_ael.legs()[0]
        for cf in leg.cash_flows():
            try:
                if cf.pay_day >= self.valday_ael and cf.start_day <= self.valday_ael and cf.start_day != None and cf.type == 'Fixed Rate':
                    if self._dirty() > self._clean():
                        days = cf.start_day.days_between(self.valday_ael, leg.daycount_method)
                    else:
                        days = self.valday_ael.days_between(cf.ex_coupon_date(), leg.daycount_method)
            except:
                pass

        return days

    def statement_detail(self):
        yield mkcaption('GILT TRANSACTION ADVICE NOTE')
        
        cum_or_ex = 'CUM' if self._dirty() > self._clean() else 'Ex'
        if self.trade.Bought():
            yield mkinfo("We confirm having BOUGHT the following stock from You FOR {0} DAYS {1}".format(self._noOfDays(), cum_or_ex))
        else:
            yield mkinfo("We confirm having SOLD the following stock to You FOR {0} DAYS {1}".format(self._noOfDays(), cum_or_ex))
        
        yield mkvalues(
            ("DEAL REFERENCE:", self.trade.Name()),
            ("COUNTERPARTY REF:", self.trade.Counterparty().Name()),
            ("NUTRON CODE:", self.trade.Counterparty().HostId()),
            ("UNEXCOR CODE:", self.unexCor()),
            ("DEALER CODE:", self.trade.Trader().Name()),
            ("STOCK DESCRIPTION:", self._stockDes()),
            ("DEAL DATE:", time.strftime('%d/%m/%Y %H:%M:%S ', time.localtime(self.trade_ael.time))),
            ("SETTLEMENT DATE:", self.trade.ValueDay()),
            ("YIELD TO MATURITY:", str(round(self.trade.Price(), 5)) + "%"),
            ("NOMINAL VALUE:", formcurr(abs(self.trade_ael.nominal_amount(self.valday_ael)))), 
            ("CLEAN PRICE:", formcurr(self._cleanPrice())),
            ("CONSIDERATION:", formcurr(abs(self.trade_ael.premium))),
            ("ACCRUED INTEREST:", formcurr(self._accInterest())))

ael_gui_parameters = {'windowCaption':'Bond Confirmation'}

def getCounterparty():
    counterparty = []
    for t in ael.Party.select():
        if t.type in ['Counterparty', 'Broker', 'Client']:
            counterparty.append(t.ptyid)
    counterparty.sort()
    return counterparty

ael_variables = stc.get_ael_variables(
    'Y:/Jhb/Ops CM/Capital Markets Confirmations/Bonds Confirmations/',
    [['Counterparty', 'Counterparty', 'string', getCounterparty(), 'ALL', 0, 0, 'To run for a counterparty', None, 1]])

def ael_main(parameters):
    counterparty = parameters['Counterparty']
    trade_numbers = stc.parse_trade_numbers(parameters['TradeNumber'])

    #  TradeNumbers & Counterparty result matrix:
    #
    #  Trdnbrs\CPTY     None      All     CPTY
    #  None             none      All     CPTY
    #  T                T         T       none

    # Get trade numbers
    if trade_numbers:
        if counterparty and counterparty.upper() != 'ALL':
            trade_numbers = []
    else:
        party = acm.FParty[counterparty]
        if party:
            trades = acm.FTrade.Select('counterparty={0}'.format(party.Oid()))
            trade_numbers = [t.Oid() for t in trades]
        else:
            acm.Log('Invalid Counterparty!')

    # Generate the reports
    if trade_numbers:
        supported_instypes = [at.INST_BOND, at.INST_INDEXLINKED_BOND, at.INST_ZERO]
        rep_params = stc.prep_reporter_args('Bonds', ReturnConfirmationReport, supported_instypes, parameters)
        reporter = stc.Reporter(rep_params)

        output_file_name = reporter.create_reports(trade_numbers)
        startFile(output_file_name)

def ASQL(*rest):
    acm.RunModuleWithParameters('SACM_Bond_Confirmation_PDF', 'Standard') #@UndefinedVariable
    return 'SUCCESS'
