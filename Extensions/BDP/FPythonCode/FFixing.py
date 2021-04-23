""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FFixing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFixing - Script for performing fixing

----------------------------------------------------------------------------"""

#Import Front modules

import FBDPGui
reload(FBDPGui)


# Tool Tip
ttresets = "Select the resets to fix"
ttextend =  "Prolong open-ended instruments with one day"
ttinstruments = "Extend specific instruments: default is  extend all open end instruments"
ttbackdatereset = "Include Backdated Resets"

q = FBDPGui.insertResets()
q2 = FBDPGui.insertOpenEndIns()

ael_variables = FBDPGui.LogVariables(
    # Variable     Display                          Type           Candidate  Default  Mandatory   Description Input Enabled
    # name         name                                            values                    Multiple          hook
    ('resets', 'Resets_Fixing', 'FReset', None, q, 0, 1, ttresets               ),
    ('extend_oe', 'Extend open end trades_Extend', 'int', [1, 0], 0, 0, 0, ttextend               ),
    ('extend_ins', 'Instruments to Extend_Extend', 'FInstrument', None, q2, 0, 1, ttinstruments          ),
    ('backdateResets', 'Include Backdated Reset_Fixing', 'int', [1, 0], 0, 2, 0, ttbackdatereset          ))

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
    import FFixPerform
    reload(FFixPerform)
    # Only used for Op Man Fixing (1 = do not commit changes)
    dictionary['GetOpManFixingRates_DoNotCommit'] = 0
    if not 'backdateResets' in dictionary.keys():
        dictionary["backdateResets"] = False
    logme = FBDPString.logme
    ScriptName = "Fixing"
    logme.setLogmeVar(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'], 
                      dictionary['ReportMessageType'])
    FBDPCommon.execute_script(FFixPerform.fix, dictionary)
    logme('FINISH')
