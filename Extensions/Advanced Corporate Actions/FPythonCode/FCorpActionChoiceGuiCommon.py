""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionChoiceGuiCommon.py"
import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActChoice
import FCorpActionPayoutViewer
import FBDPCommon
import FCustomTextObjectViewer

ael_variables = None

ADDITIONALINFO_RECORDTYPE = "CorpActChoice"
addInfoNames = FBDPCommon.getAdditionalInfoNames(ADDITIONALINFO_RECORDTYPE)

tt_Name = 'The name of the option'
tt_CaPayoutsOids = 'list of payouts for the option'
tt_CorpAction = 'The corporate action of this option'
tt_Buy = 'Indicates buy as opposed to sell'
tt_IsDefault = 'Indicate if the choice is the default one'
tt_Oid = 'The oid of the choice'

def populateGuiFromChoice(choice, fieldValues):
    for var in ael_variables:
        if var[0] in addInfoNames:
            addinfo = choice.AddInfos()
            for i in addinfo:
                spec = i.AddInf()
                name = spec.FieldName()
                if name == var[0]:
                    fieldValues[var.sequenceNumber] = i.FieldValue()
        else:
            if var[0] != 'CaPayoutsOids':
                fieldValues[var.sequenceNumber] = choice.GetProperty(var[0])
            else:
                payouts = ''
                if choice.Oid() > 0:
                    for p in choice.CaPayouts():
                        payouts += str(p.Oid())
                        payouts += ','
                    payouts = payouts[:-1]
                fieldValues[var.sequenceNumber] = payouts
    return fieldValues

def oid_cb(index, fieldValues):
    if isinstance(fieldValues[index], (int, long)):
        choice = acm.FCorporateActionChoice[fieldValues[index]]
        if choice:
            fieldValues = populateGuiFromChoice(choice, fieldValues)
    return fieldValues

def customDialog(shell, params):
    customDlg = FCorpActionPayoutViewer.PayoutsListCustomDialog(params)    
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customTextDlg(shell, params):
    customDlg = FCustomTextObjectViewer.FCustomTextObjectViewer(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

ael_variables = FBDPGui.AelVariables(
        ['Name',
                'Name',
                'string', None, None,
                None, 1, tt_Name, None, 1],
        ['CaPayoutsOids',
                'Payouts',
                'int', None, None,
                0, 0, tt_CaPayoutsOids, None, 1, customDialog],
        ['CorpAction',
                'Corporate Action',
                'FCorporateAction', None, None,
                1, 1, tt_CorpAction, None],
        ['IsDefault',
                'IsDefault',
                'int', ['1', '0'], 1,
                1, 0, tt_IsDefault],
        ['Oid',
                'Oid_hidden',
                'string', None, None,
                None, None, tt_Oid, oid_cb],
        ['ChoiceRecord',
                'Option Record_Advanced',
                'FCustomTextObject', None, None,
                None, 1, None, None, 1, customTextDlg],)
