from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FDocInspector - Run Script GUI for scaning the documentation

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION    

    FDocInspector is a scanning tool for gather information about the documentation of the
    ACM classes, ACM methods and ACM functions within the ACM browser. 

-------------------------------------------------------------------------------------------------------"""

import acm

# ----------------------Settings---------------------------

def startRunScript(eii):                
    #module, context        
    acm.RunModuleWithParameters('FDocInspector', acm.GetDefaultContext()) 

def getContext():
    context_list = []
    for i in acm.FExtensionContext.Select(''):
        context_list.append(i.Name())
    context_list.sort()
    return context_list

def getInspector():
    return ['ACM classes', 'ACM methods', 'ACM functions']

def print_stats( obj_type, numTotal, numDocumented, public, private, unclassified ):
    print ('\n%s:%s' % ( obj_type, '-'*15 ))
    print ('Total: \t\t%s' % numTotal)
    print ('Documented: \t%s' % numDocumented)
    print ('Public: \t%s' % public)
    print ('Private: \t%s' % private)
    print ('Unclassified: \t%s' % unclassified)

def num_fobjects_with_documentation( lstObjects, context ):
    ''' List all Classes, C++ Metods and CFunctions which have documentation '''
    numDocumented = 0
    for i in lstObjects:
        if len(i.DocString()) != 0 or is_private( i, context ) or is_public( i, context ):
            numDocumented += 1 
    return numDocumented

def num_fobjects_numOrphins( lstObjects, context ):
    ''' List all Classes, C++ Metods and CFunctions which have documentation '''
    numOrphins = 0
    for i in lstObjects:
        if len(i.DocString()) != 0 and not ( is_private( i, context ) or is_public( i, context ) ):
            numOrphins += 1
            print ("Documented without classification:", i.StringKey())
    return numOrphins

def is_private( klass, context ):
    return acm.FExtensionContext[context].IsMember(klass.DocString(), "FDocString", "aef", "public")

def is_public( klass, context ):
    return acm.FExtensionContext[context].IsMember(klass.DocString(), "FDocString", "aef", "private")
    
def get_count( lstObjects, context ):
    """count public, private and unclassified objects"""
    public = private = unclassified = 0
    for i in lstObjects:
        if is_private( i, context ):
            private += 1
        elif is_public( i, context ):
            public += 1
        else: 
            unclassified += 1
    return public, private, unclassified

def get_class_stats( context ):
    ''' Lists all Classes '''
    all = acm.FClass.InstancesKindOf()
    allClasses = []
    for i in all:
        if i.IsParameterized()== False:
            allClasses.append(i)
            
    numDocClasses = num_fobjects_with_documentation( allClasses, context )
    num_fobjects_numOrphins( allClasses, context )
    public, private, unclassified = get_count( allClasses, context )
    print_stats( "Classes", len(allClasses), numDocClasses, public, private, unclassified )
    
def get_method_stats( context ):
    ''' List all C++ Metods '''
    allCppMethods = acm.FCppMethod.Instances()
    allCppMethods = [ method for method in allCppMethods if method.StringKey() not in [ 'ceQuote()', 'ggerQuote()', 'teReply()'  ] and method.ReceiverClass() != None ] #SPR-288539
    numDocCppMethods = num_fobjects_with_documentation( allCppMethods, context )
    public, private, unclassified = get_count( allCppMethods, context )
    print_stats( "Methods", len(allCppMethods), numDocCppMethods, public, private, unclassified )
   
def get_function_stats( context ):
    ''' List all CFunctions '''
    allCFunctions = acm.FCFunction.Instances()
    numDocCFunctions = num_fobjects_with_documentation( allCFunctions, context )
    public, private, unclassified = get_count( allCFunctions, context )
    print_stats( "Functions", len(allCFunctions), numDocCFunctions, public, private, unclassified )

def get_stats(ael_variables):
    inspector = ael_variables['inspector']
    context = ael_variables['context']
    if inspector == 'ACM classes':
        get_class_stats( context )
    elif inspector == 'ACM methods':
        get_method_stats( context )
    elif inspector == 'ACM functions': 
        get_function_stats( context )
    else:
        raise Exception( "Type not supported" )

# ---------------------ael_variables-----------------------

ael_variables = [('context', 'Context', 'string', getContext(), 'Standard', 1, 0, 'Select the context to scan.', None, 1), 
                ('inspector', 'Inspect', 'string', getInspector(), 'ACM classes', 1, 0, 'Select wath to inspect.', None, 1),]


# -----------------------ael_main--------------------------

def ael_main(ael_variables):
    get_stats( ael_variables ) 
    
        
        

