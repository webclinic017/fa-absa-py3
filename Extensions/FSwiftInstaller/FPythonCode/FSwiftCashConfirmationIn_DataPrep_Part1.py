"""----------------------------------------------------------------------------
MODULE
    FSwiftCashConfirmationIn_DataPrep_Part1: Data preparation for 9XX message

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
import FCashConfirmationInSC
import FSwiftMLUtils
import FExternalObject
import FIntegrationUtils
import acm
import os

ONE_TRILLION = 1000000000000

XOBJsubType_ch_vals = [{'name':'MT900','description':'Swift message type'},
                       {'name':'MT910','description':'Swift message type'},
                       {'name':'MT940','description':'Swift message type'},
                       {'name':'MT950','description':'Swift message type'}]

def create_parent_eligibility_query(mt_type):
    params = []
    params.append(FSwiftMLUtils.Parameters('F%sInPairingView'%mt_type))

    for param in params:
        qNames = FSwiftMLUtils.string_as_list(getattr(param, 'AcmObjQueryDerived', ''))
        for each_query_name in qNames:
            eligibility_query = acm.FStoredASQLQuery[each_query_name]
            if not eligibility_query:
                query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
                node = query.AddOpNode('AND')
                node.AddAttrNodeString('CounterpartyAccountNetworkName', 'SWIFT', 'EQUAL')
                node.AddAttrNodeEnum('Status', 'Acknowledged')
                node.AddAttrNodeNumerical('CreateTime', '-1w', '0d')
                create_query(query, each_query_name)
            else:
                print("Query '%s' is already present"%(each_query_name))

def create_eligibility_query_with_status(mt_type, param, status):
    qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', ''))
    for each_query_name in qNames:
        eligibility_query = acm.FStoredASQLQuery[each_query_name]
        if not eligibility_query:
            query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
            node = query.AddOpNode('AND')
            node.AddAttrNodeString('CounterpartyAccountNetworkName', 'SWIFT', 'EQUAL')
            node.AddAttrNodeEnum('Status', status)

            if mt_type == 'MT910':
                fromAmt = 0
                toAmt = ONE_TRILLION
            elif mt_type == 'MT900':
                fromAmt = -1*ONE_TRILLION
                toAmt = 0

            node.AddAttrNodeNumerical('Amount', fromAmt, toAmt)
            node.AddAttrNodeNumerical('CreateTime', '-1w', '0d')
            create_query(query, each_query_name)
        else:
            print("Query '%s' is already present"%(each_query_name))

def create_eligibility_query_with_status_950(mt_type):
    """Create eligibility query for MT950"""
    param = FSwiftMLUtils.Parameters('F%sDerivedIn_Config' % mt_type)
    qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', ''))
    for each_query_name in qNames:
        eligibility_query = acm.FStoredASQLQuery[each_query_name]
        if not eligibility_query:
            query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
            node = query.AddOpNode('AND')
            node.AddAttrNodeString('CounterpartyAccountNetworkName', 'SWIFT', 'EQUAL')
            node.AddAttrNodeEnum('Status', ['Pending Closure', 'Acknowledged'])


            node = query.AddOpNode('OR')
            for each in ['MT202', 'MT210']:
                node.AddAttrNodeNumerical('Documents.SwiftMessageType', each.replace('MT', ''), each.replace('MT', ''))
            create_query(query, each_query_name)
        else:
            print("Query '%s' is already present"%(each_query_name))

def create_query(query, query_name):
    """Creating query in ADM"""
    storedQuery = acm.FStoredASQLQuery()
    storedQuery.Query(query)
    storedQuery.Name(query_name)
    storedQuery.AutoUser(False)
    storedQuery.User(None)
    FSwiftMLUtils.commit_and_retry(storedQuery)
    print("Created eligibility query '%s'" % (query_name))

def create_eligibility_query(mt_type):
    create_eligibility_query_with_status(mt_type, FSwiftMLUtils.Parameters('F%sIn_Config'%mt_type), 'Authorised')
    create_eligibility_query_with_status(mt_type, FSwiftMLUtils.Parameters('F%sDerivedIn_Config'%mt_type), 'Acknowledged')

def adm_prepare_status_message():
    """ Create additional infos/Choice list required for Statsu messages"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States
    # This will referenced by additional info with name same as state chart on
    # acm object
    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        swift_message_typ = [
                                {'name':'MT900','description':'Swift message type'},
                                {'name':'MT910','description':'Swift message type'},
                                {'name':'MT940','description':'Swift message type'},
                                {'name': 'MT950', 'description': 'Swift message type'},
                                {'name': 'MT950Derived', 'description': 'Swift message type'}
                            ]

        try:
            # Create ChoiceList for all SwiftMessageTypes
            for vals in swift_message_typ:
                try:
                    utils_obj.create_choice_list('SwiftMessageType', [vals])
                except FIntegrationUtils.ChoiceListAlreadyExist as e:
                    print("Choice List <%s> already exists"%(vals['name']))
        except Exception as e:
            print("Exception in creating Choice List : %s"%str(e))

        add_info_spec_swift_message_type_TradChinese = {
                                'FieldName':'TraditionalChinese',
                                'Description':'Use Traditional Chinese',
                                'Default':'',
                                'TypeGroup':'Standard',
                                'Type':'Boolean',
                                'Table':'Party'
                                }

        try:
            FSwiftMLUtils.create_add_info()
            additional_infos = [add_info_spec_swift_message_type_TradChinese]
            for each in additional_infos:
                try:
                    utils_obj.create_additional_info_spec(each)
                except FIntegrationUtils.AddInfoSpecAlreadyExits as e:
                    print("Additional Info <%s> already exists on table <%s>"%(each['FieldName'], each['Table']))
        except Exception as e:
            print("Exception in creating Additional info : %s"%str(e))

    except Exception as e:
        print("Exception in adm_prepare_security_sett_conf : %s"%str(e))


def run_data_prep(context=''):
    try :
        print("-"*100)
        print("Running Part-1 of Data Preps for FSwiftCashConfirmationIn")
        print("\nStep-1")
        print("Creating State Charts")
        FCashConfirmationInSC.create_9XX_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\nStep-3")
        print("Creating Additional Infos/Choice list")
        adm_prepare_status_message()
        print("Additional Infos/Choice list creation completed")
        print("\nStep-4")
        print("Creating Eligibility Query")
        for mt_type in ['MT900', 'MT910']:
            create_eligibility_query(mt_type)
        create_eligibility_query_with_status_950('MT950' )
        print("Creation of Eligibility Query completed")
        print("\nStep-5")
        print("Creating Columns")
        FSwiftMLUtils.create_columns(os.path.basename(__file__), context)
        print("Creation of Columns completed")
        print("\n")
        print("FSwiftCashConfirmationIn_DataPrep Part-1 is successfully executed.")
        print("\n")
        print("Please restart Prime application before running FSwiftCashConfirmationIn_DataPrep Part 2")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftCashConfirmationIn DataPrep Part-1:", str(e))


