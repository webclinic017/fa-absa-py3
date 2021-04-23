"""
Project                : SBL Exception Report
Department and Desk    : PCG
Requester              : Candice Johnson
Developer              : Bhavik Mistry

Description of output files:
Internal Loans     -  Calculated as the sum of open sec loans
Shorts Not Covered -  Grouped per underlying per SL sweeping desk where SL sweeping desk covered position < zero
Over-Borrows       -  Stock position per underlying per desk < zero, and Covered position per underlying per desk > zero
ACS_Lender_Diffs   -  Sum of the quantity of interdesk "No Collateral" trades <> sum of the quantity of ACS Lender 
                      legs in aggregate per stock

------------------------------------------------------------------------------
HISTORY

===============================================================================
Date        Change no       Developer           Description
-------------------------------------------------------------------------------
2014-12-11  CHNG            Bhavik Mistry       Initial version           
2015-12-10					Fancy Dire			Extended to include the Reserved stock if 
												it is short(<0),aggregated by Portfolio.
"""

import acm
from at_time import add_delta
from datetime import date
import csv
from operator import attrgetter
from itertools import groupby
from operator import itemgetter
import FReportAPIBase
import FReportAPI
from at_email import EmailHelper

# ====================================================== Helper functions ==============================================


def transform_xml(template, xml):
    """ Method to transform xml using template

    Arguments:
        template    -- the name XSLT template.
        xml         -- the xml value to be transformed.
    """
    extension = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', template)
    xsl_template = extension.Value()
    transformer = acm.CreateWithParameter('FXSLTTransform', xsl_template)
    return transformer.Transform(xml)


def write_file(name, data, access='wb'):
    """ Method to write report output to csv file

    Arguments:
        name -- the name of the file.
        data -- the data to write to file.
    """
    file_obj = open(name, access)
    csv_writer = csv.writer(file_obj, dialect='excel-tab')
    csv_writer.writerows(data)
    file_obj.close()


def email_report(body, subject, emails, email_from, attachments=None):
    """ Wrapper method to email reports

    Arguments:
        body        -- body of email.
        subject     -- subject of email.
        emails      -- email addresses to send to.
        email_from  -- text to display as from.
        attachments -- attachments in a list.
    """

    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)

    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()

    try:
        emailHelper.send()
    except Exception as e:
        print "!!! Exception: {0}\n".format(e)

# ====================================================== SBL Class =====================================================


class SBL(object):
    def __init__(self, und_ins, quantity=0, allocated_desk='', portfolio='', rate=0, price=0):
        self.und_ins = und_ins
        self.quantity = quantity
        self.allocated_desk = allocated_desk
        self.portfolio = portfolio
        self.price = price
        self.rate = rate
        

