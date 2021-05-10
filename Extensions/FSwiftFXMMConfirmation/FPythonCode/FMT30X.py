"""----------------------------------------------------------------------------
MODULE:
    FMT30X

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMT300/305
    Base class for mapping attributes.
    Default logic for extracting attributes from either the swift data or the
    confirmation object.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MT30X message. It stores the incoming message in
        FExternalItem and creates the business process.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('FXMMConfIn', 'FFXMMConfirmationInNotify_Config')
import FMTInBase
import FSwiftMLUtils


class FMT30X(FMTInBase.FMTInBase):
    """ Base class for MT mapping"""
    def __init__(self, source, direction):
        super(FMT30X, self).__init__(source, direction)
        self._related_reference = None
        self._internalRelatedReference = None
        self._internal_identifier = None
        self.acquirer = None
        self.counterparty = None
        self.set_internal_related_reference()
        self.set_internal_identifier()
        self.subject_type = 'Confirmation'

# ------------------------------------------------------------------------------
    def set_related_reference(self):
        try:
            self._related_reference = str(self.python_object.SequenceA_GeneralInformation.RelatedReference.value()) if self.python_object.SequenceA_GeneralInformation.RelatedReference else None
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_related_reference_from_swift : %s"%str(e))

    def set_internal_related_reference(self):
        try:
            if self.python_object and self.python_object.SequenceA_GeneralInformation and self.python_object.SequenceA_GeneralInformation.RelatedReference:
                ref = str(self.python_object.SequenceA_GeneralInformation.RelatedReference.value())

                index = ref.find('-')
                if index != -1:
                    ref = ref[index+1:]

                self._internalRelatedReference = ref
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_internal_related_reference : %s"%str(e))

    def set_internal_identifier(self):
        try:
            if self.python_object and self.python_object.SequenceA_GeneralInformation:
                if getattr(self.python_object.SequenceA_GeneralInformation, 'TransactionReferenceNumber', None):
                    ref = str(self.python_object.SequenceA_GeneralInformation.TransactionReferenceNumber.value())
                else:
                    ref = str(self.python_object.SequenceA_GeneralInformation.SendersReference.value())
                '''
                index = ref.find('-')
                if index != -1:
                    ref = ref[index+1:]
                '''
                self._internal_identifier = ref
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_internal_identifier : %s"%str(e))

    def InternalRelatedReference(self):
        return self._internalRelatedReference

    def InternalIdentifier(self):
        return self._internal_identifier

    def RealCounterparty(self):
        try:
            cpty = ''
            if self.python_object.SequenceA_GeneralInformation.PartyB_A:
                cpty = self.python_object.SequenceA_GeneralInformation.PartyB_A.value()
            else:
                cpty = self.python_object.SequenceA_GeneralInformation.PartyB_D.value()

            if cpty:
                return str(self.get_party_typeA(cpty))
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealCounterparty : %s"%str(e))

    def RealAcquirer(self):
        try:
            acquirer = ''
            if self.python_object.SequenceA_GeneralInformation.PartyA_A:
                acquirer = self.python_object.SequenceA_GeneralInformation.PartyA_A.value()
            else:
                acquirer = self.python_object.SequenceA_GeneralInformation.PartyA_D.value()
            if acquirer:
                return str(self.get_party_typeA(acquirer))
        except Exception as e:
            notifier.DEBUG("Exception occurred in RealAcquirer : %s"%str(e))


    def set_acquirer(self):
        try:
            acquirer = ''
            if self.direction == 'IN':
                if self.python_object.SequenceA_GeneralInformation.PartyB_A:
                    acquirer = self.python_object.SequenceA_GeneralInformation.PartyB_A.value()
                else:
                    acquirer = self.python_object.SequenceA_GeneralInformation.PartyB_D.value()
            else:
                if self.python_object.SequenceA_GeneralInformation.PartyA_A:
                    acquirer = self.python_object.SequenceA_GeneralInformation.PartyA_A.value()
                else:
                    acquirer = self.python_object.SequenceA_GeneralInformation.PartyA_D.value()
            if acquirer:
                self.acquirer = str(self.get_party_typeA(acquirer))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer : %s"%str(e))

    def set_counterparty(self):
        try:
            counterparty = ''
            if self.direction == 'IN':
                if self.python_object.SequenceA_GeneralInformation.PartyA_A:
                    counterparty = self.python_object.SequenceA_GeneralInformation.PartyA_A.value()
                else:
                    counterparty = self.python_object.SequenceA_GeneralInformation.PartyA_D.value()
            else:
                if self.python_object.SequenceA_GeneralInformation.PartyB_A:
                    counterparty = self.python_object.SequenceA_GeneralInformation.PartyB_A.value()
                else:
                    counterparty = self.python_object.SequenceA_GeneralInformation.PartyB_D.value()

            if counterparty:
                self.counterparty = str(self.get_party_typeA(counterparty))
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_counterparty : %s"%str(e))

# ------------------------------------------------------------------------------
    def set_acquirer_counterparty_from_trade(self):
        try:
            for flw in self.acm_obj.Trade().MoneyFlows():
                if flw.Type() == "Premium":
                    self.counterparty = flw.CounterpartyAccount().NetworkAlias().Name() if (flw.CounterpartyAccount() and flw.CounterpartyAccount().NetworkAlias()) else self.acm_obj.Counterparty().Swift()
                    self.acquirer = flw.AcquirerAccount().NetworkAlias().Name() if (flw.AcquirerAccount() and flw.AcquirerAccount().NetworkAlias()) else self.acm_obj.Acquirer().Swift()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_acquirer_counterparty_from_trade : %s"%str(e))

    def get_party_typeA(self, party):
        partyId = ""
        try:
            if party:
                party_data = party.split('\n')
                partyId = party_data[1] if len(party_data) > 1 else party_data[0]
        except Exception as e:
            notifier.DEBUG("Exception occurred in get_party_typeA : %s"%str(e))
        return partyId

# ------------------------------------------------------------------------------
    def RelatedReference(self):
        return self._related_reference

    def Acquirer(self):
        return self.acquirer

    def Counterparty(self):
        return self.counterparty

# ------------------------------------------------------------------------------
    def IsSupportedMessageFunction(self):
        """check if the message type is supported"""
        is_supported = False
        if self._message_function in ["NEW", "NEWT", "AMND", "CANC", "AMEND", "CANCEL"]:
            is_supported = True
        return is_supported



