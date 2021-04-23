"""----------------------------------------------------------------------------
MODULE:
    FMT0OutBase

DESCRIPTION:
    Base class for a default template for confirmations that do not have any MT type (FMT0Out).

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSwiftMLUtils
import FSwiftWriterLogger
import FSwiftOperationsAPI
#from FSettlementEnums import SettlementType
SettlementType = FSwiftOperationsAPI.GetSettlementTypeEnum()
#from FConfirmationEnums import ConfirmationType


notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')
writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')

sharedVariables = dict()

def set_money_flows(confirmation):
    global sharedVariables
    sharedVariables.clear()
    calcSpace = None
    trade = confirmation.Trade()
    mt = FSwiftMLUtils.calculate_mt_type_from_acm_object(confirmation)
    resetCashFlow = ''
    if confirmation.Reset():
        resetCashFlow = confirmation.Reset().CashFlow()
    moneyflows = trade.MoneyFlows(None, None)
    for aMoneyFlow in moneyflows:
        if aMoneyFlow.Type() == SettlementType.REDEMPTION_AMOUNT and mt == '330':
            sharedVariables['moneyFlow'] = aMoneyFlow
        if resetCashFlow == aMoneyFlow.SourceObject() and mt == '362':
            sharedVariables['moneyFlow'] = aMoneyFlow
        elif aMoneyFlow.Type() in [SettlementType.PREMIUM, SettlementType.PREMIUM_2]:
            if not calcSpace:
                calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                sharedVariables['calcSpace'] = calcSpace
            calcValue = aMoneyFlow.Calculation().Projected(calcSpace)
            if calcValue:
                amount = calcValue.Number()
                if acm.Operations.IsValueInfNanOrQNan(amount):
                    amount = 0
                if amount > 0:
                    sharedVariables['buyMoneyFlow'] = aMoneyFlow
                    sharedVariables['buyAmount'] = amount
                else:
                    sharedVariables['sellMoneyFlow'] = aMoneyFlow
                    sharedVariables['sellAmount'] = amount

            if aMoneyFlow.Type() == SettlementType.PREMIUM:
                sharedVariables['moneyFlow'] = aMoneyFlow

class FMT0Base(object):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.acm_obj = acm_obj
        self.swift_obj = swift_obj
        self.swift_message_type = 'MT0'
        set_money_flows(self.acm_obj)

    # SwiftMTBase
    # ------------------------------ value of codeword newline ----------------------
    def get_codeword_newline(self):
        codeword_newline = getattr(writer_config, "CodewordNewline", 'codeword')
        return codeword_newline

    # -------------------------- value of narrative separator -----------------------
    def get_narrative_saperator(self):
        separator = getattr(writer_config, "Separator", 'newline')
        return separator

    # -------------------------- value of swift message type ------------------------
    def get_swift_message_type(self):
        return FSwiftMLUtils.calculate_mt_type_from_acm_object(self.acm_obj)

    # SwiftMTConfirmation
    # ------------------------ value of partyA option ----------------------
    def get_partyA_option(self):
        return ''

    # ------------------------ value of partyA account ----------------------
    def get_partyA_account(self):
        partyAAccount = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            acqaccount = moneyFlow.AcquirerAccount()
            if acqaccount:
                partyAAccount = acqaccount.Account()
        return partyAAccount

    # ------------------------ value of partyA bic ------------------------
    def get_partyA_bic(self):
        partyABic = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            acqaccount = moneyFlow.AcquirerAccount()
            if acqaccount:
                partyABic = FSwiftMLUtils.get_party_bic(acqaccount)
        return partyABic

    # ------------------------- value of partyA name ------------------------
    def get_partyA_name(self):
        partyAName = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            should_use_party_fullname = getattr(writer_config, "UsePartyFullName", False)
            partyAName = FSwiftMLUtils.get_party_full_name(moneyFlow.Acquirer(), bool(should_use_party_fullname))
        return partyAName

    # ------------------------- value of partyA address ------------------------
    def get_partyA_address(self):
        partyAAddress = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            partyAAddress = FSwiftMLUtils.get_party_address(moneyFlow.Acquirer())
        return partyAAddress

    # ----------------- value of partyB option ----------------
    def get_partyB_option(self):
        partyBOption = ''
        return partyBOption

    # ---------------- value of partyB account ---------------
    def get_partyB_account(self):
        partyBAccount = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            cpaccount = moneyFlow.CounterpartyAccount()
            if cpaccount:
                partyBAccount = cpaccount.Account()
        return partyBAccount

    # --------------- value of partyB bic ---------------
    def get_partyB_bic(self):
        partyBBic = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            cp = moneyFlow.Counterparty()
            if cp:
                partyBBic = cp.Swift()
            cpaccount = moneyFlow.CounterpartyAccount()
            if cpaccount:
                partyBBic = FSwiftMLUtils.get_party_bic(cpaccount)
        return partyBBic

    # --------------- get partyB name ----------------
    def get_partyB_name(self):
        partyBName = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            cp = moneyFlow.Counterparty()
            if cp:
                should_use_party_fullname = getattr(writer_config, "UsePartyFullName", False)
                partyBName = FSwiftMLUtils.get_party_full_name(cp, bool(should_use_party_fullname))
        return partyBName

    # -------------- get partyB address -----------------
    def get_partyB_address(self):
        partyBAddress = ''
        moneyFlow = sharedVariables.get('moneyFlow')
        if moneyFlow:
            cp = moneyFlow.Counterparty()
            if cp:
                partyBAddress = FSwiftMLUtils.get_party_address(cp)
        return partyBAddress

    # --------------- get receiver bic ----------------
    def get_receiver_bic(self):
        '''Returns SWIFT bic code of settlement receiver.
        This field goes into {2:Application Header Block} -- Receiver Information.'''

        if str(getattr(writer_config, 'SwiftLoopBack', "")) == 'True':
            return str(getattr(writer_config, 'ReceiverBICLoopBack', ""))
        else:
            return self.acm_obj.CounterpartyAddress()

    # --------------- get senders bic ----------------
    def get_sender_bic(self):
        '''Returns SWIFT bic code of the Acquirer of the settlement.
        This field goes into {1: Basic Header Block} -- Address of the Sender'''

        if str(getattr(writer_config, 'SwiftLoopBack', "")) == 'True':
            return str(getattr(writer_config, 'SenderBICLoopBack', ""))
        else:
            return self.acm_obj.AcquirerAddress()

    # ------------- get seq ref ---------------
    def get_seq_ref(self):
        return str(getattr(writer_config, 'FAC', "FAC"))

    # ------------- get network ----------------
    def get_network(self):
        network = ''
        confirmation = self.acm_obj
        if confirmation.ConfTemplateChlItem():
            if confirmation.ConfTemplateChlItem().Name() == 'SWIFT':
                network = confirmation.ConfTemplateChlItem().Name()
        return network

    # ------------- get trade date ------------
    def get_trade_date(self):
        confirmation = self.acm_obj
        assert confirmation.Trade(), "The confirmation has no trade reference"
        return confirmation.Trade().TradeTime()[:10]

    # Confirmation
    # -------------- get template name -------------
    def get_confirmation_template(self):
        return self.acm_obj.ConfTemplateChlItem().Name()

    # -------------- get event name --------------
    def get_confirmation_event_name(self):
        return self.acm_obj.EventChlItem().Name()

    # -------------- get reset oid ---------------
    def get_confirmation_reset_oid(self):
        if self.acm_obj.Reset():
            return self.acm_obj.Reset().Oid()
        return None

    # ------------- get confirmation transport -----------
    def get_confirmation_transport(self):
        return self.acm_obj.Transport()

    # ------------- get confirmation trade oid -------------
    def get_confirmation_trade_oid(self):
        return self.acm_obj.Trade().Oid()

    # ------------ get confirmation cashflow -------------
    def get_confirmation_cashflow(self):
        return self.acm_obj.CashFlow()

    def _attributes_to_compare_for_amendment_generation(self):
        """ Return a list of swift fields whose values will be used to create a checksum. There should be a method corresponding to
           swift field in the class. This method should return value of that field taken from acm API."""

        return [get_func for get_func in dir(self) if get_func.startswith('get_')]

