"""----------------------------------------------------------------------------
MODULE:
    FSwiftFXMMConfirmationOut_DataPrep

DESCRIPTION:
    Data preparation script for FSwiftFXMMConfirmationOut
        Scripts performs following tasks:
        A. creates FX trade confirmation out state chart
        B. create archive tasks
        C. create operation permissions
        D. data preparation for external object

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FFXMMConfirmationOutSC
import FSwiftMLUtils

message_type_archive_task = ['MT300']
STATES = 'Acknowledged'
inorout = 'Out'

message_types_operation_permission = ['MT300', 'MT305', 'MT306', 'MT320', 'MT330', 'MT395']
XOBJsubType_ch_vals = [ {'name':'MT300','description':'Swift message type'},
                        {'name':'MT305','description':'Swift message type'},
                        {'name':'MT306','description':'Swift message type'},
                        {'name':'MT320','description':'Swift message type'},
                        {'name':'MT330','description':'Swift message type'},
                        {'name':'MT395','description':'Swift message type'},]
def run_data_prep(context=''):
    try:
        print(("-"*100))
        print("Running Data Prep for FSwiftFXMMConfirmationOut")
        print("\nStep-1")
        print("Creating State Charts")
        FFXMMConfirmationOutSC.create_fxMM_conf_out_sc()
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
        print("FSwiftFXMMConfirmationOut_DataPrep is successfully executed.")
        print(("-"*100))
    except Exception as e:
        print(("Exception in running FSwiftFXMMConfirmationOut DataPrep :", str(e)))

