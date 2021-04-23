"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecuritySettlementIn_DataPrep_Part1

DESCRIPTION:
    Data preparation script for SecuritySettlement
    Script performs following tasks:
    A. create security settlement confirmation state chart
    B. create choice list and add infos
    C. data preaparation for FExternal object
    D. create eligibility query
    E. create columns

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSecuritySettlementInSC
import FSwiftMLUtils
import FExternalObject
import FIntegrationUtils
import os

XOBJsubType_ch_vals = [{'name':'MT518','description':'Swift message type'},
                            {'name':'MT535','description':'Swift message type'},
                            {'name':'MT544','description':'Swift message type'},
                            {'name':'MT545','description':'Swift message type'},
                            {'name':'MT546','description':'Swift message type'},
                            {'name':'MT547','description':'Swift message type'},
                            {'name':'MT548','description':'Swift message type'},
                       ]

def create_unidentified_bpr_query():
    """ Create unidentified bpr query"""
    for msg_type in ['MT544', 'MT545', 'MT546', 'MT547', 'MT518']:
        param = FSwiftMLUtils.Parameters('F%sIn_Config'%(msg_type))
        #param = FSwiftMLUtils.Parameters('F%s_Config' % (msg_type))
        qName = getattr(param, 'UnpairedBPRQuery', '')
        #qName = getattr(param, 'F%s_UnpairedBPRQuery' % (msg_type), '')
        print('Creating query', qName)
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
            print("Created unidentified bpr query %s"%(qName))
        else:
            print("Query %s is already present"%(qName))


def create_eligibility_query():
    for msg_type in [('MT544', 'MT540'), ('MT545', 'MT541'), ('MT546', 'MT542'), ('MT547', 'MT543')]:
        param = FSwiftMLUtils.Parameters('F%sIn_Config'%(msg_type[0]))
        qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', ''))
        #qNames = FSwiftMLUtils.string_as_list(getattr(param, 'F%s_EligibilityQuery'%(msg_type[0]), ''))
        for each_query_name in qNames:
            eligibility_query = acm.FStoredASQLQuery[each_query_name]

            if not eligibility_query:
                query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
                node = query.AddOpNode('AND')
                node.AddAttrNodeNumerical('Documents.SwiftMessageType', msg_type[1].replace('MT', ''), msg_type[1].replace('MT', ''))
                node.AddAttrNodeEnum('Status', 'Acknowledged')

                storedQuery = acm.FStoredASQLQuery()
                storedQuery.Query(query)
                storedQuery.Name(each_query_name)
                storedQuery.AutoUser(False)
                storedQuery.User(None)
                FSwiftMLUtils.commit_and_retry(storedQuery)
                print("Created eligibility query '%s'"%(each_query_name))
            else:
                print("Query '%s' is already present"%(each_query_name))


    for msg_type in ['MT518']:
        param = FSwiftMLUtils.Parameters('F%sIn_Config'%(msg_type))
        qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', None))
        for each_query_name in qNames:
            eligibility_query = acm.FStoredASQLQuery[each_query_name]

            if not eligibility_query:
                query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
                node = query.AddOpNode('AND')
                node.AddAttrNodeNumerical('Documents.SwiftMessageType', msg_type.replace('MT', ''), msg_type.replace('MT', ''))
                node.AddAttrNodeEnum('Status', 'Pending Matching')
                '''Type should not be Cancellation'''
                node.AddAttrNodeEnum('Type', 'Cancellation').Not(True)

                storedQuery = acm.FStoredASQLQuery()
                storedQuery.Query(query)
                storedQuery.Name(each_query_name)
                storedQuery.AutoUser(False)
                storedQuery.User(None)
                FSwiftMLUtils.commit_and_retry(storedQuery)
                print("Created eligibility query '%s'"%(each_query_name))
            else:
                print("Query '%s' is already present"%(each_query_name))

    '''
    for msg_type in [('SESE025', 'SESE023')]:
        param = FSwiftMLUtils.Parameters('F%sIn_Config'%(msg_type[0]))
        qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', ''))
        #qNames = FSwiftMLUtils.string_as_list(getattr(param, 'F%s_EligibilityQuery'%(msg_type[0]), ''))
        for each_query_name in qNames:
            eligibility_query = acm.FStoredASQLQuery[each_query_name]

            if not eligibility_query:
                query = acm.CreateFASQLQuery(acm.FSettlement,'AND')
                node = query.AddOpNode('AND')
                node.AddAttrNodeNumerical('Documents.SwiftMessageType', msg_type[1].replace('SESE0', ''), msg_type[1].replace('SESE0', ''))
                node.AddAttrNodeEnum('Status', 'Acknowledged')

                storedQuery = acm.FStoredASQLQuery()
                storedQuery.Query(query)
                storedQuery.Name(each_query_name)
                storedQuery.AutoUser(False)
                storedQuery.User(None)
                FSwiftMLUtils.commit_and_retry(storedQuery)
                print("Created eligibility query '%s'"%(each_query_name))
            else:
                print("Query '%s' is already present"%(each_query_name))
    '''


def adm_prepare_security_sett_conf():
    """ Create additional infos/Choice list required for Security Settlement Conf"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States
    # This will referenced by additional info with name same as state chart on
    # acm object

    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        swift_message_typ = [{'name':'MT518','description':'Swift message type'},
                            {'name':'MT535','description':'Swift message type'},
                            {'name':'MT544','description':'Swift message type'},
                            {'name':'MT545','description':'Swift message type'},
                            {'name':'MT546','description':'Swift message type'},
                            {'name':'MT547','description':'Swift message type'},
                            {'name': 'MT548', 'description': 'Swift message type'},
                             ]



        try:
            # Create ChoiceList for all SwiftMessageTypes
            for vals in swift_message_typ:
                try:
                    utils_obj.create_choice_list('SwiftMessageType', [vals])
                except FIntegrationUtils.ChoiceListAlreadyExist as e:
                    print("Choice List <%s> already exists"%(vals['name']))
        except Exception as e:
            print("Exception in create choice list: %s"%str(e))

        try:
            FSwiftMLUtils.create_add_info()
        except Exception as e:
            print("Exception in create Additional Info specification : %s"%str(e))


    except Exception as e:
        print("Exception in adm_prepare_security_sett_conf : %s"%str(e))

def run_data_prep(context=''):
    try :
        print("-"*100)
        print("Running Part-1 of Data Preps for FSwiftSecuritySettlementIn")
        print("\nStep-1")
        print("Creating State Charts")
        FSecuritySettlementInSC.create_security_settlment_conf_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Additional Infos/Choice list")
        adm_prepare_security_sett_conf()
        print("Additional Infos/Choice list creation completed")
        print("\nStep-3")
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\nStep-4")
        print("Creating Eligibility Query")
        create_eligibility_query()
        print("Creation of Eligibility Query completed")
        print("\nStep-5")
        print("Creating Columns")
        FSwiftMLUtils.create_columns(os.path.basename(__file__), context)
        print("Creation of Columns completed")
        print("\n")
        print("FSwiftSecuritySettlementIn_DataPrep Part-1 is successfully executed.")
        print("\n")
        print("Please restart Prime application before running FSwiftSecuritySettlementIn_DataPrep Part 2")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftSecuritySettlementIn DataPrep Part-1:", str(e))



