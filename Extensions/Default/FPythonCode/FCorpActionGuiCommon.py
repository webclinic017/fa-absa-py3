""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCorpActionGuiCommon.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCorpActionGuiCommon - GUI Module which holds common GUI entities.

DESCRIPTION
    Hold tooltips, callbacks and ael_variables for the corporate action GUI
----------------------------------------------------------------------------"""
import acm
import ael
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FScripDivConst
import FBDPCommon

name_tp = ('A unique name of the corporate action, the name is generated if '
        'no name is set.')
instr_tp = 'The instrument that is subject to the Corporate Action.'
instype_tp = ('instrument types handled in the execution')
exdate_tp = ('If you purchase a stock on its ex-dividend date or after,'
             ' you will not be entitled to the corporate action.'
             ' If you purchase before the ex-dividend date,'
             ' you are entitled to the corporate action.')
settledate_tp = 'The settle date for the created trades'
effectivedate_tp = 'The effective date of the corporate action'
expirationtime_tp = 'The expiration time of the corporate action'
tradingbegindate_tp = 'The first date on which rights can be sold'
tradingenddate_tp = 'The last date on which rights can be sold'
withdrawaldate_tp = ('Last date when a shareholder can withdraw from a '
                    'previous election to participate in an offer')
lot_size_tp = 'The lot size for this corporate action'
choicetype_tp = 'The corporate action choice type'
q_tp = 'The adjustment factor is OldQuantity / NewQuantity.'
template_tp = ('A corporate action template to override variables in '
        'FCAVariables.')
strikedec_tp = 'How many decimals are there in the strike?'
new_instr_tp = ('For some corporate actions (Merger, Spin-off, Buyback, New '
        'Issue, and Stock Dividend) it may be necessary to specify a new '
        'instrument.')
cash_tp = ('A cash amount per unit specified by an exchange as part of the '
        'Corporate Action, that will be saved to the Additional Payment '
        'table.')
cashcurr_tp = 'The currency of the cash amount.'
text_tp = 'The corporate action can be described here.'
eid_tp = 'Two corporate actions can not have the same external ID'
costfrac_tp = ('The fraction of a companys total value that goes to the '
        'spinoff company in a spinoff.')
linkedCorpActions_tp = ('Link to other corporate actions. ')
status_tp = 'Status for the corporate action.'
round_tp = 'Number of decimals. -1 for no rounding'
oid_tp = 'Unique identifier.'
ttDoExeAss = ('Generate exercise and assignment transactions to close '
        'in-the-money positions')
ttDoAbandon = ('Generate abandon transactions to close out-of-the-money '
        'positions')
ttsettle_price = ('If defined, this price will be used instead of the '
        'underlying\'s settlement-price per expiration date. Should be '
        'expressed in the quote type of the underlying.')
ttstrike_price = ('The strike price used in the rights issue')
ttsettlemarket = ('The underlying\'s settlement price will primarily be '
        'taken from this Market')
ttmode = ('Defines at what price the derivative position should be closed, '
        'and the corresponding underlying trade opened')
ttInstrument = ('Specify the instruments that will be processed.')
ttCloseAll = ('Close all the positions if checked.')
ttPartialExercise = ('Specify the percentage of partial exercise')
method_tp = ('Specifies whether positions should be adjusted by a closing and '
        'an opening trade (CloseAndOpen), a closing trade (CloseDown), or by '
        'adjusting each trade in the position (Adjust).')

valid_modes = ['Market', 'Strike']
onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
           'Filters or Portfolios - should be used.')
ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'the default behaviour is to group by portfolio.')
ttScripIssuePerShare = ('The fraction that each currently held share is '
        'entitled to if the cash dividend is to be converted.  eg. 0.123456')
ttTradeQuantityRounding = 'Select the rounding convention'
ttDividend = 'The dividend for reinvestment'

ael_variables = None
qNewIns = FBDPGui.insertNewInstrument()

cvTemplate = FBDPGui.getCorpActTemplateNames()
cvTradeQuantityRounding = FScripDivConst.ROUNDING_CHOICES

ADDITIONALINFO_RECORDTYPE = "CorpAction"
addInfoNames = FBDPCommon.getAdditionalInfoNames(ADDITIONALINFO_RECORDTYPE)

def name_cb(index, fieldValues):
    ca = acm.FCorporateAction[fieldValues[index]]
    if ca:
        fieldValues = populateGuiFromCA(ca, fieldValues)

    UpdateGui(index, fieldValues)
    return fieldValues

def name_copy_cb(index, fieldValues):
    ca = acm.FCorporateAction[fieldValues[index]]
    if ca:
        fieldValues = populateGuiFromCA(ca, fieldValues)
        ca = ca.Clone()
        fieldValues[ael_variables.Name.sequenceNumber] = 'Copy of ' + \
                            fieldValues[ael_variables.Name.sequenceNumber]

    UpdateGui(index, fieldValues)
    return fieldValues
    
def template_cb(index, fieldValues):
    index = ael_variables.Template.sequenceNumber
    if hasattr(ael_variables, 'Template'):
        template = fieldValues[ael_variables.Template.sequenceNumber]
        ApplyTemplate(ael_variables, template)
    return fieldValues

def cashamount_cb(index, fieldValues):
    ael_variables.CashCurrency.enable(float(
            fieldValues[ael_variables.CashAmount.sequenceNumber].strip()
                or 0))
    return fieldValues

def settledate_cb(index, fieldValues):
    ins = fieldValues[ael_variables.Instrument.sequenceNumber].strip()
    if ins and fieldValues[ael_variables.Exdate.sequenceNumber] and \
    index == ael_variables.Exdate.sequenceNumber:
        exdate = FBDPCommon.toDate(
                fieldValues[ael_variables.Exdate.sequenceNumber])
        ins = acm.FInstrument[ins]
        exdate_spot = FBDPCommon.businessDaySpot(ins, exdate)
        if fieldValues[ael_variables.Settledate.sequenceNumber] == "":
            fieldValues[ael_variables.Settledate.sequenceNumber] = \
                exdate_spot
        if fieldValues[ael_variables.Recorddate.sequenceNumber] == "":
            fieldValues[ael_variables.Recorddate.sequenceNumber] = \
                exdate_spot
        if fieldValues[ael_variables.EffectiveDate.sequenceNumber] == "":
            fieldValues[ael_variables.EffectiveDate.sequenceNumber] = \
                exdate

    return fieldValues

def populateGuiFromCA(ca, fieldValues):
    for var in ael_variables:
        if var[0] == 'LinkedCorpActions':
            evt = ca.BusinessEvent()
            if evt:
                actions = ael.CorpAction.select(
                    'business_event_seqnbr = "%i"' % evt.Oid())
                msg = ''
                for a in actions:
                    action = FBDPCommon.ael_to_acm(a)
                    if action != ca:
                        msg += action.Name() + ','
                fieldValues[var.sequenceNumber] = msg
        elif var[0] in addInfoNames:
            addinfo = ca.AddInfos()
            for i in addinfo:
                spec = i.AddInf()
                name = spec.FieldName()
                if name == var[0]:
                    fieldValues[var.sequenceNumber] = i.FieldValue()
        elif var[0] == 'Market':
            fieldValues[var.sequenceNumber] = (ca.GetProperty(var[0]).Name()
                                            if ca.GetProperty(var[0]) else None)
        elif var[0] == 'Dividend':
            fieldValues[var.sequenceNumber] = (ca.GetProperty(var[0]).Oid()
                                            if ca.GetProperty(var[0]) else None)
        else:
            fieldValues[var.sequenceNumber] = ca.GetProperty(var[0])

    return fieldValues

def ApplyTemplate(ael_variables, template):
    parameter = acm.GetDefaultContext().GetExtension('FParameters',
                                                    'FObject', template)
    if parameter == None:
        return
    template = parameter.Value()
    for key in template.Keys():
        val = template[key]
        key = key.Text()
        k = key.split('.')
        if len(k) > 1:
            key = k[0]
            if k[1] == 'Enable':
                if hasattr(ael_variables, key):
                    attr = getattr(ael_variables, key)
                    attr[9] = val

def ClearGui(index, fieldValues):
    for variable in ael_variables:
        variable.enable(True)

def UpdateGui(index, fieldValues):
    ClearGui(index, fieldValues)
    if hasattr(ael_variables, 'Template'):
        template = fieldValues[ael_variables.Template.sequenceNumber]
        ApplyTemplate(ael_variables, template)
    if hasattr(ael_variables, 'SpinoffCostFraction'):
        index = ael_variables.Template.sequenceNumber
        ael_variables.SpinoffCostFraction.enable(
                fieldValues[index] == 'SpinOffStock')
    if hasattr(ael_variables, 'CashCurrency'):
        ael_variables.CashCurrency.enable(float(
            fieldValues[ael_variables.CashAmount.sequenceNumber] or 0))


# [VariableName,
#       DisplayName,
#       Type, CandidateValues, Default,
#       Mandatory, Multiple, Description, InputHook, Enabled]

ael_variables = FBDPGui.AelVariables(['Name',
                'Name_Definition',
                'string', None, None,
                0, None, name_tp, name_cb],
        ['Template',
                'Template_Definition',
                'string', cvTemplate, None,
                0, 0, template_tp, template_cb],
        ['CaChoiceType',
                'Corporate Action Type_Definition',
                'string', ['Mandatory', 'MandatoryWithChoice', 'Voluntary'], None,
                0, 0, 'Choose the corporate action type'],
        ['Instrument',
                'Instrument_Definition',
                'FStock', None, None,
                1, 1, instr_tp, settledate_cb],
        ['Market',
                'Market_Definition',
                'FMarketPlace', None, None,
                0, None, None],
        ['Exdate',
                'Ex-date_Definition',
                'string', ['Today', 'Next banking day'], None,
                0, None, exdate_tp, settledate_cb],
        ['Recorddate',
                'Record Date_Definition',
                'string', None, None,
                0, None, settledate_tp],
        ['Settledate',
                'Settle Date_Definition',
                'string', None, None,
                0, None, settledate_tp],
        ['EffectiveDate',
                'Effective Date_Advanced',
                'date', None, None,
                0, None, effectivedate_tp],
        ['ExpirationTime',
                'Expiration Time_Advanced',
                'date', None, None,
                0, None, expirationtime_tp],
        ['WithdrawalDate',
                'Withdrawal Date_Advanced',
                'date', None, None,
                0, None, withdrawaldate_tp],
        ['TradingBeginDate',
                'Trading Begin Date_Advanced',
                'date', None, None,
                0, None, tradingbegindate_tp],
        ['TradingEndDate',
                'Trading End Date_Advanced',
                'date', None, None,
                0, None, tradingenddate_tp],
        ['NewQuantity',
                'New Quantity_Definition',
                'string', None, '1',
                None, None, q_tp],
        ['OldQuantity',
                'Old Quantity_Definition',
                'string', None, '1',
                None, None, q_tp],
        ['NewInstrument',
                'New Instrument_Definition',
                'FInstrument', None, qNewIns,
                None, 1, new_instr_tp],
        ['CashAmount',
                'Cash Amount_Definition',
                'string', None, '0.0',
                None, None, cash_tp, cashamount_cb],
        ['CashCurrency',
                'Cash Currency_Definition',
                'FCurrency', None, None,
                None, 1, cashcurr_tp, None, 0],
        ['Text',
                'Text_Definition',
                'string', None, None,
                None, None, text_tp],
        ['ExternalId',
                'ExternalId_Definition',
                'string', None, None,
                None, None, eid_tp],
        ['SpinoffCostFraction',
                'Spinoff Cost Fraction_Definition',
                'string', None, '0.0',
                None, None, costfrac_tp],
        ['LinkedCorpActions',
                'Linked Corporate Actions_Advanced',
                'FCorporateAction', None, None,
                None, None, linkedCorpActions_tp],
        ['IssuePerShare',
                'Scrip Issue Per Share_Advanced',
                'string', None, None,
                0, 0, ttScripIssuePerShare],
        ['Dividend',
                'Dividend_Advanced',
                'FDividend', None, None,
               0, 1, ttDividend, None, 0],
        ['RoundingType',
                'Trade Quantity Rounding_Advanced',
                'string', cvTradeQuantityRounding, None,
                0, 0, ttTradeQuantityRounding],
        ['Oid',
                'Oid_hidden',
                'string', None, None,
                None, None, oid_tp],
        ['Status',
                'Status_Advanced',
                'string', ['None', 'Active', 'Inactive', 'Processed'], 'None',
                2, None, status_tp],)
                
FBDPGui.createAdditionalInfoVariables(ael_variables, ADDITIONALINFO_RECORDTYPE)
