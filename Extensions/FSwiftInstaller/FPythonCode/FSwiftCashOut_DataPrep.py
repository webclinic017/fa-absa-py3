"""----------------------------------------------------------------------------
MODULE
    FSwiftCashOut_DataPrep: Data preparation for cash message

DESCRIPTION
    Data preparation for cash message.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FCashOutSC
import FSwiftMLUtils
import FIntegrationUtils

message_type_archive_task = ['MT202']
STATES = 'Acknowledged'
inorout = 'Out'

message_types_operation_permission = ['MT103', 'MT192', 'MT199', 'MT200', 'MT202', 'MT210', 'MT292', 'MT299', 'MT304']
XOBJsubType_ch_vals = [ {'name':'MT103', 'description':'Swift message type'},
                        {'name':'MT192', 'description':'Swift message type'},
                        {'name':'MT199', 'description':'Swift message type'},
                        {'name':'MT200', 'description':'Swift message type'},
                        {'name':'MT202', 'description':'Swift message type'},
                        {'name':'MT210', 'description':'Swift message type'},
                        {'name':'MT292', 'description':'Swift message type'},
                        {'name':'MT299', 'description':'Swift message type'},
                        {'name':'MT304', 'description': 'Swift message type'}]

def create_additional_info():
    add_info_spec_swift_message_type = {
                                'FieldName':'GPI Identifier',
                                'Description':'GPI Id ',
                                'Default':'',
                                'TypeGroup':'Standard',
                                'Type':'String',
                                'Table':'Account'
                                }

    add_info_spec_swift_message_type_TradChinese = {
                                'FieldName':'TraditionalChinese',
                                'Description':'Use Traditional Chinese',
                                'Default':'',
                                'TypeGroup':'Standard',
                                'Type':'Boolean',
                                'Table':'Party'
                                }

    add_info_spec_use_extended_x_chars = {
        'FieldName': 'SWIFTExtXChrNotUsed',
        'Description': 'Extended X Character Set Not Supported',
        'Default': 'No',
        'TypeGroup': 'Standard',
        'Type': 'Boolean',
        'Table': 'Party'
    }
    add_info_spec_third_party_fx = {

    }
    additional_infos = [add_info_spec_swift_message_type, add_info_spec_swift_message_type_TradChinese, add_info_spec_use_extended_x_chars]
    for each in additional_infos:
        try:
            FIntegrationUtils.FIntegrationUtils().create_additional_info_spec(each)
        except FIntegrationUtils.AddInfoSpecAlreadyExits as e:
            print(("Additional Info <%s> already exists on table <%s>"%(each['FieldName'], each['Table'])))

def create_choicelists():
    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()
        third_party_fx_details = {'name': 'ThirdPartyFX', 'description': 'Deal - Third party FX'}
        utils_obj.create_choice_list('TradeSettleCategory', [third_party_fx_details])
    except FIntegrationUtils.ChoiceListAlreadyExist as e:
        print(("ChoiceList <%s> already exists"%third_party_fx_details['name']))
    except Exception as e:
        print(("Exception while creating Choice List <%s>"%third_party_fx_details['name']))

def run_data_prep(context=''):
    try:
        print(("-"*100))
        print("Running Data Prep for FSwiftCashOut")
        print("\nStep-1")
        print("Creating State Charts")
        FCashOutSC.create_cash_settlement_conf_out_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Archiving tasks")
        FSwiftMLUtils.create_archive_task(message_type_archive_task, STATES, inorout)
        print("Creation of Archiving tasks completed")
        print("\nStep-3")
        print("Creating Additional Info")
        create_additional_info()
        print("Creation of Additional Info completed")
        print("\nStep-4")
        print("Creating choice list")
        create_choicelists()
        print("Creation of choice list completed")
        print("\nStep-5")
        print("Creating operation permissions")
        FSwiftMLUtils.create_operation_permissions(message_types_operation_permission, inorout)
        print("Creation of operation permissions completed")
        print("\nStep-6")
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\n")
        print("FSwiftCashOut_DataPrep is successfully executed.")
        print(("-"*100))
    except Exception as e:
        print(("Exception in running FSwiftCashOut DataPrep :", str(e)))


