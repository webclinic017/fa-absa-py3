'''
D A T A B A S E   D E P E N D E N C I E S 

Author: Michael Gogins
Date: 25 March 2015

This module provides facilities for gathering all data dependencies of a 
list of FCommonObjects into a dependency graph; of providing these 
dependencies as a list of unique FCommonObjects in dependency order; of 
providing these dependencies as a list of AMBA messages that will reliably 
insert into or update any Front Arena database; and of populating an 
FUxTreeControl's tree of items, or part of that tree, with the dependency 
graph. 

Data dependencies work as follows. Take for example an FBenchmarkCurve. 
This FCommonObject contains foreign keys, also called "references out". If 
the references out do not already exist in a database, the curve itself cannot 
be inserted into that database. The curve also contains collections of 
yield points, and other collections, which contain objects that have the curve 
as a foreign key. These objects are called the curve's "references in". It is 
possible to insert the curve into a database that does not contain the 
references in, but this would not make much sense, as the curve would lack its 
actual data. References out and references in define "database dependencies."
However, "data dependencies" include not only database dependencies, but also 
logical joins created by code in the Arena Class Model, such as prices and 
other valuation data required by instruments. These logical joins are created 
by context mappings. Therefore, not only the objects selected by context 
mappings, but also the objects required to create the context mappings, are
included in data dependencies. In this code, context mappings are treated as 
if they are references out.

Unfortunately, collecting all of the references out and all of 
the references in for a complex FCommonObject might produce a tangled web of 
references that could become impractically large. In order to avoid an 
unwieldy web of references that could grow to encompass much of the database, 
this module compiles only a subset of the actual references in. This subset is 
configurable, but includes for example instruments for curve benchmarks and 
points, and trades for portfolios. There is also a configurable list of 
references out to exclude.

This module uses graph theory to analyze and manage data dependencies. A 
depender is an in node, its dependee is an out node, and the pair forms a 
directed edge. Therefore, the data dependencies of an FCommonObject form 
a directed graph. Indeed, to be usable, this directed graph must also not 
contain any loops or cycles and so must be a directed acyclic graph (DAG). 

Given an arbitrary list of FCommonObjects, the data dependencies could 
form a DAG with one root (a tree), multiple roots (a multipartite DAG), or 
even disconnected subgraphs (a forest of trees and/or multipartite DAGs).

FObjects are considered to be uniquely identified and ordered by string keys 
in the format "FClass [StringKey|Oid]". To produce a list of unique 
FCommonObjects in dependency order, the DAG is ordered first by roots, and 
then by topological sort of the dependency graph. 

To graphically display the dependencies and enable editing them, an 
FUxTreeControl is used. This usually involves some redundancies. However, 
redundant FCommonObjects are not serialized.

This module uses the open source NetworkX Python module for graph algorithms.
'''

import acm
import cProfile as Profile
import cStringIO as StringIO

import FLogger
import networkx

import PackageInstallerParametersManager

import pstats


import sys
import time
import traceback
try:
    pass #import FPythonDebugger
except:
    traceback.print_exc()


sys.setrecursionlimit(10000)

test = False

reverse_tree = False
debug = True
do_profile = False
# True means object comes before in reference;
# False means in reference comes before object.
in_requires_object = True
profiler = Profile.Profile()

# These are used to mark which references of which nodes have already been collected.
# Without avoiding already collected references, the stack overruns.
got_non_database_dependencies_for = set()
got_part_dependencies_for = set()
got_out_dependencies_for = set()
got_in_dependencies_for = set()

parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
logger = FLogger.FLogger(name=__name__, level=verbosity)
logger.info('DatabaseDependencies is using pure Python NetworkX')

try:
    import PackageInstallerReferences
except ImportError:
    try:
        import PackageInstallerReferencesTemplate as PackageInstallerReferences
    except:
        logger.error(traceback.format_exc())

PackageInstallerReferences
generator = acm.FAMBAMessageGenerator()

def target_entity_id(fobject):
    stringkey = str(fobject.Oid()).strip()
    classname = str(fobject.ClassName())
    if classname.endswith('Id'):
        return None
    if classname.endswith('Alias'):
        return None
    if classname == 'FTransactionHistory':
        return None
    return '%s [%s]' % (classname, stringkey)
    
