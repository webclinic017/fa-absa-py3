'''-----------------------------------------------------------------------------------------
MODULE
    sbl_bonus_issue_coll_report

DESCRIPTION
    Date                : 2020-01-21
    Purpose             : This will create a Bonus Issues collateral taken-on report for STRATE.
    Department and Desk : SBL Ops
    Requester           : James Stevens
    Developer           : Qaqamba Ntshobane

HISTORY
=============================================================================================
Date            Change no       Developer               Description
---------------------------------------------------------------------------------------------
2020-01-21      PCGDEV-85       Qaqamba Ntshobane       Initial Implementation
2020-04-24      PCGDEV-304      Qaqamba Ntshobane       There is a missing delivery type from
                                                        existing FA list. Implemented a 
                                                        workaround based on business partner 
                                                        value.

ENDDESCRIPTION
------------------------------------------------------------------------------------------'''

import acm
import os
import csv
import string
import at_calculation_space as acs

from at_logging import getLogger
from at_ael_variables import AelVariableHandler


ACQUIRER = 'SECURITY LENDINGS DESK'
OUTPUT_FILENAME = 'STRATE_Collateral_Take-On MNP'
VALID_STATUS = ['FO Confirmed', 'BO Confirmed']
LOGGER = getLogger(__name__)

DIRECTORY_SELECTOR = acm.FFileSelection()
DIRECTORY_SELECTOR.PickDirectory(True)
DIRECTORY_SELECTOR.SelectedDirectory('Y:\Jhb\SL Operations\G1Uploads\PROD\Out')

ael_variables = AelVariableHandler()
ael_variables.add(
    'record_date',
    label = 'Record Date',
    cls = 'date',
    default = acm.Time.DateToday(),
    )
ael_variables.add(
    'output_filename',
    label = 'Output File',
    cls = 'string',
    default = OUTPUT_FILENAME
    )
ael_variables.add(
    'file_drop_location',
    label = 'File Drop Location',
    cls = DIRECTORY_SELECTOR,
    default = DIRECTORY_SELECTOR,
    multiple = True
    )


class StrateCollateralTakeOnExtract(object):

    column_headers = ['CPTY_NAME', 'TRADE_OID', 'ORDR-ISSR', 'ORDR-NO', 'POOL REF', 'GROUP_ISSUER',
                      'GROUP NUMBER', 'LENDING DESK BPID', 'TRDNG-PARTY',
                      'SCA_NO', 'ISIN', 'TAX ID', 'LEND-BRWD-QTY',
                      'TOTAL-RTN-QTY', 'STL_TYP', 'COLL_TYP',
                      'COLL_STA', 'COLL_CRTN_DATE'
                     ]

    def __init__(self, output_file):

        self.output_file = output_file
        self.corpacts = []
        self.strate_collateral_trades = []
        self.report_data = []

    def _get_corpacts(self, record_date):

        return [ca for ca in acm.FCorporateAction.Select("recordDate = '%s' and instrument<>''" % record_date) 
                                                    if (ca.Dividend() or ca.AdditionalInfo().Gross_Taxable_Rate() or ca.Text())]

    def _get_trades(self):

        for corpact in self.corpacts:
            self.strate_collateral_trades.extend(acm.FTrade.Select('acquirer="%s" and valueDay=%s'
                                                        % (ACQUIRER, corpact.SettleDate())))

    def _trading_party(self, sett):

        return (self._business_partner_id(sett) if 
                self._business_partner_id(sett) else 
                acm.FParty[sett.TheirCorrBank()].add_info('CSDP_STRATE_BPID'))

    def _securitities_acc_number(self, sett):

        return '' if self._business_partner_id(sett) else sett.TheirCorrAccount3()

    @staticmethod
    def _business_partner_id(object, type=None):

        if type == 'acquirer':
            return object.Acquirer().add_info('CSDP_STRATE_BPID')
        return object.Counterparty().add_info('CSDP_STRATE_BPID')

    def _is_business_partner(self, trade):

        strate_bpid = self._business_partner_id(trade)
        return strate_bpid not in ('', None)

    def _delivery_type(self, trade):

        delivery_type = ''
        client_name = trade.Counterparty().Name()
        client_type = trade.Counterparty().add_info('SL_CptyType')

        if client_type == 'Borrower':
            delivery_type = 'RFP' if self._is_business_partner(trade) else 'DFP'

        if client_type == 'Lender':
            delivery_type = 'DFP' if self._is_business_partner(trade) else 'RFP'

        return delivery_type

    def _run_data_extraction(self, record_date):

        self.corpacts = self._get_corpacts(record_date)
        self._get_trades()

        for trade in set(self.strate_collateral_trades):
            settlement = acm.FSettlement.Select('trade=%s' % trade.Oid()) 

            if trade.add_info('SL_IsCorpAction') and settlement and trade.Status() in VALID_STATUS:
                settlement = settlement[0]

                self.report_data.append([
                                settlement.CounterpartyName(),
                                trade.Oid(),
                                self._business_partner_id(settlement, 'acquirer'),
                                settlement.Oid(),
                                settlement.Counterparty().add_info('STRATE_POOL_REF'),
                                '',
                                '',
                                self._business_partner_id(settlement, 'acquirer'),
                                self._trading_party(settlement),
                                self._securitities_acc_number(settlement),
                                trade.Instrument().Isin(),
                                'N',
                                abs(acs.calculate_value('FTradeSheet', trade, 'Quantity')),
                                0,
                                self._delivery_type(trade),
                                'Depo',
                                '1',
                                settlement.ValueDay()
                                ])

    def _generate_report(self, record_date):

        if self.report_data:
            with open(self.output_file, 'wb') as file:
                writer = csv.writer(file, lineterminator='\n')

                writer.writerow(self.column_headers)
                writer.writerows(self.report_data)

                LOGGER.info('Report saved to . %s' % str(self.output_file))
                return
        LOGGER.info('No bonus issues to report for %s. No report produced.' % record_date)
    
	
def ael_main(dictionary):

    record_date = dictionary['record_date']
    file_drop_location = str(dictionary['file_drop_location'])
    filename = str(dictionary['output_filename']) + '_%s.csv' % int(''.join(filter(str.isdigit, acm.Time.TimeNow())))
    output_file = os.path.join(file_drop_location, filename)

    coll_trades_extract = StrateCollateralTakeOnExtract(output_file)
    coll_trades_extract._run_data_extraction(record_date)
    coll_trades_extract._generate_report(record_date)
