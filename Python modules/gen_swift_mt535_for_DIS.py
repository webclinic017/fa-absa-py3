"""---------------------------------------------------------------------------------------------------------------------
MODULE
    gen_swift_mt535_for_DIS

DESCRIPTION
    This module creates MT535 messages for DIS instruments.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-02-19      FAOPS-690       Ntokozo Skosana         Seven Khoza             Initial Implementation.
2020-10-12      FAOPS-908       Ntokozo Skosana         Wandile Sithole         Change SOR account to a static
                                                                                value (This is a temporary solution).
                                                                                The instruments have not been updated
                                                                                with the correct account number.
2020-11-27      FAOPS-1000      Ntokozo Skosana         Wandile Sithole         Only pull the first 12 characters
                                                                                for the ISIN field.
------------------------------------------------------------------------------------------------------------------------
"""
import time
import at_time
import acm
import datetime
import gen_swift_mt535
import gen_ael_variables_date_param
import FOperationsUtils as Utils
import gen_mq
from gen_absa_xml_config_settings import SwiftParamXmlConfig, AbsaXmlConfigSettings

from demat_isin_mgmt_menex import current_authorised_amount, DIS_ISIN_REQUEST_STATE_CHART_NAME
from demat_config import DISINSquery
from at_logging import getLogger


ABSA_SWIFT_NODE = 'AbcapSwiftParameters'
STRATE_SWIFT_NODE = 'StrateSwiftParameters'
LOGGER = getLogger(__name__)
SOR_ACCOUNT = 10107099

CONFIG = AbsaXmlConfigSettings()
ABSA_SWIFT_PARAM = CONFIG.GetUniqueNode('AbcapSwiftParameters')
DIS_USER_REF_EXT = CONFIG.GetValue(ABSA_SWIFT_PARAM, 'DisUserReferenceExt', True)


def _is_number(variable):

    if type(variable) == float or type(variable) == int:
        return True
    return False



def _get_float(variable):
    if hasattr(variable, 'IsKindOf'):
        if variable.IsKindOf('FDenominatedValue'):
            return _get_float(variable.Number())

    if _is_number(variable):
        return float(variable)
    else:
        return None


class _ISIN_Holding:

    @staticmethod
    def _add_values(x, y):
        if x is not None and y is not None:
            return x + y
        elif x is None and y is None:
            return None
        elif x is None:
            return y
        else:
            return x

    def __init__(self, instrument, isCfd, quantity, market_value, book_value, accrued_interest):
        self._instrument = instrument
        self._isCfd = isCfd
        self._quantity = quantity
        self._market_value = _get_float(market_value)
        self._book_value = _get_float(book_value)
        if self._book_value:
            self._book_value *= -1
        self._accrued_interest = _get_float(accrued_interest)
        quotation = instrument.Quotation()
        self._quotation_type = quotation.QuotationType()

    @property
    def key(self):
        return self._instrument.Oid(), self._isCfd

    @property
    def instrument(self):
        return self._instrument

    @property
    def isCfd(self):
        return self._isCfd

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def quotation_type(self):
        return self._quotation_type

    @property
    def market_value(self):
        return self._market_value

    @property
    def book_value(self):
        return self._book_value

    @property
    def accrued_interest(self):
        return self._accrued_interest

    def add(self, holding):
        if self.key != holding.key:
            raise Exception('Cannot add holdings where the key differ')

        self._quantity = _ISIN_Holding._add_values(self._quantity, holding._quantity)
        self._market_value = _ISIN_Holding._add_values(self._market_value, holding._marketValue)
        self._book_value = _ISIN_Holding._add_values(self._book_value, holding._bookValue)
        self._accrued_interest = _ISIN_Holding._add_values(self._accrued_interest, holding._accruedInterest)


class _HoldingCollection:

    def __init__(self):
        self._holdings = {}

    def __iter__(self):
        return self._holdings.itervalues()

    def add(self, holding):
        if holding.key in self._holdings:
            self._holdings[holding.key].add(holding)
        else:
            self._holdings[holding.key] = holding

    def get_length_holdings(self):
        return len(self._holdings)


