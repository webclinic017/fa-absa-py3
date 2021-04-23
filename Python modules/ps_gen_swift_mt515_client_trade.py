'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Creates SWIFT MT515 messages and places them on AMB
                           for Portfolio Swap clients
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX       Francois Truter         Initial Implementation
2011-06-29 XXXXXX       Rohan vd Walt           Removed position factor
2011-07-07 XXXXXX       Bhavnisha Sarawan       Added Underlying Type for calculating the clean price
2013-07-01 XXXXXX       Anwar Banoo             Added support for FRN underlyings
2015/10-15 0003118360   Mike Schaefer           Added _getCleanPricePLDate
2017-03-08 0003118360   Jaco Swanepoel          Upgrade 2017: Changed QuoteToRoundedCleanUnitValueOverrideUnitDate 
                                                to QuoteToUnitValueBase
2017-06-13 XXXXXX       Faize Adams             Upgrade 2017: Changed QuoteToUnitValueBase to use custom code QuoteToValue instead.
                                                FIS advised that we use the custom code as the QuoteTo... functions are private.
2017-08-10 xxxxxx       Siyao Liu               Updated QuoteToValue to account for underlying
'''


'''========================== SWIFT MT515 MESSAGE ==========================='''


import acm
import gen_swift_mt515
import PS_Functions
import QuoteToValue

from gen_swift_common import CRLF

from gen_swift_mt515 import Mt515Amounts

from gen_swift_gateway_message import FrontGatewayMessage
from gen_swift_gateway_message import GatewayMessageType
from gen_swift_gateway_message import GatewayMessageFormat

from gen_absa_xml_config_settings import AmbaXmlConfig
from gen_absa_xml_config_settings import AmbaType
from gen_amb_helper import AmbHelper

'''=========================== CREATE MT515 FROM TRADE ======================'''
    
def _join(list):
    _str = ''
    delimiter = ''
    for i in list:
        if i:
            _str += delimiter + str(i)
            delimiter = ','
            
    return _str

def _getAddress(party):
    line1 = _join([party.Address(), party.Address2(), party.ZipCode()])
    line2 = _join([party.City(), party.Country()])
    return line1 + CRLF + line2

class IrrelevantInstrumentError(ValueError):
    pass

def _convertYieldToPrice(priceType, trade, date=None):
    # First, check if the instrument is relevant.
    instrument = trade.Instrument()
    relevant_by_underlying = (instrument.Underlying() is not None and
        instrument.Underlying().InsType() in ('Bond', 'IndexLinkedBond', 'FRN'))
    relevant_by_instype = instrument.InsType() in ('IndexLinkedBond', 'BuySellback',
        'Repo/Reverse', 'BondIndex', 'EquityIndex', 'Bond', 'FRN', 'Convertible',
        'Collateral', 'SecurityLoan', 'BasketRepo/Reverse')
        
    if not relevant_by_underlying and not relevant_by_instype:
        msg = '%s is not a relevant instrument for yield to price conversion.' % instrument.Name()
        raise IrrelevantInstrumentError(msg)
        
    price = QuoteToValue.getPriceForTrade(priceType, trade, date)
        
    if instrument.Underlying() != None and instrument.Underlying().InsType() in ('Bond', 'IndexLinkedBond', 'FRN', 'Bill'):
        leg = instrument.Underlying().Instrument().Legs().At(0) 
        price = QuoteToValue.getPriceForTrade(priceType, trade, date, True)
    elif instrument.Legs():
        leg = instrument.Legs().At(0)
    else:
        msg = '%s is not a relevant instrument for yield to price conversion (it does not have any legs).' % instrument.Name()
        raise IrrelevantInstrumentError(msg)
                                                                    
    return price

def _getCleanPrice(trade):
    return _convertYieldToPrice("clean", trade,)

def _getCleanPricePLDate(trade, date):
    return _convertYieldToPrice("clean", trade, date)
    
def _getDirtyPrice(trade):
    return _convertYieldToPrice("dirty", trade)
        
def _getAccruedInterest(trade):
    cleanPrice = _getCleanPrice(trade)
    dirtyPrice = _getDirtyPrice(trade)
    
    return (dirtyPrice - cleanPrice) * trade.Nominal()

def _getClientFromTrade(trade):
    portfolio = trade.Portfolio()
    portfolioSwap = portfolio.AdditionalInfo().PS_FundingIns()
    if not portfolioSwap:
        raise Exception('Additional info PS_FundingIns must be set on portfolios where MT515 messages should be generated, not set for portfolio [%s], trade %i.' % (portfolio.Name(), trade.Oid()))

    trades = portfolioSwap.Trades()
    if len(trades) != 1:
        raise Exception('Expected one trade per portfolio swap, got %i for portfolio swap [%s].' % (len(trades), sportfolioSwap.name()))

    fundingTrade = trades[0]
    return fundingTrade.Counterparty()
    
def _setPartyField(partySequenceField, party):
    swiftAlias = party.SwiftAlias()
    if swiftAlias:
        partyField = partySequenceField.Party.GetField('P')
        partyField.Value.Value = swiftAlias
    else:
        partyField = partySequenceField.Party.GetField('Q')
        partyField.Value = party.Name() + CRLF + _getAddress(party)
    
    return partyField

def _createMt515MessageFromTrade(trade, messageFunction, version):
    client = _getClientFromTrade(trade)
    instrument = trade.Instrument()
    currency = trade.Currency().Name()
    quantity = abs(trade.QuantityOrNominalAmount())
    
    isBuy = trade.Quantity() >= 0.0
    
    if instrument.Quotation().Name() == 'Yield':
        _yield = trade.Price()
        price = _getCleanPrice(trade)
        accrued = _getAccruedInterest(trade)
    else:
        _yield = None
        price = trade.Price() * instrument.Quotation().QuotationFactor()
        accrued = None

    message = gen_swift_mt515.Mt515()
    message.SetRecipientFromParty(client)
    message.SetMeridianBusinessEntityFromParty(client)
    
    body = message.Body
    body.Reference = '%i%s' % (trade.Oid(), '-%s' % version if version else '')
    body.MessageFunction.Function = messageFunction
    preperationDate = body.PreperationDate.GetField('C')
    preperationDate.Value = acm.Time().DateNow()
    body.TradeTransactionType.Indicator = 'TRAD'
    
    linkage = body.Linkages.AddSequence()
    linkage.Reference = trade.Oid()
    if messageFunction == gen_swift_mt515.Mt515MessageFunction.Cancel:
        linkage.Reference_Qualifier = 'PREV'
    else:
        linkage.Reference_Qualifier = 'TRRF'
    
    if trade.CorrectionTrade():
        correctedLinkage = body.Linkages.AddSequence()
        correctedLinkage.Reference = trade.CorrectionTrade().Oid()
        correctedLinkage.Reference_Qualifier = 'RELA'
        
    tradeDate = body.ConfirmationDate.GetField('C')
    tradeDate.Value = trade.TradeTime()
    tradeDate.Qualifier = 'TRAD'
    
    settlementDate = body.ConfirmationDate.GetField('C')
    settlementDate.Value = trade.ValueDay()
    settlementDate.Qualifier = 'SETT'
    
    if _yield:
        priceField = body.ConfirmationPrice.GetField('A')
        priceField.PercentageType = 'YIEL'
        priceField.Price = _yield
    else:
        priceField = body.ConfirmationPrice.GetField('B')
        priceField.AmountType = 'ACTU'
        priceField.Price.Value = price
        priceField.Price.Currency = currency
    
    priceField.Qualifier = 'DEAL'

    paymentIndicator = body.Indicator.GetField('H') 
    paymentIndicator.Qualifier = 'PAYM'
    paymentIndicator.Value = 'APMT'
    
    buySellIndicator = body.Indicator.GetField('H')
    buySellIndicator.Qualifier = 'BUSE'
    
    counterpartyField = _setPartyField(body.ConfirmationParties.AddSequence(), trade.Counterparty())
    clientConfirmationParty = body.ConfirmationParties.AddSequence()
    clientField = _setPartyField(clientConfirmationParty, client)
    custodyAccount = clientConfirmationParty.Account.GetField('A')
    custodyAccount.Qualifier = 'SAFE'
    custodyAccount.Value = client.SwiftCustodyAccount()
    
    if isBuy:
        buySellIndicator.Value = 'BUYI'
        clientField.Qualifier = 'BUYR'
        counterpartyField.Qualifier = 'SELL'
    else:
        buySellIndicator.Value = 'SELL'
        clientField.Qualifier = 'SELL'
        counterpartyField.Qualifier = 'BUYR'

    quantityField = body.Quantity.AddSequence().Value
    quantityField.Value = quantity
    quantityField.Qualifier = 'CONF'
    quantityField.QuantityTypeCode = 'UNIT'
    
    body.Instrument.Description = instrument.Name().replace('#', '')
    if instrument.Isin():
        body.Instrument.Isin = instrument.Isin()
    else:
        print('Warning: No ISIN for instrument [%s]. Trade number %i.' % (instrument.Name(), trade.Oid()))
    
    settlementDetails = body.SettlementDetails.AddSequence()
    indicator = settlementDetails.Indicator.AddSequence()
    indicator.Value.Qualifier = 'SETR'
    indicator.Value.Indicator = 'TRAD'
    
    settlementAmount = tradeAmount = quantity * price
    _addSettlementDetailsAmount(settlementDetails, Mt515Amounts.TradeAmount, tradeAmount, currency)
    if accrued:
        _addSettlementDetailsAmount(settlementDetails, Mt515Amounts.AccruedInterestAmount, accrued, currency)
     
    executionFee = PS_Functions.GetExecutionFeeFromTrade(trade)
    _addSettlementDetailsAmount(settlementDetails, Mt515Amounts.ExecutingBrokersCommission, executionFee, currency)
    settlementAmount += executionFee
    
    securitiesTransferTax = PS_Functions.GetSecuritiesTransferTaxFromTrade(trade)
    _addSettlementDetailsAmount(settlementDetails, Mt515Amounts.TransferTax, securitiesTransferTax, currency)
    settlementAmount += securitiesTransferTax
        
    body.SettlementAmount.Value = abs(settlementAmount)
    body.SettlementAmount.Currency = currency
    
    return message
    
def _addSettlementDetailsAmount(settlementDetails, qualifier, value, currency):
    if value != 0.0:
        amountSequence = settlementDetails.Amounts.AddSequence()
        amount = amountSequence.Amount.AddSequence()
        amount.Value_Qualifier = qualifier
        amount.Value.Value = value
        amount.Value.Currency = currency

def CreateMt515GatewayMessageFromTrade(trade, messageFunction, version, isDuplicate):
    if not messageFunction:
        messageFunction = gen_swift_mt515.Mt515MessageFunction.GetFunctionFromTrade(trade)
    
    mt515 = _createMt515MessageFromTrade(trade, messageFunction, version)
    if isDuplicate:
        mt515.Body.MessageFunction.Subfunction = gen_swift_mt515.Mt515MessageSubfunction.Duplicate
    
    recipient = mt515.ApplicationHeader.Address
    reference = mt515.Body.Reference
    
    return str(FrontGatewayMessage(recipient, ':SEME//' + reference, trade.Oid(), 'MT515', GatewayMessageType.New, GatewayMessageFormat.Swift, str(mt515)))

def _writeMt515GatewayMessageToAmb(trade, messageFunction, version, isDuplicate):
    MESSAGE_TYPE = 'MT515'
    AMBA_NODE = 'MarketsMessageGatewayAmba'
    
    message = CreateMt515GatewayMessageFromTrade(trade, messageFunction, version, isDuplicate)
    
    ambaConfig = AmbaXmlConfig(AMBA_NODE, AmbaType.Sender)
    AmbHelper.WriteSwiftMtMessageToQueue(ambaConfig, MESSAGE_TYPE, message)

ael_gui_parameters = {
    'windowCaption' : 'Run SWIFT MT515 message for trade'
}

TRADE_KEY = 'TRADE'
FUNCTION_KEY = 'FUNCTION'
AS_PER_TRADE = 'As per actual trade'
functionsDict = gen_swift_mt515.Mt515MessageFunction.OptionsDictionary()
functionsDict[AS_PER_TRADE] = None
functionsDisplay = functionsDict.keys()
functionsDisplay.sort()

IS_DUPLICATE_KEY = 'IS_DUPLICATE'

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [TRADE_KEY, 'Trade', 'FTrade', None, None, 1, 1, 'The trade(s) for which MT515 message(s) should be sent.', None, 1],
    [FUNCTION_KEY, 'Message Function', 'string', functionsDisplay, AS_PER_TRADE, 1, 0, 'What type of message should be generated: New Trade, Trade Cancellation or should it be determined from the trade? ', None, 1],
    [IS_DUPLICATE_KEY, 'Is this message a duplicate', 'string', boolDictDisplay, 'Yes', 1, 0, 'If this MT515 has previously been sent, sending it again makes it a duplicate message.', None, 1]
]

def ael_main(parameters):
    try:
        trades = parameters[TRADE_KEY]
        function = functionsDict[parameters[FUNCTION_KEY]]
        isDuplicate = boolDict[parameters[IS_DUPLICATE_KEY]]
        for trade in trades:
            try:
                _writeMt515GatewayMessageToAmb(trade, function, trade.VersionId(), isDuplicate)
                print('MT515 sent for trade %i' % trade.Oid())
            except Exception, ex:
                print('An exception occurred while processing trade %i: %s' % (trade.Oid(), str(ex)))
            
    except Exception, ex:
        print('An exception occurred while running the script:', str(ex))
    else:
        print('The script completed successfully')
