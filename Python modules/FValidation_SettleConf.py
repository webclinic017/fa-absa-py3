"""FValidation - Rules related to Settlements and Confirmations.

Before changing the code, please consult the Developer's Guide available at
<https://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer%27s+Guide>.

A list of the implemented FValidation rules is kept at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Rules>.
If you change the code, please update also that list to keep it up to date.


History
=======
2015-01-14 Dmitry Kovalenko  ???                (1) Module created; (2) added rule 13.
2015-08-20 Vojtech Sidorin   ABITFA-3743        Include rule numbers in messages.
2016-03-03 Evgeniya Baskaeva ABITFA-4042/4040   fv127_standardize_ci_name created
2016-06-13 Vojtech Sidorin   DEMAT              FV127: Include instrument category in standard confirmation
                                                instruction name.
2016-06-22 Vojtech Sidorin   DEMAT              Merge FValidation_Adaptiv_Conf_Stlm.

History merged from FValidation_Adaptiv_Conf_Stlm:
2015-??-?? Sanele Macanda    ???                Initial implementation; Adaptiv requirements;
                                                create module FValidation_Adaptiv_Conf_Stlm.
2015-06-29 Lawrence Mucheka  ADAFA-31           Add FV133 - Restrict call account withdrawals.
2016-06-22 Vojtech Sidorin   DEMAT              Refactor rules FV119, FV133; merge to FValidation_SettleConf.
2018-02-22 Bhavnisha Sarawan ABITFA-8403        Add Prolong Deposit Event Type.
2018-05-11 Willie vd Bank    CHG1000406751      Added fv138 set_security_settlement_fields.
                                                Modified fv119 to also update the trade status on a settlement.
2018-10-12 Cuen Edwards      FAOPS-246          Modified FV127 to include the alias of the internal department
                                                when specified on a confirmation instruction.  This allows for
                                                finer-grained confirmation instructions that previously could
                                                not be created due to name conflicts.  Also removed instype
                                                from the name when not specified as a confirmation instruction
                                                may only be 39 characters in length.
2018-09-15 Sadanand Upase    FAOPS-143          Set RTG flag when trade is created based on certain condition.
2019-03-12 Tawanda Mukhalela FAOPS-442          Added FV141 to prevent resubmitting of settlements that are
                                                pending sanctions approval.
2019-05-17 Stuart Wilson     FAOPS-479          Autoset of settle category SA_CUSTODIAN for automation of MT54X messages
                                                for capital markets.
2019-06-10 Tawanda Mukhalela FAOPS-488          Autoset Free of payment on Trade Optional Key 1 for SA CUstodian on Zero 
                                                Premium.
2020-04-30 Cuen Edwards      FAOPS-700          Migration of FV119-3 to Operations STP ATS.
2020-04-28 Faize Adams       PCGDEV-199         FV142: Added GUI warning when users instruct to cancel on a settlement.
                                                If the settlement is in commited status, present a confirmation
                                                popup warning the user that they are canceling a commited settlement.
2020-04-29                   FAOPS-615          Added FV143: Clears the TradArea and Settle Category fields for Internal
                                                transfer trades. This ensures that the related STP hook will
                                                 auto-populate and release settlements for trades
                                                 that meet the criteria only
2020-07-08 Faize Adams       SBL                FV144: Added GUI warning when users release a settlement and SWIFT solutions
                                                encounters an error generating the actual SWIFT message file.
2020-08-07 Faize Adams       SBL                Added additional logic to FV144 so that only relevant settlements are checked.

"""

import ael
import acm

from FValidation_core import (validate_entity,
                              validate_transaction,
                              ValidationError,
                              AccessValidationError,
                              DataValidationError,
                              show_validation_warning)
from SettlementConstants import (ACQUIRER_SHORTCODE,
                                 INSTYPE_SHORTCODE,
                                 CASHFLOWTYPE_SHORTCODE)
from Adaptiv_XML_Functions import GetCallTradeBalance
from at_type_helpers import to_acm
from demat_functions import is_demat

