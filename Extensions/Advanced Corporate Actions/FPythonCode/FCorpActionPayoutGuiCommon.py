""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionPayoutGuiCommon.py"
tt_PayoutRate = 'The rate of the payout'
tt_PayoutAmount = 'The amount of the payout'
tt_PayoutNetAmount = 'The net amount of the payout'
tt_PayoutGrossAmount = 'The gross amonut of the payout'
tt_Price = 'The price of the payout'
tt_Fee = 'The fee of the payout'
tt_CaChoice = 'The Corporate Action choice which owns the payout'
tt_Currency = 'The currency of the payout'
tt_PriceCurrency = 'The price currency of the payout'
tt_FeeCurrency = 'The fee currency of the payout'
tt_Oid = 'The oid of the payout'
tt_NewInstrument = 'The new instrument of the payout'


import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionPayout
import FBDPCommon
import FCorpActionPayoutGuiCommon

import FCustomTextObjectViewer
importlib.reload(FCustomTextObjectViewer)

ael_variables = None

ADDITIONALINFO_RECORDTYPE = "CorpActionPayout"
addInfoNames = FBDPCommon.getAdditionalInfoNames(ADDITIONALINFO_RECORDTYPE)

def customTextDlg(shell, params):
    customDlg = FCustomTextObjectViewer.FCustomTextObjectViewer(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def populateGuiFromPayout(payout, fieldValues):
    for var in ael_variables:
        if var.varName == 'CaChoice':
            fieldValues[var.sequenceNumber] = payout.CaChoice().Oid()
        elif var[0] in addInfoNames:
            addinfo = payout.AddInfos()
            for i in addinfo:
                spec = i.AddInf()
                name = spec.FieldName()
                if name == var[0]:
                    fieldValues[var.sequenceNumber] = i.FieldValue()
        elif var.varName == 'NewInstrument':
            fieldValues[var.sequenceNumber] = payout.NewInstrument()
        else:
            fieldValues[var.sequenceNumber] = payout.GetProperty(var[0])

    return fieldValues

def oid_cb(index, fieldValues):
    if isinstance(fieldValues[index], (int, long)):
        payout = acm.FCorporateActionPayout[fieldValues[index]]
        if payout:
            fieldValues = populateGuiFromPayout(payout, fieldValues)
    return fieldValues

ael_variables = FBDPGui.AelVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['PayoutRate',
                'Payout Rate',
                'string', None, None,
                None, 0, tt_PayoutRate, None, 1],
        ['PayoutAmount',
                'Payout Amount',
                'string', None, None,
                None, 0, tt_PayoutAmount, None, 1],
        ['PayoutNetAmount',
                'Payout Net Amount',
                'string', None, None,
                None, 0, tt_PayoutNetAmount, None, 1],
        ['PayoutGrossAmount',
                'Payout Gross Amount',
                'string', None, None,
                None, 0, tt_PayoutGrossAmount, None, 1],
        ['Price',
                'Price',
                'string', None, None,
                None, 0, tt_Price, None, 1],
        ['Fee',
                'Fee',
                'string', None, None,
                None, 0, tt_Fee, None, 1],
        ['CaChoice',
                'Choice',
                'FCorporateActionChoice', None, None,
                1, 0, tt_CaChoice, None],
        ['NewInstrument',
                'New Instrument',
                'FInstrument', None, None,
                None, 0, tt_NewInstrument, None, 1],
        ['Currency',
                'Currency',
                'FCurrency', None, None,
                None, 0, tt_Currency, None, 1],
        ['PriceCurrency',
                'Price Currency',
                'FCurrency', None, None,
                None, 0, tt_PriceCurrency, None, 1],
        ['FeeCurrency',
                'Fee Currency',
                'FCurrency', None, None,
                None, 0, tt_FeeCurrency, None, 1],
        ['SourceRecord',
                'Source Record_Advanced',
                'FCustomTextObject', None, None,
                None, 1, None, None, 1, customTextDlg],
        ['Oid',
                'Oid_hidden_Advanced',
                'string', None, None,
                None, None, tt_Oid, oid_cb])
