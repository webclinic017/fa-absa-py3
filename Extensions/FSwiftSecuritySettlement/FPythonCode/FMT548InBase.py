"""----------------------------------------------------------------------------
MODULE:
    FMT548InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it. User
    can extend/override the default mapping in derived class i.e. FMT548
    Base class for mapping attributes.
    Default logic for extracting attributes from either swift data or the
    settlement object.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MT548 message. It stores the incoming message in
        FExternalItem and creates the business process on it.

    UniquePair():
        Return paired object if incoming message has a unique identifier to get
        the object from acm. User can configure this.

    IsSecurityTransfer():
        Return true if the incoming message represents security transfer.
        User can configure this.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FMTInBase
import FSwiftMLUtils



class FMT548Base(FMTInBase.FMTInBase):
    """ Base class for MT54X mapping"""
    def __init__(self, source, direction, msg_type):
        super(FMT548Base, self).__init__(source, direction)
        self.type = msg_type
        self.config_param = FSwiftMLUtils.Parameters('F%sIn_Config'%(self.type))

        self._status_code = None
        self._internal_identifier = None
        self._senders_message_reference = None
        self._reason_code = None
        self._reason_narrative = None

# ------------------------------------------------------------------------------


    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT54X type"""
        try:
            if self.source == 'SWIFT':
                self.set_identifier()
                self.set_senders_message_reference()
                self.set_function_of_message()
                self.set_status_code()
                self.set_reason_code()
                self.set_reason_narrative()
        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

# ------------------------------------------------------------------------------
    # Methods to fetch data from the swift message
    def set_identifier(self):
        try:
            # settlement identifier is received as FAS-<settlement_identifier>
            # if user wants to extract the identifier in different way he can override this function in derived class
            self._identifier = 'NoIdentifier'
            for link in self.python_object.SequenceA_GeneralInformation.SubSequenceA1_Linkages:
                if link.Reference_C and 'RELA' == link.Reference_C.value()[1:5]:
                    related_ref_val = link.Reference_C.value()[7:]
                    self._identifier = str(related_ref_val)
                    self._internal_identifier = self._identifier

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identifier : %s"%str(e))


    def set_senders_message_reference(self):
        try:
            value = self.python_object.SequenceA_GeneralInformation.SendersMessageReference.value()
            self._senders_message_reference = value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_senders_message_reference : %s"%str(e))


    def set_function_of_message(self):
        try:
            value = self.python_object.SequenceA_GeneralInformation.FunctionOfTheMessage.value()
            if value:
                value = value.split('/')
                if value[0] in ['CAST', 'INST']:
                    self._message_function = str(value[0])
                sub_value = value[-1]
                if sub_value and sub_value in ['CODU', 'COPY', 'DUPL']:
                        self._sub_function =  sub_value

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_function_of_message : %s"%str(e))


    def set_status_code(self):
        try:
            for each in self.python_object.SequenceA_GeneralInformation.SubSequenceA2_Status:
                value = each.StatusCode.value()

            self._status_code = value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_status_code : %s" % str(e))


    def set_reason_code(self):
        try:
            value = None
            for each_status in self.python_object.SequenceA_GeneralInformation.SubSequenceA2_Status:
                for each_subseq in each_status.SubSequenceA2a_Reason:
                    value = each_subseq.ReasonCode.value()
            self._reason_code = value

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_reason_code : %s" % str(e))

    # optional
    def set_reason_narrative(self):
        try:
            value = None
            for each_status in self.python_object.SequenceA_GeneralInformation.SubSequenceA2_Status:
                for each_subseq in each_status.SubSequenceA2a_Reason:
                    if each_subseq and each_subseq.ReasonNarrative:
                        value = each_subseq.ReasonNarrative.value()

            self._reason_narrative = value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_reason_narrative : %s" % str(e))


# ------------------------------------------------------------------------------

    def Type(self):
        """ Get the type of the MT message"""
        return self.type

    def Identifier(self):
        return self._identifier

    def StatusCode(self):
        return str(self._status_code)

    def ReasonCode(self):
        return self._reason_code

    def FunctionOfMessage(self):
        return self._message_function

# ------------------------------------------------------------------------------

    def InternalIdentifier(self):
        return self._internal_identifier

    def get_bpr(self, external_obj, is_new):
        state_chart_name = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type(), 'In')
        reconciliation_item = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)

        bpr = FSwiftMLUtils.get_or_create_business_process(external_obj, state_chart_name, self.Type())
        if bpr:
            notifier.INFO('%s : Business process id <%i> with state chart <%s> on %s <%i>' \
                          % ('Initialized' if is_new else 'Reusing', bpr.Oid(), state_chart_name, reconciliation_item.ClassName(), reconciliation_item.Oid()))

        return bpr


    def ProcessMTMessage(self, msg_id):
        """ process the incoming mt message"""
        notifier.INFO("Processing incoming %s message."%(self.type))
        try:
            value_dict = {'swift_data':self.swift_data}

            # Check if we already have external object.
            prev_external_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(msg_typ = self.type, ext_ref = self.InternalIdentifier())

            if prev_external_obj.IsKindOf(acm.FPersistentSet):
                if not prev_external_obj:
                    prev_external_obj = None


            external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict,
                                                                                     message_typ=self.Type(),
                                                                                     channel_id=msg_id,
                                                                                     subject_typ='Settlement',
                                                                                     ext_ref=self.InternalIdentifier(),
                                                                                     in_or_out="Incoming")

            if prev_external_obj is None:
                self.get_bpr(external_obj, True)
            else:

                # Link the new external object to
                bpr = self.get_bpr(prev_external_obj, False)
                bpr.Subject(external_obj)
                bpr.Commit()

                FSwiftMLUtils.FSwiftExternalObject.set_ext_obj_parent(prev_external_obj, external_obj)

                # if the external object is linked with a settlement, relink it with new external object
                acm_obj = FSwiftMLUtils.FSwiftExternalObject.get_acm_object_from_ext_object(prev_external_obj)
                if acm_obj:
                    FSwiftMLUtils.FSwiftExternalObject.unlink_acm_object(bpr)
                    FSwiftMLUtils.FSwiftExternalObject.link_acm_object(bpr, acm_obj)

                import FSecuritySettlementInProcessing
                state_obj = FSecuritySettlementInProcessing.FSecuritySettlementStatusProcessingAdviceInProcessing(bpr)
                state_name = bpr.CurrentStep().State().Name()
                state_obj.call_process_state_flag = True

                state_callback = getattr(state_obj, 'process_state_%s' % (state_name.lower()), None)
                if state_callback:
                    state_callback()

        except Exception as e:
            notifier.ERROR("Exception occurred in ProcessMTMessage : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def UniquePair(self):
        """Lookup the unique identifier in the MT54X message and search for the specific settlement"""
        settlement_num = self.Identifier()
        if settlement_num:
            settlement_num = settlement_num.split('-')
            settlement_num = str(settlement_num[1] if len(settlement_num) > 1 else settlement_num[0])

        pair_object = acm.FSettlement[str(settlement_num)]
        if not pair_object:
            notifier.INFO('Settlement ' + str(settlement_num) + ' not found' + '\n' + self.SwiftData())
        return pair_object

    def IsSupportedMessageFunction(self):
        """check if the message type is supported"""
        if self._message_function:
            return True
        else:
            return False

    def AdjustFieldsToCompare(self, theirs_object, settlement_obj):
        ''' Use this swift data to modify the existing values on the object formed by acm object.'''
        pass