@validate_entity("SettleInstruction", "Update")
def fv13_rename_ssi_on_update(e, op):
    """Rename SSI according to the latest active SSI rule."""

    cp = ''
    i_type = ''
    settle_id = ''

    # Acquirers used for Settlement Manager
    if e.counterparty_ptynbr:
        if e.counterparty_ptynbr.ptynbr in ACQUIRER_SHORTCODE:
            cp = ACQUIRER_SHORTCODE[e.counterparty_ptynbr.ptynbr]
    else:
        if e.ptynbr.ptynbr in ACQUIRER_SHORTCODE:
            cp = ACQUIRER_SHORTCODE[e.ptynbr.ptynbr]

    # Instypes used for Settlement Manager
    if e.instype in INSTYPE_SHORTCODE:
        i_type = INSTYPE_SHORTCODE[e.instype]

    # Cashflow types used for Settlement Manager
    if cp and i_type:
        settle = ael.SettleInstruction[e.seqnbr].clone()

        for rule in settle.rules():
            if settle.settle_cf_type in CASHFLOWTYPE_SHORTCODE:
                cft = CASHFLOWTYPE_SHORTCODE[settle.settle_cf_type]
                settle_id = (rule.accnbr.name + '/' + cp + '/' +
                             i_type + '/' + cft)
            elif settle.sec_settle_cf_type in CASHFLOWTYPE_SHORTCODE:
                cft = CASHFLOWTYPE_SHORTCODE[settle.sec_settle_cf_type]
                settle_id = (rule.sec_accnbr.name + '/' + cp + '/' +
                             i_type + '/' + cft)

    # Generic SSI name
    if (cp and e.curr is not None and e.instype == 'None'
            and e.settle_cf_type == 'None' and e.und_instype == 'None'
            and e.otc_instr == 'OTC'):
        settle = ael.SettleInstruction[e.seqnbr].clone()
        for rule in settle.rules():
            settle_id = rule.accnbr.name + '/' + cp + '/GENERIC'

    # In case a new name is generated check for name clashes
    if (settle_id):
        ssis = ael.Party[e.ptynbr.ptynbr].settle_instructions()
        ssis = map(lambda s: (s.seqnbr, s.settleid), ssis)
        clashes = filter(lambda s: s[1] == settle_id, ssis)

        for c in clashes:
            if c[0] != e.seqnbr:
                msg = ('FV13: A SettleInstruction with ID "' + settle_id +
                       '" already exists. Please, re-enable or delete it.')
                # Only warn the user about the clash, allowing modification
                # of the conflicting rule, if it comes later in the
                # transaction.
                show_validation_warning(msg)
                return

        e.settleid = settle_id

    return


