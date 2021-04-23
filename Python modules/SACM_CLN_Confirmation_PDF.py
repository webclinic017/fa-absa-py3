"""Confirmation report generator for CLN and FRN-CLN basket trades.

This script is invoked by calling the homonymous ASQL query.
"""
# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    Sipho Ndlalane   Lukas Paluzga          ABITFA-1269
# Refactored to use common base; Created CLN report.

# OPS    Letitia Carboni  Lukas Paluzga          ABITFA-1795
# New letterhead

# OPS Sipho Ndlalane	Sanele Macanda		CHNG0001662676 - ABITFA -No Jira (23/01/2014)
# Replaced os.startfile() with startFile() see SAGEN_IT_Functions


import os, time

import acm

import at, SACM_Trade_Confirmation_PDF as stc
from XMLReport import mkinfo, mkvalues, mkcaption
from zak_funcs import formcurr
from SAGEN_IT_Functions import startFile

class ReturnConfirmationReport(stc.FRNReportBase):
    def validate_trade(self):
        if self.instrument.InsType() == at.INST_FRN:
            if at.addInfo.get_value(self.trade, at.addInfoSpecEnum.MM_INSTYPE) != 'CLN':
                acm.Log('Instrument type FRN is not an allowed unless CLN is specified in {0}. '.format(at.addInfoSpecEnum.MM_INSTYPE))
                return False

        return super(stc.FRNReportBase, self).validate_trade()

    def statement_detail(self):
        yield mkinfo("""The Note described in this document is subject to the terms and conditions set out in the Applicable Pricing \
Supplement and the General Terms and Conditions of the Notes set out in the Programme Memorandum dated 19 July 2007 relating \
to the Issuer's Credit-linked Note Programme (the "Programme Memorandum"). This document must be read in conjunction with \
the Applicable Pricing Supplement and the Programme Memorandum. In the event of any inconsistency between this document and \
the Applicable Pricing Supplement, the Applicable Pricing Supplement will prevail. In the event of any inconsistency between \
the Applicable Pricing Supplement and the Programme Memorandum, the Applicable Pricing Supplement will prevail.""")
        
        yield mkcaption('CLN ADVICE NOTE')    
        
        if self.trade.Bought():
            yield mkinfo("We confirm having BOUGHT the following credit-linked note FROM you.")
        else:
            yield mkinfo("We confirm having SOLD the following credit-linked note TO you.")

        values = [["DEAL REFERENCE:", self.trade.Name()],
                   ["COUNTERPARTY CODE:", self.trade.Counterparty().Name()],
                   ["NUTRON CODE:", self.trade.Counterparty().HostId()],
                   ["UNEXCOR CODE:", self.unexCor()],
                   ["CLN DESCRIPTION", self.instrument_externalid1()],
                   ["DEAL DATE:", time.strftime('%d/%m/%Y %H:%M:%S ', time.localtime(self.trade.CreateTime()))],
                   ["SETTLEMENT DATE:", self.trade.ValueDay()],
                   ["NOMINAL VALUE:", formcurr(abs(self.trade.Nominal()))],
                   ["CONSIDERATION:", formcurr(self.trade_ael.premium)]]
        
        try:
            values.append(["ISSUED BY:", self.instrument.Issuer().Name()])
        except AttributeError:
            pass

        # Do not show maturity date for combination/basket CLNs
        if not self.is_combination_or_basket():
            values.append(["MATURITY DATE:", self.instrument.ExpiryDateOnly()])

        values.append(["ALL-IN-PRICE:", self.trade.Price()])
        values.append(["ACCRUED INTEREST:", formcurr(self.traded_interest())])
        
        yield mkvalues(*values)

ael_gui_parameters = {'windowCaption':'CLN Confirmation'}
ael_variables = stc.get_ael_variables('Y:/Jhb/Ops CM/Capital Markets Confirmations/CLN Confirmations/')

def ael_main(parameters):
    trade_numbers = stc.parse_trade_numbers(parameters['TradeNumber'])

    if trade_numbers:
        allowed_instypes = [at.INST_FRN, at.INST_COMBINATION]
        reporter = stc.Reporter(stc.prep_reporter_args('CLN', ReturnConfirmationReport, allowed_instypes, parameters))

        output_file_name = reporter.create_reports(trade_numbers)
        startFile(output_file_name)

def ASQL(*rest):
    acm.RunModuleWithParameters('SACM_CLN_Confirmation_PDF', 'Standard') #@UndefinedVariable
    return 'SUCCESS'

