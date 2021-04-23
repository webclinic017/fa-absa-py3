

"""----------------------------------------------------------------------------

MODULE

    FOrderFlowSimulator: Calls FOrderFlowSimulator
    
    (C) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module calls the order flow simulator if all selected order books
    passed the safe-markets security check.

NOTES:
    
    -This module can only be used in PRIME versions from 4.0 
     
    
------------------------------------------------------------------------------"""

    
import acm
from FOrderFlowSimulatorSafeMarkets import *

    
def go(mei):
   
    tm = mei.ExtensionObject()
    sheet = tm.ActiveSheet()
    selection = sheet.Selection()
    cell = selection.SelectedCell()
    rowObject = cell.RowObject()
    col = cell.Column()
    tag = cell.Tag()
    context = col.Context()
    execOrder = rowObject
    scriptData = selection.SelectedOrderBooks()



    # ######################################## #
    #               MARKET CHECK               #
    # ######################################## #
    
    safe = True
    for ob in scriptData:
        marketPlace = ob.MarketPlace()
        unsafeOB = True
        for m in SAFE_MARKETS:
            if( marketPlace.Location().upper() == m[0].upper() and marketPlace.DataSource() == m[1] ):    
                unsafeOB = False
                break
        if( unsafeOB ):
            safe = False
            break
     
    if( safe ):
    # ######################################## #
    #          MARKET CHECK PASSED             #
    # ######################################## #
        acm.RunModuleWithParametersAndData( 'FOrderFlowSimulator', acm.GetDefaultContext(), scriptData)
        # Launch will then proceed in FOrderFlowSimulator.ael_main_ex


    else:
    # ######################################## #
    #          MARKET CHECK FAILED             #
    # ######################################## #
    
        print ('Error: unauthorized test market.')
        print ('The market with location', marketPlace.Location(), 'and port', marketPlace.DataSource(), ' has not been approved as a safe test market.')
        print ('For security reasons, the order flow simulator will not start.')


