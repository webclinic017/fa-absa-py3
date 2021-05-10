"""----------------------------------------------------------------------------
MODULE:
    FMT535InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it. User
    can extend/override the default mapping in derived class i.e. FMT535
    Base class for mapping attributes.
    Default logic for extracting attributes from either swift data or the
    settlement object.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MT535 message. It stores the incoming message in
        FExternalItem and creates the business process on it.

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


class FMT535Base(FMTInBase.FMTInBase):
    """ Base class for MT535 mapping"""

    def __init__(self, source, direction, msg_type):
        super(FMT535Base, self).__init__(source, direction)
        self.type = msg_type
        self.config_param = FSwiftMLUtils.Parameters('F%sIn_Config' % (self.type))
        self._senders_message_reference = None
        self._message_function = None
        self._sub_function = None
        self._indicator = None
        self._identification_of_financial_instrument = None
        self._date_time = None
        self._balance = None
        self._internal_identifier = None
        self._safe_keeping_account = None



    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT535 type"""
        try:
            if self.source == 'SWIFT':
                self.set_senders_message_reference()
                self.set_function_of_message()
                self.set_identification_of_financial_instrument()
                self.set_balance()
                self.set_indicator()
                self.set_date_time()
                self.set_safekeeping_acount()
                # self.set_balance()

        except Exception as e:
            notifier.ERROR("Exception occurred in SetAttributes : %s" % str(e))
            notifier.DEBUG(str(e), exc_info=1)

    # Methods to fetch data from the swift message
    def set_senders_message_reference(self):
        """ Sets senders message reference """
        try:
            value = str(self.python_object.SequenceA_GeneralInformation.SendersMessageReference.value())
            self._internal_identifier = None
            if value and 'SEME//' == value[1:7]:
                self._internal_identifier = value[7:]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_senders_message_reference : %s" % str(e))

    def set_function_of_message(self):
        """ Sets the function of message """
        try:
            value = self.python_object.SequenceA_GeneralInformation.FunctionOfMessage.value()
            if value:
                value = value.split('/')
                if str(value[0]) == 'NEWM':
                    self._message_function = str(value[0])
                sub_value = value[-1]
                if sub_value and sub_value in ['CODU', 'COPY', 'DUPL']:
                    self._sub_function = sub_value
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_function_of_message : %s" % str(e))

    def set_identification_of_financial_instrument(self):
        """ Sets the identification of financial instrument from field """
        try:
            identification_of_financial_instrument = []
            for each_SequenceB_SubSafekeepingAccount in self.python_object.SequenceB_SubSafekeepingAccount:
                for each_SubsequenceB1_FinancialInstrument in each_SequenceB_SubSafekeepingAccount.SubsequenceB1_FinancialInstrument:
                    if each_SubsequenceB1_FinancialInstrument.IdentificationOfFinancialInstrument:
                        identification_of_financial_instrument.append(
                            str(each_SubsequenceB1_FinancialInstrument.IdentificationOfFinancialInstrument.value()))
            self._identification_of_financial_instrument = identification_of_financial_instrument

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identification_of_financial_instrument : %s" % str(e))

    def set_balance(self):
        """ Get values from field and set balance """
        try:
            identification_of_financial_instrument_vs_balance = {}

            for each_SequenceB_SubSafekeepingAccount in self.python_object.SequenceB_SubSafekeepingAccount:
                for each_SubsequenceB1_FinancialInstrument in each_SequenceB_SubSafekeepingAccount.SubsequenceB1_FinancialInstrument:
                    balance_dict = {}
                    for balance in each_SubsequenceB1_FinancialInstrument.Balance:
                        if 'AGGR' in balance.value():
                            balance = balance.value()
                            if 'UNIT' in balance:
                                quantity = balance.split('UNIT/')[-1]
                                quantity = quantity.strip(',')
                                balance_dict['UNIT'] = str(quantity)
                            elif 'FAMT' in balance:
                                quantity = balance.split('FAMT/')[-1]
                                quantity = quantity.strip(',')
                                balance_dict['FAMT'] = str(quantity)


                    if each_SubsequenceB1_FinancialInstrument.IdentificationOfFinancialInstrument:
                        identification_of_ins_field_content = each_SubsequenceB1_FinancialInstrument.IdentificationOfFinancialInstrument.value()
                        identification_of_ins_field_content = identification_of_ins_field_content.split('ISIN')
                        isin = identification_of_ins_field_content[1]
                        isin = str(isin.split('\n')[0].strip())
                        identification_of_financial_instrument_vs_balance[isin] = balance_dict
                    self.identification_of_financial_instrument_vs_balance = identification_of_financial_instrument_vs_balance

        except Exception as e:
            notifier.DEBUG("Exception occurred in identification_of_financial_instrument_vs_balance : %s" % str(e))


    def set_indicator(self):
        """ Get values from Field 22F and set it """
        try:
            # check for SETT , if present only then processing to be continued -22F
            if self.python_object.SequenceA_GeneralInformation.Indicator:
                indicator_list = []
                for indicator in self.python_object.SequenceA_GeneralInformation.Indicator:
                    indicator_list.append(indicator.value())

                sett_indicator_list = []
                for each_indicator in indicator_list:
                    if 'SETT' in each_indicator:
                        sett_indicator_list.append(str(each_indicator))

                self._indicator = sett_indicator_list


        except Exception as e:
            notifier.DEBUG("Exception occurred in set_indicator : %s" % str(e))

    def set_date_time(self):
        """ Get values from Field 98a and set it """
        try:
            # logic modify check for 'STAT' only then use values - 98a
            if self.python_object.SequenceA_GeneralInformation.DateTime_A:
                date_time_list = []
                if self.python_object.SequenceA_GeneralInformation.DateTime_A:
                    date_time_tag = self.python_object.SequenceA_GeneralInformation.DateTime_A
                elif self.python_object.SequenceA_GeneralInformation.DateTime_C:
                    date_time_tag = self.python_object.SequenceA_GeneralInformation.DateTime_C
                elif self.python_object.SequenceA_GeneralInformation.DateTime_E:
                    date_time_tag = self.python_object.SequenceA_GeneralInformation.DateTime_E
                for date_time in date_time_tag:
                    date_time_list.append(str(date_time.value()))
                stat_date_time = None
                for date_time in date_time_list:
                    if 'STAT' in date_time:
                        stat_date_time = date_time
                self._date_time = stat_date_time
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_date_time : %s" % str(e))

    def set_safekeeping_acount(self):
        """ Get values from field """
        try:
            if self.python_object.SequenceA_GeneralInformation.SafekeepingAccount_A:
                self._safe_keeping_account = self.python_object.SequenceA_GeneralInformation.SafekeepingAccount_A.value()
            elif self.python_object.SequenceA_GeneralInformation.SafekeepingAccount_B:
                self._safe_keeping_account = self.python_object.SequenceA_GeneralInformation.SafekeepingAccount_B.value()

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_safekeeping_acount : %s" % str(e))

    def Isin(self):
        """ Return the isin list from identification of financial instrument """
        isin_list = []
        for each_identification in self._identification_of_financial_instrument:
            identification_of_ins_field_content = each_identification.split('ISIN')
            isin = identification_of_ins_field_content[1]
            isin = isin.split('\n')[0].strip()
            isin_list.append(isin)
        return isin_list

    # ------------------------------------------------------------------------------

    def Type(self):
        """ Get the type of the MT message"""
        return self.type

    def Identifier(self):
        """ Get the identifier """
        return self._identifier

    def Counterparty(self):
        """ Get counterparty from account details """
        counterparty = ''
        try:
            counterparty_account = self._safe_keeping_account.split('//')[-1]
            account = acm.FAccount.Select01('account=%s' % str(counterparty_account), None)
            if account:
                counterparty = account.Party().Name()
            else:
                notifier.WARN("Account <%s> does not exist in ADS" % counterparty_account)
        except Exception as e:
            notifier.ERROR("Error while getting counterparty")
        return counterparty

    def DateTime(self):
        """ Get date time """
        self._date_time = self._date_time.split('//')[-1]
        return self._date_time

    def Quantity(self):
        """ Get quantity """
        quantity_dict = {}
        if self.identification_of_financial_instrument_vs_balance:
            for isin, quantity in list(self.identification_of_financial_instrument_vs_balance.items()):
                for qualifier, balance in list(quantity.items()):
                    if 'UNIT' in qualifier:
                        quantity_dict[isin] = balance
        return quantity_dict

    def FaceValue(self):
        """ Get facevalue """
        facevalue_dict = {}
        if self.identification_of_financial_instrument_vs_balance:
            for isin, quantity in list(self.identification_of_financial_instrument_vs_balance.items()):
                for qualifier, balance in list(quantity.items()):
                    if 'FAMT' in qualifier:
                        facevalue_dict[isin] = balance
        return facevalue_dict

    def Custodian(self):
        """ Get the custodian details from the MT message"""
        sender_bic = None
        try:
            first_block = self.swift_data[0: self.swift_data.find('}') + 1]
            first_block_details = first_block[first_block.find(':'):]
            sender_bic = first_block_details[4: 15]  # getting only th bic out from the message
        except Exception as e:
            notifier.ERROR("Error while retrieving the custodian BIC from header part of message <%s>" % first_block)

        return FSwiftMLUtils.get_party_from_bic(sender_bic)

    def FunctionOfMessage(self):
        return self._message_function

    # ------------------------------------------------------------------------------

    def InternalIdentifier(self):
        """ Returns the internal identifier """
        return self._internal_identifier

    def ProcessMTMessage(self, msg_id):
        """ Process the incoming mt message"""
        notifier.INFO("Processing incoming %s message." % self.Type())
        try:
            value_dict = {'swift_data': self.swift_data}
            if not FSwiftMLUtils.check_if_externalobject_for_message_already_exists(self.InternalIdentifier()):

                external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict,
                                                                                         message_typ=self.Type(),
                                                                                         channel_id=msg_id,
                                                                                         subject_typ='Trade',
                                                                                         ext_ref=self.InternalIdentifier(),
                                                                                         in_or_out="Incoming")
                reconciliation_item = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)

                # Create a business process on the external item
                sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type())
                bpr = FSwiftMLUtils.get_or_create_business_process(external_obj, sc, self.Type())
                if bpr:
                    notifier.INFO('Initialized : Business process id <%i> with state chart <%s> on %s <%i>' \
                                  % (bpr.Oid(), sc, reconciliation_item.ClassName(), reconciliation_item.Oid()))

            else:
                external_object = FSwiftMLUtils.check_if_externalobject_for_message_already_exists(self.InternalIdentifier())
                bpr = FSwiftMLUtils.FSwiftExternalObject.get_business_process_from_external_object(external_object)
                notifier.ERROR('This Statement of holding with External Ref <%s> already exists with External Object <%s> and BPR <%s>. Hence this message will not be processed.'%(self.InternalIdentifier(), external_object.Oid(), bpr.Oid()))


        except Exception as e:
            notifier.ERROR("Exception occurred in ProcessMTMessage : %s" % str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def IsSupportedMessageFunction(self):
        """ Check if the message type is supported"""
        if self._message_function:

            return True
        else:
            return False

    def AdjustFieldsToCompare(self, theirs_object, settlement_obj):
        """ Use this swift data to modify the existing values on the object formed by acm object. """
        pass

