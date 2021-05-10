"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SBL_Trades_STRATE
    
DESCRIPTION
    Date                    : 2020-01-10
    Purpose                 : Prepare report of trades for STRATE
    Department and Desk     : PCG
    Requester               : Gasant Thulsie
    Developer               : Jaysen Naicker

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2020-01-10                         Jaysen Naicker         Initial Implementation.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""
import acm
import os

from at_logging import getLogger
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler
from FSettlementHooks import GetMTMessage

ACQUIRER = acm.FParty['SECURITY LENDINGS DESK']
AI_SPEC = acm.FAdditionalInfoSpec['CSDP_STRATE_BPID']
LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()
VALID_SETTLEMENTS_MT = ('540', '542')


def find_first_trade(trade):
    trx_trade = trade.TrxTrade()
    mirror_trade = trade.GetMirrorTrade()
    if trade.Oid() == trx_trade.Oid() or (mirror_trade and mirror_trade.Oid() != trx_trade.Oid()):
        return trade
    else:
        trade = trx_trade
        return find_first_trade(trade)


def is_borrow(trade, settlement):
    return trade.AdditionalInfo().SL_G1Counterparty1() == settlement.CounterpartyName()


def is_lender(trade, settlement):
    return trade.AdditionalInfo().SL_G1Counterparty2() == settlement.CounterpartyName()


def get_ORDER_NO(settlement, first_trade):
    for settle in first_trade.Settlements():
        if settlement.Type() == settle.Type() and settle.Status() != 'Void':
            if settlement.Counterparty().Oid() == settle.Counterparty().Oid():
                return settle.Oid()
    return settlement.Oid()


def get_STLMT_TYPE(trade, settlement):
    ai_value = settlement.Counterparty().AddInfoValue(AI_SPEC)
    # Borrower logic
    if is_borrow(trade, settlement):
        return 'RFP' if ai_value in ('', None) else 'DFP'
    # Lender logic
    if is_lender(trade, settlement):
        return 'DFP' if ai_value in ('', None) else 'RFP'
    return ''


def get_ISSR_LNDG_DESK(trade, settlement):
    ai_value = settlement.Counterparty().AddInfoValue(AI_SPEC)
    # Borrower logic
    if is_borrow(trade, settlement):
        return ai_value if ai_value not in ('', None) else ''
    # Lender logic
    if is_lender(trade, settlement):
        return ai_value if ai_value not in ('', None) else ''
    return ''


def get_TRDNG_PARTY(settlement):
    if settlement.TheirCorrBank() and not settlement.Counterparty().AddInfoValue(AI_SPEC):
        return acm.FParty[settlement.TheirCorrBank()].AddInfoValue(AI_SPEC) 
    else:
        return ''


def get_LEND_BRWD_QTY(trade):
    instrument = trade.Instrument()
    # New trade logic
    if trade.ValueDay() <= TODAY and instrument.OpenEnd() == 'Open End':
        return trade.FaceValue() 
    # Partial trade logic
    trx_trade = trade.TrxTrade()
    while trx_trade is not None:
        if trx_trade.ValueDay() <= TODAY and instrument.OpenEnd() == 'Terminated' and instrument.ExpiryDate() > TODAY:
            return round(trx_trade.FaceValue(), 2)
        trade = trx_trade
        trx_trade = trade.TrxTrade()
    raise ValueError("Trans Ref not set on initial trade.")


def get_TO_BE_RTN_QTY(trade):
    if trade.ValueDay() > TODAY and trade.Instrument().OpenEnd() == 'Open End':
        return trade.AddInfoValue('SL_ReturnedQty')
    else:
        return 0