class SBLFuncs(object):

    sec_loan_trades = []
    
    short_res_stock = []
    
    agg_stock_pos = []

    agg_sec_loans_all = []
    agg_sec_loans_internal = []
    agg_sec_loans_noCollateral = []
    agg_sec_loans_external = []
    agg_sec_loans_externalOnly = []

    covered_pos = []
    avg_und_prices = []

    def __init__(self, price_file, sec_loan_query, stock_query1, stock_query2):
        """
        Arguments:
            price_file     -- currently ACS_BDA_PosRec_XXXX. save down for underlying prices.
            sec_loan_query -- security loans query folder.
            stock_query    -- stocks query folder.
        """

        self.sec_loan_query = sec_loan_query
        self.stock_query1 = stock_query1
        self.stock_query2 = stock_query2

        print 'Getting all security loans'
        self.get_sec_loans()
        
        
        print 'Getting all stocks'
        
        key_func = attrgetter('und_ins', 'allocated_desk', 'portfolio')
        self.get_short_res_stocks(key_func)
        
        print 'Aggregated stocks'
        for i in self.short_res_stock:
            print i.und_ins, i.allocated_desk, i.portfolio, i.quantity
        
        key_func = attrgetter('allocated_desk', 'und_ins')
        self.agg_short_res_stocks(key_func)
        
        print 'Aggregated stocks'
        for i in self.agg_stock_pos:
            print i.allocated_desk, i.und_ins, i.portfolio, i.quantity

        key_func = attrgetter('und_ins')
        print 'Getting InternalOnly security loans - grouped by underlying'
        self.agg_sec_loans_internal = self.get_agg_sec_loans(key_func, 'InternalOnly')

        print 'Getting ExternalOnly security loans - grouped by underlying'
        self.agg_sec_loans_externalOnly = self.get_agg_sec_loans(key_func, 'ExternalOnly')

        print 'Getting No Collateral security loans from ACS - Script Lending only - grouped by underlying'
        self.agg_sec_loans_noCollateral = self.get_agg_sec_loans(key_func, 'No Collateral')

        print 'Getting External security loans from ACS - Script Lending only - grouped by underlying'
        self.agg_sec_loans_external = self.get_agg_sec_loans(key_func, 'External')

        key_func = attrgetter('und_ins', 'allocated_desk')
        print 'Getting all security loans - grouped by underlying, allocated_desk'
        self.agg_sec_loans_all = self.get_agg_sec_loans(key_func)

        print 'Getting stocks'
        self.get_agg_stocks1()
        
        print 'Calculating covered position - grouped by underlying, allocated_desk'
        self.calculate_covered_pos(key_func)

        print 'Getting average und prices'
        self.get_avg_und_prices(price_file)

    def get_sec_loans(self):
        """ Return all security loans from query folder """

        query = acm.FStoredASQLQuery[self.sec_loan_query]
        trade_list = query.Query().Select()

        self.sec_loan_trades = trade_list

    def _sbl_sec_loan_trades(self, trade_filter):
        """
        Further filtering of trades from security loans query folder

        trade_filter -- string value to filter out specific trades
        """
        if trade_filter == 'InternalOnly':
            new_trade_list = [t for t in self.sec_loan_trades
                              if t.Instrument().AdditionalInfo().SL_ExternalInternal() == 'Internal' and
                              t.Portfolio().Name() != 'ACS - Script Lending']

        elif trade_filter == 'ExternalOnly':
            new_trade_list = [t for t in self.sec_loan_trades
                              if t.Instrument().AdditionalInfo().SL_ExternalInternal() == 'External' and
                              t.Portfolio().Name() != 'ACS - Script Lending']

        elif trade_filter == 'No Collateral':
            new_trade_list = [t for t in self.sec_loan_trades
                              if t.Instrument().AdditionalInfo().SL_ExternalInternal() == 'No Collateral' and
                              t.Portfolio().Name() == 'ACS - Script Lending']

        elif trade_filter == 'External':
            new_trade_list = [t for t in self.sec_loan_trades
                              if t.Instrument().AdditionalInfo().SL_ExternalInternal() == 'External' and
                              t.Portfolio().Name() == 'ACS - Script Lending' and
                              t.AdditionalInfo().SL_G1Counterparty2() == 'SLL ACS LENDER']

        else:
            new_trade_list = [t for t in self.sec_loan_trades if t.Portfolio().Name() != 'ACS - Script Lending']
        
        return new_trade_list

    def get_agg_sec_loans(self, key_func, trade_filter=None):
        """
        Aggregate security loans on specific attribute

        key_func        -- Attribute to aggregate on.
        trade_filter    -- Filter out certain trades (InternalOnly, ExternalOnly, No Collateral, External).

        return: List of aggregated security loans.
        """

        sec_loans = []
        agg_sec_loans = []
        total_quantity = 0
        total_rate = 0

        self.get_sec_loans()
        trades = self._sbl_sec_loan_trades(trade_filter)

        for t in trades:
            sec_loans.append(SBL(t.Instrument().Underlying().Name(),
                                 t.Quantity() * t.Instrument().RefValue(),
                                 t.Portfolio().AdditionalInfo().SL_AllocatedDesk(),
                                 t.Portfolio().Name(),
                                 t.Instrument().Legs()[0].FixedRate()))

        sorted_input = sorted(sec_loans, key=key_func)
        groups = groupby(sorted_input, key=key_func)

        for key, rows in groups:
            group_list = list(rows)
    
            for item in group_list: 
                total_quantity += item.quantity
                total_rate += item.rate
        
            agg_sec_loans.append(SBL(item.und_ins, round(total_quantity, 2),
                                     item.allocated_desk,
                                     total_rate/len(group_list)))

            total_quantity = 0  
            total_rate = 0  

        return agg_sec_loans

    def get_short_res_stocks(self, key_func):
        """ Return all reserved stock from query folder 
        
        And  Aggregate stocks on specific attribute

        key_func        -- Attribute to aggregate on.

        return: List of aggregated short reserved stocks.
        """

        query = acm.FStoredASQLQuery[self.stock_query2]
        trade_list = query.Query().Select()
    
        stocks = []
        agg_stock = []
        total_quantity = 0

        for t in trade_list:
            stocks.append(SBL(t.Instrument().Name(),
                                 t.Quantity(),
                                 t.Portfolio().AdditionalInfo().SL_AllocatedDesk(),
                                 t.Portfolio().Name()))

        sorted_input = sorted(stocks, key=key_func)
        groups = groupby(sorted_input, key=key_func)

        for key, rows in groups:
            group_list = list(rows)
    
            for item in group_list: 
                total_quantity += item.quantity
            
            if total_quantity < 0:
                agg_stock.append(SBL(item.und_ins, round(total_quantity, 2),
                                     item.allocated_desk, item.portfolio))

            total_quantity = 0 
            
        self.short_res_stock = agg_stock
        
    def agg_short_res_stocks(self, key_func):
        """ Aggregate stocks on specific attribute

        key_func        -- Attribute to aggregate on.

        return: List of aggregated short reserved stocks.
        """
   
        agg_stock = []
        total_quantity = 0

        sorted_input = sorted(self.short_res_stock, key=key_func)
        groups = groupby(sorted_input, key=key_func)

        for key, rows in groups:
            group_list = list(rows)
    
            for item in group_list: 
                total_quantity += item.quantity
            
            if total_quantity < 0:
                agg_stock.append(SBL(item.und_ins, round(total_quantity, 2),
                                     item.allocated_desk))

            total_quantity = 0 
            
        self.agg_stock_pos = agg_stock
        
    def get_agg_stocks1(self):
        """
        Return aggregated stocks on specific attribute based of trading sheet template.
        Sheet populated by specified stock query folder and grouped by allocated desk.
        """

        report_param_base = FReportAPI.FWorksheetReportApiParameters(reportName='SBLStock',
                                                                     storedASQLQueries=self.stock_query1,
                                                                     grouping='SL_AllocatedDesk')

        report_builder = FReportAPIBase.FReportBuilder(report_param_base)

        report_builder.params.includeColorInformation = 0
        report_builder.params.includeFormattedData = 0
        report_builder.params.includeDefaultData = 1
        report_builder.params.includeFullData = 0
        report_builder.params.includeRawData = 1

        temp = acm.FTradingSheetTemplate['sbl_stock_pos']
        trading_sheet = temp.TradingSheet()
        include_rows = False
        container_name = 'sbl_stock_pos'

        report_grid, output = report_builder.createReportGridBySheet(trading_sheet, include_rows, container_name)
        sheet_type = str(trading_sheet.ClassName())

        report_builder.simulateSheetSettings(report_grid, sheet_type)
        report_grid.Generate()
        xml = output.AsString()

        desk = ''
        sheet_data = transform_xml('FStrippedCSVTemplateAllData', xml).split('\r')
        sheet_data.pop(0)  # remove column header

        for line in sheet_data:
            row = (line.rstrip(',')).split(',')
            if len(row) == 1:
                desk = row[0]
            else:
                self.agg_stock_pos.append(SBL(row[0], round(float(row[1]), 2), desk))
                
                
    def calculate_covered_pos(self, key_func):
        """
        Covered position is the sum of the stock position and security loan position.

        key_func -- attribute to aggregate on.
        """
        total_quantity = 0

        positions = self.agg_sec_loans_all + self.agg_stock_pos

        sorted_input = sorted(positions, key=key_func)
        groups = groupby(sorted_input, key=key_func)

        for key, rows in groups:
            group_list = list(rows)
    
            for item in group_list: 
                total_quantity += item.quantity
        
            self.covered_pos.append(SBL(item.und_ins, round(total_quantity, 2), item.allocated_desk))

            total_quantity = 0
                
    def get_avg_und_prices(self, input_file):
        """
        Aggregate underlying price from file based instrument

        price_file     -- currently ACS_BDA_PosRec_XXXX. save down for underlying prices.
        """
        file_rows = []
        total_price_end = 0

        with open(input_file, 'rb') as price_file:
            for row in price_file:
                file_rows.append(row.rstrip('\n').split(','))

        file_rows.pop(0)  # remove headers from list
        sorted_input = sorted(file_rows, key=itemgetter(0)) 
        groups = groupby(sorted_input, key=itemgetter(0)) 

        for key, rows in groups:
            prices = list(rows)

            for price in prices:
                total_price_end += float(price[18])

            self.avg_und_prices.append(SBL(key, price=(total_price_end / len(prices))))
            total_price_end = 0
    
    def get_internal_loans(self):
        """
        Helper function to get internal loans data to write to file.
        Columns to display -- 'Underlying Instrument', 'Net Quantity'
        """

        internal_loans = [['Underlying Instrument', 'Net Quantity']]

        for item in self.agg_sec_loans_internal:
            internal_loans.append([item.und_ins, item.quantity])

        return internal_loans

    def get_shorts(self):
        """
        Helper function to get shorts data to write to file.
        Columns to display -- 'Underlying Instrument', 'SL Sweeping Desk', 'Net Uncovered Position'
        """

        shorts = [['Underlying Instrument', 'SL Sweeping Desk', 'Net Uncovered Position']]
    
        for item in self.covered_pos:
            if item.quantity < 0:
                shorts.append([item.und_ins, item.allocated_desk, item.quantity])
            
        return shorts

    def get_over_borrows(self):
        """
        Helper function to get over borrows data to write to file..
        Columns to display -- 'Stock', 'SBL Sweeping Book', 'Over-Borrow', 'Underlying Price',
                              'Collateral (Haircut 105%)', 'Rate', 'Approx PnL Impact'
        """

        over_borrows = [['Stock', 'SBL Sweeping Book', 'Over-Borrow', 'Underlying Price',
                         'Collateral (Haircut 105%)', 'Rate', 'Approx PnL Impact']]

        prices = self.avg_und_prices
        avg_rate = 0.35

        for item in self.agg_stock_pos:
            if item.quantity < 0:
                covered_pos_match = [x for x in self.covered_pos if x.und_ins == item.und_ins and
                                     x.allocated_desk == item.allocated_desk]
                
                if covered_pos_match:
                    if covered_pos_match[0].quantity > 0:  # Should only be one match
                        stock_und_price = [x for x in prices if x.und_ins == covered_pos_match[0].und_ins]
                        collateral = covered_pos_match[0].quantity * stock_und_price[0].price / 100 * 1.05
                        rate_match = [x for x in self.agg_sec_loans_externalOnly if x.und_ins == covered_pos_match[0].und_ins]

                        if rate_match:
                            avg_rate = rate_match[0].rate
                        approx_pnl = covered_pos_match[0].quantity * stock_und_price[0].price * avg_rate / 100 / 365 / 100
        
                        over_borrows.append([covered_pos_match[0].und_ins, covered_pos_match[0].allocated_desk,
                                             covered_pos_match[0].quantity, stock_und_price[0].price, collateral,
                                             avg_rate, approx_pnl])
                        avg_rate = 0.35
            
        return over_borrows            

    def get_acs_lender_diffs(self):
        """
        Helper function to get ACS lender diffs data to write to file.
        Columns to display -- 'Security', 'No Collateral (Sells)', 'External ACS Lender', 'No Coll vs ACS Lender'
        """

        agg_lender_diffs = []
        total_quantity = 0

        acs_lender_diffs = [['Security', 'No Collateral (Sells)', 'External ACS Lender', 'No Coll vs ACS Lender']]

        positions = self.agg_sec_loans_noCollateral + self.agg_sec_loans_external

        sorted_input = sorted(positions, key=attrgetter('und_ins'))
        groups = groupby(sorted_input, key=attrgetter('und_ins'))

        for key, rows in groups:
            group_list = list(rows)
    
            for item in group_list: 
                total_quantity -= item.quantity
        
            agg_lender_diffs.append(SBL(item.und_ins, round(total_quantity, 2), item.allocated_desk))

            total_quantity = 0  

        for item in agg_lender_diffs:
            if item.quantity != 0:
                external_pos_match = [x for x in self.agg_sec_loans_external if x.und_ins == item.und_ins]
                no_collateral_pos_match = [x for x in self.agg_sec_loans_noCollateral if x.und_ins == item.und_ins]

                external = external_pos_match[0].quantity if external_pos_match else 0
                no_collateral = no_collateral_pos_match[0].quantity if no_collateral_pos_match else 0

                acs_lender_diffs.append([item.und_ins, no_collateral, external, item.quantity])

        return acs_lender_diffs


