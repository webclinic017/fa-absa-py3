'''-----------------------------------------------------------------------
MODULE
    SL_Collateral_Exposure

DESCRIPTION
    AIRB Project Implementation (which is Regulatory Reporting Requirement)
    
    Date                : 2010-08-10
    Purpose             : AIRB project for collateral management
    Department and Desk : CTB BUS INFRASTRUCTURE
    Requester           : Jan Ehlers 
    Developer           : Anwar Banoo & Ickin Vural
    CR Number           : C000000392741,C000000428517,C000000454782

ENDDESCRIPTION
-----------------------------------------------------------------------'''
import acm, ael


def _get_party_list():
    party_list = acm.FCounterParty.Select('').AsSet()
    party_list.Union(acm.FClient.Select(''))


today = ael.date_today()
ael_variables = [ ['CFDFilter', 'Select Filter_ cfd', 'string', None, 'SL_Collateral', 1],
                  ['Date', 'Date_ cfd', 'string', None, 'Today', 1],
                  ['Portfolio', 'Select Portfolio_ cfd', 'string', acm.FPhysicalPortfolio.Select(''), None, 0, 1],
                  ['CounterParty', 'Select CounterParty_ cfd', 'string', _get_party_list(), None, 0, 1],
                  ['SLFilter', 'Select Filter_ sl feed', 'string', None, 'SL_CollateralAndLoan_AddedPtf', 1],
                  ['Filename', 'File Name_ output', 'string', None, 'Stockbroker_Exposure', 1],
                  ['Filepath', 'File Path_ output', 'string', None, 'F:\\', 1]]

def _produceSLFeed(filter, fileName):

    #SL Feed Constants
    GROUPER_NAME = ['Trade CounterParty / SL Instype']
    SHEET_TYPE = 'FPortfolioSheet'
    PARTYLEVEL = 'Counterparty Party Level'
    COLLATERALLEVEL = 'Collateral Type Party Level'
    LOANVALUE = 'Loan Value'
    TOTALCOLLATERAL = 'Total Collateral Value'


    tradeFilter = acm.FTradeSelection[filter]
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(context, SHEET_TYPE)

    def getColumn(node, column_name):
        return calc_space.CalculateValue(node, column_name)

    def createSheet():
        top_node = calc_space.InsertItem(tradeFilter)
        top_node.ApplyGrouper(acm.Risk().GetGrouperFromName(GROUPER_NAME))
        calc_space.Refresh()


    outfile = open(fileName, 'a')
                   
    createSheet()
    
    tradeFilterIterator = calc_space.RowTreeIterator().FirstChild()
    child_iter = tradeFilterIterator.FirstChild()

    count = 0
    outputDate = ael.date_from_string(acm.Time().DateToday()).to_string('%Y%m%d')

    while child_iter:
        item = child_iter.Tree().Iterator().FirstChild()
        while item:
            expDay = acm.Time().SmallDate()
            startDay = acm.Time().BigDate()
            tradeNumber = None
            traderID = None
            valueDay = None
            
            for trade in item.Tree().Item().Trades().AsArray():
                if trade.Instrument().ExpiryDate() > expDay:
                    expDay = trade.Instrument().ExpiryDateOnly()
                    
                if trade.Instrument().StartDate() < startDay:
                    startDay = trade.Instrument().StartDate()
                    valueDay = trade.ValueDay()
                    tradeNumber = trade.Oid()
                    traderID = trade.TraderId()

            
            partyLevel = getColumn(item.Tree(), PARTYLEVEL)
            collateralLevel = getColumn(item.Tree(), COLLATERALLEVEL)
            
            try:
                loanValue = round(getColumn(item.Tree(), LOANVALUE).Number(), 2)
            except:
                loanValue = 0
            
            try:
                totalCollateral = round(getColumn(item.Tree(), TOTALCOLLATERAL).Number(), 2)
            except:
                totalCollateral = 0
                
            if collateralLevel == 'SecurityLoan':
                collateralLevel = 'Loan Value'
                
            if collateralLevel == 'Loan Value':
                if partyLevel != 'ABSA SECURITIES LENDING':
                    loanValue = -1 * loanValue
            else:
                loanValue = abs(totalCollateral)
                
            if collateralLevel == 'Loan Value':
                totalCollateral = loanValue * 1.05
            else:
                totalCollateral = loanValue
                
            party = acm.FParty[partyLevel]
            partySDS = party.add_info('BarCap_SMS_CP_SDSID')
            
            try:
                _ExpDay = ael.date_from_string(expDay).to_string('%Y%m%d')
            except:
                _ExpDay = expDay
            
            try:
                _StartDay = ael.date_from_string(startDay).to_string('%Y%m%d')
            except:
                _StartDay = startDay
                
            try:
                _ValueDay = ael.date_from_string(valueDay).to_string('%Y%m%d')
            except:
                _ValueDay = valueDay
                    
            outfile.write('AS,ZAR,%s,%s,%s,%s,Absa Capital,%s,%s,%s,null,%s,%s,%s,null,null,null,null,null,null,Senior,Post Acceptance,Financial Bond,Absa Capital Securities (Pty) Ltd,%s\n' 
                          %(_ExpDay, str(partySDS), loanValue, collateralLevel, outputDate, _StartDay, tradeNumber, _ValueDay, traderID, tradeNumber, totalCollateral))

            item = item.NextSibling()        
        
        child_iter = child_iter.NextSibling()

    outfile.close()  