class ReconReport(CSVReportCreator):
    """Creates the report"""
    def __init__(self, in_file_name, query_folder, report_date):
        file_name = os.path.basename(in_file_name)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(in_file_name)
        self.report_date = report_date
        self.query_folder = query_folder
        self.settlement = None
        self.trade = None
        self.first_trade = None
        super(ReconReport, self).__init__(file_name_only, file_suffix, file_path)

    def _collect_data(self):
        """Collect data for this report"""
        LOGGER.info('collecting .... {0}'.format(acm.Time.TimeNow()))
        trades = self.query_folder.Query().Select()
        for trade in trades:
            self.trade = trade
            self.first_trade = trade.Contract()
            settlements = trade.Settlements()
            for settlement in settlements:
                self.settlement = settlement
                if GetMTMessage(self.settlement, '') in VALID_SETTLEMENTS_MT:
                    if not self.settlement.IsChildInHierarchy():
                        if self.first_trade.Instrument().StartDate() <= TODAY:
                            self.content.append(self._get_row_data())
        LOGGER.info('finished reading data {0}'.format(acm.Time.TimeNow()))

    def _get_row_data(self):
        """Collect row data"""
        row = [ 
                self.settlement.Counterparty().Name(),
                ACQUIRER.AddInfoValue(AI_SPEC),
                get_ORDER_NO(self.settlement, self.first_trade),
                ACQUIRER.AddInfoValue(AI_SPEC),
                self.first_trade.Oid(),
                self.trade.Oid(),
                get_ISSR_LNDG_DESK(self.trade, self.settlement),
                get_TRDNG_PARTY(self.settlement),
                '' if get_ISSR_LNDG_DESK(self.trade, self.settlement) else self.settlement.TheirCorrAccount3(),
                self.first_trade.Instrument().Underlying().Isin() if self.first_trade.Instrument().Underlying() else '',
                abs(get_LEND_BRWD_QTY(self.trade)),
                '0',
                '0',
                get_STLMT_TYPE(self.trade, self.settlement),
                'LOAN',
                '1',
                '0',
                self.first_trade.Instrument().StartDate(),
                'N'
                ]
        return row

    def _header(self):
        """Define column headers for the report """
        field_names = [
            'COUNTERPARTY',
            'ORDR_ISSR',
            'ORDR_NO',
            'GROUP_ISSR',
            'GROUP_NO',
            'TRADE_NO',
            'ISSR_LNDG_DESK',
            'TRDNG_PARTY',
            'SCA_NO',
            'ISIN',
            'LEND_BRWD_QTY',
            'TO_BE_RTN_QTY',
            'TOTAL_RTN_QTY',
            'STLMT_TYPE',
            'LOAN_TYPE',
            'LOAN_STA',
            'STLMT_AMT',
            'LOAN_CRTN_DATE',
            'LOAN_TAX_IND'
        ]
        return field_names


ael_variables = AelVariableHandler()

ael_variables.add_directory(
        'output_directory',
        label='Ouput Directory',
        default=r'/services/frontnt/Task')

ael_variables.add(
        'file_name',
        label='File Name',
        default='SBL_Trades_STRATE.csv')

ael_variables.add(
        'query_folder',
        label='Query Folder',
        cls=acm.FStoredASQLQuery,
        collection=sorted(acm.FStoredASQLQuery.Select('')),
        default=acm.FStoredASQLQuery['SBL_Trades_STRATE'])

ael_variables.add(
        'date',
        label='Date',
        cls='string',
        default='Today')


def ael_main(config):
    LOGGER.msg_tracker.reset()
    file_name = config['file_name']
    report_date = config['date']
    if report_date == 'Today': 
        report_date = TODAY
    full_file_path = os.path.join(str(config['output_directory']), file_name)
    query_folder = config['query_folder']
    report = ReconReport(full_file_path, query_folder, report_date)
    LOGGER.info('Generating SBL_Trades_STRATE report...{0}'.format(acm.Time.TimeNow()))
    report.create_report()
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Output wrote to {0} at {1}'.format(full_file_path, acm.Time.TimeNow()))
    LOGGER.info('Completed successfully')
