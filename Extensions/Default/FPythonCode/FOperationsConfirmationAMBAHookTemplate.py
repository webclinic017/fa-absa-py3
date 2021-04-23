""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/templates/FOperationsConfirmationAMBAHookTemplate.py"
"""
    If there is a heavy load on the ATS:es, then it is possible to increase
    the performance by using multiple ATS:es. The code in this module is meant
    to show examples on how to write hooks if muliple ATS:es are needed.

    The examples in this module shows how to add dedicated documentation ATS:es
    for confirmations.

    To use the examples in this module the following prerequisites must be met:
    * One dedicated AMBA for confirmations. The AMBA .ini file must include
        the hook modify_outgoing_amba_message and the module containing the
        hook:
        -ael_module_name ConfirmationAMBAHook
        -ael_sender_modify modify_outgoing_amba_message

        Note:
        For general use it is not required to have one dedicated AMBA for
        confirmations and one AMBA for settlements. The only case this is required
        is when using the settlement hook ConfirmationEvent. The examples in this
        module are based on that the ConfirmationEvent hook is used and that there
        is a dedicated AMBA for confirmations and one for settlements.

    * One confirmation ATS.
    * At least one documentation ATS dedicated for confirmations.
    * Each documentation ATS must override the parameters receiverName and
        receiverMBName in the configuration files. Example:
        Doc ATS 1:
        -task_parameters receiverMBName doc_conf_RECEIVER_1;receiverSource doc_confirmation_1
        Doc ATS 2:
        -task_parameters receiverMBName doc_conf_RECEIVER_2;receiverSource doc_confirmation_2
        Doc ATS 3:
        -task_parameters receiverMBName doc_conf_RECEIVER_3;receiverSource doc_confirmation_3
    * The receiverSource for the documentation ATS:es must be based on a common
        string which the ATS number will be added to.
        Example: The following ATS:es share a common base source: "doc_confirmation_"
        Doc ATS 1:  doc_confirmation_1
        Doc ATS 2:  doc_confirmation_2
        Doc ATS 3:  doc_confirmation_3
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
    BASE_SOURCE = "doc_confirmation_"
    means that you will be using 3 documentation ATS:es and they will have
    the receiver sources:
    doc_confirmation_1
    doc_confirmation_2
    doc_confirmation_3

    Important: These receiver sources should map to the receiver sources
    overridden in the .ini files for the doc ATS:es.

    There are three modes in this file:
    MODE_TRADE:
    Uses round robin for assigning tasks between the doc ATS:es by using
    modulo calculations. The doc ATS is assigned in the following way:
    Doc ATS = (trade oid % NUMBER_OF_DOC_ATSES) + 1

    MODE_SPECIFIC_TEMPLATES:
    In this mode the doc ATS with the highest number will be dedicated for
    confirmations whose template's are included in the list TEMPLATES_LIST.
    The rests of the doc ATS:es will handle all other confirmations.
    Example:
    TEMPLATES_LIST = ["Front_FXOpen", "SWIFT"]
    doc_confirmation_1:     will use round robin based on trade
    doc_confirmation_2:     will use round robin based on trade
    doc_confirmation_3:     will handle all confirmations with templates
                            Front_FXOpen or SWIFT.



    DISCLAIMER:
    The hooks in this module are EXAMPLES on how one could setup multiple
    ATS:es, not suggestions. To get optimal results the bottlenecks must be
    identified because different needs requires different setups and hooks.

"""

NUMBER_OF_DOC_ATSES     = 2
BASE_SOURCE             = "doc_confirmation_bodev415_"

#Parameter used by mode MODE_SPECIFIC_TEMPLATES
TEMPLATES_LIST          = ["Front_FXOpen", "SWIFT"]

#Parameters for deciding the mode to run
MODE_TRADE              = 1
MODE_SPECIFIC_TEMPLATES = 2


#Set the MODE parameter to either MODE_TRADE, MODE_SWIFT or MODE_SPECIFIC_TEMPLATES
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

    if (event_type_as_string == 'INSERT_CONFIRMATION' or
          event_type_as_string == 'UPDATE_CONFIRMATION'):
        senderSource = filter_function(amba_message)
        subject = senderSource + subject[subject.index("/"):]
        result_tuple = (amba_message, subject)
    elif (event_type_as_string == 'INSERT_OPERATIONSDOCUMENT' or
          event_type_as_string == 'UPDATE_OPERATIONSDOCUMENT'):
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
    sender_source = ""
    if confirmation and number_of_doc_atses > 0:
        trade_nbr = confirmation.mbf_find_object('TRDNBR')
        if trade_nbr:
            ats_number = (int(trade_nbr.mbf_get_value()) % number_of_doc_atses) + 1
            sender_source = get_ats_source(ats_number)

    return sender_source

def filter_on_specific_templates(amba_message):
    sender_source = ""
    confirmation = object_by_name(amba_message, ['', '+', '!'], 'CONFIRMATION')
    if confirmation and NUMBER_OF_DOC_ATSES >= 1:
        template_obj = confirmation.mbf_find_object('CONF_TEMPLATE_CHLNBR.ENTRY')
        if template_obj and template_obj.mbf_get_value() in TEMPLATES_LIST:
            sender_source = get_ats_source(NUMBER_OF_DOC_ATSES)
        else:
            if NUMBER_OF_DOC_ATSES == 1:
                sender_source = get_ats_source(NUMBER_OF_DOC_ATSES)
            else:
                #the rest of ats:es will use round robin
                #to process all other confirmations
                sender_source = filter_on_trade_helper(confirmation, NUMBER_OF_DOC_ATSES-1)

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
    return BASE_SOURCE + str(ats_number)




