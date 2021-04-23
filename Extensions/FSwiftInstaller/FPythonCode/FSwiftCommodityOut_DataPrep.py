"""----------------------------------------------------------------------------
MODULE:
    FSwiftCommodityOut_DataPrep

DESCRIPTION:
    Data preparation script for FSwiftCommoditySettlementOut, FSwiftCommodityConfirmationOut
        Scripts performs following tasks:
        A. Creates Commodity confirmation state chart
        B. Creates Archiving Tasks
        C. Create Operations permissions
     Note:
        Make sure that FSwiftSolutionBase and FSwiftCommodity extension modules are present
        in extension manager.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FCommodityConfirmationOutSC
import FCommoditySettlementOutSC
import FIntegrationUtils
import FSwiftMLUtils

STATES = 'Acknowledged'
inorout = 'Out'

def adm_prepare_status_message():
    """ Create additional infos/Choice list required for Statsu messages"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States
    # This will referenced by additional info with name same as state chart on
    # acm object
    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        cmdty_delivery_details =   [{'name':'CFR',	'description':'Cost and Freight'},
                                    {'name':'CIF',	'description':'Cost, Insurance, and Freight'},
                                    {'name':'CIP',	'description':'Carriage and Insurance Paid'},
                                    {'name':'CPT',	'description':'Carriage Paid To'},
                                    {'name':'DAF',	'description':'Delivered At Frontier'},
                                    {'name':'DDP',	'description':'Delivered Duty Paid'},
                                    {'name':'DDU',	'description':'Delivered Duty Unpaid'},
                                    {'name':'DEQ',	'description':'Delivered Ex Quay'},
                                    {'name':'DES',	'description':'Delivered Ex Ship'},
                                    {'name':'DTD',	'description':'Door To Door'},
                                    {'name':'EXW',	'description':'EX Works'},
                                    {'name':'FAS',	'description':'Free Alongside Ship'},
                                    {'name':'FCA',	'description':'Free Carrier'},
                                    {'name':'FOB',	'description':'Free On Board'},
                                    {'name':'LOC',	'description':'LOCO London'},
                                    {'name':'OTH',	'description':'Other'}
                                    ]

        # Create ChoiceList for all Commodity Delivery Details
        for vals in cmdty_delivery_details:
            try:
                utils_obj.create_choice_list('CmdtyDlvryDtls', [vals])
            except FIntegrationUtils.ChoiceListAlreadyExist as e:
                print(("Choice List <%s> already exists" % (vals['name'])))
            except Exception as e:
                print(("Exception in creating Choice List : %s" % str(e)))

        add_info_spec_cmdty_dlvry_dtls = {
            'FieldName': 'CommodityDlvryDtls',
            'Description': 'CmdtyDlvryDtls',
            'Default': '',
            'TypeGroup': 'RecordRef',
            'Type': 'ChoiceList',
            'Table': 'Trade',
        }

        add_info_spec_cmdty_alloc_dtls = {
                                'FieldName':'CommodityAllocated',
                                'Description':'Commodity Allocated',
                                'Default':'',
                                'TypeGroup':'Standard',
                                'Type':'Boolean',
                                'Table':'Trade'
                                }

        FSwiftMLUtils.create_add_info()

        for each in [add_info_spec_cmdty_dlvry_dtls, add_info_spec_cmdty_alloc_dtls]:
            try:
                utils_obj.create_additional_info_spec(each)
            except FIntegrationUtils.AddInfoSpecAlreadyExits as e:
                print(("Additional Info <%s> already exists on table <%s>"%(each['FieldName'], each['Table'])))
            except Exception as e:
                print(("Exception in creating Additional info : %s"%str(e)))

    except Exception as e:
        print(("Exception in adm_prepare_security_sett_conf : %s"%str(e)))

def run_data_prep_confirmtion(context=''):
    """ run the data prep for confirmations"""
    try:
        message_types_operation_permission = ['MT600', 'MT699', 'MT620']
        message_type_archive_task = ['MT600', 'MT699', 'MT620']
        print(("-"*100))
        print("Running Data Prep for FSwiftCommodityConfirmationOut")
        print("\nStep-1")
        print("Creating State Charts")
        FCommodityConfirmationOutSC.create_commodity_conf_out_sc()
        FCommodityConfirmationOutSC.create_free_format_out_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Archiving tasks")
        FSwiftMLUtils.create_archive_task(message_type_archive_task, STATES, inorout)
        print("Creation of Archiving tasks completed")
        print("\nStep-3")
        print("Creating operation permissions")
        FSwiftMLUtils.create_operation_permissions(message_types_operation_permission, inorout)
        print("Creation of operation permissions completed")
        print("\nStep-4")
        print("Creating Additional Infos/Choice list")
        adm_prepare_status_message()
        print("Creation of Additional Infos/Choice completed")
        print("\n")
        print("FSwiftCommodityConfirmationOut_DataPrep is successfully executed.")
        print(("-"*100))
    except Exception as e:
        print(("Exception in running FSwiftCommodityConfirmationOut DataPrep :", str(e)))

def run_data_prep_settlement(context = ''):
    """ run the data prep for settlements"""
    try:
        message_type_archive_task = ['MT604', 'MT605']
        message_types_operation_permission = ['MT604', 'MT605']
        print(("-"*100))
        print("Running Data Prep for FSwiftCommoditySettlementOut")
        print("\nStep-1")
        print("Creating State Charts")
        FCommoditySettlementOutSC.create_commodity_sett_out_sc()
        FCommoditySettlementOutSC.create_free_format_out_sc()
        print("State Chart creation completed.")
        print("\nStep-2")
        print("Creating Archiving tasks")
        FSwiftMLUtils.create_archive_task(message_type_archive_task, STATES, inorout)
        print("Creation of Archiving tasks completed")
        print("\nStep-3")
        print("Creating operation permissions")
        FSwiftMLUtils.create_operation_permissions(message_types_operation_permission, inorout)
        print("Creation of operation permissions completed")
        print("\n")
        print("FSwiftCommoditySettlementOut_DataPrep is successfully executed.")
        print(("-"*100))
    except Exception as e:
        print(("Exception in running FSwiftCommoditySettlementOut DataPrep :", str(e)))

def run_data_prep(context = ''):
    """ run the data preps"""
    run_data_prep_confirmtion(context)
    run_data_prep_settlement(context)


