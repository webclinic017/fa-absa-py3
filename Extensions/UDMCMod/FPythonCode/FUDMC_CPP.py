

import FUDMCParser_CPP
import FUDMCSemanticAnalyzer_CPP
from FUDMCCommon_CPP import SafeASTTraversal, MCError, dump_trace

class FUDMCValuationFunctionBuilder(SafeASTTraversal):
    """Traverse tree and write to a FObject representation for execution"""
    def __init__(self, payoffScript, tree, variables):        
        """Initialize FUDMCValuationFunctionBuilder
        
          payoffScript -- an FUDMCScriptPayoff instance
          tree    -- final tree representation of PEL code, McAstNode
          variables-- list of variables
        """
        SafeASTTraversal.__init__(self, tree )
        self.payoffScript = payoffScript
        self.variables = variables
        self.builtnodes = {}
    def build(self):
        """Build FObject representation onto self.payoffScript"""
        self._add_variables()
        self.postorder()
        """A zero start node Id means that the tree has no statements 
            (it can still have declarations). """
        startNodeId = (len(self.ast) > 1) and self.ast[1].impid or 0
        self.payoffScript.vm_setstartnode(startNodeId)
    def _add_variables(self): 
        """Add variables to valfun, in order defined."""
        vars = self.variables.items()
        vars.sort( lambda x, y: cmp( y[1].impid, x[1].impid) )
        for varname, var in vars:
            initinfo = 0
            if not (var.isparam or var.isprocess):
                initinfo = var.initinfo.impid
            self.payoffScript.vm_mkCVarNode(var.impid, var.vartype, varname, 
                                   var.isparam, var.isprocess, initinfo)
            self.builtnodes[var.impid] = 1
    def default(self, node):
        """Callback handler all node types, builds executable representation"""
        if node.impid in self.builtnodes: 
            return #vars have multiple refs
        childids = [ child.impid for child in node ]        
        self.payoffScript.vm_mkCNode(node.impid, node.typename, node.attr, node.valuetype, \
                          childids, node.debuginfo)        
        self.builtnodes[node.impid] = 1


def build_FMCValuationFunction(payoffScript, pelcode):
    """Build executable expression for pelcode onto payoffScript.
    
    This is the main entry point use d by PRIME. Ir should NEVER pass
    exceptions back to PRIME, these are instead returned as strings in
    the return dict under the key '_errormsg'
    
      payoffScript  -- an FUDMCScriptPayoff instance
      pelcode  -- string, containing Payoff Expression Language code
    """
    try:
        ast_tree = FUDMCParser_CPP.parse(pelcode)
        tree, variables = FUDMCSemanticAnalyzer_CPP.analyze(ast_tree)
        builder = FUDMCValuationFunctionBuilder(payoffScript, tree, variables)
        builder.build()
        return {}
    except MCError as err:
        return {'_errormsg' : str(err)}
    except Exception as err:
        """ Let all unexpected exceptions pass through to ease debugging. """
        trace = dump_trace()
        return {'_errormsg' : str(err), '_trace' : trace}