def _read_holdings(date):
    holdings = _HoldingCollection()
    instruments = acm.FStoredASQLQuery[DISINSquery].Query().Select()

    for instrument in instruments:
        instr_auth_amount = current_authorised_amount(instrument)
        if type(instr_auth_amount) != str:
            processes = acm.BusinessProcess.FindBySubjectAndStateChart(instrument, DIS_ISIN_REQUEST_STATE_CHART_NAME)
            if processes:
                process = processes[0]
                cs = process.CurrentStep()
                if cs.State().Name() == 'Active':
                    quantity = instr_auth_amount and float(instr_auth_amount) or 0.0
                    holdings.add(_ISIN_Holding(instrument, False, quantity, '', '', ''))

    return holdings


def _get_mt535_from_client(holdings, date, frequency, statement_number, i, continuation_indicator):
    message = gen_swift_mt535.Mt535()

    strate_swift_parameters = SwiftParamXmlConfig(STRATE_SWIFT_NODE)
    message.SetRecipientFromParty(strate_swift_parameters.LogicalTerminalBic)

    abcap_swift_parameters = SwiftParamXmlConfig(ABSA_SWIFT_NODE)
    message.Header.LogicalTerminal.BicCode = abcap_swift_parameters.LogicalTerminalBic  \
                                             + abcap_swift_parameters.IssueragentBicExtension

    meridian_business_entity = str(int(time.time()*10))[-8:] + 'MS10' + DIS_USER_REF_EXT + '002'
    message.SetMeridianBusinessEntityFromParty(meridian_business_entity)

    body = message.Body
    statement_number_field = body.StatementNumber.GetField('A')
    statement_number_field.Value = statement_number

    body.Reference = str(datetime.datetime.utcnow())[0:16].replace(':', '').replace('-', '').replace(' ', '') + str(i)
    body.MessageFuntion.Function = 'NEWM'
    body.MessageFuntion.SubFunction = 'COPY'

    statement_page_number = body.PageNumber
    statement_page_number.Value = i
    statement_page_number.ContinuationIndicator = continuation_indicator

    preperation_date = body.Date.GetField('C')
    preperation_date.Qualifier = 'PREP'
    preperation_date.Value = at_time.time_now()

    statement_date = body.Date.GetField('A')
    statement_date.Qualifier = 'STAT'
    statement_date.Value = date

    statement_type_field = body.Indicator.AddSequence()
    statement_type_field.Value.Qualifier = 'STTY'
    statement_type_field.Value.Indicator = gen_swift_mt535.Mt535StatementType.Custody

    statement_basis = body.Indicator.AddSequence()
    statement_basis.Value.Qualifier = 'STBA'
    statement_basis.Value.Indicator = 'SETT'

    frequency_indicator = body.Indicator.AddSequence()
    frequency_indicator.Value.Qualifier = 'SFRE'
    frequency_indicator.Value.Indicator = frequency

    completeness_indicator = body.Indicator.AddSequence()
    completeness_indicator.Value.Qualifier = 'CODE'
    completeness_indicator.Value.Indicator = 'COMP'

    senders_reference = body.Linkages.AddSequence()
    senders_reference.StartOfBlock_Linkages = 'LINK'
    senders_reference.Reference = body.Reference
    senders_reference.Reference_Qualifier = 'PREV'

    account = body.SafekeepingAccount.GetField('B')
    account.DataSourceScheme = 'STRA'
    account.AccountType = 'RECA'

    activity_flag = body.Flag.AddSequence()
    activity_flag.Value_Qualifier = 'ACTI'
    activity_flag.Value = 'Y'

    sub_account_level_flag = body.Flag.AddSequence()
    sub_account_level_flag.Value_Qualifier = 'CONS'
    sub_account_level_flag.Value = 'N'

    sub_account = body.SubSafekeepingAccount.AddSequence()
    for holding in holdings:

        currency = holding.instrument.Currency().Name()
        instrument_holding = sub_account.Instrument.AddSequence()
        isin = holding.instrument.Isin()[0:12]
        account.AccountNumber = str(SOR_ACCOUNT)
        if isin:
            instrument_holding.Identification.Isin = isin
        else:
            print 'Warning: No ISIN for instrument [%s].' % holding.instrument.Name()
        quantity = instrument_holding.Balance.AddSequence()
        quantity.Value.QuantityTypeCode = 'FAMT'
        quantity.Value.Quantity = holding.quantity
        quantity.Value.Qualifier = 'AGGR'

        if hasattr(holding.instrument, 'AccruedDays'):
            accrued_days = None
            try:
                accrued_days = holding.instrument.AccruedDays()
            except Exception:
                pass  # If instrument doesn't implement method 'AccruedDays', pass

            if accrued_days:
                instrument_holding.DaysAccrued = accrued_days

        if holding.market_value:
            market_value = instrument_holding.Amount.AddSequence()
            market_value.Value.Currency = currency
            market_value.Value.Value = holding.market_value
            market_value.Value_Qualifier = 'HOLD'

        if holding.book_value:
            book_value = instrument_holding.Amount.AddSequence()
            book_value.Value.Currency = currency
            book_value.Value.Value = holding.book_value
            book_value.Value_Qualifier = 'BOOK'

        if holding.accrued_interest and holding.accrued_interest != 0.00:
            accrued_interest = instrument_holding.Amount.AddSequence()
            accrued_interest.Value.Currency = currency
            accrued_interest.Value.Value = holding.accrued_interest
            accrued_interest.Value_Qualifier = 'ACRU'

    return message


