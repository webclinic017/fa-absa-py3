""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./etc/FReconciliationUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationUtils

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
from FReconciliationValueMapping import GetCalculator
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


def RemoveRemainingReconItems(reconInstance):
    logger.info('Removing recon items exceeding the threshold controlling the maximum number of tolerated unclosed items...')    
    allWorkflows = set([w for w in reconInstance.Workflows()])
    unclWorkflows = set([w for w in reconInstance.UnclosedWorkflows()])
    unclWorkflowsComplement = allWorkflows.difference(unclWorkflows)
    for workflow in unclWorkflowsComplement:
        reconInstance.Remove(workflow)
    logger.info('Successfully removed %d unclosed item(s).' % len(unclWorkflowsComplement))
        
def RemoveZeroPositions(reconInstance):
    logger.info('Removing recon items related to closed positions...')
    calculator = GetCalculator(reconInstance)    
    candidateWorkflows = [w for w in reconInstance.Workflows()]
    zeroPositionWorkflows = list()
    while len(candidateWorkflows) > 0:
        workflow = candidateWorkflows.pop()
        if workflow.ACMObject():
            # Prevent nil objects from being inserted
            calculator.InsertItem(workflow.ACMObject())
            if calculator.IsInactivePos():        
                zeroPositionWorkflows.append(workflow)
            calculator.Clear()
    for workflow in zeroPositionWorkflows:
        reconInstance.Remove(workflow)
    logger.info('Successfully removed %d recon item(s) due to zero positions.' % len(zeroPositionWorkflows))        

def RemoveSuccessfulReconItems(reconInstance):
    logger.info('Removing recon items that have been successfully reconciled...')                
    workflows = [w for w in reconInstance.Workflows() if w.IsClosed()]    
    for workflow in workflows:
        reconInstance.Remove(workflow)   
    logger.info('Successfully removed %d successfully reconciled item(s).' % len(workflows))
            

''' Convenience functions '''

def GetOrCreatePositions(trades, positionSpecifications):
    positions = set()
    for trade in trades:
        for positionSpec in positionSpecifications:
            try:
                position = positionSpec.GetPosition(trade)
                positions.add(position)
                logger.info('Trade %d belongs to position "%s" for specification "%s"',
                            trade.Oid(), position.Name(), positionSpec.Name())
                break
            except ValueError:
                # Trade does not match this position specification
                pass
            except Exception as e:
                logger.error('Failed creating position from specification "%s": %s', positionSpec.Name(), e)
                raise
        else:
            logger.debug('Trade %d does not match any position specification.', trade.Oid())
    return positions

def GetUpdatedTrades(earliestUpdateTime):
    query = 'updateTime >= "' + earliestUpdateTime + '" AND status <> 7 AND status <> 8'
    trades = acm.FTrade.Select(query).AsSet()
    return [t for t in trades.AsArray()]

def GetTradesInPositionSpecifications(positionSpecifications):
    ''' This method can potentially return a very large collection. Use GetOrCreatePositions
        to instead retrieve the positions. If the trades are not given, use the FPositionSpecification 
        class to retrieve the position definitions given a wildcarded query and an attribute dict.
    '''
    trades = set()
    for spec in positionSpecifications:
        try:
            trades.update(spec.StoredWildcardedQuery().Query().Select())
        except Exception as e:
            logger.error('Failed to load trades from position specification "%s": %s', spec.Name(), e)
    return list(trades)