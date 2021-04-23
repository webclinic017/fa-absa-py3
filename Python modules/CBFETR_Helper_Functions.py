'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Helper_Functions
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module contains functions that are being used throughout the entire solution.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2013-02-05      XXXXXX          Heinrich Cronje                 Added Get Country Code function to be reference
                                                                from ASQL for static reports.
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade
2013-08-19      XXXXXX          Heinrich Cronje                 Post Production Changes - Updated Isin ZAG 
                                                                restriction section.
2015-06-11      BOP-12          Melusi Maseko                   ZAR to ZAR transactions changes - For ZAR transactions,
                                                                business status on the cpty has to be Interbank
2015-10-28      FXFA-1969       Melusi Maseko                   FX Bloomberg trades Restrictions - Exclude trades marked
                                                                with a MidasSettlement indicator that is "true" 
2015-12-04      MINT-456        Melusi Maseko                   Enable Cash Payment moneyFlows to be sent through

2016-07-13      FXFA-2987       Melusi Maseko                   Update midassettlement logic to be used from trade object and not via object calculation space.

2016-09-14      MINT-789        Melusi Maseko                   Restrict trades where a counterparty holds a Vostro account with ABSA

2016-09-27      MINT-956        Melusi Maseko                   If Acquirer = EQ Derivatives Desk and Trader = OBP_USER_PRD, then exclude as valid moneyflow. (DO NOT FEED ODP).

2018-01-19      ABITFA-5211     Melusi Maseko                   Remove Portfolio Swaps from being sent for BoP Reporting irrespective of the acquirer.        

2018-05-25      AMD-222         Melusi Maseko                   Restrict trades where portfolios are LCH and acquirer is IRD Desk

2018-10-01      AMD-315         Sizwe Sokopo                    Restricting Trades from PRIME SERVICES DESK, by Trader ATS 

