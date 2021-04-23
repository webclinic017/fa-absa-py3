""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/rollback/etc/FPurgeRollbackTable.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPurgeRollbackTable - Deletes old RollbackData

DESCRIPTION
    This script deletes old rollback data. Old rollback data is rollback
    data that correspond to a rollback specification which older than open
    days.
----------------------------------------------------------------------------"""


import ael


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCurrentContext


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters')


ael_variables = FBDPGui.RollbackVariables()


def ael_main(parameter):

    import FBDPString
    importlib.reload(FBDPString)
    FBDPCurrentContext.CreateLog('PurgeRollbackTable',
                      parameter['Logmode'],
                      parameter['LogToConsole'],
                      parameter['LogToFile'],
                      parameter['Logfile'],
                      parameter['SendReportByMail'],
                      parameter['MailList'],
                      parameter['ReportMessageType'])

    FBDPCurrentContext.Logme()(None, 'START')
    for spec in parameter['rollbackSpec']:
        spec = ael.RollbackSpec[spec.Oid()]
        FBDPCurrentContext.Logme()(spec.name, 'DEBUG')
        clone = spec.clone()
        while clone.rollback_data():
            for rd in clone.rollback_data().members()[:64]:
                FBDPCurrentContext.Logme()(rd.seqnbr, 'DEBUG')
                FBDPCurrentContext.Logme()(rd.entity, 'DEBUG')
                rd.delete()
            clone.commit()
        ael.poll()
        spec.delete()
    FBDPCurrentContext.Logme()(None, 'FINISH')
