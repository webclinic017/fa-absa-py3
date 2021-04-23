"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecuritySettlementOut_DataPrep

DESCRIPTION:
    Data preparation script for SecuritySettlementOut
    Script performs following tasks:
    A. creates security settlement confirmation out state chart
    B. create archive tasks
    C. create operation permissions
    D. data preparation for FExternal object

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSecuritySettlementOutSC
import FSwiftMLUtils

message_type_archive_task = ['MT540']
STATES = 'Acknowledged'
inorout = 'Out'

message_types_operation_permission = ['MT540', 'MT541', 'MT542', 'MT543', 'MT518']
XOBJsubType_ch_vals = [ {'name':'MT540', 'description':'Swift message type'},
                        {'name':'MT541', 'description':'Swift message type'},
                        {'name':'MT542', 'description':'Swift message type'},
                        {'name':'MT543', 'description':'Swift message type'},
                        {'name':'MT518', 'description':'Swift message type'},]

def run_data_prep(context=''):
    try:
        print(("-"*100))
        print("Running Data Prep for FSwiftSecuritySettlementOut")
        print("\nStep-1")
        print("Creating State Charts")
        FSecuritySettlementOutSC.create_sec_settlement_conf_out_sc()
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
        print("Data preparation for FExternal Object")
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print("Data preparation for FExternal Object completed")
        print("\n")
        print("FSwiftSecuritySettlementOut_DataPrep is successfully executed.")
        print(("-"*100))
    except Exception as e:
        print(("Exception in running FSwiftSecuritySettlementOut DataPrep:", str(e)))

