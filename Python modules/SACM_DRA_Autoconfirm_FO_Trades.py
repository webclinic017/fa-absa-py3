"""
Business require an automated script to BO confirm specific for Philips trades.
For each trade where the counterparty (CP) is 'DRA TRANSAKSIES', the script checks
if the status field is 'FO confirmed'. The analyst then checks if the Nominal Value
and premium sub-total fields at the bottom half of the report is zero for the corresponding
INSID of the trades that were 'FO Confirmed'. If trade status is FO confirmed and the Nominal Value 
and Premium is zero, the analyst then BO-BO confirms the trades

Date            JIRA              Developer               Requester
==========      ===========       ==================      ======================
2013-12-09      ABITFA-1726       Pavel Saparov           Sipho Ndlalane
2015-05-06      FAU-736           Pavel Saparov           Anwar Banoo
"""
from time import mktime
from datetime import datetime, timedelta
from operator import itemgetter
from itertools import groupby

from at_ael_variables import AelVariableHandler
from auto_confirm import AutoConfirmation as AC


ael_gui_parameters = {'windowCaption': 'SACM DRA Autoconfirm FO Trades'}

ael_variables = AelVariableHandler()

ael_variables.add('trade_filter',
                  mandatory=True,
                  label='Trade Filter',
                  cls='FTradeSelection',
                  default='SACM_DRA_Since_Inception',
                  alt='Select your trade filter with trade population')

ael_variables.add('trade_execution',
                  mandatory=True,
                  label='Trade Time Execution',
                  cls='string',
                  default='-2h',
                  alt='Specify your execution filtering')


class AutoConfirmation:

    # Dictionary of FO trades grouped by security's name
    grouped = dict()

    def __init__(self, trades, exec_delay):
        """Initializer

        Arguments:
        trades -- a list of FTrade objects
        exec_delay -- a string value representing delay (ex: -1s, -2h, -5d)
        """
        td = dict(list(zip(
            ('s', 'm', 'h', 'd', 'w'),
            ('seconds', 'minutes', 'hours', 'days', 'weeks')
        )))

        delta = timedelta(**{td[exec_delay[-1]]: int(exec_delay[:-1])})
        self.exec_delay = mktime((datetime.now() + delta).timetuple())
        self.__group_trades(trades)

    def __group_trades(self, trades):
        """Method groups a list by of FTrade objects by security's
        name also summing up nominal and premium for a group.

        Arguments:
        trades -- a list of FTrade objects
        """
        tmp_trades = list()

        for trade in trades:
            security_name = trade.Instrument().Security().Name()
            tmp_trades.append((security_name, trade))
        tmp_trades.sort(key=lambda t: t[0])

        for k, g in groupby(tmp_trades, key=itemgetter(0)):
            t_list = map(itemgetter(1), g)

            self.grouped[k] = dict()
            self.grouped[k]['fo_trades'] = \
                [t for t in t_list if t.Status() == "FO Confirmed"]
            self.grouped[k]['sum_nominal'] = \
                sum([round(t.Nominal(), 2) for t in t_list])
            self.grouped[k]['sum_premium'] = \
                sum([round(t.Premium(), 2) for t in t_list])

    def bo_confirm_trades(self):
        """Method BO Confirms trades if its security group is equal
        to zero ie. total net position is flat.

        """
        mirror_trades = list()

        for _, g in self.grouped.iteritems():
            if g['sum_nominal'] == 0.0 and g['sum_premium'] == 0.0:
                # iterate through trade list copy and remove
                # mirror trades from the original list, so
                # we can easily BO trades as mirror trades
                # are BO Confirmed automatically
                for trade in g['fo_trades'][:]:
                    mirror = trade.GetMirrorTrade()
                    if (mirror and mirror in g['fo_trades']
                        and trade not in mirror_trades):
                            mirror_trades.append(mirror)
                            g['fo_trades'].remove(mirror)

                # BO Confirm trades without mirror trades
                for trade in g['fo_trades']:
                    if trade.ExecutionTime() <= self.exec_delay:
                        mirror = trade.GetMirrorTrade()

                        if (trade.Portfolio().Name().startswith('Allocate')):
                            print "Skipping BO-BO confirmation as " \
                                  "trade {0} is in Allocate portfolio".format(
                                      trade.Oid())
                            continue
                        elif (mirror and
                              mirror.Portfolio().Name().startswith('Allocate')):
                            print "Skipping BO-BO confirmation as " \
                                  "mirror trade {0} is in Allocate portfolio".format(
                                      mirror.Oid())
                            continue
                        else:
                            try:
                                # FIXME Remove once Prime >= 2015.3 is deployed
                                AC.hotfix_confirm_trade(trade, "BO-BO Confirmed")

                                #trade.Status("BO-BO Confirmed")
                                #trade.Commit()
                                print "Trade {0} was automatically " \
                                      "BO-BO Confirmed".format(trade.Oid())
                            except Exception as e:
                                trade.Undo()
                                print "Unable to BO-BO Confirm " \
                                      "trade {0}".format(trade.Oid())
                                print " Reason: {0}".format(e)
                    else:
                        print "Skipping BO-BO confirmation " \
                              "for trade {0}".format(trade.Oid())


def ael_main(params):

    print "Executing {0}".format(__name__)

    # convert and copy from FPersistentSet to Python list
    trades = list(params['trade_filter'].Trades())
    exec_delay = params['trade_execution']

    # verify valid trades for confirmation
    dra_engine = AutoConfirmation(trades, exec_delay)

    # BO Confirm valid trades
    dra_engine.bo_confirm_trades()

    print "Completed successfully"
