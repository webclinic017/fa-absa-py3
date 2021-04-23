'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Runs SWIFT MT535 messages for Portfolio Swap clients
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  695005
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 686159    Francois Truter           Initial Implementation
2011-06-23 695005    Francois Truter           Showing positions on trade date
                                               Updated instrument descriptions
2011-07-08 707904    Rohan vd Walt             Fix query folder to select trades for today in _hasTransactions   
2011-07-15 713436    Bhavnisha Sarawan         Removed Market price from being sent to the client.
2011-08-26 750738    Bhavnisha Sarawan         Updated the CustodyAccount additional info call from the Client to the Portfolio.
2011-08-29 753484    Bhavnisha Sarawan         Updated the CustodyAccount for NoneType.
2011-08-31 755836    Bhavnisha Sarawan         Updated the CustodyAccount for NoneType.
2011-09-01 757043    Heinrich Cronje           Updated the activity flag to check the holdings length
2011-09-02 757903    Heinrich, Bhavnisha       Removed line374 due to valid holdings but 0 quantity.
'''

import acm

import gen_swift_mt535
import gen_swift_mt_messages
import gen_swift_gateway_message

import gen_absa_xml_config_settings

from gen_amb_helper import AmbHelper
from pprint import pprint

AMBA_NODE = 'MarketsMessageGatewayAmba'

import gen_ael_variables_date_param

INVALID_STATUSSES = ['Void', 'Confirmed Void', 'Simulated']
    
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

    #def __init__(self, instrument, isCfd, quantity, price, marketValue, bookValue, accruedInterest):
    def __init__(self, instrument, isCfd, quantity, marketValue, bookValue, accruedInterest):
        self._instrument = instrument
        self._isCfd = isCfd
        self._quantity = quantity
        #self._price = None
        self._marketValue = _getFloat(marketValue)
        self._bookValue = _getFloat(bookValue)
        if self._bookValue:
            self._bookValue *= -1
        self._accruedInterest = _getFloat(accruedInterest)
        
        quotation = instrument.Quotation()
        #price = _getFloat(price)
        #if _isNumber(price) and quotation:
        #    self._price = float(price) * quotation.QuotationFactor()
            
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

def _getPortfolioSwapTrades(party):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
            
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Portfolio Swap'))
    
    op = query.AddOpNode('AND')
    for status in INVALID_STATUSSES:
        op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
    
    if party:
        op = query.AddOpNode('AND')
        op.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
        
    return query.Select()
    
def _getPortfolioSwapInstruments(party):
    trades = _getPortfolioSwapTrades(party)
    instruments = set()
    for trade in trades:
        instruments.add(trade.Instrument())
    
    return instruments

def _getPortfolioSwapCustodyAccount(party, date):
    query = _getClientQuery(party)
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    
    top_node = calc_space.InsertItem(query)
    calc_space.Refresh()
    
    if (top_node.Iterator().FirstChild() <> None):
        portfolioTypeIterator = top_node.Iterator().FirstChild()
    else:
        CustodyAccount = '-'
        print 'Warning: No Custody Account saved for client.'
        return CustodyAccount
        
    if (portfolioTypeIterator.Tree() <> None):
        trades = portfolioTypeIterator.Tree().Item().Trades()
    else:
        CustodyAccount = '-'
        print 'Warning: No Custody Account saved for client.'
        return CustodyAccount
    
    list = trades.AsList()
    t = list[0]
    try:
        CustodyAccount= t.Portfolio().AdditionalInfo().PS_ClientFundName()
    except:
        CustodyAccount = '-'
        print 'Warning: No Custody Account saved for client.'
    
    if CustodyAccount == None:
        CustodyAccount = '-'
    return CustodyAccount
        
def _getPortfolioSwapClients():
    trades = _getPortfolioSwapTrades(None)
    clientSet = set()
    for trade in trades:
        clientSet.add(trade.Counterparty())
    clients = []
    for client in clientSet:
        if client.AdditionalInfo().MeridianSwiftBusEnt() and client.AdditionalInfo().MT535Et515Recipient():
            clients.append(client)
    return clients

def _getClientQuery(party):
    instruments = _getPortfolioSwapInstruments(party)
    if not instruments:
        return None
    
    query = acm.CreateFASQLQuery('FAdditionalInfo', 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('AddInf.Name', 'EQUAL', 'PS_FundingIns')
    
    op = query.AddOpNode('OR')
    for instrument in instruments:
        op.AddAttrNode('FieldValue', 'EQUAL', instrument.Name())
        
    additionalInfos = query.Select()
    if not additionalInfos:
        return None
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    op = query.AddOpNode('AND')
    for status in INVALID_STATUSSES:
        op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
    
    op = query.AddOpNode('OR')
    for additionalInfo in additionalInfos:
        op.AddAttrNode('Portfolio.Oid', 'EQUAL', additionalInfo.Recaddr())
    return query

def _readHoldings(client, date):
    holdings = _HoldingCollection()
    query = _getClientQuery(client)
    if not query:
        return holdings
    
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Inception')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    
    top_node = calc_space.InsertItem(query)
    top_node.ApplyGrouper(acm.FAttributeGrouper('Trade.Portfolio.AdditionalInfo.PS_PortfolioType'))
    calc_space.Refresh()
    
    UNITS_COLUMN = 'Client Swift Units'
    PRICE_COLUMN = 'Market Price'
    MARKET_VALUE_COLUMN = 'Client Market Value'
    BOOK_VALUE_COLUMN = 'Client Swift Book Value'
    ACCRUED_INTEREST_COLUMN = 'Client Accrued Interest'
    
    portfolioTypeIterator = top_node.Iterator().FirstChild()
 
    while portfolioTypeIterator:
        isCfd = False
        portfolioType = portfolioTypeIterator.Tree().Item().StringKey()
        if portfolioType == 'CFD':
            isCfd = True
        
        instrumentIterator = portfolioTypeIterator.Clone().FirstChild()
        while instrumentIterator:
            instrument = acm.FInstrument[instrumentIterator.Tree().Item().StringKey()]
            readQuantity = calc_space.CreateCalculation(instrumentIterator.Tree(), UNITS_COLUMN).Value()

            if not _isNumber(readQuantity):
                instrumentIterator = instrumentIterator.NextSibling()
                continue
             
            quantity = float(readQuantity)
            #price = calc_space.CreateCalculation(instrumentIterator.Tree(), PRICE_COLUMN).Value()
            marketValue = calc_space.CreateCalculation(instrumentIterator.Tree(), MARKET_VALUE_COLUMN).Value()
            bookValue = calc_space.CreateCalculation(instrumentIterator.Tree(), BOOK_VALUE_COLUMN).Value()
            accruedInterest = calc_space.CreateCalculation(instrumentIterator.Tree(), ACCRUED_INTEREST_COLUMN).Value()

            #holdings.Add(_Holding(instrument, isCfd, quantity, price, marketValue, bookValue, accruedInterest))
            holdings.Add(_Holding(instrument, isCfd, quantity, marketValue, bookValue, accruedInterest))
            instrumentIterator = instrumentIterator.NextSibling()
            
        portfolioTypeIterator = portfolioTypeIterator.NextSibling()
    
    return holdings
        
def _getStatementNumber(party, date):
    statementNumber = '%03i' % party.Mt535NextStatementNumber(date)
    if len(statementNumber) > 3:
        raise Exception('Statement number cannot exceed three characters. Party %(portfolio)s MT535 statmenet number is %(statement)s' % 
            {'portfolio': portfolio.Name(), 'statement': statementNumber})
    return statementNumber

def _getMt535FromClient(client, date, frequency, statementNumber):
    holdings = _readHoldings(client, date)
    message = gen_swift_mt535.Mt535()    
    message.SetRecipientFromParty(client)
    message.SetMeridianBusinessEntityFromParty(client)
    
    body = message.Body
    statementNumberField = body.StatementNumber.GetField('A')
    statementNumberField.Value = statementNumber
    
    body.Reference = gen_swift_mt_messages.GetTransactionReferenceFromStatement(client, date, statementNumber)
    body.MessageFuntion.Function = 'NEWM'
    body.MessageFuntion.SubFunction = 'COPY'
    
    statementDate = body.Date.GetField('A')
    statementDate.Qualifier = 'STAT'
    statementDate.Value = date
    
    preperationDate = body.Date.GetField('C') 
    preperationDate.Qualifier = 'PREP'
    preperationDate.Value = acm.Time().TimeNow()

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
    
    ownerBic = client.SwiftAlias()
    if ownerBic:
        owner = body.AccountOwner.GetField('P')
        owner.Value.BicCode = ownerBic
        
    account = body.SafekeepingAccount.GetField('A')
    account.Value = _getPortfolioSwapCustodyAccount(client, date)
    
    activityFlag = body.Flag.AddSequence()
    activityFlag.Value_Qualifier = 'ACTI'
    activityFlag.Value = 'Y' if holdings.get_length_holdings() > 0 else 'N'
    
    subAccountLevelFlag = body.Flag.AddSequence()
    subAccountLevelFlag.Value_Qualifier = 'CONS'
    subAccountLevelFlag.Value = 'N'
    
    if holdings.get_length_holdings() == 0:
        return message
        
    subAccount = body.SubSafekeepingAccount.AddSequence()
    for holding in holdings:
        #Removed this section on 2011-09-02 due to valid holdings but 0 quantity.
        #if holding.Quantity == 0.0:
        #    continue
    
        currency = holding.Instrument.Currency().Name()
    
        instrumentHolding = subAccount.Instrument.AddSequence()
        instrumentHolding.Identification.AssignDescriptionFromInstrument(holding.Instrument, holding.IsCfd)
        isin = holding.Instrument.CustomOtcOrIsin(holding.IsCfd)
        if isin:
            instrumentHolding.Identification.Isin = isin
        else:
            print 'Warning: No ISIN for instrument [%s].' % holding.Instrument.Name()
        '''
        if holding.Price:
            if holding.QuotationType == 'Yield':
                price = instrumentHolding.Price.GetField('A')
                price.PercentageType = 'YIEL'
                price.Price = holding.Price
            else:
                price = instrumentHolding.Price.GetField('B')
                price.AmountType = 'ACTU'
                price.Price.Currency = currency
                price.Price.Value = holding.Price
            
            price.Qualifier = 'MRKT'
        '''
        quantity = instrumentHolding.Balance.AddSequence()            
        if holding.QuotationType == 'Yield':
            quantity.Value.QuantityTypeCode = 'FAMT'
        else:
            quantity.Value.QuantityTypeCode = 'UNIT'
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
    
def _writeClientMt535ToAmb(client, date, frequency):
    MESSAGE_TYPE = 'MT535'
    
    statementNumber = _getStatementNumber(client, date)
    mt535 = _getMt535FromClient(client, date, frequency, statementNumber)
    recipient  = mt535.ApplicationHeader.Address
    uniqueReference = ':SEME//' + mt535.Body.Reference
    subSystemId = client.Oid()
    gatewayMessage = gen_swift_gateway_message.FrontGatewayMessage(recipient, uniqueReference, subSystemId, MESSAGE_TYPE, gen_swift_gateway_message.GatewayMessageType.New, gen_swift_gateway_message.GatewayMessageFormat.Swift, str(mt535))
    ambaConfig = gen_absa_xml_config_settings.AmbaXmlConfig(AMBA_NODE, gen_absa_xml_config_settings.AmbaType.Sender)
    AmbHelper.WriteSwiftMtMessageWithStatementToQueue(ambaConfig, MESSAGE_TYPE, str(gatewayMessage), client.Oid(), statementNumber, date)
    
def _hasTransactions(client, date):
    query = _getClientQuery(client)
    if not query:
        print 'NO QUERY'
        return False

    op = query.AddOpNode('AND')
    op.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    op.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    if query.Select():
        return True
    
    return False

ALL_CLIENTS = 'All clients set up for MT535'    
def _getClientList():
    clients = []
    for client in _getPortfolioSwapClients():
        clients.append(client.Name())
    
    clients.sort()
    clients.insert(0, ALL_CLIENTS)
    return clients
    
CLIENT_KEY = 'Client'
print 'Loading clients...'
clientList = _getClientList()

FREQUENCY_KEY = 'Frequency'
frequencyDict = gen_swift_mt535.Mt535Frequency.OptionsDictionary()
frequenciesDisplay = frequencyDict.keys()
frequenciesDisplay.sort()

ONLY_IF_TRANSACTIONS_KEY = 'ONLY_IF_TRANSACTIONS'
boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

OK_AND_CANCEL = 1
OK = 1
CANCEL = 2

ael_gui_parameters = {
    'windowCaption' : 'Run SWIFT MT535 statements for Portfolios'
}

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [CLIENT_KEY, 'Clients', 'string', clientList, ALL_CLIENTS, 1, 1, 'The clients to run statements for. Note that the additional infos CustodyAccount, MeridianSwiftBusEnt and Mt535Et515Recipient must be completed on the client.', None, 1],
    [FREQUENCY_KEY, 'Statement Frequency', 'string', frequenciesDisplay, 'Daily', 1, 0, 'How frequently is the statement sent?', None, 1],
    [ONLY_IF_TRANSACTIONS_KEY, 'Only send if there were transactions', 'string', boolDictDisplay, 'Yes', 1, 0, 'Should a statement only be sent if there were transactions?', None, 1]
]

dateParemeter = gen_ael_variables_date_param.DateParameter.AddParameter(ael_variables, 1, 'DATE', 'Date', gen_ael_variables_date_param.DateEnum.Today, True, 'Date of statement.')

def ael_main(parameters):
    try:
        statementDate = dateParemeter.GetAcmDate(parameters)
        if statementDate > acm.Time().DateNow():
            message = 'Note that future dated trades might not be included when running for a future date. If you want to run a future dated statement, log in for that date.'
            if str(acm.Class()) == 'FTmServer':
                func=acm.GetFunction('msgBox', 3)
                buttonSelected = func('Warning', message + '\nClick [OK] to continue or [Cancel] to abort.', 1)
                if buttonSelected != OK:
                    print 'Message aborted'
                    return
            else:
                print 'WARNING!' + message
        
        onlyIfTransactions = boolDict[parameters[ONLY_IF_TRANSACTIONS_KEY]]
        frequency = frequencyDict[parameters[FREQUENCY_KEY]]
        
        selectedClientNames = parameters[CLIENT_KEY]
        if ALL_CLIENTS in selectedClientNames:
            selectedClientNames = []
            selectedClientNames.extend(clientList)
            selectedClientNames.remove(ALL_CLIENTS)
        
        for name in selectedClientNames:
            client = acm.FParty[name]
            if not client:
                print 'Could not load client [%s].' % name
            
            try:
                if onlyIfTransactions and not _hasTransactions(client, statementDate):
                    print 'No transactions for client [%s] on %s. No statement will be sent.' % (client.Name(), statementDate)
                    continue
                
                _writeClientMt535ToAmb(client, statementDate, frequency)
                print 'Sent MT535 for client [%s]' % name
            except Exception, ex:
                print 'Exception while sending MT535 for client [%s]: %s' % (name, ex)
        
    except Exception, ex:
        print 'An exception occurred while running the script:', str(ex)
    else:
        print 'The script completed successfully'
