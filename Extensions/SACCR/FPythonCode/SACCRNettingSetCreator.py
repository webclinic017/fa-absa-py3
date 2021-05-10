""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/saccr/./etc/SACCRNettingSetCreator.py"
import AAComposer
from collections import defaultdict
import AAParamsAndSettingsHelper as Params
logger = Params.getAdaptivAnalyticsLogger()

def createSACCRNettingSetWithTags(tags, collateralAgreement, openingBalance, collateralAssetsList):
    nettingSet = AAComposer.PairList()
    nettingSet["Object"] = "NettingCollateralSet"
    nettingSet["Reference"] = "Non-netted trades"
    nettingSet["MtM"] = "&lt;undefined&gt;"
    nettingSet["Tags"] = "[" + tags + "]"
    nettingSet["Netted"] = "False"
    nettingSet["Collateralized"] = "False"
    nettingSet["Apply_Closeout_When_Uncollateralized"] = "No"
    return nettingSet.compose()

def createSACCRNettingSet(creditBalance, collateralAgreement, openingBalance, collateralAssetsList):
    nettingSet = AAComposer.PairList()
    nettingSet["Object"] = "NettingCollateralSet"
    nettingSet["MtM"] = "&lt;undefined&gt;"
    if collateralAgreement:
        nettingSet["Reference"] = creditBalance.Name() + ': : :'
        insType = 'Swap'
        #if creditBalance.BalancePortfolio().Trades().Size() > 0:
            #insType = creditBalance.BalancePortfolio().Trades()[0].Instrument().InsType()
        tags = creditBalance.Name() + ',0,Interest Rate,' + creditBalance.Currency().Name() + ':' + creditBalance.Currency().Name() + ',' + insType + ',False'
        nettingSet["Tags"] = '[' + tags + ']'
        nettingSet["Netted"] = "True"
        nettingSet["Collateralized"] = "True"
        nettingSet["Agreement_Currency"] = collateralAgreement.Currency().Name()
    else:
        nettingSet["Reference"] = "Non-netted trades"
        insType = 'Swap'
        #if creditBalance.BalancePortfolio().Trades().Size() > 0:
        #    insType = creditBalance.BalancePortfolio().Trades()[0].Instrument().InsType()
        tags = '&lt;NONE&gt;,0,Interest Rate,' + creditBalance.Currency().Name() + ':' + creditBalance.Currency().Name() + ',' + insType + ',False'
        nettingSet["Tags"] = '[' + tags + ']'
        nettingSet["Netted"] = "False"
        nettingSet["Collateralized"] = "False"
        nettingSet["Agreement_Currency"] = creditBalance.Currency().Name()
    nettingSet["Apply_Closeout_When_Uncollateralized"] = "No"
    return nettingSet.compose()