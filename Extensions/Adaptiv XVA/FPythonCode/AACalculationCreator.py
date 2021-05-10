""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACalculationCreator.py"
import AAComposer
import AAUtilFunctions as Util
import AAParamsAndSettingsHelper as Params

def createBaseValuationXML(valuationDate, baseCurrency):
    baseValCalculation = AAComposer.PairList()
    baseValCalculation["Object"] = "BaseValuation"
    baseValCalculation["Base_Date"] = Util.createDateString(valuationDate)
    baseValCalculation["Currency"] = baseCurrency.Name()
    baseValCalculation["Calculate_MtM"] = "Yes"
    baseValCalculationString = baseValCalculation.compose()
    return "<Calculation>" + baseValCalculationString + "</Calculation>"

def GetCVAParameters(creditCurveLabel, bankCurveLabel, correlation, cvaWithWrongWayRisk):
    cvaParameters = AAComposer.PairList()
    cvaParameters["Calculate"] = "Yes"
    cvaParameters["First_To_Default_Adjustment"] = Params.getCVAFirstToDefaultAdjustment()
    cvaParameters["Counterparty"] = creditCurveLabel
    cvaParameters["Bank"] = bankCurveLabel
    cvaParameters["Deflate_Stochastically"] = Params.getCVADeflateStochastically()
    stochasticHazardRateFlag = "No"
    if cvaWithWrongWayRisk:
        stochasticHazardRateFlag = "Yes"
    cvaParameters["Stochastic_Hazard_Rates"] = stochasticHazardRateFlag
    cvaParameters["CDS_Tenors"] = ""
    cvaParameters["Counterparty_Bank_Correlation"] = correlation
    cvaParametersString= cvaParameters.compose()
    return cvaParametersString

def GetCVAResultsView():
    cvaResults = AAComposer.PairList()
    cvaResults["Object"] = ""
    cvaResults["Show"] = "CVA"
    cvaResultsString= cvaResults.compose()
    return '<ResultsViewer ViewTypes="Pivot">' + cvaResultsString + "</ResultsViewer>"

def GetPFEResultsView():
    pfeResults = AAComposer.PairList()
    pfeResults["Object"] = ""
    pfeResults["Show"] = "PFE"
    pfeResultsString = pfeResults.compose()
    return '<ResultsViewer ViewTypes="Series">' + pfeResultsString + "</ResultsViewer>"

def GetCashflowResultsView():
    pfeResults = AAComposer.PairList()
    pfeResults["Object"] = ""
    pfeResults["Show"] = "Cashflow_Analysis"
    pfeResultsString = pfeResults.compose()
    return '<ResultsViewer ViewTypes="Pivot">' + pfeResultsString + "</ResultsViewer>"

def GetCollateralResultsView():
    pfeResults = AAComposer.PairList()
    pfeResults["Object"] = ""
    pfeResults["Show"] = "Collateral"
    pfeResultsString = pfeResults.compose()
    return '<ResultsViewer ViewTypes="Pivot">' + pfeResultsString + "</ResultsViewer>"

def getDeterministicScenarios(getRiskFactorArchiveFunc, valuationDate):
    useDeterministic = Params.useRiskFactorArchive()
    deterministicScenarios = \
        "[Deterministic_Scenarios=%s,Scenario_Path=%s,Database_Name=]" % (
        "FromFile" if useDeterministic else "Off",
        getRiskFactorArchiveFunc(valuationDate) if useDeterministic else ""
    )
    return deterministicScenarios

