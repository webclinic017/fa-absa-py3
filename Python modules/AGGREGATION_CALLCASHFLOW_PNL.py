"""
Date                    : 2019/05/09
Purpose                 : Generate file with volumes for cashflows, settlements and confirmations for data maintenance MI reports
Department and Desk     : IT - Data Maintenance
Requester               : Gerhard Engelbrecht
Developer               : Bhavnisha Sarawan

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
"""

import os
from datetime import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_report import CSVReportCreator

context = acm.GetDefaultContext()
CALC_SPACE = acm.Calculations().CreateCalculationSpace( context, 'FTradeSheet')
LOGGER = getLogger(__name__)

class DepositCashflowVolumesReport(CSVReportCreator):

    def __init__(self, instruments, file_name, file_suffix, path):
        super(DepositCashflowVolumesReport, self).__init__(file_name, file_suffix, path)

        self.instruments = instruments

    def _collect_data(self):
        for ins in self.instruments:
            name = ins.Name()
            port = 'N/A'
            balance = 'N/A'
            sett_int = 'N/A'
            cashflows = ins.Legs()[0].CashFlows()
            c_size = cashflows.Size() # Includes Redemption Amount cashflow
            num_of_confirmations = 0
            num_of_settlements = 0
            
            if ins.Trades():
                first_trade = ins.Trades()[0]
                if first_trade.Portfolio():
                    port = first_trade.Portfolio().Name()
                balance = CALC_SPACE.CalculateValue(first_trade, 'Deposit balance').Number()
                sett_int = CALC_SPACE.CalculateValue(first_trade, 'Portfolio Settled Interest').Number()

                num_of_confirmations = first_trade.Confirmations().Size()
                num_of_settlements = first_trade.Settlements().Size()
            
            line = (
                name,
                port,
                balance,
                sett_int,
                c_size,
                num_of_confirmations,
                num_of_settlements
            )

            self.content.append(line)

    def _header(self):
        header = [
            'Instrument',
            'Portfolio',
            'Balance',
            'Settled Interest',
            'Num of Cashflows',
            'NumOfConfirmations',
            'NumOfSettlements'
        ]

        return header

ael_variables = AelVariableHandler()
ael_variables.add('filename', label='Filename',
    default='AGGREGATION_CALLCASHFLOW_PNL', alt='Filename')

ael_variables.add('path', label='Path',
    default='/services/frontnt/Task', alt='Path')


def ael_main(config):
    instruments = acm.FStoredASQLQuery['FA_MI_CallCashflowVolumesReport'].Query().Select()
    full_filename = config['filename'] + str(datetime.now().strftime('%y%m%d%H%M%S'))
    report = DepositCashflowVolumesReport(instruments,
        file_name=full_filename, file_suffix='csv',
        path=config['path'])

    LOGGER.info('Generating deposit cashflow stats report')
    report.create_report()
    
    LOGGER.info('Wrote secondary output to {0}'.format(report._full_path))
    LOGGER.info('Completed Successfully')
