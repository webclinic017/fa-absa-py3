"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapReports

DESCRIPTION
    Institutional CFD Project

    Date                : 2010-10-23
    Purpose             : Generates the PDF statements for CFDs.
                          XSLT Template is located under ABSAPortfolioSwap module and called PSClientStatement.
                          The ATS user has an override on the XSLT Template to reference the fop location on the backend.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Michael Klimke
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2010-10-23 455227    Michael Klimke     Initial Implementation
2010-11-09 486643    Herman Hoon        Correct the TPL that is incorrectly shown as Deposit on the Statement if the statement is run a over rolling period.
2011-05-19 654996    Herman Hoon        Remove the margin factor override of 1 if it is 0.
2011-07-18 715943    Herman Hoon        Added the logic for DMA and Non DMA EquityTradeType Execution premiums, and prevented Voided trades from being picked up.
2011-09-16 771481    Herman Hoon        Updated the code for the Performance Summary section to reference the correct values.
2013-02-18 809119    Peter Kutnik       Updates for Voice fees on Equities
2014-11-05 000000    Andrei Conicov     Have added new functionality. Emails are sent using at_email.
ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael
import ABSAPortfolioSwapCustom
import ABSAPortfolioSwapEmailTrigger
from ABSAXML import *
import os
DEBUG = True
'''================================================================================================
================================================================================================'''
ClientStratergies = {}
ClientListCallAccounts = {}
'''================================================================================================
================================================================================================'''
def DirectorySelection():
    dir_selection = acm.FFileSelection()
    dir_selection.PickDirectory(True)
    return dir_selection
'''================================================================================================
================================================================================================'''
def BuildClientStrategyList(Client):
    PortfolioSwapList = []
    for PortfolioSwap in acm.FPortfolioSwap.Select(''):
        if IncludePortfolioSwap(PortfolioSwap, Client):
            PortfolioSwapList.append(PortfolioSwap)
    return PortfolioSwapList
'''================================================================================================
    #1 The call account and the portfolio swap should have the same conunterparty
    #2 AdditionalInfo
    #3 AdditionalInfo
    #4 Check for base portfolio  NB
    #5 The call account has trades
================================================================================================'''


def IncludePortfolioSwap(PortfolioSwap, Client):
    ''' Check that the portfolio swap is booked against the Client and confirm that it has been
        correctly set up.
    '''
    validTrades = [trade for trade in PortfolioSwap.Trades() if trade.Status() not in ('Void', 'Simulated')]

    if not validTrades:
        return False

    counterParty = validTrades[0].Counterparty()
    if counterParty is None:
        ael.log("WARNING: Portfolio swap '%s' does not have a trade counter party:" % (PortfolioSwap.Name()))
        return False

    if counterParty != Client:
        return False

    fund_portfolio = PortfolioSwap.FundPortfolio()
    if ABSAPortfolioSwapCustom.GetBasePortfolio(fund_portfolio) is None:
        if not fund_portfolio.add_info('PSClientName'):
            ael.log("WARNING: Portfolio swap '%s' does not have PSClientName add info on fund portfolio nor base portfolio:" % (PortfolioSwap.Name()))
            return False

    return True
'''================================================================================================
NOTE:
    This function will return a list of the cfd clients.
    The clients will only be in the list if they have certain criteria.

    1# They have a valid call account to with a trade to witch they are they counterparty
    2# The additional-info on the call account "Funding Instype" is set to "Call CFD Funding"
================================================================================================'''
def GetClientList():

    sql = \
    "select \
        distinct \
        P.ptyid, \
        I.insaddr \
    from \
        Instrument I,\
        Party P,\
        Trade T \
    where \
        I.instype       = 'Deposit' \
        and P.ptynbr    = T.counterparty_ptynbr \
        and I.insaddr   = T.insaddr \
        and add_info(T,'Funding Instype')= 'Call CFD Funding'\
        and I.open_end ~= 'Terminated'\
        and T.status not in ('Void','Simulated')"

    columns, data = ael.asql(sql, 0)
    for table in data:
        for row in table:
            _ClientName = row[0]
            _ACMParty = acm.FParty[row[0]]
            _ACMCallAccount = acm.FDeposit[int(row[1])]
            _PortfolioSwapList = BuildClientStrategyList(_ACMParty)
            ClientListCallAccounts[_ClientName] = [_ACMParty, _ACMCallAccount, _PortfolioSwapList]  # Note:this may grow very large

GetClientList()
'''================================================================================================
================================================================================================'''
INCEPTION = ael.date('1970-01-01')
TODAY = ael.date_today()
FIRSTOFYEAR = TODAY.first_day_of_year()
FIRSTOFMONTH = TODAY.first_day_of_month()
PREVBUSDAY = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)  # NOTE: Should really get default calendar
TWOBUSDAYSAGO = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  # NOTE: Should really get default calendar
TWODAYSAGO = TODAY.add_days(-2)
YESTERDAY = TODAY.add_days(-1)
trueFalse = ['False', 'True']
'''================================================================================================
TODO:
    Convert this to acm, problem there is no convert date to string using format
================================================================================================'''
ReportDateList = {'Inception':INCEPTION.to_string(ael.DATE_ISO), \
                    'First Of Year':FIRSTOFYEAR.to_string(ael.DATE_ISO), \
                    'First Of Month':FIRSTOFMONTH.to_string(ael.DATE_ISO), \
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO), \
                    'TwoBusinessDaysAgo':TWOBUSDAYSAGO.to_string(ael.DATE_ISO), \
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),
                    'Now':TODAY.to_string(ael.DATE_ISO)}
'''================================================================================================
================================================================================================'''
ReportTypes = ['Client Statement']
'''================================================================================================
Notes:
    Called when the Client Selection is Changed, This really should only be possible if one client is selected?
    Why would you go through the
================================================================================================'''
def SettingsCallBack(Index, FieldValues):
    if Index == 1:
        if FieldValues[1] != '<ALL>':
            List = ['<NONE>']
            for PS in ClientListCallAccounts[FieldValues[1]][2]:
                List.append(PS.Name())
            ael_variables[2][3] = List
        else:
            ael_variables[2][3] = []

    return FieldValues  # NOTE:always remember to return this else callback will not work
