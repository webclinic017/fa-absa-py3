""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FSetFinalExercisePrices.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FSetFinalExercisePrices - Sets the final settlement prices in all
    Exercise/Assign/Abandon trades done on the specified date.

DESCRIPTION
    Sets the final settlement price from the exchange into trades with trade
    type Exercise, Assign (Options and Warrants) and Closing (Future/Forward)
    made on the date specified as input. The premium of the trades are updated
    accordingly.

    When instrument is cash-settled the final settlement prices from the
    exchange should be stored on the MtM Market called "SETTLEMENT", from which
    they are selected in this script. If no price is available on the
    "SETTLEMENT" market, the MtM-price will be used instead.

    If physical delivery is used, the settlement trade could either be done to
    the strike price or to the market price. The closing trade of the option
    (with trade type Exercise/Assign/Abandon) should then get a price
    according to the method.

    If cash delivery is used, the choice of Strike or Market does not matter.
    The market price will be used in the closing trade no matter what mode is
    selected.

DATA-PREP
    A Party of type MtM Market and with the name "SETTLEMENT" is required.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import ael


import FBDPGui
import importlib


ScriptName = 'SetFinalExercisePrices'


Date = FBDPGui.FBDPParameters().Date
if Date == "Today":
    display_day = "Today"
else:
    diff = Date
    if diff > 0:
        diff = '+ ' + str(diff)
    display_day = 'Today ' + str(diff) + ' days'


ttDate = 'Date'
ttMode = 'Exercise mode'


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['date',
                'Date',
                'string', [str(ael.date_today()), 'Today'], display_day,
                1, 0, ttDate, None, None],
        ['mode',
                'Exercise Mode',
                'string', ['Market', 'Strike'], 'Strike',
                2, 0, ttMode, None, None]
        )


def ael_main(execParam):

    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPInstrument
    importlib.reload(FBDPInstrument)
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
            execParam['Logmode'],
            execParam['LogToConsole'],
            execParam['LogToFile'],
            execParam['Logfile'],
            execParam['SendReportByMail'],
            execParam['MailList'],
            execParam['ReportMessageType'])
    import FExeAssPerform
    importlib.reload(FExeAssPerform)
    import FSetFinalExePrcPerform
    importlib.reload(FSetFinalExePrcPerform)

    FBDPCurrentContext.Logme()(None, 'START')

    execParam['date'] = FBDPCommon.toDate(execParam['date'])
    pr_trades = FSetFinalExePrcPerform.get_trades(execParam['date'])
    FSetFinalExePrcPerform.set_final_settle_prices(pr_trades,
            execParam['date'], execParam['mode'], int(execParam['Testmode']))

    FBDPCurrentContext.Logme()(None, 'FINISH')
