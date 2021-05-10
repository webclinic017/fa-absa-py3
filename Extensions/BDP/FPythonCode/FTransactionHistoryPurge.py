""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/transaction_history/FTransactionHistoryPurge.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FTransactionHistoryPurge

DESCRIPTION
    Use to delete transaction histories from the ADS. Also possible to save the 
    deleted rows to file, even if no purge is performed.

NOTE
    The modules uses the Reporting module.


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import datetime
import os

import FLogger
import FRunScriptGUI

import FOutputFileSettingsTab

falseTrue = ['False', 'True']

logger = FLogger.FLogger('FATHPurge')

def validateVariables(params):
    if params['queryName'] == '':
        raise Exception("Query name must be specified")
        
    if not falseTrue.index(params['purge']) and not falseTrue.index(params['fileOutput']):
        raise Exception("Purge and/or Enable File Output must be checked")
        
    return FOutputFileSettingsTab.validateVariables(params)

def getTransactionHistorys(params):
    """Retrieve the Transaction Histories found with query"""

    queryName = params['queryName']
    try:
        storedQuery = acm.FStoredASQLQuery.Select('name="%s"' % queryName)[0]
        return storedQuery.Query().Select().Sort()
    except:
        raise Exception("Exception when retrieving transaction history's from stored query " + queryName)
    return None

def perform(params):
    res = None
    
    try:
        validateVariables(params)
        res = getTransactionHistorys(params)
    except Exception as ex:
        logger.LOG('FTransactionHistoryPurge, Aborted, exception: %s', str(ex))
        return
            
    if res is None:
        return

    doPurge = falseTrue.index(params['purge'])
    doSaveToFile = falseTrue.index(params['fileOutput'])

    purgeCount = 0
    
    if doSaveToFile:
        outputDir = None
        file = None
        try:
            outputDir = FOutputFileSettingsTab.createOutputDir(params)
            if outputDir:
                file = FOutputFileSettingsTab.getNewFilePath(params, outputDir, ".xml")
            else:
                logger.LOG('FTransactionHistoryPurge, Aborted, could not create output directory')
                return
        except Exception as ex:
            logger.LOG('FTransactionHistoryPurge, Aborted, exception: %s', str(ex))
            return
        
        gen = acm.FAMBAMessageGenerator()
        gen.ShowAll()
        gen.ShowChanges(True)

        output = acm.FCharacterOutputFileStream(file)
        formatter = acm.FTaggedMessageXMLFormatter()
        formatter.EnableWhitespace(True)
        
        formatter.WritePrologToStream(output);
        output.Write('<MESSAGES>\n')
        formatter.Indent(1)

        saveCount = 0
        for th in res:
            try:
                thmsg = gen.GenerateTransactionHistory(th)
            except Exception as ex:
                logger.LOG('FTransactionHistoryPurge, skipped transaction historiy %d, exception: %s', th.SeqNbr(), str(ex))
                continue
                
            if doPurge:
                try:
                    th.Delete()
                except Exception as ex:
                    logger.LOG('FTransactionHistoryPurge, exception when deleting transaction historiy %d, exception: %s', th.SeqNbr(), str(ex))
                    continue
                purgeCount = purgeCount + 1
                
            try: 
                formatter.FormatStream(output, thmsg)
                saveCount = saveCount + 1
            except Exception as ex:
                logger.LOG('FTransactionHistoryPurge, error when writing message, exception %s', str(ex))
            
        formatter.Indent(-1)
        output.Write('</MESSAGES>\n')
        output.Close()
        
        logger.LOG('FTransactionHistoryPurge, wrote %d transaction histories to file %s', saveCount, file)

        if doPurge:
            logger.LOG('FTransactionHistoryPurge, purged %d transaction histories', purgeCount)
    else:
        for th in res:
            if doPurge:
                try:
                    th.Delete()
                    purgeCount = purgeCount + 1
                except Exception as ex:
                    logger.LOG('FTransactionHistoryPurge, exception when deleting transaction historiy %d, exception: %s', th.SeqNbr(), str(ex))
        logger.LOG('FTransactionHistoryPurge, purged %d transaction histories', purgeCount)

class TransactionHistoryPurge(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        self.queryOld=''
        allQueries = acm.FStoredASQLQuery.Select('')
        queries = []
        for q in allQueries:
            try:
                if q.QueryClass() == acm.FTransactionHistory:
                    queries.append(q.Name())
            except:
                pass
        queries.sort()

        vars =[
               ['queryName', 'Query Name', 'string', queries, None, 1, 0, 'Name of a stored query', None, 1],
               ['purge', 'Purge', 'string', falseTrue, 'False', 1, 0, 'Purge transaction history\'s from database', None, 1]
              ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FOutputFileSettingsTab.getAelVariables())

def ael_main(params):
    perform(params)

ael_gui_parameters = {'windowCaption':'FTransactionHistoryPurge'}
ael_variables = TransactionHistoryPurge()
