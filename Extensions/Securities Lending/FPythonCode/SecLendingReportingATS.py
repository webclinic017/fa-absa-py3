""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/SecLendingReportingATS.py"
"""--------------------------------------------------------------------------
MODULE
    SecLendingReportingATS
    
    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Module to be run by ATS (continuous mode) to create outgoing files using the
    Reporting framework.
    To run fron a command line use:
    ats -module_name SecLendingReportingATS -user ... -password ... -server ...
    Main functions: start, work, stop.

-----------------------------------------------------------------------------"""

import acm
import ael
import traceback
import os
import time
from FWorkflow import Logger
from GenerateOrderReportAPI import GenerateOrderReport

SEC_LENDING_STATE_CHART = 'Securities Lending'
SEC_LEND_RESPOND_STATE = 'Awaiting Reply'
SEC_LEND_REJECT_STATE = 'Rejected'
SEC_LEND_BOOK_STATE = 'Booked'

SEC_LEND_REPORTING_STATES = [SEC_LEND_RESPOND_STATE, SEC_LEND_REJECT_STATE, SEC_LEND_BOOK_STATE]
SEC_LEND_REPORT_TO_DESTINATIONS = ['FTP Service', 'E-mail Service'] #Destinations shoudn't be hardcoded, they should be taken from the list of valid destinations

LOOK_BACK_PERIOD = '-1d'

logger = Logger()
#logger.Reinitialize(level=2) #Debug mode

subscribeTo = acm.FBusinessProcess.Select("stateChart = '%s'" % SEC_LENDING_STATE_CHART)

updatedBusinessProcesses = set()

def start():
    logger.info('Starting business process subscriptions.')
    subscribeTo.AddDependent(SecLendingCB())
    InitializeTrades()
    logger.info('%s started.' % __name__)
    
def work():
    while updatedBusinessProcesses:
        bp = updatedBusinessProcesses.pop()
        try:
            logger.debug('Processing {0} update {1} for trade {2}'.format(bp.StateChart().Name(), bp.Oid(), bp.Subject().StringKey()))
            ReactOnSecLendingState(bp.Subject(), bp)
        except Exception:
            logger.error('Error processing business process {} for trade {}'.format(bp.Oid(), bp.Subject().StringKey()))
            logger.error(traceback.format_exc())

def stop():
    for dependent in subscribeTo.Dependents():
        if isinstance(dependent, SecLendingCB):
            subscribeTo.RemoveDependent(dependent)
            

def InitializeTrades():
    dt = acm.Time.PeriodSymbolToDate(LOOK_BACK_PERIOD)
    logger.info('Recovering trades with trade time greater than %s' % dt)
    for bp in subscribeTo.AsArray():
        try:
            if bp.Subject() and bp.Subject().TradeTime() >= dt:
                logger.debug('Recovering {0} business process {1} for trade {2}'.format(bp.StateChart().Name(), bp.Oid(), bp.Subject().StringKey()))
                ReactOnSecLendingState(bp.Subject(), bp)
        except Exception:
            logger.error('Error processing business process {} for trade {}'.format(bp.Oid(), bp.Subject().StringKey()))
            logger.error(traceback.format_exc())

class SecLendingCB:
    def ServerUpdate(self, sender, event, bp):
        if str(event) in ['update']:
            try:
                logger.debug('Got {0} update {1} by {2} for trade {3}'.format(bp.StateChart().Name(), bp.Oid(), bp.UpdateUser().Name(), bp.Subject().StringKey()))
                updatedBusinessProcesses.add(bp)
            except Exception:
                logger.error('Error processing business process {} update for trade {}'.format(bp.Oid(), bp.Subject().StringKey()))
                logger.error(traceback.format_exc())


def SecLendBusinessProcess(trade):
    try:
        return acm.BusinessProcess.FindBySubjectAndStateChart(trade, SEC_LENDING_STATE_CHART)[0]
    except IndexError:
        return None

def SetResponseSent(process, response):
    bp = process.StorageImage()
    currentStep = bp.CurrentStep()
    diaryEntry = currentStep.DiaryEntry()
    if not diaryEntry.Parameters() and not diaryEntry.Notes():
        diaryEntry = acm.FBusinessProcessDiaryEntry()
    params = diaryEntry.Parameters()
    params.AtPut('Response', response)    
    diary = bp.Diary()
    diary.PutEntry(bp, currentStep, diaryEntry)
    bp.Commit()

def RespondOnOrders(businessProcesses, fileDestination):
    tradeIds = [bp.Subject().Oid() for bp in businessProcesses]
    response = GenerateOrderReport(tradeIds, fileDestination, businessProcesses[0].Subject().Counterparty())
    for bp in businessProcesses:
        SetResponseSent(bp, response + str(businessProcesses[0].Oid()))
    return response
    

def HandleRespondError(stateName, bps, destination, error):
    msg = 'Failed to send {0} response for trades {1} to {2} [{3}]'
    msg = msg.format(stateName, [bp.Subject().Oid() for bp in bps], destination, error)
    logger.error(msg)
    acm.BeginTransaction()
    try:
        for bp in bps:
            bp.ForceToErrorState(msg)
            bp.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        logger.error('Failed to set businessprocesses to error state - %s' % e)
       
        
def GetSettingsParameters(params, bpStep):
    if params.HasKey('TargetTrades'):
        return params
    prevStep = bpStep.PreviousStep()
    if prevStep:
        params = prevStep.DiaryEntry().Parameters()
        return GetSettingsParameters(params, prevStep)
    return params
    
def ReactOnSecLendingState(trade, businessProcess=None):
    if not businessProcess:
        businessProcess = SecLendBusinessProcess(trade)
    if businessProcess:
        bpStep = businessProcess.CurrentStep()
        if bpStep.State().Name() in SEC_LEND_REPORTING_STATES:
            params = bpStep.DiaryEntry().Parameters()
            if not params.At('Response'): 
                params = GetSettingsParameters(params, bpStep)
                if not params.At('Response'):
                    destination = params.At('TargetSource', trade.Market() and trade.Market().Name())
                    if destination in SEC_LEND_REPORT_TO_DESTINATIONS:
                        tradeString = params.At('TargetTrades')
                        if not tradeString:
                            msg = 'There should always be a specification of which trades to report on together. '
                            msg += 'That is the parameter TargetTrades that should be set by the OrderManager command.'
                            raise KeyError(msg)
                        bps = [SecLendBusinessProcess(acm.FTrade[t]) for t in tradeString.split(',')]
                        if bps and all(bp.CurrentStep().State().Name() == bpStep.State().Name() for bp in bps):
                            try:
                                response = RespondOnOrders(bps, destination)
                            except Exception as e:
                                HandleRespondError(bpStep.State().Name(), bps, destination, e)
                                return
                            msg = 'Sent {0} response {1} for trade {2} to {3}'
                            logger.info(msg.format(bpStep.State().Name(), response, trade.Oid(), destination))
                        else:
                            logger.debug('Not all trades in the transaction are in the same state')
                    else:
                        logger.debug('%s is not a valid output destination' % destination)
                else:
                    if params.At('Response', '').startswith('NO'):
                        logger.debug("Shouldn't send any response %s" % params)
                    else:
                        logger.debug('Already responded in previous step %s' % params)
            else:
                if params.At('Response', '').startswith('NO'):
                    logger.debug("Shouldn't send any response %s" % params)
                else:
                    logger.debug('Already responded %s' % params)
        else:
            logger.debug("No reporting state '%s'" % bpStep.State().Name())
    else:
        logger.debug('No BusinessProcess')
