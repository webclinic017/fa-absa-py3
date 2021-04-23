""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FOpenCorpAction.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FOpenCorpAction - GUI Module to handle saving
                      a corporate action definition.

DESCRIPTION
----------------------------------------------------------------------------"""
import acm
import ael

import FBDPCommon
import FBusinessProcessUtils
import FCorpActionStatesSetup

infoSpecs = acm.FAdditionalInfoSpec.Select("recType=CorpAction")

def __setBusinessEvent(ca, parentCorpAction):
    bEvent = None
    if not parentCorpAction:
        bEvent = acm.FBusinessEvent()
        bEvent.Commit()
    else:
        if parentCorpAction.IsKindOf('FCorporateAction'):
            bEvent = parentCorpAction.BusinessEvent()

        if isinstance(parentCorpAction, type('')):
            parentCorpAction = parentCorpAction.strip()
            parentCorpAction = acm.FCorporateAction[parentCorpAction]
            bEvent = parentCorpAction.BusinessEvent()

        if isinstance(parentCorpAction, type([])):
            bEvent = parentCorpAction[0].BusinessEvent()

    if bEvent:
        ca.BusinessEvent = bEvent

    if ca.BusinessEvent() is None:
        print('No business event linked with the Corporate action.')
        return

def __setTemplate(ca, template):
    if not template:
        return

    cats = ca.Templates()
    cats.Delete()

    if isinstance(acm.FCorpactTemplate(), template):
        cat = template
    elif isinstance(template, type('')):
        cat = acm.FCorpactTemplate()
        cat.Name(template)
    elif isinstance(template, type([])):
        cat = template[0]

    if cat:
        cat.CorporateAction(ca)
        cat.Commit()

def run_main(d, ca):
    ca.Name = d['Name']
    ca.ExDate = FBDPCommon.toDate(d['Exdate']) or ''
    ca.RecordDate = FBDPCommon.toDate(d['Recorddate']) or ''
    ca.SettleDate = FBDPCommon.toDate(d['Settledate']) or ''
    ca.EffectiveDate = FBDPCommon.toDate(d['EffectiveDate']) or ''
    ca.ExpirationTime = FBDPCommon.toDate(d['ExpirationTime']) or ''
    ca.TradingBeginDate = FBDPCommon.toDate(d['TradingBeginDate']) or ''
    ca.TradingEndDate = FBDPCommon.toDate(d['TradingEndDate']) or ''
    ca.WithdrawalDate = FBDPCommon.toDate(d['WithdrawalDate']) or ''
    ca.Instrument = d['Instrument'][0]
    if d['Market']:
        ca.Market = d['Market']

    if len(d['Text']) > 38:
        print("Description text too long, only the first 38 characters will "
                "be saved!")
        d['Text'] = d['Text'][:38]
    ca.Text = d['Text']
    ca.SpinoffCostFraction = 'SpinoffCostFraction' in d and d['SpinoffCostFraction']
    ca.ExternalId = 'ExternalId' in d and d['ExternalId']
    ca.CaChoiceType = ael.enum_from_string('CorpActionChoiceType',
                                                d['CaChoiceType'])
    ca.AdjustQuantity = 1
    ca.AdjustTradePrice = 1
    if 'Dividend' in d and d['Dividend']:
        div = d['Dividend']
        if div:
            ca.Dividend = div[0].Oid()

    ca.Status = d['Status']
    existingAddInfoSpec = []
    addinfo = ca.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        existingAddInfoSpec.append(name)
        if name in d.keys():
            i.FieldValue(d[name])
    ca.Commit()

    addinfo = ca.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        if name in d.keys() and name not in existingAddInfoSpec:
            existingAddInfoSpec.append(name)
            i.FieldValue(d[name])
            i.Commit()

    for spec in infoSpecs:
        name = spec.Name()
        if name in existingAddInfoSpec:
            continue

        if name in d.keys() and d[name]:
            newAddInfo = acm.FAdditionalInfo()
            newAddInfo.AddInf(spec)
            newAddInfo.Parent(ca)
            newAddInfo.FieldValue(d[name])
            newAddInfo.Commit()

    if FCorpActionStatesSetup.CorporateActionUsingBusinessProcess():
        bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(ca,
                                'CorporateActionStateChart')
        bp.Commit()
    __setTemplate(ca, d['Template'])