target_entity_ids = set()

def load_target_entity_ids(file):
    try:
        logger.debug('load_target_entity_ids() from "%s"...' % file)
        target_entity_ids.clear()
        with open(file, 'r') as fyle:
            lines = fyle.readlines()
        for line in lines:
            target_entity_ids.add(line.strip())
    except:
        logger.error(traceback.format_exc())
        target_entity_ids.clear()
    finally:
        logger.debug('load_target_entity_ids(): %s entity ids.' % len(target_entity_ids))
        
def should_follow_target_entity(fobject):
    key = target_entity_id(fobject)
    if key in target_entity_ids:
        return False
    return True

def key_for_entity(entity):
    return '%s[%s]' % (entity.ClassName(), entity.Oid())

def clean_list(oldlist):
    cleanlist = []
    for item in oldlist:
        if item != None:
            try:
                if item.IsKindOf(acm.FCommonObject):
                    if item not in cleanlist:
                        cleanlist.append(item)
            except:
                logger.error(traceback.format_exc())
    return cleanlist

def reference_classes(object, reference):
    return '%s|%s' % (object.ClassName(), reference.ClassName()) 

def node_id(fobject):
    try:
        return '%s [%s|%s]' % (fobject.ClassName(), fobject.StringKey(), fobject.Oid())
    except:
        logger.error('Could not generate node ID for: %s %s' % (type(fobject), fobject))
        
def edge_id(depender, dependee):
    return '%s requires %s' % (node_id(depender), node_id(dependee))
    
def set_attribute(graph, node, key, value, override = False):
    if override == True:
        graph.node[node][key] = value
    else:
        if key not in graph.node[node]:
            graph.node[node][key] = value
    
def get_attribute(graph, node, key, default=None):
    if node not in graph.node:
        return None
    attributes = graph.node[node]
    if attributes == None:
        return default
    if key not in attributes:
        return default
    return attributes[key]

def remove_attribute(graph, node, key):
    attributes = graph.node[node]
    if attributes != None:
        if key in attributes:
            del attributes[key]
            
def list_dependencies(graph, dependencies):
    for dependency in dependencies:
        logger.info('%s %s %s' % (node_id(dependency), get_attribute(graph, dependency, 'reference'), get_attribute(graph, dependency, 'exclude', '+')))
    logger.info('%s %s' % (len(dependencies), 'dependencies.'))
        
def list_edges(graph):
    for edge in graph.edges():
        in_node = edge[0]
        out_node = edge[1]
        out_reference = get_attribute(graph, out_node, 'reference')
        logger.info('%s requires:' % node_id(in_node))
        logger.info('  %-3s %s' % (out_reference, node_id(out_node)))

def get_references_out(fobject):
    references_out = fobject.ReferencesOut()
    return references_out
    
def get_references_in(fobject):
    references_in = fobject.ReferencesIn()
    return references_in
    
def find_roots(graph):
    began_find_roots = time.clock()
    try:
        logger.debug('Began find_roots()...')
        # Mark roots. These are not necessarily the objects selected by the user.
        dependencies = networkx.topological_sort(graph)
        roots = set()
        for dependency in dependencies:
            neighbors = networkx.ancestors(graph, dependency)
            if neighbors == None or len(neighbors) == 0:
                logger.debug('Found root node: %s' % node_id(dependency))
                roots.add(dependency)
                set_attribute(graph, dependency, 'reference', 'root', True)
        # Also return a list of the roots in classname, id, oid order.
        return sorted(roots, key=node_id)
    except:
        logger.error(traceback.format_exc())
    finally:
        ended_find_roots = time.clock()
        elapsed_find_roots = ended_find_roots - began_find_roots
        logger.debug('Ended find_roots (%12.4f seconds).' % elapsed_find_roots)
        
def find_nodes(graph):#this function is currently not being used
    began = time.clock()
    try:
        logger.debug('Began find_nodes()...')
        result = set()
        for node in graph.nodes():
            result.add(node)
        result = set()
        sorted_result = sorted(result, key=node_id)
        return sorted_result
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_nodes (%12.4f seconds).' % elapsed)

