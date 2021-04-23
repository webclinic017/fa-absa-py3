"""----------------------------------------------------------------------------
MODULE
    FSwiftCashConfirmationIn_DataPrep_Part2: Data preparation for 9XX message

DESCRIPTION
    Data preparation for 9XX message.

FUNCTION
    run_data_prep()
        Entry point for starting the execution of the data preparations.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftMLUtils
import acm
CreateOperationFlag = False
message_types = ['MT900', 'MT910', 'MT940']
STATES = 'Matched'

def create_operation_permissions():
    try:
        if CreateOperationFlag:
            operation_names = set()
            for mt_type in ['MT900', 'MT910']:
                state_chart = FSwiftMLUtils.get_state_chart_name_for_mt_type(mt_type)
                state_chart_states = FSwiftMLUtils.get_state_chart_states(state_chart)

                state_chart_derived = state_chart.replace('FSwift', 'FSwiftDerived')
                derived_state_chart_states = FSwiftMLUtils.get_state_chart_states(state_chart_derived)

                for state in state_chart_states:
                    operation_name = 'BPR_' + state_chart + '_' + state
                    operation_names.add(operation_name)

                for state in derived_state_chart_states:
                    operation_name = 'BPR_' + state_chart_derived + '_' + state
                    operation_names.add(operation_name)

            for mt_type in ['MT940', 'MT950']:
                state_chart = FSwiftMLUtils.get_state_chart_name_for_mt_type(mt_type)
                state_chart_states = FSwiftMLUtils.get_state_chart_states(state_chart)

                for state in state_chart_states:
                    operation_name = 'BPR_' + state_chart + '_' + state
                    operation_names.add(operation_name)

            for name in operation_names:
                FSwiftMLUtils.AddOperation(name)
    except Exception as err:
        print('Exception while running create_operation_permissions', str(err))

def create_unidentified_bpr_query(mt_type):
    """ Create unidentified bpr query"""
    params = []
    params.append(FSwiftMLUtils.Parameters('F%sIn_Config'%mt_type))

    for param in params:
        qName = getattr(param, 'UnpairedBPRQuery', '')
        sc = getattr(param, 'StateChart', '')
        unidentified_bpr = acm.FStoredASQLQuery[qName]

        if not unidentified_bpr:
            query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
            node = query.AddOpNode('AND')
            if FSwiftMLUtils.get_acm_version() < 2018.2:
                node.AddAttrNodeString('CurrentStep.State.StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStep.State.Name', 'Unpaired', 'EQUAL')
            else:
                node.AddAttrNodeString('StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStateName', 'Unpaired', 'EQUAL')
            node.AddAttrNodeEnum('AdditionalInfo.SwiftMessageType', mt_type)

            create_query(query, qName)
        else:
            print("Query %s is already present"%(qName))

def create_query(query, qName):
    """Creating query in ADM"""
    print("Created unidentified bpr query %s" % (qName))
    storedQuery = acm.FStoredASQLQuery()
    storedQuery.Query(query)
    storedQuery.Name(qName)
    storedQuery.AutoUser(False)
    storedQuery.User(None)
    FSwiftMLUtils.commit_and_retry(storedQuery)

def create_unidentified_parent_bpr_query_950(mt_type):
    """ Create unidentified bpr query"""

    params = []
    params.append(FSwiftMLUtils.Parameters('F%sIn_Config'%mt_type))
    for param in params:
        qName = getattr(param, 'UnpairedBPRQuery', '')
        sc = getattr(param, 'StateChart', '')
        unidentified_bpr = acm.FStoredASQLQuery[qName]

        if not unidentified_bpr:
            query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
            node = query.AddOpNode('AND')

            if FSwiftMLUtils.get_acm_version() < 2018.2:
                node.AddAttrNodeString('CurrentStep.State.StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStep.State.Name', 'RowNotMatched', 'EQUAL')
            else:
                node.AddAttrNodeString('StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStateName', 'RowNotMatched', 'EQUAL')
            node.AddAttrNodeEnum('AdditionalInfo.SwiftMessageType', mt_type)
            create_query(query, qName)
        else:
            print("Query %s is already present"%(qName))

def create_unidentified_parent_bpr_query(mt_type):
    """ Create unidentified bpr query"""

    params = []
    params.append(FSwiftMLUtils.Parameters('F%sIn_Config'%mt_type))
    for param in params:
        qName = getattr(param, 'UnpairedBPRQuery', '')
        sc = getattr(param, 'StateChart', '')
        unidentified_bpr = acm.FStoredASQLQuery[qName]

        if not unidentified_bpr:
            query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'AND')
            node = query.AddOpNode('AND')

            if FSwiftMLUtils.get_acm_version() < 2018.2:
                node.AddAttrNodeString('CurrentStep.State.StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStep.State.Name', 'CheckStatements', 'EQUAL')
            else:
                node.AddAttrNodeString('StateChart.Name', sc, 'EQUAL')
                node.AddAttrNodeString('CurrentStateName', 'CheckStatements', 'EQUAL')
            node.AddAttrNodeEnum('AdditionalInfo.SwiftMessageType', mt_type)

            create_query(query, qName)
        else:
            print("Query %s is already present"%(qName))

def run_data_prep(context=''):
    try:
        print("-"*100)
        print("Running Part-2 of Data Preps for FSwiftCashConfirmationIn")
        print("\nStep-1")
        print("Creating Business Process Queries")
        for mt_type in ['MT900', 'MT910']:
            create_unidentified_bpr_query(mt_type)

        for mt_type in ['MT940']:
            create_unidentified_parent_bpr_query(mt_type)
        for mt_type in ['MT950']:
            create_unidentified_parent_bpr_query_950(mt_type)
        print("Creation of Business Process Queries completed")
        print("\nStep-2")
        print("Creating Archiving tasks")
        FSwiftMLUtils.create_archive_task(message_types, STATES)
        print("Creation of Archiving tasks completed")
        print("\nStep-3")
        print("Creating operation permissions")
        create_operation_permissions()
        print("Creation of operation permissions completed")
        print("\n")
        print("FSwiftCashConfirmationIn_DataPrep Part-2 is successfully executed.")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftCashConfirmationIn DataPrep Part-2 :", str(e))


