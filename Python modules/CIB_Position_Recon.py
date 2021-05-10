"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CIB_Position_Recon
    
DESCRIPTION
    Date                    : 2019-11-09
    Purpose                 : Consolidation of ZAR payments Recon reports
    Department and Desk     : Post Trade Services
    Requester               : Martin Wortmann
    Developer               : Jaysen Naicker
    CR Number               : 
    

HISTORY
====================================================================================================================================================
Date              CR Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2018-09-20                         Jaysen Naicker         Initial Implementation.
2020-04-17        FAOPS-783        Cuen Edwards           Addition of two new columns and minor inspection fixes/simplifications.
2020-05-13        FAOPS-790        Cuen Edwards           Change to prevent small decimals from being formatted in scientific notation.  Addition of
                                                          two new columns.  Change to determine buy/sell direction using face value instead of buy/
                                                          sell indicator on trade.
2020-05-20        FAOPS-817        Tawanda Mukhalela      Fixed Current Nominal to calculate per trade
----------------------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import os

from at_logging import getLogger
from at_report import CSVReportCreator
from at_ael_variables import AelVariableHandler

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
CALC_SPACE_COLLECTION = acm.Calculations().CreateStandardCalculationsSpaceCollection()
LOGGER = getLogger(__name__)
TODAY = acm.Time().DateToday()


