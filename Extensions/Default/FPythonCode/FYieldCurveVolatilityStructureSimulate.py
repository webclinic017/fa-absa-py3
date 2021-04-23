import acm, ael, time
global threadName
threadName = 'ycRecalcThread'

import FLogger
logger = FLogger.FLogger("FYieldCurveVolatilityStructureSimulate")

import logging
log_formatter = logging.Formatter( '%(asctime)s %(message)s', '%y%m%d %H%M%S' )
for hndlr in logger.Handlers():
    hndlr.setFormatter(log_formatter)

#----------------------------------------------------------------------
#-----------------  Observer  -----------------------------------------
#----------------------------------------------------------------------

class Observer:
    def __init__(self):
        self.insert = []
    def ServerUpdate(self, all, action, entity):
        if str(action) == 'insert':
            self.insert.append(all)

global observer
observer = None

#----------------------------------------------------------------------
#-----------------Yield Curve------------------------------------------
#----------------------------------------------------------------------

def simulateCurves(curves):
    for curve in curves:
        curveClone = curve.Clone()
        acm.SynchronizedMessageSend(curveClone, 'Calculate', [])
        acm.SynchronizedMessageSend(curve, 'Apply', [curveClone])
        logger.LOG( 'Calc + Sim YC  %s' % curve.Name() )
        
def commitCurves(curves):
    for curve in curves:
        curveClone = curve.Clone()
        acm.SynchronizedMessageSend(curveClone, 'Calculate', [])
        acm.SynchronizedMessageSend(curve, 'Apply', [curveClone])
        acm.SynchronizedMessageSend(curve, 'Commit', [])
        logger.LOG( 'Commited Calc + Sim YC %s' % curve.Name() )
        
def getCurvesRecursively(yieldCurve, curves, done):
    if yieldCurve.Name() not in done:
        done.append(yieldCurve.Name())
        curves.append(yieldCurve)

def getAllMappedCurves( rows, curves, done = [] ):
    tag = acm.GetGlobalEBTag()
    context = acm.GetDefaultContext()
    curvesTmp = []
    for row in rows:
        try:
            curvesTmp = acm.GetCalculatedValueFromString( row, context, 'benchmarkCurvesInRiskBaseValue', tag)
            try:
                for curve in curvesTmp.Value():
                    getCurvesRecursively(curve, curves, done)
            except:
                getCurvesRecursively(curvesTmp.Value(), curves, done)
        except:
            logger.ELOG( 'No YC for row %s' % row )
            pass

def simulateAllMappedCurves(rows):
    curves = []
    done   = []
    getAllMappedCurves( rows, curves, done )
    simulateCurves( curves )

def commitAllMappedCurves(rows):
    curves = []
    done   = []
    getAllMappedCurves( rows, curves, done )
    commitCurves( curves )
    
def recalcAndSimulate( invokationInfo ):
    rows = getInstrumentsAndTradesForCell( invokationInfo )
    simulateAllMappedCurves( rows )

def recalcAndSimulateAll( invokationInfo ):
    rows = getInstrumentsAndTradesForSheet( invokationInfo )
    if rows.Size() > 0:
        thread = acm.FThread()
        thread.Run( simulateAllMappedCurves, [ rows ] )
        thread.Cancel()
        thread.TestCancel()

def recalcAndCommitAll( invokationInfo ):
    rows = getInstrumentsAndTradesForSheet( invokationInfo )
    if rows.Size() > 0:       
        doCalc = 1
        func = acm.GetFunction( 'msgBox', 3 )
        doCalc = func( "Warning", "This will recalculate and commit all yield curves mapped to instruments in your positions. Continue?", 1 )
        if 1 == doCalc:
            commitAllMappedCurves( rows )

def unsimulateCurves( curves ):
    for curve in curves:
        acm.SynchronizedMessageSend( curve, 'Undo', [])
        logger.LOG( 'Unsimulate YC  %s' % curve.Name() )
        
def unsimulateAllMappedCurves( rows ):
    curves = []
    done   = []
    getAllMappedCurves( rows, curves, done )
    unsimulateCurves( curves )

