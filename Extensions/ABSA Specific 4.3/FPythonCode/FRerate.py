""" Compiled: 2011-06-29 20:34:26 """

"""----------------------------------------------------------------------------
MODULE
    FRerate - Script for performing rerate

    (c) Copyright 2006 by Front Capital Systems AB. All rights reserved.

----------------------------------------------------------------------------"""

#Import Front modules

import ael
import FBDPGui
reload(FBDPGui)

if  __name__ == '__main__':
    logme('Running FFixing from the platform has not been '\
        'implemented, Must be run from within the client.', 'ERROR')
else:

    # Tool Tip
    ttrerate = "Select the instrument to rerate"
    ttdate = "Enter the start date for the new rate"
    ttrate = "Enter a new rate"

    ael_variables = FBDPGui.LogVariables(
        ('instruments', 'Instruments_Fixing', 'FInstrument', None, None, 0, 1, ttrerate),
        ('date', 'Date_Fixing', 'string', [ael.date_today()], ael.date_today(), 0, 0, ttdate),
        ('rate', 'Rate_Fixing', 'double', [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], 0.0, 0, 0, ttrate)
    )

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

        logme.setLogmeVar(
            ScriptName,
            dictionary['Logmode'],
            dictionary['LogToConsole'],
            dictionary['LogToFile'],
            dictionary['Logfile'],
            dictionary['SendReportByMail'],
            dictionary['MailList'],
            dictionary['ReportMessageType']
        )

        FBDPCommon.execute_script(
            FReratePerform.rerate,
            dictionary
        )
