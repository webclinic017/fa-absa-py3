import acm
import FLogger

from FOperationsATSRoutines import FOperationsATSRoutines
from FOperationsATSRoutines import FOperationsATSEngine
from FRoutingUtils import fetch_receivers
from FRoutingUtils import is_member_of_or_same_as

logger = FLogger.FLogger.GetLogger('ROUTING')
logger.Reinitialize(level=1)

class FRoutingATSEngine(FOperationsATSEngine):
    def __init__(self, params, subjects):
        super(FRoutingATSEngine, self).__init__('FRoutingATS', subjects, params, 'FRoutingParametersTemplate')

    def Start(self):
        pass

    def FindRoutingInstruction(self, trade):
        mapping = acm.Mapping().GetMap('routingInstructionMapping')
        if mapping:
            return mapping.MatchSingle(trade)
        else:
            return None
        
    def Work(self, mbf_object, obj):
    
        def execute_instruction(trade, instruction):
            result = instruction.Execute(trade)
            
            try:            
                acm.BeginTransaction()
                trade.Commit()
                logger.debug('Committing routed trade %d', trade.Oid())
                for artifact in result.CreatedArtifacts():
                    if artifact.Class() == acm.FDealPackage and artifact.IsEditable() == True:
                        artifact.Save()
                    else:
                        artifact.Commit()
                    logger.debug('Committing artifact %s', artifact.ClassName())                
                acm.CommitTransaction()
                logger.debug('Transaction completed')
            except:            
                acm.AbortTransaction()
                logger.debug('Could not commit transaction')
                raise

        def route(trade, routing_instruction):
            logger.debug('Executing routing instruction "%s" on trade %d', routing_instruction.Name(), trade.Oid())
            
            try:
                execute_instruction(trade, routing_instruction)
                logger.info('Routing of trade %d completed, using instruction "%s"', trade.Oid(), routing_instruction.Name())
            except Exception as e:
                message = mbf_object.mbf_object_to_string()
                handle_failure(message)
                logger.ELOG('Routing of trade %d failed: %s', trade.Oid(), str(e))    


        def handle_failure(message):
            
            def move_trade(trade):
                trade.Portfolio(acm.Routing().FailedOperationPortfolio())
                trade.Commit()
                logger.debug('Trade %d moved to failed operation portfolio', trade.Oid())
        
            def find_near_leg(far_leg):
                assert far_leg.IsFxSwapFarLeg()
                near_leg = far_leg.ConnectedTrade()
                assert near_leg.IsFxSwapNearLeg()
                
                return near_leg
                
            try:
                # Recreating the trade from the AMBA message to revert any changes
                # done during the failed operation execution
                trade = acm.AMBAMessage.CreateSimulatedObject(message)
                
                if trade and trade.Class() is acm.FTrade and trade.IsFxSwapFarLeg():
                    far_leg = trade
                    near_leg = find_near_leg(far_leg)
                    # Reverts transformation
                    near_leg.Undo()
                    try:
                        acm.BeginTransaction()
                        move_trade(far_leg)
                        move_trade(near_leg)
                        acm.CommitTransaction()
                    except:
                        acm.AbortTransaction()
                        raise
                else:
                    move_trade(trade)
            except Exception as e:
                logger.ELOG('Failure handling did not complete: %s', str(e))

        
        def is_in_source_portfolio(trade):
            source = acm.Routing().SourcePortfolio()
            return is_member_of_or_same_as(trade.Portfolio(), source)


        def configuration_valid():
            source = acm.Routing().SourcePortfolio()
            failure = acm.Routing().FailedOperationPortfolio()
            if not source:
                logger.ELOG('Invalid configuration: No source portfolio set')
                return False
            elif not failure:
                logger.ELOG('Invalid configuration: No failed operation portfolio set')
                return False
            elif is_member_of_or_same_as(failure, source):
                logger.ELOG('Invalid configuration: Failed operation portfolio %s is member of or same as source portfolio %s', failure.Name(), source.Name())
                return False
            else:
                logger.debug('Configuration is valid')
                return True
        
        
        def should_be_routed(trade):
            if not configuration_valid():
                return False
            elif trade.IsFxSwapNearLeg():
                logger.debug('Will not route FX swap near leg trades')
                return False
            elif not is_in_source_portfolio(trade):
                logger.debug('Trade %d is not in source portfolio', trade.Oid()) 
                return False
            elif trade.IsGroupChild():
                logger.debug('Will not route FX child trade %d', trade.Oid()) 
                return False
            else:
                return True



        def handle_trade_message(trade):
            if should_be_routed(trade):
                logger.debug('Message is trade %d', trade.Oid())
                routing_instruction = self.FindRoutingInstruction(trade)
                
                if routing_instruction:
                    route(trade, routing_instruction)
                else:
                    logger.debug('No routing instruction matched for trade %d', trade.Oid())
            else:
                logger.debug('Trade %d is not a candidate for routing', trade.Oid())
        
        def handle_redirection_message(redirection):
            if redirection.Status() == 'Enabled':
                try:
                    logger.debug('Sending redirection message for %s' % str(redirection))
                    acm.Routing.SendRedirectionMessage(redirection)
                except Exception as e:
                    logger.ELOG('Could not send redirection: %s' % str(e))

        
        logger.debug('Processing message')

        if obj and obj.IsKindOf(acm.FTrade):
            handle_trade_message(obj)
        elif obj and obj.IsKindOf(acm.FRoutingRedirection):
            handle_redirection_message(obj)
        else:
            message = mbf_object.mbf_object_to_string()
            logger.debug('Cannot handle message %s' % message)

def InitATS():
    params = _ImportInstanceParameters(acm.UserName())
    subjects = _SubjectsToListenTo(params)
    engine = FRoutingATSEngine(params, subjects)
    return FOperationsATSRoutines(engine)
    
def work():
    global ats
    if ats:
        ats.Work()
        
def start():
    global ats
    ats = InitATS()
    ats.Start()
    
    
def _SubjectsToListenTo(params):
    dbTables = ['TRADE', 'ROUTINGREDIRECTION']
    receivers = fetch_receivers()
    
    if len(receivers) > 1:
        return [ '%s/%s' % (s, params.receiverMBName) for s in dbTables ]
    else:
        return dbTables


def _ImportInstanceParameters(atsInstanceName):
    try:
        from FRoutingParameters import RoutingATSSettings
        paramClass = getattr(RoutingATSSettings, atsInstanceName)
        return paramClass
    except Exception as e:
        raise Exception('Could not find any configuration parameters for ATS instance named %s: %s' % (atsInstanceName, str(e)))
    

        
            