'''================================================================================================
================================================================================================'''
FirstTab = \
[
['reportDate', 'Report Date:', 'string', ReportDateList.keys(), TODAY.to_string(ael.DATE_ISO), 1, 0, None],
['client', 'Client:', 'string', ClientListCallAccounts.keys(), '<ALL>', 1, 0, '', SettingsCallBack],
['portfolioSwaps', 'Portfolio Swaps:', 'string', None, '<ALL>', 0, 1, None],
# ['showExpired','Show Expired Portfolio Swaps','string',trueFalse,None,0,0,'',None,1],
['reportType', 'Report Type:', 'string', ReportTypes, None, 1, 0, None],
['outputPath', 'Output Path:', DirectorySelection(), None, DirectorySelection(), 0, 1, None],
['pdfToScreen', 'PDF to Screen', 'string', trueFalse, None, 0, 0, '', None, 1],
['triggerEmail', 'Email from server_Email', 'string', trueFalse, None, 0, 0, '', None, 1],
['triggerOutputPath', 'Email Trigger File Output Path:_Email', DirectorySelection(), None, DirectorySelection(), 0, 1, 'Output path on the backend where the email trigger xml file will be created.'],
['bccAdresses', 'BBC Email Adresses_Email', 'string', None, 'abcapprimesynthetics@absacapital.com,collateral.management@absacapital.com', 0, 1, 'List of BCC email adressess seperated by a comma.'],
['fromAdress', 'From Email Adress_Email', 'string', None, 'collateral.management@absacapital.com', 0, 0, 'From email adress.'],
['testRun', 'Test run_Email', 'string', trueFalse, None, 0, 0, '', None, 1]
]
ael_variables = \
FirstTab
'''================================================================================================
================================================================================================'''
def get_report_parameters(name):
    return acm.FExtensionContext['Standard'].GetExtension('FParameters', 'FObject', name).Value()
'''================================================================================================
================================================================================================'''
def ael_main(ael_dict):

    ReportDate = ael_dict['reportDate']
    if ReportDate in ReportDateList.keys():
        ReportDate = ReportDateList[ReportDate]

    if ael_dict['client'] == '<ALL>':
        ClientList = ClientListCallAccounts.keys()
    else:
        ClientList = [ael_dict['client']]

    for Client in ClientList:
        try:

            runReport(Client, ael_dict, ReportDate)

        except Exception, e:
            acm.Log('ERROR: Statement for client %s, the following exception occurred:%s' % (Client, e))
'''================================================================================================
 #Why dont we pass the Strategy List Rather ???
================================================================================================'''
def runReport(Client, ael_dict, ReportDate):
    
    test_run = ael_dict['testRun'] == 'True'
    print('Test run set to {0}'.format(test_run))
    
    if not os.path.exists(str(ael_dict['outputPath'].SelectedDirectory())):
        print("Error: The specified directory '{0}' does not exist.".format(ael_dict['outputPath']))
        return
    
    XML = ABSAReportXML(ael_dict['reportType'], Client, ReportDate)
    XML.InputParams = ael_dict
    WorkbookUsed = get_report_parameters(ael_dict['reportType']).At('Workbook')
    StrategyList = []

    CfdClientDetails(XML, XML.RootNode, acm.FParty[Client])

    for Strategy in ClientListCallAccounts[Client][2]:  # Strategy Name is Portfolio SwapName

        if acm.Time.DateDifference(Strategy.ExpiryDate(), ReportDate) > 0  and acm.Time.DateDifference(Strategy.StartDate(), ReportDate) <= 0:

            if '<NONE>' not in ael_dict['portfolioSwaps']:

                if Strategy.Name() in ael_dict['portfolioSwaps'] or '<ALL>' in ael_dict['portfolioSwaps']:  # Filter should we do it like this??? Maybe use FPortfolio?

                    StrategyNode = XML.create_tag(XML.RootNode, 'Strategy')
                    XML.create_full_tag(StrategyNode, 'StrategyName', Strategy.Trades()[0].Portfolio().Name())
                    XML.create_full_tag(StrategyNode, 'StrategyDate', ReportDate)

                    CfdPerformanceSummary(XML, StrategyNode, Strategy, ReportDate)
                    CfdTradeActivity(XML, StrategyNode, Strategy, ReportDate)
                    CfdManufaturedDividend(XML, StrategyNode, Strategy, ReportDate)
                    CfdSyntheticFinancing(XML, StrategyNode, Strategy, ReportDate)
                    StrategyList.append(Strategy)

    if len(StrategyList) > 0:
        CfdMarginCallStatement(XML, XML.RootNode, StrategyList, ReportDate)
        CfdSummaryOfTerms(XML, XML.RootNode, StrategyList, ReportDate)

    CfdCashTransactionReport(XML, XML.RootNode, ClientListCallAccounts[Client][2], ClientListCallAccounts[Client][1], ReportDate)

    # TODO:Move to ABSAXMLReport
    StyleSheet = get_report_parameters(ael_dict['reportType']).At('Workbook')  # MKLIMKE can this not be moved to Object must be?

    XML.TranformToFo(StyleSheet)
    XML.FopConversion()

    if ael_dict['pdfToScreen'] == 'True':
        XML.PDFToScreen()
    if ael_dict['triggerEmail'] == 'True':
        ABSAPortfolioSwapEmailTrigger.writeTriggerXml(Client, ael_dict, ReportDate, XML.FileName)
        file_path = os.path.join(str(XML.InputParams['outputPath'].SelectedDirectory()), XML.FileName + '.pdf')
        attachments = [str(file_path)]
        ABSAPortfolioSwapEmailTrigger.send_statement(Client, ael_dict, ReportDate, attachments, test_run)

