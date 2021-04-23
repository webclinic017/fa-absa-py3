

from __future__ import print_function
import acm
import ael
import time

def listlistAsMatrix(listlist):
    res = acm.FRealMatrix()
    for row in range(len(listlist)):
        newRow = acm.FRealArray()
        for col in range(len(listlist[row])):
            newRow.Add(listlist[row][col])
        res.AddRow(newRow)
    return res

CreateCValuationFunction = acm.GetFunction('udmcFunction', 1)
CorrLogNormProcess       = acm.GetFunction('udmcCorrLogNormProcess', 16)
datetime                 = acm.GetFunction('datetime', 1)
double                   = acm.GetFunction('double', 1)
NowAsDays                = acm.GetFunction('NowAsDays', 0)
asianBasketFuncADFL      = acm.GetFunction('asianBasketArithmeticFixMonteCarlo', 15)
basketFuncADFL           = acm.GetFunction('basketMonteCarlo', 13)

def RunPerformanceTests():
    expiryDate          = '2008-04-02'
    payDate             = '2008-04-04 12:00:00'
    valuationDateTime   = str("2006-11-29")
    asianDate           = '2008-01-02'

    multiUnderlyingValue = [100.0, 100.0, 100.0]
    multiUnderlyingVolatility =  [0.25, 0.20, 0.30]
    
    multiUnderlyingCorrelationMatrixList = [[1.0,   0.7,    0.7], \
                                            [0.7,  1.0,    0.7], \
                                            [0.7,  0.7,   1.0]]
    multiUnderlyingCorrelationMatrix = listlistAsMatrix(multiUnderlyingCorrelationMatrixList)
    udmcDividends = [acm.FDenominatedValueArray(), acm.FDenominatedValueArray(), acm.FDenominatedValueArray()]
    stdmcDividends = [[], [], []]
    isQuantoOption = False
    multiUnderlyingQuantoCorrelation = []
    multiUnderlyingVolatilityForQuantoAdjustedCarryCost = []
    multiUnderlyingFxVolatility = []
    discRate = 0.05
    divDisc = [discRate, discRate,  discRate]
    basketFxAdjustedWeights = [0.333333, 0.333333, 0.333333]
    
    histPrices = acm.FRealMatrix()
    histPrices.AddRow(acm.FRealArray())
    histPrices.AddRow(acm.FRealArray())
    histPrices.AddRow(acm.FRealArray())

    strikeValue = 100.0
    asianWeights = [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]

    # UDMC Parameters
    
    vanillaBasketFor = """
    param double strikeValue;
    param matrix(double) basketFxAdjustedWeights;
    matrix(double) bwt = transpose(basketFxAdjustedWeights);
    double basketValue = 0.0;
    double optionValue = 0.0;
    int nAsset = 3;
    int i = 0;
    process matrix(double) S;
    basketValue = 0.0;
    for i = 0 to nAsset{
        basketValue = basketValue + bwt[i,0] * S[i, 0];
    };
    optionValue = max(0.0,basketValue-strikeValue);
    cashFlow(0, optionValue);
    """

    vanillaBasketElMul = """
    param double strikeValue;
    param matrix(double) basketFxAdjustedWeights;
    matrix(double) bwt = transpose(basketFxAdjustedWeights);
    double basketValue = 0.0;
    double optionValue = 0.0;
    process matrix(double) S;
    basketValue = sum(bwt .* S);
    optionValue = max(0.0,basketValue-strikeValue);
    cashFlow(0, optionValue);
    """

    nSim =  1000000
    seed = 730403
    udmcRandomGenerator = 3
    udmcSeed = 730403
    antiThetic = 0

    multiUnderlyingUdmcProcess = CorrLogNormProcess(multiUnderlyingValue, multiUnderlyingVolatility, [expiryDate], histPrices, multiUnderlyingCorrelationMatrix, divDisc, divDisc, udmcDividends, valuationDateTime, isQuantoOption, multiUnderlyingQuantoCorrelation, multiUnderlyingVolatilityForQuantoAdjustedCarryCost, multiUnderlyingFxVolatility, udmcRandomGenerator, udmcSeed, antiThetic);
    valFuncElMul = CreateCValuationFunction(vanillaBasketElMul)
    valFuncFor = CreateCValuationFunction(vanillaBasketFor)
    
    parameters = {'S':multiUnderlyingUdmcProcess, \
                    'strikeValue':strikeValue, \
                    'basketFxAdjustedWeights': basketFxAdjustedWeights, \
                    'payDate': payDate}

    aelExpiryDate = ael.date(expiryDate)
    aelTexp = ael.date_today().years_between(aelExpiryDate)

    print ('****************** Performance test: vanilla basket call option ******************')
    tuc = time.clock()
    stdmc = basketFuncADFL(multiUnderlyingValue, multiUnderlyingVolatility, strikeValue, discRate, divDisc, divDisc, 1, valuationDateTime, payDate, stdmcDividends, multiUnderlyingCorrelationMatrix, basketFxAdjustedWeights, nSim)
    tic = time.clock()
    udmcElMul = valFuncElMul.PerformCValuationFlatRate(parameters, discRate, valuationDateTime, payDate, "EUR", [expiryDate], nSim)

    tac = time.clock()
    udmcFor = valFuncFor.PerformCValuationFlatRate(parameters, discRate, valuationDateTime, payDate, "EUR", [expiryDate], nSim)
    

    toc = time.clock()
    print ('                   Value          (Time (s))')
    print ('STDMC:             ', stdmc, '(', tic - tuc, ')')
    print ('UDMC (el wise mul):', udmcElMul.At('result'), '(', tac - tic, ')', (tac - tic) / (tic - tuc) * 100.0, '%')
    print ('UDMC (for loop):   ', udmcFor.At('result'), '(', toc - tac, ')', (toc - tac) / (tic - tuc) * 100.0, '%')
    print ('\n')
    
    asianElMul = """
    param double strikeValue;
    param matrix(double) basketFxAdjustedWeights;
    matrix(double) bwt = transpose(basketFxAdjustedWeights);
    double basketValue = 0.0;
    double optionValue = 0.0;
    process matrix(double) S;
    basketValue = sum(bwt .* rowAverage(S,0,2));
    optionValue = max(0.0,basketValue-strikeValue);
    cashFlow(0, optionValue);
    """

    asianFor = """
    param double strikeValue;
    param matrix(double) basketFxAdjustedWeights;
    matrix(double) bwt = transpose(basketFxAdjustedWeights);
    double basketValue = 0.0;
    double optionValue = 0.0;
    double aw = 0.5;
    int a = 0;
    int t = 0;
    process matrix(double) S;
    basketValue = 0.0;
    for a = 0 to 3
    {
        for t = 0 to 2
        {
            basketValue = basketValue + aw * S[a,t] * bwt[a, 0];
        };
    };
    optionValue = max(0.0,basketValue-strikeValue);
    cashFlow(0, optionValue);
    """
    
    asianBskValFuncElMul = CreateCValuationFunction(asianElMul)
    asianBskValFuncFor = CreateCValuationFunction(asianFor)
    asianBskProcess = CorrLogNormProcess(multiUnderlyingValue, multiUnderlyingVolatility, [expiryDate, expiryDate, expiryDate], histPrices, multiUnderlyingCorrelationMatrix, divDisc, divDisc, udmcDividends, valuationDateTime, isQuantoOption, multiUnderlyingQuantoCorrelation, multiUnderlyingVolatilityForQuantoAdjustedCarryCost, multiUnderlyingFxVolatility, udmcRandomGenerator, udmcSeed, antiThetic);
    ap = {'S':asianBskProcess, \
            'strikeValue':strikeValue, \
            'basketFxAdjustedWeights': basketFxAdjustedWeights, \
            'payDate': payDate}
            
    aelAsianDate = ael.date(asianDate)
    aelTAsian = ael.date_today().years_between(aelAsianDate)
    asianTimes = [aelTAsian, aelTexp]
            
    tuc = time.clock()
    asianStdmc = asianBasketFuncADFL(multiUnderlyingValue, multiUnderlyingVolatility, strikeValue, discRate, divDisc, divDisc, 1, valuationDateTime, expiryDate, stdmcDividends,  multiUnderlyingCorrelationMatrix, basketFxAdjustedWeights, [expiryDate, expiryDate, expiryDate], 0.333333333333, nSim)
            
    tic = time.clock()
    asianElMul = asianBskValFuncElMul.PerformCValuationFlatRate(ap, discRate, valuationDateTime, payDate, "EUR", [expiryDate], nSim)
    
    tac = time.clock()
    asianFor = asianBskValFuncFor.PerformCValuationFlatRate(ap, discRate, valuationDateTime, payDate, "EUR", [expiryDate], nSim)
    
    toc = time.clock()
    print ('****************** Performance test: asian basket call option ******************')
    print ('                   Value          (Time (s))')
    print ('STDMC:             ', asianStdmc, '(', tic - tuc, ')')
    print ('UDMC (el wise mul):', asianElMul.At('result'), '(', tac - tic, ')', (tac - tic) / (tic - tuc) * 100.0, '%')
    print ('UDMC (for loop):   ', asianFor.At('result'), '(', toc - tac, ')', (toc - tac) / (tic - tuc) * 100.0, '%')
    print ('\n')
    
RunPerformanceTests()




