'''----------------------------------------------------------------------------------------------------------------------------
MODULE                  :       ConfirmationAMBAHook
PURPOSE                 :       Contains Confirmation AMBA hook functions

-------------------------------------------------------------------------------------------------------------------------------

HISTORY
===============================================================================================================================
Date            Change no       Developer               Description
-------------------------------------------------------------------------------------------------------------------------------
2016-04-11      CHNG0003588948  Lawrence Mucheka        Initial Implementation -
                                                        Based on FOperationsConfirmationAMBAHookTemplate
2016-07-28      CHNG0003871835  Gabriel Marko           Use 1 thread for PDFs and 4 for SWIFTs
2017-12-07      CHNG0005212519  Willie van der Bank     Modifying the above mentioned change so that Swift confirmations are
                                                        processed by 1 dedicated ATS and PDFs split amongst the remaining 4
2019-05-15      Upgrade2018     Jaysen Naicker          Make sure receiver source names are cast to strings to prevent 
                                                        amba from crashing
-------------------------------------------------------------------------------------------------------------------------------
'''

import FDocumentationParameters

NUMBER_OF_DOC_ATSES     = 5
BASE_SOURCE = FDocumentationParameters.receiverSourceConfBase

#Parameter used by mode MODE_SPECIFIC_TEMPLATES
TEMPLATES_LIST          = ["Front_FXOpen", "SWIFT"]

#Parameters for deciding the mode to run
MODE_TRADE              = 1
MODE_SPECIFIC_TEMPLATES = 2


# Set the MODE parameter to either: MODE_TRADE, MODE_SWIFT or MODE_SPECIFIC_TEMPLATES
MODE = MODE_TRADE


def modify_outgoing_amba_message(amba_message, subject):
    result_tuple = (amba_message, subject)

    if MODE == MODE_TRADE:
        result_tuple = perform_filtering(amba_message, subject, filter_on_trade)
    elif MODE == MODE_SPECIFIC_TEMPLATES:
        result_tuple = perform_filtering(amba_message, subject, filter_on_specific_templates)

    return result_tuple


def perform_filtering(amba_message, subject, filter_function):

    event_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type_as_string = event_type.mbf_get_value()
    result_tuple = (amba_message, subject)

    if event_type_as_string in ('INSERT_CONFIRMATION', 'UPDATE_CONFIRMATION'):
        senderSource = filter_function(amba_message)
        subject = senderSource + subject[subject.index("/"):]
        result_tuple = (amba_message, subject)
    elif event_type_as_string in ('INSERT_OPERATIONSDOCUMENT', 'UPDATE_OPERATIONSDOCUMENT'):
        if not opdoc_is_confirmation(amba_message):
            result_tuple = None

    return result_tuple


def filter_on_trade(amba_message):
    sender_source = ""
    confirmation = object_by_name(amba_message, ['', '+', '!'], 'CONFIRMATION')
    if confirmation:
        sender_source = filter_on_trade_helper(confirmation, NUMBER_OF_DOC_ATSES)
    return sender_source



def filter_on_trade_helper(confirmation, number_of_doc_atses):
    sender_source = 1

    if confirmation and number_of_doc_atses > 0:
        trade_nbr = confirmation.mbf_find_object('TRDNBR')
        if trade_nbr:

            # for Swifts use the first ATS
            # the rest of the ATSes will use round robin
            # to process all other confirmations
            transport_type = confirmation.mbf_find_object('TRANSPORT')
            if transport_type is not None:
                transport_value = transport_type.mbf_get_value()

                swift_ats = 1
                swift_confo_transport_values = ('TRANSPORT_TYPE_EMAIL', 'Network')

                if transport_value in swift_confo_transport_values:
                    # use first ats for Swifts
                    sender_source = swift_ats
                else:
                    ats_number = (int(trade_nbr.mbf_get_value()) % (number_of_doc_atses - swift_ats)) + (swift_ats + 1)
                    sender_source = ats_number

    return str(get_ats_source(sender_source))

def filter_on_specific_templates(amba_message):
    sender_source = ""
    confirmation = object_by_name(amba_message, ['', '+', '!'], 'CONFIRMATION')

    if confirmation and NUMBER_OF_DOC_ATSES >= 1:
        template_obj = confirmation.mbf_find_object('CONF_TEMPLATE_CHLNBR.ENTRY')

        if template_obj and template_obj.mbf_get_value() in TEMPLATES_LIST:
            sender_source = str(get_ats_source(NUMBER_OF_DOC_ATSES))
        else:
            if NUMBER_OF_DOC_ATSES == 1:
                sender_source = str(get_ats_source(NUMBER_OF_DOC_ATSES))
            else:
                # for PDFs use the first ATS
                # the rest of ATSes will use round robin
                # to process all other confirmations
                sender_source = filter_on_trade_helper(
                    confirmation,
                    NUMBER_OF_DOC_ATSES
                )

    return sender_source


def opdoc_is_confirmation(amba_message):
    is_confirmation = False
    opdoc_obj = object_by_name(amba_message, ['', '+', '!'], 'OPERATIONSDOCUMENT')
    if opdoc_obj:
        confirmation_seqnbr_obj = opdoc_obj.mbf_find_object("CONFIRMATION_SEQNBR")
        if confirmation_seqnbr_obj:
            if int(confirmation_seqnbr_obj.mbf_get_value()) > 0:
                is_confirmation = True
    return is_confirmation


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