# ====================================================== Main =========================================================


# AEL Variables :
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = []
ael_variables.append(['PricePath', 'Price file path: ', 'string', None, 'F:\\\\', 1])
ael_variables.append(['OutPath', 'Output Path: ', 'string', None, 'F:\\\\', 1])
ael_variables.append(['Sec_Loan', 'Sec Loan Query: ', 'string', None, None, 1, 0])
ael_variables.append(['Stock1', 'Stock Query (Reserved Stock = No): ', 'string', None, 'SBL_Stock_Res_No', 1, 0])
ael_variables.append(['Stock2', 'Stock Query (Reserved Stock = Yes): ', 'string', None, 'SBL_Stock_Res_Yes', 1, 0])
ael_variables.append(['emailAddr', 'Email Address', 'string', None, '', 0, 1, 'Email', None, 1])


def ael_main(data):

    price_file = data['PricePath']
    output_path = data['OutPath']
    sec_loan_query = data['Sec_Loan']
    stock_query1 = data['Stock1']
    stock_query2 = data['Stock2']
    emails = data['emailAddr']

    attachments = []
    TODAY = add_delta(date.today(), -1, 0, 0)
    
    acm.Log('Date today: ' + str(TODAY))

    price_file = price_file + '/' + str(TODAY) + '/' + 'ACS_BDA_PosRec_' + TODAY.strftime("%y%m%d") + '.csv'
    acm.Log('Price file used: ' + price_file)

    funcs = SBLFuncs(price_file, sec_loan_query, stock_query1, stock_query2)

    write_file(output_path + '/Internal_Loans_' + str(TODAY) + '.xls', funcs.get_internal_loans())
    attachments.append(output_path + '/Internal_Loans_' + str(TODAY) + '.xls')
    acm.Log('Wrote secondary output to:::' + output_path + '/Internal_Loans_' + str(TODAY) + '.xls')

    write_file(output_path + '/Shorts_not_covered_' + str(TODAY) + '.xls', funcs.get_shorts())
    attachments.append(output_path + '/Shorts_not_covered_' + str(TODAY) + '.xls')
    acm.Log('Wrote secondary output to:::' + output_path + '/Shorts_not_covered_' + str(TODAY) + '.xls')

    write_file(output_path + '/Over_Borrows_' + str(TODAY) + '.xls', funcs.get_over_borrows())
    attachments.append(output_path + '/Over_Borrows_' + str(TODAY) + '.xls')
    acm.Log('Wrote secondary output to:::' + output_path + '/Over_Borrows_' + str(TODAY) + '.xls')

    write_file(output_path + '/ACS_Lender_Diffs_' + str(TODAY) + '.xls', funcs.get_acs_lender_diffs())
    attachments.append(output_path + '/ACS_Lender_Diffs_' + str(TODAY) + '.xls')
    acm.Log('Wrote secondary output to:::' + output_path + '/ACS_Lender_Diffs_' + str(TODAY) + '.xls')

    email_report("SBL Exception Reporting for SBL Sweeping Scripts", "SBL Sweeping Script Exceptions " + str(TODAY), emails, "Prime", attachments=attachments)
    acm.Log('Emailed reports to:::' + str(emails))
