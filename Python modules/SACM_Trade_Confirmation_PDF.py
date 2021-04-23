"""Base class for all confirmation report generators.

Extracted from SACM_FRN_Confirmation_PDF
"""
# Desk   Requester        Developer             CR Number
# What
# =============================================================================

# OPS    Sipho Ndlalane   Lukas Paluzga         ABITFA-1269
# Refactored to use common base.

# OPS    Letitia Roux     Lukas Paluzga         ABITFA-1795
# Refactored to use XMLReport. In effect that updates the letterhead.

# OPS    Letitia Roux     Jan Sinkora           CHNG0001185185
# Nominal now calculated in acm instead of ael (acm returns consistent values)

# OPS Sipho Ndlalane    Pavel Saparov           ABITFA-2237 (02/07/2014)
# Saving Confo Date Sent and Confo Text

#                       Willie vd Bank          2017-08-28 (FA Upgrade)
# Changed deprecated method QuoteToRoundedCleanUnitValueOverrideUnitDate to QuoteToUnitValueBase


import os, time

import acm, ael

import at, XMLReport
import at_time

class Reporter(object):
    """Class for mass generation of confirmation reports."""
    def __init__(self, params):
        self.allowed_ins_types = params['allowed_ins_types']
        self.confirmation_type = params['confirmation_type']
        self.date = params['date']
        self.filename_prefix = params.get('filename_prefix', self.confirmation_type + '_Confirmation_')
        self.output_directory = params['output_directory']
        self.report_cls = params['report_cls']
        self.xsl_pdf_template = params.get('xsl_pdf_template', 'XMLReport')

    def _create_report_xml(self, trade_number):
        trade = acm.FTrade[trade_number]
        instype = trade.Instrument().InsType()

        if instype not in self.allowed_ins_types:
            acm.Log('Instrument type {0} is not an allowed instype for confirmation generation'.format(instype))
            return

        if trade.Status() not in [at.TS_FO_CONFIRMED, at.TS_BO_CONFIRMED, at.TS_BOBO_CONFIRMED]:
            acm.Log('Trade {0} has status {1} that is not allowed for confirmation generation.'.format(trade.Oid(), trade.Status()))
            return

        report = self.report_cls(trade, self.date)

        if report.validate_trade():
            acm.Log('Generating Report for trade {0}'.format(trade_number))
            return report.create_report()

    def create_reports(self, trade_numbers):
        """Create the confirmation reports and return a list of report file names."""

        if not trade_numbers:
            acm.Log('No trades to process')
            return

        generator = XMLReport.XMLReportGenerator(
            output_dir = self.output_directory,
            xsl_fo_template_name = self.xsl_pdf_template)

        xmls = []
        for tn in trade_numbers:
            xml = self._create_report_xml(tn)
            if xml: xmls.append(xml)


        timestr = str(time.ctime().replace(':', ''))
        filename = '{0} Confirmation {1}'.format(self.confirmation_type, timestr)

        return generator.create_merged(xmls, filename)


class Report(XMLReport.StatementReportBase):
    """Base class for trade confirmation reports that includes some shared business data."""
    def __init__(self, trade, date):
        self.date = date

        # acm
        self.trade = trade
        self.instrument = trade.Instrument()

        #ael
        self.trade_ael = ael.Trade[trade.Oid()]
        self.instrument_ael = self.trade_ael.insaddr

        #utility
        self.valday_ael = self.trade_ael.value_day

    def client_address(self):
        """Return client address."""
        return XMLReport.contact_from_pty(self.trade.Counterparty())

    def unexCor(self):
        """Do best to return UnexCor Code additional info."""
        try: # sandboxed
            return self.trade.Counterparty().AdditionalInfo().UnexCor_Code()
        except:
            return ''

    def create_report(self):
        xml = super(Report, self).create_report()

        # Update two additional info fields 'Confo Date Sent' and 'Confo Text'
        try:
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_DATE_SENT,
                            at_time.time_now())
            at.addInfo.save(self.trade,
                            at.addInfoSpecEnum.CONFIRMATION_TEXT,
                            acm.User().Name())
        except:
            acm.Log('Error: Unable to save Confo Date Sent add info timestamp.')

        return xml

    def validate_trade(self):
        """Validate the state of the trade."""
        return True