@validate_transaction
def fv138set_security_settlement_fields(transaction_list):
    """(1) For GHS instruments an additional payment (fee) is added during the insert process, the amount of which is calculated as a percentage of the trade premium.
        (2) When a trade has settlements in Settled status, a warning is raised when amendments are made and Voids are completely blocked.
        (3) On an Insert or Update the optional key 1 is set according to the premium value.
        (4) On an Insert or Update the trade settlement category is set according to the currency.
        (5) On insert of trade set the RTG field based on the condition"""

    for entity, operation in transaction_list:
        if entity.record_type == "Trade":

            if entity.insaddr.instype in (
            "Bond", "Bill", "FRN", "Repo/Reverse", "IndexLinkedBond", "Combination", "BuySellback",
            "Collateral") and entity.status == "FO Confirmed":
                if operation in ("Insert", "Update"):
                    acm_trade = acm.Ael.AelToFObject(entity)
                    curr = acm_trade.Currency().Name()
                    block_trade = acm.FChoiceList.Select01("list = 'TradArea' and name='Block Trade'",
                                             'Error trying to retrieve Block Trade choicelist')
                    if curr == "ZAR":
                        valid_block_trade = False
                        if acm_trade.Instrument().AddInfoValue("Exchange") == "BESA":
                            if acm_trade.OptKey1():
                                if acm_trade.OptKey1() == block_trade:
                                    valid_block_trade = True

                        if acm_trade.Counterparty().AddInfoValue("UnexCor Code") or valid_block_trade:
                            if acm_trade.Counterparty().AddInfoValue("BESA_Member_Agree") not in ("Closed", "No") or valid_block_trade:
                                if acm_trade.Counterparty().HostId() not in ("INTERNAL", "") or valid_block_trade:
                                    if not entity.settle_category_chlnbr:
                                        entity.settle_category_chlnbr = acm.FChoiceList.Select01 \
                                            ("list = 'TradeSettleCategory' and name='SA_CUSTODIAN'",
                                             'Error trying to retrieve SA_CUSTODIAN settle category choicelist').Oid()

                                        print(('FV138: Settle Category set to %s.' % 'SA_CUSTODIAN'))

                                    if acm_trade.SettleCategoryChlItem().Name() == 'SA_CUSTODIAN' and entity.premium == 0:
                                        free_of_payment = acm.FChoiceList.Select('name="Free of payment" and list=TradArea')
                                        if free_of_payment:
                                            entity.optkey1_chlnbr = free_of_payment[0].Oid()
                                            print ('FV138: Trade Optional Key 1 set to Free of payment.')

            if (entity.insaddr.instype in ("Bond", "Bill")
                    and entity.acquirer_ptynbr
                    and entity.acquirer_ptynbr.ptyid in ("AFRICA DESK")):

                if operation in ("Insert", "Update"):

                    if entity.status in ("FO Confirmed", "Simulated"):
                        acm_trade = acm.FTrade[entity.trdnbr]
                        curr = acm_trade.Currency().Name()
                        if curr in ('BWP', 'GHS', 'KES', 'MUR', 'NGN', 'UGX', 'ZMW', 'ZWD'):
                            if not entity.settle_category_chlnbr:
                                TradeSettleCategories = acm.FChoiceList.Select('list = TradeSettleCategory')
                                for tsc in TradeSettleCategories:
                                    if curr in tsc.Name():
                                        entity.settle_category_chlnbr = tsc.Oid()
                                        print(('FV138: Settle Category set to %s.' % tsc.Name()))
                            if not entity.optkey1_chlnbr:
                                if entity.premium == 0:
                                    FoP = acm.FChoiceList.Select('name="Free of payment" and list=TradArea')
                                    if FoP:
                                        entity.optkey1_chlnbr = FoP[0].Oid()
                                        print ('FV138: Trade Optional Key 1 set to Free of payment.')

                if operation == "Insert" and entity.curr.insid == 'GHS':
                    new_pmt = ael.Payment.new(entity)
                    new_pmt.type = 'Premium'

                if operation == "Insert" and entity.curr.insid == 'GHS' and \
                        (not entity.optkey1_chlnbr or entity.optkey1_chlnbr.entry != 'Free of payment'):
                    if acm.FPayment.Select('trade=%s type="%s"' % (entity.trdnbr, 'Premium')):
                        new_pmt = _get_premium_payment(entity)
                    else:
                        new_pmt = ael.Payment.new(entity)
                        new_pmt.type = 'Premium'

                    new_pmt.payday = entity.value_day
                    new_pmt.valid_from = ael.date_from_time(entity.time)
                    new_pmt.amount = -1 * abs(entity.premium * 0.0001)
                    new_pmt.ptynbr = 21907  # STANDARD CHARTERED BANK GHANA SCBLGHAC
                    new_pmt.text = 'CSD Fees'
                    print ('FV138: CSD Fee additional payment created for GHS trade.')

                if (operation == "Update"
                        and entity.status in ('BO Confirmed', 'BO-BO Confirmed', 'Void')):
                    settled_settlements = [s for s in entity.original().settlements()
                                           if s.status == 'Settled' and s.type == 'Security Nominal']
                    if settled_settlements:
                        if entity.status == 'Void':
                            raise ValidationError("FV138: This trade has settled settlements. These have to be closed "
                                                  "before voiding the trade!")
                        else:
                            show_validation_warning("FV138: This trade has settled settlements. No economic amendments "
                                                    "should be made.", popup=True)

            if entity.insaddr.instype in ("Bond", "Bill", "FRN", "Repo/Reverse"):
                if operation == "Insert":
                    acm_trade = acm.FTrade[entity.trdnbr]
                    curr = acm_trade.Currency().Name()
                    if curr in ('GBP', 'USD', 'ZAR', 'EUR', 'JPY'):
                        rtg_value = '0'
                        if acm_trade.ValueDay() == acm.Time.DateFromTime(acm_trade.CreateTime()) or \
                                acm_trade.ValueDay() == acm.Time.DateToday():
                            rtg_value = '1'
                        # setting addinfo this part can be refactored at the level of fvalidation because while setting
                        # addinfo in fvalidation you dont want to commit anything.
                        spec_name = 'RTG'
                        add_info_spec = ael.AdditionalInfoSpec[str(spec_name)]
                        add_info_to_set = None
                        for add_info in entity.additional_infos():
                            if add_info.addinf_specnbr == add_info_spec:
                                add_info_to_set = add_info
                                break
                        if add_info_to_set:
                            add_info_to_set.value = rtg_value
                        else:
                            add_info_to_set = ael.AdditionalInfo.new(entity)
                            add_info_to_set.addinf_specnbr = add_info_spec
                            add_info_to_set.value = rtg_value
                        print(('FV138: RTG flag set to %s.' % rtg_value))

    return transaction_list