def get_all_nodes(graph):
    began = time.clock()
    try:
        logger.debug('Began get_all_nodes()...')
        result = set()
        for node in graph.nodes():
            result.add(node)
        sorted_result = sorted(result, key=node_id)
        return sorted_result
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended get_all_nodes (%12.4f seconds).' % elapsed)

def find_edges(graph):
    began = time.clock()
    try:
        logger.debug('Began find_edges()...')
        return graph.edges()
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_edges (%12.4f seconds).' % elapsed)

def find_ancestors(graph, fobject):
    began = time.clock()
    try:
        logger.debug('Began find_ancestors()...')
        ancestors = networkx.ancestors(graph, fobject)
        return sorted(ancestors, key=node_id)
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_ancestors (%12.4f seconds).' % elapsed)

def find_descendants(graph, fobject):
    began = time.clock()
    try:
        logger.debug('Began find_descendants()...')
        descendants = networkx.descendants(graph, fobject)
        return sorted(descendants, key=node_id)
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_descendants (%12.4f seconds).' % elapsed)
    
def find_predecessors(graph, fobject):
    began = time.clock()
    try:
        logger.debug('Began find_predecessors()...')
        predecessors = graph.predecessors(fobject)
        return sorted(predecessors, key=node_id)
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_predecessors (%12.4f seconds).' % elapsed)

def find_successors(graph, fobject):
    began = time.clock()
    try:
        logger.debug('Began find_successors()...')
        successors = graph.successors(fobject)
        return sorted(successors, key=node_id)
    except:
        logger.error(traceback.format_exc())
    finally:
        ended = time.clock()
        elapsed = ended - began
        logger.debug('Ended find_successors (%12.4f seconds).' % elapsed)

    
'''
Removes certain 'sub-messages' from an FAMBAMessage.
This is essential for preserving correct dependencies
importing AMBA messages that have been created in dependency order.
'''
def remove_sub_messages(message):
    main_message = message.Messages().AsList().First()
    sub_messages = main_message.Messages().AsList()
    parent = str(message.StringKey())
    for sub_message in sub_messages:
        child = str(sub_message.StringKey())
        if PackageInstallerReferences.should_remove_sub_message(parent, child):
            logger.debug('Removed sub_message:  %s %s' % (parent, child))
            main_message.RemoveMessage(sub_message)
        else:
            logger.debug('Retained sub_message: %s %s' % (parent, child))
    return message    