class ReconReport(CSVReportCreator):
    """Creates the report"""
    
    def __init__(self, full_file_path, query_folder, report_date):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)
        self.report_date = report_date
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
        CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.report_date)
        CALC_SPACE.SimulateGlobalValue('Valuation Date', self.report_date)
        trade_grouper = acm.FAttributeGrouper('Trade.Oid')
        cash_value = CALC_SPACE.InsertItem(query_folder)
        cash_value.ApplyGrouper(trade_grouper)
        CALC_SPACE.Refresh()
        super(ReconReport, self).__init__(file_name_only, file_suffix, file_path)
        
    def _collect_data(self):
        """Collect data for this report"""
        LOGGER.info('collecting .... {0}'.format(acm.Time.TimeNow()))
        trade_filter_iterator = CALC_SPACE.RowTreeIterator().FirstChild()
        child_iter = trade_filter_iterator.FirstChild()
        while child_iter:
            item = child_iter.Tree().Iterator().FirstChild()
            while item:
                self.content.append(self._get_row_data(item))
                item = item.NextSibling()  
            child_iter = child_iter.NextSibling()
        CALC_SPACE.RemoveGlobalSimulation('Valuation Date')
        CALC_SPACE.RemoveGlobalSimulation('Valuation Parameter Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
        CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
        CALC_SPACE.Clear()
        LOGGER.info('finished reading data {0}'.format(acm.Time.TimeNow()))

    @staticmethod
    def _get_row_data(item):
        """Collect row data"""
        trade = item.Tree().Item().Trade()
        instrument = trade.Instrument()
        portfolio = trade.Portfolio()
        has_fixed_leg = instrument.IsCashFlowInstrument() and instrument.FirstFixedLeg()
        has_float_leg = instrument.IsCashFlowInstrument() and instrument.FirstFloatLeg()
        face_value = CALC_SPACE.CalculateValue(trade, 'FaceValue')
        current_nominal = CALC_SPACE.CalculateValue(trade, 'Current Nominal')
        row = [
            portfolio.Name(),
            instrument.InsType(),
            instrument.Underlying().InsType() if instrument.Underlying() else '',
            instrument.Name(),
            instrument.Underlying().Name() if instrument.Underlying() else '',
            instrument.FirstFixedLeg().AmortType() if has_fixed_leg else '',
            instrument.FirstFloatLeg().AmortType() if has_float_leg else '',
            trade.SettleCategoryChlItem().Name() if trade.SettleCategoryChlItem() else '',
            str(trade.ExecutionTime()),
            str(trade.TradeTime()),
            str(trade.AcquireDay()),
            instrument.OpenEnd(),
            CALC_SPACE.CalculateValue(item.Tree(), 'Instrument Start Date'),
            str(instrument.ExpiryDate()),
            trade.Oid(),
            trade.GetMirrorTrade().Oid() if trade.GetMirrorTrade() else '',
            trade.TrxTrade().Oid() if trade.TrxTrade() else '',
            trade.Acquirer().Name() if trade.Acquirer() else '',
            trade.Counterparty().Name() if trade.Counterparty() else '',
            instrument.Issuer().Name() if instrument.Issuer() else '',
            instrument.Isin() if len(instrument.Isin()) > 0 else CALC_SPACE.CalculateValue(
                item.Tree(), 'Underlying ISIN'),
            instrument.ExternalId1(),
            instrument.ExternalId2(),
            trade.Currency().Name(),
            'Buy' if face_value > 0 else 'Sell',
            instrument.TotalIssued(),
            '{face_value:.2f}'.format(face_value=face_value),
            '{current_nominal:.2f}'.format(current_nominal=current_nominal),
            CALC_SPACE.CalculateValue(item.Tree(), 'Trade Category'),
            CALC_SPACE.CalculateValue(item.Tree(), 'mmInstype'),
            CALC_SPACE.CalculateValue(item.Tree(), 'InsOverride'),
            CALC_SPACE.CalculateValue(item.Tree(), 'fundingInsTypeAddInfo'),
            CALC_SPACE.CalculateValue(item.Tree(), 'approxLoad'),
            instrument.AdditionalInfo().Demat_Instrument(),
            instrument.AdditionalInfo().DIS_Instrument(),
            portfolio.PortfolioOwner().Name() if portfolio.PortfolioOwner() else '',
            CALC_SPACE.CalculateValue(item.Tree(), 'Instrument End Date'),
            instrument.Underlying().ExternalId1() if instrument.Underlying() else '',
            instrument.Currency().Name(),
            instrument.Underlying().Currency().Name() if instrument.Underlying() else ''
        ]
        return row

    def _header(self):
        """Define column headers for the report """
        field_names = [
            'Portfolio',
            'Instrument Type',
            'Underlying Type',
            'Name',
            'Underlying',
            'FirstFixedLeg.AmortType',
            'FirstFloatLeg.AmortType',
            'SettleCategoryChlItem.Name',
            'ExecutionDate',
            'Trd Time',
            'Acquire Day',
            'Open End',
            'Start Day',
            'Expiry',
            'Trd No',
            'MirrorTrade.Oid',
            'TrxTrade.Oid',
            'Acquirer',
            'Cpty',
            'Issuer',
            'ISIN_UndISIN_Name',
            'External ID 1',
            'External ID 2',
            'TradeCurr',
            'B/S',
            'Total Issue Size',
            'Face Value',
            'Current Nominal',
            'Trade Category',
            'MM Instype',
            'InsOverride',
            'Funding Instype',
            'Approx Load',
            'Demat Instrument',
            'DIS Instrument',
            'Portfolio Owner',
            'Instrument End Date',
            'Underlying External ID 1',
            'Instrument Curr',
            'Underlying Instrument Curr'
        ]
        return field_names


ael_variables = AelVariableHandler()

ael_variables.add_directory(
    'output_directory',
    label='Ouput Directory',
    default=r'/services/frontnt/Task'
)

ael_variables.add(
    'file_name',
    label='File Name',
    default='CIB_Position_Recon.csv'
)

ael_variables.add(
    'query_folder',
    label='Query Folder',
    cls=acm.FStoredASQLQuery,
    collection=sorted(acm.FStoredASQLQuery.Select('')),
    default=acm.FStoredASQLQuery['CIB_Position_Recon']
)

ael_variables.add(
    'date',
    label='Date',
    cls='string',
    default='Today'
)


def ael_main(config):
    LOGGER.msg_tracker.reset()
    file_name = config['file_name']
    report_date = config['date']
    if report_date == 'Today':
        report_date = TODAY
    full_file_path = os.path.join(str(config['output_directory']), file_name)
    query_folder = config['query_folder']
    report = ReconReport(full_file_path, query_folder, report_date)
    LOGGER.info('Generating CIB_Position_Recon report...{0}'.format(acm.Time.TimeNow()))
    report.create_report()
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Output wrote to {0}'.format(full_file_path))
    LOGGER.info('Completed successfully')
