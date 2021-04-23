"""----------------------------------------------------------------------------
MODULE
    F273728_ConvertFXTrades - Script for converting pre 4.0 FX Trades to new format.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION

        Run the script by loading it into the Python Editor and selecting
        Special -> Reload Module. A GUI appears that let's you choose between running
        the script in test mode or normal mode. In test mode no changes would be commited
        to the database. The GUI also lets you choose between running the script with no
        diagnostics written to the log console or with detailed diagnostics.

        The execution can be rolled back by using the script FStartRollback. See FCA2324
        about how to roll back a script execution.
        
        Currency Trades are updated with a FX Spot tag on the trade_process bit array field. 
        FX Swap trades are voided and an FX Forward trade or an FX Swap trade pair are created 
        in the Currency Instrument to replace the original deal. The original deal's trade 
        number is stored on the newly created trades' free_text2 field.


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import ael, acm
import FBDPRollback
import FBDPCommon

Summary = FBDPCommon.Summary

class ConvertFXTrades(FBDPRollback.RollbackInfo):

        
    def perform(self, args):
        import FBDPString
        logme = FBDPString.logme
        self.ael_variables_dict = args
        terminated_trades=[]
        
        for i in ael.Instrument.select("instype='Curr'"):
            logme('Processing Currency %s.'%i.insid, 'INFO')                                                  
            for t in i.trades():                                                            
                if (t.trade_process != 0 and t.connected_trdnbr!=None):
                    continue
                logme('Processing a Curr trade', 'DEBUG')
                t = t.clone()
                t.trade_process = 4096
                print t.trdnbr
                if t.connected_trdnbr==None:
                    t.connected_trdnbr=t.trdnbr
                    print 'updated trdnbr'
                self.add(t, ['trade_process'])
                self.add(t, ['connected_trdnbr'])
                Summary().ok(t, Summary().UPDATE)                        
                self.beginTransaction()
                try:
                    self.commitTransaction()
                except :
                    self.abortTransaction()
                    Summary().fail(t, Summary().CREATE, i.insid+' failed to commit', t.trdnbr)  
                    continue

    
try:
    import FBDPGui
    FBDPParameters = FBDPGui.Parameters('FBDPParameters')
    Testmode = FBDPParameters.Testmode
    Logmode = FBDPParameters.Logmode
    LogToConsole = FBDPParameters.LogToConsole
    LogToFile = FBDPParameters.LogToFile
    Logfile = FBDPParameters.Logfile
except:
    Testmode = 1
    Logmode = 0
    LogToConsole = 1
    LogToFile = 0
    Logfile = 'F273728_log'

ael_variables = [('TestMode', 'TestMode', 'int', [0, 1], Testmode, 0, 0),
                  ('Logmode', 'LogMode', 'int', [0, 1, 2], Logmode, 1, 0),
                  ('LogToConsole', 'Log To Console', 'int', [1, 0], LogToConsole, 1, 0),
                  ('LogToFile', 'Log To File', 'int', [1, 0], LogToFile, 1, 0),
                  ('Logfile', 'Logfile', 'string', None, Logfile, 0, 0)]

def ael_main(args):
    print args
    ScriptName = 'ConvertFXTrades'
    import FBDPString
    reload(FBDPString)
    reload(FBDPRollback)
    reload(FBDPCommon)
    logme = FBDPString.logme
    logme.setLogmeVar(ScriptName,
                      args['Logmode'],
                      args['LogToConsole'],
                      args['LogToFile'],
                      args['Logfile'],
                      0, 
                      0, 
                      0)
    logme(None, 'START')
    ConvertFXTrades(ScriptName,
               args,
               Testmode=args['TestMode'])

