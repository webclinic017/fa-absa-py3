"""
Purpose                 :Market Risk feed files,[Fixed the rolling period]
Department and Desk     :IT,Market Risk
Requester:              :Natalie Austin,Susan Kruger
Developer               :Douglas Finkel, Tshepo Mabena
CR Number               :264536,290307,275268,627760, 632872, 701575,[824244 - 919,952,1037,1054]

Description
Portfolios are referenced via a Trade Filter - MR_Portfolios
Remove special character backtick (`) from the instrument name
Added IndexType function
Added ASQL functions specifically for MR_EQOptions_American
Added support for extra rolling periods (Lukas Paluzga, C590239, 2012-11-08)
Fix a change in FInstrument.MappedDiscountLink API (Peter Basista, FA-Upgrade-2014, 2015-02-11)

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2015-11-25                                         Brendan Bosman     MINT 412, MINT 416, MINT 417
2016-02-23     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-483
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
2020-10-23     CHG0134281	    Anji Mandepudi	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-856
"""

import ael, string, acm
global excludedPortfolioList
excludedPortfolioList = []
EXCLUDED_PORTFOLIOSQUERYFOLDER_NAME = 'MR_RiskWatch_ExcludedPortfolios'
QUERYFOLDER = acm.FStoredASQLQuery.Select01('name = %s' %EXCLUDED_PORTFOLIOSQUERYFOLDER_NAME, '')

class CalcSpace( object ):
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def AppendOptionType(Instrument):
    if Instrument.IsCallOption():
        return '_C'
    return '_P'

def Datefix(d, *rest):
    if d == None:
        return ''
    else:
        return ael.date_from_string(d).to_string('%Y/%m/%d')

def DayCountFix(d, *rest):
    if d == 'Act/365':
        return 'actual/365'
    if d == 'Act/ActISMA':
        return 'actual/actual'
    if d == 'Act/ActAFB':
        return 'actual/actual French'
    if d == 'Act/360':
        return 'actual/360'
    if d == 'Act/364':
        return 'actual/364'
    if d == '30E/360':
        return '30/360 European'
    if d == '30E/365':
        return '30/360 European'
    if d == '30/365':
        return '30/360'
    if d == '30/360SIA':
        return '30/360'
    if d == 'Act/ActISDA':
        return 'actual/actual'
    if d == '30/360':
        return '30/360'
    if d == 'Act/365L':
        return 'actual/365'
    if d == 'Bus/252':
        return 'business/252'
    if d == 'NL/365':
        return 'actual/365' 
    else:
        return 'undefined'

def DayCountFixNotionalIndex(d, *rest):
    if d == 'Act/365':
        return 'actual/365'
    if d == 'Act/ActISMA':
        return 'actual/actual'
    if d == 'Act/ActAFB':
        return 'actual/actual French'
    if d == 'Act/360':
        return 'actual/360'
    if d == 'Act/364':
        return 'actual/364'
    if d == '30E/360':
        return '30/360 European'
    if d == '30E/365':
        return '30/360 European'
    if d == '30/365':
        return '30/360'
    if d == '30/360SIA':
        return '30/360'
    if d == 'Act/ActISDA':
        return 'actual/actual'
    if d == '30/360':
        return '30/360'
    if d == 'NL/365':
        return 'actual/365' 
    else:
        return 'actual/365'

def NameFix(ins, *rest):
    modname = string.replace(ins, ',', '_')
    modname = string.replace(modname, '#', '_')
    modname = string.replace(modname, "'", '')
    modname = string.replace(modname, '_ Currency = ZAR', '')
    modname = string.replace(modname, '[Rel Spot]', '')
    modname = string.replace(modname, '^', '')
    modname = string.replace(modname, '*', '')
    modname = string.replace(modname, '|', '')
    modname = string.replace(modname, '`', '')
    return modname

def Rolling_NameFix(ins, *rest):
    modname = string.replace(ins, 'm', '')
    modname = string.replace(modname, 'd', '')
    modname = string.replace(modname, 'w', '')
    modname = string.replace(modname, 'Y', '')
    modname = string.replace(modname, 'y', '')
    return modname

def TrueFalse(tf, *rest):
    if tf == 1:
        return 'True'
    if tf == 0:
        return 'False'
    else:
        return tf

portfolioTree = acm.FList()
MR_Portfolio = acm.FList()
keepLooking = True

