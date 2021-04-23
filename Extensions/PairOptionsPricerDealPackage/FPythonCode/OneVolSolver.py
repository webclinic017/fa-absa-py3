
from __future__ import print_function
import acm

myTag = ['originalTag', 'copyTag']

arrayAny = acm.GetFunction('arrayAny', 1)
typeLot = type(acm.FLot([]))
double = acm.GetFunction('double', 1)

def CheckValues(original, copy):
    if hasattr(original, 'IsKindOf') and hasattr(copy, 'IsKindOf'):
        if original.IsKindOf('FEvaluator') and copy.IsKindOf('FEvaluator'):
            return original.Value() == copy.Value()
        elif original.IsKindOf('FArray') and copy.IsKindOf('FArray'):
            for o, c in zip(original, copy):
                if not CheckValues(o, c):
                    return False
            return True
        elif original.IsEqual(copy):
            return True
        return True
    elif original == copy:
        return True
    raise ValueError('Different types %s %s %s %s' % (original, type(original), copy, type(copy)))

def IsSimpleDataType(value):
    return hasattr(value, 'IsKindOf') and value.IsKindOf('FNumber') or isinstance(value, (str, int, float))

def SetSimulations(original, copy):
    if original.Value() != copy.Value():
        simulatedChild = False
        for oi, ci in zip(original.AllInputs(), copy.AllInputs()):
            if not CheckValues(oi, ci):
                simulatedChild = True
                SetSimulations(oi, ci)
        if not simulatedChild or original.HasSimulatedValue():
            if copy.HasSimulatedValue():
                copy.RemoveSimulation()
                if original.Value() == copy.Value():
                    return
            try:
                value = original.Value()
                if isinstance(value, typeLot):
                    value = arrayAny(value)
                if IsSimpleDataType(arrayAny(value)[0]):
                    copy.Simulate(value, False)
            except Exception as e:
                print ('Failed to simulate', copy, original.Value(), e)


def CopyEvaluator(object, eval, context):
    global myTag
    if myTag[0] == eval.Tag():
        tag = myTag[1]
    else:
        tag = acm.CreateEBTag()
        myTag = [eval.Tag(), tag]
    evalCopy = acm.GetCalculatedValueFromString(object, context, eval.Entity(), tag)
    SetSimulations(eval, evalCopy)
    return evalCopy


def ImplyBidAsk(object, target, shiftEntities, solverValue, context, precision, min, max, maxIterations):
    targetCopy = CopyEvaluator(object, target, context)
    parameterNodes = targetCopy.FindAdHoc(shiftEntities, None)
    
    bidValues = [min] + [arrayAny(node.Value())[0] for node in parameterNodes] + [max]
    askValues = [min] + [arrayAny(node.Value())[-1] for node in parameterNodes] + [max]
    
    def SetParameterValue(bidAsk, value):
        for node in parameterNodes:
            nodeValue = node.Value()
            if isinstance(nodeValue, typeLot):
                simValue = list(nodeValue)
                simValue[0 if bidAsk == 'Bid' else -1] = value
            else:
                simValue = value
            node.Simulate(simValue, False)
    
    def SolveBlock(args, value):
        try:
            bidAsk = args['BidAsk']
            SetParameterValue(bidAsk, value)
            targetValue = targetCopy.Value()
            if isinstance(targetValue, typeLot):
                targetValue = targetValue[0 if bidAsk == 'Bid' else -1]
            return targetValue
        except Exception as e:
            print ('Solverblock failed', e)
            raise

    previousResult = arrayAny(targetCopy.Value())
    
    for i in range(maxIterations):
        for bidAsk, boundaries in [('Bid', bidValues), ('Ask', askValues)]:
            for minValue, maxValue in zip(boundaries[:-1], boundaries[1:]):
                solveResult = acm.Math.Solve(SolveBlock, {'BidAsk':bidAsk}, solverValue[0 if bidAsk == 'Bid' else -1], minValue, maxValue, precision * 0.01, maxIterations)                
                if acm.Math.IsFinite(solveResult):
                    SetParameterValue(bidAsk, solveResult)
                    break
            else:
                raise ValueError('Failed to solve %s volatility' % bidAsk)
        resultValue = arrayAny(targetCopy.Value())
        for v, s in zip(resultValue, solverValue):
            if acm.Math.Abs(double(v) - double(s)) > precision and resultValue != previousResult:
                break
        else:
            break
        previousResult = resultValue

    else:
        for v, s in zip(resultValue, solverValue):
            if acm.Math.Abs(double(v) - double(s)) > precision * 1000 and resultValue != previousResult:
                raise ValueError('Failed to solve')
        
    result = acm.DenominatedValue(parameterNodes[0].Value(), None, None)

    for node in parameterNodes:
        node.RemoveSimulation()

    return result
