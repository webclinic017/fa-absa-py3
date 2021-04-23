"""----------------------------------------------------------------------------
MODULE:
    FFreeFormatUtils

DESCRIPTION:
    A module for common functions used across Free Format messages.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
    1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
    2. This module is not customizable.
    3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftWriterUtils
import FSwiftMLUtils

writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

def get_sequence_number(settlement):
    """ Get the sequence number for the Settlement
    :return:
    """
    seq_number = ''
    if settlement:
        seq_number = settlement.Oid()
    return seq_number


def get_settlement_reference_prefix():
    """ Method to get settlement reference prefix to be sent in the MT message. """
    cash_settlement_out_config = FSwiftWriterUtils.get_config_from_fparameter('FCashOut_Config')
    if str(getattr(cash_settlement_out_config, 'FAS', "")) == "":
        return str(getattr(writer_config, 'FAS', "FAS"))
    return str(getattr(cash_settlement_out_config, 'FAS', None))


def get_message_version_number(fObject, is_free_text_msg = False, child_mt_type=''):
    """ Method to get the message version number
    :param fObject: object from which message version number is to be fetched
    :param is_free_text_msg: flag indicating is_free_text_msg
    :return: message version number
    """
    msg_version_number = fObject.VersionId()
    if is_free_text_msg:
        msg_version_number = str(msg_version_number) + 'F'
        if child_mt_type and child_mt_type == 'MT103':
            msg_version_number = str(msg_version_number) + 'O'
        elif child_mt_type and child_mt_type == 'MT199':
            msg_version_number = str(msg_version_number) + 'F'
    return str(msg_version_number)


def get_corresponding_mt_type_of_canc_paygood(acm_obj, swift_message_type, canc_or_paygood):
    """ Method to get corresponding MT Type in case of the canc or paygood scenarios
    :param acm_obj: settlement object
    :param swift_message_type: MT type from parent settlement line
    :param canc_or_paygood: flag indicating whether its a cancellation or paygoodvalue scenario
    :return:
    """
    msg_typ = FSwiftWriterUtils.get_mt_type_from_acm_obj(acm_obj.Children()[-1])
    try :
        import FCashOutMain
        dict = FCashOutMain.message_type_and_corresponding_messages.get(msg_typ)
        if dict: #{'103':['199','192'],'202COV':['299','292']}
            parent_msg_type = str(swift_message_type)[2:]
            for child_msg_type, (paygood, canc) in dict.items():
                if ("canc" == canc_or_paygood and canc == parent_msg_type) or ("paygood" == canc_or_paygood and paygood == parent_msg_type):
                    msg_typ = child_msg_type
                    return msg_typ
                else:
                    return msg_typ
    except Exception as e:
        notifier.WARN('Exception in method get_corresponding_mt_type_of_canc_paygood: {}'.format(e))
    return msg_typ


def get_narrative_description(settlement, mt_type=None):
    """ Optional field 79 for n92 Settlement.
    :param settlement: settlement object
    :param mt_type: message type
    :return: narrative description
    """
    narrative_description = ''
    if mt_type in ['MT199', 'MT299']:
        ccy = settlement.Currency().Name()
        amount = str(abs(settlement.Amount()))
        value_date = settlement.ValueDay()
        original_value_day = settlement.Children()[-1].ValueDay()
        related_ref = "%s-%s-%s" % (str(get_settlement_reference_prefix()), str(settlement.Oid()), str(get_message_version_number(settlement)))
        narrative_description = """TODAY WE HAVE SENT YOU A PAYMENT INSTRUCTION UNDER REFERENCE {0} FOR {1} {2} WITH VALUE DATE {3}.WITH REGARDS TO THIS PAYMENT WE HEREBY INSTRUCT YOU TO ARRANGE A BACKVALUATION FROM VALUE DATE {3} TO VALUE DATE {4}.""".format(related_ref, ccy, amount, value_date, original_value_day)
    else:
        if is_cancellation(settlement):
            related_settlement = get_related_settlement(settlement)
            narrative_description = 'Settlement Id %s was due to %s' % (related_settlement.Oid(), related_settlement.ValueDay())
        elif is_nak_cancellation(settlement):
            narrative_description = 'Cancelling previous MT%s' % (get_original_message_type(settlement))

    return narrative_description

