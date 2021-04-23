""" Compiled: 2013-04-12 13:37:02 """

"""----------------------------------------------------------------------------
MODULE
    FManualExercise - Module to invoke manual ExerciseAssign.

    (c) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module runs a task dialog from a context menu on the Trading Sheet
    to manually exercise or abandon selected trades, with the option of
    manually forcing exercise or abandon.

    Task parameters are read from this module by the FManualExercise script.

----------------------------------------------------------------------------"""
import traceback

import acm
import ael

import FBDPGui

# Tool Tip
ttDoExeAss = "Generate exercise and assignment transactions to close in-the-money positions for 'Normal' trades"
ttDoAbandon =  "Generate abandon transactions to close out-of-the-money and at-the-money 'Normal' positions"
ttsettle_price = "If defined, this price will be used instead of the underlying's settlement-"\
                 "price per expiration date"
tttrades = "The positions that should be handled by the script"
ttactions = "Manual overrides to force exercise or abandon"
ttsettlemarket = "The underlying's settlement price will primarely be taken from this Market"
ttmode = "Defines at what price the derivative position should be closed, and the "\
         "corresponding underlying trade opened"
ttDoFixPhysicals = ("Fix physically settled futures and options so that the "
"close-out trade has pay date and acquire date equal to the expiry date of "
"the future/option")
valid_modes=['Market','Strike']

# Fill in smart default values
smarkets = map(lambda x: x.ptyid, ael.Party.select("type = 'MtM Market'"))
spot = acm.FParty['SPOT']
smarkets.append(spot.Name())
prices = ['MtM', 'Zero', 'Average']

ael_variables = None

def onManualExerciseAssign(invokationInfo):
    global ael_variables

    try:
        selection = invokationInfo.ExtensionObject().ActiveSheet().Selection()
        cells = selection.SelectedCells()
        trades = []
        actionsForTrades = {}
        for cell in cells:
            column = cell.Column()
            columnId = str(column.ColumnId())
            if columnId == 'Trade Action':
                rowObject = cell.RowObject()
                trade = rowObject.Trade()
                action = cell.Evaluator().Value()
                if action == 'Assign':
                    action = 'Exercise'
                actionsForTrades[trade.Oid()] = action
                trades.append(trade.Oid())

        tradeIds = ''
        for i in range(len(trades)):
            tradeIds = tradeIds + str(trades[i])
            if i <= len(trades) - 2:
                tradeIds = tradeIds + ', '
        ael_variables = FBDPGui.TestVariables(
            ('DoExeAss', 'Exercise ITM Normal Trades', 'int', ['1', '0'], 1, 1, 0, ttDoExeAss),
            ('DoAbandon', 'Abandon OTM and ATM Normal Trades', 'int', ['1', '0'], 1, 1, 0, ttDoAbandon),
            ('settle_price', 'Settle Price', 'string', '', '', 0, None, ttsettle_price),
            ('trades', 'Trades', 'FTrade', None, tradeIds, 2, 1, tttrades),
            ('actions_for_trades', 'Actions', 'string', None, str(actionsForTrades), 0, 0, ttactions),
            ('settlemarket', 'Name of Settlement Market', 'string', smarkets, 'SPOT', 2, None, ttsettlemarket),
            ('mode', 'Mode', 'string', valid_modes, 'Strike', 2, None, ttmode),
            ('DoFixPhysicals', 'Fix physically settled futures/options', 'int', ['1', '0'], 1, 1, 0, ttDoFixPhysicals))

        acm.RunModuleWithParameters('FManualExercise', 'Standard')
    except:
        traceback.print_exc()

def actionStatus(trd,*rest):
    status = "Normal"

    if trd.Type() == 'Abandon':
        return "Abandon"
    elif trd.Type() == 'Exercise':
        return "Exercise"
    elif trd.Type() == 'Assign':
        return "Assign"
    elif trd.Type() == 'Normal':
        ins = trd.Instrument()
        trades = ins.Trades()
        for t in trades:
            if t.Contract() and t.Contract().Oid() == trd.Oid() and t.Oid != trd.Oid() and t.Status() != 'Void' and t.Oid() > 0:
                status= t.Type()

    return status

