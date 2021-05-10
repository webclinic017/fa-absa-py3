import acm

def getCPIPrice(ins, zarSwap, zarReal, valday):
    maturity = ins.ExpiryDate()
    days = acm.Time().DateDifference(maturity, valday)
    tf = 182.5 / days
    df1 = zarReal.Discount(valday, maturity)
    df2 = zarSwap.Discount(valday, maturity) 
    cpiPrice = (((df1/df2) ** tf) - 1) * 2
    cpiPrice = cpiPrice * 100 
    return ins.DenominatedValue(cpiPrice, valday)
        
def getYieldCurve(ycName):
    yc = acm.FBenchmarkCurve[ycName]
    if yc.RealTimeUpdated():
        yc.Calculate()
    return yc
    
def shiftBenchmarkPriceBucketCPI(yc, shift, bucketStart, bucketEnd, benchmark, zarCPICurve):
    shiftBm = acm.GetFunction("shiftBenchmarkPriceBucket", 5)
    createReplaceCurve = acm.GetFunction("createReplaceCurve", 2)
    zarCPI = acm.FBenchmarkCurve["ZAR-CPI"]
    if yc == zarCPI:
        now = acm.Time().TimeNow()
    
        # Shift benchmark in the ZAR-SWAP curve
        zarSwap = getYieldCurve("ZAR-SWAP")
        shiftedZarSwap = shiftBm(zarSwap, shift, bucketStart, bucketEnd, benchmark)
        shiftedZarSwapCurve = shiftedZarSwap.IrCurveInformation()
        
        # Shift benchmark in the ZAR-REAL curve
        zarReal = getYieldCurve("ZAR-REAL")
        shiftedZarReal = shiftBm(zarReal, shift, bucketStart, bucketEnd, benchmark)
        shiftedZarRealCurve = shiftedZarReal.IrCurveInformation()
        
        # Calculate new benchmark prices for the ZAR-CPI curve 
        bmInstruments = zarCPI.BenchmarkInstruments()
        bmPrices = acm.FArray();
        for bmInstrument in bmInstruments:
            bmPrice = getCPIPrice(bmInstrument, shiftedZarSwapCurve, shiftedZarRealCurve, now)
            bmPrices.Add(bmPrice)
        
        # Create a new ZAR-CPI curve that is calibrated to the shifted benchmark prices
        resultCurve = zarCPICurve.Clone()
        resultCurve.Calculate(zarCPI, bmPrices)
        resultYC = createReplaceCurve(resultCurve, zarCPI)
        return resultYC
        
    else:
        # This is not the ZAR-CPI curve => use standard functionality
        return shiftBm(yc, shift, bucketStart, bucketEnd, benchmark)
