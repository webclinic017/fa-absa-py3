

from __future__ import print_function
import string

from FUDMCCommon_CPP import MCError, MCVariable, McAstNode, SafeASTTraversal
from FUDMCCommon_CPP import is_valid_type

import acm

funccall_name = lambda n : n[0].attr
funccall_params = lambda n : n[1]
variable_name = lambda n: n[0].attr
assignment_variable = lambda n:n[0]

binopdict = {'*':'mul', '-':'sub', '+':'add', '/':'div', '>':'gt', '<':'lt',
             '.*':'elmul', './':'eldiv', '==':'eq', '>=':'gteq', '<=':'lteq', '!=':'neq'}

unopdict = {'-':'neg', '+':'pos'}

reswordlist = ['STDEV', 'RELSTDEV', 'result']

# This is the conversion map between the types exposed in the PEL-language and the
# corresponding C-types used internally.
fobj_typemap = {'FRealArray':'matrix(double)', 'UDMCDoubleMatrix':'matrix(double)'}

def check_for_operator_conversion_error(funcname, lh_type, rh_type, node):
    mclib = acm.FUDMCLibrary()
    params = (rh_type != None) and [lh_type, rh_type] or [lh_type]
    if not mclib.FunctionExists(funcname, convert_parameter_types(params)):
        if rh_type and (lh_type != rh_type):
            raise MCError(str("Possible type conversion error (automatic conversion not supported): %s to %s"%(lh_type, rh_type)), \
                          node=node)

def translateFObjtype(typename):
    return fobj_typemap.get(typename, typename)

def convert_parameter_types(typenames):
    """ In the CPP-layer we use the notation doublemat instead of matrix(double)"""
    convert = (lambda x : ((x == "matrix(double)") and "doublemat") or x)
    return [convert(name) for name in typenames]

def check_type(typename):
    """Raise an error if typename is not valid"""
    if not is_valid_type(typename):
        raise MCError(str("Unknown type " + typename))
    
def get_binop_name(binop):
    """Get function name for a binary operator, specialized by type."""
    if not binop in binopdict:
        raise MCError(str("Unknown binop %s." % binop))
    return binopdict[binop]

def get_unop_name(unop):
    """Get function name for a unary operator."""
    if not unop in unopdict:
        raise MCError(str("Unknown unary operator %s." % unop))
    return unopdict[unop]

def assert_nodetype(node, types, msg):
    if not node.valuetype in types:
        raise MCError(msg, node=node)
    
class UDMCSemanticAnalyzer:
    """A user defined payoff expression, including vars and params"""
    def __init__(self, tree):        
        """Create an instance given text definition"""
        self.variables = {}
        try:
            JoinVariablesPass(tree)
            InitialTypeInfoPass(tree, self)
            PropagateTypes(tree, self)  # Resolve function parameter's variable types.
            AssignmentsPass(tree)
            FunctionCallsPass(tree)     # Create specific function nodes.
            TransformIndexExpressionPass(tree)
            LastCleanupPass(tree)
        except MCError as err:
            print ("/Error when doing semantic analysis: ", str(err))
            #tree.show()
            raise        
    def add_variable(self, varname, vartype, isparam, isprocess, 
                     initinfo, impid):
        """Add a variable"""
        if varname in self.variables:
            raise MCError(str("Variable %s already exists"%varname))            
        """Raise an error if varname is a reserved word"""
        if varname in reswordlist:
            raise MCError(str("Variable %s is a reserved word"%varname))            
        self.variables[varname] = MCVariable(varname, vartype, isparam,  \
                                             isprocess, initinfo, impid)
    def get_var(self, node):
        """Retrieve variable object corresponding to a variable node"""
        varname = variable_name(node)
        if not varname in self.variables:
            raise MCError(str("Variable %s not found"%varname), node=node)
        return self.variables[varname]

class ASTUtilsMixIn:
    def propagate_return_type(self, node, func_short_name):
        
        # The functions parameter nodes.
        realparams = funccall_params(node)
        
        child_types = [paramnode.valuetype for paramnode in realparams]        
       
        # Get return type matching the given set of parameters.
        mclib = acm.FUDMCLibrary()
        
        parameter_types = convert_parameter_types(child_types)
        
        if mclib.FunctionExists(func_short_name, parameter_types):
            udmc_return_type = translateFObjtype(mclib.GetFunctionReturnCType(func_short_name, parameter_types))
            node.valuetype = udmc_return_type
        else:
            params_str = string.join([type_name for type_name in child_types], sep=', ')
            raise MCError(str("No overloaded function matches call to '%s' with parameters %s."%(func_short_name, params_str)),\
                          node=node)

    def make_func(self, node, func_short_name):
        """ Validate parameters and look up proper MC Function. """
        mclib = acm.FUDMCLibrary()

        # The parameter nodes
        actual_params = funccall_params(node)       

        # The parameter types that are actually passed to the function.
        actual_param_types = [paramnode.valuetype for paramnode in actual_params]
        converted_param_types = convert_parameter_types(actual_param_types)
        
        if mclib.FunctionExists(func_short_name, converted_param_types):
            udmc_return_type = translateFObjtype(mclib.GetFunctionReturnCType(func_short_name, converted_param_types))
            node.valuetype = udmc_return_type
            node.attr = mclib.GetFunctionFromParameterTypes(func_short_name, converted_param_types)
        else:
            params_str = string.join([type_name for type_name in actual_param_types])
            raise MCError(str("No overloaded function matches call to '%s' with parameters %s."%(func_short_name, params_str)), \
                         node=node)
                              
    def convert_to_func(self, node, funcname, arglist):
        """Convert a node to a function call , changing type & replacing children"""
        opsymnode = McAstNode('sym', funcname)
        arglistnode = McAstNode('statementlist')
        arglistnode[:] = arglist        
        node[:] = [opsymnode, arglistnode]
        node.typename = "funccall"
        self.make_func(node, funcname)
        
