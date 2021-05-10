
import acm
from DealPackageDevKit import DealPackageException
from SP_DealPackageHelper import InstrumentAndDealPackageId

def ExerciseAccumulator(accumulatorPackage, exerciseDate, doCommit = True):
    
    if accumulatorPackage.Class() != acm.FDealPackage:
        raise DealPackageException ('Method ExerciseAccumulator can only be called for Accumulator Deal Packages')

    dpDefinition = accumulatorPackage.Definition()
        
    if dpDefinition.Name() != acm.FSymbol('SP_Accumulator'):
        raise DealPackageException ('Method ExerciseAccumulator can only be called for Accumulators')

    if dpDefinition['Type'] != acm.FSymbol('Normal'):
        raise DealPackageException ('Only accumulators of type "Normal" can be exercised')

    exerciseTrades, closingTrades = accumulatorPackage.GetAttribute('exercise')(exerciseDate)
    
    for singleExTrade in exerciseTrades:
        if doCommit:
            singleExTrade.Commit()
        if accumulatorPackage.IncludesTrade(singleExTrade):
            acm.Log( 'INFORMATION: created exercise for Accumulator %s' 
                        % (InstrumentAndDealPackageId(accumulatorPackage) ) )
        else:
            acm.Log( 'INFORMATION: created exercise trade %i for Accumulator "%s"' 
                    % (singleExTrade.Originator().Oid(), InstrumentAndDealPackageId(accumulatorPackage) ) )
    
    for singleClsTrade in closingTrades:
        if doCommit:
            singleClsTrade.Commit()
        acm.Log( 'INFORMATION: created closing trade %i for Accumulator "%s"' 
                % (singleClsTrade.Originator().Oid(), InstrumentAndDealPackageId(accumulatorPackage) ) )
    

