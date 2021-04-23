'''--------------------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : Runs SWIFT MT535 messages for Portfolio Swap clients
                          Developed from the module ps_gen_swift_mt535_for_client
-----------------------------------------------------------------------------------------

HISTORY
=========================================================================================
Date       Change no            Developer             Description
-----------------------------------------------------------------------------------------
2016-08-24 CHNG0003744247       Willie van der Bank   Initial implementation.
2016-09-08 CHNG0003938069       Gabriel Marko         Send Messages 1 by 1:
                                                      Meridian can't process bulk uploads
                                                      as it can't parse multiple
                                                      concatenated messages.
2017-02-27 CHNG0004357437       Willie van der Bank   Changed to only include busines
                                                      processes in Active status.
'''

import acm, datetime
import gen_swift_mt535
import gen_swift_mt_messages
import gen_swift_gateway_message
import gen_ael_variables_date_param
import FOperationsUtils as Utils
import gen_mq
import pymqi
from gen_absa_xml_config_settings import SwiftParamXmlConfig

from gen_amb_helper import AmbHelper
from pprint import pprint
from demat_isin_mgmt_menex import current_authorised_amount, MMSS_ISIN_REQUEST_STATE_CHART_NAME
from demat_config import INSquery
import at_time

ABSA_SWIFT_NODE = 'AbcapSwiftParameters'
STRATE_SWIFT_NODE = 'StrateSwiftParameters'

#AMBA_NODE = 'MarketsMessageGatewayAmba'

def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber

def _getFloat(object):
    if hasattr(object, 'IsKindOf'):
        if object.IsKindOf('FDenominatedValue'):
            return _getFloat(object.Number())

    if _isNumber(object):
        return float(object)
    else:
        return None

class _Holding:

    @staticmethod
    def _addValues(x, y):
        if x is not None and y is not None:
            return x + y
        elif x is None and y is None:
            return None
        elif x is None:
            return y
        else:
            return x

    def __init__(self, instrument, isCfd, quantity, marketValue, bookValue, accruedInterest):
        self._instrument = instrument
        self._isCfd = isCfd
        self._quantity = quantity
        self._marketValue = _getFloat(marketValue)
        self._bookValue = _getFloat(bookValue)
        if self._bookValue:
            self._bookValue *= -1
        self._accruedInterest = _getFloat(accruedInterest)
        quotation = instrument.Quotation()
        self._quotationType = quotation.QuotationType()

    @property
    def Key(self):
        return (self._instrument.Oid(), self._isCfd)

    @property
    def Instrument(self):
        return self._instrument

    @property
    def IsCfd(self):
        return self._isCfd

    @property
    def Quantity(self):
        return self._quantity

    @property
    def Price(self):
        return self._price

    @property
    def QuotationType(self):
        return self._quotationType

    @property
    def MarketValue(self):
        return self._marketValue

    @property
    def BookValue(self):
        return self._bookValue

    @property
    def AccruedInterest(self):
        return self._accruedInterest

    def Add(self, holding):
        if self.Key != holding.Key:
            raise Exception('Cannot add holdings where the key differ')

        self._quantity = _Holding._addValues(self._quantity, holding._quantity)
        self._marketValue = _Holding._addValues(self._marketValue, holding._marketValue)
        self._bookValue = _Holding._addValues(self._bookValue, holding._bookValue)
        self._accruedInterest = _Holding._addValues(self._accruedInterest, holding._accruedInterest)

class _HoldingCollection:

    def __init__(self):
        self._holdings = {}

    def __iter__(self):
        return self._holdings.itervalues()

    def Add(self, holding):
        if holding.Key in self._holdings:
            self._holdings[holding.Key].Add(holding)
        else:
            self._holdings[holding.Key] = holding

    def get_length_holdings(self):
        return len(self._holdings)

def _readHoldings(date):
    holdings = _HoldingCollection()
    instruments = acm.FStoredASQLQuery[INSquery].Query().Select()

    for instrument in instruments:
        instrAuthAmount = current_authorised_amount(instrument)
        if type(instrAuthAmount) != str :
            processes = acm.BusinessProcess.FindBySubjectAndStateChart(instrument, MMSS_ISIN_REQUEST_STATE_CHART_NAME)
            if processes:
                process = processes[0]
                cs = process.CurrentStep()
                #if cs.State().Name() != 'DeIssued':
                if cs.State().Name() == 'Active':
                    quantity = instrAuthAmount and float(instrAuthAmount) or 0.0
                    holdings.Add(_Holding(instrument, False, quantity, '', '', ''))

    return holdings