def GetDependencyGraph_(depth, fobject, graph):#check if this function even gets called
    if fobject not in got_non_database_dependencies_for:
        got_non_database_dependencies_for.add(fobject)
        non_database_references = PackageInstallerReferences.non_database_dependencies(fobject)
        for non_database_reference in non_database_references:
            GetDependencyGraph_(depth + 1, non_database_reference, graph)
    # We don't want "parts" (i.e. AMBA "sub-messages"), so therefore 
    # we need to treat the references out of the parts as references out of THIS object.
    # Except for this object, of course!
    if fobject not in got_part_dependencies_for:
        got_part_dependencies_for.add(fobject)
        for parts in fobject.Parts():
            for part in parts:
                if PackageInstallerReferences.should_remove_part(fobject, part):
                    for reference in part.ReferencesOut():
                        if PackageInstallerReferences.should_follow_reference_out(part, reference):      
                            if fobject != reference and fobject != part:
                                edge = (fobject, reference)
                                if edge not in graph.edges():
                                    graph.add_edge(*edge)
                                    logger.debug('%9d Adding part edge: %s' % (depth, edge_id(*edge)))                                
                                    if networkx.is_directed_acyclic_graph(graph) == False:
                                        cycles = networkx.simple_cycles(graph)
                                        for cycle in cycles:
                                            logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                            for node in cycle:
                                                logger.info('              %s' % node_id(node))
                                        graph.remove_edge(*edge)
                                        logger.info('          Removed part edge (%s) to break cycle.' % edge_id(*edge))
                                    else:
                                        GetDependencyGraph_(depth + 1, reference, graph)
    if fobject not in got_out_dependencies_for:
        got_out_dependencies_for.add(fobject)
        for reference in get_references_out(fobject):
            if PackageInstallerReferences.should_follow_reference_out(fobject, reference) == False:      
                logger.debug('          Not following "out" (%s).' % edge_id(fobject, reference))
                pass
            else:
                if fobject != reference:
                    edge = (fobject, reference)
                    if edge not in graph.edges():
                        graph.add_edge(*edge)
                        logger.debug('%9d Adding out edge:  %s' % (depth, edge_id(*edge)))                                
                        if networkx.is_directed_acyclic_graph(graph) == False:
                            cycles = networkx.simple_cycles(graph)
                            for cycle in cycles:
                                logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                for node in cycle:
                                    logger.info('              %s' % node_id(node))
                            graph.remove_edge(*edge)
                            logger.info('          Removed out edge (%s) to break cycle.' % edge_id(*edge))
                        else:
                            set_attribute(graph, reference, 'reference', 'out')
                            GetDependencyGraph_(depth + 1, reference, graph)
    # Some references are never followed (no trades as references in of instruments, e.g.).
    if fobject not in got_in_dependencies_for:
        got_in_dependencies_for.add(fobject)
        for reference in get_references_in(fobject):
            if PackageInstallerReferences.should_follow_reference_in(fobject, reference) == False:    
                logger.debug('          Not following "in" (%s).' % edge_id(fobject, reference))
            else:
                if fobject != reference:
                    edge = (reference, fobject)
                    if edge not in graph.edges():
                        graph.add_edge(*edge)
                        logger.debug('%9d Adding in edge:   %s' % (depth, edge_id(*edge)))
                        if networkx.is_directed_acyclic_graph(graph) == False:
                            cycles = networkx.simple_cycles(graph)
                            for cycle in cycles:
                                logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                for node in cycle:
                                    logger.info('              %s' % node_id(node))
                            graph.remove_edge(*edge)
                            logger.info('          Removed in edge %s to break cycle.' % edge_id(*edge))
                        else:
                            set_attribute(graph, reference, 'reference', 'in')
                            GetDependencyGraph_(depth + 1, reference, graph)
    return graph
    
