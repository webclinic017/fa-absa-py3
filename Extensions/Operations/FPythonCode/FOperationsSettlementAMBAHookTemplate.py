""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/templates/FOperationsSettlementAMBAHookTemplate.py"
"""
    If there is a heavy load on the ATS:es, then it is possible to increase
    the performance by using multiple ATS:es. The code in this module is meant
    to show examples on how to write hooks if muliple ATS:es are needed.

    The examples in this module shows how to add dedicated documentation ATS:es
    for settlements.

    To use the examples in this module the following prerequisites must be met:
    * One dedicated AMBA for settlements. The AMBA .ini file must include
        the hook modify_outgoing_amba_message and the module containing the
        hook:
        -ael_module_name SettlementAMBAHook
        -ael_sender_modify modify_outgoing_amba_message

        Note:
        For general use it is not required to have one dedicated AMBA for
        settlements and one AMBA for confirmations. The only case this is required
        is when using the settlement hook ConfirmationEvent. The examples in this
        module are based on that the ConfirmationEvent hook is used and that there
        is a dedicated AMBA for settlements and one for confirmations.

    * One settlement ATS.
    * At least one documentation ATS dedicated for settlements.
    * Each documentation ATS must override the parameters receiverSource and
        receiverMBName in the configuration files. Example:
        Doc ATS 1:
        -task_parameters receiverMBName doc_settlement_RECEIVER_1;receiverSource doc_settlement_1
        Doc ATS 2:
        -task_parameters receiverMBName doc_settlement_RECEIVER_2;receiverSource doc_settlement_2
        Doc ATS 3:
        -task_parameters receiverMBName doc_settlement_RECEIVER_3;receiverSource doc_settlement_3
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

    There are two modes in this file:
    MODE_TRADE:
    Uses round robin for assigning tasks between the doc ATS:es by using modulo
    calculations. The doc ATS is assigned in the following way:
    Doc ATS = (trade oid % NUMBER_OF_DOC_ATSES) + 1
    If there is no trade reference the oid of the settlement is used instead.


    MODE_AMOUNT_COUNTERPARTY:
    In this mode the doc ATS with the highest number will be dedicated to
    handle all settlements that have a counterparty that is in
    the FILTERED_COUNTERPARTIES list AND have a settlement amount
    where MIN_AMOUNT <= amount <= MAX_AMOUNT. The rest of the doc ATS:es
    will use round roubin between themselves for the rest of the settlements.
    Example when using three doc ATS:es:
    doc_settlement_1:   will use round robin
    doc_settlement_2:   will use round robin
    doc_settlement_3:   handles settlements with valid amount and counterparty


    DISCLAIMER:
    The hooks in this module are EXAMPLES on how one could setup multiple
    ATS:es, not suggestions. To get optimal results the bottlenecks must be
    identified because different needs requires different setups and hooks.

"""

NUMBER_OF_DOC_ATSES         = 3
BASE_SOURCE                 = "doc_settlement_bodev415_"

#These parameters are used by mode MODE_AMOUNT_COUNTERPARTY
MIN_AMOUNT                  = -1000000
MAX_AMOUNT                  = 0
FILTERED_COUNTERPARTIES     = ["MyCounterparty"]

#Parameters for deciding the mode to run
MODE_TRADE                  = 1
MODE_AMOUNT_COUNTERPARTY    = 2





#Set the MODE parameter to either MODE_TRADE or MODE_AMOUNT_COUNTERPARTY
MODE = MODE_TRADE

def modify_outgoing_amba_message(amba_message, subject):
    result_tuple = (amba_message, subject)

    if MODE == MODE_TRADE:
        result_tuple = perform_filtering(amba_message, subject, filter_on_trade)
    elif MODE == MODE_AMOUNT_COUNTERPARTY:
        result_tuple = perform_filtering(amba_message, subject, filter_on_amount_and_counterparty)

    return result_tuple


def perform_filtering(amba_message, subject, filter_function):
    event_type = amba_message.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    event_type_as_string = event_type.mbf_get_value()
    result_tuple = (amba_message, subject)

    if (event_type_as_string == 'INSERT_SETTLEMENT' or
          event_type_as_string == 'UPDATE_SETTLEMENT'):
        sender_source = filter_function(amba_message)
        subject = sender_source + subject[subject.index("/"):]
        result_tuple = (amba_message, subject)
    elif (event_type_as_string == 'INSERT_OPERATIONSDOCUMENT' or
          event_type_as_string == 'UPDATE_OPERATIONSDOCUMENT'):
        if not opdoc_is_settlement(amba_message):
            result_tuple = None

    return result_tuple


def filter_on_trade(amba_message):
    sender_source = ""
    settlement_obj = object_by_name(amba_message, ['', '+', '!'], 'SETTLEMENT')
    if settlement_obj:
        sender_source = filter_on_trade_helper(settlement_obj, NUMBER_OF_DOC_ATSES)

    return sender_source

def filter_on_trade_helper(settlement_obj, number_of_doc_atses):
    sender_source = ""
    if settlement_obj and number_of_doc_atses > 0:
        seqnbr_obj = settlement_obj.mbf_find_object("TRDNBR")
        if not seqnbr_obj or seqnbr_obj.mbf_get_value() == "0":
            seqnbr_obj = settlement_obj.mbf_find_object("SEQNBR")
        if seqnbr_obj:
            ats_number = (int(seqnbr_obj.mbf_get_value()) % number_of_doc_atses) + 1
            sender_source = get_ats_source(ats_number)

    return sender_source

def filter_on_amount_and_counterparty(amba_message):
    sender_source = ""
    settlement_obj = object_by_name(amba_message, ['', '+', '!'], 'SETTLEMENT')
    if settlement_obj:
        if (is_amount_within_interval(settlement_obj) and
            is_counterparty_in_list(settlement_obj)):
            sender_source = get_ats_source(NUMBER_OF_DOC_ATSES)
        else:
            sender_source = filter_on_trade_helper(settlement_obj, NUMBER_OF_DOC_ATSES - 1)
    return sender_source

def is_amount_within_interval(settlement_obj):
    within_interval = False
    if settlement_obj:
        amount_obj = settlement_obj.mbf_find_object("AMOUNT")
        if amount_obj:
            amount = float(amount_obj.mbf_get_value())
            if amount >= MIN_AMOUNT and amount <= MAX_AMOUNT:
                within_interval = True
    return within_interval

def is_counterparty_in_list(settlement_obj):
    in_list = False
    if settlement_obj:
        counterparty_obj = settlement_obj.mbf_find_object("COUNTERPARTY_PTYNBR.PTYID")
        if counterparty_obj and counterparty_obj.mbf_get_value() in FILTERED_COUNTERPARTIES:
            in_list = True
    return in_list

def opdoc_is_settlement(amba_message):
    is_settlement = False
    opdoc_obj = object_by_name(amba_message, ['', '+', '!'], 'OPERATIONSDOCUMENT')
    if opdoc_obj:
        settlement_seqnbr = opdoc_obj.mbf_find_object("SETTLEMENT_SEQNBR")
        if settlement_seqnbr:
            if int(settlement_seqnbr.mbf_get_value()) > 0:
                is_settlement = True
    return is_settlement


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
