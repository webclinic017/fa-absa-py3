""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPCurrentContext.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
Module
    FBDPCurrentContext

DESCRIPTION
    This moudule is to enable the user to access the Logme and Summary in a
    global scope.  Everytime you reload the module, your previous log and
    summary will be lost.
----------------------------------------------------------------------------"""


import FBDPString
import FBDPCommon

ElectionGUIUpdaterFunc = None
ChoiceGUIUpdaterFunc = None
PayoutGUIUpdaterFunc = None

class ScriptLogging:
    ScriptLogme = None
    ScriptSummary = None


def Summary():
    if not ScriptLogging.ScriptSummary:
        ScriptLogging.ScriptSummary = FBDPCommon.CreateSummary()
    return ScriptLogging.ScriptSummary


def Logme():
    if not ScriptLogging.ScriptLogme:
        ScriptLogging.ScriptLogme = FBDPString.createLogme()
    return ScriptLogging.ScriptLogme


def CreateLog(ScriptName, LogMode, LogToConsole, LogToFile, Logfile,
        SendReportByMail, MailList, ReportMessageType):
    ScriptLogging.ScriptSummary = FBDPCommon.CreateSummary()
    ScriptLogging.ScriptLogme = FBDPString.createLogme().setLogmeVar(
            ScriptName, LogMode, LogToConsole, LogToFile, Logfile,
            SendReportByMail, MailList, ReportMessageType)


def ElectionGUIUpdater():
    if ElectionGUIUpdaterFunc:
        return ElectionGUIUpdaterFunc
    return None


def RegisterElectionGUIUpdater(updater):
    if updater:
        global ElectionGUIUpdaterFunc
        ElectionGUIUpdaterFunc = updater
    else:
        ElectionGUIUpdaterFunc = None


def ChoiceGUIUpdater():
    if ChoiceGUIUpdaterFunc:
        return ChoiceGUIUpdaterFunc
    return None


def RegisterChoiceGUIUpdater(updater):
    if updater:
        global ChoiceGUIUpdaterFunc
        ChoiceGUIUpdaterFunc = updater
    else:
        ChoiceGUIUpdaterFunc = None


def PayoutGUIUpdater():
    if PayoutGUIUpdaterFunc:
        return PayoutGUIUpdaterFunc
    return None


def RegisterPayoutGUIUpdater(updater):
    if updater:
        global PayoutGUIUpdaterFunc
        PayoutGUIUpdaterFunc = updater
    else:
        PayoutGUIUpdaterFunc = None
