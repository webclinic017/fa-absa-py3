"""----------------------------------------------------------------------------------------------
MODULE
    sbl_credit_risk_report

DESCRIPTION
    Date                : 2020-04-01
    Purpose             : This creates a credit risk report for either cash or noncash collateral
    Department and Desk : Credit Risk
    Requester           : Credit Risk
    Developer           : Qaqamba Ntshobane

HISTORY
==================================================================================================
Date            Change no       Developer               Description
--------------------------------------------------------------------------------------------------
2020-04-01      PCGDEV-57       Qaqamba Ntshobane       Initial Implementation

ENDDESCRIPTION
-----------------------------------------------------------------------------------------------"""

import acm
import os
import csv

from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ACTIVE_FLAG = "Y"
REPORT_FREQUENCY = "D"
MITIGANT_SENIORITY = "1"
APPLICATION_ID ="Front Arena"
DATE_TODAY = acm.Time.DateToday()
ABSA_SDSID = acm.FParty["ABSA SECURITIES LENDING"].AdditionalInfo().BarCap_SMS_LE_SDSID()

DIRECTORY_SELECTOR = acm.FFileSelection()
DIRECTORY_SELECTOR.PickDirectory(True)
DIRECTORY_SELECTOR.SelectedDirectory('Y:\Jhb\SL Operations\G1Uploads\PROD\Out')

CALC_SPACE = acm.FCalculationMethods().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')

def switch_query_folder(ael_var):

    for var in ael_variables:
        if var[0] == 'query_folder' and ael_var.value == 'true':
            var.value = acm.FStoredASQLQuery["sbl_cash_collateral"]
        elif var[0] == 'query_folder' and ael_var.value == 'false':
            var.value = acm.FStoredASQLQuery["sbl_noncash_collateral"]
        switch_report_name(ael_var)


def switch_report_name(ael_var):

    for var in ael_variables:
        if var[0] == 'output_filename' and ael_var.value == 'true':
            var.value = 'seclendingcollateralc.d'
        elif var[0] == 'output_filename' and ael_var.value == 'false':
            var.value = 'seclendingcollateralnc.d'


ael_variables = AelVariableHandler()
ael_variables.add(
    'output_filename',
    label = 'Output File',
    cls = 'string'
    )
ael_variables.add(
    'file_drop_location',
    label = 'File Drop Location',
    cls = DIRECTORY_SELECTOR,
    default = DIRECTORY_SELECTOR,
    multiple = True
    )
ael_variables.add(
    'is_cash_collateral',
    label = 'Cash Collateral?',
    cls="bool",
    collection=(True, False),
    default = False,
    hook=switch_query_folder
    )
ael_variables.add(
    'query_folder',
    label = 'Query Folder',
    cls = "FStoredASQLQuery",
    multiple = True
    )


class CreditRiskReportProcessor(object):

    column_headers = ['Mitigant Bank application ID', 'Frequency', 'Extract Date',
                      'Mitigant ID', 'Mitigant Group', 'Mitigant Description',
                      'Country of Mitigant', 'Start Date', 'End Date', 'Release Date',
                      'Active Flag', 'Beneficiary SDS ID', 'Provider SDS ID',
                      'Instrument Issuer SDS ID', 'Instrument Issuer Name',
                      'Value Required Currency', 'Value Required Amount',
                      'Value Required Percentage', 'Mitigant Seniority',
                      'ISIN Code', 'Security Name'
                     ]

    def __init__(self, coll_type):

        self.is_cash_coll = coll_type

    def _run_data_extraction(self, trades):

        report_data = []

        for trade in trades:
            instype = trade.Instrument().InsType()
            
            self.set_global_variables(trade, acm.Time.DateAddDelta(DATE_TODAY, 0, 0, -1))
            market_value = CALC_SPACE.CalculateValue(trade, 'SOB Market Value')

            if not isinstance(market_value, float):
                market_value = market_value.Number()
            market_value = abs(market_value)

            if trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID():
                client_sdsid = trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID() 
            else:
                client_sdsid = trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()
            
            if not market_value:
                continue

            trade_data = [APPLICATION_ID,
                          REPORT_FREQUENCY,
                          DATE_TODAY,
                          trade.Oid(),
                          instype if instype != "Deposit" else "Cash",
                          trade.Instrument().Currency().Name() if instype == "Deposit"
                                                               else trade.Instrument().Name().split("/")[1],
                          "",
                          trade.ValueDay(),
                          "",
                          "",
                          ACTIVE_FLAG,
                          ABSA_SDSID if trade.Counterparty().Name().startswith("SLL") else client_sdsid,
                          ABSA_SDSID if trade.Counterparty().Name().startswith("SLB") else client_sdsid,
                          "",
                          "",
                          trade.Instrument().Currency().Name(),
                          market_value,
                          "",
                          MITIGANT_SENIORITY
                         ]

            if not self.is_cash_coll:
                trade_data.extend([trade.Instrument().Isin(),
                                   trade.Instrument().Issuer().Name() if trade.Instrument().Issuer()
                                                                      else trade.Instrument().Security().Name()])
            report_data.append(trade_data)
            self.remove_global_simulations(trade)

        return report_data

    @staticmethod
    def set_global_variables(trade_object, end_date):

        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', end_date)

        CALC_SPACE.SimulateValue(trade_object, 'Valuation Date', end_date)
        CALC_SPACE.SimulateValue(trade_object, 'Valuation Parameter Date', end_date)

    @staticmethod
    def remove_global_simulations(trade_object):

        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')

        CALC_SPACE.RemoveSimulation(trade_object, 'Valuation Date')
        CALC_SPACE.RemoveSimulation(trade_object, 'Valuation Parameter Date')


    def _generate_report(self, report_data, output_file):

        if self.is_cash_coll:
            self.column_headers = self.column_headers[:-2]

        if report_data:
            with open(output_file, 'wb') as file:
                writer = csv.writer(file, delimiter='\t')

                writer.writerow(self.column_headers)
                writer.writerows(report_data)

                LOGGER.info('Report saved to . %s' % str(output_file))
                return

        LOGGER.info("Credit Risk report failed not created for %s. No trades were found." % acm.Time.DateToday())


def ael_main(dictionary):

    file_drop_location = str(dictionary['file_drop_location'])
    is_cash_collateral = dictionary['is_cash_collateral']
    query_folder = dictionary['query_folder']
    filename = str(dictionary['output_filename']) + ".%s.txt" % int(''.join(filter(str.isdigit, acm.Time.DateToday())))
    output_file = os.path.join(file_drop_location, filename)

    credit_risk_processor = CreditRiskReportProcessor(is_cash_collateral)
    trades = query_folder[0].Query().Select()

    report_data = credit_risk_processor._run_data_extraction(trades)
    credit_risk_processor._generate_report(report_data, output_file)

    LOGGER.info("Finished Successfully")