''' 
Returns a directed acyclic graph, which may be a tree, a multipartite
DAG, or a forest of trees and/or multipartite graphs, that represents 
the data dependencies of the list of FObjects. These dependencies 
include most of the out references of those objects, recursively, and selected 
in references of those objects, recursively. Non-database dependencies 
may also be included.
'''
def GetDependencyGraph_(depth, fobject, graph, update_status = None):
    if fobject not in got_non_database_dependencies_for:
        got_non_database_dependencies_for.add(fobject)
        non_database_references = PackageInstallerReferences.non_database_dependencies(fobject)
        for non_database_reference in non_database_references:
            if should_follow_target_entity(non_database_reference) == False:
                logger.debug('          Not following "non-database" (%s), already in target.' % edge_id(fobject, non_database_reference))
            else:
                GetDependencyGraph_(depth + 1, non_database_reference, graph)
    # We don't want "parts" (i.e. AMBA "sub-messages"), so therefore 
    # we need to treat the references out of the parts as references out of THIS object.
    # Except for this object, of course!
    if fobject not in got_part_dependencies_for:
        got_part_dependencies_for.add(fobject)
        for parts in fobject.Parts():
            for part in parts:
                if PackageInstallerReferences.should_remove_part(fobject, part):
                    for reference in part.ReferencesOut():
                        if PackageInstallerReferences.should_follow_reference_out(part, reference):      
                            if should_follow_target_entity(reference) == False:
                                logger.debug('          Not following "part" (%s), already in target.' % edge_id(fobject, reference))
                            else:
                                if fobject != reference and fobject != part:
                                    edge = (fobject, reference)
                                    if edge not in graph.edges():
                                        graph.add_edge(*edge)
                                        logger.debug('%9d Adding part edge: %s' % (depth, edge_id(*edge)))                                
                                        if networkx.is_directed_acyclic_graph(graph) == False:
                                            cycles = networkx.simple_cycles(graph)
                                            for cycle in cycles:
                                                logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                                for node in cycle:
                                                    logger.info('              %s' % node_id(node))
                                            graph.remove_edge(*edge)
                                            logger.info('          Removed part edge (%s) to break cycle.' % edge_id(*edge))
                                        else:
                                            if update_status:
                                                update_status('Please wait... added part dependency: %s...' % edge_id(*edge))
                                            GetDependencyGraph_(depth + 1, reference, graph)
    if fobject not in got_out_dependencies_for:
        got_out_dependencies_for.add(fobject)
        for reference in get_references_out(fobject):
            if PackageInstallerReferences.should_follow_reference_out(fobject, reference) == False:      
                logger.debug('          Not following "out" (%s).' % edge_id(fobject, reference))
            elif should_follow_target_entity(reference) == False:
                logger.debug('          Not following "out" (%s), already in target.' % edge_id(fobject, reference))
            else:
                if fobject != reference:
                    edge = (fobject, reference)
                    if edge not in graph.edges():
                        graph.add_edge(*edge)
                        logger.debug('%9d Adding out edge:  %s' % (depth, edge_id(*edge)))                                
                        if networkx.is_directed_acyclic_graph(graph) == False:
                            cycles = networkx.simple_cycles(graph)
                            for cycle in cycles:
                                logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                for node in cycle:
                                    logger.info('              %s' % node_id(node))
                            graph.remove_edge(*edge)
                            logger.info('          Removed out edge (%s) to break cycle.' % edge_id(*edge))
                        else:
                            if update_status:
                                update_status('Please wait... added out dependency: %s...' % edge_id(*edge))
                            set_attribute(graph, reference, 'reference', 'out')
                            GetDependencyGraph_(depth + 1, reference, graph)
    # Some references are never followed (no trades as references in of instruments, e.g.).
    if fobject not in got_in_dependencies_for:
        got_in_dependencies_for.add(fobject)
        for reference in get_references_in(fobject):
            if PackageInstallerReferences.should_follow_reference_in(fobject, reference) == False:    
                logger.debug('          Not following "in" (%s).' % edge_id(fobject, reference))
            elif should_follow_target_entity(reference) == False:
                logger.debug('          Not following "in" (%s), already in target.' % edge_id(fobject, reference))
            else:
                if fobject != reference:
                    edge = (reference, fobject)
                    if edge not in graph.edges():
                        graph.add_edge(*edge)
                        logger.debug('%9d Adding in edge:   %s' % (depth, edge_id(*edge)))                                
                        if networkx.is_directed_acyclic_graph(graph) == False:
                            cycles = networkx.simple_cycles(graph)
                            for cycle in cycles:
                                logger.info('          *** Found cycle after adding edge %s:' % edge_id(*edge))
                                for node in cycle:
                                    logger.info('              %s' % node_id(node))
                            graph.remove_edge(*edge)
                            logger.info('          Removed in edge %s to break cycle.' % edge_id(*edge))
                        else:
                            if update_status:
                                update_status('Please wait... added in dependency: %s...' % edge_id(*edge))                    
                            set_attribute(graph, reference, 'reference', 'in')
                            GetDependencyGraph_(depth + 1, reference, graph)
    return graph
    