def getMMYC(i, *rest):
    instrument = acm.FInstrument[i.insid]
    '''
    global calcSpace
    global collectLimit
    global collect
    '''
    calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    component = instrument.Calculation().MoneyMarketYieldCurveComponents(calcSpace)
    if component:
        if component.IsKindOf('FYieldCurve'):
            return component.Name()
        if component.IsKindOf('FArray') and component.Size() > 0:
            for c in component:
                if c.Currency().Name() == instrument.Currency().Name():
                    return c.Name()
    return ''
    
def PortfolioSearch():
    queryFolderList = acm.FTradeSelection['MR_Portfolios']
    for i in queryFolderList.FilterCondition():
        if i[4] not in MR_Portfolio:
            MR_Portfolio.Add(i[4])

def get_port_struc(port, portfolioTree):
    portfolioTree.Add(port.Name())
    for item in port.MemberLinks():
        ownerPort = item.OwnerPortfolio()
        if ownerPort:
            get_port_struc(ownerPort, portfolioTree)

def TradeValid(trades):
    ValidPortfolio = 0
    trade = acm.FTrade[trades]
    portfolioTree = acm.FList()
    get_port_struc(trade.Portfolio(), portfolioTree)
    for Portfolio in MR_Portfolio:
        if str(Portfolio) in portfolioTree:
            ValidPortfolio = 1
    return ValidPortfolio

def ValidTradeNo(trades, *rest):
    if len(MR_Portfolio) == 0:
        PortfolioSearch()
    if trades.status not in ('Void', 'Terminated', 'Simulated'):
        if TradeValid(trades.trdnbr) == 1:
            tv = 0
        else:
            tv = 1
    else:
        tv = 1
    return tv

def BusRule(d, *rest):
    if d == 'Mod. Following':
        return 'Following'
    if d == 'Following':
        return 'Following'
    if d == 'Mod. Preceding':
        return 'Preceding'
    if d == 'Preceding':
        return 'Preceding'

    if d == 'Annual Comp':
        return 'annual'
    if d == 'Quarterly':
        return 'quarter'
    if d == 'Continuous':
        return 'continuous'
    if d == 'Semi Annual':
        return 'semi-annual'
    if d == 'Monthly':
        return 'month'
    if d == 'Discount':
        return 'discount'
    else:
        return 'undefined'

def BusRuleFRB(d, *rest):
    if d == 'Mod. Following':
        return 'Following'
    if d == 'Following':
        return 'Following'
    if d == 'Mod. Preceding':
        return 'Preceding'
    if d == 'Preceding':
        return 'Preceding'

    if d == 'Annual Comp':
        return 'annual'
    if d == 'Quarterly':
        return 'quarter'
    if d == 'Continuous':
        return 'continuous'
    if d == 'Semi Annual':
        return 'semi-annual'
    if d == 'Monthly':
        return 'month'
    if d == 'Discount':
        return 'discount'
    else:
        return 'None'

def BusConv(d, *rest):
    if d == 'Mod. Following':
        return 'Modified'
    if d == 'Following':
        return 'Regular'
    if d == 'Mod. Preceding':
        return 'Modified'
    if d == 'Preceding':
        return 'Regular'
    else:
        return 'None'

def BusPerd(d, *rest):
    if d == 'Annual Comp':
        return 'annual'
    if d == 'Quarterly':
        return 'quarter'
    if d == 'Continuous':
        return 'continuous'
    if d == 'Semi Annual':
        return 'semi-annual'
    if d == 'Monthly':
        return 'month'
    if d == 'Discount':
        return 'discount'
    else:
        return 'undefined'


def CurveDays(d,*rest):
    if string.find(d, 'm') <> -1:
        modname = string.replace(d, 'm', '')
        days = (365.0/12.0)*float(modname)
        return int(days)

    if string.find(d, 'w') <> -1:
        modname = string.replace(d, 'w', '')
        days = 7 * float(modname)
        return round(days)

    if string.find(d, 'd') <> -1:
        modname = string.replace(d, 'd', '')
        days = modname
        return days

    if string.find(d, 'y') <> -1:
        modname = string.replace(d, 'y', '')
        days = 365*float(modname)
        return round(days)

    return 'Undefined'

def CurveUnits(d,*rest):
    if string.find(d, 'm') <> -1:
        return 'Months'

    if string.find(d, 'w') <> -1:
        return 'Weeks'

    if string.find(d, 'd') <> -1:
        return 'Days'

    if string.find(d, 'y') <> -1:
        return 'Years'

    return 'Undefined'

def VolSurfRel(ins):

    i = acm.FInstrument[ins.insid]

    relativeStrikePriceFromAbsolute = acm.GetFunction('relativeStrikePriceFromAbsolute', 4)

    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    ins_calc = i.Calculation()
    Rel_Spot = str(relativeStrikePriceFromAbsolute(ins_calc.UnderlyingPrice(cs), i.StrikePrice(), 2, False))
    return  NameFix(Rel_Spot)


