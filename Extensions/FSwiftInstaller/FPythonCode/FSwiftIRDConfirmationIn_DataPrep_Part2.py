"""----------------------------------------------------------------------------
MODULE:
    FSwiftIRDConfirmationIn_DataPrep_Part2

DESCRIPTION:
    Data preparation script for FSwiftIRDConfirmationIn
        Scripts performs following tasks:
        A. creates unidentified business process query
        B. create archive tasks
        C. create operation permissions

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSwiftMLUtils
message_types = ['MT361']
STATES = 'Matched'

def create_unidentified_bpr_query():
    for msg_type in ['MT361']:
        param = FSwiftMLUtils.Parameters('F%sIn_Config'%(msg_type))
        qName = getattr(param, 'UnpairedBPRQuery', None)
        sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(msg_type)
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

            node.AddAttrNodeEnum('AdditionalInfo.SwiftMessageType', msg_type)

            storedQuery = acm.FStoredASQLQuery()
            storedQuery.Query(query)
            storedQuery.Name(qName)
            storedQuery.AutoUser(False)
            storedQuery.User(None)
            FSwiftMLUtils.commit_and_retry(storedQuery)
            print("Created unidentified bpr query '%s'"%(qName))
        else:
            print("Query '%s' is already present"%(qName))

def run_data_prep(context=''):
    try:
        print("-"*100)
        print("Running Part-2 of Data Preps for FSwiftIRDConfirmationIn")
        print("\nStep-1")
        print("Creating Business Process Queries")
        create_unidentified_bpr_query()
        print("Creation of Business Process Queries completed")
        print("\nStep-2")
        print("Creating Archiving tasks")
        FSwiftMLUtils.create_archive_task(message_types, STATES)
        print("Creation of Archiving tasks completed")
        print("\nStep-3")
        print("Creating operation permissions")
        FSwiftMLUtils.create_operation_permissions(message_types)
        print("Creation of operation permissions completed")
        print("\n")
        print("FSwiftIRDConfirmationIn_DataPrep Part-2 is successfully executed.")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftIRDConfirmationIn DataPrep Part-2 :", str(e))