'''================================================================================================
Can get just one Sheet , What class is th FSheet? Can I get just One
================================================================================================'''
def CfdClientDetails(XML, Node, Client):

    ClientDetailsNode = XML.create_tag(Node, 'ClientDetails')
    XML.create_full_tag(ClientDetailsNode, 'ClientName', Client.Name())
    XML.create_full_tag(ClientDetailsNode, 'ClientFullName', Client.Fullname())
    XML.create_full_tag(ClientDetailsNode, 'ClientAccount', str(Client.Oid()))
    XML.create_full_tag(ClientDetailsNode, 'ClientTelephone', str(Client.Telephone()))
    XML.create_full_tag(ClientDetailsNode, 'ClientEmail', Client.Email())
    XML.create_full_tag(ClientDetailsNode, 'Address', Client.Address())
    XML.create_full_tag(ClientDetailsNode, 'Address2', Client.Address2())
    XML.create_full_tag(ClientDetailsNode, 'ZipCode', Client.ZipCode())
    XML.create_full_tag(ClientDetailsNode, 'City', Client.City())

'''================================================================================================
================================================================================================'''
def HasJustRolled(PortfolioSwap, Date):
    Port = PortfolioSwap.FundPortfolio().Name()
    return acm.FPortfolioSwap.Select01("fundPortfolio = '" + Port + "' and expiryDate = '" + Date + "'", '')
'''================================================================================================
================================================================================================'''
def CfdPerformanceSummary(XML, Node, PortfolioSwap, Date):

    PerformanceStartegyNode = XML.create_tag(Node, 'PerformaceSummary')
    DetailsNode = XML.create_tag(PerformanceStartegyNode, 'Details')
    PositionsNode = XML.create_tag(PerformanceStartegyNode, 'Positions')

    Calendar = acm.FCalendar['ZAR Johannesburg']
    OpeningDate = Calendar.AdjustBankingDays(Date, -1)
    ClosingDate = Calendar.AdjustBankingDays(Date, 0)

    TotalOpeningMarketExposure = 0.0
    TotalClosingMarketExposure = 0.0
    TotalTradingProfitLoss = 0.0

    for Leg in PortfolioSwap.Legs():

        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM':

            Instrument = Leg.IndexRef()
            OpeningPrice = ABSAPortfolioSwapCustom.Price(Instrument, OpeningDate)
            ClosingPrice = ABSAPortfolioSwapCustom.Price(Instrument, ClosingDate)

            RolledIns = HasJustRolled(PortfolioSwap, Date)
            if RolledIns is None:
                OpenIns = PortfolioSwap
            else:
                OpenIns = RolledIns

            OpeningPosition = GetInstrumentPosition(OpenIns, Instrument, OpeningDate)
            OpeningExposure = (OpeningPosition * OpeningPrice) / 100
            TotalOpeningMarketExposure = TotalOpeningMarketExposure + OpeningExposure

            ClosingPosition = GetInstrumentPosition(PortfolioSwap, Instrument, Date)
            ClosingExposure = (ClosingPosition * ClosingPrice) / 100
            TotalClosingMarketExposure = TotalClosingMarketExposure + ClosingExposure

            DailyExposure = GetDailyExpsosure(PortfolioSwap, Instrument, Date)
            DailyDividends = GetDailyDividends(OpeningPosition, Instrument, Date)
            DailyTPL = ((ClosingExposure - OpeningExposure) - DailyExposure) + DailyDividends
            TotalTradingProfitLoss = TotalTradingProfitLoss + DailyTPL

            if DailyTPL != 0.0 or (OpeningPosition <> 0.0 or ClosingPosition <> 0.0):
                PositionNode = XML.create_tag(PositionsNode, 'Position')
                XML.create_full_tag(PositionNode, 'CFDName', Leg.IndexRef().Name())
                XML.create_full_tag(PositionNode, 'OpeningPosition', formnum(OpeningPosition, 0))
                XML.create_full_tag(PositionNode, 'OpeningMarketPrice', formnum(OpeningPrice))
                XML.create_full_tag(PositionNode, 'OpeningMarketExposure', formnum(OpeningExposure))
                XML.create_full_tag(PositionNode, 'ClosingPosition', formnum(ClosingPosition, 0))
                XML.create_full_tag(PositionNode, 'ClosingMarketPrice', formnum(ClosingPrice))
                XML.create_full_tag(PositionNode, 'ClosingMarketExposure', formnum(ClosingExposure))
                XML.create_full_tag(PositionNode, 'TradingProfitLoss', formnum(DailyTPL))

    TotalsNode = XML.create_tag(PositionsNode, 'Totals')
    XML.create_full_tag(PositionsNode, 'TotalOpeningMarketExposure', formnum(TotalOpeningMarketExposure))
    XML.create_full_tag(PositionsNode, 'TotalClosingMarketExposure', formnum(TotalClosingMarketExposure))
    XML.create_full_tag(PositionsNode, 'TotalTradingProfitLoss', formnum(TotalTradingProfitLoss))
'''================================================================================================
Notes:
================================================================================================'''
def GetDailyExpsosure(PortfolioSwap, Security, Date):

    SecurityExpsoure = 0.0
    for Trade in PortfolioSwap.FundPortfolio().Trades():
        if Trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'] and not acm.Time.DateDifference(Date, Trade.TradeTime()):
            if Trade.Instrument() == Security:

                aelPortfolio = ael.Portfolio[PortfolioSwap.FundPortfolio().Oid()]
                ExecutionRate = getExecutionRate(Trade, aelPortfolio, Date)
                TradeExposure = (Trade.Price() * Trade.Quantity()) / 100
                ExecutionPrem = abs((TradeExposure * ExecutionRate) / 100)
                AllInExpsoure = TradeExposure + ExecutionPrem
                SecurityExpsoure = SecurityExpsoure + AllInExpsoure
    return SecurityExpsoure

'''================================================================================================
Notes:
================================================================================================'''
def GetDailyDividends(Position, Security, Date):
    for Dividend in Security.Dividends():
        if not acm.Time.DateDifference(Date, Dividend.ExDivDay()):
            return Position * Dividend.Amount()
    return 0.0
'''================================================================================================
================================================================================================'''
def GetReset(CashFlow, Type, Date):
    for Reset in CashFlow.Resets():
        if Reset.ResetType() == Type and not acm.Time.DateDifference(Date, Reset.Day()):
            return Reset
    return None


