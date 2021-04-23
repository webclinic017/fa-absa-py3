"""Confirmation report generator for BuySellback and Repo/Reverse trades.

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


import os

import acm

import at, SACM_Trade_Confirmation_PDF as stc
from zak_funcs import formcurr
from XMLReport import mkcaption, mkvalues, mkinfo
from SAGEN_IT_Functions import startFile

class ReturnConfirmationReport(stc.Report):
    def statement_detail(self):
        instype = self.instrument_ael.instype
        ins_ael = self.instrument_ael;
        underlying_ael = ins_ael.und_insaddr

        # Caption
        if instype == at.INST_BUYSELLBACK:
            repo_type = 'BUY SELLBACK' if self.trade.Quantity() > 0 else 'SELL BUYBACK'
        elif instype == at.INST_REPO_REVERSE:
            repo_type = 'REVERSE REPO' if self.trade.Quantity() > 0 else 'REPO'

        yield mkcaption(repo_type + " ADVICE NOTE")
        
        # Info text
        yield mkinfo("We confirm the following " + repo_type + " with you.") 
        
        # Values -- prepare data
        if self.instrument_ael.instype == at.INST_BUYSELLBACK:
            nominal_value = abs(self.trade_ael.nominal_amount(self.valday_ael))
            yield_leg1 = self.trade.Price()
            yield_leg2 = self.instrument.RefPrice()
            clean_leg1 = underlying_ael.clean_from_yield(self.valday_ael, None, None, self.trade_ael.price)
            clean_leg2 = underlying_ael.clean_from_yield(ins_ael.exp_day, None, None, ins_ael.ref_price)
            premium2 = self.instrument_ael.ref_value * self.trade_ael.quantity
            interest = abs(ins_ael.ref_value * self.trade_ael.quantity)- abs(self.trade_ael.premium)
            repo_rate = self.instrument.Rate()
        elif self.instrument_ael.instype == at.INST_REPO_REVERSE:
            nominal_value = ins_ael.ref_value * self.trade_ael.quantity
            yield_leg1 = self.instrument.RefPrice()
            yield_leg2 = 0.0
            clean_leg1 = underlying_ael.clean_from_yield(self.valday_ael, None, None, ins_ael.ref_price)
            clean_leg2 = 0.0
            premium2 = 0.0
            interest = 0.0
            repo_rate = ''
            days = self.valday_ael.days_between(ins_ael.exp_day, 'Act/365')
            for l in ins_ael.legs():
                premium2 = -self.trade_ael.premium - self.trade_ael.premium * l.fixed_rate * days / 36500
                interest = -self.trade_ael.premium * l.fixed_rate * days / 36500
                repo_rate = str(l.fixed_rate)
        else:
            raise Exception('Invalid instype')
        
        # Values
        yield mkvalues(
            ("COUNTERPARTY REF", self.trade.Counterparty().Name()),
            ("NUTRON CODE", self.trade.Counterparty().HostId()),
            ("UNEXCOR CODE", self.unexCor()),
            ("DEAL NO", self.trade.Name()),
            ("STOCK DESCRIPTION", self.instrument.Underlying().Name()),
            ("OUR PURCHASE/SALE", 'PURCHASE' if self.trade.Quantity() > 0 else 'SALE'),
            ("NOMINAL VALUE", formcurr(nominal_value)),
            ("REPO RATE", str(repo_rate) + "%"),
            ("DEAL DATE", self.trade.TradeTime()),
            ("SETTLEMENT DATE (LEG1)", self.trade.ValueDay()),
            ("SETTLEMENT DATE (LEG2)", self.instrument.ExpiryDateOnly()),
            ("YIELD TO MATURITY(LEG1)", str(yield_leg1) + "%"),
            ("YIELD TO MATURITY(LEG2)", str(yield_leg2) + "%"),
            ("CLEAN PRICE (LEG1)", clean_leg1),
            ("CLEAN PRICE (LEG2)", clean_leg2),
            ("PREMIUM (LEG1)", formcurr(self.trade.Premium())),
            ("PREMIUM (LEG2)", formcurr(premium2)),
            ("INTEREST", formcurr(interest)))

ael_gui_parameters = {'windowCaption':'BSB Confirmation'}

ael_variables = stc.get_ael_variables('Y:/Jhb/Ops CM/Capital Markets Confirmations/BSB Confirmations/')

def ael_main(parameters):
    trade_numbers = stc.parse_trade_numbers(parameters['TradeNumber'])

    if trade_numbers:
        allowed_instypes = [at.INST_BUYSELLBACK, at.INST_REPO_REVERSE]
        reporter = stc.Reporter(stc.prep_reporter_args('BSB', ReturnConfirmationReport, allowed_instypes, parameters))

        output_file_name = reporter.create_reports(trade_numbers)
        startFile(output_file_name)

def ASQL(*rest):
    acm.RunModuleWithParameters('SACM_BSB_Confirmation_PDF', 'Standard') #@UndefinedVariable
    return 'SUCCESS'
