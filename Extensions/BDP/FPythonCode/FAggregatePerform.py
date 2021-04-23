""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FAggregatePerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
import importlib
"""----------------------------------------------------------------------------
MODULE
    FAggregatePerform - Module which executes the aggregation

DESCRIPTION
    This module executes the Aggregation procedure based on the
    parameters passed from the script FAggregation.

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import os
import sys
import time
import traceback


import acm


import FBDPCommon
from FBDPValidation import FBDPValidate
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


def perform_aggregation(dictionary):
    Summary()
    aggregation = FAggregatePerform()
    isDiffOk = aggregation.perform_aggregation(dictionary)
    if dictionary['diff_test']:
        if not isDiffOk:
            raise Exception('P/L values differs')

class FAggregatePerform(FBDPValidate):
    def createPath(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print('Created report output directory:', path)
            except:
                print('Failed to create report directory:' + path)
                raise

    def validateValuationParams(self):
        return True

    def perform_aggregation(self, dictionary):
        if dictionary['sheet_names'] and not dictionary['sheet_templates']:
            Logme()("None of the typed sheet names represent valid sheets of "
                    "the workbook. Using default columns.", "WARNING")

        diffTest = False
        if dictionary.get('diff_test'):
            if dictionary['diff_test']:
                diffTest = True
        day = FBDPCommon.toDate(dictionary.get('date'))
        Logme()('Aggregation date:%s' % str(day))

        report_path = dictionary.get('report_path')
        if diffTest:
            self.createPath(report_path)
            if os.path.isdir(report_path):
                report_path += os.sep
                report_path += "report" + time.strftime('%d%m%y') + os.sep
                dictionary['report_path'] = report_path
            else:
                Logme()('Report Directory Path %s is not a directory.' %
                        report_path, 'ERROR')
                return

        # Find out the aggregation rule filters in use.
        # For "filters", None represents "all".
        # For "fltnbrs", each individual filter number required must be
        # found, and sorted in the ascending order of aggregation rule
        # number/name.
        filters = None
        fltnbrs = None
        if ('aggrule_filters' in dictionary and dictionary['aggrule_filters']):
            filters = dictionary['aggrule_filters']
            # Find all filter numbers in the 'right' ordering, and only keep
            # those specified.
            allFltnbrs = [aggRule.Fltnbr() for aggRule
                                           in acm.FAggregationRule.Instances()]
            fltnbrs = [fltnbr for fltnbr in allFltnbrs
                              if fltnbr in dictionary['aggrule_filters']]
        else:
            filters = None
            fltnbrs = [aggRule.Fltnbr() for aggRule
                                        in acm.FAggregationRule.Instances()]

        self.make_report("portfolio_report_before_aggregation",
                         fltnbrs, dictionary)

        Logme()('Aggregating...')
        acm.PollDbEvents()
        # Logmode: 0,1,2 -> aggregation flag Verbose: 1,2,3
        log_agg = int(dictionary['Logmode'])
        poll_agg = 1
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        bypassTradeValidation = dictionary.get('bypassTradeValidation', 0)
        result = acm.AggregateTrades(day, log_agg, poll_agg,
                useSelectedFundingDay, filters, bypassTradeValidation)
        self.show_result(result, dictionary)
        self.make_report("portfolio_report_after_aggregation",
                         fltnbrs, dictionary)

        is_ok = self.make_diff_report(fltnbrs, dictionary)
        Logme()(None, 'FINISH')
        return is_ok

    def pluralize(self, nr, obj):
        return '%s %s' % (nr, obj + (((nr > 1) and 's') or ''))

    def show_result(self, resDic, dictionary):
        if resDic['error']:
            Logme()('Failed to aggregate: %s' % resDic['error'], 'ERROR')
        else:
            aggRes = resDic['agg_info_per_rule']
            nr_rules_processed = 0
            nr_of_trades_excluded = 0
            nr_archived_trades = 0
            nr_dearchived_trades = 0
            nr_fwd_val_trades = 0
            nr_aggregates_created = 0
            nr_aggregates_changed = 0
            nr_aggregates_deleted = 0
            nr_aggregated_positions = 0
            nr_deaggregated_positions = 0
            Logme()("Aggregation finished.", "INFO")

            class DummyRule:
                def RecordType(self):
                    return "AggRule"

            class DummyAgg:
                def RecordType(self):
                    return "Aggregate"

            class DummyPos:
                def RecordType(self):
                    return "Position"

            class DummyTrade:
                def RecordType(self):
                    return "Trade"
            r = DummyRule()
            a = DummyAgg()
            t = DummyTrade()
            p = DummyPos()

            for ruleRes in aggRes:
                Logme()("*" * 27, "NOTIME")
                Logme()('Summary for aggrule %s' % ruleRes['rule'],
                        'NOTIME_INFO')
                Logme()("*" * 27, "NOTIME")
                if ruleRes['error']:
                    Summary().fail(r, Summary().PROCESS, ruleRes['error'],
                            ruleRes['rule'])
                    Logme()(ruleRes['error'], 'ERROR')
                if ruleRes['warning']:
                    Summary().warning(r, Summary().PROCESS,
                            ruleRes['warning'], ruleRes['rule'])
                    Logme()(ruleRes['warning'], 'WARNING')
                if ruleRes['ignore']:
                    Summary().ignore(r, Summary().PROCESS, ruleRes['ignore'],
                            ruleRes['rule'])
                    Logme()(ruleRes['ignore'], 'INFO')
                if ruleRes.HasKey('PLReportDate'):
                    reportDate = ruleRes['PLReportDate']
                    options = ['REPORT_DATE_NONE', 'REPORT_DATE_TODAY',
                            'REPORT_DATE_INSTRUMENT_SPOT',
                            'REPORT_DATE_GROUPING_SPOT']
                    dictionary['PLReportDate'] = options[reportDate]
                if ruleRes.HasKey('PeriodicAggregation'):
                    aggPeriod = ruleRes['PeriodicAggregation']
                    options = ['None', 'Yearly', 'Monthly', 'Weekly', 'Daily']
                    dictionary['PeriodicAggregation'] = options[aggPeriod]
                if ruleRes['nr_of_trades_excluded'] > 0:
                    nr = ruleRes['nr_of_trades_excluded']
                    Logme()('Excluded %s due to Trade Status.' %
                            self.pluralize(nr, 'trade'), 'NOTIME_INFO')
                    nr_of_trades_excluded += nr
                if ruleRes['nr_aggregated_positions'] > 0:
                    nr = ruleRes['nr_aggregated_positions']
                    Logme()('Aggregated %s.' % self.pluralize(nr, 'position'),
                            'NOTIME_INFO')
                    nr_aggregated_positions += nr
                if ruleRes['nr_deaggregated_positions'] > 0:
                    nr = ruleRes['nr_deaggregated_positions']
                    Logme()('Deaggregated %s.' % self.pluralize(nr,
                            'position'), 'NOTIME_INFO')
                    nr_deaggregated_positions += nr
                if ruleRes.HasKey('position_results'):
                    nr_rules_processed += 1
                    for posRes in ruleRes['position_results']:
                        posName = ('(Instrument="{0}", Portfolio='
                                '"{1}")'.format(posRes['Instrument'],
                                posRes['Portfolio']))
                        if ((Logme().LogMode >= 1) or posRes.HasKey('error') or
                                posRes.HasKey('warning')):
                            Logme()("%s:" % posName, "NOTIME_INFO")
                        if posRes['nr_fwd_val_trades'] > 0:
                            nr = posRes['nr_fwd_val_trades']
                            Logme()("   Excluded %s due to forward value." %
                                    self.pluralize(nr, 'trade'), 'NOTIME_INFO')
                            nr_fwd_val_trades += nr
                        if posRes['nr_archived_trades'] > 0:
                            nr = posRes['nr_archived_trades']
                            Logme()("   Archived %s." % self.pluralize(nr,
                                    'trade'), 'NOTIME_INFO')
                            nr_archived_trades += nr
                        if posRes['nr_dearchived_trades'] > 0:
                            nr = posRes['nr_dearchived_trades']
                            Logme()("   Dearchived %s." % self.pluralize(nr,
                                    'trade'), 'NOTIME_INFO')
                            nr_dearchived_trades += nr
                        if posRes['nr_aggregates_created'] > 0:
                            nr = posRes['nr_aggregates_created']
                            Logme()("   Created %s." % self.pluralize(nr,
                                    'aggregate trade'), 'NOTIME_INFO')
                            nr_aggregates_created += nr
                        if posRes['nr_aggregates_changed'] > 0:
                            nr = posRes['nr_aggregates_changed']
                            Logme()("   Changed %s." % self.pluralize(nr,
                                    'aggregate trade'), 'NOTIME_INFO')
                            nr_aggregates_changed += nr
                        if posRes['nr_aggregates_deleted'] > 0:
                            nr = posRes['nr_aggregates_deleted']
                            Logme()("   Deleted %s." % self.pluralize(nr,
                                    'aggregate trade'), 'NOTIME_INFO')
                            nr_aggregates_deleted += nr
                        if posRes.HasKey('IgnoredTrade'):
                            Logme()(posRes['IgnoredTrade'], 'NOTIME_INFO')
                        if posRes.HasKey('error'):
                            Logme()(posRes['error'], 'ERROR')
                            Summary().fail(p, Summary().AGGREGATE,
                                    posRes['error'], posName)
                        if posRes.HasKey('warning'):
                            Logme()(posRes['warning'], 'ERROR')
                            Summary().warning(p, Summary().AGGREGATE,
                                    posRes['error'], posName)
            Summary().ok(r, Summary().PROCESS, None, nr_rules_processed)
            Summary().ok(t, Summary().ARCHIVE, None, nr_archived_trades)
            Summary().ok(t, Summary().DEARCHIVE, None, nr_dearchived_trades)
            Summary().ok(t, Summary().EXCLUDE, None, (nr_of_trades_excluded +
                    nr_fwd_val_trades))
            Summary().ok(a, Summary().CREATE, None, nr_aggregates_created)
            Summary().ok(a, Summary().UPDATE, None, nr_aggregates_changed)
            Summary().ok(a, Summary().DELETE, None, nr_aggregates_deleted)
            Summary().ok(p, Summary().AGGREGATE, None, nr_aggregated_positions)
            Summary().ok(p, Summary().DEAGGREGATE, None,
                    nr_deaggregated_positions)
            Summary().log(dictionary)

    def make_report(self, file_name, fltnbrs, dictionary):

        # If diff_test not set, don't need to make any report
        if not dictionary['diff_test']:
            return
        # Set report name
        if 'before' in file_name:
            report_name = 'Before aggregation'
        else:
            report_name = 'After aggregation'
        Logme()('', 'NOTIME')
        Logme()('Generating Portfolio Reports...')
        # Redirect output during comparison run.
        old = sys.stdout
        r = self.RedirectLoggingToStream(sys.stdout)
        sys.stdout = r
        try:
            import FAggregationPortfolioCompare
            importlib.reload(FAggregationPortfolioCompare)

            fltnbrGrouperPairList = \
                FAggregationPortfolioCompare.\
                    get_aggregation_rule_fltnbr_grouper_pair_list(fltnbrs)
            FAggregationPortfolioCompare.run_portfolio_reports(
                                             fltnbrGrouperPairList,
                                             dictionary['report_path'],
                                             file_name,
                                             dictionary['used_context'],
                                             dictionary['sheet_templates'],
                                             report_name,
                                             0)
        except:
            sys.stdout = old
            traceback.print_exc(file=sys.stdout)
        sys.stdout = old
        Logme()('Done.')

    def make_diff_report(self, fltnbrs, dictionary):
        is_ok = True
        # If diff_test not set, no report to compare, always return okay.
        if not dictionary['diff_test']:
            return is_ok
        # Get all the aggregation rules' filter numbers in the ascending order
        # of the aggregation rule number/name.  Then remove those not
        # specified by the filter.  This keeps the filter number sorted in the
        # ascending order of aggregation rule/name.  Note, no filter is
        # specified at all, we use all aggregation rule fitlers.
        allAggRuleFltnbrList = [aggRule.Fltnbr() for aggRule
                                in acm.FAggregationRule.Instances()]
        if not dictionary['aggrule_filters']:
            fltnbrList = allAggRuleFltnbrList
        else:
            fltnbrList = [fltnbr for fltnbr in allAggRuleFltnbrList
                                 if fltnbr in dictionary['aggrule_filters']]

        import FAggregationPortfolioCompare
        # Run report comparison
        Logme()('', 'NOTIME')
        Logme()('Comparing Portfolio Reports:')
        fltnbrGrouperPairList = FAggregationPortfolioCompare.\
                get_aggregation_rule_fltnbr_grouper_pair_list(fltnbrList)
        result = FAggregationPortfolioCompare.compare_reports(
                     fltnbrGrouperPairList,
                     dictionary['report_path'],
                     'portfolio_report_before_aggregation',
                     'portfolio_report_after_aggregation',
                     float(dictionary['absolute_precision']),
                     float(dictionary['relative_precision']),
                     dictionary['ignore_precision'])
        # No result means no difference between two report.
        if result:
            Logme()('Some differences were found during the profit and loss '
                  'comparison')
            Logme()('Generating Diff Reports...')
            resultLines = result.split('\n')
            for line in resultLines:
                Logme()(line, 'DEBUG')
            Logme()('Done.')
            is_ok = False
        else:
            Logme()('All profit and loss values were the same before and '
                    'after aggregation.')
        # Return the value of is_ok.
        return is_ok

    class RedirectLoggingToStream:
        def __init__(self, stdout):
            self.stdout = stdout

        def write(self, string):
            if string != '\n':
                sys.stdout = self.stdout
                Logme()(string, "DEBUG")
                sys.stdout = self