''' 
Returns a directed acyclic graph, which may be a tree, a multipartite
DAG, or a forest of trees and/or multipartite graphs, that represents 
the data dependencies of the list of FObjects. These dependencies 
include most of the out references of those objects, recursively, and selected 
in references of those objects, recursively. Non-database dependencies 
may also be included.
'''
def GetDependencyGraph(fobjects, update_status = None):
    if do_profile == True:
        profiler.enable()
    began_get_dependency_graph = time.clock()
    got_non_database_dependencies_for.clear()
    got_part_dependencies_for.clear()
    got_out_dependencies_for.clear()
    got_in_dependencies_for.clear()   
    logger.debug('Began Python GetDependencyGraph()...')
    try:
        # To ensure that the graph for any ordering of the same fobjects 
        # has the same order, the fobjects are sorted first. After that, order 
        # is determined by topological sort.
        fobjects = sorted(fobjects, key=node_id)
        graph = networkx.DiGraph()
        for fobject in fobjects:
            GetDependencyGraph_(1, fobject, graph, update_status)
        return graph
    except:
        logger.error(traceback.format_exc())
    finally:
        ended_get_dependency_graph = time.clock()
        elapsed_get_dependency_graph = ended_get_dependency_graph - began_get_dependency_graph
        logger.debug('Ended python GetDependencyGraph (%12.4f seconds).' % elapsed_get_dependency_graph)
        if update_status:
            update_status('Finished finding dependencies.')
        if do_profile == True:
            profiler.disable()
            print()
            print('TOTAL TIME (not counting sub-calls)')
            print()
            stringio = StringIO.StringIO()
            statistics = pstats.Stats(profiler, stream=stringio).sort_stats('time')
            statistics.print_stats()
            print(stringio.getvalue())        
            print()
            print('CUMULATIVE TIME (counting sub-calls)')
            print()
            stringio = StringIO.StringIO()
            statistics = pstats.Stats(profiler, stream=stringio).sort_stats('cumulative')
            statistics.print_stats()
            print(stringio.getvalue())  
'''
Returns a list of the unique FCommonObjects, in order of increasing dependency, 
in the graph.
'''
def GetDependencyList(graph, update_status = None):
    logger.debug('Began GetDependencyList()...')
    began_get_dependency_list = time.clock()
    try:
        dependencies = networkx.topological_sort(graph)
        dependencyset = set()
        uniquedependencies = []
        for dependency in dependencies:
            if dependency not in dependencyset:
                dependencyset.add(dependency)
                uniquedependencies.append(dependency)
        return uniquedependencies[::-1]
    except:
        logger.error(traceback.format_exc())
    finally:
        ended_get_dependency_list = time.clock()
        elapsed_get_dependency_list = ended_get_dependency_list - began_get_dependency_list
        logger.debug('Ended GetDependencyList (%12.4f seconds).' % elapsed_get_dependency_list)


'''
Populate the tree control rooted in treeitem with the graph constructed from 
the fobjects. Only one level at a time is built. If the user double-clicks on 
a node, that node is then expanded.
'''
def PopulateFuxTreeControl(fobjects, rootitem, exclusions = None, exclusion_types = None, update_status = None):

    began_populate_fux_tree_control = time.clock()
    try:
        logger.debug('Began PopulateFuxTreeControl()...')
        if isinstance(fobjects, tuple):
            fobjects = fobjects[0]
        graph = GetDependencyGraph(fobjects, update_status)
        if reverse_tree:
            graph.reverse(False)
        roots = find_roots(graph)
        classNames = set()
        parent_item = None
        for root in roots:
            b_new = False
            treeitem = None
            if root.ClassName() in classNames:
                pass
            else:
                b_new = True
                classNames.add(root.ClassName())
            if b_new:
                b_new = False
                parent_item = rootitem.AddChild()
                parent_item.Label(root.ClassName(), 1)
                exclude = get_attribute(graph, root, 'exclude', '+')
                if (exclusion_types and root.ClassName().AsString() in exclusion_types):
                    exclude = '-'
                    set_attribute(graph, root, 'exclude', '-')
                    if str(parameters.read('ShowExcludedInDependencyTree')).upper() == 'TRUE':
                        i = 0
                        while i <= 5:#updating all columns
                            parent_item.Style(i, False, \
                            acm.UX().Colors().Create(200, 200, 200).ColorRef(), \
                            acm.UX().Colors().Create(255, 255, 255).ColorRef())
                            i = i + 1
                    else:
                        parent_item.Visible(False)
                parent_item.Label(exclude, 5)
            treeitem = parent_item.AddChild()
            treeitem.SetData(root)
            treeitem.Label(root.StringKey(), 0)
            treeitem.Label(root.ClassName(), 1)
            treeitem.Label(root.Table().Name(), 2)
            treeitem.Label(root.Oid(), 3)
            reference = get_attribute(graph, root, 'reference')
            treeitem.Label(reference, 4)
            exclude = get_attribute(graph, root, 'exclude', '+')
            if (exclusion_types and root.ClassName().AsString() in exclusion_types) or (exclusions and root in exclusions):
                exclude = '-'
                set_attribute(graph, root, 'exclude', '-')
                if str(parameters.read('ShowExcludedInDependencyTree')).upper() == 'TRUE':
                    i = 0
                    while i <= 5:#updating all columns
                        treeitem.Style(i, False, \
                        acm.UX().Colors().Create(200, 200, 200).ColorRef(), \
                        acm.UX().Colors().Create(255, 255, 255).ColorRef())
                        i = i + 1
                else:
                    treeitem.Visible(False)
            treeitem.Label(exclude, 5)
        if reverse_tree:
            graph.reverse(False)
        return graph
    finally:
        ended_populate_fux_tree_control = time.clock()
        elapsed_populate_fux_tree_control = began_populate_fux_tree_control - began_populate_fux_tree_control
        logger.debug('Ended PopulateFuxTreeControl(%12.4f).' % elapsed_populate_fux_tree_control)
        
