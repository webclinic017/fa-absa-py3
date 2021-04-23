"""----------------------------------------------------------------------------
MODULE:
    FSwiftFXMMConfirmationIn_DataPrep_Part1

DESCRIPTION:
    Data preparation script for FSwiftFXMMConfirmationIn
        Scripts performs following tasks:
        A. creates FX trade confirmation state chart
        B. create choice lists and add infos
        C. create eligibility query
        d. create columns

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FFXMMConfirmationInSC
import FSwiftMLUtils
import FExternalObject
import FIntegrationUtils
import os

XOBJsubType_ch_vals = [{'name':'MT300','description':'Swift message type'},
                       {'name':'MT305','description':'Swift message type'},
                       {'name':'MT320','description':'Swift message type'},
                       {'name':'MT330','description':'Swift message type'},
                       {'name':'MT399','description':'Swift message type'}]

SUPPORTED_MSG_TYPE = ['MT300', 'MT305', 'MT320', 'MT330']


def create_narrative_eligibility_query(msg_type='MT399'):
    for msg_type in ['MT399']:
        param = FSwiftMLUtils.Parameters('F%sIn_Config' % (msg_type))
        qNames = FSwiftMLUtils.string_as_list(getattr(param, 'EligibilityQuery', None))
        for each_query_name in qNames:
            eligibility_query = acm.FStoredASQLQuery[each_query_name]

            if not eligibility_query:
                query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
                node = query.AddOpNode('AND')
                node.AddAttrNodeEnum('Status', ['Pending Matching', 'Matched', 'Acknowledged'])

                '''Type should not be Cancellation'''
                node.AddAttrNodeEnum('Type', 'Cancellation').Not(True)
                node = query.AddOpNode('OR')
                for each in SUPPORTED_MSG_TYPE:
                    node.AddAttrNodeNumerical('Documents.SwiftMessageType', each.replace('MT', ''),
                        each.replace('MT', ''))

                storedQuery = acm.FStoredASQLQuery()
                storedQuery.Query(query)
                storedQuery.Name(each_query_name)
                storedQuery.AutoUser(False)
                storedQuery.User(None)
                FSwiftMLUtils.commit_and_retry(storedQuery)
                print("Created eligibility query '%s'" % (each_query_name))
            else:
                print("Query '%s' is already present" % (each_query_name))


def create_eligibility_query():
    for msg_type in ['MT300', 'MT305', 'MT320', 'MT330']:
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


def adm_prepare_fx_trade_conf():
    """ Create additional infos/Choice list required for FSwiftFXMMConfirmationIn"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States
    # This will referenced by additional info with name same as state chart on
    # acm object
    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        swift_message_typ = [
                                   {'name':'MT300','description':'Swift message type'},
                                   {'name':'MT305','description':'Swift message type'},
                                   {'name':'MT320','description':'Swift message type'},
                                   {'name':'MT330','description':'Swift message type'},
                                    {'name': 'MT399', 'description': 'Swift message type'}
                                   ]

        for vals in swift_message_typ:
            try:
                utils_obj.create_choice_list('SwiftMessageType', [vals])
            except FIntegrationUtils.ChoiceListAlreadyExist as e:
                print("Choice List <%s> already exists"%(vals['name']))

        try:
            FSwiftMLUtils.create_add_info()
        except Exception as e:
            print("Exception in create Additional Info specification : %s"%str(e))


    except Exception as e:
        print("Exception in adm_prepare_fx_trade_conf : %s"%str(e))

def run_data_prep(context=''):
    try:
        print("-"*100)
        print("Running Part-1 of Data Preps for FSwiftFXMMConfirmationIn")
        print("\nStep-1")
        print("Creating State Charts")
        FFXMMConfirmationInSC.create_fx_trade_conf_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Additional Infos/Choice list")
        adm_prepare_fx_trade_conf()
        print("Additional Infos/Choice list creation completed")
        print("\nStep-3")
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\nStep-4")
        print("Creating Eligibility Query")
        create_eligibility_query()
        create_narrative_eligibility_query()
        print("Creation of Eligibility Query completed")
        print("\nStep-5")
        print("Creating Columns")
        FSwiftMLUtils.create_columns(os.path.basename(__file__), context)
        print("Creation of Columns completed")
        print("\n")
        print("FSwiftFXMMConfirmationIn_DataPrep Part-1 is successfully executed.")
        print("\n")
        print("Please restart Prime application before running FSwiftFXMMConfirmationIn_DataPrep Part 2")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftFXMMConfirmationIn DataPrep Part-1:", str(e))



