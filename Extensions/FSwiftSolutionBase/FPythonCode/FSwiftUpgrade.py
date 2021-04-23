"""----------------------------------------------------------------------------
MODULE:
    FSwiftUpgrade

DESCRIPTION:
    This script upgrades needed adm data across versions.
    e.g. addInfo spec changes

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import re

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SwiftReader', 'FSwiftReaderNotifyConfig')
from FExternalObject import FExternalObject
import FSwiftMLUtils
import FIntegrationUtils
def upgrade():
    """ adm changes for fx trade and security settlement confirmations"""
    upgarde_fx_trade_conf_msg()
    upgarde_sec_settlement_conf_msg()

def upgarde_fx_trade_conf_msg():
    """ adm changes for fx trade confimations"""
    try:
        import FFXTradeConfMsgMain
    except Exception as e:
        return

    try:
        # Populate the swift message type add info
        FSwiftMLUtils.populate_swift_msg_type_on_bpr(['300', '305'])

        sc = FSwiftMLUtils.get_state_chart_name_for_mt_type('MT300')
        state_choice_list = sc + 'States'
        FSwiftMLUtils.create_choice_list(state_choice_list, FSwiftMLUtils.get_state_chart_states(sc))

        add_info_name = FSwiftMLUtils.get_add_info_name_for_mt_type('MT300')
        add_info_spec = {'FieldName': add_info_name,
                         'Description': state_choice_list,
                         'Default': '',
                         'TypeGroup': 'RecordRef',
                         'Type': 'ChoiceList',
                         'Table': 'Confirmation',
                        }
        new_add_info_spec = acm.FAdditionalInfoSpec[add_info_spec['FieldName']]
        if new_add_info_spec is None:
            FSwiftMLUtils.update_additional_info_spec('FxTradeConfBPRState', add_info_spec)
            print('Updated additional info spec %s on table %s'%(add_info_spec['FieldName'], add_info_spec['Table']))
        FSwiftMLUtils.update_additional_info_spec('FXTradeConfMsg', add_info_spec)
        print('Updated additional info spec %s on table %s'%(add_info_spec['FieldName'], add_info_spec['Table']))
        #populate_swift_msg_type_on_ext_obj('Confirmation')
        update_swift_data(['MT300', 'MT305'])
    except Exception as e:
        print("Exception in upgarde_fx_trade_conf_msg : %s"%str(e))

def upgarde_sec_settlement_conf_msg():
    """ adm changes for security settlement confirmations"""
    try:
        import FSecuritySettlementInMain
    except Exception as e:
        return

    try:
        # Populate the swift message type add info
        FSwiftMLUtils.populate_swift_msg_type_on_bpr(['544', '545', '546', '547'])

        sc = FSwiftMLUtils.get_state_chart_name_for_mt_type('MT544')
        state_choice_list = sc + 'States'
        FSwiftMLUtils.create_choice_list(state_choice_list, FSwiftMLUtils.get_state_chart_states(sc))
        add_info_name = FSwiftMLUtils.get_add_info_name_for_mt_type('MT544')

        add_info_spec = {'FieldName': add_info_name,
                         'Description': state_choice_list,
                         'Default': '',
                         'TypeGroup': 'RecordRef',
                         'Type': 'ChoiceList',
                         'Table': 'Settlement',
                        }
        new_add_info_spec = acm.FAdditionalInfoSpec[add_info_spec['FieldName']]
        if new_add_info_spec is None:
            FSwiftMLUtils.update_additional_info_spec('SecSettConfBPRState', add_info_spec)
            print('Updated additional info spec %s on table %s'%(add_info_spec['FieldName'], add_info_spec['Table']))
        FSwiftMLUtils.update_additional_info_spec('SecuritySettlementC', add_info_spec)
        print('Updated additional info spec %s on table %s'%(add_info_spec['FieldName'], add_info_spec['Table']))
        #populate_swift_msg_type_on_ext_obj('Settlement')
        update_swift_data(['MT544', 'MT545', 'MT546', 'MT547'])
    except Exception as e:
        print("Exception in upgarde_sec_settlement_conf_msg : %s"%str(e))

def populate_swift_msg_type_on_bpr(old_msg_types):  #One time use - move it to upgrade script
    """ Populate additional info SwiftMessageType on bpr with type stored in Subject_subtype"""
    uitls_obj = FIntegrationUtils.FIntegrationUtils()
    for msg_type in old_msg_types:
        new_msg_type = 'MT' + msg_type
        # Change the bpr subject subtype to add prefix MT
        bp_select = acm.FBusinessProcess.Select("subject_subtype = %d" % int(msg_type))
        for bp in list(bp_select):
            try:
                uitls_obj.set_additional_info('SwiftMessageType', bp, new_msg_type)
            except AddInfoSpecNotExist as e:
                notifier.ERROR(str(e))
            except Exception as e:
                notifier.ERROR(str(e))
            bp.Subject_subtype(0)
            FSwiftMLUtils.commit_and_retry(bp)
            notifier.INFO('Setting SwiftMessageType to %s for bp %d'%(new_msg_type, bp.Oid()))

        # Change the add info XOBJsubType to add prefix MT
        ai_select = acm.FAdditionalInfo.Select("fieldValue = '%s' and addInf = '%s'" %(msg_type, 'XOBJsubType'))
        for ai in list(ai_select):
            FSwiftMLUtils.update_addtional_info(ai, new_msg_type)
            notifier.INFO('Setting XOBJsubType to %s for additional info %d'%(new_msg_type, ai.Oid()))

def update_swift_data(mt_types):
    """ update the swift dat to store values as per schema"""
    try:
        for mt_type in mt_types:
            ext_objs = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = acm_object, integration_type = 'Outgoing', msg_typ = mt_type)
            #ext_objs = FExternalObject.ExtReferences(subtype=mt_type)
            for ext_obj in ext_objs:
                ext_data = ext_obj.Data()
                if ext_data:
                    swift_data = ext_data['swift_data']
                    if swift_data:
                        swift_data = modify_swift_data(swift_data)
                        value_dict = acm.FDictionary()
                        value_dict['swift_data'] = swift_data
                        ext_obj.Data(value_dict)
                        FSwiftMLUtils.commit_and_retry(ext_obj)
                        notifier.INFO('Modified external object %d'%(ext_obj.Oid()))
    except Exception as e:
        notifier.ERROR("Exception in update_swift_data : %s"%str(e))
        notifier.DEBUG(str(e), exc_info=1)

def modify_swift_data(swift_data):
    """ modify swift data"""
    SWIFT_TAGS = ['36B', '19A', '32B', '34R', '34P', '36', '33B', '37K']
    for tag in SWIFT_TAGS:
        for (search_str) in re.findall( r':%s:(.*)\n'%(tag), swift_data, re.M|re.I):
            swift_data = swift_data.replace(search_str, search_str.replace('.', ','))
    return swift_data

def populate_swift_msg_type_on_ext_obj(subject_type):
    """ Populate additional info on external object"""
    try:
        ext_objs = FExternalObject.ExtReferences(subjectType=subject_type)
        for ext_obj in ext_objs:
            rItem = ext_obj.ReconciliationItem()
            print('Processing external object %d'%(rItem.Oid()))
            swift_data = FSwiftMLUtils.get_external_value_using_ael(rItem).At('swift_data')
            mt_type = FSwiftMLUtils.get_mt_type_from_swift(swift_data)
            if not ext_obj.SubType():
                ext_obj.SubType(mt_type)
                print('  Updating external object %d with sub type %s'%(ext_obj.Oid(), ext_obj.SubType()))
            if not ext_obj.ExtType():
                ext_obj.ExtType('SWIFT15022')
                print('  Updating external object %d with ext type %s'%(ext_obj.Oid(), ext_obj.ExtType()))
            if not ext_obj.StorageType():
                ext_obj.StorageType('FDictionary')
                print('  Updating external object %d with storage type %s'%(ext_obj.Oid(), ext_obj.StorageType()))
            if not ext_obj.Source():
                ext_obj.Source('AMB')
                print('  Updating external object %d with soruce type %s'%(ext_obj.Oid(), ext_obj.Source()))
            if not ext_obj.Data():
                value_dict = acm.FDictionary()
                value_dict['swift_data'] = swift_data
                ext_obj.Data(value_dict)
                print('  Updating external object %d with Data %s'%(ext_obj.Oid(), ext_obj.Data()))
            FSwiftMLUtils.commit_and_retry(ext_obj)
    except Exception as e:
        print(e)
