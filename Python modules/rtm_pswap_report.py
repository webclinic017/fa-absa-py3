import os
import csv
import sys
import time
import string
import traceback
from collections import defaultdict

import acm

from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator
from at_logging import getLogger, bp_start
from PS_FormUtils import DateField

# Logging
LOGGER = getLogger(__name__)
import logging
LOGGER.setLevel(logging.DEBUG)
VERSION = "1.0"

# One global instance of calculation space
CONTEXT = acm.GetDefaultContext()
SHEET_CLASS = 'FPortfolioSheet'
CALC_SPACE = acm.Calculations().CreateCalculationSpace(CONTEXT, SHEET_CLASS)

# Dates
DATES = DateField.get_captions([
    'PrevBusDay',
    'Now',
    'Custom Date'])

class RTMPortfolioSwapReport(CSVReportCreator):
    """Generic report to expose how sweeping amounts are calculated."""
    def __init__(self, full_file_path, date):
        # Add report date
        self.report_date = date
        # Split full path into individual parameters of the parent class.
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)
        super(RTMPortfolioSwapReport, self).__init__(
            file_name_only,
            file_suffix,
            file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        # Apply date settings
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.report_date)
        CALC_SPACE.SimulateGlobalValue('Valuation Date', self.report_date)
        CALC_SPACE.SimulateGlobalValue('Valuation Parameter Date', self.report_date)

        # Calculate report data
        for pswap in acm.FPortfolioSwap.Select('name like "RTM_*"'):
            if "43190" in pswap.Name() in pswap.Name():
                # Skip pswaps booked for the Proof-of-Concept
                continue
            # Collect pswap data
            LOGGER.debug("Processing %s", pswap.Name())
            self._collect_pswap_data(pswap)

        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        CALC_SPACE.RemoveGlobalSimulation('Valuation Date')
        CALC_SPACE.RemoveGlobalSimulation('Valuation Parameter Date')

    def _collect_pswap_data(self, pswap):
        """Collect data for individual pswaps."""
        start = time.time()
        
        # Stock portfolio values
        stock_portfolio = pswap.FundPortfolio()
        
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', stock_portfolio.Name())
        query.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', acm.EnumFromString('InsType', 'Swap'))
        
        stock_cash_end = CALC_SPACE.CalculateValue(query, 'Portfolio Cash End').Number()
        stock_val_end = CALC_SPACE.CalculateValue(query, 'Total Val End').Number()
        stock_fees_settled =  CALC_SPACE.CalculateValue(query, 'Settled Fees')
        stock_fees_unsettled =  CALC_SPACE.CalculateValue(query, 'Unsettled Fees')
        settled_divs = CALC_SPACE.CalculateValue(query, 'ACSSettledDividends')
        unsettled_divs = CALC_SPACE.CalculateValue(query, 'ACSPVUnsettledDividends')
        
        # Recon values for stock portfolio
        stock_cash_end_excl_divs_fees = stock_cash_end - settled_divs - stock_fees_settled
        stock_val_end_excl_divs_fees = stock_val_end - unsettled_divs - stock_fees_unsettled
                
        for trade in pswap.Trades():
            # Pswap values
            pswap_cash_end = CALC_SPACE.CalculateValue(trade, 'Portfolio Cash End').Number()
            pswap_val_end = CALC_SPACE.CalculateValue(trade, 'Total Val End').Number()
            pswap_qty = trade.Quantity()
            
            # Fees on the portfolio swap
            pswap_fees_settled =  CALC_SPACE.CalculateValue(trade, 'Settled Fees')
            pswap_fees_unsettled = CALC_SPACE.CalculateValue(trade, 'Unsettled Fees')
            
            # TPL excluding fees
            # FIXME: add exclusion once fees are enabled
            pswap_cash_excl_fees = pswap_cash_end
            pswap_val_excl_fees = pswap_val_end
            
            # Recon differences
            if pswap_qty > 0:
                # Bank side of the RTM (should be equal)
                cash_diff = stock_cash_end_excl_divs_fees - pswap_cash_excl_fees
                val_diff = stock_val_end_excl_divs_fees - pswap_val_excl_fees
            else:
                # ACS side of the RTM (should be equal and opposite)
                cash_diff = stock_cash_end_excl_divs_fees + pswap_cash_excl_fees
                val_diff = stock_val_end_excl_divs_fees + pswap_val_excl_fees
            
            # Add record to the report
            row = [
                stock_portfolio.Name(),
                trade.Instrument().Name(),
                trade.Oid(),
                pswap_qty,
                trade.Portfolio().Name(),
                stock_cash_end,
                stock_val_end,
                stock_fees_settled,
                stock_fees_unsettled,
                settled_divs,
                unsettled_divs,
                stock_cash_end_excl_divs_fees,
                stock_val_end_excl_divs_fees,                
                pswap_cash_end,
                pswap_val_end,
                pswap_fees_settled,
                pswap_fees_unsettled,
                pswap_cash_excl_fees,
                pswap_val_excl_fees,
                cash_diff,
                val_diff
            ]
            LOGGER.debug(row)
            self.content.append(row)
            
        end = time.time()
        LOGGER.debug("Done in %s seconds", end - start)


    def _header(self):
        """Return columns of the header."""
        header = [
            "Stock Portfolio",
            "Pswap",
            "Pswap Trade",
            "Pswap Quantity",
            "Pswap Portfolio",
            "Stock Cash End",
            "Stock Val End",
            "Stock Fees Settled",
            "Stock Fees Unsettled",
            "Stock Settled Dividends",
            "Stock Unsettled Dividends",
            "Stock Cash excl. Settled Dividends & Fees",
            "Stock Val excl. Unsettled Dividends & Unsettled Fees",
            "Pswap Cash End",
            "Pswap Val End",
            "Pswap Settled Fees",
            "Pswap Unsettled Fees",
            "Pswap Cash excl. Settled Fees",
            "Pswap Val excl. Unsettled Fees",
            "Cash Diff",
            "Val Diff"
        ]
        return header
        

def add_date_to_path(output_file, date):
    """Return the file path with date paremeter."""
    file_path_template = string.Template(output_file)
    file_path = file_path_template.substitute(DATE=date.replace("-", ""))
    return file_path


def custom_date_hook(selected_variable):
    """Enable/Disable Custom Date base on Date value."""
    start_date = ael_variables.get('date')
    start_date_custom = ael_variables.get('date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add("output_file",
                  label="Output file")
ael_variables.add("date",
                  label="Date",
                  default="Now",
                  collection=DATES,
                  hook=custom_date_hook)

ael_variables.add("date_custom",
                  label="Date Custom",
                  default=acm.Time().DateToday(),
                  enabled=False)


def ael_main(config):
    """Entry point of the script."""
    if config['date'] == 'Custom Date':
        date = config['date_custom']
    else:
        date = DateField.read_date(config['date'])
    output_file = config["output_file"]
    
    # Generate the report
    file_path = add_date_to_path(output_file, date)
    report = RTMPortfolioSwapReport(file_path, date)
    master_start = time.time()
    try:
        report.create_report()
        master_end = time.time()
        LOGGER.info("Secondary output wrote to %s", file_path)
        LOGGER.info("Completed successfully %s seconds.", master_end - master_start)        
    except Exception:
        traceback.print_exc()
