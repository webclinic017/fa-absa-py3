"""
    If there is a heavy load on the ATS:es, then it is possible to increase                                                                             
    the performance by using multiple ATS:es. The code in this module is meant
    to show examples on how to write hooks if muliple ATS:es are needed.

    The examples in this module shows how to add dedicated documentation ATS:es
    for Settlements.

    To use the examples in this module the following prerequisites must be met:
    * One dedicated AMBA for Settlements. The AMBA .ini file must include
        the hook modify_outgoing_amba_message and the module containing the
        hook:
        -ael_module_name SettlementAMBAHook
        -ael_sender_modify modify_outgoing_amba_message

        Note:
        For general use it is not required to have one dedicated AMBA for
        Settlements and one AMBA for settlements. The only case this is required
        is when using the settlement hook SettlementEvent. The examples in this
        module are based on that the SettlementEvent hook is used and that there
        is a dedicated AMBA for Settlements and one for settlements.

    * One Settlement ATS.
    * At least one documentation ATS dedicated for Settlements.
    * Each documentation ATS must override the parameters receiverName and
        receiverMBName in the configuration files. Example:
        Doc ATS 1:
        -task_parameters receiverMBName doc_conf_RECEIVER_1;receiverSource doc_settlement_1
        Doc ATS 2:
        -task_parameters receiverMBName doc_conf_RECEIVER_2;receiverSource doc_settlement_2
        Doc ATS 3:
        -task_parameters receiverMBName doc_conf_RECEIVER_3;receiverSource doc_settlement_3
    * The receiverSource for the documentation ATS:es must be based on a common
        string which the ATS number will be added to.
        Example: The following ATS:es share a common base source: "doc_settlement_"
        Doc ATS 1:  doc_settlement_1
        Doc ATS 2:  doc_settlement_2
        Doc ATS 3:  doc_settlement_3
        ...


    There are two important parameters in this file:
    NUMBER_OF_DOC_ATSES:    This is the number of documentation ATS:es that
                            will be used.
    BASE_SOURCE:            This is the string that all documentation ATS:es
                            share. It is also this string that will be used
                            to create the receiver sources for the different
                            documentation ATS:es.

    Example:
    Setting the parameters to the following values:
    NUMBER_OF_DOC_ATSES = 3
    BASE_SOURCE = "doc_settlement_"
    means that you will be using 3 documentation ATS:es and they will have
    the receiver sources:
    doc_settlement_1
    doc_settlement_2
    doc_settlement_3

    Important: These receiver sources should map to the receiver sources
    overridden in the .ini files for the doc ATS:es.

    This module uses round robin for assigning tasks between the doc ATS:es by using
    modulo calculations. The doc ATS is assigned in the following way:
    Doc ATS = (trade oid % NUMBER_OF_DOC_ATSES) + 1  
-------------------------------------------------------------------------------------------------------------------------------

HISTORY
===============================================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------------------------
2019-05-15      Upgrade2018     Jaysen Naicker          Make sure receiver source names are cast to strings to prevent 
                                                        amba from crashing
-------------------------------------------------------------------------------------------------------------------------------
"""
import FDocumentationParameters

NUMBER_OF_DOC_ATSES = 5
BASE_SOURCE = FDocumentationParameters.receiverSourceStlmBase


def modify_outgoing_amba_message(amba_message, subject):
    event_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type_as_string = event_type.mbf_get_value()
    result_tuple = (amba_message, subject)
    print 'current', result_tuple
    if (event_type_as_string == 'INSERT_SETTLEMENT' or
          event_type_as_string == 'UPDATE_SETTLEMENT'):
        print 'splitting load'
        senderSource = filter_on_trade(amba_message)
        #Anwar - prod hotfix for lost messages that dont have a sendersource
        if senderSource == "":
            senderSource = str(get_ats_source(1))
        print 'updated', senderSource
        subject = senderSource + subject[subject.index("/"):]
        result_tuple = (amba_message, subject)

    return result_tuple


def filter_on_trade(amba_message):
    sender_source = ""
    settlement = object_by_name(amba_message, ['', '+', '!'], 'SETTLEMENT')
    if settlement:
        sender_source = filter_on_trade_helper(settlement, NUMBER_OF_DOC_ATSES)

    return sender_source

def filter_on_trade_helper(settlement, number_of_doc_atses):
    sender_source = ""
    if settlement and number_of_doc_atses > 0:
        trade_nbr = settlement.mbf_find_object('TRDNBR')
        if trade_nbr:
            ats_number = (int(trade_nbr.mbf_get_value()) % number_of_doc_atses) + 1
            sender_source = str(get_ats_source(ats_number))
    return sender_source

def objects_by_name(parent_obj, name_prefixes, name):
    obj = parent_obj.mbf_first_object()
    names = list()
    for name_prefix in name_prefixes:
        names.append(name_prefix + name)
    while obj:
        if obj.mbf_get_name() in names:
            yield obj
        obj = parent_obj.mbf_next_object()


def object_by_name(parent_obj, name_prefixes, name):
    for obj in objects_by_name(parent_obj, name_prefixes, name):
        return obj
    return None

def get_ats_source(ats_number):
    return str(BASE_SOURCE + str(ats_number))