def AddDatePeriod(currdate, d,*rest):
    if string.find(d, 'm') <> -1:
        modname = string.replace(d, 'm', '')
        return currdate.add_months(int(modname))

    if string.find(d, 'w') <> -1:
        modname = string.replace(d, 'w', '')
        days = 7 * float(modname)
        return currdate.add_days(int(days))

    if string.find(d, 'd') <> -1:
        modname = string.replace(d, 'd', '')
        return currdate.add_days(int(modname))

    if string.find(d, 'y') <> -1:
        modname = string.replace(d, 'y', '')
        return currdate.add_years(int(modname))

    return 'Undefined'

def DatePeriodUnit(rolling_period, mode = 0):
    """
    Converts dateperiod string to period unit.

    @type  mode: number
    @param mode: Output mode. Use 0 for nouns, 1 for adverbs.

    """


    # I have no idea why is there 0m or 0y considered as a year, but whatever... taken from previous script

    mapping = [
        (['1m'],                                                                  ['month', 'month']),
        (['90d', '91d', '92d', '3m'],                                                ['quarter', 'quarter']),
        (['126d', '180d', '181d', '182d', '183d', '184d', '6m'],                        ['semi-annual', 'semi-annual']),
        (['360d', '361d', '362d', '363d', '364d', '365d', '366d', '0m', '12m', '0y', '1y',], ['annual', 'annual']),
        (['6d'],                                                                  ['day', 'day']),
        (['0d', '1d'],                                                             ['simple', 'simple'])]

    for (keys, values) in mapping:
        if rolling_period in keys:
            return values[mode]

    return 'undefined'

def RollingPeriodFix(rolling_period):
    return DatePeriodUnit(rolling_period, 1)

def RollingPeriodFixISABonds(rolling_period):
    return DatePeriodUnit(rolling_period, 0)

def Seniority(entry):

    if entry=='Senior':
        return '6'
    if entry=='SenSec':
        return '5'
    elif entry=='SenSub':
        return '4'
    elif entry=='SenUn':
        return '3'
    elif entry=='Sub':
        return '2'
    elif entry=='Unsecured':
        return '1'
    else:
        return'0'

def IndexType(Type, Item):

    if Type == 'None':
        if Item == 'TermNB':
            return '0'
        elif Item == 'TermUNIT':
            return 'Months'

    if Type == 'CPI -3Months(30)':
        if Item == 'TermNB':
            return '3'
        elif Item == 'TermUNIT':
            return 'Months'

    elif Type == 'CPI -3Months':
        if Item == 'TermNB':
            return '3'
        elif Item == 'TermUNIT':
            return 'Months'

    elif Type == 'CPI -4Months':
        if Item== 'TermNB':
            return '4'
        elif Item== 'TermUNIT':
            return 'Months'

    elif Type == 'CPI JGB':
        if Item == 'TermNB':
            return '0'
        elif Item == 'TermUNIT':
            return 'Months'

    elif Type == 'CPI -3Months No Interpol':
        if Item == 'TermNB':
            return '3'
        elif Item == 'TermUNIT':
            return 'Months'

    elif Type == 'CPI -2Months No Interpol':
        if Item == 'TermNB':
            return '2'
        elif Item == 'TermUNIT':
            return 'Months'

'''
This is used on the MR ASQL files only
MR_Cash_Instrument
MR_EQOptions_American
'''

def ASQLNameFix(o, Item, *rest):
    if Item == 'icurrinsid':
        ins= o.curr.insid
        modname = string.replace(ins, ',', '_')
        modname = string.replace(modname, '#', '_')
        modname = string.replace(modname, "'", '')
        modname = string.replace(modname, '_ Currency = ZAR', '')
        modname = string.replace(modname, '[Rel Spot]', '')
        modname = string.replace(modname, '^', '')
        modname = string.replace(modname, '*', '')
        modname = string.replace(modname, '|', '')
        modname = string.replace(modname, '`', '')

    if Item == 'iinsid':
        ins= o.insid
        modname = string.replace(ins, ',', '_')
        modname = string.replace(modname, '#', '_')
        modname = string.replace(modname, "'", '')
        modname = string.replace(modname, '_ Currency = ZAR', '')
        modname = string.replace(modname, '[Rel Spot]', '')
        modname = string.replace(modname, '^', '')
        modname = string.replace(modname, '*', '')
        modname = string.replace(modname, '|', '')
        modname = string.replace(modname, '`', '')

    return modname