def ExpandFuxTreeNode(graph, treeitem):
    logger.debug('ExpandFuxTreeNode()...')
    object = treeitem.GetData()
    logger.debug('treeitem: ' + str(treeitem))
    logger.debug('object: ' + node_id(object))
    if treeitem != None and object != None and treeitem.ChildrenCount() == 0:
        if reverse_tree:
            dependees = networkx.ancestors(graph, object)
        else:
            dependees = networkx.descendants(graph, object)
        for dependee in sorted(dependees, key=node_id):
            child = None
            child = treeitem.AddChild()
            child.SetData(dependee)
            child.Label(dependee.StringKey(), 0)
            child.Label(dependee.ClassName(), 1)
            child.Label(dependee.Table().Name(), 2)
            child.Label(dependee.Oid(), 3)
            reference = get_attribute(graph, dependee, 'reference')
            child.Label(reference, 4)
            exclude = get_attribute(graph, dependee, 'exclude', '+')
            child.Label(exclude, 5)
            logger.debug('%s %s' % (node_id(dependee), exclude))
    treeitem.Expand()
            
def PopulateFuxTreeControlFromGraph(graph, treeitem = None, trim = True):
    began_populate_fux_tree_control_from_graph = time.clock()
    logger.debug('PopulateFuxTreeControlFromGraph()...')
    dependencies = GetDependencyList(graph)
    logger.debug('')
    logger.debug('PopulateFuxTreeControlFromGraph dependencies:')
    logger.debug('')
    list_dependencies(graph, dependencies)
    logger.debug('')
    logger.debug('PopulateFuxTreeControlFromGraph edges:')
    logger.debug('')
    list_edges(graph)
    logger.debug('')
    for root in find_roots(graph):
        PopulateFuxTreeControl_(root, graph, 1, treeitem)
    ended_populate_fux_tree_control_from_graph = time.clock()
    elapsed_populate_fux_tree_control_from_graph = ended_populate_fux_tree_control_from_graph - began_populate_fux_tree_control_from_graph
    logger.debug('Ended PopulateFuxTreeControlFromGraph(%12.4f).' % elapsed_populate_fux_tree_control_from_graph)
    return graph
'''
Given a graph and one of its nodes, finds the subgraph of the node. Then,
finds the difference, i.e. the graph less the subgraph. Marks (or unmarks)
all nodes in the graph that are in to the subgraph, but not in the difference.
Returns the difference.
'''
def difference(graph, node, mark = True):
    logger.debug('difference(node: %s mark="%s")...' % (node_id(node), mark))
    """
    if mark:
        exclude = '-'
    else:
        exclude = '+'
    """
    try:
        subgraph = networkx.dfs_tree(graph, node)
    except:
        logger.error('Could not find subgraph for %s %s in graph.' % (type(node), node_id(node)))
        logger.error(traceback.format_exc())
        return
    graph_edges = graph.edges()
    subgraph_edges = subgraph.edges()
    graph_less_subgraph = networkx.DiGraph()
    for graph_edge in graph_edges:
        if graph_edge not in subgraph_edges:
            graph_less_subgraph.add_edge(*graph_edge)
    difference_ = set(graph_less_subgraph.nodes())
    if node in difference_:
        difference_.remove(node)
    for node in subgraph.nodes():
        if node not in difference_:
            if mark == True:
                set_attribute(graph, node, 'exclude', '-', True)
                logger.info('Excluding: %s' % node_id(node))
            else:
                set_attribute(graph, node, 'exclude', '+', True)
                logger.info('Including: %s' % node_id(node))
            value = get_attribute(graph, node, 'exclude', '+')
            logger.debug('node: %s %s' % (node_id(node), value))
    return difference_