def _produceCFDFeed(cpty, port, prevDay, date, tradeFilter, fileName):

    #CFD Constants      
    DRAWN_AMOUNT = 0            
    MARGIN_AMOUNT = 1
    EXPIRY = 2
    START = 3
    VALUE = 4
    TRADE_NO = 5
    TRADER_ID = 6

    Amt = 0
    temp_dict = acm.FDictionary()    
    total_temp = acm.FDictionary()
    filteredTrades = acm.FTradeSelection[tradeFilter]
    prevDay = date.add_banking_day(ael.Instrument['ZAR'], -1)
    acmYesterday = acm.Time().AsDate(prevDay)
    acmToday = acm.Time().AsDate(date)

    if port:
        for portfolio in port:    
            Portfolio = acm.FPhysicalPortfolio[portfolio]        
            for trade in Portfolio.Trades():
                if trade.Instrument().InsType() in ('Stock', 'Bond') and trade.TradeCategory() != 'Collateral' and trade.Status() not in ('Void', 'Simulated'):
                    if (trade.ValueDay() <= acmToday):
                        if ((trade.Counterparty().Name() in cpty) or (trade.Counterparty().ParentOrSelf().Name() in cpty)):
            
                            TradeNbr     =  trade.Name()
                            Instrument   =  trade.Instrument().Name()
                            CounterParty =  trade.Counterparty().Name()
                            Parent_Party =  trade.Counterparty().ParentOrSelf().Name()
                            Type = 'Loan value'
                            
                            if trade.ValueDay() <= acmYesterday :
                            
                                if trade.Instrument().InsType() == 'Stock':                            
                                    Amt = ((trade.Quantity() * trade.Instrument().ContractSize())*(trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0))/100)
                                else:
                                    #to implement to bond code here properly!!!
                                    Amt = ((trade.Quantity() * trade.Instrument().ContractSize())*(trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0))/100)
                                
                            else:
                                Amt = 0
                                
                            
                            temp_dict  = [Parent_Party, CounterParty, Type]

                            if total_temp.HasKey(temp_dict):
                                try:
                                    total_temp[temp_dict][DRAWN_AMOUNT] += Amt 
                                    if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                        total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                                    if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                        total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                        total_temp[temp_dict][VALUE] = trade.ValueDay()
                                        total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                        total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                                except:
                                    pass
                                    
                            else:
                                try:
                                    total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                                except:
                                    pass
                                    
        for key in total_temp.Keys():
            total_temp[key][DRAWN_AMOUNT] = (abs(total_temp[key][DRAWN_AMOUNT])* -1)     
                
        for portfolio in port:
            Portfolio = acm.FPhysicalPortfolio[portfolio]
            for trade in Portfolio.Trades():
                if (trade.Counterparty().Name() in cpty and trade.Instrument().InsType() == 'Deposit' and trade.Status() not in ('Void', 'Simulated')) or (trade.Counterparty().ParentOrSelf().Name() in cpty and trade.Instrument().InsType() == 'Deposit' and trade.Status() not in ('Void', 'Simulated')):
                    TradeNbr     =  trade.Name()
                    Instrument   =  trade.Instrument().Name()
                    CounterParty =  trade.Counterparty().Name()
                    Parent_Party =  trade.Counterparty().ParentOrSelf().Name() 
                        
                    if trade.Instrument().InsType() == 'Deposit':
                        if trade.Instrument().OpenEnd() == 'None':
                            
                            if trade.Instrument().ExpiryDateOnly() > acmToday:
                                Amt = abs(trade.Premium())
                                Type = 'Fixed cash'
                            else:
                                Amt  = 0
                                Type = 'Fixed cash'
                    
                            temp_dict  = [Parent_Party, CounterParty, Type]
                            if total_temp.HasKey(temp_dict):
                                try:
                                    total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                                    if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                        total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                                    if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                        total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                        total_temp[temp_dict][VALUE] = trade.ValueDay()
                                        total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                        total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                                except:
                                    pass
                                    
                    else:
                        try:
                            total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                        except:
                            pass
                    
        
        ins = acm.FDeposit.Select('openEnd = 1') 

        for instruments in ins:        
            for trade in instruments.Trades():            
                if trade.Status() not in ('Void', 'Simulated'):       
                    if (trade.Counterparty().Name() in cpty) or (trade.Counterparty().ParentOrSelf().Name() in cpty) :                    
                        Amt = 0            
                        for l in trade.Instrument().Legs():
                            for cf in l.CashFlows():
                                if cf.PayDate() <= acmToday:
                                    
                                    TradeNbr     =  trade.Name()
                                    Instrument   =  trade.Instrument().Name()
                                    CounterParty =  trade.Counterparty().Name()
                                    Parent_Party =  trade.Counterparty().ParentOrSelf().Name()
                                    
                                    Amt  += (cf.FixedAmount())
                                    Type = 'Call cash'
                                    Cflow = cf.Oid()
                            
                        temp_dict  = [Parent_Party, CounterParty, Type]

                        if total_temp.HasKey(temp_dict):
                            try:
                                total_temp[temp_dict][DRAWN_AMOUNT] += abs(Amt)
                                if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                    total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                                if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                    total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                    total_temp[temp_dict][VALUE] = trade.ValueDay()
                                    total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                    total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                            except:
                                pass
                                
                        else:
                            try:
                                total_temp[temp_dict] = (abs(Amt), 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                            except:
                                pass
    
    for trade in filteredTrades.Trades():        
        TradeNbr     =  trade.Name()
        Instrument   =  trade.Instrument().Name()
        CounterParty =  trade.Counterparty().Name()
        Parent_Party =  trade.Counterparty().ParentOrSelf().Name()
        
        if trade.Instrument().InsType() == 'Bill':
            Type = trade.AdditionalInfo().MM_Instype()
        else:
            Type =  trade.Instrument().InsType()
        
        temp_dict  = [Parent_Party, CounterParty, Type]
        
        if trade.Instrument().InsType() == 'Stock':
            if trade.ValueDay() <= acmYesterday:
                if trade.Instrument().QuoteType() == 'Per 100 Units':
                    Amt = (trade.Quantity() * trade.Instrument().ContractSize())*(trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0)/100)
                    Amt = abs(Amt)
                    
                    if trade.Quantity() < 0:
                        Amt = -1.0 * Amt
                    else:
                        pass
                else:
                    Amt = (trade.Quantity() * trade.Instrument().ContractSize())*(trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0))
                    Amt = abs(Amt)
                    
                    if trade.Quantity() < 0:
                        Amt = -1.0 * Amt
                    else:
                        pass
            
            if total_temp.HasKey(temp_dict):
                try:
                    total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                    if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                        total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                    if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                        total_temp[temp_dict][START] = trade.Instrument().StartDate()
                        total_temp[temp_dict][VALUE] = trade.ValueDay()
                        total_temp[temp_dict][TRADE_NO] = trade.Oid()
                        total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                except:
                    pass
                    
            else:
                try:
                    total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                except:
                    pass
        else:
            
            if trade.Instrument().ExpiryDateOnly() >= acmToday: 
                if trade.Instrument().InsType() == 'Bill':
                    if trade.Instrument().QuoteType() == 'Per 100 Units':
                        Amt = (trade.Quantity() * trade.Instrument().NominalAmount()) / 100
                    else:
                        Amt = trade.Quantity() * trade.Instrument().NominalAmount()

                    if total_temp.HasKey(temp_dict):
                        try:
                            total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                            if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                            if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                total_temp[temp_dict][VALUE] = trade.ValueDay()
                                total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                        except:
                            pass
                            
                    else:
                        try:
                            total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                        except:
                            pass
                else:
                    if trade.Instrument().InsType() == 'FRN':
                        if trade.Instrument().QuoteType() == 'Per 100 Units':
                            Amt = (trade.Quantity() * trade.Instrument().NominalAmount()) / 100
                        else:
                            Amt = trade.Quantity() * trade.Instrument().NominalAmount()
                        
                        if total_temp.HasKey(temp_dict):
                            try:
                                total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                                if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                    total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                                if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                    total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                    total_temp[temp_dict][VALUE] = trade.ValueDay()
                                    total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                    total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                            except:
                                pass
                                
                        else:
                            try:
                                total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                            except:
                                pass
                    else:
                        if trade.Instrument().QuoteType() == 'Per 100 Units':
                            Amt = (trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0)/100)
                        else:
                            Amt = trade.Instrument().MtMPrice(prevDay, trade.Instrument().Currency(), 0)
                            
                        if total_temp.HasKey(temp_dict):
                            try:
                                total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                                if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                                    total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                                if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                                    total_temp[temp_dict][START] = trade.Instrument().StartDate()
                                    total_temp[temp_dict][VALUE] = trade.ValueDay()
                                    total_temp[temp_dict][TRADE_NO] = trade.Oid()
                                    total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                            except:
                                pass
                        else:
                            try:
                                total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                            except:
                                pass    
            else:
                Amt = 0
                
                if total_temp.HasKey(temp_dict):
                    try:
                        total_temp[temp_dict][DRAWN_AMOUNT] += Amt
                        if trade.Instrument().ExpiryDate() > total_temp[temp_dict][EXPIRY]:
                            total_temp[temp_dict][EXPIRY] = trade.Instrument().ExpiryDateOnly()
                        if trade.Instrument().StartDate() < total_temp[temp_dict][START]:
                            total_temp[temp_dict][START] = trade.Instrument().StartDate()
                            total_temp[temp_dict][VALUE] = trade.ValueDay()
                            total_temp[temp_dict][TRADE_NO] = trade.Oid()
                            total_temp[temp_dict][TRADER_ID] = trade.TraderId()
                    except:
                        pass
                else:
                    try:
                        total_temp[temp_dict] = (Amt, 0, trade.Instrument().ExpiryDateOnly(), trade.Instrument().StartDate(), trade.ValueDay(), trade.Oid(), trade.TraderId())
                    except:
                        pass
                
    temp_dict  = [Parent_Party, CounterParty, Type]
    
    counterparty_list1 = []
    multiparty_list1   = []
    
    for key in total_temp.Keys():
        if (key[2] not in ('Loan value')) and (total_temp[key][DRAWN_AMOUNT] > 0):
            if key[1] not in counterparty_list1:
                counterparty_list1.append(key[1])
            else:
                if key[1] not in multiparty_list1:
                    multiparty_list1.append(key[1])
                else:
                    pass
    
    counterparty_list2 = []
    multiparty_list2   = []               
                    
    for key in total_temp.Keys():
        if (key[2] in ('Call cash', 'Fixed cash')) and (total_temp[key][DRAWN_AMOUNT] > 0):
            if key[1] not in counterparty_list2:
                counterparty_list2.append(key[1])
            else:
                if key[1] not in multiparty_list2:
                    multiparty_list2.append(key[1])
                else:
                    pass
                    
    multiparty_list   = []
    
    for item in multiparty_list1:
        if item not in multiparty_list2:
            multiparty_list.append(item)
    
    for key in total_temp.Keys(): 
        if key[2]  == 'Loan value':
            total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT]  * 1.05)
        if key[2]  == 'Fixed cash':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.05)
        if key[2]  == 'Call cash':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.05)
        if key[2]  == 'Bond':
            total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT] 
        if key[2]  == 'NCD':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.10)
        if key[2]  == 'NCC':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.10)
        if key[2]  == 'FRN':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.10)
        if key[2]  == 'Stock':
            if key[1] not in multiparty_list:
                total_temp[key][MARGIN_AMOUNT] = total_temp[key][DRAWN_AMOUNT]
            else:
                total_temp[key][MARGIN_AMOUNT] = (total_temp[key][DRAWN_AMOUNT] / 1.15)
        else:
            pass
    
    outfile = open(fileName, 'a')
    outputDate = ael.date_from_string(acm.Time().DateToday()).to_string('%Y%m%d')
    
    for i in range(0, total_temp.Size()):
        key = total_temp.Keys()[i]
        value = total_temp.Values()[i]
        
        Parent_Party = key[0]
        CounterParty = key[1]
        Type         = key[2]
        Margin_Amt   = value[MARGIN_AMOUNT]
        Amt          = value[DRAWN_AMOUNT]
        try:
            Expiry       = ael.date_from_string(value[EXPIRY]).to_string('%Y%m%d')
        except:
            Expiry       = value[EXPIRY]
            
        try:
            Start        = ael.date_from_string(value[START]).to_string('%Y%m%d')
        except:
            Start        = value[START]
        
        try:
            Value        = ael.date_from_string(value[VALUE]).to_string('%Y%m%d')
        except:
            Value        = value[VALUE]
            
        Trade        = value[TRADE_NO]
        TraderId     = value[TRADER_ID]
        
        partySDS = acm.FParty[CounterParty].add_info('BarCap_SMS_CP_SDSID')
        if partySDS != 40041796: 
            outfile.write('AS,ZAR,%s,%s,%s,%s,Absa Capital,%s,%s,%s,null,%s,%s,%s,null,null,null,null,null,null,Senior,Post Acceptance,Financial Bond,Absa Capital Securities (Pty) Ltd,%s\n' 
                          %(Expiry, str(partySDS), Amt, Type, outputDate, Start, Trade, Value, TraderId, Trade, Margin_Amt))
            
    outfile.close()



