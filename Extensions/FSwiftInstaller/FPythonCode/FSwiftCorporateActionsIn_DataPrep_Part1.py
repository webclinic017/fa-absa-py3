"""----------------------------------------------------------------------------
MODULE:
    FSwiftCorporateActionsIn_DataPrep_Part1

DESCRIPTION:
    Data preparation script for FCorporateAction
    Scripts performs following tasks:
    A. creates corporate action state chart
    B. create choice lists and add infos
    C. create columns

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FCorporateActionsInSC
import FSwiftMLUtils
import FExternalObject
import FIntegrationUtils
import os

XOBJsubType_ch_vals = [{'name':'MT564','description':'Swift message type'}]

def adm_prepare_corp_actions():
    """ Create additional infos/Choice list required for corporate actions"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States
    # This will referenced by additional info with name same as state chart on
    # acm object

    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        #FSwiftMLUtils.create_choice_list(state_choice_list, FSwiftMLUtils.get_state_chart_states(sc))
        swift_message_typ = [{'name':'MT564','description':'Swift message type'}]

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
        print("Exception in adm_prepare_corp_actions : %s"%str(e))

def run_data_prep(context=''):
    try:
        print("-"*100)
        print("Running Part-1 of Data Preps for FSwiftCorporateActionsIn")
        print("\nStep-1")
        print("Creating State Charts")
        FCorporateActionsInSC.create_corporate_action_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Additional Infos/Choice list")
        adm_prepare_corp_actions()
        print("Additional Infos/Choice list creation completed")
        print("\nStep-3")
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\nStep-4")
        print('Creating columns')
        FSwiftMLUtils.create_columns(os.path.basename(__file__), context)
        print("Creation of Columns completed")
        print("\n")
        print("FSwiftCorporateActionsIn_DataPrep Part-1 is successfully executed.")
        print("\n")
        print("Please restart Prime application before running FSwiftCorporateActionsIn_DataPrep Part 2")
        print("-"*100)
    except Exception as e:
        print("Exception in running FSwiftCorporateActionsIn DataPrep Part-1:", str(e))

