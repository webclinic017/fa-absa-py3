"""
A report that shows positions on stocks, etfs and security loans for the given
portfolios on dividend dates in the specified time range. Positions are shown
for ldt and ldt+3.

History

Date        Change number       Requester           Developer           Comment
2013-07-16  1171482             Candice Johnson     Jan Sinkora         Initial deployment
2016-11-03  4071788             Sabiha Adam         Libor Svoboda       Updated output format,
                                                                        removed T+5 columns.
2016-11-15  4096068             Sabiha Adam         Libor Svoboda       Optimised the code, refactored.
"""
import acm
import ael
import csv
import os
from at_ael_variables import AelVariableHandler
import at_dbsql
from collections import defaultdict
from datetime import datetime


ZAR_CALENDAR = acm.FInstrument['ZAR'].Calendar()
DATE_TODAY = acm.Time.DateToday()
DATE_YEAR_START = acm.Time.DateFromYMD(acm.Time.DateToYMD(DATE_TODAY)[0], 1, 1)


def change_mode(var_mode):
    """Changes the GUI mode (YTD <-> custom range)."""
    var_start_date = ael_variables.get('start_date')
    var_end_date = ael_variables.get('end_date')

    if var_mode.value == 'YTD':
        var_start_date.enabled = False
        var_end_date.enabled = False
    else:
        var_start_date.enabled = True
        var_end_date.enabled = True


ael_variables = AelVariableHandler()
ael_variables.add(
    'query_folder_include',
    label='Portfolio Query Folder',
    default='Dividends_Accrued_PS_EQD_ACS',
    cls='FStoredASQLQuery',
    collection=acm.FStoredASQLQuery.Select("subType='FPhysicalPortfolio'")
)
ael_variables.add(
    'query_folder_exclude',
    label='Portfolio Query Folder - Exclusions',
    default='Dividends_Accrued_PS_EQD_ACS_Ex',
    cls='FStoredASQLQuery',
    collection=acm.FStoredASQLQuery.Select("subType='FPhysicalPortfolio'")
)
ael_variables.add(
    'outpath',
    label='Output directory'
)
ael_variables.add(
    'filename',
    label='File name'
)
ael_variables.add(
    'date_mode',
    label='Date selection mode',
    default='YTD',
    collection=['YTD', 'Custom'],
    hook=change_mode
)
ael_variables.add(
    'start_date',
    label='Date from',
    cls='date',
    enabled=False,
    default=DATE_YEAR_START
)
ael_variables.add(
    'end_date',
    label='Date to',
    cls='date',
    enabled=False,
    default=DATE_TODAY
)


