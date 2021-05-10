""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsLogger.py"

#-------------------------------------------------------------------------
# Logger interface 
#-------------------------------------------------------------------------
class Logger(object):
    
    def LP_Log(self, log):
        pass

    def LP_LogVerbose(self, log):
        pass

    def LP_Flush(self):
        pass

