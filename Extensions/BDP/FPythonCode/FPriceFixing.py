""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_options/etc/FPriceFixing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPriceFixing - Stores price fixings/cut time prices into internal markets.

----------------------------------------------------------------------------"""


import acm
import ael
import FBDPGui
import importlib
importlib.reload(FBDPGui)


ScriptName = 'FPriceFixing'


def insertFixingSource():
    q = acm.CreateFASQLQuery(acm.FParty, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('OR')
    op.AddAttrNode('Type', 'RE_LIKE_NOCASE',
            ael.enum_from_string('PartyType', 'MtM Market'))
    return q


def insertMarket():
    q = acm.CreateFASQLQuery(acm.FParty, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('OR')
    op.AddAttrNode('Type', 'RE_LIKE_NOCASE',
            ael.enum_from_string('PartyType', 'Market'))
    return q


def insertCurrencyPairs():
    q = acm.CreateFASQLQuery(acm.FCurrencyPair, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q


def insertInstruments():
    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('InsType', 'EQUAL', None)
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return q


ttFixingSource = ('Select fixing source (cut time market in which to store '
        'fixing prices)')
ttMarket = 'Select market (external market from which to obtain prices).'
ttCurrencyPairs = ('Select currency pairs for which to obtain fixings/cut '
        'time prices')
ttInstruments = ('Select instruments for which to obtain fixings/cut time '
        'prices')
ttSubscribeTimeout = ('Seconds for which to subscribe to updates after the '
        'start of the task')


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['fixing_source',
                'Fixing source',
                'FParty', None, insertFixingSource(),
                2, 1, ttFixingSource],
        ['market',
                'Market',
                'FParty', None, insertMarket(),
                0, 1, ttMarket],
        ['currency_pairs',
                'Currency pairs',
                'FCurrencyPair', [], insertCurrencyPairs(),
                0, 1, ttCurrencyPairs],
        ['instruments',
                'Instruments',
                'FInstrument', [], insertInstruments(),
                0, 1, ttInstruments],
        ['subscribe_time',
                'Subscription timeout',
                'string', [30], 30,
                0, 0, ttSubscribeTimeout])


def ael_main(execParam):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FPriceFixingPerform
    importlib.reload(FPriceFixingPerform)
    import FBDPCurrentContext

    FBDPCurrentContext.CreateLog(ScriptName,
                      execParam['Logmode'],
                      execParam['LogToConsole'],
                      execParam['LogToFile'],
                      execParam['Logfile'],
                      execParam['SendReportByMail'],
                      execParam['MailList'],
                      execParam['ReportMessageType'])

    FBDPCommon.execute_script(FPriceFixingPerform.perform_fixing, execParam)