class JoinVariablesPass(SafeASTTraversal):            
    """Give multiple instances of same variable identical impids"""
    def __init__(self, ast):
        self.varimpids = {}   # varname -> impid
        SafeASTTraversal.__init__(self, ast)
        self.postorder()        
    def n_variable(self, node):        
        """Make sure that all variable nodes have the same impid"""
        node.impid = self.varimpids.get(node[0].attr, node.impid)
        self.varimpids[node[0].attr] = node.impid

class InitialTypeInfoPass(SafeASTTraversal):
    """Visitor that resolves functions and variables, adds type info"""
    type_map = { 'int': "int", 'double' : "double" }
    def __init__(self, ast, mcexpr):
        SafeASTTraversal.__init__(self, ast)
        self.varimpids = {}
        self.mcexpr = mcexpr
        self.postorder()        
    def handle_declaration(self, node, isparam, isprocess):
        vartypename = node.first_child_oftype('typedeclaration')[0].attr
        check_type(vartypename)
        varnode = node.first_descendant_oftype('variable')
        varinit = None
        if node.first_descendant_oftype('assignment'):
            varinit = node.first_descendant_oftype('assignment')[1]
        self.mcexpr.add_variable(varnode[0].attr, vartypename, isparam, \
                                 isprocess, varinit, varnode.impid)
    def n_paramdeclaration(self, node):
        self.handle_declaration(node, isparam=True, isprocess=False)
    def n_vardeclaration(self, node):
        self.handle_declaration(node, isparam=False, isprocess=False)
    def n_processdeclaration(self, node):
        self.handle_declaration(node, isparam=False, isprocess=True)        
    def n_typedeclaration(self, node):
        node.valuetype = node[0].attr
        check_type(node.valuetype)
    def default(self, node):
        node.valuetype = InitialTypeInfoPass.type_map.get(node.typename, None)

class FunctionCallsPass(SafeASTTraversal, ASTUtilsMixIn):
    """Visitor that resolves specialized function names (must be done after variable names are resolved)."""
    def __init__(self, ast):
        SafeASTTraversal.__init__(self, ast)
        self.postorder()
    def n_funccall(self, node):
        """Resolve types for a function call node"""        
        self.make_func(node, funccall_name(node))

class AssignmentsPass(SafeASTTraversal):
    def __init__(self, ast):
        SafeASTTraversal.__init__(self, ast)
        self.postorder()
    def n_assignment(self, node):
        if node[0].valuetype != node[1].valuetype:
            raise MCError(str("Assignment type mismatch. Expected %s got %s"%(node[0].valuetype, node[1].valuetype)), \
                          node=node)
        node.valuetype = node[0].valuetype        
        node[0].lvalue = True
    def n_forloop(self, node):
        """This assertion must be preceeded by n_assignment above."""
        assign, endval, block = node
        assert_nodetype(assign, ['int'], 'Loop variable must be an integer')
        assert_nodetype(endval, ['int'], 'End condition for foor loop must be an integer')