def ASQLStringConcat(o,Item,*rest):
    ResultString = ''

    if (Item == 'InsInsaddr'):
        ResultString = 'insaddr_' + str(o.insaddr)

    elif (Item == 'InsUndInsaddr'):
        ResultString = 'insaddr_' + str(o.und_insaddr.insaddr)

    elif (Item == 'InsCurrInsid'):
        ResultString = ASQLNameFix(o, 'icurrinsid') + str('_Cash')

    elif Item == 'TradeTrdnbr':
        ResultString = 'trdnbr_' + str(o.trdnbr)

    elif Item == 'TradePrfnbrPrfid':
        if o.prfnbr:
            ResultString   =       'prfid_' + str(o.prfnbr.prfid)
        else:
            ResultString   =       ''

    elif Item == 'TradeCounterparty_ptynbrPtyid':
        if o.counterparty_ptynbr:
            ResultString    =    str(o.counterparty_ptynbr.ptyid)
        else:
            ResultString       =       ''

    elif Item == 'TraderName':
        if o.owner_usrnbr:
            ResultString        =    str(o.owner_usrnbr.name)
        else:
            ResultString    =       ''

    return ResultString

def ASQLDatefix(o, *rest):
    d = o.exp_day
    if d == None:
        return ''
    else:
        return ael.date_from_string(d).to_string('%Y/%m/%d')

def ASQLMappedCurveLink(o,Item,*rest):

    ResultString = ''
    Instrument = acm.FInstrument[o.insid]

    if Item == 'MappedVolatilityLink':
        ResultString = Instrument.MappedVolatilityLink().LinkName()
        if ResultString == None:
            ResultString = 'None'
    elif Item == 'MappedDiscountLink':
        try:
            ResultString   =       Instrument.MappedDiscountLink(Instrument.Currency(), False, None).Link().YieldCurveComponent().Name()
        except:
            ResultString   =       Instrument.MappedDiscountLink(Instrument.Currency(), False, None).Link().YieldCurveComponent().Curve().Name()
    elif Item == 'MappedRepoLink':
        ResultString = Instrument.MappedRepoLink(Instrument.Currency()).Link().YieldCurveComponent().Curve().Name()

    return ResultString

def ASQLVolatility(o,*rest):

    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    Instrument = acm.FInstrument[o.insid]
    calc = Instrument.Calculation()
    ResultString = calc.Volatility(cs)

    return ResultString

def ASQLRounding(o,Item,*rest):

    if Item == 'TradeQuantity':
        ResultString = str(o.quantity)
    elif Item == 'StrikePriceDiv100':
        ResultString = str(o.strike_price/100)
    elif Item == 'StrikePrice':
        ResultString = str(o.strike_price)

    return ResultString

def CompoundConvention(spread, reset_type, rolling_period):
    """
    Converts dateperiod string to period unit.

    @type  mode: number
    @param mode: Output mode. Use 0 for nouns, 1 for adverbs.

    """

    # I have no idea why is there 0m or 0y considered as a year, but whatever... taken from previous script

    if spread!=0 and reset_type == 'Compound':
        ResultString = str('_' + DatePeriodUnit(rolling_period, 0))
    else:
        ResultString = ''

    return ResultString

def setExcludedPortfoliosList(queryFolder):
    global excludedPortfolioList
 
    #retreiving the ASQL nodes of the Portfolio criteria from the QueryFolder
    try:
        fASQLAttrNodes = queryFolder.Query().Decompose('Portfolio').Second().AsqlNodes()[0].AsqlNodes()
    except:
        fASQLAttrNodes = []
        
    for fASQLAttrNode in fASQLAttrNodes:
        if fASQLAttrNode.ClassName().Text() == 'FASQLAttrNode':
            excludedPortfolioList.append(fASQLAttrNode.AsqlValue().Text())

setExcludedPortfoliosList(QUERYFOLDER)

def isExcludedPortfolioFromPortfolio(temp, portfolio, *resr):
    global excludedPortfolioList
    
    portfolio = acm.FPhysicalPortfolio.Select01('oid = %i' %portfolio, '')
    if portfolio and portfolio.Name() in excludedPortfolioList:
        return True
    return False
    
def IsExcludedPortfolio(aelTrade, *rest):
    global excludedPortfolioList
    
    portfolio = aelTrade.prfnbr
    prfid = ''
    
    if portfolio:
        prfid = portfolio.prfid
    
    if prfid in excludedPortfolioList:
        return True
    else:
        return False
