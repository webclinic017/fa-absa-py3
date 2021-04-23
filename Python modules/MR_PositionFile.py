import ael, acm, string, MR_MainFunctions

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536,316586,287397,290307

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-03-08     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-528
'''


def NameFix(ins, *rest):
    modname = string.replace(ins, ',', '_')
    modname = string.replace(modname, '#', '_')
    modname = string.replace(modname, "'", '')
    modname = string.replace(modname, '_ Currency = ZAR', '')
    return modname

def CreatePosition(t, filename):
    
    outfile = open(filename, 'a')
    
    BASFLAG	        =	'BAS'
    HeaderName	        =	'Position'
    OBJECT	        =	'PositionSPEC'
    TYPE	        =	'Position'
    IDENTIFIER	        =	'trdnbr_'+str(t.trdnbr)
    PositionUnitsCAL	=	''
    PositionUnitsDAYC	=	''
    PositionUnitsFUNC	=	''
    PositionUnitsPERD	=	''
    PositionUnitsSTRG	=	''
    PositionUnitsUNIT	=	''
    PositionUnitsVAL	=	t.quantity
    
    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfid_'+str(t.prfnbr.prfid)
    else:
        PortfolioXREF   =       ''
        
    SettlmntAccntXREF	=	''
    SettlementProcFUNC	=	''

    if t.counterparty_ptynbr:
        CounterpartySTRG	=	t.counterparty_ptynbr.ptyid
    else:
        CounterpartySTRG   	=       ''
    
    if t.owner_usrnbr:
        TraderNAME	        =	t.owner_usrnbr.name
    else:
        TraderNAME		=       ''

    TradeAggregationNAME = IDENTIFIER

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, TradeAggregationNAME))
    outfile.close()
    
    return ''
    
    
def CreatePositionIRSwap(t, filename):
    
    outfile = open(filename, 'a')

    BASFLAG	        =	'BAS'
    HeaderName	        =	'Position'
    OBJECT	        =	'PositionSPEC'
    TYPE	        =	'Position'
    IDENTIFIER          =       ''
    
    if t.insaddr.instype in ('Cap', 'Floor'):
        for l in t.insaddr.legs():
            for cf in l.cash_flows():
                if cf.type not in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
                    IDENTIFIER = 'trdnbr_'+ str(t.trdnbr)+'_CFEdited'
                else:
                    IDENTIFIER = 'trdnbr_'+str(t.trdnbr)
    else:
        IDENTIFIER = 'trdnbr_'+str(t.trdnbr)
    
    PositionUnitsCAL	=	''
    PositionUnitsDAYC	=	''
    PositionUnitsFUNC	=	''
    PositionUnitsPERD	=	''
    PositionUnitsSTRG	=	''
    PositionUnitsUNIT	=	''
    PositionUnitsVAL	=	t.quantity
    
    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)
    
    if t.insaddr.instype in ('Cap', 'Floor'):
        for l in t.insaddr.legs():
            for cf in l.cash_flows():
                if cf.type not in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):
                    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)+ '_CFEdited'
                else:
                    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfid_'+str(t.prfnbr.prfid)
    else:
        PortfolioXREF   =       ''
        
    SettlmntAccntXREF	=	''
    SettlementProcFUNC	=	''

    if t.counterparty_ptynbr:
        CounterpartySTRG	=	t.counterparty_ptynbr.ptyid
    else:
        CounterpartySTRG   	=       ''
    
    if t.owner_usrnbr:
        TraderNAME	        =	t.owner_usrnbr.name
    else:
        TraderNAME		=       ''

    TradeAggregationNAME = 'trdnbr_'+str(t.trdnbr)

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, UserDefinedNAME4))
    outfile.close()

    return ''
    


def CreatePositionFX(t, filename):
    
    outfile = open(filename, 'a')
    
    BASFLAG	        =	'BAS'
    HeaderName	        =	'Position'
    OBJECT	        =	'PositionSPEC'
    TYPE	        =	'Position'
    IDENTIFIER	        =	'trdnbr_'+str(t.trdnbr)
    PositionUnitsCAL	=	''
    PositionUnitsDAYC	=	''
    PositionUnitsFUNC	=	''
    PositionUnitsPERD	=	''
    PositionUnitsSTRG	=	''
    PositionUnitsUNIT	=	''
    PositionUnitsVAL	=	t.quantity
    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)+'_'+str(t.trdnbr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfid_'+str(t.prfnbr.prfid)
    else:
        PortfolioXREF   =       ''
        
    SettlmntAccntXREF	=	''
    SettlementProcFUNC	=	''

    if t.counterparty_ptynbr:
        CounterpartySTRG	=	t.counterparty_ptynbr.ptyid
    else:
        CounterpartySTRG   	=       ''
    
    if t.owner_usrnbr:
        TraderNAME	        =	t.owner_usrnbr.name
    else:
        TraderNAME		=       ''

    UserDefinedNAME4 = IDENTIFIER

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, TradeAggregatioNAME))
    outfile.close()
    
    return ''
    
def CreatePositionFwds(t, filename):
    
    outfile = open(filename, 'a')
    
    BASFLAG	        =	'BAS'
    HeaderName	        =	'Position'
    OBJECT	        =	'PositionSPEC'
    TYPE	        =	'Position'
    IDENTIFIER	        =	'trdnbr_'+str(t.trdnbr)
    PositionUnitsCAL	=	''
    PositionUnitsDAYC	=	''
    PositionUnitsFUNC	=	''
    PositionUnitsPERD	=	''
    PositionUnitsSTRG	=	''
    PositionUnitsUNIT	=	''
    PositionUnitsVAL	=	t.quantity
    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)+'_'+str(t.trdnbr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfid_'+str(t.prfnbr.prfid)
    else:
        PortfolioXREF   =       ''
        
    SettlmntAccntXREF	=	''
    SettlementProcFUNC	=	''

    if t.counterparty_ptynbr:
        CounterpartySTRG	=	t.counterparty_ptynbr.ptyid
    else:
        CounterpartySTRG   	=       ''
    
    if t.owner_usrnbr:
        TraderNAME	        =	t.owner_usrnbr.name
    else:
        TraderNAME		=       ''

    UserDefinedNAME4 = IDENTIFIER

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, UserDefinedNAME4))
    outfile.close()
    
    return ''
    

def CreatePositionCash(p,FileDir,Filename,PositionName,*rest):

    filename = FileDir + PositionName
    outfile = open(filename, 'a')

    TradeCurrL = []
    for PortTrades in p.trades():
        if PortTrades.status not in ('Void', 'Simulated') and MR_MainFunctions.TradeValid(PortTrades.trdnbr) == 1 and PortTrades.curr.insid != 'ZAR':
            if (PortTrades.curr.insid) not in TradeCurrL:
                TradeCurrL.append(PortTrades.curr.insid)
    
    for TradeCurr in TradeCurrL:
        BASFLAG	                =	'BAS'
        HeaderName              =	'Position'
        OBJECT	                =	'PositionSPEC'
        TYPE	                =	'Position'
        
        IDENTIFIER              =       str(TradeCurr) + '_Cash_' + str(p.prfid)
        
        InstrumentXREF          =       str(TradeCurr)+ '_Cash'
        
        PositionUnitsCAL	=	''
        PositionUnitsDAYC	=	''
        PositionUnitsFUNC	=	''
        PositionUnitsPERD	=	''
        PositionUnitsSTRG	=	''

        PositionUnitsVAL        =	0
        
        PortfolioXREF           =       'prfid_' + str(p.prfid)

        SettlmntAccntXREF	=	''
        SettlementProcFUNC	=	''
        
        CounterpartySTRG   	=       ''
        TraderNAME		=       ''
        PositionUnitsUNIT       =       ''
        
        for Trades in p.trades():
            if Trades.status not in ('Void', 'Simulated') and TradeCurr == Trades.curr.insid and MR_MainFunctions.TradeValid(Trades.trdnbr) == 1:
                PositionUnitsVAL	=	PositionUnitsVAL + Trades.accumulated_cash()

        UserDefinedNAME4 = IDENTIFIER

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, UserDefinedNAME4))
    outfile.close()
    
    return ''

def CreatePositionStock(temp,FileDir,Filename,PositionName,InsName,PortName,CounterParty,Position,*rest):
    
    filename = FileDir + PositionName
    outfile = open(filename, 'a')
    
    Instrument = ael.Instrument[InsName]
    
    BASFLAG	                =	'BAS'
    HeaderName                  =	'Position'
    OBJECT	                =	'PositionSPEC'
    TYPE	                =	'Position'
    
    IDENTIFIER                  =       str(Instrument.insid) + '_' + str(PortName) + '_' + str(CounterParty)
    
    InstrumentXREF              =       'insaddr_'+str(Instrument.insaddr)
    
    PositionUnitsCAL	        =	''
    PositionUnitsDAYC	        =	''
    PositionUnitsFUNC	        =	''
    PositionUnitsPERD	        =	''
    PositionUnitsSTRG	        =	''
    
    PositionUnitsVAL            =	str(Position)
    
    PortfolioXREF               =       'prfid_' + str(PortName)
    
    SettlmntAccntXREF	        =	''
    SettlementProcFUNC	        =	''
    
    CounterpartySTRG   	        =       str(CounterParty)
    TraderNAME		        =       ''
    PositionUnitsUNIT           =       ''
    
    UserDefinedNAME4 = IDENTIFIER
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, UserDefinedNAME4))
    outfile.close()

    return ''

def CreatePositionOnTrades(temp,FileDir,Filename,PositionName,FilterName,*rest):
    
    filename = FileDir + PositionName
    trades = acm.FTradeSelection[FilterName]
    for trade in trades.Trades():    
        ACM_ConvertionToAEL(trade, filename)

    return ''
    
def ACM_ConvertionToAEL(t, filename):
    tr=ael.Trade[t.Oid()]
    CreatePositionIRSwap(tr, filename)
    return ''
