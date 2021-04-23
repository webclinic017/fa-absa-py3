from __future__ import print_function
"""FTMPerfStats - Output performance stats for ADFL calculations from TM

NOTE:
 Avoid having several columns with the same name (for example the same 
 column from different contexts or columns with same name but different IDs)
 they will be treated as the same and performance scores will be wrong.

SUITABLE Menu extensions

FPortfolioSheet:Performance Data By Cell =
  Function=FTMPerfStats.dump_perf_menu_detailed_cb
  MenuType=GridCell
  ParentMenu=AEF Performance

FPortfolioSheet:Performance Data By Column =
  Function=FTMPerfStats.dump_perf_menu_cb
  MenuType=GridCell
  ParentMenu=AEF Performance

FPortfolioSheet:Performance Data By Column Advanced =
  Function=FTMPerfStats.dump_perf_menu_advanced_cb
  MenuType=GridCell
  ParentMenu=AEF Performance


(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

"""

from sets import Set

import acm

def safe_str(obj):
    """String representation of obj which will use StringKey for FObjects"""
    if hasattr(obj, "StringKey"):
        return obj.StringKey()
    return str(obj)

def all_evaluators(ev):
    """Get all unique nodes in an evaluator tree as a set"""
    def recurse(ev, res, indent = ""):
        if hasattr(ev, "IsKindOf") and ev.IsKindOf(acm.FEvaluator):
            res.add(ev)
            for child in ev.AllInputs():
                if not child in res:
                    recurse(child, res, indent + " ")
    res = Set()
    recurse(ev, res)
    return res

    
class FGridStats(object):
    """Performance statistics for a grid, adfl trees"""

    def __init__(self, grid_sel, advanced):
        """Snapshot of stats is taken on creation
        
        Will not hold any refs to FObjects after creation
        
          grid_sel   An FGridSelection
          advanced   Collect advanced statistics 
        """
    
        cells = [cell for cell in grid_sel.SelectedCells() if cell.RowObject()]
        
        # Create a column -> evaluator mapping 
        ev_by_col = {}
        for cell in cells:
            if cell.Evaluator():
                ev_by_col.setdefault(cell.Column(), Set()).union_update(all_evaluators(cell.Evaluator()))
        
        # Calculate number of columns each evaluator occurs in
        ev_use_count = {}
        for evs in ev_by_col.values():
            for ev in evs:
                ev_use_count[ev] = ev_use_count.get(ev, 0) + 1
        
        self.col_cost = {}

        # Calculate number of evs + reuse weighted score for each column
        for col, evs in ev_by_col.items():
            score = sum( [ 1.0 / ev_use_count[ev] for ev in evs] )
            self.col_cost[col.StringKey()] = (len(evs), score)
        if advanced:
            colwidth = 20
            self.column_sim = "Inter column reuse\n"
            for colname in  [" "] + [col.StringKey() for col in ev_by_col.keys()]:
                self.column_sim += colname.ljust(colwidth) +  "\t"
            for cola, evsa in ev_by_col.items():
                self.column_sim += "\n" + cola.StringKey().ljust(colwidth) + "\t"
                for colb, evsb in ev_by_col.items():
                    self.column_sim += "\t" + str(round(1.0*len(evsa & evsb) / len(evsa), 2)).ljust(colwidth)
        else:
            self.column_sim = "Column similarity not calculated unless running in advanced mode"


def dump_grid(cells):
    cell_sum = 0
    columns = [] # maintain the order
    columns_dict = {}
    rows = [] # maintain the order
    rows_dict = {}
    default_size = 6
    row_id_max = default_size 

    for cell in cells:
        if cell.RowObject():
            row_id = cell.RowObject().StringKey()
            col_id = cell.Column().StringKey()
            
            if not columns_dict.has_key(col_id):
                columns_dict[col_id] = 1
                columns.append((col_id, max([len(col_id), default_size])))
            
            if not rows_dict.has_key(row_id):
                rows_dict[row_id] = {}
                rows.append(row_id)
                if len(row_id) > row_id_max:
                    row_id_max = len(row_id)

            nbr_evals = len(all_evaluators(cell.Evaluator()))
            rows_dict[row_id][col_id] = nbr_evals
            cell_sum += nbr_evals

    print ()
    print (' '*row_id_max, end= '')
    for c, l in columns:
        s = "%"+str(l)+"s"
        print (s % c, end='')
    print ()
 
    print ('-'*row_id_max, end='')
    for c, l in columns:
        print ('-'*l, end='')
    print ()

    for row_id in rows:
        row = rows_dict[row_id]
        s = "%-"+str(row_id_max)+"s"
        print (s % row_id, end='')
 
        for c, l in columns:
            if row.has_key(c):
                s = "%"+str(l)+"d"
                print (s % row[c], end='')
            else:
                print (" "*l, end='')
        print ()
    print ()
    return cell_sum

def dump_perf(eii, verbose = False, advanced = False):
    """Dump performance stats for a grid selection"""
    print ("** Performance statistics for grid selection in: ", end='')
    trdmgr = eii.ExtensionObject() # A FUiTrdMgrFrame
    gridselection = trdmgr.ActiveSheet().Selection()
    print (trdmgr.ActiveSheet().StringKey())
    cells = gridselection.SelectedCells()
    if verbose:
        cell_sum = dump_grid(cells)
        print ("Sum of cells = ", cell_sum)
    grid_stats = FGridStats(gridselection, advanced)

    print ("\nColumn cost")
    tot_count, tot_score = 0, 0
    for col, (ev_count, score) in grid_stats.col_cost.items():
        print (col.ljust(25), " : ", ev_count, " ( ", int(score), ")")
        tot_count += ev_count
        tot_score +=  score
    
    if advanced:
        print ("\n", grid_stats.column_sim)

    print ("------------------------------------------------------")
    print ("Total                      :  ", tot_count, " ( ", int(tot_score), ")")
    if advanced:
        print ("         global reuse factor = ", tot_count*1.0 / tot_score)

def dump_perf_menu_cb(eii):
    dump_perf(eii, False)

def dump_perf_menu_advanced_cb(eii):
    dump_perf(eii, False, True)

def dump_perf_menu_detailed_cb(eii):
    dump_perf(eii, True)
