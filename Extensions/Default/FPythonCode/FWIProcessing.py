""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/wi_processing/etc/FWIProcessing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FWhenIssueProcessing - Module which processes When Issued bonds.

DESCRIPTION
    This module is used to process trades beloning to When Issued bonds.  It is
    also possible to use this module to rollback trades that have been
    processed.

DATA-PREP
    The variables that should be set are:

        instrument   String     The instrument to which processed trades will
                                belong
        tradefilter  String     A tradefilter in which all trades are included
                                that should be considered for processing
        process      String     Set to Process if processing or Rollback if
                                doing rollbacking
        verbosity    int        Integer that indicate the level of information
                                that will be generated in the AEL console

    There are a number of functions that are called from this module:

        get_ins_and_trds_for_processing() Creates a list of instruments and
                                          trades that are to be processed
        process_wi()                      Process trades
        get_ins_and_trds_for_rollback()   Creates a list of instruments and
                                          trades that are to be processed.
        rollback_wi()                     Rollback trades

REFERENCES
    See modules FWIParams and FWIGeneral.
----------------------------------------------------------------------------"""


import time


import ael


import FWIParams
import importlib
importlib.reload(FWIParams)
import FWIGeneral
importlib.reload(FWIGeneral)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


class ExitScriptError(Exception):

    def __init__(self, msg):
        Exception.__init__(self)
        self.__msg = msg

    def __str__(self):
        return str(self.__msg)


day = str(ael.date_today())
tradefilters = ael.TradeFilter.select()
tf_list = []
for tf in tradefilters:
    tf_list.append(tf.fltid)


instruments = ael.Instrument.select('instype="Bond"')
ins_list = []
for i in instruments:
    ins_list.append(i.insid)


## Tool Tips


ttTradefilter = ("A tradefilter in which all included trades are considered "
        "for processing.  A tradefilter is created with the help of the "
        "Trade Filter application found under the Data-menu.")
ttProcess = "Set to Process if processing or Rollback if rollbacking."
ttIns = "The instrument to which processed trades will belong."
ttVerb = "Defines the amount of logging produced."


ael_variables = [
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['tradefilter',
                'Tradefilter',
                'string', tf_list, None,
                1, 1, ttTradefilter],
        ['process',
                'Process/Rollback',
                'string', ['Process', 'Rollback'], None,
                0, 0, ttProcess],
        ['ins',
                'Target Instrument',
                'string', ins_list, None,
                0, 0, ttIns],
        ['verb',
                'Logmode',
                'int', ['0', '1', '2'], '1',
                0, 0, ttVerb]
]


def ael_main(parameter):

    tradefilter = parameter.get('tradefilter')
    process = parameter.get('process')
    ins = parameter.get('ins')
    verb = parameter.get('verb')

    wi = FWIParams.FWhenIssued(tradefilter, ins, verb)
    FWIGeneral.log(1, verb, 'Processing date:%s' % day)
    if process == 'Process':
        FWIGeneral.log(1, verb, "\n1 Create a list of all instruments and "
                "trades that are to be processed.\n")
        wi.get_ins_and_trds_for_processing()
        FWIGeneral.log(1, verb, '\n2 Processing started\n')
        wi.process_wi()
    elif process == 'Rollback':
        FWIGeneral.log(1, verb, "\n1 Create a list of all instruments and "
                "trades that are to be rollbacked.\n")
        wi.get_ins_and_trds_for_rollback()
        FWIGeneral.log(1, verb, '\n2 Rollback started \n')
        wi.rollback_wi()
    FWIGeneral.log(1, verb, "\nWhen Issued process finished %s" %
            str(time.ctime(time.time())))
    FWIGeneral.log(1, verb, "When Issue process has been successful!")