def _getMt535FromClient(holdings, date, frequency, statementNumber, i, ContinuationIndicator):
    message = gen_swift_mt535.Mt535()

    strateSwiftParameters = SwiftParamXmlConfig(STRATE_SWIFT_NODE)
    message.SetRecipientFromParty(strateSwiftParameters.LogicalTerminalBic)

    abcapSwiftParameters = SwiftParamXmlConfig(ABSA_SWIFT_NODE)
    message.Header.LogicalTerminal.BicCode = abcapSwiftParameters.LogicalTerminalBic  + abcapSwiftParameters.IsinMgmtBicExtension
    message.SetMeridianBusinessEntityFromParty('53680036MS10P002')

    body = message.Body
    statementNumberField = body.StatementNumber.GetField('A')
    statementNumberField.Value = statementNumber

    body.Reference = str(datetime.datetime.utcnow())[0:16].replace(':', '').replace('-', '').replace(' ', '') + str(i)
    body.MessageFuntion.Function = 'NEWM'
    body.MessageFuntion.SubFunction = 'COPY'

    statementPageNumber = body.PageNumber
    statementPageNumber.Value = i
    statementPageNumber.ContinuationIndicator = ContinuationIndicator

    statementDate = body.Date.GetField('A')
    statementDate.Qualifier = 'STAT'
    statementDate.Value = date

    preperationDate = body.Date.GetField('C')
    preperationDate.Qualifier = 'PREP'
    preperationDate.Value = at_time.time_now()

    frequencyIndicator = body.Indicator.AddSequence()
    frequencyIndicator.Value.Qualifier = 'SFRE'
    frequencyIndicator.Value.Indicator = frequency

    completenessIndicator = body.Indicator.AddSequence()
    completenessIndicator.Value.Qualifier = 'CODE'
    completenessIndicator.Value.Indicator = 'COMP'

    statementTypeField = body.Indicator.AddSequence()
    statementTypeField.Value.Qualifier = 'STTY'
    statementTypeField.Value.Indicator = gen_swift_mt535.Mt535StatementType.Custody

    statementBasis = body.Indicator.AddSequence()
    statementBasis.Value.Qualifier = 'STBA'
    statementBasis.Value.Indicator = 'SETT'

    account = body.SafekeepingAccount.GetField('B')
    account.AccountType = 'ABRD'
    account.AccountNumber = '90000038'

    activityFlag = body.Flag.AddSequence()
    activityFlag.Value_Qualifier = 'ACTI'
    activityFlag.Value = 'Y'

    subAccountLevelFlag = body.Flag.AddSequence()
    subAccountLevelFlag.Value_Qualifier = 'CONS'
    subAccountLevelFlag.Value = 'N'

    subAccount = body.SubSafekeepingAccount.AddSequence()
    for holding in holdings:

        currency = holding.Instrument.Currency().Name()

        instrumentHolding = subAccount.Instrument.AddSequence()
        #instrumentHolding.Identification.AssignDescriptionFromInstrument(holding.Instrument, holding.IsCfd)    #Adds instype and ID
        isin = holding.Instrument.Isin()
        if isin:
            instrumentHolding.Identification.Isin = isin
        else:
            print 'Warning: No ISIN for instrument [%s].' % holding.Instrument.Name()
        quantity = instrumentHolding.Balance.AddSequence()
        quantity.Value.QuantityTypeCode = 'FAMT'
        quantity.Value.Quantity = holding.Quantity
        quantity.Value.Qualifier = 'AGGR'

        if hasattr(holding.Instrument, 'AccruedDays'):
            accruedDays = None
            try:
                accruedDays = holding.Instrument.AccruedDays()
            except Exception:
                pass
            if accruedDays:
                instrumentHolding.DaysAccrued = accruedDays

        if holding.MarketValue:
            marketValue = instrumentHolding.Amount.AddSequence()
            marketValue.Value.Currency = currency
            marketValue.Value.Value = holding.MarketValue
            marketValue.Value_Qualifier = 'HOLD'

        if holding.BookValue:
            bookValue = instrumentHolding.Amount.AddSequence()
            bookValue.Value.Currency = currency
            bookValue.Value.Value = holding.BookValue
            bookValue.Value_Qualifier = 'BOOK'

        if holding.AccruedInterest and holding.AccruedInterest != 0.00:
            accruedInterest = instrumentHolding.Amount.AddSequence()
            accruedInterest.Value.Currency = currency
            accruedInterest.Value.Value = holding.AccruedInterest
            accruedInterest.Value_Qualifier = 'ACRU'

    return message

