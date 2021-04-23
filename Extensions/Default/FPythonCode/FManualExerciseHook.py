""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FManualExerciseHook.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FManualExercise - Module to invoke manual ExerciseAssign.

DESCRIPTION
    This module runs a task dialog from a context menu on the Trading Sheet
    to manually exercise or abandon selected trades, with the option of 
    manually forcing exercise or abandon.
    
    Task parameters are read from this module by the FManualExercise script.

----------------------------------------------------------------------------"""
import sys
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
ttGrouper = ('Specify a grouper. If no grouper is selected, '
                'the default behaviour is to group by trade number.')
valid_modes=['Market','Strike']

# Fill in smart default values
smarkets = map(lambda x: x.ptyid, ael.Party.select("type = 'MtM Market'"))

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
            tag = cell.Tag()
            column = cell.Column()
            columnId = str(column.ColumnId())
            if columnId == 'Trade Action':
                rowObject = cell.RowObject()
                trade = rowObject.Trade()
                action = cell.Evaluator().Value()
                actionsForTrades[trade.Oid()] = action
                trades.append(trade.Oid())
                
        tradeIds = ''
        for i in range(len(trades)):
            tradeIds = tradeIds + str(trades[i])
            if i <= len(trades) - 2:
                tradeIds = tradeIds + ', '
        ael_variables = FBDPGui.TestVariables(
            ('DoExeAss', 'Exercise ITM Normal Trades', 'int', ['1', '0'], 0, 1, 0, ttDoExeAss),
            ('DoAbandon', 'Abandon OTM and ATM Normal Trades', 'int', ['1', '0'], 0, 1, 0, ttDoAbandon),
            ('settle_price', 'Settle Price', 'string', '', '', 0, None, ttsettle_price),
            ('trades', 'Trades', 'FTrade', None, tradeIds, 2, 1, tttrades),
            ('actions_for_trades', 'Actions', 'string', None, str(actionsForTrades), 1, 0, ttactions),
            ('settlemarket', 'Name of Settlement Market', 'string', smarkets, FBDPGui.getMtMMarket(), 2, None, ttsettlemarket),
            ('mode', 'Mode', 'string', valid_modes, 'Strike', 2, None, ttmode),
            ('PortfolioGrouper', 'Portfolio Grouper', 'FStoredPortfolioGrouper', None, None, 0, 1, ttGrouper))
        ScriptName = "Manual Exercise Assign Hook"

        acm.RunModuleWithParameters('FManualExercise', 'Standard')
    except:
        traceback.print_exc()

def actionStatus(trade):
    status = "Normal"
    if trade.Type() in ['Abandon', 'Exercise', 'Assign']:
        status = trade.Type()
    elif 'Normal' == trade.Type():
        for insTrade in trade.Instrument().Trades():
            if trade.IsEqual(insTrade.Contract()) and not trade.IsEqual(insTrade):
                status = insTrade.Type()
    
    # Assign trades should be treated as Exercise trades
    if 'Assign' == status:
        status = 'Exercise'
    
    return status