@validate_transaction
def fv119_set_trade_status_according_to_confirmation_or_settlement(transaction_list):
    """Set Trade status according to Confirmation or settlement status.

    (1) Set Trade status to BO Confirmed when the Confirmation gets released.
    (2) Set Trade status to BO-BO Confirmed when the Confirmation gets matched.
    (3) Set Trade status to BO Confirmed when the Security Nominal Settlement gets Acknowledged.

    Demat instruments are excluded from this rule.
    Call accounts are excluded from sub-rule (2).
    """

    for entity, operation in transaction_list:
        if entity.record_type == "Confirmation" and operation == "Update":
            conf = entity
            trade = conf.trdnbr
            acm_trade = to_acm(trade)
            acm_instrument = acm_trade.Instrument()

            if (conf.type != "Cancellation" and conf.event_chlnbr.entry in
                    ("New Trade", "New Trade Call", "Novation", "Prolong Deposit")
                    and not is_demat(acm_instrument)):

                # FV119-1: Move Trade to BO Confirmed.
                if (conf.status in ("Acknowledged", "Pending Matching")
                        and conf.original().status == "Released"
                        and trade.status == "FO Confirmed"):
                    trade_clone = trade.clone()
                    trade_clone.status = "BO Confirmed"
                    transaction_list.append((trade_clone, "Update"))
                    msg = ("FV119-1: Trade {0} BO Confirmed."
                           .format(trade_clone.trdnbr))
                    print(msg)

                # FV119-2: Move Trade to BO-BO Confirmed.
                if (conf.status == "Matched"
                        and conf.original().status == "Pending Matching"
                        and not acm_instrument.IsCallAccount()):
                    trade_clone = trade.clone()
                    trade_clone.status = "BO-BO Confirmed"
                    transaction_list.append((trade_clone, "Update"))
                    msg = ("FV119-2: Trade {0} BO-BO Confirmed."
                           .format(trade_clone.trdnbr))
                    print(msg)

        if entity.record_type == "Settlement" and operation in ("Insert", "Update"):
            stmnt = to_acm(entity)
            if acm.FStoredASQLQuery["Collateral_Auto_Settlements"].Query().IsSatisfiedBy(stmnt) and stmnt.Status() in ("Authorised", "Exception"):
                entity.status = "Settled"
                msg = ("Settlement {0} moved to Settled from Authorised\Exception.".format(stmnt.Oid()))
                print(msg)

    return transaction_list