def _pageIndicator(i, splits):
    if splits == 1:
        return 'ONLY'
    elif i == splits:
        return 'LAST'
    else:
        return 'MORE'


def _splitHoldings(date):
    splitHoldings = {}
    holdings = _readHoldings(date)
    set = 1
    splitHoldings[set] = []
    counter = 0
    for holding in holdings:
        splitHoldings[set].append(holding)
        if counter < 43:
            counter += 1
        else:
            set += 1
            splitHoldings[set] = []
            counter = 0
    return splitHoldings


def _writeClientMt535ToAmb(date, frequency):
    MESSAGE_TYPE = 'MT535'
    splitHoldings = _splitHoldings(date)
    splits = len(splitHoldings.keys())
    errors = 0
    message_count = 0
    
    if splits > 0:
        for i in splitHoldings.keys():

            message_count += 1

            try:
                mt535 = str(_getMt535FromClient(
                    splitHoldings[i],
                    date,
                    frequency,
                    '',
                    i,
                    _pageIndicator(i, splits)
                ))
            except Exception as ex:
                Utils.Log(True, "Could not create MT535 message\nError:%s" % ex)
                errors += 1
                continue

            try:
                mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
                mq_mess.Put(mt535)
                Utils.Log(True, '--------------------------------Start Message--------------------------------')
                Utils.Log(True, mt535)
                Utils.Log(True, '---------------------------------End Message---------------------------------')
                Utils.Log(True, 'Message queued...')
            except Exception as ex:
                Utils.Log(True, "Could not place swift message on MQ\nError:%s" % ex)
                errors += 1
                continue

        Utils.Log(True, "Messages processed: %s" % message_count)
        Utils.Log(True, "Errors:             %s" % errors)

        return errors == 0

    #recipient  = mt535.ApplicationHeader.Address
    #uniqueReference = ':SEME//' + mt535.Body.Reference
    #subSystemId = client.Oid()
    #$gatewayMessage = gen_swift_gateway_message.FrontGatewayMessage(recipient, uniqueReference, subSystemId, MESSAGE_TYPE, gen_swift_gateway_message.GatewayMessageType.New, gen_swift_gateway_message.GatewayMessageFormat.Swift, str(mt535))
    #ambaConfig = gen_absa_xml_config_settings.AmbaXmlConfig(AMBA_NODE, gen_absa_xml_config_settings.AmbaType.Sender)
    #AmbHelper.WriteSwiftMtMessageWithStatementToQueue(ambaConfig, MESSAGE_TYPE, str(gatewayMessage), client.Oid(), statementNumber, date)

FREQUENCY_KEY = 'Frequency'
frequencyDict = gen_swift_mt535.Mt535Frequency.OptionsDictionary()
frequenciesDisplay = frequencyDict.keys()
frequenciesDisplay.sort()

ael_gui_parameters = {
    'windowCaption' : 'Run SWIFT MT535 statements for Demat instruments'
}

ael_variables = [
    [
        FREQUENCY_KEY,
        'Statement Frequency',
        'string',
        frequenciesDisplay,
        'Daily',
        1,
        0,
        'How frequently is the statement sent?',
        None,
        1
    ]
]

dateParemeter = gen_ael_variables_date_param.DateParameter.AddParameter(
    ael_variables,
    1,
    'DATE',
    'Date',
    gen_ael_variables_date_param.DateEnum.Today,
    True,
    'Date of statement.'
)

def ael_main(parameters):
    #try:
    statementDate = dateParemeter.GetAcmDate(parameters)
    frequency = frequencyDict[parameters[FREQUENCY_KEY]]
    if _writeClientMt535ToAmb(statementDate, frequency):
        print 'MT535 script completed successfully'
