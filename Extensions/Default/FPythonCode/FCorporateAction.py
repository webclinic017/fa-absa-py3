""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCorporateAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCorporateAction - Module which executes Corporate Actions.

DESCRIPTION
    This module executes the Corporate Actions.

----------------------------------------------------------------------------"""


import acm
import ael

import FBDPCommon
import FBDPGui
import importlib
importlib.reload(FBDPGui)

import FScripDivConst

ScriptName = 'Corporate Action'
Logfile = 'CorporateAction.log'
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
            'FCAVariables', 'FTemplateBasis')


"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

recently_changed_rows = []

qStockIns = FBDPGui.insertStock()
qNewIns = FBDPGui.insertInstruments(
    instype=('Stock', 'Option', 'Warrant', 'EquityIndex'))

Markets = []
for pt in ael.Party.select():
    if pt.type in ('Market', 'Broker', 'MtM Market'):
        Markets.append(pt.ptyid)


qCorpAction = FBDPGui.insertCorpAction()
cvTemplate = FBDPGui.getCorpActTemplateNames()


supportedDerivativeTypes = ('Option', 'Warrant', 'Future', 'CFD',
        'DepositaryReceipt', 'Total Return Swaps', 'SecurityLoan', 'Repo')


toDoList = ('Distribute it', 'Move the stock position to it',
        'Use it as underlying to adjusted derivatives')

disabledTemplateExceptions = ('Corpact', 'Instrument', 'Exdate',
        'Template', 'NewQuantity', 'OldQuantity', 'NewInstrument',
        'StrikeDecimals', 'CashAmount')

def instrumentQuery():
    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    op = q.AddOpNode('OR')
    op.AddAttrNode('InsType', 'EQUAL', None)
    return q


def baseTemplate():
    return FBDPGui.Parameters('FTemplateBasis').__dict__.copy()


def enableVar(ael_variable, enabled, disabledTooltip):
    ael_variable.enable(enabled, disabledTooltip)
    recently_changed_rows.append(ael_variable)


def clearDisabledField(fieldValues):
    for ael_var in recently_changed_rows:
        if not ael_var.isEnabled() and \
        ael_var[0] not in ["NewQuantity", "OldQuantity"]:
            fieldValues[ael_var.sequenceNumber] = None

    del recently_changed_rows[:]
    return fieldValues


def disableRow(row, enabled=0, disabledTooltip='', fieldValues={}):
    if row[0] in ('Logfile',
                  'Testmode',
                  'Logmode',
                  'LogToConsole',
                  'LogToFile',
                  'SendReportByMail',
                  'MailList',
                  'ReportMessageType',
                  'ShortCodeFieldName',
                  'OldShortCode',
                  'NewShortCode',
                  'Date',
                  'ProtectedMarkets',
                  'SavePriceChanges',
                  'CashCurrency',
                  'ChangeWeights',
                  'ProtectedComb',
                  'ChangeWeightsWithRfactor',
                  'ChangeWeightsWithStrikeDiff',
                  'NewContractSizeFormula',
                  'OldContractSizeFormula'):
        return
    rows = [row]
    values = [enabled]
    tt = [disabledTooltip]
    if row[0] == 'CashAmount':
        rows.append(getattr(ael_variables, 'CashCurrency'))
        values.append(enabled)
        tt.append(disabledTooltip)
    elif row[0] == 'ChangeHistoricalPrices':
        rows.extend([getattr(ael_variables, 'ProtectedMarkets'),
                getattr(ael_variables, 'SavePriceChanges')])
        on = enabled and int(fieldValues[
                ael_variables.ChangeHistoricalPrices.sequenceNumber])
        values.extend([on, on])
        t = ("This variable is only enabled if Historical Prices under the "
                "Change tab is selected.")
        tt.extend([t, t])
    elif row[0] == 'ChangeQuantity':
        rows.append(getattr(ael_variables, 'ChangeWeights'))
        rows.append(getattr(ael_variables, 'ProtectedComb'))
        rows.append(getattr(ael_variables, 'ChangeWeightsWithRfactor'))
        rows.append(getattr(ael_variables, 'ChangeWeightsWithStrikeDiff'))

        on1 = enabled and int(
                fieldValues[ael_variables.ChangeQuantity.sequenceNumber])
        on2 = enabled and int(
                fieldValues[ael_variables.ChangeWeights.sequenceNumber])
        tt1 = ('This variable is only enabled if Quantity under the Change '
                'tab is selected.')
        tt2 = ('This variable is only enabled if Weights under the Change '
                'tab is selected.')
        values.extend([on1, on2, on2, on2])
        tt.extend([tt1, tt2, tt2, tt2])

    for i in range(len(rows)):
        enableVar(rows[i], values[i], tt[i])

def disableTemplate(fieldValues,
                    obj='',
                    exceptions=disabledTemplateExceptions,
                    force=None,
                    toolTip='This variable is not applicable.'):
    obj = obj.split(',')
    if force or force == None and len(obj) > 1:
        enabled = False
        obj = ''
    else:
        enabled = True
        obj = obj and obj[0]
    for i in ael_variables:
        variableName = i[0]
        if variableName in exceptions:
            e = 1
        else:
            e = enabled
        disableRow(i, enabled=e, disabledTooltip=toolTip,
                fieldValues=fieldValues)
    enableVar(ael_variables.Date, force or
        not fieldValues[ael_variables.Template.sequenceNumber] and
        not fieldValues[ael_variables.Corpact.sequenceNumber],
        'It is only possible to edit this variable if no templates and no '
        'corporate actions are chosen.')
    return obj


def setVariables(d, fieldValues):
    return ael_variables.setVariables(d, fieldValues)


def date_callback(index, fieldValues):
    date = fieldValues[index]
    toolTip = 'This field is not applicable if a Date is entered.'
    disableTemplate(fieldValues,
                    exceptions=['Date'],
                    force=date,
                    toolTip=toolTip)

    if not date:
        fieldValues = ael_variables.InstrumentType.callback(fieldValues)

    return clearDisabledField(fieldValues)


def corpact_callback(index, fieldValues):
    ca = fieldValues[index]
    toolTip = ('This field is not applicable if several corporate actions are '
            'choosen.')
    ca = disableTemplate(fieldValues, ca, ['Corpact'], toolTip=toolTip)
    ca = ca.strip('<>')
    fieldValues[index] = ca
    acmCorpAct = acm.FCorporateAction[ca.strip('"')]

    if acmCorpAct:
        template = disableTemplate(fieldValues, acmCorpAct.Template(),
                toolTip=toolTip)
        templateVariables = FBDPGui.Parameters(template).__dict__
        for vp in acmCorpAct.ViewableProperties().split():
            if vp == 'ExerciseMode':
                templateVariables[vp] = \
                    'Strike' if acmCorpAct.GetProperty(vp) else 'Market'
            else:
                templateVariables[vp] = acmCorpAct.GetProperty(vp)

        fieldValues = setVariables(templateVariables, fieldValues)
        fieldValues = ael_variables.Template.callback(fieldValues)
    return clearDisabledField(fieldValues)


def template_callback(index, fieldValues):
    template = fieldValues[index]
    toolTip = 'This field is not applicable if several templates are choosen.'
    template = disableTemplate(fieldValues, template, toolTip=toolTip)

    if acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
            template):
        d = baseTemplate()
        d.update(FBDPGui.Parameters(template).__dict__)
        fieldValues = setVariables(d, fieldValues)
        fieldValues[index] = "<" + fieldValues[index] + ">"
    fieldValues = ael_variables.InstrumentType.callbackIfEnabled(fieldValues)
    fieldValues = ael_variables.ChangeQuantity.callbackIfEnabled(fieldValues)
    fieldValues = ael_variables.ChangeContractSize.callbackIfEnabled(
        fieldValues)

    return clearDisabledField(fieldValues)


def InstrumentType_callback(index, fieldValues):
    instype = fieldValues[index]

    name = (fieldValues[index] == instype and fieldValues[index] or
            fieldValues[index] + '(' + instype + ')')
    toolTip = 'This variable is not applicable to InstrumentType ' + name + '.'

    enabledFields = (("AliasType",
                          "ChangeName",
                          "InstrumentNameDecimals",
                          "ChangeStrike",
                          "ChangeRebate",
                          "ChangeBarriers",
                          "StrikeDecimals",
                          "CopyIsin",
                          "AddModifier",
                          "AdjustOTC",
                          "NewOptions",
                          "DerivativeTypes",
                          "Derivatives"),
                         ('NewPrice',
                          "ChangeDividends",
                          "DividendDecimals"))
    isStock = instype == 'Stock'
    for i in ael_variables:
        if i[0] in enabledFields[not isStock]:
            enabled = 0
        else:
            enabled = 1

        if enabled and "InstrumentType" in i[7] or \
            not enabled and (i.isEnabled() or "InstrumentType" in i[7]):
            disableRow(i, enabled=enabled, disabledTooltip=toolTip)

    fieldValues = ael_variables.NewInstrument.callbackIfEnabled(fieldValues)
    return clearDisabledField(fieldValues)

def NewInstrument_callback(index, fieldValues):
    ins = fieldValues[index]
    tt = ("This variable is only applicable if a new instrument is specified "
            "in the NewInstrument field")
    if isinstance(ins, str) and ins != '':
        ins = acm.FInstrument[ins] and ael_variables.NewInstrument.isEnabled()
    if (ins and fieldValues[ael_variables.InstrumentType.sequenceNumber] ==
                "Derivative"):
        enableVar(ael_variables.ShortCodeFieldName, True, "")
        ael_variables.ShortCodeFieldName.callback(fieldValues)
    elif (fieldValues[ael_variables.Template.sequenceNumber] ==
                '<NameChangeDerivative>'):
        enableVar(ael_variables.ShortCodeFieldName, False, "")
        fieldValues[ael_variables.ShortCodeFieldName.sequenceNumber] = 'Other'
        ael_variables.ShortCodeFieldName.callback(fieldValues)
    else:
        ttt = tt + "and the InstrumentType field equals Derivative."
        enableVar(ael_variables.ShortCodeFieldName, False, ttt)
        enableVar(ael_variables.OldShortCode, False, ttt)
        enableVar(ael_variables.NewShortCode, False, ttt)

    disableRow(ael_variables.WhatToDoWithNewInstrument, ins, tt)
    fieldValues = ael_variables.WhatToDoWithNewInstrument.callback(fieldValues)
    return clearDisabledField(fieldValues)


def NewPrice_callback(index, fieldValues):
    newprice = fieldValues[index]
    disableRow(ael_variables.SpinoffCostFraction, newprice == 'CostFraction',
               'This variable is only applicable if the new price of the '
               'distributed Instument is of type CostFraction.')
    if newprice == 'CostFraction':
        f = 0.0
    else:
        f = ""
    fieldValues[ael_variables.SpinoffCostFraction.sequenceNumber] = f
    return clearDisabledField(fieldValues)


def WhatToDo_callback(index, fieldValues):
    enabled = ael_variables.WhatToDoWithNewInstrument.isEnabled()
    enable_newprice = (enabled and
            fieldValues[ael_variables.InstrumentType.sequenceNumber] == 'Stock'
            and fieldValues[index] in ('Distribute it',
            'Move the stock position to it'))
    enable_costfraction = (enable_newprice and
            fieldValues[ael_variables.NewPrice.sequenceNumber] ==
            'CostFraction')
    disableRow(ael_variables.NewPrice, enable_newprice, 'This variable is '
            'only applicable if a new instrument is distributed, or if a '
            'stock position is moved to a new instrument.')
    disableRow(ael_variables.SpinoffCostFraction, enable_costfraction,
            'This variable is only applicable if the new price of the '
            'distributed Instument is of type CostFraction.')
    return clearDisabledField(fieldValues)


def HistPrices_callback(index, fieldValues):
    enable = 0
    tt = ("This variable is only enabled if Historical Prices under the "
            "Change tab is selected.")
    if int(fieldValues[index]):
        enable = 1
    enableVar(ael_variables.ProtectedMarkets, enable, tt)
    enableVar(ael_variables.SavePriceChanges, enable, tt)
    return clearDisabledField(fieldValues)


def Weights_callback(index, fieldValues):
    enable = 0
    tt = ("This variable is only enabled if '%s' under the Change tab is "
            "selected.")
    if not fieldValues[index]:
        return fieldValues
    if int(fieldValues[index]):
        enable = 1
    if index == ael_variables.ChangeQuantity.sequenceNumber:
        enableVar(ael_variables.ChangeWeights, enable, tt % 'Quantity')
        ael_variables.ChangeContractSize.enable(not enable)

    enableVar(ael_variables.ProtectedComb, enable and
            fieldValues[ael_variables.ChangeWeights.sequenceNumber],
            tt % 'Weights')
    enableVar(ael_variables.ChangeWeightsWithRfactor, enable and
            fieldValues[ael_variables.ChangeWeights.sequenceNumber],
            tt % 'Weights')
    enableVar(ael_variables.ChangeWeightsWithStrikeDiff, enable and
            fieldValues[ael_variables.ChangeWeights.sequenceNumber],
            tt % 'Weights')
    return clearDisabledField(fieldValues)


def FormulaContractSize_callback(index, fieldValues):
    enable = 0
    tt = ("This variable is only enabled if '%s' under the Change tab is "
            "selected.")
    if bool(fieldValues[index]):
        enable = 1
    if index == ael_variables.ChangeContractSize.sequenceNumber:
        ael_variables.ChangeQuantity.enable(not enable)

        enableVar(ael_variables.NewContractSizeFormula, enable,
                tt % 'Contract Size')
        enableVar(ael_variables.OldContractSizeFormula, enable,
                tt % 'Contract Size')

    return clearDisabledField(fieldValues)


def FieldName_callback(index, fieldValues):
    enable = False
    tt = "This variable is only applicable if ShortCodeFieldName equals Other."
    if fieldValues[index] == "Other":
        enable = True
    enableVar(ael_variables.OldShortCode, enable, tt)
    enableVar(ael_variables.NewShortCode, enable, tt)
    return clearDisabledField(fieldValues)

def position_cb(index, fieldValues):
    tt = 'You can only select one type of object.'
    for field in (ael_variables.TradeFilter,
        ael_variables.Portfolio):
        if ael_variables[index] != field:
            enableVar(field, not fieldValues[index], tt)
    return clearDisabledField(fieldValues)

def settledate_callback(index, fieldValues):
    if not fieldValues[ael_variables.Settledate.sequenceNumber] and \
            fieldValues[ael_variables.Instrument.sequenceNumber] and \
            fieldValues[ael_variables.Exdate.sequenceNumber]:
        exdate = FBDPCommon.toDateAEL(
                fieldValues[ael_variables.Exdate.sequenceNumber])
        ins = acm.FInstrument[
                fieldValues[ael_variables.Instrument.sequenceNumber]]
        fieldValues[ael_variables.Settledate.sequenceNumber] = \
                FBDPCommon.businessDaySpot(ins, exdate)
    return clearDisabledField(fieldValues)

def Derivative_cb(index, fieldValues):
    tt = 'You can only select one type of object.'
    for field in [ael_variables.DerivativeTypes,
            ael_variables.Derivatives]:
        if ael_variables[index] != field:
            enableVar(field, not fieldValues[index], tt)
    return clearDisabledField(fieldValues)

def recordDateCallback(index, fieldValues):
    pass


#Tooltip
exdate_tp = 'The corporate action takes place on this date'
corpact_tp = 'Select the corporate action to execute. '
settledate_tp = 'The settle date for the created trades.'
recorddate_tp = ('The record date is the cut-off date used to determine'
        ' which shareholders are eligible to receive a distribution.')
template_tp = ('The Template(s) specifies type of corporate action and scope '
        'of execution.  If this field is empty, and the field Date is '
        'defined, the hook \'get_corporate_actions\' will be run if defined.  '
        'If this hook is not defined all corporate actions with exdate before '
        '\'Date\' will be run.')
instrument_tp = ('The instrument subject to the corporate action. This field '
        'should only contain one instrument.  If more than one is selected, '
        'the first one will be assumed to be the subject of the corporate '
        'action.')
derivatives_tp = ('The derivatives handled in the execution.')
newqty_tp = ('Specifies, together with OldQuantity, the ratio for the '
        'corporate action')
oldqty_tp = ('Specifies, together with NewQuantity, the ratio for the '
        'corporate action')
chtradep_tp = 'Should the script adjust the average price of the position?'
chqty_tp = 'Should the script adjust the quantity of the position?'
chctrsize_tp = 'Should the contract size of the derivatives be adjusted?'
newFormula_tp = ('Should the contract size of the derivatives be adjusted by '
        'the adjustment factor (i.e. Eurex R-factor, OldQuantity divided by '
        'NewQuantity)?  Note: This is the new approach introduced in Eurex '
        'Release 11.0 on 10th November 2008.')
oldFormula_tp = ('Should the contract size of the derivatives be adjusted by '
        'the strike factor (i.e. the rounded new strike price divided by the '
        'old strike price)?  Note: This is the old approach used before '
        'Eurex Release 11.0, which was introduced on 10th November 2008.')
chname_tp = 'Should the script adjust the name of the instrument(s)?'
chstrike_tp = 'Should the script adjust the strike price of the options?'
chbarriers_tp = 'Should the script adjust the barriers of the options?'
chrebate_tp = 'Should the script adjust the rebate of the options?'
chhistp_tp = ('Should the script adjust historical prices for the '
        'instrument(s)? Should only be used if using method Adjust.')
chdiv_tp = 'Should the script adjust dividends connected to the stock?'
chwght_tp = ('Should the corresponding weights in Combinations and Equity '
        'Indices be adjusted?')
chwghtWithRfactor_tp = ('Should the weights be adjusted by the adjustment '
        'factor (i.e. Eurex R-factor, OldQuantity divided by NewQuantity)?  '
        'Note: This is the new approach introduced in Eurex Release 11.0 on '
        '10th November 2008.')
chwghtWithStrike_tp = ('Should the weights be adjusted by the strike factor '
        '(i.e. the rounded new strike price divided by the old strike '
        'price)?  Note: This is the old approach used before Eurex Release '
        '11.0, which was introduced on 10th November 2008.')
round_tp = 'Number of decimals. -1 for no rounding'
date_tp = ('Run the hook \'get_corporate_actions\' if possible, else perform '
        'all corporate actions with Exdate before this date.')
whattodo_tp = 'Specifies how the NewInstrument should be used'
instype_tp = ('instrument types handled in the execution (Derivative = '
        'Options, Futures and Warrants)')
casham_tp = ('A cash amount per unit specified by an exchange as part of the '
        'Corporate Action, that will be saved to the Additional Payment '
        'table.')
cashcurr_tp = 'Currency of the cash payment'
newins_tp = ('For stock adjustment, used to specify new instrument in '
        'spin-off, New Issue etc. For derivative adjustment, used to specify '
        'new underlying')
addmod_tp = ('Should new derivatives have a trailing X, Y or Z in the '
        'instrument id?')
copyisin_tp = ('Should the ISIN-code of the old derivative be copied to the '
        'new one or should the isin of the new instrument be blank?')
adjotc_tp = 'Whether or not OTC instruments should be adjusted'
alias_tp = 'Only derivatives with an alias of this type will be adjusted'
shortcode_tp = ('Used for renaming options in connection with change of '
        'underlying. This field of the old and new underlying should hold the '
        'old and new short code.')
oldshortcode_tp = ('Used for renaming of options. Replace this string in the '
        'option name with the string in NewShortCode.')
newshortcode_tp = ('Used for renaming of options. In the option name, replace '
        'the string in OldShortCode with this string.')
roundcomp_tp = ('Create cash payment to compensate for rounding differences '
        'in closing and opening trades')
method_tp = ('Specifies whether positions should be adjusted by a closing and '
        'an opening trade (CloseAndOpen), a closing trade (CloseDown), by '
        'adjusting each trade in the position (Adjust), or by increasing or '
        'decreasing the positions (Increase/Decrease Position).')
newprice_tp = ('Specifies to which price the NewInstrument should be '
        'distributed')
spinoffcf_tp = ('The fraction of the total value that goes to the '
        'spinoffcompany in a stock spinoff. Expressed in percentage, written '
        'in the form 0.2 (which means 20%). ')
protmarket_tp = 'Historical prices on these market will not be adjusted'
saveprice_tp = ('Controls the possibility to roll back changes in historical '
        'prices (performance reasons)')
startdate_tp = 'Ignore trades made before this date'
newopt_tp = ('Whether the script should create new instrument or use the ones '
        'already received from an exchange')
closingprice_tp = ('Positions will be closed at this price (only relevant for '
        'method CloseDown and CloseAndOpen)')
protcomb_tp = ('Do not adjust weights in these Combinations and Equity '
        'Indices.')
onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
                'Filters or Portfolios - should be used.')
ttStoredFolder = ('Select positions using Stored Folders. '
                '{0}'.format(onlyOne))
ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'the default behaviour is to group by portfolio.')
ttDoExeAss = ('Generate exercise and assignment transactions to close '
        'in-the-money positions')
ttDoAbandon = ('Generate abandon transactions to close out-of-the-money '
        'positions')
ttsettle_price = ('If defined, this price will be used instead of the '
        'underlying\'s settlement-price per expiration date. Should be '
        'expressed in the quote type of the underlying.')
ttstrike_price = ('The strike price used in the right issue')
#tttrades = ('Select the positions that should be handled by the script')
ttsettlemarket = ('The underlying\'s settlement price will primarily be '
        'taken from this Market')
ttmode = ('Defines at what price the derivative position should be closed, '
        'and the corresponding underlying trade opened')
ttCloseAll = ('Close all the positions if checked.')
ttPartialExercise = ('Specify the percentage of partial exercise')
ttScripIssuePerShare = ('The fraction that each currently held share is '
        'entitled to if the cash dividend is to be converted.  eg. 0.123456')
ttTradeQuantityRounding = 'Select the rounding convention'
ttPreview = ('Run the corporate action in preview mode. The newly created '
'trades will be in simulated status and the corporate action is pending '
'for approval.')

valid_modes = ['Market', 'Strike']
smarkets = map(lambda x: x.Name(), acm.FMTMMarket.Select(''))

defaultMode = 'Strike'

cvTradeQuantityRounding = FScripDivConst.ROUNDING_CHOICES

try:
    import FBDPHook
    importlib.reload(FBDPHook)
    defaultMode = FBDPHook.exercise_mode(1) and 'Strike' or 'Market'
except:
    pass

cvNewOptions = ['Already received from the Exchange', 'Please create']
cvNewPrice = ['Zero', 'MarkToMarket', 'StockPriceMinusRightStrike',
              'CostFraction', 'Diluted']
cvShortCodeFieldName = ['Insid', 'Extern_id1', 'Extern_id2', 'Other']
cvAdjustOTC = ['All', 'Only OTC', 'Only non OTC']
advancedMethods = [
    'Close And Open', 'Close Down', 'Adjust', 'Increase/Decrease Position'
]

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Preview',
                'Preview',
                'int', ['0', '1'], None,
                0, 0, ttPreview],
        ['Corpact',
                'Corpact',
                'FCorporateAction', None, qCorpAction,
                None, 1, corpact_tp, corpact_callback],
        ['Template',
                'Template',
                'string', cvTemplate, None,
                None, 1, template_tp, template_callback],
        ['Instrument',
                'Instrument',
                'FInstrument', None, qStockIns,
                None, 1, instrument_tp, settledate_callback],
        ['Exdate',
                'Exdate',
                'string', ['Today', 'Next banking day', ''], None,
                1, None, exdate_tp, settledate_callback],
        ['Recorddate',
                'Record Date',
                'string', None, None,
                None, None, recorddate_tp, recordDateCallback],
        ['Settledate',
                'Settledate',
                'string', None, None,
                1, None, settledate_tp],
        ['NewQuantity',
                'NewQuantity', 'string', None,
                None, None, None, newqty_tp],
        ['OldQuantity',
                'OldQuantity',
                'string', None, None,
                None, None, oldqty_tp],
        ['Date',
                'Date',
                'string', ['Today'], None,
                None, None, date_tp, date_callback],
        ['InstrumentType',
                'InstrumentType',
                'string', ['Stock', 'Derivative'], None,
                2, None, instype_tp, InstrumentType_callback],
        ['DerivativeTypes',
                'DerivativeTypes',
                'string', supportedDerivativeTypes, None,
                0, 1, instype_tp, Derivative_cb],
        ['Derivatives',
                'Derivatives',
                'FInstrument', None, instrumentQuery(),
                None, 1, derivatives_tp, Derivative_cb],
        ['CashAmount',
                'CashAmount',
                'string', None, None,
                None, None, casham_tp],
        ['CashCurrency',
                'CashCurrency',
                'FCurrency', None, None,
                None, 1, cashcurr_tp],
        ['ClosingPrice',
                'ClosingPrice',
                'string', ['Zero', 'Average', 'MarkToMarket'], None,
                None, None, closingprice_tp],
        ['NewInstrument',
                'NewInstrument',
                'FInstrument', None, qNewIns,
                None, 1, newins_tp, NewInstrument_callback],
        ['NewPrice',
                'NewPrice',
                'string', cvNewPrice, 'MarkToMarket',
                None, None, newprice_tp, NewPrice_callback],
        ['SpinoffCostFraction',
                'SpinoffCostFraction',
                'string', None, None,
                None, None, spinoffcf_tp],
        ['WhatToDoWithNewInstrument',
                'WhatToDoWithNewInstrument',
                'string', toDoList, toDoList[0],
                None, None, whattodo_tp, WhatToDo_callback],
        ['ChangeTradePrice',
                'Trade Price_Change',
                'int', ['0', '1'], None,
                None, None, chtradep_tp],
        ['ChangeQuantity',
                'Quantity_Change',
                'int', ['0', '1'], None,
                None, None, chqty_tp, Weights_callback],
        ['ChangeContractSize',
                'Contract Size_Change',
                'int', ['0', '1'], None,
                None, None, chctrsize_tp, FormulaContractSize_callback],
        ['NewContractSizeFormula',
                'Adjust contract size with Adjustment Factor_Change',
                'int', ['0', '1'], 1,
                None, None, newFormula_tp, FormulaContractSize_callback],
        ['OldContractSizeFormula',
                'Adjust contract size with Strike Factor_Change',
                'int', ['0', '1'], None,
                None, None, oldFormula_tp, FormulaContractSize_callback],
        ['ChangeName',
                'Name_Change',
                'int', ['0', '1'], None,
                None, None, chname_tp],
        ['ChangeStrike',
                'Strike_Change',
                'int', ['0', '1'], None,
                None, None, chstrike_tp],
        ['ChangeHistoricalPrices',
                'Historical Prices_Change',
                'int', ['0', '1'], None,
                None, None, chhistp_tp, HistPrices_callback],
        ['ChangeDividends',
                'Dividends_Change',
                'int', ['0', '1'], None,
                None, None, chdiv_tp],
        ['ChangeWeights',
                'Weights_Change',
                'int', ['0', '1'], None,
                None, None, chwght_tp, Weights_callback],
        ['ChangeWeightsWithRfactor',
                'Adjust weights with Adjustment Factor_Change',
                'int', ['0', '1'], 1,
                None, None, chwghtWithRfactor_tp],
        ['ChangeWeightsWithStrikeDiff',
                'Adjust weights with Strike Factor_Change',
                'int', ['0', '1'], None,
                None, None, chwghtWithStrike_tp],
        ['ChangeBarriers',
                'Barriers_Change',
                'int', ['0', '1'], None,
                None, None, chbarriers_tp],
        ['ChangeRebate',
                'Rebate_Change',
                'int', ['0', '1'], None,
                None, None, chrebate_tp],
        ['TradePriceDecimals',
                'TradePrice_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['QuantityDecimals',
                'Quantity_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['ContractSizeDecimals',
                'ContractSize_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['InstrumentNameDecimals',
                'InstrumentName_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['StrikeDecimals',
                'Strike_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['HistoricalPriceDecimals',
                'HistoricalPrice_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['DividendDecimals',
                'Dividend_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['WeightDecimals',
                'Weight_Rounding',
                'string', None, None,
                None, None, round_tp],
        ['AddModifier',
                'AddModifier_Advanced',
                'int', ['0', '1'], None,
                None, None, addmod_tp],
        ['CopyIsin',
                'CopyIsin_Advanced',
                'int', ['0', '1'], None,
                None, None, copyisin_tp],
        ['AdjustOTC',
                'AdjustOTC_Advanced',
                'string', cvAdjustOTC, None,
                None, None, adjotc_tp],
        ['AliasType',
                'AliasType_Advanced',
                'string', None, None,
                None, None, alias_tp],
        ['ShortCodeFieldName',
                'ShortCodeFieldName_Advanced',
                'string', cvShortCodeFieldName, 'Insid',
                None, None, shortcode_tp, FieldName_callback],
        ['OldShortCode',
                'OldShortCode_Advanced',
                'string', None, None,
                None, None, oldshortcode_tp],
        ['NewShortCode',
                'NewShortCode_Advanced',
                'string', None, None,
                None, None, newshortcode_tp],
        ['RoundingCompensationCash',
                'RoundingCompensationCash_Advanced',
                'int', ['0', '1'], None,
                None, None, roundcomp_tp],
        ['Method',
                'Method_Advanced',
                'string', advancedMethods, None,
                2, None, method_tp],
        ['ProtectedMarkets',
                'ProtectedMarkets_Advanced',
                'string', Markets, None,
                0, 1, protmarket_tp],
        ['SavePriceChanges',
                'SavePriceChanges_Advanced',
                'int', ['0', '1'], 1,
                None, None, saveprice_tp],
        ['StartDate',
                'StartDate_Advanced',
                'string', None, None,
                None, None, startdate_tp],
        ['NewOptions',
                'NewOptions_Advanced',
                'string', cvNewOptions, None,
                None, None, newopt_tp],
        ['ProtectedComb',
                'ProtectedCombinations_Advanced',
                'FInstrument', None, FBDPGui.insertCombinations(),
                None, 1, protcomb_tp],
        ['DoExerciseAssign',
                'Do Exercise Assign_Elective',
                'int', ['1', '0'], 1,
                1, 0, ttDoExeAss],
        ['DoAbandon',
                'Do Abandon_Elective',
                'int', ['1', '0'], 1,
                1, 0, ttDoAbandon],
        ['CloseAll',
                'Close All Positions_Elective',
                'int', ['1', '0'], 1,
                1, 0, ttCloseAll],
        ['ExercisePct',
                'Partially Exercise_Elective',
                'string', '0', '100',
                0, 0, ttPartialExercise],
        ['SettlePrice',
                'Settle Price_Elective',
                'string', '', '',
                0, None, ttsettle_price],
        ['StrikePrice',
                'Strike Price_Elective',
                'string', '', '',
                0, None, ttstrike_price],
        ['SettleMarket',
                'Name of Settlement Market_Elective',
                'string', smarkets, FBDPGui.getMtMMarket(),
                0, None, ttsettlemarket],
        ['ExerciseMode',
                'Mode_Elective',
                'string', valid_modes, defaultMode,
                0, None, ttmode],
        ['IssuePerShare',
                'Scrip Issue Per Share_Elective',
                'string', None, None,
                0, 0, ttScripIssuePerShare],
        ['RoundingType',
                'Trade Quantity Rounding_Elective',
                'string', cvTradeQuantityRounding, None,
                0, 0, ttTradeQuantityRounding],
        ['TradeFilter',
                'Trade Filter_Positions',
                'FTradeSelection', None, None,
                0, 1, ttTradeFilter, position_cb],
        ['Portfolio',
                'Portfolio_Positions',
                'FPhysicalPortfolio', None, None,
                0, 1, ttPortfolio, position_cb],
        ['Grouper',
                'Portfolio Grouper_Positions',
                'FStoredPortfolioGrouper', None, None,
                0, 1, ttGrouper, None]
)

def ael_main(dictionary):
    import FBDPCurrentContext
    import FBDPString
    importlib.reload(FBDPString)
    import FCAAction
    importlib.reload(FCAAction)

    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    if (FBDPCommon.toDate(dictionary['StartDate']) or
            ael.date_from_time(0)) > FBDPCommon.toDate(dictionary['Exdate']):
        raise Exception("StartDate must be smaller than ExDate.")
    for field in ['Template']:
        dictionary[field] = list(dictionary[field])
        for value in dictionary[field]:
            new_value = value.strip('<>')
            if new_value:
                dictionary[field][dictionary[field].index(value)] = new_value
            else:
                dictionary[field].pop(dictionary[field].index(value))

    pythonCorpAction = FCAAction.PerformCorporateActions()
    pythonCorpAction.perform(dictionary)
