
import acm

def isEvaluator(obj):
    return hasattr(obj, "IsEvaluator") and obj.IsEvaluator()

def nodeCount(eval):
    """Get number of nodes in an evaluator tree"""
    if not isEvaluator(eval):
        return 0
    return eval.ReferencedNodes().Size()
    
def uniqueNodeCount(eval):
    """Get number of unique nodes in an evaluator tree"""
    if not isEvaluator(eval):
        return 0
    return eval.ReferencedUniqueNodes().Size()

def doDependentCount(eval, log):
    """Get number of evaluators dependant of an evaluator, ie parents"""
    if not isEvaluator(eval):
        return 0
        
    dependents = eval.Dependents()
    count = 0
    if log:
        skippedMsgs = []
        print ('***************************')
        print ('Input: ' + str(eval))
    for dep in dependents:
        if hasattr(dep, "IsKindOf"):
            # exclude dependencies for the profiling columns
            if str(dep)[:13] == 'valuationView':
                if log:
                    skippedMsgs.append('*** SKIPPED profiling dependent: ' + str(dep))
                continue
            if dep.IsEvaluator():
                if log:
                    print ('    Dependent: ' + str(dep))
                    print ('        Class: ' + str(dep.ClassName()))
                count += 1
            elif dep.IsKindOf(acm.FDependentArray) and len(dep) > 0 and dep[0].IsEvaluator():
                if log:
                    print ('    Dependent: ' + str(dep))
                    print ('        Class: ' + str(dep.ClassName()))
                count += 1
            else:
                if log:
                    skippedMsgs.append('*** SKIPPED: ' + str(dep) + ', Class: ' + str(dep.ClassName()))
        else:
            if log:
                skippedMsgs.append('*** SKIPPED (obj has no IsKindOf func): ' + str(dep))
    if log:
        for logStr in skippedMsgs:
            print (logStr)
        print ('***************************')
    return count

def dependentCount(eval):
    if not isEvaluator(eval):
        return 0
    return doDependentCount(eval, False)
    
def getProfilingData(ev):
    if hasattr(ev, "IsKindOf") and ev.IsKindOf(acm.FEvaluator):
        f = acm.GetFunction("GetGridCellProfilingData", 1)
        if f is not None:
            return f(ev)
    return None

def avg(ev):
    """Get average profiling time for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.Tavg()
    return ""

def acc(ev):
    """Get accumulated profiling time for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.Tacc()
    return ""

def max(ev):
    """Get max profiling time for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.Tmax()
    return ""

def min(ev):
    """Get min profiling time for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.Tmin()
    return ""

def cost(ev):
    """Get propagated cost profiling time for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.PropagatedCost()
    return ""

def count(ev):
    """Get profiling call count for an evaluator"""
    profData = getProfilingData(ev)
    if profData is not None:
        return profData.Count()
    return ""

def dcount(ev):
    """Get profiling total call count for evaluator descendants"""
    profData = getProfilingData(ev)
    if profData is not None:
        a = profData.Descendants().AsArray()
        if len(a) > 0:
            return profData.DescendantCount(a[0])
    return ""

def isGridCellProfilingEnabled():
    f = acm.GetFunction("IsGridCellProfilingEnabled", 0)
    if f is not None:
        return f()
    else:
        print ("GetFunction('IsGridCellProfilingEnabled', 0) returned None")
        return False;

def logDependants(eii):
    vv = eii.ExtensionObject() # A CValuationViewerAppFrame
    rowNodes = vv.GetSelected()
    if rowNodes != None:
        for rowNode in rowNodes:
            item = rowNode.Evaluator()
            if item != None:
                doDependentCount(item, True)
    
def excludeColumn(eii, doExclude):
    if not isGridCellProfilingEnabled():
        print ("Can not include/exclude column(s) as grid cell profiling is disabled")
        return
        
    trdmgr = eii.ExtensionObject() # A FUiTrdMgrFrame
    gridselection = trdmgr.ActiveSheet().Selection()
    cells = gridselection.SelectedCells()
    done = Set() # grid cells may also be selected with col header cell
    for cell in cells:
        col = cell.Column()
        if not col in done:
            col.ExcludeFromProfiling(doExclude)
            done.add(col)
    
def excludeColumnFromProfiling(eii):
    excludeColumn(eii, True)
    
def includeColumnInProfiling(eii):
    excludeColumn(eii, False)

def enableGridCellProfiling(eii):
    if isGridCellProfilingEnabled():
        print ("Grid cell profiling is already enabled")
        return;
    
    f = acm.GetFunction("EnableGridCellProfiling", 1)
    if f is not None:
        f(-1)
        print ("Grid cell profiling is now enabled")
    else:
        print ("GetFunction('EnableGridCellProfiling', 1) returned None")

def disableGridCellProfiling(eii):
    if not isGridCellProfilingEnabled():
        print ("Grid cell profiling is already disabled")
        return;
        
    f = acm.GetFunction("DisableGridCellProfiling", 0)
    if f is not None:
        f()
        print ("Grid cell profiling is now disabled")
    else:
        print ("GetFunction('DisableGridCellProfiling', 0) returned None")

def clearGridCellProfiling(eii):
    if not isGridCellProfilingEnabled():
        print ("Grid cell profiling is disabled")
        return;
        
    f = acm.GetFunction("EnableGridCellProfiling", 1)
    if f is not None:
        f(-1)
        print ("Grid cell profiling is now cleared")
    else:
        print ("GetFunction('EnableGridCellProfiling', 1) returned None")
