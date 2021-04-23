"""
Description             : Added settle type
Department and Desk     : Securities Lending
Requester               : Sabir Ballim
Developer               : Ickin Vural
CR Number               : C000000466028

History
=======

2017-01-31  Vojtech Sidorin     ABITFA-4481:   Update the use of FCallDepositFunctions.backdate
2020-12-22  Ncediso Nkambule    FAOPS-1022:    Added Client party type to the party type check on the module
"""

import acm
import ael

from FCallDepositFunctions import (
        NumberFormatting,
        amendTradeAccountLink,
        intEndDay,
        adjust,
        backdate,
        )
import SAGEN_str_functions


global ssiFA
global ssiFACurrent
global ssiCFRA
global ssiCFRACurrent
global ssiFRA
global ssiFRACurrent

ssiFA = []
ssiFACurrent = ''
ssiFRA = []
ssiFRACurrent = ''

try:
    ssiFA = ssiFAx
    ssiFACurrent = ssiFACurrentx
    ssiFRA = ssiFRAx
    ssiFRACurrent = ssiFRACurrentx

except:
    pass

ael_gui_parameters = {'runButtonLabel':   '&&Update',
                      'hideExtraControls': True,
                      'windowCaption' : 'Backdate cashflows'}
ael_variables=[
                ['amount', 'Amount', 'string', '', '', 0, 0, "The fixed amount.", NumberFormatting],
                ['date', 'Date', 'date', '', '', 0, 0, "The date when the cash should have been entered."],
                ['payday', 'Pay Day', 'date', '', ael.date_today(), 1, 0],
                ['settleType', 'Settlement Type', 'string', ["Settle", "Internal", "DTI", "Against Paper", "Reversal", "Square Off", "Interest Repayment", "Please Phone", "Migration Adjustment", "Debit Cheque Account"], "Settle", 0, 0],
                ['cfFA', 'Fixed Amount', 'string', ssiFA, ssiFACurrent],
                ['cfFRA', 'Backdated Interest', 'string', ssiFRA, ssiFRACurrent],
              ]


def backDate(eii):
    global ssiFAx
    global ssiFACurrentx
    global ssiFRAx
    global ssiFRACurrentx

    ssiFAx = []
    ssiFACurrentx = ''
    ssiFRAx = []
    ssiFRACurrentx = ''

    ins = eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().RowObject().Instruments()[0]
    trd = ins.Trades()[0]

    for ssiFAC in trd.Counterparty().SettleInstructions():
        if ssiFAC.CashSettleCashFlowType() == 'Fixed Amount':
            ssiFAx.append(ssiFAC.Name())
        elif ssiFAC.CashSettleCashFlowType() == 'Fixed Rate Adjustable':
            ssiFRAx.append(ssiFAC.Name())

    if trd.AccountLinks():
        for tal in trd.AccountLinks():
            if tal.PartyType() in ['Counterparty', 'Client']:
                if tal.SettleInstruction():
                    if tal.SettleInstruction().CashSettleCashFlowType() == 'Fixed Amount':
                        ssiFACurrentx = tal.SettleInstruction().Name()
                    if tal.SettleInstruction().CashSettleCashFlowType() == 'Fixed Rate Adjustable':
                        ssiFRACurrentx = tal.SettleInstruction().Name()

    acm.RunModuleWithParametersAndData('ABSABackDateAmount', 'Standard', eii)


def ael_main_ex(parameter, addData):
    eii = addData.At('customData')
    date = parameter['date']
    amount = float(parameter['amount'].replace(',', ''))
    payday = parameter['payday']

    if date in (None, ""):
        date = payday

    inslist = eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().RowObject().Instruments()
    ins = inslist.At(0)
    amendTradeAccountLink(ins, parameter['cfFA'], None, parameter['cfFRA'])
    bank = SAGEN_str_functions.split_string(1, parameter['cfFA'], '/', 0)

    int_per_end = intEndDay(ins, date)
    if int_per_end is not None and int_per_end < ael.date_today():
        backdate(ins, amount, date, payday, parameter['settleType'], bank=bank)
    else:
        adjust(ins, amount, date, settle_type=parameter["settleType"], bank=bank)