def getExecutionRate(Trade, aelPortfolio, Date):
    '''Get the execution rate for a certain trade
    '''
    ExecutionRate = 0.0
    trade_type = Trade.EquityTradeType()

    if trade_type == 'Trade Report':
        ExecutionRate = float(ABSAPortfolioSwapCustom.get_timseries_value(aelPortfolio, 'PSExtExecPremNonDMA', ael.date(Date)))
    elif trade_type == 'Voice':
        ExecutionRate = float(ABSAPortfolioSwapCustom.get_timseries_value(aelPortfolio, 'PSExtExecPremVoice', ael.date(Date)))
    else:
        ExecutionRate = float(ABSAPortfolioSwapCustom.get_timseries_value(aelPortfolio, 'PSExtExecPremRate', ael.date(Date)))
    return ExecutionRate

'''================================================================================================
Notes:
    Might be better to do a select for Trades.
    The Trade need to be grouped by their Instruments
XML:
    </TradingActivity/Trades/Security/Trade>                    path where all the trades are
    </TradingActivity/Trades/Security/TradeInstrument/"ZAR/AGL">  node value is the trade instrument
TODO:
    Is such a long path necessary for the trades keeping in mind we have to group?

Notes why don't we build the dictionary like in the Margin Call Statment ???
==============================================================================================='''
def CfdTradeActivity(XML, Node, PortfolioSwap, Date):

    TradingActivityNode = XML.create_tag(Node, 'TradingActivity')
    TradesNode = XML.create_tag(TradingActivityNode, 'Trades')
    TotalBuyQuantity = 0.0
    TotalSellQuantity = 0.0
    TotalTradeExposure = 0.0
    IntrumentVWAPBuy = {}
    IntrumentVWAPSell = {}

    for Trade in PortfolioSwap.FundPortfolio().Trades():

        if Trade.Status() in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'] and not acm.Time.DateDifference(Date, Trade.TradeTime()):

            InstrumentNode = XML.FindNodeWithValue(TradesNode, 'TradeInstrument', Trade.Instrument().Name())
            if InstrumentNode is None:
                SecurityNode = XML.create_tag(TradesNode, 'Security')
                XML.create_full_tag(SecurityNode, 'TradeInstrument', Trade.Instrument().Name())
            else:
                SecurityNode = InstrumentNode.parentNode


            TradePrice = Trade.Price()
            TradeQuantity = Trade.Quantity()
            TradeExposure = (TradePrice * TradeQuantity) / 100

            aelPortfolio = ael.Portfolio[PortfolioSwap.FundPortfolio().Oid()]

            ExecutionRate = getExecutionRate(Trade, aelPortfolio, Date)
            ExecutionPrem = abs((TradeExposure * ExecutionRate) / 100)

            TradeNode = XML.create_tag(SecurityNode, 'Trade')
            XML.create_full_tag(TradeNode, 'TradeReference', str(Trade.Oid()))
            XML.create_full_tag(TradeNode, 'TradeTime', str(Trade.TradeTime()))
            XML.create_full_tag(TradeNode, 'TradePrice', formnum(TradePrice))
            XML.create_full_tag(TradeNode, 'TradeQuantity', formnum(TradeQuantity, 0))

            Ex = TradePrice * TradeQuantity
            TotalTradeExposure = TotalTradeExposure + Ex

            if TradeQuantity > 0:

                if Trade.Instrument().Name() not in IntrumentVWAPBuy.keys():
                    IntrumentVWAPBuy[Trade.Instrument().Name()] = [Ex, TradeQuantity]
                else:
                    IntrumentVWAPBuy[Trade.Instrument().Name()][0] = IntrumentVWAPBuy[Trade.Instrument().Name()][0] + Ex
                    IntrumentVWAPBuy[Trade.Instrument().Name()][1] = IntrumentVWAPBuy[Trade.Instrument().Name()][1] + TradeQuantity

                VWAPPrice = IntrumentVWAPBuy[Trade.Instrument().Name()][0] / IntrumentVWAPBuy[Trade.Instrument().Name()][1]

                XML.create_full_tag(TradeNode, 'TradeBuySell', 'Buy')
                XML.UpdateNodeValue(SecurityNode, 'TotalLongTradePrice', float(VWAPPrice), 1)
                XML.UpdateNodeValue(SecurityNode, 'TotalLongTradeQuantity', TradeQuantity, 0, 0)
                XML.UpdateNodeValue(SecurityNode, 'TotalLongTradeExposure', TradeExposure)
                XML.UpdateNodeValue(SecurityNode, 'TotalLongTradeExecutionPremium', ExecutionPrem)
                XML.UpdateNodeValue(SecurityNode, 'TotalLongTradeAllInExposure', TradeExposure + ExecutionPrem)
            else:
                if Trade.Instrument().Name() not in IntrumentVWAPSell.keys():
                    IntrumentVWAPSell[Trade.Instrument().Name()] = [Ex, TradeQuantity]
                else:
                    IntrumentVWAPSell[Trade.Instrument().Name()][0] = IntrumentVWAPSell[Trade.Instrument().Name()][0] + Ex
                    IntrumentVWAPSell[Trade.Instrument().Name()][1] = IntrumentVWAPSell[Trade.Instrument().Name()][1] + TradeQuantity

                VWAPPrice = IntrumentVWAPSell[Trade.Instrument().Name()][0] / IntrumentVWAPSell[Trade.Instrument().Name()][1]

                XML.create_full_tag(TradeNode, 'TradeBuySell', 'Sell')
                XML.UpdateNodeValue(SecurityNode, 'TotalShortTradePrice', float(VWAPPrice), 1)
                XML.UpdateNodeValue(SecurityNode, 'TotalShortTradeQuantity', TradeQuantity, 0, 0)  # Need to Add Decimal Places here
                XML.UpdateNodeValue(SecurityNode, 'TotalShortTradeExposure', TradeExposure)
                XML.UpdateNodeValue(SecurityNode, 'TotalShortTradeExecutionPremium', ExecutionPrem)
                XML.UpdateNodeValue(SecurityNode, 'TotalShortTradeAllInExposure', TradeExposure + ExecutionPrem)

            XML.create_full_tag(TradeNode, 'TradeExposure', formnum(TradeExposure))
            XML.create_full_tag(TradeNode, 'TradeExectionPreium', formnum(ExecutionPrem))
            XML.create_full_tag(TradeNode, 'TradeAllInExpsoure', formnum(TradeExposure + ExecutionPrem))