@validate_entity("ConfInstruction", "Insert")
def fv127_set_conf_instruction_name(entity, operation):
    """Set standard Confirmation Instruction name.

    When saving a new Confirmation Instruction, set its name to follow a
    standard format.

    The name consists of the following 4 components in the given order:
        Internal Department:    empty if not set
        Ins Category:           empty if not set
        Instrument type:        empty if not set
        Event:                  empty if not set
        Transport type:         'Email' or 'Network'

    If another Confirmation Instruction with the same standard name already
    exists for a given counterparty, raise an exception and show the error
    message to the user.

    Confirmation instructions with the following names are excluded from this
    rule:
        NA Generic_FATLM_Upload
        Generic_FATLM_Upload
    """
    EXCLUDE_CI_NAMES = ["NA Generic_FATLM_Upload", "Generic_FATLM_Upload"]

    # Exclude certain Confirmation Instructions.
    if entity.name in EXCLUDE_CI_NAMES:
        return

    # Generate the standard name.
    name_parts = []
    # Internal Department.
    if entity.interndept_ptynbr:
        if not entity.interndept_ptynbr.ptyid2:
            error_msg = "FV127: No alias on internal department specified. Please specify one and try saving again."
            raise DataValidationError(error_msg)
        name_parts.append(entity.interndept_ptynbr.ptyid2)
    # Ins Category (choice list Settle Category).
    if entity.settle_category_chlnbr:
        name_parts.append(entity.settle_category_chlnbr.entry)
    # Instrument Type.
    if entity.instype != 'None':
        name_parts.append(entity.instype)
    # Event (choice list Event).
    if entity.event_chlnbr:
        name_parts.append(entity.event_chlnbr.entry)
    # Transport type.
    name_parts.append(entity.transport)
    standard_name = " ".join(name_parts)

    # Check for duplicate Confirmation Instructions.
    cpty_name = entity.counterparty_ptynbr.ptyid
    query = ("name = '{0}' and counterparty = '{1}' and oid <> {2} and oid > 0"
             .format(standard_name, cpty_name, entity.seqnbr))
    collisions = acm.FConfInstruction.Select(query)
    if collisions:
        error_msg = ("FV127: Another ConfInstruction with the same name "
                     "already exists for the counterparty. Please change the "
                     "combination of fields Internal Department, Ins Category, "
                     "Instrument type, Event, and Transport type; or delete the "
                     "other ConfInstruction.")
        raise DataValidationError(error_msg)

    # Set the standard name.
    entity.name = standard_name


@validate_entity("Settlement", "Update", caller="validate_transaction")
def fv141_prevent_resubmit_and_regenerate_nak_on_sanctions_pending(settlement, operation):
    """
    Preventing Resubmitting Nack and Regeneration on a nacked settlements
    [1]     Prevent resubmitting of settlements that are pending sanctions
            approval.
    [2]     Prevent regenerate functionality of settlements that are pending sanctions
            approval
    """
    # check if document status is "SWIFT NAK    :Sanctions Pending"
    if not _is_settlement_sanctions_pending(settlement.original()):
        return
    # Check if the actions is a resubmit
    if _is_settlement_resubmit_nak(settlement):
        error_message = 'FV141: You are not permitted to Resubmit NAK for a settlement '
        error_message += 'that is pending sanctions approval.'
        raise AccessValidationError(error_message)
    # Check if the actions is a regenerate
    if _is_settlement_regenerate_nak(settlement):
        error_message = 'FV141: You are not permitted to Regenerate or Change Status for a settlement '
        error_message += 'that is pending sanctions approval.'
        raise AccessValidationError(error_message)


@validate_entity("Settlement", "Update", caller="validate_transaction")
def fv142_collateral_settlements_warn_on_commit_cancel(settlement, operation):
    YES = "Button1"
    NO = "Button2"
    continueAnswer = YES
    #Lets the validation pass if there are errors since we are testing this and dont want to impact anything
    try:
        acmSettlement = to_acm(settlement)
        if acmSettlement.Trade().SettleCategoryChlItem():
            if acmSettlement.Status() == "Acknowledged" and\
               acmSettlement.Trade().SettleCategoryChlItem().Name() == "SL_STRATE" and\
               acmSettlement.Trade().TradeCategory() == "Collateral" and\
               _is_settlement_instruct_to_cancel(settlement):
                shell = acm.UX().SessionManager().Shell()
                message = "FV142: Settlement %s is in a commited status. Please confirm Instruct to Cancel" % acmSettlement.Oid()
                continueAnswer = acm.UX().Dialogs().MessageBoxYesNo(shell, "Question", message)
    except Exception, e:
        print(("Exception fv142: %s" % str(e)))

    if continueAnswer == YES:
        return
    else:
        print ("Failed rule fv142")
        raise DataValidationError("Status change not applied.")


