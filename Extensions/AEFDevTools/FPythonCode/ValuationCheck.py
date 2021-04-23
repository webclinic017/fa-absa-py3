from __future__ import print_function
import acm
import TreeADFLViewer
reload(TreeADFLViewer)

isLot = acm.GetFunction("isLot", 1)

exclusionEntities = set([
])

def isEval(obj):
    try:
        if isLot( obj ):
            res = False
        else:
            res = obj.IsEvaluator()
    except:
        res = False
    return res
    
def FindDuplicates_Impl( parentEntity, idx, eval, visited, evalsByKey ):
    if eval is None:
        return

    if eval in visited:
        return
    visited.add( eval )

    if not isEval( eval ):
        return
    if eval.IsClone():
        return
    entity = eval.Entity()
    try:
        if not entity or str(entity) == "":
            entity = acm.FSymbol(str(parentEntity) + "_" + str(idx))
        if entity and str(entity) != "":
            val = eval.Value()
            cls = eval.Class()
            extClass = eval.ExtendedClass()
            receiver = None
            if eval.IsKindOf( acm.FMethodEvaluator ):
                receiver = eval.Receiver()
            proprietor = eval.Proprietor() and eval.Proprietor().Value()
            key = tuple([entity, val, cls, extClass, receiver, proprietor])
            if not evalsByKey.has_key( key ):
                evalsByKey[ key ] = []
            evalsByKey[key].append( eval )
    except:
        pass
    
    for idx, input in enumerate(eval.AllInputs()):
        FindDuplicates_Impl( entity, idx, input, visited, evalsByKey )

def InputsDiffer( inputsByEval, idx ):
    input = None
    for eval in inputsByEval.keys():
        eInput = inputsByEval[ eval ][idx]
        if input is None:
            input = eInput
        else:
            if input != eInput:
                return True
    return False
    
def CheckInputs( badEvalKey, badEval, badEvals, badEvalsByKey, inputs, parentChildRelations, badEvalsThatAreChildren ):
    evals = badEvalsByKey[ badEvalKey ]
    inputsByEval = {}
    for eval in evals:
        inputsByEval[ eval ] = eval.AllInputs()
    
    for idx, input in enumerate(inputs):
        if isEval( input ):
            if input in badEvals and InputsDiffer( inputsByEval, idx ):
                badEvalsThatAreChildren.add(input)
                if not parentChildRelations.has_key( badEval ):
                    parentChildRelations[ badEval ] = []
                parentChildRelations[ badEval ].append( input )

    
def FindDuplicates( eval ):
    visited = set()
    evalsByKey = {}
    FindDuplicates_Impl( "", 0, eval, visited, evalsByKey )
    badEvals = set()
    badEvalsByKey = {}
    for key in evalsByKey.keys():
        evals = evalsByKey[ key ]
        if len(evals) > 1:
            badEvalsByKey[ key ] = evals
            for e in evals:
                if not e.Entity() in exclusionEntities:
                    badEvals.add( e )
    
    parentChildRelations = {}
    badEvalsThatAreChildren = set()
    for key in badEvalsByKey.keys():
        evals = badEvalsByKey[key]
        for be in evals:
            inputs = be.AllInputs()
            CheckInputs( key, be, badEvals, badEvalsByKey, inputs, parentChildRelations, badEvalsThatAreChildren )

    parents = parentChildRelations.keys()
    roots = []
    for eval in badEvals:
        if not eval in badEvalsThatAreChildren:
            roots.append( eval )

    return badEvals, parents, roots, parentChildRelations

def CheckEvals(eii):
    cells = eii.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    for cell in cells:
        duplicates, parents, roots, parentChildRelations = FindDuplicates( cell.CalculatedValue().GetEvaluator() )
        print (cell.RowObject().StringKey(), len(duplicates))

def BuildPath( eval, parentChildRelations, paths ):
    if parentChildRelations.has_key( eval ):
        children = parentChildRelations[eval]
        paths[eval] = {}
        for child in children:
            BuildPath( child, parentChildRelations, paths[eval] )
    else:
        paths[eval] = None
    
def CheckEvalInDialog(eii):
    cells = eii.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    for cell in cells:
        try:
            duplicates, parents, roots, parentChildRelations = FindDuplicates( cell.CalculatedValue().GetEvaluator() )
            paths = {}
            for root in roots:
                BuildPath(root, parentChildRelations, paths)
            
            TreeADFLViewer.StartDialog( eii, paths, cell.RowObject().StringKey() )
            break
        except:
            pass