def unSimulate( invokationInfo ):
    rows = getInstrumentsAndTradesForCell( invokationInfo )
    if rows.Size() > 0:
        unsimulateAllMappedCurves( rows )
    
def unSimulateAll( invokationInfo ):
    rows = getInstrumentsAndTradesForSheet( invokationInfo )
    if rows.Size() > 0: 
        unsimulateAllMappedCurves( rows )
        
def performLoop( rows, updateInterval, observer, thread ):
    curves = []
    done   = []
    getAllMappedCurves( rows, curves, done )
    while 1==1:
        thread.TestCancel()
        if len(observer.insert):
            getAllMappedCurves( observer.insert, curves, done )
            observer.insert = []
        simulateCurves( curves )
        time.sleep( updateInterval )

def intervalSimulateAllCurves( rows, threadName ):
    global observer
    if not observer:
        observer = Observer()
    for row in rows:
        row.RemoveDependent( observer )
        row.AddDependent( observer )
    context = acm.GetDefaultContext()
    updateInterval = context.GetDefaultValueEx( "ycUpdateInterval", context )
    threads = acm.FThread.Select('.Name = "%s"' % threadName )
    doCalc = 1
    if len( threads ):
        func = acm.GetFunction('msgBox', 3)
        doCalc = func("Warning", "A previously started yield curve recalculation will be stopped. Continue?", 1)
    if doCalc:
        for thread in threads:
            thread.Cancel()
        logger.LOG( 'YC recaluclation every %s second started' % updateInterval )
        thread = acm.FThread()
        thread.Name( threadName )
        thread.Run( performLoop, [ rows, updateInterval, observer, thread ] )

def intervalSimulateYieldCurves(invokationInfo):
    rows = getInstrumentsAndTradesForCell(invokationInfo)
    if rows.Size() > 0:
        intervalSimulateAllCurves( rows, rows[0].StringKey() )
    else:
        logger.ELOG( 'No Objects with instruments found' )
    
def intervalSimulateAllYieldCurves( invokationInfo ):
    global threadName
    rows = getInstrumentsAndTradesForSheet( invokationInfo )
    if rows.Size() > 0:
        intervalSimulateAllCurves( rows, threadName )                
    else:
        logger.ELOG( 'No row objects with instruments found' )

def stopThread( name ):
    threads = acm.FThread.Select( '.Name = "%s"' % name )
    for thread in threads:
        thread.Cancel()
    logger.LOG( 'YC recalculation stopped' )
    
def stopUpdate( invokationInfo ):
    global observer
    rows = getInstrumentsAndTradesForCell( invokationInfo )
    if rows.Size() == 1:
        if observer:
            rows[0].RemoveDependent( observer )
        stopThread( rows[0].StringKey() )

def stopUpdateAll( invokationInfo ):
    global threadName
    global observer
    if observer:
        rows = getInstrumentsAndTradesForSheet( invokationInfo )
        for row in rows:
            row.RemoveDependent( observer )
    stopThread( threadName )

def setUpdateInterval( row, col, calcval, value, operation ):
    context = acm.GetDefaultContext()
    oldValue = context.GetDefaultValueEx("ycUpdateInterval", context)
    if str(operation)=='insert' and str(oldValue)!=value:
        s = "FObject:ycUpdateInterval\n%s" % (value)
        context.EditImport('FExtensionValue', s)
        m = context.EditModule()
        if m.CanBeModified():
            m.Commit()

def getInstrumentsAndTradesForSheet(invokationInfo):
    allRows = acm.FArray()
    activeSheet = invokationInfo.ExtensionObject().ActiveSheet()
    if activeSheet.SheetClass().IncludesBehavior('FPortfolioSheet') or activeSheet.SheetClass().IncludesBehavior('FVerticalPortfolioSheet'):
        allRows = activeSheet.GetAllOfType('FPortfolioInstrumentAndTrades')
    elif activeSheet.SheetClass().IncludesBehavior('FTimeSheet'):
        allTBO = activeSheet.GetAllOfType('FTimeBucketAndObject');
        for tbo in allTBO:
            # Get the top row
            if not tbo.TimeBucket():
                row = tbo.Object()
                allRows.Add(row)
            
    else:
        logger.ELOG( 'Calc+Sim can only be run for a Portfolio sheet, Vertical Portfolio sheet or a Time Sheet' )
    return allRows