def createCommonXML(valuationDate, baseCurrency, deflationCurveLabel, nbrScenarios, getRiskFactorArchiveFunc):
    calculation = AAComposer.PairList()
    calculation["Object"] = "CreditMonteCarlo"
    calculation["Base_Date"] = Util.createDateString(valuationDate)
    calculation["Currency"] = baseCurrency.Name()
    calculation["Adjust_To_External_MtM"] = Params.getAdjustToExternalMtM()
    calculation["Base_Time_Grid"] = Params.getCVABaseTimeGrid()
    calculation["Sub_Calculations"] = "[[Bank,,,Auto,Bank,0,0],[Counterparty,,,Auto,Counterparty,0,0]]"
    calculation["Scenarios"] = str(nbrScenarios)
    calculation["Antithetic"] = Params.getCVAAntithetic()
    calculation["Sampling"] = "Unstratified"
    calculation["Random_Seed"] = Params.getRandomSeed()
    calculation["Use_Dynamic_Dates"] = Params.getCVAUseDynamicDates()
    calculation["Scenario_Time_Grid"] = Params.getCVAScenarioTimeGrid()
    calculation["Max_Horizon"] = Params.getCVAMaxHorizon()
    calculation["Deflation_Interest_Rate"] = deflationCurveLabel
    calculation["Deterministic_Scenarios"] = getDeterministicScenarios(
        getRiskFactorArchiveFunc=getRiskFactorArchiveFunc,
        valuationDate=valuationDate
    )
    calculation["Default_Conditioning"] = "[Calculate=No,Counterparty=]"
    return calculation

def createCVAXML(valuationDate, baseCurrency, creditCurveLabel, bankCurveLabel, deflationCurveLabel, nbrScenarios, correlation, cvaWithWrongWayRisk):
    cvaCalculation = createCommonXML(
        valuationDate=valuationDate, baseCurrency=baseCurrency,
        deflationCurveLabel=deflationCurveLabel, nbrScenarios=nbrScenarios,
        getRiskFactorArchiveFunc=Params.getRiskFactorArchiveFileCva
    )
    cvaCalculation["Exclude_Paid_Today"] = Params.getExcludePaidToday()
    cvaCalculation["No_Model_Evolution"] = Params.getNoModelEvolution()
    cvaCalculation["Credit_Valuation_Adjustment"] = "[" + GetCVAParameters(creditCurveLabel, bankCurveLabel, correlation, cvaWithWrongWayRisk) + "]"
    cvaCalculationString = cvaCalculation.compose()
    return "<Calculation>" + cvaCalculationString + "</Calculation>" + GetCVAResultsView()

def createPFEXML(valuationDate, baseCurrency, deflationCurveLabel, nbrScenarios, pfePercentile, pfeProfileSettings):
    pfeCalculation = createCommonXML(
        valuationDate=valuationDate, baseCurrency=baseCurrency,
        deflationCurveLabel=deflationCurveLabel, nbrScenarios=nbrScenarios,
        getRiskFactorArchiveFunc=Params.getRiskFactorArchiveFilePfe
    )
    pfeCalculation["Percentiles"] = pfePercentile
    pfeCalculation["Exclude_Paid_Today"] = Params.getExcludePaidToday()
    pfeCalculation["Base_Time_Grid"] = Params.getPFEBaseTimeGrid()
    pfeCalculation["Antithetic"] = Params.getPFEAntithetic()
    pfeCalculation["Use_Dynamic_Dates"] = Params.getPFEUseDynamicDates()
    pfeCalculation["Scenario_Time_Grid"] = Params.getPFEScenarioTimeGrid()
    pfeCalculation["Max_Horizon"] = Params.getPFEMaxHorizon()
    pfeCalculation["No_Model_Evolution"] = Params.getNoModelEvolution()
    cflProfileOutput =  'None' if pfeProfileSettings.At("cashflowProfileOutput") == 'No' else \
        pfeProfileSettings.At("cashflowProfileOutput")
    pfeCalculation["Cashflow_Analysis"] = "[" + "Output=" + cflProfileOutput + "," + "Currency_Options=" + pfeProfileSettings.At("cashflowProfileCurrencyOptions") + "," + "Percentiles=" + pfePercentile + "]"
    pfeCalculation["Collateral"] = "[" + "Output=" + pfeProfileSettings.At("collateralProfileOutput") + "," + "Funding_Charge=" + pfeProfileSettings.At("collateralProfileFundingCharge") + "," + "Partition_By_Deal=" + pfeProfileSettings.At("collateralProfilePartitionByDeal") + "]"
    pfeCalculationString = pfeCalculation.compose()
    return "<Calculation>" + pfeCalculationString + "</Calculation>" + GetPFEResultsView() + GetCashflowResultsView() + GetCollateralResultsView()