class PropagateTypes(SafeASTTraversal, ASTUtilsMixIn):
    """Visitor, propagates typeinfo upwards in tree and transforms binops"""
    def __init__(self, ast, mcexpr):        
        SafeASTTraversal.__init__(self, ast)
        self.mcexpr = mcexpr
        self.postorder()
    def n_sliceexpr(self, node):
        vec, (start, end) = node
        assert_nodetype(vec, ['matrix(double)'], "Can only take index of double matrices")
        node.valuetype = 'matrix(double)'
    def n_slice(self, node):
        for child in node:
            assert_nodetype(child, ['int', ], "Only integer types may be used in a slice expression.")
        node.valuetype = 'slice'
    def n_emptyslice(self, node):
        node.valuetype = 'emptyslice'
    def n_funccall(self, node):
        self.propagate_return_type(node, funccall_name(node))
    def n_indexexpr(self, node):
        mat, index = node
        assert_nodetype(mat, ['matrix(double)'], "Can only take index of double matrices.")
        assert_nodetype(index, ['int'], "Index into matrix must be an integer.")
        node.valuetype = 'double'
    def n_matindexexpr(self, node):
        mat, rowindex, colindex = node
        assert_nodetype(mat, ['matrix(double)'], "Can only take index of matrix")
        assert_nodetype(rowindex, ['int', 'slice', 'emptyslice'], "Row index into matrix must be an integer or a slice.")
        assert_nodetype(colindex, ['int', 'slice', 'emptyslice'], "Column index into matrix must be an integer or a slice.")
        if rowindex.valuetype == 'int' and colindex.valuetype == 'int': 
            node.valuetype = 'double'
        else:
            node.valuetype = 'matrix(double)'

    #drtodo , we're starting to use a few too many 'temporary' value types
    def n_variable(self, node):
        node.valuetype = self.mcexpr.get_var(node).vartype
    def n_operator(self, node): 
        params = []
        if len(node) == 3:
            lhs, opsym, rhs = node[0], node[1], node[2]
            opfunname = get_binop_name(opsym.attr)
            params = [lhs, rhs]
            check_for_operator_conversion_error(opfunname, lhs.valuetype, rhs.valuetype, node)
        elif len(node) == 2:
            opsym, rhs = node[0], node[1]
            opfunname = get_unop_name(opsym.attr)
            params = [rhs]
        else:
            raise MCError(str("Bad number of operator parameters: %i"%len(node)))
        self.convert_to_func(node, opfunname, params)
    def n_logicoperator(self, node):
        for child in node:
            assert_nodetype(child, ['int'], 'Can only use logic operators (and, or, not) with integer expressions.')
        node.valuetype = 'int'
    def n_andstatement(self, node):
        self.n_logicoperator(node)
    def n_orstatement(self, node):
        self.n_logicoperator(node)
    def n_notstatement(self, node):
        self.n_logicoperator(node)
    def n_ifstatement(self, node):
        assert_nodetype( node[0], ['int'], 'Test clause in if statement must evaluate to integer');

# DRTODO type check of slice as in m[1:2.3, 3]

def makeintnode(i):
    intnode = McAstNode('int', i)
    intnode.valuetype = 'int'
    return intnode

def getsliceindex(node):
    # In case of a single integer start is set equal to end.
    if node.valuetype == 'int':
        return node, node
    if node.valuetype == 'slice':
        return node[0], node[1]
    if node.valuetype =='emptyslice':
        return makeintnode(0), makeintnode(-1)
    raise Exception("internal error, unhandled type in getsliceindex")
                    
class TransformIndexExpressionPass(SafeASTTraversal, ASTUtilsMixIn):
    """Transformed matrix/vector slice syntax for lvalues and rvalues to function call"""
    def __init__(self, ast):
        SafeASTTraversal.__init__(self, ast)
        self.postorder()       
    def n_sliceexpr(self, node):
        if node.lvalue:
            return # lvalue case is handled by parent assign node drtodo possibly handle this by having an earlier pass
        vec, (start, end) = node
        self.convert_to_func(node, "extract", [vec, start, end] )
    def n_matindexexpr(self, node):
        if node.lvalue:
            return # lvalue case is handled by parent assign node drtodo posibly handle this by having an earlier pass        
        mat, rowindex, colindex = node       
        rowitype, colitype = rowindex.valuetype, colindex.valuetype
        if rowitype =='int' and colitype == 'int':
            return # simple indexing handled directly by VM
        elif rowitype == 'int' or colitype == 'int':
            if rowitype == 'int':
                colstart, colstop = getsliceindex(colindex)
                self.convert_to_func(node, "extractmrightslice", [mat, rowindex, colstart, colstop])
            else:
                rowstart, rowstop = getsliceindex(rowindex)
                self.convert_to_func(node, "extractmleftslice", [mat, rowstart, rowstop, colindex])
        else:
            rowstart, rowstop = getsliceindex(rowindex)
            colstart, colstop = getsliceindex(colindex)
            self.convert_to_func(node, "extractm", [mat, rowstart, rowstop, colstart, colstop])
    def n_assignment(self, node):
        pass

class LastCleanupPass(SafeASTTraversal):
    """Make some last cleanup transformations"""
    def __init__(self, ast):
        SafeASTTraversal.__init__(self, ast)
        self.postorder()       
    def n_funccall(self, node):
        """Remove statement list and symbol node, place params as children"""
        unused_symnode, stmnlist = node[0], node[1]
        node[:] = stmnlist[:]
        
def analyze(ast_tree):
    """Analyze an astTree (parser output), resolve functions and types

     Arguments:
       ast_tree   -- Output from UDMCParser - will be modified in place to 
                    form decorated_tree
    
    Returns:  decorated_tree, variables_dict
    """
    res = UDMCSemanticAnalyzer(ast_tree)
    return ast_tree, res.variables




