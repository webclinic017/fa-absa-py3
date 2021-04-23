""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FRerate.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FRerate - Script for performing rerate

----------------------------------------------------------------------------"""

#Import Front modules

import ael
import FBDPGui
reload(FBDPGui)


# Tool Tip
ttrerate = "Select the instrument to rerate"
ttdate = "Enter the start date for the new rate"
ttrate = "Enter a new rate"

cvRate = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

ael_variables = FBDPGui.LogVariables(
    # Variable      Display               Type           Candidate           Default           Mandatory   Description Input Enabled
    # name          name                                 values                                      Multiple          hook
    ('instruments', 'Instruments_Fixing', 'FInstrument', None, None, 0, 1, ttrerate               ),
    ('date', 'Date_Fixing', 'string', [ael.date_today()], ael.date_today(), 0, 0, ttdate                 ),
    ('rate', 'Rate_Fixing', 'double', cvRate, 0.0, 0, 0, ttrate                 ))

def ael_main(dictionary):

    import FBDPString
    reload(FBDPString)
    import FBDPCommon
    reload(FBDPCommon)
    try:
        import FBDPHook
        reload(FBDPHook)
    except:
        pass
    import FReratePerform
    reload(FReratePerform)
    logme = FBDPString.logme
    ScriptName = "Rerate"
    logme.setLogmeVar(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'], 
                      dictionary['ReportMessageType'])
    FBDPCommon.execute_script(FReratePerform.rerate, dictionary)
    logme('FINISH')