'''================================================================================================
================================================================================================'''
def CfdManufaturedDividend(XML, Node, PortfolioSwap, Date):

    TotalDivs = 0.0
    Calendar = acm.FCalendar['ZAR Johannesburg']
    PosDate = Calendar.AdjustBankingDays(Date, -1)
    ManufaturedDividendsNode = XML.create_tag(Node, 'ManufacturedDividends')

    for i in PortfolioSwap.FundPortfolio().Instruments():  # TODO: maybe better todo legs
        for div in i.Dividends():
            if not acm.Time.DateDifference(Date, div.ExDivDay()):
                DividendNode = XML.create_tag(ManufaturedDividendsNode, 'Dividend')
                Pos = GetInstrumentPosition(PortfolioSwap, i, PosDate)  # NOTE: must get position -1 business day
                XML.create_full_tag(DividendNode, 'CFDName', i.Name())
                XML.create_full_tag(DividendNode, 'LDTPosition', formnum(Pos))
                XML.create_full_tag(DividendNode, 'DPS', str(div.Amount()))
                XML.create_full_tag(DividendNode, 'Factor', str(div.TaxFactor()))
                XML.create_full_tag(DividendNode, 'Total', formnum(Pos * div.Amount()))
                XML.create_full_tag(DividendNode, 'Type', 'Cash')
                TotalDivs = TotalDivs + (Pos * div.Amount())

    XML.create_full_tag(ManufaturedDividendsNode, 'TotalDividends', formnum(TotalDivs))
'''================================================================================================
================================================================================================'''
def CfdSyntheticFinancing(XML, Node, PortfolioSwap, Date):

    SyntheticFinacingNode = XML.create_tag(Node, 'SyntheticFinacing')
    Calendar = acm.FCalendar['ZAR Johannesburg']
    OpeningDate = Calendar.AdjustBankingDays(Date, -1)
    DateDiff = acm.Time.DateDifference(Date, OpeningDate)

    TotalOpeningMarketValue = 0.0
    TotalOverNightPremium = 0.0

    for Leg in PortfolioSwap.Legs():

        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM':

            Instrument = Leg.IndexRef()
            RolledIns = HasJustRolled(PortfolioSwap, Date)

            if RolledIns is None:
                OpenIns = PortfolioSwap
            else:
                OpenIns = RolledIns

            OpeningPos = GetInstrumentPosition(OpenIns, Instrument, OpeningDate)
            Pos = GetInstrumentPosition(PortfolioSwap, Instrument, Date)

            if OpeningPos <> 0.0:

                InstrumentNode = XML.create_tag(SyntheticFinacingNode, 'Instrument')
                OpeningPrice = ABSAPortfolioSwapCustom.Price(Instrument, OpeningDate)
                OpeningMarketValue = (OpeningPos * OpeningPrice) / 100
                ReferenceRate, FinancingSpread, ScriptSpread, AllInRate = GetFinancingRates(PortfolioSwap, Instrument, Date, OpeningPos)

                OverNightPremium = (((OpeningMarketValue * AllInRate) / 365) / 100) * DateDiff

                XML.create_full_tag(InstrumentNode, 'CFDName', Instrument.Name())
                XML.create_full_tag(InstrumentNode, 'OpeningMarketValue', formnum(OpeningMarketValue))
                XML.create_full_tag(InstrumentNode, 'ReferenceRate', formnum(ReferenceRate, 2))
                XML.create_full_tag(InstrumentNode, 'OverNightRate', formnum(FinancingSpread, 2))

                ScriptSpread = ScriptSpread * -1
                if abs(round(ScriptSpread, 2)) == 0.00:
                    ScriptSpread = abs(ScriptSpread)

                XML.create_full_tag(InstrumentNode, 'ShortRate', formnum(ScriptSpread, 2))
                XML.create_full_tag(InstrumentNode, 'AllInFinacingRate', formnum(AllInRate, 2))
                XML.create_full_tag(InstrumentNode, 'OverNightPremium', formnum(OverNightPremium * -1))

                TotalOpeningMarketValue = TotalOpeningMarketValue + OpeningMarketValue
                TotalOverNightPremium = TotalOverNightPremium + OverNightPremium


    XML.create_full_tag(SyntheticFinacingNode, 'TotalOpeningMarketValue', formnum(TotalOpeningMarketValue))
    XML.create_full_tag(SyntheticFinacingNode, 'TotalOverNightPremium', formnum(TotalOverNightPremium * -1))
    XML.create_full_tag(SyntheticFinacingNode, 'FundingDays', str(DateDiff))
'''================================================================================================
NOTE:
================================================================================================'''
def GetFinancingRates(PortfolioSwap, Instrument, Date, OpeningPos):

    ReferenceRate = 0.0  # note: base rate from rate index, underlying rate index if spread
    FinancingSpread = 0.0  # note: spread on top of base rate , represented and a rate-index with and underlying rate-ind+ex
    ScriptSpread = 0.0  # note: short lending rate, see RepoRate() function for description
    AllInRate = 0.0

    aelPortSwap = ael.Instrument[PortfolioSwap.Name()]  # TODO: Convert to ACM
    RateIndex = acm.FInstrument[PortfolioSwap.add_info('PSONPremIndex')]

    if RateIndex.Underlying() is None:
        ReferenceRate = ABSAPortfolioSwapCustom.Price(RateIndex, Date, 0, -1)
        if OpeningPos < 0:
            ScriptSpread = ABSAPortfolioSwapCustom.RepoRate(aelPortSwap, None, Instrument, Date)
    else:
        ReferenceRate = ABSAPortfolioSwapCustom.Price(RateIndex.Underlying(), Date, 0, -1)
        if OpeningPos > 0:
            FinancingSpread = ABSAPortfolioSwapCustom.Price(RateIndex, Date, 2, -1)
        else:
            FinancingSpread = ABSAPortfolioSwapCustom.Price(RateIndex, Date, 1, -1)
            ScriptSpread = ABSAPortfolioSwapCustom.RepoRate(aelPortSwap, None, Instrument, Date)

    AllInRate = (ReferenceRate + (FinancingSpread - ScriptSpread))
    return [ReferenceRate, FinancingSpread, ScriptSpread, AllInRate]
