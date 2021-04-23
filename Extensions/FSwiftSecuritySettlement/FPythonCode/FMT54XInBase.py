"""----------------------------------------------------------------------------
MODULE:
    FMT54XInBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it. User
    can extend/override the default mapping in derived class i.e. FMT544/545/546/547
    Base class for mapping attributes.
    Default logic for extracting attributes from either swift data or the
    settlement object.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MT54X message. It stores the incoming message in
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
import re

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FMTInBase
import FSwiftMLUtils
import FIntegrationUtils
import FSwiftMTBase


class FMT54XBase(FMTInBase.FMTInBase):
    """ Base class for MT54X mapping"""
    def __init__(self, source, direction, msg_type):
        super(FMT54XBase, self).__init__(source, direction)
        self.type = msg_type
        self.config_param = FSwiftMLUtils.Parameters('F%sIn_Config'%(self.type))

        self._settled_amount = None
        self._settled_date = None
        self._trade_date = None
        self._amount = None
        self._currency = None
        self._premium = None
        self._value_day = None
        self._safekeeping_account = None
        self._indicator = ''
        self._isin = None
        self._partial_indicator = 'None'
        self._internal_identifier = None
        self._settled_date_code = None
        self._trade_date_code = None
        self._value_day_code = None
        # Workaround fix for SPR 393260 start
        self._buyer_seller = None
        self._buyer_seller_account = None
        self._custodian = None
        self._custodian_account = None
        self._intermediary1 = None
        self._intermediary1_account = None
        self._intermediary2 = None
        self._intermediary2_account = None
        self._agent = None
        self._agent_account = None
        self._place_of_settlement = None
        # Workaround fix for SPR 393260 end

        self._buyer_seller_prop_code = None
        self._custodian_prop_code = None
        self._agent_prop_code = None
        self._intermediary1_prop_code = None
        self._intermediary2_prop_code = None

        self._buyer_seller_data_source_scheme = None
        self._custodian_data_source_scheme = None
        self._agent_data_source_scheme = None
        self._intermediary1_data_source_scheme = None
        self._intermediary2_data_source_scheme = None

        #################################################

        self._buyer_seller_extended = None
        self._buyer_seller_account_extended = None
        self._buyer_seller_prop_code_extended = None
        self._buyer_seller_data_source_scheme_extended = None

        self._custodian_extended = None
        self._custodian_account_extended = None
        self._custodian_prop_code_extended = None
        self._custodian_data_source_scheme_extended = None

        self._intermediary1_extended = None
        self._intermediary1_account_extended = None
        self._intermediary1_prop_code_extended = None
        self._intermediary1_data_source_scheme_extended = None

        self._intermediary2_extended = None
        self._intermediary2_account_extended = None
        self._intermediary2_prop_code_extended = None
        self._intermediary2_data_source_scheme_extended = None

        self._agent_extended = None
        self._agent_account_extended = None
        self._agent_prop_code_extended = None
        self._agent_data_source_scheme_extended = None

# ------------------------------------------------------------------------------

    def getAccountDataSourceScheme(self, account, dssItem):
        dss_func = getattr(account, dssItem, None)

        if dss_func is not None:
            func = dss_func()
            if func:
                return func.Alias()
        else:
            dss_func = getattr(account, dssItem+'ChlItem', None)
            if dss_func is not None:
                func = dss_func()
                if func:
                    return func.Name()

    def getAlternateDSS(self, correspondent_bank):
        if correspondent_bank is not None:
            partyAlias = correspondent_bank.PartyAlias()
            if partyAlias is not None:
                dss_func = getattr(partyAlias, 'DataSourceScheme', None)
                if dss_func:
                    return partyAlias.DataSourceScheme()
                else:
                    return ''

    def get_party_bic_dss(self, account):
        bic = ''
        dss = ''
        try:
            party = account.Party()
            bic = FSwiftMTBase.GetPartyBic(account)
            accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme')
            if accnt_dss:
                dss = accnt_dss
            else:
                dss = self.getAlternateDSS(account.CorrespondentBank())
        except Exception as e:
            notifier.ERROR("Exception occurred in get_party_bic_dss : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

        return bic, dss


    def get_custodian_bic_dss(self, account):
        bic = ''
        dss = ''
        try:
            if account.CorrespondentBank3():
                if account.Bic():
                    bic = account.Bic().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme2')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank2())
        except Exception as e:
            notifier.ERROR("Exception occurred in get_custodian_bic_dss : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)
        return bic, dss

    def get_intermediery1_bic_dss(self, account):
        bic = ''
        dss = ''
        try:
            if account.CorrespondentBank5() or account.CorrespondentBank4():
                if account.CorrespondentBank4():
                    if account.Bic2():
                        bic = account.Bic2().Alias()

                    accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme3')

                    if accnt_dss:
                        dss = accnt_dss
                    else:
                        dss = self.getAlternateDSS(account.CorrespondentBank3())
        except Exception as e:
            notifier.ERROR("Exception occurred in get_intermediery1_bic_dss : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)
        return bic, dss

    def get_intermediery2_bic_dss(self, account):
        bic = ''
        dss = ''
        try:
            if account.CorrespondentBank5():
                if account.Bic3():
                    bic = account.Bic3().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme4')

                if account.CorrespondentBank4() and accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank4())
        except Exception as e:
            notifier.ERROR("Exception occurred in get_intermediery2_bic_dss : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)
        return bic, dss

    def get_agent_bic_dss(self, account):
        bic = ''
        dss = ''
        try:
            if account.CorrespondentBank5():
                if account.Bic4():
                    bic = account.Bic4().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme5')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank5())
            elif account.CorrespondentBank4():
                if account.Bic3():
                    bic = account.Bic3().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme4')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank4())
            elif account.CorrespondentBank3():
                if account.Bic2():
                    bic = account.Bic2().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme3')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank3())
            elif account.CorrespondentBank2():
                if account.Bic():
                    bic = account.Bic().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme2')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    dss = self.getAlternateDSS(account.CorrespondentBank2())
            elif account.CorrespondentBank():
                if account.NetworkAlias():
                    bic = account.NetworkAlias().Alias()

                accnt_dss = self.getAccountDataSourceScheme(account, 'DataSourceScheme')

                if accnt_dss:
                    dss = accnt_dss
                else:
                    #dss = self.getAlternateDSS(account.Party())
                    dss = self.getAlternateDSS(account.CorrespondentBank())
        except Exception as e:
            notifier.ERROR("Exception occurred in get_agent_bic_dss : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)
        return bic, dss


    def SetAttributes(self):
        """ Set the attributes from incoming swift message/acm object to MT54X type"""
        try:
            if self.source == 'SWIFT':
                self.set_identifier()
                self.set_amounts()
                self.set_premium()
                self.set_value_settled_trade_day()
                self.set_party_details() # Workaround fix for SPR 393260
                self.set_safekeeping_account()
                self.set_isin()
                self.set_message_function()
                self.set_indicator()
                self.set_settlement_transaction_condition_indicator()
            elif self.source == 'ACM':
                self.set_identifier_from_settlement()
                self.set_amount_from_settlement()
                self.set_settled_amount_from_settlement()
                self.set_currency_from_settlement()
                self.set_premium_from_settlement()
                self.set_trade_date_from_settlement()
                self.set_value_day_from_settlement()
                self.set_party_details_from_settlement() # Workaround fix for SPR 393260
                self.set_safekeeping_account_from_settlement()
                self.set_isin_from_settlement()
                self.set_settlement_transaction_condition_indicator_from_settlement()
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
                    self._internal_identifier = str(related_ref_val)
                    self._identifier = str(related_ref_val)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identifier : %s"%str(e))

    def set_amounts(self):
        try:
            self._amount = 0.0
            self._settled_amount = 0.0

            for amt in self.python_object.SequenceC_FinancialInstrumentAccount.QuantityOfFinancialInstrument:
                amt = amt.value()
                qualifier = amt[0:5]

                if qualifier == ':ESTT':
                    self._settled_amount = FSwiftMLUtils.swiftmt_to_float(amt[12:])
                if qualifier in [':ESTT', ':RSTT']:
                    self._amount += FSwiftMLUtils.swiftmt_to_float(amt[12:])


            if self.type in ['MT547', 'MT546']:
                self._amount *= -1
                self._settled_amount *= -1

        except Exception as e:
            notifier.DEBUG("Exception occurred in set_amounts : %s"%str(e))

    def set_premium(self):
        try:
            for amt in self.python_object.SequenceE_SettlementDetails.SubSequenceE3_Amounts:
                for amount in amt.Amount:
                    amount = str(amount.value())
                    qualifier = amount[0:5]
                    if qualifier == ':ESTT':
                        sign_indicator = None
                        currency = None

                        premium_index = re.search('\d', amount).start()
                        premium = FSwiftMLUtils.swiftmt_to_float(amount[premium_index:])
                        curr_str = amount[7:premium_index]

                        if len(curr_str) == 4:
                            sign_indicator = curr_str[0]
                            currency = curr_str[1:]
                        else:
                            currency = curr_str

                        self._currency = currency
                        self._premium = premium

                        if self.type in ['MT545']:
                            if sign_indicator != 'N':
                                self._premium *= -1
                        elif self.type in ['MT547']:
                            if sign_indicator == 'N':
                                self._premium *= -1
                        break
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium : %s"%str(e))

    def set_settlement_transaction_condition_indicator(self):
        try:
            for indicator in self.python_object.SequenceE_SettlementDetails.Indicator:
                indicator_val = str(indicator.value())
                qualifier = indicator_val[0:5]
                if qualifier == ':STCO':
                    sett_transaction_condition_indicator = indicator_val[-4:]
                    self._partial_indicator = sett_transaction_condition_indicator
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_type_of_settlement_transaction_indicator : %s" % str(e))

    def set_value_settled_trade_day(self):
        try:
            for each_date in self.python_object.SequenceB_TradeDetails.DateTime_A:
                each_date = str(each_date.value())
                qualifier = each_date[0:5]
                if qualifier == ':ESET':
                    self._settled_date = FSwiftMLUtils.swiftmt_to_date(each_date[7:15])
                elif qualifier == ':SETT':
                    self._value_day = FSwiftMLUtils.swiftmt_to_date(each_date[7:15])
                elif qualifier == ':TRAD':
                    self._trade_date = FSwiftMLUtils.swiftmt_to_date(each_date[7:15])


            for each_date in self.python_object.SequenceB_TradeDetails.DateTime_C:
                each_date = str(each_date.value()).split('//')
                if len(each_date) > 1:
                    qualifier = each_date[0]
                    if qualifier == ':ESET':
                        self._settled_date = FSwiftMLUtils.swiftmt_to_date(each_date[1][:8])
                    elif qualifier == ':SETT':
                        self._value_day = FSwiftMLUtils.swiftmt_to_date(each_date[1][:8])
                    elif qualifier == ':TRAD':
                        self._trade_date = FSwiftMLUtils.swiftmt_to_date(each_date[1][:8])

            for each_date in self.python_object.SequenceB_TradeDetails.DateTime_B:
                each_date = str(each_date.value()).split('/')
                if len(each_date) > 2:
                    qualifier = each_date[0]
                    if qualifier == ':ESET':
                        self._settled_date_code = each_date[2]
                    elif qualifier == ':SETT':
                        self._value_day_code = each_date[2]
                    elif qualifier == ':TRAD':
                        self._trade_date_code = each_date[2]

            if not self._value_day:
                self._value_day = self._settled_date
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_value_settled_trade_day : %s"%str(e))

    def __set_party_from_qualifier(self, qualifier, pty_identifier):
        if not pty_identifier:
            return

        if self.Type() in ['MT546', 'MT547']:
            if qualifier in [':BUYR']:
                self._buyer_seller = pty_identifier
            elif qualifier in [':RECU']:
                self._custodian = pty_identifier
            elif qualifier in [':REAG']:
                self._agent = pty_identifier
            elif qualifier in [':REI1']:
                self._intermediary1 = pty_identifier
            elif qualifier in [':REI2']:
                self._intermediary2 = pty_identifier
        elif self.Type() in ['MT544', 'MT545']:
            if qualifier in [':SELL']:
                self._buyer_seller = pty_identifier
            elif qualifier in [':DECU']:
                self._custodian = pty_identifier
            elif qualifier in [':DEAG']:
                self._agent = pty_identifier
            elif qualifier in [':DEI1']:
                self._intermediary1 = pty_identifier
            elif qualifier in [':DEI2']:
                self._intermediary2 = pty_identifier
        if qualifier == ':PSET':
            self._place_of_settlement = pty_identifier

    def __set_party_account_from_qualifier(self, qualifier, pty_account):
        if not pty_account:
            return
        if self.Type() in ['MT546', 'MT547']:
            if qualifier in [':BUYR']:
                self._buyer_seller_account = pty_account
            elif qualifier in [':RECU']:
                self._custodian_account = pty_account
            elif qualifier in [':REAG']:
                self._agent_account = pty_account
            elif qualifier in [':REI1']:
                self._intermediary1_account = pty_account
            elif qualifier in [':REI2']:
                self._intermediary2_account = pty_account
        elif self.Type() in ['MT544', 'MT545']:
            if qualifier in [':SELL']:
                self._buyer_seller_account = pty_account
            elif qualifier in [':DECU']:
                self._custodian_account = pty_account
            elif qualifier in [':DEAG']:
                self._agent_account = pty_account
            elif qualifier in [':DEI1']:
                self._intermediary1_account = pty_account
            elif qualifier in [':DEI2']:
                self._intermediary2_account = pty_account

    def __set_prop_code_from_qualifier(self, qualifier, prop_code):
        if not prop_code:
            return
        if self.Type() in ['MT546', 'MT547']:
            if qualifier in [':BUYR']:
                self._buyer_seller_prop_code = prop_code
            elif qualifier in [':RECU']:
                self._custodian_prop_code = prop_code
            elif qualifier in [':REAG']:
                self._agent_prop_code = prop_code
            elif qualifier in [':REI1']:
                self._intermediary1_prop_code = prop_code
            elif qualifier in [':REI2']:
                self._intermediary2_prop_code = prop_code
        elif self.Type() in ['MT544', 'MT545']:
            if qualifier in [':SELL']:
                self._buyer_seller_prop_code = prop_code
            elif qualifier in [':DECU']:
                self._custodian_prop_code = prop_code
            elif qualifier in [':DEAG']:
                self._agent_prop_code = prop_code
            elif qualifier in [':DEI1']:
                self._intermediary1_prop_code = prop_code
            elif qualifier in [':DEI2']:
                self._intermediary2_prop_code = prop_code

    def __set_data_source_scheme_from_qualifier(self, qualifier, dss):
        if not dss:
            return
        if self.Type() in ['MT546', 'MT547']:
            if qualifier in [':BUYR']:
                self._buyer_seller_data_source_scheme = dss
            elif qualifier in [':RECU']:
                self._custodian_data_source_scheme = dss
            elif qualifier in [':REAG']:
                self._agent_data_source_scheme = dss
            elif qualifier in [':REI1']:
                self._intermediary1_data_source_scheme = dss
            elif qualifier in [':REI2']:
                self._intermediary2_data_source_scheme = dss
        elif self.Type() in ['MT544', 'MT545']:
            if qualifier in [':SELL']:
                self._buyer_seller_data_source_scheme = dss
            elif qualifier in [':DECU']:
                self._custodian_data_source_scheme = dss
            elif qualifier in [':DEAG']:
                self._agent_data_source_scheme = dss
            elif qualifier in [':DEI1']:
                self._intermediary1_data_source_scheme = dss
            elif qualifier in [':DEI2']:
                self._intermediary2_data_source_scheme = dss


    def set_party_details(self):
        try:
            for setPty in self.python_object.SequenceE_SettlementDetails.SubSequenceE1_SettlementParties:
                qualifier = ''
                pty_identifier = ''
                pty_account = ''
                # For party with option P
                for pty in setPty.PARTY_P:
                    pty = str(pty.value())
                    qualifier = pty[0:5]
                    pty_identifier = pty[7:]
                    self.__set_party_from_qualifier(qualifier, pty_identifier)

                # For party with option R
                for pty in setPty.PARTY_R:
                    pty = str(pty.value())
                    qualifier = pty[0:5]
                    data_source_and_prop_code = pty[6:].split('/', 1)
                    data_source_scheme = data_source_and_prop_code[0] if len(data_source_and_prop_code) > 0 else ''
                    prop_code = data_source_and_prop_code[1] if len(data_source_and_prop_code) > 1 else ''
                    self.__set_data_source_scheme_from_qualifier(qualifier, data_source_scheme)
                    self.__set_prop_code_from_qualifier(qualifier, prop_code)

                # For for the account field
                if setPty.SafekeepingAccount_A :
                    pty_account = str(setPty.SafekeepingAccount_A.value())
                    pty_account = pty_account[7:] if len(pty_account) > 6 else ''
                    self.__set_party_account_from_qualifier(qualifier, pty_account)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_parties_from_swift : %s"%str(e))

    def set_safekeeping_account(self):
        try:
            for act in self.python_object.SequenceC_FinancialInstrumentAccount.Account_A:
                self._safekeeping_account = str(act.value()[7:])
                break
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_safekeeping_account : %s"%str(e))

    def set_isin(self):
        try:
            self._isin = ''
            financialIdentifier = str(self.python_object.SequenceB_TradeDetails.IdentificationOfFinancialInstrument.value())
            if len(financialIdentifier) > 4 and financialIdentifier[0:4] == 'ISIN':
                self._isin = financialIdentifier[5:17]
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_isin : %s"%str(e))

    def set_message_function(self):
        try:
            self._message_function = str(self.python_object.SequenceA_GeneralInformation.FunctionOfMessage.value()[:4])
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_message_function : %s"%str(e))

    def set_indicator(self):
        try:
            if self.python_object.SequenceA_GeneralInformation.Indicator_F:
                for indicator in self.python_object.SequenceA_GeneralInformation.Indicator_F:
                    self._indicator = str(indicator.value())
                    break
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_indicator : %s"%str(e))

# ------------------------------------------------------------------------------
    # Method to fetch data from the adm
    def set_identifier_from_settlement(self):
        try:
            self._identifier = self.acm_obj.Oid()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_identifier_from_settlement : %s"%str(e))

    def set_amount_from_settlement(self):
        try:
            self._amount = self.acm_obj.Amount()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_amount_from_settlement : %s"%str(e))

    def set_settled_amount_from_settlement(self):
        try:
            self._settled_amount = self.acm_obj.Amount()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_amount_from_settlement : %s"%str(e))

    def set_currency_from_settlement(self):
        try:
            get_currency = getattr(self.acm_obj, "CashCurrency", None)
            if get_currency is not None:
                if get_currency() is not None:
                    self._currency = get_currency().Name()

            if self._currency is None:
                self._currency = self.acm_obj.Currency().Name()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_currency_from_settlement : %s"%str(e))

    def set_premium_from_settlement(self):
        try:
            self._premium = self.acm_obj.CashAmount()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_premium_from_settlement : %s"%str(e))

    def set_value_day_from_settlement(self):
        try:
            self._value_day = self.acm_obj.ValueDay()
        except Exception as e:
            notifier.ERROR("Exception occurred in set_value_day_from_settlement : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def _GetTradeValueDays(self, settlement, allDates):
        if settlement.Trade():
            allDates.add(acm.Time.AsDate(settlement.Trade().TradeTime()))
        else:
            for s in settlement.Children():
                self._GetTradeValueDays(s, allDates)
            if settlement.SplitParent():
                self._GetTradeValueDays(settlement.SplitParent(), allDates)

    def GetTradeDatetimeDate(self, settlement):
        allDates = set()
        self._GetTradeValueDays(settlement, allDates)
        return sorted(allDates, reverse=True).pop()

    def set_trade_date_from_settlement(self):
        try:
            self._trade_date = self.GetTradeDatetimeDate(self.acm_obj)
        except Exception as e:
            notifier.DEBUG(str(e), exc_info=1)
            notifier.ERROR("Exception occurred in set_trade_date_from_settlement : %s"%str(e))

    def get_module_handle(self):
        module = ''
        try:
            utils_obj = FIntegrationUtils.FIntegrationUtils()
            outgoing_mt_type = FSwiftMLUtils.calculate_mt_type_from_acm_object(self.acm_obj)
            module = utils_obj.import_module_from_string('FSwiftMT%s' % str(outgoing_mt_type))
        except Exception as e:
            notifier.DEBUG("Exception occurred in get_module_handle : %s"%str(e))
        return module

    def find_bic_dss_from_qualifier(self, acm_obj, qualifier, accountOrPropCode):
        bic = ''
        dss = ''
        counterPartyAccountRef = acm_obj.CounterpartyAccountRef()

        if qualifier in ['SELL', 'BUYR']:
            bic, dss = self.get_party_bic_dss(counterPartyAccountRef)
            self._buyer_seller_extended = bic
            self._buyer_seller_data_source_scheme_extended = dss
            self._buyer_seller_prop_code_extended = self._buyer_seller_account_extended = accountOrPropCode
        elif qualifier in ['DECU', 'RECU']:
            bic, dss = self.get_custodian_bic_dss(counterPartyAccountRef)
            self._custodian_extended = bic
            self._custodian_data_source_scheme_extended = dss
            self._custodian_account_extended = self._custodian_prop_code_extended = accountOrPropCode
        elif qualifier in ['DEI1', 'REI1']:
            bic, dss = self.get_intermediery1_bic_dss(counterPartyAccountRef)
            self._intermediary1_extended = bic
            self._intermediary1_data_source_scheme_extended = dss
            self._intermediary1_account_extended = self._intermediary1_prop_code_extended = accountOrPropCode
        elif qualifier in ['DEI2', 'REI2']:
            bic, dss = self.get_intermediery2_bic_dss(counterPartyAccountRef)
            self._intermediary2_extended = bic
            self._intermediary2_data_source_scheme_extended = dss
            self._intermediary2_account_extended = self._intermediary2_prop_code_extended = accountOrPropCode
        elif qualifier in ['DEAG', 'REAG']:
            bic, dss = self.get_agent_bic_dss(counterPartyAccountRef)
            self._agent_extended = bic
            self._agent_data_source_scheme_extended = dss
            self._agent_account_extended = self._agent_prop_code_extended = accountOrPropCode

        return bic, dss


    def set_party_details_from_settlement(self):
        try:
            party_details = None
            try:
                import FSwiftOperationsAPI
                party_details = FSwiftOperationsAPI.GetPartyDetails(self.acm_obj)
            except (ImportError, AttributeError):
                module = self.get_module_handle()
                party_details = module.GetPartyDetails(self.acm_obj)
            for each_party_detail in party_details:
                pty_accnt_ext = None
                qualifier = each_party_detail.At('qualifier')
                pty_identifier = each_party_detail.At('bic')

                self.__set_party_from_qualifier(':'+qualifier, pty_identifier)

                pty_account = each_party_detail.At('safekeepingaccount')
                self.__set_party_account_from_qualifier(':'+qualifier, pty_account)

                if pty_account:
                    pty_accnt_ext = pty_account

                pty_account = each_party_detail.At('partyproprietarycode')

                if pty_account:
                    pty_accnt_ext = pty_account

                if pty_account:
                    self.__set_prop_code_from_qualifier(':'+qualifier, pty_account)

                data_source_scheme = each_party_detail.At('datasourcescheme')

                if data_source_scheme:
                    self.__set_data_source_scheme_from_qualifier(':'+qualifier, data_source_scheme)

                bic, dss = self.find_bic_dss_from_qualifier(self.acm_obj, qualifier, pty_accnt_ext)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_parties_from_settlement : %s"%str(e))

    def set_safekeeping_account_from_settlement(self):
        try:
            try:
                import FSwiftOperationsAPI
                self._safekeeping_account = FSwiftOperationsAPI.GetAccountNumber(self.acm_obj)
            except (ImportError, AttributeError):
                module = self.get_module_handle()
                self._safekeeping_account = module.GetAccountNumber(self.acm_obj)
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_safekeeping_account_from_settlement : %s"%str(e))

    def set_isin_from_settlement(self):
        try:
            #SecurityInstrument is used to make sure that all instrument types are handled  like
            #Repo . SecurityInstrument returns reference to underlying instrument
            if self.acm_obj.SecurityInstrument() and self.acm_obj.SecurityInstrument().Isin():
                self._isin = self.acm_obj.SecurityInstrument().Isin()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_isin_from_settlement : %s"%str(e))

    def set_settlement_transaction_condition_indicator_from_settlement(self):
        try:
            if self.acm_obj:
                self._partial_indicator = self.acm_obj.PartialSettlementType()
        except Exception as e:
            notifier.DEBUG("Exception occurred in set_settlement_transaction_condition_indicator_from_settlement : %s"%str(e))

# ------------------------------------------------------------------------------
    # Method to fetch data used in the Pairing and Matching attributes in the FParameter
    def Type(self):
        """ Get the type of the MT message"""
        return self.type

    def SettledAmount(self):
        """ Get the settled amount attribute"""
        return self._settled_amount

    def SettledDate(self):
        """ Get the settled date attribute"""
        return self._settled_date

    def Amount(self):
        """ Get the amount attribute"""
        return self._amount

    def Currency(self):
        """ Get the currency attribute"""
        return self._currency

    def Premium(self):
        """ Get the premium attribute"""
        return self._premium

    def ValueDate(self):
        """ Get the value date attribute"""
        return self._value_day

    def SafekeepingAccount(self):
        """ Get the safekeeping account number attribute"""
        return self._safekeeping_account

    def Isin(self):
        """ Get the isin attribute"""
        return self._isin

    def Indicator(self):
        """ Get the indicator attribute"""
        return self._indicator

    def Partial(self):
        """Get the partial attribute"""
        return self._partial_indicator

    def TradeDate(self):
        """Get the Trade Date attribute"""
        return self._trade_date

    def BuyerSeller(self):
        """Get the Buyer Seller attribute"""
        return self._buyer_seller

    def Custodian(self):
        """Get the Custodian attribute"""
        return self._custodian

    def Intermediary1(self):
        """Get the Intermediary1 attribute"""
        return self._intermediary1

    def Intermediary2(self):
        """Get the Intermediary2 attribute"""
        return self._intermediary2

    def Agent(self):
        """Get the Agent attribute"""
        return self._agent

    def PlaceOfSettlement(self):
        """Get the PlaceOfSettlement attribute"""
        return self._place_of_settlement

    def BuyerSellerAccount(self):
        """Get the Buyer Seller account attribute"""
        return self._buyer_seller_account

    def CustodianAccount(self):
        """Get the Custodian account attribute"""
        return self._custodian_account

    def Intermediary1Account(self):
        """Get the Intermediary1 account attribute"""
        return self._intermediary1_account

    def Intermediary2Account(self):
        """Get the Intermediary2 account attribute"""
        return self._intermediary2_account

    def AgentAccount(self):
        """Get the Agent account attribute"""
        return self._agent_account

    def BuyerSellerDSS(self):
        return self._buyer_seller_data_source_scheme

    def BuyerSellerPropCode(self):
        return self._buyer_seller_prop_code

    def CustodianDSS(self):
        return self._custodian_data_source_scheme

    def CustodianPropCode(self):
        return self._custodian_prop_code

    def Intermediary1DSS(self):
        return self._intermediary1_data_source_scheme

    def Intermediary1PropCode(self):
        return self._intermediary1_prop_code

    def Intermediary2DSS(self):
        return self._intermediary2_data_source_scheme

    def Intermediary2PropCode(self):
        return self._intermediary2_prop_code

    def AgentDSS(self):
        return self._agent_data_source_scheme

    def AgentPropCode(self):
        return self._agent_prop_code
# ------------------------------------------------------------------------------

    def InternalIdentifier(self):
        return self._internal_identifier

    def ProcessMTMessage(self, msg_id):
        """ process the incoming mt message"""
        notifier.INFO("Processing incoming %s message."%(self.type))
        try:
            value_dict = {'swift_data':self.swift_data}
            #external_obj = FSwiftMLUtils.create_external_object(value_dict, self.Type(), 'Settlement',  acm_obj, 'Incoming')
            #reconciliation_item = external_obj.ReconciliationItem()
            external_obj = FSwiftMLUtils.FSwiftExternalObject.create_external_object(value_dict, message_typ=self.Type(), channel_id=msg_id, subject_typ='Settlement', ext_ref=self.InternalIdentifier(), in_or_out="Incoming")
            reconciliation_item = FSwiftMLUtils.FSwiftExternalObject.subject_for_business_process(external_obj)

            #create a business process on the external item
            sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(self.Type(), 'In')

            bpr = FSwiftMLUtils.get_or_create_business_process(external_obj, sc, self.Type())
            if bpr:
                notifier.INFO('Initialized : Business process id <%i> with state chart <%s> on %s <%i>' \
                                      %(bpr.Oid(), sc, reconciliation_item.ClassName(), reconciliation_item.Oid()))
        except Exception as e:
            notifier.ERROR("Exception occurred in ProcessMTMessage : %s"%str(e))
            notifier.DEBUG(str(e), exc_info=1)

    def UniquePair(self):
        """Lookup the unique identifier in the MT54X message and search for the specific settlement"""
        pair_object = None
        if self.Type() in ['MT544', 'MT545', 'MT546', 'MT547']:
            #settlement_num = self.Identifier()
            settlement_num = self.Identifier().split('-')[0] if len(self.Identifier().split('-')) == 1 else self.Identifier().split('-')[1]
            pair_object = acm.FSettlement[str(settlement_num)]
            if not pair_object:
                notifier.INFO('Settlement ' + str(settlement_num) + ' not found' + '\n' + self.SwiftData())
        return pair_object

    def IsSupportedMessageFunction(self):
        """check if the message type is supported"""
        return self._message_function == "NEWM"

    def IsSecurityTransfer(self):
        """Return True if incoming message represents Security transfer"""
        is_security_transfer = False
        if self.BuyerSeller() == 'XXX':
            is_security_transfer = True
        return is_security_transfer

    def IsExchangeTradeRepoConfirmation(self):
        """There can not be a default implementation for this because to decide if its an exchange traded repo confirmation
           or not will be based on the BIC in field 95P for BUYR or SELLR"""
        return False

    def RepoCompareTolerance(self):
        """Tolerance used for comparing repo amounts.This can be configured by user. This method should return a integer/float as string"""
        return '0.01'

    def AdjustFieldsToCompare(self, theirs_object, settlement_obj):
        ''' Use this swift data to modify the existing values on the object formed by acm object.'''
        if theirs_object.BuyerSeller() != None or theirs_object.BuyerSellerDSS() != None:
            if None != theirs_object.BuyerSeller():
                self._buyer_seller = self._buyer_seller_extended
                self._buyer_seller_account = self._buyer_seller_account_extended
                self._buyer_seller_data_source_scheme = None
                self._buyer_seller_prop_code = None
            else:
                self._buyer_seller = None
                self._buyer_seller_account = None
                self._buyer_seller_data_source_scheme = self._buyer_seller_data_source_scheme_extended
                self._buyer_seller_prop_code = self._buyer_seller_prop_code_extended

        if theirs_object.Custodian() != None or theirs_object.CustodianDSS() != None:
            if theirs_object.Custodian() != None:
                self._custodian = self._custodian_extended
                self._custodian_account = self._custodian_account_extended
                self._custodian_data_source_scheme = None
                self._custodian_prop_code = None
            else:
                self._custodian_data_source_scheme = self._custodian_data_source_scheme_extended
                self._custodian_prop_code = self._custodian_prop_code_extended
                self._custodian = None
                self._custodian_account = None

        if theirs_object.Intermediary1() != None or theirs_object.Intermediary1DSS() != None:
            if theirs_object.Intermediary1() != None:
                self._intermediary1 = self._intermediary1_extended
                self._intermediary1_account = self._intermediary1_account_extended
                self._intermediary1_data_source_scheme = None
                self._intermediary1_prop_code = None
            else:
                self._intermediary1_data_source_scheme = self._intermediary1_data_source_scheme_extended
                self._intermediary1_prop_code = self._intermediary1_prop_code_extended
                self._intermediary1 = None
                self._intermediary1_account = None

        if theirs_object.Intermediary2() != None or theirs_object.Intermediary2DSS() != None:
            if theirs_object.Intermediary2() != None:
                self._intermediary2 = self._intermediary2_extended
                self._intermediary2_account = self._intermediary2_account_extended
                self._intermediary2_data_source_scheme = None
                self._intermediary2_prop_code = None
            else:
                self._intermediary2_data_source_scheme = self._intermediary2_data_source_scheme_extended
                self._intermediary2_prop_code = self._intermediary2_prop_code_extended
                self._intermediary2 = None
                self._intermediary2_account = None

        if theirs_object.Agent() != None or theirs_object.AgentDSS() != None:
            if theirs_object.Agent() != None:
                self._agent = self._agent_extended
                self._agent_account = self._agent_account_extended
                self._agent_data_source_scheme = None
                self._agent_prop_code = None
            else:
                self._agent_data_source_scheme = self._agent_data_source_scheme_extended
                self._agent_prop_code = self._agent_prop_code_extended
                self._agent = None
                self._agent_account = None



    @staticmethod
    def GetColumnMetaData():
        column_metadata = {
            'Identifier': {'THEIRS_SWIFT_TAG' : '20C', 'OURS_SWIFT_TAG' : '20C', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'MessageFunction': {'THEIRS_SWIFT_TAG' : '23G', 'OURS_SWIFT_TAG' : '23G', 'SEQUENCE': 'General Information', 'COLOR': ''},
            'Indicator': {'THEIRS_SWIFT_TAG' : '22A', 'OURS_SWIFT_TAG' : '22A', 'SEQUENCE': 'General Information', 'COLOR': ''},

            'SettledDate': {'THEIRS_SWIFT_TAG' : '98A', 'OURS_SWIFT_TAG' : '98A', 'SEQUENCE': 'Trade Details', 'COLOR': '', 'FORMAT': 'DateOnly'},
            'ValueDate': {'THEIRS_SWIFT_TAG' : '98A', 'OURS_SWIFT_TAG' : '98A', 'SEQUENCE': 'Trade Details', 'COLOR': '', 'FORMAT': 'DateOnly'},
            'TradeDate': {'THEIRS_SWIFT_TAG' : '98A', 'OURS_SWIFT_TAG' : '98A', 'SEQUENCE': 'Trade Details', 'COLOR': '', 'FORMAT': 'DateOnly'},
            'Isin': {'THEIRS_SWIFT_TAG' : '35B', 'OURS_SWIFT_TAG' : '35B', 'SEQUENCE': 'Trade Details', 'COLOR': ''},

            'SettledAmount': {'THEIRS_SWIFT_TAG' : '36B', 'OURS_SWIFT_TAG' : '36B', 'SEQUENCE': 'Financial Instrument/Account', 'COLOR': '', 'FORMAT':'NumDefault'},
            'Amount': {'THEIRS_SWIFT_TAG' : '36B', 'OURS_SWIFT_TAG' : '36B', 'SEQUENCE': 'Financial Instrument/Account', 'COLOR': ''},
            'SafekeepingAccount': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Financial Instrument/Account', 'COLOR': ''},

            'Partial': {'THEIRS_SWIFT_TAG' : '22F', 'OURS_SWIFT_TAG' : '22F', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Premium': {'THEIRS_SWIFT_TAG' : '19A', 'OURS_SWIFT_TAG' : '19A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Currency': {'THEIRS_SWIFT_TAG' : '19A', 'OURS_SWIFT_TAG' : '19A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'BuyerSeller': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'BuyerSellerAccount': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Custodian': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'CustodianAccount': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Intermediary1': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Intermediary1Account': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Intermediary2': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Intermediary2Account': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Agent': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'AgentAccount': {'THEIRS_SWIFT_TAG' : '97A', 'OURS_SWIFT_TAG' : '97A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'PlaceOfSettlement': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'BuyerSellerDSS': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'BuyerSellerPropCode': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'AgentDSS': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'AgentPropCode': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'CustodianDSS': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'CustodianPropCode': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Intermediary1DSS': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Intermediary1PropCode': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            'Intermediary2DSS': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},
            'Intermediary2PropCode': {'THEIRS_SWIFT_TAG' : '95A', 'OURS_SWIFT_TAG' : '95A', 'SEQUENCE': 'Settlement Details', 'COLOR': ''},

            }
        return column_metadata

    @staticmethod
    def GetColumnNamePrefix():
        return 'MT54X'

