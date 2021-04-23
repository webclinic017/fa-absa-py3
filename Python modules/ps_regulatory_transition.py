"""----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Replace all FA objects for Prime Services fund that
                           goes through a regulatory transition.
DEPARTMENT AND DESK     :  Pime Services Client Coverage
REQUESTER               :  Sarshnee Pather
DEVELOPER               :  Jakub Tomaga
CR NUMBER               :  3733743
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date         Change no   Developer      Description
--------------------------------------------------------------------------------
2016-06-14   3733743    Jakub Tomaga    Initial Implementation
2016-08-25   3907026    Jakub Tomaga    Exclude FileID_SoftBroker from task
                                        attributes that need to be changed
2016-09-27   3974633    Jakub Tomaga    Simplify the process
"""

import acm
from at_time import to_datetime
from at_ael_variables import AelVariableHandler
from PS_Functions import (get_pb_fund_counterparty,
                          get_pb_fund_counterparties,
                          get_pb_fund_shortname,
                          modify_asql_query)
from collections import deque


IGNORE_MODULE_TASKS = [
    "PS_MO_Onboarding",
    "ps_regulatory_transition",
    "ps_counterparty_name_change"
]


IGNORE_TASK_ATTRIBUTES = [
    "fileID_SoftBroker",
]


SHORTNAMES = [get_pb_fund_shortname(cp) for cp in get_pb_fund_counterparties()]


def get_query_attr_with_value(acm_query, value):
    """Lookup all attributes in the query and return together with operator."""
    asql_nodes = acm_query.AsqlNodes()
    deck = deque([(False, node) for node in asql_nodes])
    while deck:
        not_flag, node = deck.popleft()
        if node.IsKindOf(acm.FASQLAttrNode):
            attribute_value = str(node.AsqlValue())
            if attribute_value == value:
                yield (not_flag, node.AsqlAttribute().AttributeString().Text())
        elif node.IsKindOf(acm.FASQLOpNode):
            not_flag = node.Not()
            child_nodes = node.AsqlNodes()
            deck.extend([(not_flag, node) for node in child_nodes])


def counterparty_name_hook(selected_variable):
    """Display current counterparty name."""
    if selected_variable.value:
        cp = get_pb_fund_counterparty(selected_variable.value)
        update_date = str(to_datetime(cp.UpdateTime())).split(" ")[0]
        if update_date != acm.Time.DateToday():
            cp_name = ael_variables.get('original_cpty')
            cp_name.value = cp.Name()


def amend_Saxo_trades(orig_party, new_party, dry_run):
    ADDINFO_NAME = "Relationship_Party"
    print("AddInfo '%s' on trades..." % ADDINFO_NAME)
    query = acm.CreateFASQLQuery('FAdditionalInfo', 'AND')
    query.AddAttrNode('AddInf.Name', 'EQUAL', ADDINFO_NAME)
    query.AddAttrNode('FieldValue', 'EQUAL', orig_party)
    add_info_list = query.Select()
    
    print("\tnumber of addinfos to change: #%d" % len(add_info_list))
        
    forbidden_statuses = ('Void', 'Simulated', 'Terminated')
    for addinfo in add_info_list:
        trade = acm.FTrade[addinfo.Recaddr()]
        if trade.Status() not in forbidden_statuses \
            and trade.ArchiveStatus() == 0:
            if not dry_run:
                addinfo.FieldValue(new_party)
                addinfo.Commit()
        else:
            print("Skipping addinfo on trade %d (status=%s,archived=%d)" \
                %(trade.Oid(), trade.Status(), trade.ArchiveStatus()))
    
            
ael_variables = AelVariableHandler()
ael_variables.add("shortname",
                  label="Fund Shortname",
                  collection=sorted(SHORTNAMES),
                  hook=counterparty_name_hook)
ael_variables.add("original_cpty",
                  label="Original Counterparty Name",
                  enabled=False)
ael_variables.add_bool("dry_run",
                       label="Dry Run",
                       default=True)


def ael_main(config):
    """Entry point of the script."""
    original_cpty = config["original_cpty"]
    shortname = config["shortname"]
    dry_run = config["dry_run"]
    party = get_pb_fund_counterparty(shortname)

    # Find all tasks which require amendments
    print("TASKS:")
    all_tasks = acm.FAelTask.Select("")
    for task in all_tasks:
        if task.ModuleName() in IGNORE_MODULE_TASKS:
            continue
        if shortname in task.Name().upper():
            params = task.Parameters()
            for param in params:
                if str(param) in IGNORE_TASK_ATTRIBUTES:
                    continue
                value = params.AtString(param)
                if value == original_cpty:
                    print("\t{0}: {1}".format(task.Name(), param))
                    params.AtPutStrings(param, party.Name())
            if not dry_run:
                params.Commit()
                task.Parameters(params)
                task.Commit()

    # Find all query folders which require amendments
    print("QUERY FOLDERS:")
    all_query_folders = acm.FStoredASQLQuery.Select("")
    for query_folder in all_query_folders:
        if shortname in query_folder.Name().upper():
            for op, attr in get_query_attr_with_value(query_folder.Query(), original_cpty):
                print("\t{0}: {1}{2}".format(query_folder.Name(), "<NOT>" if op else "", attr))
                if not dry_run:
                    query = modify_asql_query(query_folder.Query(), attr, op, new_value=party.Name())
                    query_folder.Query(query)
                    query_folder.AutoUser(False)
                    query_folder.Commit()

    amend_Saxo_trades(original_cpty, party.Name(), dry_run)