'''================================================================================================
TODO:
    List for easy Identification of Dictionary items
================================================================================================'''
def CfdMarginCallStatement(XML, Node, PortfolioSwaps, Date):


    Positions = {}
    MarginCallStatementNode = XML.create_tag(Node, 'MarginCallStatement')
    XML.create_full_tag(MarginCallStatementNode, 'Date', Date)

    Calendar = acm.FCalendar['ZAR Johannesburg']
    OpeningDate = Calendar.AdjustBankingDays(Date, -1)
    ClosingDate = Calendar.AdjustBankingDays(Date, 0)

    TotalOpeningMarketValue = 0.0
    TotalOpeningMarginRequirement = 0.0
    TotalClosingMarketValue = 0.0
    TotalChangeInMarginRequirement = 0.0
    TotalCloseInMarginRequirement = 0.0

    for PortfolioSwap in PortfolioSwaps:  # Go through all Portfolio Swap and Add the value's
        for Leg in PortfolioSwap.Legs():
            if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM':

                Instrument = Leg.IndexRef()
                RolledIns = HasJustRolled(PortfolioSwap, Date)
                if RolledIns is None:
                    OpenIns = PortfolioSwap
                else:
                    OpenIns = RolledIns

                OpeningPos = GetInstrumentPosition(OpenIns, Instrument, OpeningDate)  # CHECK: Use this function in CFD Summary
                OpeningPrice = ABSAPortfolioSwapCustom.Price(Instrument, OpeningDate)
                OpeningMarketValue = (OpeningPos * OpeningPrice) / 100

                ClosingPos = GetInstrumentPosition(PortfolioSwap, Instrument, ClosingDate)  # CHECK: Use this function in CFD Summary
                ClosingPrice = ABSAPortfolioSwapCustom.Price(Instrument, ClosingDate)
                ClosingMarketValue = (ClosingPos * ClosingPrice) / 100

                TodaysMarginRate = GetMarginRate(PortfolioSwap, Instrument, Date)
                YesterdaysMarginRate = GetMarginRate(OpenIns, Instrument, OpeningDate)

                OpeningMarginRequired = ((OpeningMarketValue * YesterdaysMarginRate) / 100)
                ClosingMarginRequired = ((ClosingMarketValue * TodaysMarginRate) / 100)


                if Instrument.Name() in Positions.keys():
                    Positions[Instrument.Name()][2] = Positions[Instrument.Name()][2] + OpeningMarketValue
                    Positions[Instrument.Name()][3] = Positions[Instrument.Name()][3] + OpeningMarginRequired
                    Positions[Instrument.Name()][4] = Positions[Instrument.Name()][4] + ClosingMarketValue
                    Positions[Instrument.Name()][6] = Positions[Instrument.Name()][6] + ClosingMarginRequired
                else:
                    Positions[Instrument.Name()] = [0, 0, 0, 0, 0, 0, 0]
                    Positions[Instrument.Name()][0] = Instrument.add_info('PSSectorCode')
                    Positions[Instrument.Name()][1] = TodaysMarginRate
                    Positions[Instrument.Name()][2] = OpeningMarketValue
                    Positions[Instrument.Name()][3] = OpeningMarginRequired
                    Positions[Instrument.Name()][4] = ClosingMarketValue
                    Positions[Instrument.Name()][6] = ClosingMarginRequired

    for Position in Positions.keys():

        if Positions[Position][2] != 0 or Positions[Position][4] != 0:

            ChangeInMarginRequired = abs(Positions[Position][6]) - abs(Positions[Position][3])
            TotalOpeningMarketValue = TotalOpeningMarketValue + Positions[Position][2]
            TotalOpeningMarginRequirement = TotalOpeningMarginRequirement + abs(Positions[Position][3])
            TotalClosingMarketValue = TotalClosingMarketValue + Positions[Position][4]
            TotalChangeInMarginRequirement = TotalChangeInMarginRequirement + ChangeInMarginRequired
            TotalCloseInMarginRequirement = TotalCloseInMarginRequirement + abs(Positions[Position][6])

            PositionNode = XML.create_tag(MarginCallStatementNode, 'Position')
            XML.create_full_tag(PositionNode, 'CFDName', Position)
            XML.create_full_tag(PositionNode, 'Category', str(Positions[Position][0]))
            XML.create_full_tag(PositionNode, 'MarginPercentage', formnum(Positions[Position][1]))
            XML.create_full_tag(PositionNode, 'OpeningMarketValue', formnum(Positions[Position][2]))
            XML.create_full_tag(PositionNode, 'OpeningMarginRequirement', formnum(abs(Positions[Position][3])))
            XML.create_full_tag(PositionNode, 'ClosingMarketValue', formnum(Positions[Position][4]))
            XML.create_full_tag(PositionNode, 'ChangeInMarginRequirement', formnum(ChangeInMarginRequired))
            XML.create_full_tag(PositionNode, 'CloseInMarginRequirement', formnum(abs(Positions[Position][6])))

    XML.create_full_tag(MarginCallStatementNode, 'TotalOpeningMarketValue', formnum(TotalOpeningMarketValue))
    XML.create_full_tag(MarginCallStatementNode, 'TotalOpeningMarginRequirement', formnum(TotalOpeningMarginRequirement))
    XML.create_full_tag(MarginCallStatementNode, 'TotalClosingMarketValue', formnum(TotalClosingMarketValue))
    XML.create_full_tag(MarginCallStatementNode, 'TotalChangeInMarginRequirement', formnum(TotalChangeInMarginRequirement))
    XML.create_full_tag(MarginCallStatementNode, 'TotalCloseInMarginRequirement', formnum(TotalCloseInMarginRequirement))

    Portfolio = ABSAPortfolioSwapCustom.GetBasePortfolio(PortfolioSwaps[0].FundPortfolio())
    if Portfolio:
        account_name = Portfolio.add_info('PSClientCallAcc')
    else:
        account_name = PortfolioSwaps[0].FundPortfolio().add_info('PSClientCallAcc')
    CallAccount = acm.FInstrument[account_name]
    Balance = CalculatedBalance(PortfolioSwaps, CallAccount, ClosingDate)

    XML.create_full_tag(MarginCallStatementNode, 'ClosingCashBalance', formnum(Balance))
    XML.create_full_tag(MarginCallStatementNode, 'MarginAvailableToYou', formnum(round(Balance, 2) - round(TotalCloseInMarginRequirement, 2)))
