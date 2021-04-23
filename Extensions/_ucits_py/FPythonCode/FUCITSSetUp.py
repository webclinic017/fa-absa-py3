""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSSetUp.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSSetUp

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FRunScriptGUI
import FAssetManagementUtils
from FUCITSSetUpChoiceLists import SetUpChoiceLists
from FUCITSSetUpAdditionalInfos import SetUpAdditionalInfos
from FUCITSSetUpPageGroups import SetUpPageGroups

logger  = FAssetManagementUtils.logger
logDict = FAssetManagementUtils.logDict

class UCITSApply(FRunScriptGUI.AelVariablesHandler):

    @staticmethod
    def IsSetUp():
        return SetUpChoiceLists.IsSetUp() and SetUpAdditionalInfos.IsSetUp() and \
               SetUpPageGroups.IsSetUp()


    def __init__(self):
        sAddInfos = "Create necessary additional infos. This must be done before the templates are applied"
        sLog = 'Logmode 0 shows WARNING and ERROR messages. Logmode 1 shows INFORMATION messages, and also includes the messages from Logmode 0.\
                Logmode 2 shows DEBUG messages and includes all other message types. '
        variables = [
                      ['CREATE_ADD_INFOS',  'Set up',            'bool', [0, 1], 0, 1, 0, sAddInfos,        None, not UCITSApply.IsSetUp()],
                      ['LOG_MODE', 'Logmode_Logging', 'string', sorted(logDict), '1. Normal', 2, 0, sLog]
                    ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)


ael_variables = UCITSApply()

def ael_main(params):
    logger.Reinitialize(level=logDict[ params['LOG_MODE'] ],
                        keep=None,
                        logOnce=None,
                        logToConsole=1,
                        logToPrime=None,
                        logToFileAtSpecifiedPath=None,
                        filters=None,
                        lock=None
                    )

    if params['CREATE_ADD_INFOS']:
        restart = False
        logger.info('--Setup Started--')
        restart = SetUpChoiceLists.SetUp()
        restart |= SetUpAdditionalInfos.SetUp()
        restart |= SetUpPageGroups.SetUp()
        logger.info('--Setup Finished--')
        if restart:
            msg = "Created necessary additional infos, page groups and choice lists. Please restart the PRIME session,"\
                  "set all static data, and re-run the script to apply limit templates"
        else:
            msg = "Created necessary additional infos, page groups and choice lists. Please restart the run-script, " \
                  "set all static data, and re-run the script to apply limit templates"
        acm.UX().Dialogs().MessageBoxInformation(acm.UX().SessionManager().Shell(), msg)