2020-07-16      AMFD-116        Sizwe Sokopo                    Filter Out Mirror Trades 
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Various helper functions that are used by various modules for the CBFETR implementation.
'''
import acm, ael, amb
import CBFETR_Parameters as Params
import CBFETR_Message_Detail as Detail

def isForeignClient(party):
    foreignClient = False
    if party:
        if party.Free2ChoiceList():
            if party.Free2ChoiceList().Name() == 'Yes':
                foreignClient = True
    return foreignClient

def get_Message_Info(MESSAGE_TYPE, REQUEST_ID, MESSAGE_COUNT, ERROR_MESSAGE, COMMAND_NAME = '', COMMAND_PARAMETER = ''):
    message_detail = {}
    message_detail['MESSAGE_TYPE'] = MESSAGE_TYPE
    message_detail['REQUEST_ID'] = REQUEST_ID
    message_detail['MESSAGE_COUNT'] = MESSAGE_COUNT
    message_detail['ERROR_MESSAGE'] = ERROR_MESSAGE
    message_detail['COMMAND_NAME'] = COMMAND_NAME
    message_detail['COMMAND_PARAMETER'] = COMMAND_PARAMETER
    
    return [('MESSAGE_DETAIL', message_detail)]

def construct_AMBA_Message(messageDetail):
    '''--------------------------------------------------------------------------
                            Constructing the AMBA Message
    --------------------------------------------------------------------------'''
    message = amb.mbf_start_message(None, 'SYSTEM_GENERATED', '1.0', None, Params.senderSource)
    
    msgList = message.mbf_start_list('DATA')

    for section in messageDetail:
        tag_list = [msgList]
        
        for tuple in section:
            mb_msg = tag_list[len(tag_list) - 1].mbf_start_list(tuple[0])
            for item in tuple[1]:
                mb_msg.mbf_add_string(item, str(tuple[1][item]))
            tag_list.append(mb_msg)
        
        item = len(tag_list) - 1
        for i in range(item, 0):
            tag_list[i].mbf_end_list()
    
    msgList.mbf_end_list()
    
    message.mbf_end_message()
    
    return message

def get_Country_Code(temp, country, *rest):
    countryCode = None
    detailClass = Detail.Message_Detail(None)
    if detailClass:
        countryCode = detailClass.get_Country_Code(country)
    return countryCode

def get_Reportable_Indicator(temp, moneyFlow, *rest):
    reportingIndicator = None
    if moneyFlow.Currency().Name() == 'ZAR' and not isForeignClient(moneyFlow.Counterparty()):
        reportingIndicator = 'N/A'
    else:
        detailClass = Detail.Message_Detail(moneyFlow)
        reportingIndicator = detailClass.get_Reportable_Indicator()
    return reportingIndicator

def CallFixedRateAdjustableTest(temp, moneyFlow, today, *rest):
    testResult = False
    if moneyFlow.Type() == 'Call Fixed Rate Adjustable':
        instrument = moneyFlow.Trade().Instrument()
        leg = instrument.Legs()[0]
        if leg.Reinvest() == False:
            rollingBaseDate = ael.date(leg.RollingPeriodBase())
            if rollingBaseDate <= today:
                ael_InstrumentCurr = ael.Instrument[instrument.Currency().Name()]
                cashflow = moneyFlow.SourceObject()
                cf_startDate = ael.date(cashflow.StartDate())
                cf_endDate = ael.date(cashflow.EndDate())
                cf_payDate = ael.date(cashflow.PayDate())
                cf_adjustedEndDate = ael.date(cf_endDate.adjust_to_banking_day(ael_InstrumentCurr, 'Following'))
                PREV_BANKING_DATE = today.add_banking_day(ael_InstrumentCurr, -1)
                
                if (PREV_BANKING_DATE >= cf_startDate and PREV_BANKING_DATE < cf_endDate) or (cf_adjustedEndDate != cf_payDate and cf_payDate == today):
                    testDate = rollingBaseDate
                    rollingPeriod = leg.RollingPeriod()
                    
                    if rollingPeriod == '0d':
                        return testResult
                    
                    while testDate <= today.add_months(-1):
                        testDate = testDate.add_period(rollingPeriod)
                    
                    testDate = testDate.adjust_to_banking_day(ael_InstrumentCurr, leg.ResetDayMethod())
                    
                    if testDate == today:
                        testResult = True 
    else:
        testResult = True
    
    return testResult
    
class Data_Selection():
    def __init__(self, AMBA_Data_Struct):
        self.Control_Message = None
        self.MessageCounter = 0
        self.AMBA_Data_Struct = AMBA_Data_Struct
        self.TODAY = ael.date(self.AMBA_Data_Struct.AMBA_Date)
        self.START_DATE = self.TODAY.add_days(-15)
        self.MONEY_FLOW_DATE = self.TODAY.add_years(-1)
        self.Scope_Objects = None
        self.Messages = acm.FArray()
    
    def __del__(self):
        self.Control_Message = None
        self.MessageCounter = None
        self.AMBA_Data_Struct = None
        self.Scope_Object = None
        self.Messages.Clear()
        self.Messages = None

    def isValidForCBFETReporting(self, moneyFlow):
        validForReporting = False
        if moneyFlow.Trade().Status() == 'Terminated' and moneyFlow.Type() != 'Termination Fee':
            return validForReporting
        
        projectedAmount = float(Detail.format_Projected_Money_Flow(moneyFlow, 'Cash Analysis Projected'))
        moneyFlowCurrency = moneyFlow.Currency().Name()
        
        if  abs(projectedAmount) > 0.01:
            if moneyFlowCurrency != 'ZAR':
                validForReporting = True

            elif moneyFlowCurrency == 'ZAR' \
            and moneyFlow.Acquirer().Name() in ('IRD DESK', 'IRP_FX Desk', 'NLD DESK') and moneyFlow.Instrument().InsType() in ('CurrSwap', 'Swap', 'Option', 'FRA') \
            and moneyFlow.Counterparty().Name() in ('BARCLAYS BANK PLC', 'BARCLAYS BANK PLC LONDON', 'CREDIT AGRICOLE CIB PARIS', 'SOCIETE GENERALE PARIS'):
                validForReporting = False

            else:
                if isForeignClient(moneyFlow.Counterparty()) and (moneyFlow.Trade().Counterparty().BusinessStatus() and moneyFlow.Trade().Counterparty().BusinessStatus().Name() == 'Interbank'):
                    validForReporting = True
                        
        return validForReporting

    def remove_Trades_Busienss_Rules(self, tradeList):
        validTrades = acm.FArray()
        objCalcSpace = acm.FCalculationSpaceCollection().GetSpace("FTradeSheet", acm.GetDefaultContext())

        for trade in tradeList:
            tradeObj = acm.FTrade[trade]
            instrument = tradeObj.Instrument()

            #Inward Listings    
            if instrument.ExternalId2().__contains__('Inward Listed'):
                continue

            #Mirror Trade
            elif tradeObj.MirrorTrade() and (tradeObj.Oid() <> tradeObj.MirrorTrade().Oid()):
                continue
                
            #FX trades Restrictions - Restrict trades marked with a "true" MidasSettlement indicator
            elif tradeObj.MidasSettlement():
                continue

            #FX Restrictions - Report only African and Precious Metals Currencies
            elif instrument.InsType() == 'Curr' and objCalcSpace.CalculateValue(tradeObj, 'fxSubType') != 'Cash Payment' \
                and (not (instrument.Currency().Name() in Params.AFRICAN_CURRENCIES or instrument.Currency().Name() in Params.PRECIOUS_METALS_CURRENCIES \
                    or tradeObj.Currency().Name() in Params.AFRICAN_CURRENCIES or tradeObj.Currency().Name() in Params.PRECIOUS_METALS_CURRENCIES)):
                continue
                
            #Restrict instruments with ISIN containing GB
            elif instrument.Isin().__contains__('GB') or (instrument.Underlying() and instrument.Underlying().Isin().__contains__('GB')):
                continue
                
            #Restrict moneyflows with ISIN containing GB and the specified moneyflow types
            elif instrument.Isin().__contains__('GB') or (instrument.Underlying() and instrument.Underlying().Isin().__contains__('GB')):
                for mf in self.get_MoneyFlows_From_Trade(trade):
                    if mf.Type() in ('Dividend', 'Dividend Transfer') and mf.Currency().Name()=='ZAR' \
                    and instrument.InsType() in ('Stock', 'CFD', 'EquityIndex', 'Security Loan'):
                        continue
                        
            #Restrict combination instruments with ISIN containing GB            
            elif instrument.InstrumentMaps():
                for comb in  instrument.InstrumentMaps():
                    if comb.Instrument().Isin().__contains__('GB') or (comb.Instrument().Underlying() and comb.Instrument().Underlying().Isin().__contains__('GB')):
                        continue
                
            #Isin ZAG restriction
            elif instrument.Isin().__contains__('ZAG') or (instrument.Underlying() and instrument.Underlying().Isin().__contains__('ZAG')):
                continue

            #Restrict if Acquirer = EQ Derivatives Desk and Trader = OBP_USER_PRD, then exclude as valid moneyflow. (DO NOT FEED ODP). MINT-956
            elif (tradeObj.Trader() and tradeObj.Trader().Name() == 'OBP_USER_PRD') and (tradeObj.Acquirer() and tradeObj.Acquirer().Name() == 'EQ Derivatives Desk'):
                continue
                
            #ABITFA-5211 - Exclude Portfolio Swaps from being sent for BoP Reporting
            elif instrument.InsType() == 'Portfolio Swap':
                continue

            #Restrict trades where portfolios are LCH and acquirer is IRD Desk
            elif tradeObj.Portfolio().Name() in Params.LCH_PORTFOLIOS:
                continue

            #AMD-315 Prime Services Elimination
            elif (tradeObj.Acquirer() and tradeObj.Acquirer().Name() == 'PRIME SERVICES DESK') and (tradeObj.Trader() and tradeObj.Trader().Name() == 'ATS'):
                if (tradeObj.Portfolio() and tradeObj.Portfolio().Name() == 'PB_GPP_PRINCIPAL') and (instrument.InsType() == 'Stock' or instrument.InsType() == 'Curr'):
                    continue
                elif (tradeObj.Portfolio() and tradeObj.Portfolio().Name() == 'PB_SAXO_PRINCIPAL') and instrument.InsType() == 'Stock' :
                    continue
            
            #AMD-355 Removing Funding Desk Acquirer Trades
            elif (tradeObj.Acquirer() and tradeObj.Acquirer().Name() == 'Funding Desk'):
                continue

            else:
                validTrades.Add(trade)
            
        return validTrades
    
    def get_Valid_Trades(self):
        if self.Scope_Objects:
            initialTradeSelection =  [t.Oid() for t in self.Scope_Objects if \
                    (t.Status() in ('BO Confirmed', 'BO-BO Confirmed', 'Terminated', 'FO Confirmed')) \
                and (t.Instrument().ExpiryDate() >= self.START_DATE or t.ValueDay() >= self.START_DATE) \
                and t.add_info('MIDAS_MSG') != 'Sent'
                ]

            return self.remove_Trades_Busienss_Rules(initialTradeSelection)
        else:
            return []
        
    def get_MoneyFlows_From_Trade(self, trade):
        trade = acm.FTrade[trade]
        return [m for m in trade.MoneyFlows(self.MONEY_FLOW_DATE, self.TODAY) if \
            self.isValidForCBFETReporting(m) == True\
            and m.Counterparty() and (m.Counterparty().Type() != 'Intern Dept') and (trade.Counterparty().Name() not in Params.PREVENT_COUNTERPARTY) \
            and ael.date(m.PayDate()) == self.TODAY \
            and m.Currency().Name() in Params.VALID_CURRENCIES
            and m.Type() not in Params.MONEYFLOW_TYPE_EXCLUSION
            and CallFixedRateAdjustableTest(None, m, self.TODAY) == True
            ]

    def createMessage(self, moneyFlow):
        '''--------------------------------------------------------------------------
                                    Getting Message Detail
        --------------------------------------------------------------------------'''    
        messageDetail = Detail.Message_Detail(moneyFlow)
        self.MessageCounter = self.MessageCounter + 1
        messageDetail.Message_Detail.insert(0, get_Message_Info('MONEY_FLOW', self.AMBA_Data_Struct.AMBA_Request_Id, str(self.MessageCounter), ''))
            
        self.Messages.Add(construct_AMBA_Message(messageDetail.Message_Detail))

    def is_Valid_Portfolio(self, portfolio):
        if portfolio.Name() == 'ACS RTM - 41012':
            return False
        elif not portfolio.Compound():
            return True
        else:
            raise Exception('Portfolio %s is a Compound Portfolio.' %portfolio.Name())
    
    def get_Single_Trade_Objects(self):
        trade = None
        if self.AMBA_Data_Struct.AMBA_Scope_Name:
            try:
                trade = [acm.FTrade.Select01('name = %s' %self.AMBA_Data_Struct.AMBA_Scope_Name, None)]
            except:
                raise Exception('Trade %s does not exist in Front Arena.' %self.AMBA_Data_Struct.AMBA_Scope_Name)
        
        if trade:
            self.Scope_Objects = trade
    
    def get_Instrument_Trade_Objects(self):
        instrument = None
        if self.AMBA_Data_Struct.AMBA_Scope_Name:
            try:
                instrument = acm.FInstrument.Select01('name = %s' %self.AMBA_Data_Struct.AMBA_Scope_Name, None)
            except:
                raise Exception('Instrument with insid %s does not exist in Front Arena.' %self.AMBA_Data_Struct.AMBA_Scope_Name)
        
        if instrument:
            self.Scope_Objects = instrument.Trades()
    
    def get_Portfolio_Trade_Objects(self):
        portfolio = None
        if self.AMBA_Data_Struct.AMBA_Scope_Name:
            try:
                portfolio = acm.FPhysicalPortfolio.Select01('name = %s' %self.AMBA_Data_Struct.AMBA_Scope_Name, None )
            except:
                raise Exception('Portfolio with name %s does not exist in Front Arena.' %self.AMBA_Data_Struct.AMBA_Scope_Name)
        
        if portfolio and self.is_Valid_Portfolio(portfolio):
            self.Scope_Objects = portfolio.Trades()
    
    def get_Scope_Objects(self):
        if self.AMBA_Data_Struct.AMBA_Request_Type == 'SINGLE_TRADE':
            self.get_Single_Trade_Objects()
        elif self.AMBA_Data_Struct.AMBA_Request_Type == 'INSTRUMENT_TRADES':
            self.get_Instrument_Trade_Objects()
        elif self.AMBA_Data_Struct.AMBA_Request_Type == 'PORTFOLIO_TRADES':
            self.get_Portfolio_Trade_Objects()
        else:
            raise Exception('Received an unsupported Request Type. %s' %self.AMBA_Data_Struct.AMBA_Request_Type)
    
    def select_And_Create_Msgs(self):
        valid_trades = self.get_Valid_Trades()
        for t in valid_trades:
            for mf in self.get_MoneyFlows_From_Trade(t):
                self.createMessage(mf)
        valid_trades = None

        self.Control_Message = construct_AMBA_Message([get_Message_Info('CONTROL', self.AMBA_Data_Struct.AMBA_Request_Id, '0', '')])

class Message_Info_MESSAGE():
    def __init__(self, MESSAGE_TYPE, REQUEST_ID, ERROR_MESSAGE, COMMAND_NAME = '', COMMAND_PARAMETER = ''):
        self.MESSAGE_TYPE = MESSAGE_TYPE
        self.REQUEST_ID = REQUEST_ID
        self.ERROR_MESSAGE = ERROR_MESSAGE
        self.AMBA_Error_Message = None
        self.COMMAND_NAME = COMMAND_NAME
        self.COMMAND_PARAMETER = COMMAND_PARAMETER
        self.create_Message_Info_MESSAGE()
    
    def create_Message_Info_MESSAGE(self):
        self.AMBA_Error_Message = construct_AMBA_Message([get_Message_Info(self.MESSAGE_TYPE, self.REQUEST_ID, '1', self.ERROR_MESSAGE, self.COMMAND_NAME, self.COMMAND_PARAMETER)])

