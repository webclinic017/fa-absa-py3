"""----------------------------------------------------------------------------
MODULE:
    FMTColumnHook

DESCRIPTION:
    This module provides the functions to regulate the contents of the parameterize
    columns on the settlement/confirmation sheet.

FUNCTIONS:
          get_column_value_for_incoming_confirmation_msg() - Implementation for the incoming confirmation Swift messages.
          get_column_value_for_outgoing_confirmation_msg() - Implementation for the outgoing confirmation Swift messages.
          get_column_value_for_incoming_settlement_msg()   - Implementation for the incoming settlement Swift messages.
          get_column_value_for_outgoing_settlement_msg() - Implementation for the outgoing confirmation Swift messages.


VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
try:
    import FSwiftWriterLogger

    notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')
except Exception as e:
    import FSwiftReaderLogger

    notifier = FSwiftReaderLogger.FSwiftReaderLogger('SwiftReader', 'FSwiftReaderNotifyConfig')
import FSwiftMLUtils
import FSwiftErrorCodes


def get_bpr_details_settlement_in(bpr_list):
    """ Get bpr details for incoming settlements
    :param bpr_list: list of bprs on settlement
    :return: list of tags of the swift message on the bpr
    """
    tag_val_list = []
    for bpr in bpr_list:
        mt_msg, isderived = FSwiftMLUtils.get_generic_swift_data_from_bpr(bpr)
        if not isderived:
            tag_val_list += FSwiftMLUtils.swift_message_to_list(mt_msg)
        else:
            parent_bpr = FSwiftMLUtils.get_parent_bpr(bpr)
            mt_msg, isderived = FSwiftMLUtils.get_generic_swift_data_from_bpr(parent_bpr)
            tag_val_list = FSwiftMLUtils.swift_message_to_list(mt_msg)

    return tag_val_list


def get_details_from_bpr(bpr_list):
    """ Get dictionary of bpr id and tag value list
    :param bpr_list: list of the bpr
    :return: dict: #{bpr.Oid():(mt_type, tag_value_list)}
    """
    import FSwiftWriterAPIs
    tag_val_list = []
    mt_type = None
    bpr = None
    dict_bpr = {}
    for bpr in bpr_list:
        bpr_mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(bpr.Subject())
        if FSwiftWriterAPIs.get_swift_format_of_message(bpr_mt_type) == 'MT':
            mt_msg = FSwiftMLUtils.get_swift_data_from_bpr(bpr)
            if mt_msg:
                mt_type = FSwiftMLUtils.get_mt_type_from_swift(mt_msg)
                tag_val_list = FSwiftMLUtils.swift_message_to_list(mt_msg)
                dict_bpr[bpr.Oid()] = (mt_type, tag_val_list)
            else:
                dict_bpr[bpr.Oid()] = (None, None)
    return dict_bpr


def _get_column_value_for_outgoing_object(enum_val, bpr_list):
    """ Get value of the enum for populating into the column in GUI
    :param enum_val: enum of the tag name
    :param bpr_list: list of the bpr on current object
    :return:
    """
    try:
        tag_name, mt_type = get_tag_name(enum_val)
        if mt_type in ['MT699']:
            bpr_list = get_latest_mt699_bpr(bpr_list)

        if mt_type is None:
            if bpr_list:
                acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr_list[0])
                acm_obj_mt_type = str(FSwiftMLUtils.calculate_mt_type_from_acm_object(acm_obj))
                if str(enum_val) in ['ParentBPRState', 'ParentBPRStateChart'] :
                    ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj, msg_typ='FSwiftParent', integration_type='Outgoing')
                    if ext_obj:
                        bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(ext_obj)
                        if bpr:
                            if str(enum_val) == 'ParentBPRState':
                                return str(bpr.CurrentStateName())
                            else:
                                return str(bpr.StateChart().Name())

                if acm_obj_mt_type in ['103', '192', '199', '200', '202', '202COV', '210', '292', '299', '600', '604', '605', '620', '699']:
                    return ''

        dict_bpr = get_details_from_bpr(bpr_list)
        for bpr in bpr_list:
            ext_item = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(bpr)
            bpr_mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_item)
            if (mt_type and (bpr_mt_type == mt_type)) or not mt_type:
                if tag_name in ['ErrorText', 'BusinessProcessCurrentState', 'StateChart', 'NackStatusCode', 'NackStatus']:
                    if not dict_bpr:
                        bpr_text = handle_bpr_text(tag_name, bpr)
                    else:
                        bpr_text = handle_bprs_text(dict_bpr, mt_type, tag_name)
                    if bpr_text is not None:
                        return bpr_text
                    
        tag_name_final = ''
        for mt_type_frm_bpr, swift_msg_list in list(dict_bpr.values()):
            if swift_msg_list:
                for tags in swift_msg_list:
                    if tag_name == tags[0]:
                        tag_name_final += tags[1] + '; '
        return tag_name_final[:-2] if tag_name_final else ''
    except Exception as e:
        return "Error occurred while processing _get_column_value_for_outgoing_object: %s" % str(e)



def handle_bprs_text(dict_bpr, mt_type, tag_name):
    """ tag_name : tag_name provided by user on column to be fetched Ex: StateChart
    mt_type : In case user specifies the tag_name for specific MT_TYPE like MT103:StateChart, then mt_type will be MT103
    :param dict_bpr: dictionary of bpr id and tag value list
    :param mt_type: MT message type
    :param tag_name: name of the swift tag
    :return:
    """
    import acm
    bpr_text = ''
    for bpr_id, mttype_tagvalue in dict_bpr.items():
        bpr = acm.FBusinessProcess[bpr_id]
        mt_type_from_dict, tag_value_list = mttype_tagvalue
        text = handle_bpr_text(tag_name, bpr)
        if mt_type_from_dict and mt_type and mt_type_from_dict == mt_type:
            bpr_text = bpr_text + text + '; '
            break
        if not mt_type and text:
            bpr_text = bpr_text + text + '; '
    return bpr_text[:-2] if bpr_text else ''


def handle_bpr_text(tag, bpr):
    """ Get bpr name as text
    :param tag: name of the tag
    :param bpr: bpr of to check tag on
    :return: str: name of the state chart or error
    """
    if bpr:
        if 'ErrorText' == tag:
            params = bpr.CurrentStep().DiaryEntry().Parameters()
            if params.HasKey('Error'):
                return str(params['Error'])
            elif params.HasKey('Error1'):
                return str(params['Error1'])
        elif tag in ['BusinessProcessCurrentState', 'DerivedBusinessProcessCurrentState']:
            return bpr.CurrentStep().State().Name()
        elif tag in ['StateChart', 'DerivedStateChart']:
            return bpr.StateChart().Name()
        elif tag == 'NackStatus':
            params = bpr.CurrentStep().DiaryEntry().Parameters()
            if params.HasKey('error_desc'):
                return str(params['error_desc'])
        elif tag == 'NackStatusCode':
            params = bpr.CurrentStep().DiaryEntry().Parameters()
            if params.HasKey('error_code'):
                return str(params['error_code'])
        
    return None


def get_tag_name(tags):
    """ Get tag name when using tag on specific MT type.
    possible values of tags MT548:StateChart
    MT548:25D_Status
    MT103:StateChart or MT202COV:BusinessProcessCurrentState
    :param tags: tag name
    :return: tag name
    """
    tag_list = tags.split('_', 1)
    tag_mt_list = tag_list[0].split(':')
    if  len(tag_mt_list ) > 1:
        mt_type = tag_mt_list[0]
        tag = tag_mt_list[1]
        return tag, mt_type
    else:
        return tag_mt_list[0], None


'''---------------------------------------------------------------------------------------
   Modify or Provide your implementation to control the values on the columns for
   incoming Swift confirmation messages.e.g. MT300, MT305, MT320, MT330
   ---------------------------------------------------------------------------------------'''


def get_column_value_for_incoming_confirmation_msg(enum_val, bpr_list):
    """ Get value of the enum for populating incoming confirmation message column in GUI
        :param enum_val: enum value of the column
        :param bpr_list: list of bpr on settlement object
        :return: tag value
    """
    try:
        dict_bpr = get_details_from_bpr(bpr_list) #{bpr.Oid():(mt_type, tag_value_list)}
        tag_name, mt_type = get_tag_name(enum_val)
        if tag_name in ['ErrorText', 'BusinessProcessCurrentState', \
                        'DerivedBusinessProcessCurrentState', 'StateChart', 'DerivedStateChart']:
            bpr_text = handle_bprs_text(dict_bpr, mt_type, tag_name)
            if bpr_text is not None:
                return bpr_text

        tag_name_final = ''
        for mt_type_frm_bpr, swift_msg_list in list(dict_bpr.values()):
            if mt_type and mt_type_frm_bpr and mt_type == mt_type_frm_bpr:
                for tags in swift_msg_list:
                    if tag_name == tags[0]:
                        tag_name_final += tags[1] + '; '
            if not mt_type and swift_msg_list:
                for tags in swift_msg_list:
                    if tag_name == tags[0]:
                        tag_name_final += tags[1] + '; '

        return tag_name_final[:-2] if tag_name_final else ''
    except Exception as e:
        return "Error occurred while processing get_column_value_for_incoming_confirmation_msg: %s" % str(e)


'''---------------------------------------------------------------------------------------
   Modify or Provide your implementation to control the values on the columns for
   incoming Swift confirmation messages.e.g. MT300, MT305
   ---------------------------------------------------------------------------------------'''


def get_latest_mt699_bpr(bpr_list):
    """ Get latest bpr from multiple MT699 bpr.
    :param bpr_list: List of bpr on the acm object
    :return: list: latest bpr of mt699
    """
    for bpr in bpr_list:
        acm_obj = FSwiftMLUtils.get_acm_object_from_bpr(bpr)
        external_object_for_699 = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj=acm_obj,
                                                                                         integration_type='Outgoing',
                                                                                         msg_typ='MT699')
        if external_object_for_699:
            latest_bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(
                external_object_for_699)
            bpr_list = [latest_bpr]
            break
    return bpr_list


def get_column_value_for_outgoing_confirmation_msg(enum_val, bpr_list):
    """ Get value of the enum for populating confirmation column in GUI
    :param enum_val: enum value of the column
    :param bpr_list: list of bpr on confirmation object
    :return: tag value
    """
    return _get_column_value_for_outgoing_object(enum_val, bpr_list)


'''---------------------------------------------------------------------------------------
   Modify or Provide your implementation to control the values on the columns for
   incoming Swift settlement messages.e.g. MT544-MT547, MT900
   ---------------------------------------------------------------------------------------'''


def get_column_value_for_incoming_settlement_msg(enum_val, bpr_list):
    """ Get value of the enum for populating incoming settlement message column in GUI
        :param enum_val: enum value of the column
        :param bpr_list: list of bpr on settlement object
        :return: tag value
    """
    try:
        swift_msg_list = get_bpr_details_settlement_in(bpr_list)
        tag_name, mt_type = get_tag_name(enum_val)
        bpr_text = None

        tag_name_final = ''
        for tags in swift_msg_list:
            if tag_name == tags[0]:
                tag_name_final += tags[1] + ', '

        if tag_name == '24B':
            tag_name_final = get_value_for_reason_desc(swift_msg_list, tag_name_final[:-2])
            return tag_name_final
        if tag_name == '70D':
            if 'EROR' in tag_name_final:
                error_code = tag_name_final[-6:-2]
                return "(%s) %s" % (error_code, FSwiftErrorCodes.get_error_reason_from_code(error_code))
            else:
                return ''
        if tag_name == '25D':
            return tag_name_final[-6:-2]
        if tag_name == '70E':
            if 'AFFI' in tag_name_final:
                return 'AFFI'
            elif 'NAFI' in tag_name_final:
                return 'NAFI'
        if tag_name_final:
            return tag_name_final[:-2]

        for bpr in bpr_list:
            bpr_mt_type = bpr.AdditionalInfo().SwiftMessageType()

            if bpr_mt_type in ['MT544', 'MT545', 'MT546', 'MT547', 'MT548'] and mt_type is None:
                return ''

            if mt_type is not None:
                if bpr_mt_type in ['MT544', 'MT545', 'MT546', 'MT547']:
                    bpr_mt_type = 'MT54X'
                if bpr_mt_type == mt_type:
                    bpr_text = handle_bpr_text(tag_name, bpr)
                    break
            else:
                dummy_var, isderived = FSwiftMLUtils.get_generic_swift_data_from_bpr(bpr)
                if isderived:
                    if 'derived'.upper() in tag_name.upper():
                        bpr_text = handle_bpr_text(tag_name, bpr)
                        break
                else:
                    if 'derived'.upper() not in tag_name.upper():
                        bpr_text = handle_bpr_text(tag_name, bpr)
                        break

        if bpr_text is not None:
            return bpr_text
    except Exception as e:
        return "Error occurred while processing get_column_value_for_incoming_settlement_msg: %s" % str(e)


def get_value_for_reason_desc(swift_msg_list, qualifier):
    for tags in swift_msg_list:
        if tags[0] == '24B':
            tag_values = tags[1].split('/')
            qualifier = tag_values[0]
            reason_code = tag_values[-1]
            qualifier = qualifier.strip(':')
            desc = FSwiftMLUtils.get_reason_codes_desc(qualifier, reason_code)
            return desc


'''---------------------------------------------------------------------------------------
   Modify or Provide your implementation to control the values on the columns for
   outgoing Swift settlement messages.e.g. MT540-MT543, MT210, MT103
   ---------------------------------------------------------------------------------------'''


def get_column_value_for_outgoing_settlement_msg(enum_val, bpr_list):
    """ Get value of the enum for populating settlement column in GUI
        :param enum_val: enum value of the column
        :param bpr_list: list of bpr on settlement object
        :return: tag value
    """
    val = []
    for bpr in bpr_list:
        mt_msg, isderived = FSwiftMLUtils.get_generic_swift_data_from_bpr(bpr)
        swift_msg_list = FSwiftMLUtils.swift_message_to_list(mt_msg, 'MT598_130')
        tag, code = enum_val.split('_')
        tag_name_final = ''
        for tags in swift_msg_list:
            if tag == tags[0]:
                if tag == '79':
                    tag_lines = tags[1].split('\n')
                    for each in tag_lines:
                        if code in each:
                            tag_name_final += each
                else:
                    tag_name_final += tags[1]
        if tag_name_final:
            val.append(tag_name_final)
    return val