'''================================================================================================
    Difference in trading manager is that uese TimeSeries Test , Rather have one function
NOTES:
    Margin Fact sits on the FundPortfolio....
================================================================================================'''
def GetMarginRate(PortfolioSwap, Instrument, Date):

    TempIns = ael.Instrument[Instrument.Oid()]
    TempPortACM = ABSAPortfolioSwapCustom.GetBasePortfolio(PortfolioSwap.FundPortfolio())
    if TempPortACM:
        TempPort = ael.Portfolio[TempPortACM.Oid()]
    else:
        TempPort = ael.Portfolio[PortfolioSwap.FundPortfolio().Oid()]
    PSSectorMargin = float(ABSAPortfolioSwapCustom.get_timseries_value(TempIns, 'PSSectorMargin', ael.date(Date)))  # TODO: rewrite this to use ACM
    PSMarginFactor = float(ABSAPortfolioSwapCustom.get_timseries_value(TempPort, 'PSMarginFactor', ael.date(Date)))  # TODO: rewrite this to use ACM

    if PSSectorMargin:
        return PSSectorMargin * PSMarginFactor
    else:
        return 100
'''================================================================================================
TODO:
    Exception handling
    Need top get callaccount
================================================================================================'''
def CfdCashTransactionReport(XML, Node, PortfolioSwaps, CallAccount, Date):

    CashTransactionReportNode = XML.create_tag(Node, 'CashTransactionReport')
    Calendar = acm.FCalendar['ZAR Johannesburg']
    OpeningDate = Calendar.AdjustBankingDays(Date, -1)
    FirstDayOfMonth = acm.Time.FirstDayOfMonth(Date)
    NameList = []  # Note: Need to get a list of the pswap names to compare with additional-info's

    for PortfolioSwap in PortfolioSwaps:
        NameList.append(PortfolioSwap.Name())
    #----------------------------------------------------------------------------------------------------------------------
    aelCallAccount = ael.Instrument[CallAccount.Oid()]

    if acm.Time.DateDifference(Date, FirstDayOfMonth) == 0:  # should this be business days ???

        MonthToDateAccruedInterest = 0
        DailyAccruedInterest = 0
    else:
        DailyAccruedInterest = GetCalculation(CallAccount.Trades()[0], Date, 'Portfolio Carry Daily')
        MonthToDateAccruedInterest = GetCalculation(CallAccount.Trades()[0], Date, 'Portfolio Carry Monthly')
        FitsDayInterest = GetCalculation(CallAccount.Trades()[0], FirstDayOfMonth, 'Portfolio Carry Daily')
        MonthToDateAccruedInterest = MonthToDateAccruedInterest - FitsDayInterest


    InterestCapitalised = aelCallAccount.interest_settled(ael.date(OpeningDate), ael.date(Date)) * -1
    #----------------------------------------------------------------------------------------------------------------------

    Deposits = 0.0
    Sweep = 0.0
    CurrentReset = CallAccount.CurrentReset(OpeningDate)
    if CurrentReset is not None:
        FixedRate = CurrentReset.FixingValue()
    else:
        FixedRate = 0.0

    for CashFlow in CallAccount.Legs()[0].CashFlows():

        Strategy = CashFlow.add_info('PSCashType')
        if CashFlow.CashFlowType() == 'Fixed Amount':

            if not acm.Time.DateDifference(Date, CashFlow.StartDate()):  # and the StartDate is ''
                if Strategy in NameList:
                    CFDProfitLossNode = XML.create_tag(CashTransactionReportNode, 'CFDProfitLoss')
                    XML.create_full_tag(CFDProfitLossNode, 'Amount', formnum(CashFlow.FixedAmount()))
                    XML.create_full_tag(CFDProfitLossNode, 'Strategy', acm.FPortfolioSwap[Strategy].Trades()[0].Portfolio().Name())
                    XML.create_full_tag(CFDProfitLossNode, 'Date', CashFlow.PayDate())
                    Sweep = Sweep + CashFlow.FixedAmount()
                else:
                    CFDProfitLossNode = XML.create_tag(CashTransactionReportNode, 'Payment')
                    XML.create_full_tag(CFDProfitLossNode, 'Amount', formnum(CashFlow.FixedAmount()))
                    XML.create_full_tag(CFDProfitLossNode, 'Date', CashFlow.PayDate())
                    Deposits = Deposits + CashFlow.FixedAmount()

            if not acm.Time.DateDifference(Date, CashFlow.PayDate()) and CashFlow.StartDate() == '':

                if Strategy in NameList:
                    CFDProfitLossNode = XML.create_tag(CashTransactionReportNode, 'CFDProfitLoss')
                    XML.create_full_tag(CFDProfitLossNode, 'Amount', formnum(CashFlow.FixedAmount()))
                    XML.create_full_tag(CFDProfitLossNode, 'Strategy', acm.FPortfolioSwap[Strategy].Trades()[0].Portfolio().Name())
                    XML.create_full_tag(CFDProfitLossNode, 'Date', CashFlow.PayDate())
                    Sweep = Sweep + CashFlow.FixedAmount()

                else:
                    CFDProfitLossNode = XML.create_tag(CashTransactionReportNode, 'Payment')
                    XML.create_full_tag(CFDProfitLossNode, 'Amount', formnum(CashFlow.FixedAmount()))
                    XML.create_full_tag(CFDProfitLossNode, 'Date', CashFlow.PayDate())
                    Deposits = Deposits + CashFlow.FixedAmount()

    OpeningBalance = GetCalculation(CallAccount.Trades()[0], OpeningDate, 'CFD Balance')
    ClosingBalance = OpeningBalance + Deposits + Sweep + InterestCapitalised

    XML.create_full_tag(CashTransactionReportNode, 'Date', Date)
    XML.create_full_tag(CashTransactionReportNode, 'DailyAccruedInterest', formnum(DailyAccruedInterest * -1))
    XML.create_full_tag(CashTransactionReportNode, 'MonthToDateAccruedInterest', formnum(MonthToDateAccruedInterest * -1))
    XML.create_full_tag(CashTransactionReportNode, 'FixedRate', formnum(FixedRate, 2))
    XML.create_full_tag(CashTransactionReportNode, 'OpeningBalance', formnum(OpeningBalance))
    XML.create_full_tag(CashTransactionReportNode, 'Deposits', formnum(Deposits))
    XML.create_full_tag(CashTransactionReportNode, 'OverNightInterest', formnum(InterestCapitalised))
    XML.create_full_tag(CashTransactionReportNode, 'ClosingBalance', formnum(ClosingBalance))
    XML.create_full_tag(CashTransactionReportNode, 'Account', str(CallAccount.Trades()[0].Oid()))
