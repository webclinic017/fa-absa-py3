"""Confirmation report generator for FRN trades.

This script is invoked by calling the homonymous ASQL query.
"""
# ABITFA-569
# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    Aaeda Salejee    Ickin Vural            C000000697493
# Decommission platypus and move all existing reports using it to FOP

# OPS    Sipho Ndlalane   Bhavnisha Sarawan      94899
# Removed output fields and added calculation for All in price.

# OPS    Sipho Ndlalane   Bhavnisha Sarawan      C116487
# Added Accrued Interest calculation (Traded Interest TM column)

# OPS    Sipho Ndlalane   Lukas Paluzga          ABITFA-1269
# Refactored to use common base

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS    Letitia Carboni  Jan Sinkora            CHNG0001185185
# maturity date -> stock maturity date (changed label)

# OPS Sipho Ndlalane	Sanele Macanda		CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions


import os, time

import acm

import at, SACM_Trade_Confirmation_PDF as stc
from XMLReport import mkcaption, mkvalues, mkinfo
from zak_funcs import formcurr
from SAGEN_IT_Functions import startFile

class ReturnConfirmationReport(stc.FRNReportBase):
    def statement_detail(self):
        yield mkcaption("FRN ADVICE NOTE")

        if self.trade.Bought():
            yield mkinfo("We confirm having BOUGHT the following stock FROM you.")
        else:
            yield mkinfo("We confirm having SOLD the following stock TO you.")

        values = [("DEAL REFERENCE", self.trade.Name()),
                  ("COUNTERPARTY CODE", self.trade.Counterparty().Name()),
                  ("NUTRON CODE", self.trade.Counterparty().HostId()),
                  ("UNEXCOR CODE", self.unexCor()),
                  ("STOCK DESCRIPTION", self.instrument_externalid1()),
                  ("DEAL DATE", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.trade_ael.creat_time))),
                  ("SETTLEMENT DATE", self.trade.ValueDay()),
                  ("NOMINAL VALUE", formcurr(self._nominal_value())),
                  ("CONSIDERATION", formcurr(self.trade_ael.premium))]
        try:
            values.append(("ISSUED BY", self.instrument.Issuer().Name()))
        except AttributeError:
            pass
        values.append(("STOCK MATURITY DATE", self.instrument.ExpiryDateOnly()))
        values.append(("ALL-IN-PRICE", str(self.convert_yield_to_price() * 100)+ "%"))
        values.append(("ACCRUED INTEREST", formcurr(self.traded_interest())))

        yield mkvalues(*values)

ael_gui_parameters = {'windowCaption':'FRN Confirmation'}
ael_variables = stc.get_ael_variables('Y:/Jhb/Ops CM/Capital Markets Confirmations/FRN Confirmations/')

def ael_main(parameters):
    trade_numbers = stc.parse_trade_numbers(parameters['TradeNumber'])

    if trade_numbers:
        reporter = stc.Reporter(stc.prep_reporter_args('FRN', ReturnConfirmationReport, [at.INST_FRN], parameters))

        output_file_name = reporter.create_reports(trade_numbers)
        startFile(output_file_name)

def ASQL(*rest):
    acm.RunModuleWithParameters('SACM_FRN_Confirmation_PDF', 'Standard') #@UndefinedVariable
    return 'SUCCESS'
