"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecuritySettleInstrIn_DataPrep_Part1

DESCRIPTION:
    Data preparation script for SecSettlementInstrIn
    Script performs following tasks:
    A. creates security settlement confirmation state chart
    B. create choice list and add infos
    C. data preparation for FExternal Object
    D. create columns

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSecuritySettlementInstructionInSC
import FSwiftMLUtils
import FExternalObject
import FIntegrationUtils
import os

XOBJsubType_ch_vals = [{'name':'MT540','description':'Swift message type'},
                            {'name':'MT541','description':'Swift message type'},
                            {'name':'MT542','description':'Swift message type'},
                            {'name':'MT543','description':'Swift message type'},]

def adm_prepare_security_sett_conf():
    """ Create additional infos/Choice list required for Security Settlement Conf"""
    # Create choice list for possible values in additional info. Choice list will
    # have name as <state_chart_name>States

    try:
        utils_obj = FIntegrationUtils.FIntegrationUtils()

        swift_message_typ = [{'name':'MT540','description':'Swift message type'},
                            {'name':'MT541','description':'Swift message type'},
                            {'name':'MT542','description':'Swift message type'},
                            {'name':'MT543','description':'Swift message type'},]


        try:
            # Create ChoiceList for all SwiftMessageTypes
            for vals in swift_message_typ:
                try:
                    utils_obj.create_choice_list('SwiftMessageType', [vals])
                except FIntegrationUtils.ChoiceListAlreadyExist, e:
                    print "Choice List <%s> already exists"%(vals['name'])
        except Exception, e:
            print "Exception in create choice list: %s"%str(e)

        try:
            FSwiftMLUtils.create_add_info()
        except Exception, e:
            print "Exception in create Additional Info specification : %s"%str(e)
    except Exception, e:
        print "Exception in adm_prepare_security_sett_conf : %s"%str(e)

def run_data_prep(context=''):
    try:
        print "-"*100
        print "Running Part-1 of Data Preps for FSwiftSecuritySettleInstrIn"
        print "\nStep-1"
        print "Creating State Charts"
        FSecuritySettlementInstructionInSC.create_security_settlment_conf_sc()
        print "State Chart creation completed."
        print "\nStep-2"
        print "Creating Additional Infos/Choice list"
        adm_prepare_security_sett_conf()
        print "Additional Infos/Choice list creation completed"
        print "\nStep-3"
        print "Data preparation for FExternal Object"
        FSwiftMLUtils.adm_prepare_ext_object(XOBJsubType_ch_vals)
        print "Data preparation for FExternal Object completed"
        print "\nStep-4"
        print 'Creating columns'
        FSwiftMLUtils.create_columns(os.path.basename(__file__), context)
        print "Creation of Columns completed"
        print "\n"
        print "FSwiftSecuritySettleInstrIn_DataPrep Part-1 is successfully executed."
        print "\n"
        print "Please restart Prime application before running FSwiftSecuritySettleInstrIn_DataPrep Part 2"
        print "-"*100
    except Exception, e:
        print "Exception in running FSwiftSecuritySettleInstrIn DataPrep Part-1:", str(e)


