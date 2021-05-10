""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FOpManFixing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
    MODULE
    FOpManFixing - Script for performing fixing from the Operations Manager

----------------------------------------------------------------------------"""
import acm
import FFixPerform
import FBDPString
import FBDPCommon

def getResetAndLogInfo( invokationInfo ):
    # Create a dictionary for the Fixing
    resetsDict = dict()
    resetsDict['resets'] = acm.FArray()
    resetsDict['extend_oe'] = 0
    resetsDict['Logmode'] = 1
    resetsDict['LogToConsole'] = 1
    resetsDict['LogToFile'] = 0
    resetsDict['Logfile'] = None
    resetsDict['SendReportByMail'] = 0
    resetsDict['MailList'] = ""
    resetsDict['ReportMessageType'] = "Full Log"
    resetsDict['GetOpManFixingRates_DoNotCommit'] = 1
    # Only used for initial fixing performed from insdef
    resetsDict["backdateResets"] = False
    # Add the resets to the dictionary
    for reset in invokationInfo:
        resetsDict['resets'].Add( reset )
    return resetsDict

def runFixing( invokationInfo ):
    # Create a dictionary containing all Resets
    if invokationInfo.Size() > 0:
        resetsDict = getResetAndLogInfo( invokationInfo )
        # Log variables Setup
        logme = FBDPString.logme
        ScriptName = "Operations Manager Fixing"
        logme.setLogmeVar( ScriptName,
                           resetsDict['Logmode'],
                           resetsDict['LogToConsole'],
                           resetsDict['LogToFile'],
                           resetsDict['Logfile'],
                           resetsDict['SendReportByMail'], 
                           resetsDict['MailList'], 
                           resetsDict['ReportMessageType'] )
        # Use standard FFixPerform.fix to get the rates
        FBDPCommon.execute_script( FFixPerform.fix, resetsDict )
        return 1
    return 0