def AddObjectsToPackage(self, *params):
    try:
        rootItem = self.m_buildPackageDialog.m_packageDependenciesTree.GetRootItem()
        recalculate = False
        objects = None
        if not self.m_buildPackageDialog.graph:
            if self.m_buildPackageDialog.m_queryFolderContent and params[0][0].IsKindOf(acm.FStoredASQLQuery):
                for object in params[0]:
                    instances = object.Query().Select()
                    for instance in instances:
                        try:
                            if instance in self.m_buildPackageDialog.m_package_objects:
                                logger.info('Object already in list: %s' % node_id(instance))
                            else:
                                try:
                                    self.m_buildPackageDialog.m_package_objects.Add(instance)
                                except:
                                    self.m_buildPackageDialog.m_package_objects.add(instance)
                                logger.info('Added object to list: %s' % node_id(instance))
                                recalculate = True
                        except Exception, e:
                            print("GOT ERROR", str(e))
                self.m_buildPackageDialog.m_queryFolderContent = False
            else:
                self.m_buildPackageDialog.m_package_objects = params[0]
            self.m_buildPackageDialog.PopulatePackageObjectsTree(self.m_buildPackageDialog.m_package_objects)
            self.m_buildPackageDialog.graph = PopulateFuxTreeControl(self.m_buildPackageDialog.m_package_objects, rootItem, \
                self.m_buildPackageDialog.m_exclusions, self.m_buildPackageDialog.m_exclusion_types, None)
            objects = GetDependencyList(self.m_buildPackageDialog.graph)
            self.m_buildPackageDialog.UpdateFuxTreeControlFromGraph(self.m_buildPackageDialog.graph)
        else:
            objects = GetDependencyList(self.m_buildPackageDialog.graph)
            logger.debug('objects: %s %s' % (type(objects), len(objects) if objects else objects))
            recalculate = False
            for object in self.selection:
                if object not in self.m_buildPackageDialog.m_package_objects:
                    try:
                        self.m_buildPackageDialog.m_package_objects.Add(object)
                    except:
                        self.m_buildPackageDialog.m_package_objects.add(object)
                if not object in objects:
                    if self.m_buildPackageDialog.m_queryFolderContent and object.IsKindOf(acm.FStoredASQLQuery):
                        instances = object.Query().Select()
                        for instance in instances:
                            try:
                                if instance in self.m_buildPackageDialog.m_package_objects:
                                    logger.info('Object already in list: %s' % node_id(instance))
                                else:
                                    try:
                                        self.m_buildPackageDialog.m_package_objects.Add(instance)
                                    except:
                                        self.m_buildPackageDialog.m_package_objects.add(instance)
                                    logger.info('Added object to list: %s' % node_id(instance))
                                    recalculate = True
                            except Exception, e:
                                print("GOT ERROR", str(e))
                        self.m_buildPackageDialog.m_queryFolderContent = False
                    objects.append(object)
                    logger.info('Added object to list: %s' % node_id(object))
                    recalculate = True
            self.m_buildPackageDialog.PopulatePackageObjectsTree(self.m_buildPackageDialog.m_package_objects)
            if recalculate == True:
                for child in rootItem.Children():
                    child.Remove()
            self.m_buildPackageDialog.graph = PopulateFuxTreeControl(self.m_buildPackageDialog.m_package_objects, rootItem, \
                self.m_buildPackageDialog.m_exclusions, self.m_buildPackageDialog.m_exclusion_types, None)
            objects = GetDependencyList(self.m_buildPackageDialog.graph)
            self.m_buildPackageDialog.UpdateFuxTreeControlFromGraph(self.m_buildPackageDialog.graph)
    except:
        logger.error(traceback.format_exc())