class FRNReportBase(Report):
    """Base class for FRN and FRN-like reports (CLN)."""
    def convert_yield_to_price(self):
        trade_valueday = self.trade.ValueDay()

        denominatedvalue = acm.GetFunction('denominatedvalue', 4)
        denominatedYtm = denominatedvalue(self.trade_ael.price, self.instrument.Currency(), None, trade_valueday)
        underlying = self.instrument.Underlying()
        if underlying != None and underlying.Instrument().InsType() in (at.INST_BOND, at.INST_INDEXLINKED_BOND):
            leg = self.instrument.Underlying().Instrument().Legs().At(0)
        else:
            leg = self.instrument.Legs().At(0)
        # Front Upgrade 2013.3 -- leg info & quote to rounded clean unit value changed for 2013.3
        staticLegInfo = leg.StaticLegInformation(self.instrument, trade_valueday, None)
        legInfo = leg.LegInformation(trade_valueday)

        toDirty = True
        price = self.instrument.QuoteToUnitValueBase(denominatedYtm, trade_valueday, trade_valueday, toDirty, 
            [legInfo], [staticLegInfo], self.instrument.Quotation(), 1.0, 0.0)

        return price.Number()

    def instrument_externalid1(self):
        """Return instrument external ID 1, without the '-A', '-B'... suffix."""
        eid1 = self.instrument.ExternalId1()
        return eid1.partition('-')[0].strip()

    def is_combination_or_basket(self):
        """Return true when the trade is a combination/basket."""
        return self.instrument.InsType() == 'Combination'

    def traded_interest(self):
        context = acm.GetDefaultContext()
        calc_space = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')

        trade = acm.FTrade[self.trade_ael.trdnbr]
        top_node = calc_space.InsertItem(trade)
        try:
            calculation = calc_space.CreateCalculation(top_node, 'Portfolio Traded Interest')
            return calculation.Value().Number()

        except Exception, e:
            print 'Error calculating Original Premium', e

        return 0.0

    def _nominal_value(self):
        if self.is_combination_or_basket():
            return self.trade.Nominal()
        else:
            l = self.trade_ael.insaddr.legs()[0]
            cashflows = l.cash_flows()
            for cf in cashflows:
                if cf.type == 'Float Rate':
                    if cf.pay_day >= self.trade_ael.value_day and cf.start_day <= self.trade_ael.value_day:
                        # The ael way was not working for all deals.
                        #return abs(self.trade_ael.nominal_amount(self.trade_ael.value_day))
                        return abs(self.trade.Nominal())


# Following are helper functions that generate the GUI, etc.
def get_ael_variables(output, additional_vars = []):
    """Return ael variables for report generation dialog.

    :param output: The directory where the report(s) will be generated.
    :param additional_vars: Additional UI variables.

    """
    output_obj = acm.FFileSelection()
    output_obj.PickDirectory(True)
    output_obj.SelectedDirectory(output)

    today = acm.Time().DateNow()

    top =       [['OutputDirectory', 'Output Directory', output_obj, None,  output_obj, 0, 1,
                  'The directory where the report(s) will be generated.',      None, 1],
                 ['TradeNumber',     'Trade Number',     'string',   None,  None,       0, 0,
                  'To run for a soecific trade, enter the trade number here.', None, 1]]

    bottom =    [['date',            'date',             'string',   today, today,      1]]

    return top + additional_vars + bottom

def parse_trade_numbers(trades_list_string):
    """Parse comma separated trade numbers.

    :param trades_list_string: Comma-separated list of trade numbers.

    """
    return [int(s) for s in trades_list_string.split(',') if s.strip()]

def prep_reporter_args(confirmation_type, report_cls, allowed_ins_types, gui_parameters):
    """Parse task gui_parameters and return dictionary with values for reporter constructor.

    :param confirmation_type: Confirmation type. Used as prefix for reports, etc.
    :param report_cls: Type of report inherited from ``SACM_Trade_Confirmation_PDF.Report``.
    :type report_cls: class
    :param allowed_ins_types: Allowed instrument types.
    :type allowed_ins_types: enumerable

    """

    output_dir = os.path.join(str(gui_parameters['OutputDirectory']), ael.date_today().to_string('%Y%m%d')) + os.path.sep
    return { 'date': gui_parameters['date'],
             'output_directory': output_dir,
             'confirmation_type': confirmation_type,
             'report_cls': report_cls,
             'allowed_ins_types': allowed_ins_types }

