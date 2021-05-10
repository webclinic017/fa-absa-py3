
"""--------------------------------------------------------------------------
MODULE
    FileSecLendWorkflowATS

DESCRIPTION
    Module to be run by ATS (continuous mode) to create security loans from incoming files 
        and create outgoing files.
    Main functions: start, work, stop.

-----------------------------------------------------------------------------"""

import acm
import ael
import traceback
import os
import time
from FWorkflow import Logger
from FileImporterExporter import FileImporter, ExportTrade, moveFileAndZip


SEC_LENDING_STATE_CHART = 'Securities Lending'
SEC_LEND_RESPOND_STATE = 'Awaiting Reply'
SEC_LEND_REJECT_STATE = 'Rejected'

LOOK_BACK_DAYS = '-1d'
IMPORT_PATH = 'C:\\temp\\SecLend\\import'
EXPORT_PATH = 'C:\\temp\\SecLend\\export'
ARCHIVE_PATH = 'C:\\temp\\SecLend\\archive'
ERROR_PATH = 'C:\\temp\\SecLend\\error'

logger = Logger()

def start():   
    logger.info('Starting business process subscriptions.')
    InitializeTrades()
    ael.BusinessProcess.subscribe(SecLendingCB)
    
def work():
    CheckForFiles()

def stop():
    ael.BusinessProcess.unsubscribe(SecLendingCB)
    
def SecLendingCB(obj, ael_entity, arg, event):
    if event in ['update']:
        try:
            bp = acm.Ael.AelToFObject(ael_entity)
            logger.info('get bp update {0} {1}'.format(bp.Oid(), bp.StateChart().Name()))
            if bp.StateChart().Name() == SEC_LENDING_STATE_CHART:
                ReactOnSecLendingState(bp.Subject(), bp)

        except Exception:
            logger.error(traceback.format_exc())


def InitializeTrades():
    # without dedicated business process or similar it's not clear if accept/reject hasn't bee already sent
    dt = acm.Time.PeriodSymbolToDate(LOOK_BACK_DAYS)
    for trade in acm.FTrade.Select('tradeTime >= {0}'.format(dt)):
        try:
            ReactOnSecLendingState(trade)
        except Exception:
            logger.error(traceback.format_exc())
            

def CheckForFiles():
    for file in os.listdir(IMPORT_PATH):
        filePath = os.path.join(IMPORT_PATH, file)
        importer = FileImporter(filePath)
        if importer.fileReadOK():
            try:
                importer.process()
                moveFileAndZip(filePath, ARCHIVE_PATH, '%Y%m%d%H%M%S%f')
            except Exception:
                logger.error(traceback.format_exc())
                logger.info('Trade cration failed, file moved to error folder {0}'.format(filePath))
                moveFileAndZip(filePath, ERROR_PATH, '%Y%m%d%H%M%S%f')
        else:
            logger.error('Removing failing file'.format(filePath))
            moveFileAndZip(filePath, ERROR_PATH, '%Y%m%d%H%M%S%f')       

def secLendBusinessProcess(trade):
    try:
        return acm.BusinessProcess.FindBySubjectAndStateChart(trade, SEC_LENDING_STATE_CHART)[0]
    except IndexError:
        return None

def ReactOnSecLendingState(trade, businessProcess=None):
    if not businessProcess:
        businessProcess = secLendBusinessProcess(trade)
    if businessProcess and trade.Market() and trade.Market().Name() == 'File':
        if businessProcess.CurrentStep().State().Name() == SEC_LEND_RESPOND_STATE:
            logger.info('Sending accept for trade {0}'.format(trade.Oid()))
            ExportTrade(trade, EXPORT_PATH, 'Respond')
                
        elif businessProcess.CurrentStep().State().Name() == SEC_LEND_REJECT_STATE:
            logger.info('Sending reject for trade {0}'.format(trade.Oid()))
            ExportTrade(trade, EXPORT_PATH, 'Reject')

                