def getInstrumentsAndTradesForCell(invokationInfo):
    cell = invokationInfo.Parameter("ClickedButton") 
    if not cell:
        cell = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCell()
    row = cell.RowObject()
    allRows = acm.FArray()
    if row.Class().IncludesBehavior('FMultiInstrumentAndTrades'):
        allRows.Add( row )
    elif row.Class().IncludesBehavior('FTimeBucketAndObject'):
        instrumentAndTradesRow = row.Object()
        allRows.Add(instrumentAndTradesRow)
    else:
        logger.ELOG( 'Calc+Sim can only be run for aggregate rows' )
    return allRows


#----------------------------------------------------------------------
#-----------------Volatility Structure---------------------------------
#----------------------------------------------------------------------

def simulateVols(allVols):
    for vol in allVols:
        volClone = vol.Clone()
        if ( 'SABR' == volClone.StructureType() ):
            acm.SynchronizedMessageSend(volClone, 'UpdateUnderlyingForwards', [])
            acm.SynchronizedMessageSend(volClone, 'CalcSabrAtmVol', [])
            acm.SynchronizedMessageSend(volClone, 'CalcImpliedVolatilities', [])
        if ( 'SVI' == volClone.StructureType() ):
            acm.SynchronizedMessageSend(volClone, 'UpdateUnderlyingForwards', [])
            acm.SynchronizedMessageSend(volClone, 'CalcImpliedVolatilities', [])
        acm.SynchronizedMessageSend(volClone, 'Calibrate', [])
        acm.SynchronizedMessageSend(vol, 'Apply', [volClone])
        acm.SynchronizedMessageSend(vol, 'Simulate', [])
        logger.LOG( 'Calc + Sim Vol %s' % vol.Name() )
      
def getVolsRecursively(vol, allVols):
    undVol = vol.UnderlyingStructure()
    if undVol:
        getVolsRecursively(undVol, allVols)
    else:
        allVols.append(vol)

def recalcAndSimulateVols(invokationInfo):
    allVols = getVolsForCell(invokationInfo)
    simulateVols(allVols)

def unSimulateVols(invokationInfo):
    allVols = getVolsForCell(invokationInfo)
    for vol in allVols:
        acm.SynchronizedMessageSend(vol, 'Undo', []) 
        logger.LOG( 'Unsimulate Vol %s' % vol.Name() )

def getVolsForCell(invokationInfo):
    cell = invokationInfo.Parameter("ClickedButton") 
    if not cell:
        cell = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCell()
    row = cell.RowObject()    
    allVols = []
    if row.Class().IncludesBehavior('FMultiInstrumentAndTrades'):
        tag = cell.Tag()
        context = cell.Column().Context()
        try:
            vols = acm.GetCalculatedValueFromString(row, context, 'volatilityStructuresInTheoreticalValue', tag)
            try:
                for vol in vols.Value():
                    getVolsRecursively(vol, allVols)
            except:
                getVolsRecursively(vols.Value(), allVols)
        except:
            pass
    else:
        logger.ELOG( 'Calc+Sim Vol can only be run for aggregate rows' )
    return unique(allVols)

#----------------------------------------------------------------------
#-----------------Common-----------------------------------------------
#----------------------------------------------------------------------


def recalcAndSimulateYieldVols(invokationInfo):
    # Calc + Sim, Yield Curves
    recalcAndSimulate(invokationInfo)
    # Calc + Sim, Volatility Structures
    recalcAndSimulateVols(invokationInfo)

def unSimulateYieldVols(invokationInfo):
    # Unsimulate, Yield Curves
    unSimulate(invokationInfo)
    # Unsimulate, Volatility Structures
    unSimulateVols(invokationInfo)
    
def createClick(invokationInfo):
    cell = invokationInfo.Parameter("Cell") 
    res = False
    if cell!=None and hasattr(cell, "RowObject"):
        row = cell.RowObject()
        if row!=None:
            if row.Class().IncludesBehavior('FMultiInstrumentAndTrades'):
                res = True
    return res
    
def unique(seq):
    # Get a list of unique items
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()