'''================================================================================================
================================================================================================'''
def CalculatedBalance(PortfolioSwaps, CallAccount, Date):
    Calendar = acm.FCalendar['ZAR Johannesburg']
    OpeningDate = Calendar.AdjustBankingDays(Date, -1)
    FirstDayOfMonth = acm.Time.FirstDayOfMonth(Date)
    NameList = []  # Note: Need to get a list of the pswap names to compare with additional-info's

    for PortfolioSwap in PortfolioSwaps:
        NameList.append(PortfolioSwap.Name())

    #----------------------------------------------------------------------------------------------------------------------
    aelCallAccount = ael.Instrument[CallAccount.Oid()]
    InterestCapitalised = aelCallAccount.interest_settled(ael.date(OpeningDate), ael.date(Date)) * -1
    #----------------------------------------------------------------------------------------------------------------------
    Deposits = 0.0
    Sweep = 0.0

    for CashFlow in CallAccount.Legs()[0].CashFlows():

        Strategy = CashFlow.add_info('PSCashType')

        if CashFlow.CashFlowType() == 'Fixed Amount':


            if not acm.Time.DateDifference(Date, CashFlow.StartDate()):  # and the StartDate is ''
                if Strategy in NameList:
                    Sweep = Sweep + CashFlow.FixedAmount()
                else:
                    Deposits = Deposits + CashFlow.FixedAmount()

            if not acm.Time.DateDifference(Date, CashFlow.PayDate()) and CashFlow.StartDate() == '':
                if Strategy in NameList:
                    Sweep = Sweep + CashFlow.FixedAmount()
                else:
                    Deposits = Deposits + CashFlow.FixedAmount()




    OpeningBalance = GetCalculation(CallAccount.Trades()[0], OpeningDate, 'CFD Balance')

    ClosingBalance = OpeningBalance + Deposits + Sweep + InterestCapitalised
    return ClosingBalance

'''================================================================================================
================================================================================================'''
def CfdSummaryOfTerms(XML, Node, PortfolioSwaps, Date):

    SummaryOfTermsNode = XML.create_tag(Node, 'SummaryOfTerms')
    for PortfolioSwap in PortfolioSwaps:

        StartegyNode = XML.create_tag(SummaryOfTermsNode, 'Strategy')
        ExecutionPremium = float(ABSAPortfolioSwapCustom.get_timseries_value(ael.Portfolio[PortfolioSwap.FundPortfolio().Oid()], 'PSExtExecPremRate', ael.date(Date)))
        RateIndex = acm.FInstrument[PortfolioSwap.add_info('PSONPremIndex')]
        ReferenceRate = 0.0

        if RateIndex.Underlying() is None:
            ReferenceRate = RateIndex.Name()
        else:
            ReferenceRate = RateIndex.Underlying().Name()

        FixedRate = 0

        BasePort = ABSAPortfolioSwapCustom.GetBasePortfolio(PortfolioSwap.FundPortfolio())
        if BasePort:
            account_name = BasePort.add_info('PSClientCallAcc')
        else:
            account_name = PortfolioSwaps[0].FundPortfolio().add_info('PSClientCallAcc')
        CallAccount = acm.FInstrument[account_name]
        
        FixedRate = CallAccount.Legs()[0].FixedRate()


        XML.create_full_tag(StartegyNode, 'StrategyName', PortfolioSwap.Trades()[0].Portfolio().Name())
        XML.create_full_tag(StartegyNode, 'ExecutionPremium', formnum(ExecutionPremium * 100) + 'bp')
        XML.create_full_tag(StartegyNode, 'ReferenceFundingRate', ReferenceRate)

'''================================================================================================
==============================================================================================='''
def GetPositionReset(PortfolioSwap, Date):
    for Leg in PortfolioSwap.Legs():
        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM':
           return GetReset(Leg.CashFlows()[0], 'Nominal Scaling', Date)  # TODO Go directlty to Reset
'''================================================================================================
================================================================================================'''
def GetInstrumentPosition(PortfolioSwap, Instrument, Date):
    for Leg in PortfolioSwap.Legs():
        if ABSAPortfolioSwapCustom.LegType(Leg) == 'MTM' and Leg.IndexRef() == Instrument:
           Reset = GetReset(Leg.CashFlows()[0], 'Nominal Scaling', Date)
           if Reset is not None:
                return Reset.FixingValue()
           else:
                return 0.0  # Should we do this?
    return 0.0
'''================================================================================================
================================================================================================'''
def startRunScript(eii):
    acm.RunModuleWithParameters('ABSAPortfolioSwapReports', acm.GetDefaultContext())
'''================================================================================================
Rather Pass Column Name
================================================================================================'''
def GetCalculation(Item, EndDate, Column):

    calcSpace = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')

    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')

    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', EndDate)

    # EdmundoChissungo (quick and dirty method):the patch to supress the trading manager #
    # which caused the original error that broke this client report
    try:

        Calc = calcSpace.CreateCalculation(Item, Column)
        Balance = Calc.Value().Number()

    except Exception, e:
        acm.Log('ERROR:%s: temp solution on Line# 898' % e)
        Balance = 0.0

    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')

    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    return Balance
