"""-------------------------------------------------------------------------------------------------------
MODULE
    FLoggerTab

    (c) Copyright 2010-2018 by FIS Front Arena. All rights reserved.

DESCRIPTION

    This is a GUI tab for logging parameters

-------------------------------------------------------------------------------------------------------"""
import FRunScriptGUI

class LoggerTab(FRunScriptGUI.AelVariablesHandler):
    """ The RunScript GUI tab """
    yesTrue=('Yes', 'True', '1', True)

    def prevActiveCB(self,rnge=1):
        def prevActiveCBi(index, fieldValues):
            """disable/enable settings before toggle"""
            rng=rnge
            for idx in range(index -rng, index):
                self.ael_variables[idx][9] = not (fieldValues[index] in self.yesTrue)
            return fieldValues
        return prevActiveCBi

    def nextActiveCB(self,rnge=1):
        memory=[]
        def nextActiveCBi(index, fieldValues):
            """disable/enable settings after toggle"""
            rng=rnge
            for idx in range(index +1, index + 1 + rng):
                #print "idx",idx, "len",len(self.ael_variables),self.ael_variables[idx],""
                while len(self.ael_variables[idx]) < 10:
                    # Need to add some entries to be able to set the 9:th.
                    self.ael_variables[idx].append(None)

                reset=(fieldValues[index] not in self.yesTrue)
                if reset:
                    memory.append(self.ael_variables[idx][9])
                else:
                    if len(memory)>0:
                        reset=memory.pop(0) not in self.yesTrue
                self.ael_variables[idx][9] = not reset
            return fieldValues
        return nextActiveCBi

    def prevDeactiveCB(self, index, fieldValues):
        """disable/enable settings before toggle"""
        rng=0
        for idx in range(index -rng, index):
            self.ael_variables[idx][9] = (fieldValues[index] in self.yesTrue)
        return fieldValues
        
    def nextDeactiveCB(self,rnge=1):
        memory=[]
        def nextDeactiveCBi(index, fieldValues):
            """disable/enable settings after toggle"""
            rng=rnge
            for idx in range(index +1, index + 1 + rng):
                #print "idx",idx, "len",len(self.ael_variables),self.ael_variables[idx],""
                while len(self.ael_variables[idx]) < 10:
                    # Need to add some entries to be able to set the 9:th.
                    self.ael_variables[idx].append(None)

                reset=(fieldValues[index] in self.yesTrue)
                if reset:
                    memory.append(self.ael_variables[idx][9])
                else:
                    if len(memory)>0:
                        reset=memory.pop(0) not in self.yesTrue
                self.ael_variables[idx][9] = not reset
            return fieldValues
        return nextDeactiveCBi

    def logfile_cb(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        return fieldValues
        
    def __init__(self):
        tab_name = '_Logging'
        
        ttLogDefault = "Use the default settings for this logger. Ignore all other settings."
        ttLogMode = "Defines the amount of logging produced. (1 INFO, 2 DEBUG, 3 WARN, 4 ERROR)"
        ttLogToCon = "Whether logging should be output to the Log Console or not."
        ttLogToFile = "Defines whether logging should be output to file."
        ttLogFile = "Name of the logfile. Could include the whole path, c:\log\..."
        
        logmodes = ['1 INFO', '2 DEBUG', '3 WARN', '4 ERROR']
        aelvars = [['LogDefaults', 'Use defaults' + tab_name, 'int', [0, 1], 1, 1, 0, ttLogDefault, self.nextDeactiveCB(4), 1],
              ['Logmode', 'Logmode' + tab_name, 'int', logmodes, logmodes[0], 2, 0, ttLogMode, None, 1],
              ['LogToConsole', 'Log To Console' + tab_name, 'int', [0, 1], 1, 1, 0, ttLogToCon, None, 1],
              ['LogToFile', 'Log To File' + tab_name, 'int', [0, 1], 0, 1, 0, ttLogToFile, self.nextActiveCB(1), 1],
              ['Logfile', 'Logfile' + tab_name, 'string', None, None, 0, 0, ttLogFile, None, 0]
             ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, aelvars, __name__)

def getAelVariables():
    ael_vars = LoggerTab()
    ael_vars.LoadDefaultValues(__name__)

    return ael_vars
