
import sys
import traceback

import acm
import ael

import FBDPGui

# Tool Tip
tttrades = "The list of trades that should be rollback"


ael_gui_parameters = {'windowCaption': 'Manual Rollback', 'hideExtraControls': True}

def onManualRollback(invokationInfo):
    global ael_variables
    try:
        selection = invokationInfo.ExtensionObject().ActiveSheet().Selection()
        cells = selection.SelectedCells()
        trades = []
        for cell in cells:
            tag = cell.Tag()
            column = cell.Column()
            columnId = str(column.ColumnId())
            if columnId == 'Trade Action':
                rowObject = cell.RowObject()
                trade = rowObject.Trade()
                action = cell.Evaluator().Value()
                trades.append(trade.Oid())
        tradeIds = ''
        for i in range(len(trades)):
            tradeIds = tradeIds + str(trades[i])
            if i <= len(trades) - 2:
                tradeIds = tradeIds + ', '
        ael_variables =  [('trades', 'Trades', 'FTrade', None, tradeIds, 2, 1, tttrades)]
        ScriptName = "Manual RollBack of Trades"

        acm.RunModuleWithParameters('FXO_ManualRollback', 'Standard')
    except:
        traceback.print_exc()

def ael_main(dict, *rest):
    trades = dict['trades']
    vt = []
    for t in trades:
        
        et = acm.FTrade.Select('contractTrdnbr = %s and status <> "Void" and oid > 0 name <> %i  ' %(t.Oid(), t.Oid()))
        if et:
            print 'List of Trades ', et
            acm.BeginTransaction()
            try:
                for trd in et:
                    trd.Status('Void')
                    trd.Text1('Rollback Exercise')
                    trd.Commit()
                    print trd.Oid(), trd.Status()
                    vt.append(trd.Oid())
                acm.CommitTransaction()
                print 50*'='
                print '\n\n Manual Rollback of trade number: ', t.Oid(), 'on Instrument: ', t.Instrument().Name(), '\n'
                for tn in vt:
                    print 'Trade Number: ', tn, ' has been voided \n'
                print 50*'='
            except:
                acm.AbortTransaction()
                print 'Transaction Aborted'
    acm.PollAllEvents()
                
              