class ReportCreator(object):

    column_names = (
        'Instrument', 'Div ex date', 'Pay date', 'Record date',
        'Rate', 'Ldt', 'Ldt+3', 'Desk', 'Portfolio', 'Ldt stock position',
        'Ldt loan position', 'Ldt+3 stock position', 'Ldt+3 loan position',
        'Real dividend T3', 'Manufactured dividend T3', 
        'Sum of ZAR value of div T3',
    )

    position_keys = (
        'ldt_stock_pos', 'ldt_loan_pos',
        'ldt_p3_stock_pos', 'ldt_p3_loan_pos',
        'real_div_t3', 'mand_div_t3', 'total_div_t3',
    )
    
    div_info_keys = (
        'date', 'pay_date', 'record_date', 
        'amount', 'ldt', 'ldt_p3',
    )
    
    def __init__(self, from_date, to_date):
        self._from_date = from_date
        self._to_date = to_date
        self._summary = {}
        self._ins_no_divs = []
        self._query_result = []
    
    @classmethod
    def parse_date(cls, s):
        """Parse dates returned from dbsql."""
        db_date_beginning = '1970-01-01 00:00:00'
        db_date_end = '2999-01-01 00:00:00'
    
        if s == db_date_beginning:
            # None is converted to this date by ael.dbsql. Set the big date 
            # instead as this is to be the upper limit.
            s = db_date_end
    
        # Exception not handled intentionally. It would mean that 
        # the db changed behavior.
        result = datetime.strptime(s, '%Y-%m-%d %H:%M:%S').date()
        return result.strftime("%Y-%m-%d")
    
    @classmethod
    def get_portfolios_id_set(cls, portfolios):
        """Returns a set of portfolio database ids (prfnbrs) for the given acm
        entities.
        """
        return set(at_dbsql.portfolio_ids_list(map(lambda p: p.Name(), portfolios)))
    
    @classmethod
    def data_dict(cls):
        return {
            'ldt_stock_pos': 0.0,
            'ldt_loan_pos': 0.0,
            'ldt_p3_stock_pos': 0.0,
            'ldt_p3_loan_pos': 0.0,
            'real_div_t3': 0.0,
            'mand_div_t3': 0.0,
            'total_div_t3': 0.0,
        }
    
    @classmethod
    def calculate_dividends(cls, rate, ldt_stock_position, ldt_loan_position):
        """Returns (real dividend, manufactured dividend)."""
        if ldt_stock_position > 0 and ldt_loan_position >= 0:
            return (ldt_stock_position * rate, 0.0)
        elif ldt_stock_position > 0 and ldt_loan_position < 0:
            return ((ldt_stock_position + ldt_loan_position) * rate,
                    ldt_loan_position * -1 * rate)
        elif ldt_stock_position < 0:
            return (0.0, ldt_stock_position * rate)
        else:
            return (0.0, 0.0)
    
    @classmethod
    def values_at_keys(cls, data, keys):
        return map(lambda key: data[key], keys)

    def get_data(self, portfolios_include, portfolios_exclude):
        """Get the trades via dbsql.
    
        This selects all non-aggregate Stocks, ETFs and Security Loans on Stocks
        and ETFs in the given portfolios. The goal is to not materialize any
        acm/ael entities in the rest of the module.
        """
        prfs_in = self.get_portfolios_id_set(portfolios_include)
        prfs_ex = self.get_portfolios_id_set(portfolios_exclude)
    
        prfs_list = "({0})".format(",".join(map(str, (prfs_in - prfs_ex))))
    
        query = """
        SELECT
            t.trdnbr,
            i.instype,
            sl_insid =
                CASE i.instype
                    WHEN {instype_sl} THEN u.insid
                    ELSE i.insid
                END,
            quantity =
                CASE i.instype
                    WHEN {instype_sl} THEN t.quantity * i.ref_value
                    ELSE t.quantity
                END,
            end_day =
                CASE i.instype
                    WHEN {instype_sl} THEN
                        CASE i.open_end
                            WHEN 1 THEN NULL
                            ELSE l.end_day
                        END
                    WHEN {instype_etf} THEN i.exp_day
                    ELSE NULL
                END,
            t.value_day,
            ai.value,
            p.prfid
        FROM trade AS t
        INNER JOIN portfolio AS p ON p.prfnbr = t.prfnbr
        INNER JOIN instrument AS i ON t.insaddr = i.insaddr
        LEFT JOIN instrument AS u ON i.und_insaddr = u.insaddr
        LEFT JOIN leg AS l ON (i.instype = {instype_sl} AND i.insaddr = l.insaddr)
        LEFT JOIN additional_info AS ai ON (ai.addinf_specnbr = {addinf_specnbr} AND ai.recaddr = t.prfnbr)
        WHERE t.prfnbr IN {prfs_list}
        AND (i.instype IN {sec_instypes} OR (i.instype = {instype_sl} AND u.instype IN {sec_instypes}))
        AND t.value_day < '{to_date}'
        AND t.aggregate = 0
        AND t.status NOT IN {statuses}
        """.format(instype_sl=at_dbsql.enum.instype('SecurityLoan'),
                   instype_etf=at_dbsql.enum.instype('ETF'),
                   addinf_specnbr=acm.FAdditionalInfoSpec['SL_AllocatedDesk'].Oid(),
                   prfs_list=prfs_list,
                   sec_instypes=at_dbsql.enum.instype('Stock', 'ETF'),
                   to_date=self._to_date,
                   statuses=at_dbsql.enum.tstatus('Simulated', 'Void', 'Confirmed Void'))
        self._query_result = ael.dbsql(query)[0]
    
    def _get_dividends(self, instrument):
        dividends = []
        for div in instrument.Dividends():
            date = div.ExDivDay()
            ldt = ZAR_CALENDAR.AdjustBankingDays(date, -1)
            if ldt < self._from_date or ldt > self._to_date:
                continue

            ldt_p3 = ZAR_CALENDAR.AdjustBankingDays(ldt, 3)
            dividends.append({
                 'id': div.Oid(),
                 'amount': div.Amount(),
                 'date': date,
                 'pay_date': div.PayDay(),
                 'record_date': div.RecordDay(),
                 'ldt': ldt,
                 'ldt_p3': ldt_p3,
                 'desks': defaultdict(lambda: defaultdict(self.data_dict))
            })
        return dividends
        
    def prepare_data(self):
        """Converts values to the right types and prepares data for calculation.
        """
        for row in self._query_result:
            # Prepare the trade data - process values from ael.dbsql.
            trd_data = dict(list(zip(['trdnbr', 'instype', 'sl_insid', 'quantity',
                'end_day', 'value_day', 'sl_allocated_desk', 'prfid'], row)))
            trd_data['end_day'] = self.parse_date(trd_data['end_day'])
            trd_data['value_day'] = self.parse_date(trd_data['value_day'])
            trd_data['quantity'] = float(trd_data['quantity'])
            trd_data['instype'] = str(acm.EnumToString('InsType', int(trd_data['instype'])))
            if not trd_data['sl_allocated_desk']:
                trd_data['sl_allocated_desk'] = 'No SL. Desk'
            
            ins = acm.FInstrument[trd_data['sl_insid']]
            if not ins:
                raise RuntimeError("Instrument %s not found." % trd_data['sl_insid'])
            if ins.Name() in self._ins_no_divs:
                continue
            if ins.Name() not in self._summary:
                dividends = self._get_dividends(ins)
                if dividends:
                    self._summary[ins.Name()] = dividends
                else:
                    self._ins_no_divs.append(ins.Name())
                    continue
            for div in self._summary[ins.Name()]:
                prf_summary = div['desks'][trd_data['sl_allocated_desk']][trd_data['prfid']]
                ldt = div['ldt']
                ldt_p3 = div['ldt_p3']
                if (ldt >= trd_data['value_day'] and
                    (not trd_data['end_day'] or ldt < trd_data['end_day'])):
                    # The trade falls into this dividend's ldt bucket.
                    if trd_data['instype'] == 'Stock':
                        prf_summary['ldt_stock_pos'] += trd_data['quantity']
                    elif trd_data['instype'] == 'SecurityLoan':
                        prf_summary['ldt_loan_pos'] += trd_data['quantity']
                
                if (ldt_p3 >= trd_data['value_day'] and
                    (not trd_data['end_day'] or ldt_p3 < trd_data['end_day'])):
                    # The trade falls into this dividend's ldt+3 bucket.
                    if trd_data['instype'] == 'Stock':
                        prf_summary['ldt_p3_stock_pos'] += trd_data['quantity']
                    elif trd_data['instype'] == 'SecurityLoan':
                        prf_summary['ldt_p3_loan_pos'] += trd_data['quantity']
    
    def calculate_data(self):
        """Calculates portfolio level dividend values."""
        for insid, divs in self._summary.iteritems():
            for div in divs:
                for desk, desk_summary in div['desks'].iteritems():
                    for prf_name, prf_summary in desk_summary.iteritems():
                        real_div_t3, mand_div_t3 = self.calculate_dividends(div['amount'],
                            prf_summary['ldt_p3_stock_pos'],
                            prf_summary['ldt_p3_loan_pos'])
                
                        prf_summary['real_div_t3'] = real_div_t3
                        prf_summary['mand_div_t3'] = mand_div_t3
                        prf_summary['total_div_t3'] = real_div_t3 + mand_div_t3
    
    def save_csv(self, file_path):
        """Saves the csv with the final report."""
        with open(file_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
    
            # Write the header.
            csvwriter.writerow(self.column_names)
    
            for insid, divs in sorted(self._summary.iteritems()):
                for div in sorted(divs, key=lambda x: x['date']):
                    for desk, desk_summary in sorted(div['desks'].iteritems()):
                        for prf_name, prf_summary in sorted(desk_summary.iteritems()):
                            csvwriter.writerow(
                                [insid] +
                                self.values_at_keys(div, self.div_info_keys) + 
                                [desk] +
                                [prf_name] + 
                                self.values_at_keys(prf_summary, self.position_keys)
                            )


def ael_main(ael_dict):
    query_folder_include = ael_dict['query_folder_include']
    query_folder_exclude = ael_dict['query_folder_exclude']
    date_mode = ael_dict['date_mode']
    if date_mode == 'YTD':
        from_date = DATE_YEAR_START
        to_date = DATE_TODAY
    else:
        from_date = str(ael_dict['start_date'])
        to_date = str(ael_dict['end_date'])

    outpath = ael_dict['outpath']
    filename = ael_dict['filename']

    prfs_in = query_folder_include.Query().Select()
    prfs_ex = query_folder_exclude.Query().Select()
    
    report_creator = ReportCreator(from_date, to_date)
    
    # Pull data from dbsql.
    print 'Get data started', acm.Time.TimeNow()
    report_creator.get_data(prfs_in, prfs_ex)
    print 'Get data finished', acm.Time.TimeNow()

    # Convert value types and group data.
    report_creator.prepare_data()
    print 'Prepare data finished', acm.Time.TimeNow()

    # Calculate the aggregated values.
    report_creator.calculate_data()
    print 'Calculate data finished', acm.Time.TimeNow()

    # Save the report.
    full_path = os.path.join(outpath, filename)
    report_creator.save_csv(full_path)

    print "Wrote secondary output to " + full_path
    print "completed successfully"

