import acm
import xlsxwriter
from at_logging import getLogger
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
from at_ael_variables import AelVariableHandler
ael_variables = AelVariableHandler()

LOGGER = getLogger()
RESULTS_HEADERS = ['Date', 'Bond Trade', 'CDS Trade', 'Deposit Trade', 'CCS Trade', 'CCS PV ZAR', 'Bond PV ZAR',
                   'Depo PV ZAR', 'CDS PV ZAR', 'USD/ZAR Spot', 'Total PV', 'Threshold', 'Fraction', 'Status']
STD_CALC_SPACE_COLL = acm.Calculations().CreateStandardCalculationsSpaceCollection()

ael_variables.add('in_path',
                  label='Input Path',
                  default='/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/Development/Shalini/',
                  multiple=False)
ael_variables.add('input_filename',
                  label='Input file name',
                  default='trigger_note_input_file.xlsx')
ael_variables.add('out_path',
                  label='Output Path',
                  default='/services/frontnt/Task/',
                  multiple=False)
ael_variables.add('result_output_filename',
                  label='Result file name',
                  default='trigger_note_report.xlsx')


def write_xls_file(output_file_location, results_list):
    workbook = xlsxwriter.Workbook(output_file_location)
    worksheet = workbook.add_worksheet()
    row = 0
    for i in (results_list):
        col = 0
        while col < len(i):
            worksheet.write(row, col, i[col])
            col += 1
        row += 1
    workbook.close()    


class ReadTradesFromExcelXLS(SimpleXLSFeedProcessor):
    def __init__(self, file_path):
        self.results_list = []
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)

    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record
        bond_trade = 0
        cds_trade = 0
        deposit_trade = 0
        ccs_trade = 0
        if record_data['BOND']:
            bond_trade = int(record_data['BOND'])
        elif record_data['DEPOSIT'] and record_data['CDS']:
            cds_trade = int(record_data['CDS'])
            deposit_trade = int(record_data['DEPOSIT'])
        ccs_trade = int(record_data['CCS'])
        threshold = int(record_data['THRESHOLD'])
        creator = ThresholdCheck(bond_trade, ccs_trade, cds_trade, deposit_trade, threshold)
        self.results_list = creator.monitor()


class ThresholdCheck(object):

    DATE_TODAY = acm.Time().DateToday()
    result = []
    result.append(RESULTS_HEADERS)             
    conversion_rate = acm.FPrice.Select('instrument = "USD" and currency = "ZAR" and market = "SPOT"')[0].Last()

    def __init__(self, bond_trade, ccs_trade, cds_trade, deposit_trade, threshold):
        self.bond_trade = acm.FTrade[bond_trade]
        self.ccs_trade = acm.FTrade[ccs_trade]
        self.cds_trade = acm.FTrade[cds_trade]
        self.deposit_trade = acm.FTrade[deposit_trade]
        self.threshold = threshold

    def monitor(self):
        ccs_oid = self.ccs_trade.Oid()
        if self.bond_trade and self.ccs_trade:
            pv_ccs_zar = self.ccs_trade.Calculation().PresentValue(STD_CALC_SPACE_COLL).Value().Number()
            pv_bond_usd = self.bond_trade.Calculation().PresentValue(STD_CALC_SPACE_COLL).Value().Number()

            pv_bond_zar = pv_bond_usd * self.conversion_rate

            total_pv = -1*(pv_bond_zar + pv_ccs_zar)
            if total_pv < self.threshold:
                status = 'TERMINATE'
            else:
                status = '-'
				
            fraction = str(((total_pv - self.threshold)/self.threshold)*100) + '%'
            self.result.append([self.DATE_TODAY, self.bond_trade.Oid(), 0, 0, self.ccs_trade.Oid(), pv_ccs_zar,
                                pv_bond_zar, 0, 0, self.conversion_rate, total_pv, self.threshold, fraction, status])

        elif self.cds_trade and self.deposit_trade and self.ccs_trade:
            pv_ccs_zar = self.ccs_trade.Calculation().PresentValue(STD_CALC_SPACE_COLL).Value().Number()
            pv_cds_zar = self.cds_trade.Calculation().PresentValue(STD_CALC_SPACE_COLL).Value().Number()
            pv_deposit_usd = self.deposit_trade.Calculation().PresentValue(STD_CALC_SPACE_COLL).Value().Number()
            pv_deposit_zar = pv_deposit_usd * self.conversion_rate
            total_pv = -1*(pv_deposit_zar + pv_cds_zar + pv_ccs_zar)
            if total_pv < self.threshold:
                status = 'TERMINATE'
            else:
                status = '-'
				
            fraction = str(((total_pv - self.threshold)/self.threshold)*100) + '%'
            self.result.append([self.DATE_TODAY, 0, self.cds_trade.Oid(), self.deposit_trade.Oid(),
                                self.ccs_trade.Oid(), pv_ccs_zar, 0, pv_deposit_zar, pv_cds_zar,
                                self.conversion_rate, total_pv, self.threshold, fraction, status])
        return self.result


def ael_main(ael_dict):
    input_file_location = str(ael_dict['in_path']) + str(ael_dict['input_filename'])
    output_file_location = str(ael_dict['out_path']) + str(ael_dict['result_output_filename'])
    proc = ReadTradesFromExcelXLS(input_file_location)
    proc.add_error_notifier(notify_log)
    proc.process(False)
    results_list = proc.results_list
    try:
        write_xls_file(output_file_location, results_list)
        LOGGER.info("Completed successfully.")
    except Exception as exc:
            LOGGER.exception("Error writing to file: %s", exc)
