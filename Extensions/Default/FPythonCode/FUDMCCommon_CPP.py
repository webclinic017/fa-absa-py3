

from __future__ import print_function
import __builtin__
import sys
import string

import re
import os
import spark 

import traceback

# Code to get around import problems in PRIME some packages
# such as pydot fail to import properly with PRIMEs default import
# functionality

def dump_trace():    
    traceback.print_exc(file=sys.stdout)            
    sys.stdout.flush()
    return str(sys.exc_value)+ "".join(traceback.format_list(traceback.extract_tb(sys.exc_traceback)))

def native_import(modname, extrapath = None):
    if extrapath:
        if not extrapath in sys.path:
            sys.path.append(extrapath)
    try:
        native_import_func = __builtin__.__old__import__
    except AttributeError:
        # fallback for older version or when running externally
        # print ("native_import failed to find __builtin__.__old__import__")
        native_import_func = __builtin__.__import__
    prime_import_func = __builtin__.__import__
    try:
        __builtin__.__import__ = native_import_func
        return __import__(modname)
    finally:
        __builtin__.__import__ = prime_import_func


# pydot should be installed for the tree graphing, if needed. 
# It can be downloaded from http://www.dkbza.org/pydot.html
# The path can be set in site-startup module, the default install location: 
# C:\Python26\Lib\site-packages
try:
    pydot = native_import("pydot", r"C:\Python26\Lib\site-packages")    
except ImportError as e:
    pydot = False
except Exception as e:
    print ("Failed to import pydot, non ImportError", e)
    pydot = False


# Drtodo hopefully we can make do with the FObject type system
# when doing the final implementatiosn
class MCType:
    """Represents a type such as int in MC mini language"""
    instances = {}
    def __init__(self, name):
        self.name = name
        MCType.instances[name] = self
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

def is_valid_type(typename):
    """Check that a typename is valid"""
    return typename in MCType.instances


# Basic types used ny MC mini language
mc_int =  MCType('int')
mc_double = MCType('double')
mc_doublematrix = MCType('matrix(double)')
mc_process = MCType('process') # 'internal' type, never directly exposed to users.

class MCVariable:
    """A variable or parameter in a payoff expression"""
    def __init__(self, varname, vartype, isparam, isprocess, initinfo, impid):
        self.varname = varname
        self.vartype = vartype
        self.isparam = isparam
        self.isprocess = isprocess
        self.initinfo = initinfo
        self.impid = impid
        
NOIMPID = 0        
class McAstNode:
    """Node type used for tree representation of expressions"""
    cnt = 1 
    def __init__(self, typename, attr='', terminal=False):
        self.typename = typename        
        self.attr = attr
        self.cnt = McAstNode.cnt
        self._kids = []
        McAstNode.cnt += 1
        self.valuetype = None
        self.debuginfo = ""    
        self.terminal = terminal
        self.error = None
        self.pos = -1
        self.lvalue = False
        self.impid = McAstNode.cnt
    def first_child_oftype(self, typename):
        """Get first child of type or None if not found"""
        for child in self._kids:
            if child.typename == typename:
                return child
    def first_descendant_oftype(self, typename):
        """Get first child of type or None if not found"""
        if self.typename == typename: 
            return self
        for child in self._kids:
            res = child.first_descendant_oftype(typename)
            if res: 
                return res                  
    def __str__(self):
        if self.valuetype:
            stringrep =  self.typename + " : " + str(self.valuetype)
        else:
            stringrep = self.typename
        return str(self.impid) + " " + stringrep
    def __debug_str__(self):
        stringrep = "NodeType = " + self.typename + ", attr = " + str(self.attr)
        if self.valuetype:
            stringrep = stringrep + ", ValueType = " + self.valuetype
        return stringrep
    def __cmp__(self, other):
        return cmp(self.typename, other)
    def __repr__(self):
        return self.typename +' '+ str(self.attr)  +' '+ str(self.cnt)
    def __getitem__(self, i):
        return self._kids[i]
    def __len__(self):
        return len(self._kids)
    def __setslice__(self, low, high, seq):
        self._kids[low:high] = seq
    def show(self):
        """Show graphic of tre for debug purposes"""
        if pydot:
            graph = MCDotGraph(self, type_decorator)
            graph.show()
        else:
            print ("/Failed to import pydot, tree graphing will not be available")
            print ("/if needed, download and install from : ")
            print ("/http://www.dkbza.org/pydot.html")
        
class SafeASTTraversal(spark.GenericASTTraversal):
    """Add exception handler for node creation to allow multierror reporting"""
    def postorder(self, node=None):
        """Traverse tree bottom up order, with exception handling"""
        try:
            spark.GenericASTTraversal.postorder(self, node)
        except MCError as err:
            raise err
    
def stringtodict(liststring):
    """Utility to convert a comma separated list to a dict"""
    return dict([ (item.strip(), 1) for item in liststring.split(",")])

class MCDotGraph(spark.GenericASTTraversal):
    """Traverse tree and construct pydot graph"""
    def __init__(self, ast, nodedecorator=None, edgedecorator=None):
        spark.GenericASTTraversal.__init__(self, ast)
        self.graph = pydot.Dot()
        self.graph.ordering = 'out'
        self.nodedecorator = nodedecorator
        self.edgedecorator = edgedecorator
        self.postorder()
    def default(self, node):
        """Add node to graph"""
        label = str(node) + "|" + str(node.attr)
        label = label.replace(">", "\\>")
        label = label.replace(":", " ")
        pydotnode = pydot.Node(str(id(node)), label=label, shape='record')
        self.graph.add_node(pydotnode)
        if self.nodedecorator:
            self.nodedecorator(pydotnode, node)
        for child in node:
            edge = pydot.Edge( str(id(node)), str(id(child)))
            self.graph.add_edge( edge )
    def show(self):
        """Generate picture and display"""
        outfile = r"c:\mcgraph.gif"
        self.graph.write_gif(outfile, prog='dot')        
        os.startfile(outfile)

def type_decorator(dotobj, mcast):
    """Decorate a dotty object based on type"""
    if hasattr(mcast, "valuetype") and mcast.valuetype:
        dotobj.set_style('bold')
    if mcast.error:
        dotobj.set_color("red")
        id1 = str(id(dotobj))+"err"
        errnode = pydot.Node(id1, label=mcast.error, color="red")        
        dotobj.parent_graph.add_node(errnode)
        edge = pydot.Edge( id1, dotobj.get_name() )
        dotobj.parent_graph.add_edge( edge )

class MCError(Exception):

    def __init__(self, msg, node=None, token=None, debug_info=None):
        self.msg          = msg
        self.node         = node
        self.token        = token
        self.debug_info   = debug_info
        
        Exception.__init__(self, msg)
    
    """Connect the information into a readable error string."""
    def __str__(self):
        str_repr = self.msg
        if self.node:
            str_repr = str_repr + " : " + str(self.node)
        if self.token:
            str_repr = str_repr + " : " + str(self.token)
        if self.debug_info:
            str_repr = str_repr + " : " + self.debug_info
        return str_repr




