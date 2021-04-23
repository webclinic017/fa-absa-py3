""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FOpenCorpActionPayout.py"
"""----------------------------------------------------------------------------
MODULE
    FOpenCorpActionPayout - GUI Module to open to a corporate action 
    Payout definition.

DESCRIPTION
----------------------------------------------------------------------------"""



import ast
import acm
import FBDPCommon

infoSpecs = acm.FAdditionalInfoSpec.Select("recType=CorpActionPayout")

def run_main(d, payout):
    payout.PayoutRate = d['PayoutRate']
    payout.PayoutAmount = d['PayoutAmount']
    payout.PayoutNetAmount = d['PayoutNetAmount']
    payout.PayoutGrossAmount = d['PayoutGrossAmount']
    payout.Price = d['Price']
    payout.Fee = d['Fee']
    payout.CaChoice = d['CaChoice'].Oid() if d['CaChoice'] else None
    payout.Currency = d['Currency'].Oid() if d['Currency'] else None
    payout.PriceCurrency = d['PriceCurrency'].Oid() if d['PriceCurrency'] else None
    payout.FeeCurrency = d['FeeCurrency'].Oid() if d['FeeCurrency'] else None
    payout.NewInstrument = d['NewInstrument'].Oid() if d['NewInstrument'] else None
    
    existedAddInfoSpec = []
    addinfo = payout.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        existedAddInfoSpec.append(name)
        if name in list(d.keys()):
            i.FieldValue(d[name])

    srcRecord = payout.SourceRecord()
    if srcRecord and not payout.Name():
        txt = srcRecord.Text()
        srcDict = ast.literal_eval(txt)
        if all (k in srcDict for k in ('Payout Number', 'Option Number', 'CA ID')):
            name = ' '.join([srcDict['Payout Number'], srcDict['Option Number'], srcDict['CA ID']])
            payout.Name(name)

    payout.Commit()
    addinfo = payout.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        if name in list(d.keys()) and name not in existedAddInfoSpec:
            existedAddInfoSpec.append(name)
            i.FieldValue(d[name])
            i.Commit()

    for spec in infoSpecs:
        name = spec.Name()
        if name in existedAddInfoSpec:
            continue
        if name in list(d.keys()) and d[name]:
            newAddInfo = acm.FAdditionalInfo()
            newAddInfo.AddInf(spec)
            newAddInfo.Parent(payout)
            newAddInfo.FieldValue(d[name])
            newAddInfo.Commit()
