""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AANettingSetCreator.py"
import AAComposer
from collections import defaultdict
import AAParamsAndSettingsHelper as Params
logger = Params.getAdaptivAnalyticsLogger()

def createNettingSet(collateralAgreement, openingBalance, collateralAssetsList):
    nettingSet = AAComposer.PairList()
    nettingSet["Object"] = "NettingCollateralSet"
    nettingSet["Netted"] = "True"

    if collateralAgreement:
        nettingSet["Collateralized"] = "True"
        nettingSet["Agreement_Currency"] = collateralAgreement.Currency().Name()
        nettingSet["Credit_Support_Amounts"] = "[Received_Threshold=1=" + str(int(round(collateralAgreement.ThresholdReceive()))) + \
                                                "\,Posted_Threshold=1=" + str(-int(round(collateralAgreement.ThresholdPost()))) + \
                                                "\,Minimum_Received=1=" + str(collateralAgreement.MinimumReceiveAmount()) + \
                                                "\,Minimum_Posted=1="  + str(collateralAgreement.MinimumPostAmount()) + "\]"
        nettingSet["Settlement_Period"] = str(collateralAgreement.SettlementPeriodInDays())
        nettingSet["Liquidation_Period"] = str(collateralAgreement.LiquidationPeriodInDays())
        nettingSet["Opening_Balance"] = str(int(openingBalance))
        nettingSet["Balance_Currency"] = collateralAgreement.Currency().Name()
        nettingSet["Collateral_Assets"] = createCollateralAssetStr(collateralAssetsList)
        
    else:
        nettingSet["Collateralized"] = "False"
    
    nettingSet["Apply_Closeout_When_Uncollateralized"] = "No"
    return nettingSet.compose()
    
def createCollateralAssetStr(collateralAssetsList):
    stringDict = defaultdict(str)
    sepCharDict = defaultdict(str)
    
    for coll in collateralAssetsList:
        collAsset = AAComposer.PairList()

        if coll[0] == "Cash":
            collAsset["Haircut_Posted"] = str(0)
            collAsset["Haircut_Received"] = str(0)
            collAsset["Currency"] = coll[2].Name()
            collAsset["Amount"] = str(abs(coll[1]))

        elif coll[0] == "Bond":
            try:
                collAsset["Issuer"] = coll[2].Name()
            except:
                logger.ELOG("Missing required field for collateral instrument %s: Issuer" % coll[8])
                continue
            collAsset["Haircut_Posted"] = "%s%%" % str(coll[3]).replace(",", ".")
            collAsset["Haircut_Received"] = "%s%%" % str(coll[3]).replace(",", ".")
            collAsset["Currency"] = coll[4].Name()
            collAsset["Maturity"] = "%sD" % str(int(coll[5]))
            collAsset["Principal"] = str(abs(coll[1]))
            collAsset["Coupon_Rate"] = "%s%%" % str(coll[6]).replace(",", ".")
            collAsset["Coupon_Interval"] = str(coll[7])
            
        else:
            collAsset["Haircut_Posted"] = "%s%%" % str(coll[3]).replace(",", ".")
            collAsset["Haircut_Received"] = "%s%%" % str(coll[3]).replace(",", ".")
            collAsset[coll[0]] = coll[2]
            collAsset["Units"] = str(abs(coll[1]))
            
        collStr = "[" + collAsset.compose() + "]"
        stringDict[coll[0]] = sepCharDict[coll[0]].join([stringDict[coll[0]], collStr])
        sepCharDict[coll[0]] = ","
    
    collAssets = AAComposer.PairList()
    if len(stringDict["Bond"]):
        collAssets["Bond_Collateral"] = "[" + stringDict["Bond"] + "]"
    if len(stringDict["Cash"]):
        collAssets["Cash_Collateral"] = "[" + stringDict["Cash"] + "]" 
    if len(stringDict["Equity"]):
        collAssets["Equity_Collateral"] = "[" + stringDict["Equity"] + "]"
    if len(stringDict["Commodity"]):
        collAssets["Commodity_Collateral"] = "[" + stringDict["Commodity"] + "]"
    
    return "[" + collAssets.compose() + "]"