def _page_indicator(i, splits):
    if splits == 1:
        return 'ONLY'
    elif i == splits:
        return 'LAST'
    else:
        return 'MORE'


def _split_holdings(date):
    split_holdings = {}
    holdings = _read_holdings(date)
    set_value = 1
    split_holdings[set_value] = []
    counter = 1
    for holding in holdings:
        split_holdings[set_value].append(holding)
        if counter < 43:
            counter += 1
        else:
            set_value += 1
            split_holdings[set_value] = []
            counter = 1
    return split_holdings


def _write_client_mt535_to_mq(date, frequency):
    split_holdings = _split_holdings(date)
    splits = len(split_holdings.keys())
    error_count = 0
    message_count = 0

    if splits > 0:
        for i in split_holdings.keys():

            message_count += 1

            try:
                mt535 = str(_get_mt535_from_client(
                    split_holdings[i],
                    date,
                    frequency,
                    '',
                    i,
                    _page_indicator(i, splits)
                ))
            except Exception as error:
                LOGGER.error("Could not create MT535 message")
                LOGGER.exception(error)
                error_count += 1
                raise

            try:
                mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
                mq_mess.Put(mt535)
                Utils.Log(True, '--------------------------------Start Message--------------------------------')
                Utils.Log(True, mt535)
                Utils.Log(True, '---------------------------------End Message---------------------------------')
                Utils.Log(True, 'Message queued...')
            except Exception as error:
                LOGGER.error("Could not place swift message on MQ")
                LOGGER.exception(error)
                error_count += 1
                raise

        Utils.Log(True, "Messages processed: %s" % message_count)
        Utils.Log(True, "Errors:             %s" % error_count)

        return error_count == 0


FREQUENCY_KEY = 'Frequency'
frequency_dict = gen_swift_mt535.Mt535Frequency.OptionsDictionary()
frequencies_display = frequency_dict.keys()
frequencies_display.sort()

ael_gui_parameters = {
    'windowCaption': 'Run SWIFT MT535 statements for Demat instruments'
}

ael_variables = [
    [
        FREQUENCY_KEY,
        'Statement Frequency',
        'string',
        frequencies_display,
        'Daily',
        1,
        0,
        'How frequently is the statement sent?',
        None,
        1
    ]
]

dateParameter = gen_ael_variables_date_param.DateParameter.AddParameter(
    ael_variables,
    1,
    'DATE',
    'Date',
    gen_ael_variables_date_param.DateEnum.Today,
    True,
    'Date of statement.'
)


def ael_main(parameters):

    statement_date = dateParameter.GetAcmDate(parameters)
    frequency = frequency_dict[parameters[FREQUENCY_KEY]]
    if _write_client_mt535_to_mq(statement_date, frequency):
        LOGGER.info('MT535 script completed successfully')
