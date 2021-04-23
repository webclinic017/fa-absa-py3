""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/rollback/etc/FStartRollback.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FStartRollback - Module used to rollback / undo BDP scripts.

DESCRIPTION
    A Macro variables window is displayed with different script executions
    possible to roll back.
----------------------------------------------------------------------------"""

# Name of this script used in START, STOP and FINISH messages:

ScriptName = 'Rollback'

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import ael
import FBDPCurrentContext


INS_TT = 'Only roll back data referring to these instruments'
VOID_TT = 'Whether the roll-back script should \
            Delete or Void trades that \
            have been created by a script'


def rollback(ael_variables_dict):
    '''
    Rollback function
    '''
    import FBDPRollback
    spec = ael_variables_dict['rollbackSpec']
    spec = [ael.RollbackSpec[i.Oid()] for i in spec]
    spec = [(-i.specnbr, i) for i in spec]
    spec.sort()
    spec = [i[1] for i in spec]

    for spi in spec:
        rbinfo = FBDPRollback.RollbackInfo()
        rbinfo.void = ael_variables_dict.get('void')
        rbinfo.rollback(spi.name, ael_variables_dict['instruments'])
        ael.poll()

ael_variables = FBDPGui.RollbackVariables(['void',
                                           'Void Trades_Advanced',
                                           'string',
                                           ['Void', 'Delete'],
                                           'Delete', 1, None, VOID_TT],
                                           ['instruments',
                                           'Instruments_Advanced',
                                           'FInstrument',
                                            None,
                                            None,
                                            None,
                                            1,
                                            INS_TT])


def ael_main(dictionary):

    """
    Main function
    """
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    dictionary['instruments'] = [x.Oid() for x in dictionary['instruments']]
    FBDPCommon.execute_script(rollback, dictionary)
    FBDPCurrentContext.Summary().log(dictionary)
    FBDPCurrentContext.Logme()(None, 'FINISH')