@validate_entity("Trade", "Insert")
def fv143_clear_internal_transfer_fields(trade, operation):
    """"
    Automatically clear the 'TradArea' and 'SettleCatogry'
    for internal transfer fields
    """
    rule = 'FV143'

    if trade.optkey1_chlnbr is not None:

        if trade.optkey1_chlnbr.entry == 'Internal Transfer':
            print('Clearing TradArea and SettleCategory ...')
            _clear_trad_area(rule, trade)
            _clear_trade_settle_category(rule, trade)


@validate_entity("Settlement", "Update", caller="validate_transaction")
def fv144_sbl_settlement_swift_prerelease_validation(settlement, operation):
    try:
        acmSettlement = to_acm(settlement)
        if _should_generate_sbl_settlement_swift(acmSettlement, "FV144"):
            from FSwiftWriterUtils import generate_swift_message
            swift_message, mt_py_object, exceptions, getter_values = generate_swift_message(acmSettlement, msg_type)
            if exceptions:
                raise DataValidationError("FV144: SWIFT message failed to generate.")
    except Exception, e:
        print(("Exception FV144: %s" % str(e)))

    return


def _should_generate_sbl_settlement_swift(settlement, rule):
    try:
        if settlement.Trade().SettleCategoryChlItem():
            if settlement.Status() == "Authorised" and\
                settlement.Trade().SettleCategoryChlItem().Name() in ["SL_STRATE", "SL_CUSTODIAN"]:

                from FSwiftMLUtils import calculate_mt_type_from_acm_object
                from FSwiftServiceSelector import is_security_loan_settlement, is_collateral_settlement

                msg_type = 'MT' + str(calculate_mt_type_from_acm_object(settlement))

                if is_collateral_settlement(settlement, msg_type) or is_security_loan_settlement(settlement, msg_type):
                    return True
    except Exception, e:
        print(("Exception %s (_settlement_is_sbl_settlement): %s" % (rule, str(e))))

    return False


def _clear_trad_area(rule, trade):
    """
    Auto-set Trade Optional Key 1 (TradArea) to the specified value
    if not already set.
    """

    trade.optkey1_chlnbr = None

    print(("{rule}: Trade Optional Key 1 (TradArea) set to '{name}'.".format(
        rule=rule,
        name=None
    )))


def _clear_trade_settle_category(rule, trade):
    """
    Clears the Trade Settle Category
    """
    trade.settle_category_chlnbr = None
    print(("{rule}: Trade Settle Category set to '{name}'.".format(
        rule=rule,
        name=None
    )))


def _is_settlement_sanctions_pending(settlement):
    if not _is_settlement_swift_nak(settlement):
        return False
    operations_document = _get_settlement_operations_document(settlement)
    if operations_document.status != 'Send failed':
        return False
    return operations_document.status_explanation == 'SCA: Sanctions Pending'


def _is_settlement_swift_nak(settlement):
    if settlement.status != 'Not Acknowledged':
        return False
    power = ael.enum_from_string('StatusExplanation', 'SWIFT NAK')
    encoded_value = 2 ** power
    return settlement.status_explanation & encoded_value != 0


def _get_settlement_operations_document(settlement):
    select_expression = 'settlement_seqnbr = {seqnbr}'.format(
        seqnbr=settlement.seqnbr
    )
    operations_documents = ael.OperationsDocument.select(select_expression)
    if len(operations_documents) != 1:
        raise RuntimeError('Expecting one operations document for settlement {seqnbr}'.format(
            seqnbr=settlement.seqnbr
        ))
    return operations_documents[0]


def _is_settlement_resubmit_nak(settlement):
    return _is_settlement_status_transition(settlement, 'Not Acknowledged', 'Authorised')


def _is_settlement_regenerate_nak(settlement):
    return _is_settlement_status_transition(settlement, 'Not Acknowledged', 'Exception')


def _is_settlement_instruct_to_cancel(settlement):
    return _is_settlement_status_transition(settlement, 'Acknowledged', 'Void')


def _is_settlement_status_transition(settlement, from_status, to_status):
    if settlement.status != to_status:
        return False
    original_settlement = settlement.original()
    if original_settlement is None:
        return False
    return original_settlement.status == from_status


def _get_premium_payment(trade):
    payments = ael.Payment.select('trdnbr={tradeId}'.format(tradeId=trade.trdnbr))
    for payment in payments:
        if payment.type == 'Premium':
            return payment
