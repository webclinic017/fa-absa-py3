""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_fva/./etc/AAFVACalculationCreator.py"
import AAComposer
import ast
import FBDPCommon
import AAUtilFunctions as Util
import AACalculationCreator as BaseCreator
import AAParamsAndSettingsHelper as Params
import AAFVAPluginSettings as FVAParams

def GetFVAParameters(currency, creditCurveLabel, bankCurveLabel, correlation, cvaWithWrongWayRisk):
    fundingCostInterestCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingCostInterestCurve')
    fundingCostInterestCurve = ast.literal_eval(fundingCostInterestCurve)
    
    fundingBenefitInterestCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingBenefitInterestCurve')
    fundingBenefitInterestCurve = ast.literal_eval(fundingBenefitInterestCurve)
    
    fundingCreditCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'FundingCreditCurve')
    fundingCreditCurve = ast.literal_eval(fundingCreditCurve)
    
    riskFreeCurve = FBDPCommon.valueFromFParameter('FxVAParameters', 'RiskFreeCurve')
    riskFreeCurve = ast.literal_eval(riskFreeCurve)
    
    fvaParameters = AAComposer.PairList()
    fvaParameters["Calculate"] = "Yes"
    fvaParameters["Deflate_Stochastically"] = Params.getCVADeflateStochastically()
    fvaParameters["Funding_Cost_Interest_Curve"] = FVAParams.getCurveName(currency.Name(), fundingCostInterestCurve)
    fvaParameters["Funding_Benefit_Interest_Curve"] = FVAParams.getCurveName(currency.Name(), fundingBenefitInterestCurve)
    fvaParameters["Funding_Credit_Curve"] = FVAParams.getCurveName(currency.Name(), fundingCreditCurve)
    fvaParameters["Risk_Free_Curve"] = FVAParams.getCurveName(currency.Name(), riskFreeCurve)
    fvaParameters["Survival_Factors"] = ""
    fvaParameters["Stochastic_Funding"] = "No"
    fvaParametersString= fvaParameters.compose()
    return fvaParametersString

def GetFVAResultsView():
    fvaResults = AAComposer.PairList()
    fvaResults["Object"] = ""
    fvaResults["Show"] = "FVA (plugin)"
    fvaResultsString= fvaResults.compose()
    return '<ResultsViewer ViewTypes="Pivot">' + fvaResultsString + "</ResultsViewer>"

def createFVAXML(valuationDate, baseCurrency, creditCurveLabel, bankCurveLabel, deflationCurveLabel, nbrScenarios, correlation, cvaWithWrongWayRisk):
    fvaCalculation = BaseCreator.createCommonXML(
        valuationDate=valuationDate, baseCurrency=baseCurrency,
        deflationCurveLabel=deflationCurveLabel, nbrScenarios=nbrScenarios,
        getRiskFactorArchiveFunc=Params.getRiskFactorArchiveFileFva
    )
    fvaCalculation["Adjust_To_External_MtM"] = "Yes"
    fvaCalculation["FVA Calculation Properties"] = "[" + GetFVAParameters(baseCurrency, creditCurveLabel, bankCurveLabel, correlation, cvaWithWrongWayRisk) + "]"
    fvaCalculationString = fvaCalculation.compose()
    return "<Calculation>" + fvaCalculationString + "</Calculation>" + GetFVAResultsView()