def ael_main(parameter):    
    tradeFilter = parameter['CFDFilter']   
    inputDate = parameter['Date']
    if inputDate == 'Today':
        date = ael.date_today()
    else:
        date = ael.date_from_string(inputDate, '%Y-%m-%d')
        
    prevDay = date.add_banking_day(ael.Instrument['ZAR'], -1)
    port = parameter['Portfolio']
    cpty = parameter['CounterParty']
    outputName = parameter['Filename']
    outputPath = parameter['Filepath']
    
    slTradeFilter = parameter['SLFilter']    
    
    
    fileName = outputPath + '/' + outputName + '.csv'
    

    outfile = open(fileName, 'w')
    outfile.write('DATA_ID,CCY_EXPOSURE,CONTRACTUAL_MATURITY_DATE,SDS_ID,DRAWN_AMOUNT,PRODUCT_NAME,RECOURSE_SBU_NAME,DATE_CAPTURED,START_DATE,' + \
                   'ACCOUNT_NUMBER,ABCAP_STRUCTURE,REVIEW_DATE,USER_ID,SYSTEM_ID,LDP_SP,GOV_STRUCT_FUNC,FIN_STM_TYPE,ES_GG_COVER_ID_IND,' + \
                   'COLLECTION_LEVEL,CITY_EXTERNAL_RATING,SENIORITY,LETTER_OF_CREDIT_TYPE,BGI_TYPE,RESPCNTRID,COLLATERAL_VALUE\n')
    outfile.close()
    
    _produceSLFeed(slTradeFilter, fileName)
    _produceCFDFeed(cpty, port, prevDay, date, tradeFilter, fileName)    
    print 'Output Complete'
    print 'Wrote secondary output to::: ' + fileName
