

'''
Purpose                 :[Market Risk feed files],[A change to include prfnbr on PortfolioXREF]
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel, Tshepo Mabena
CR Number               :264536,316586,287397,290307,434459,CHNG0000048637

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-427
'''
import ael, acm, string, MR_MainFunctions

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
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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
    
    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype


    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()
    
    return ''

def CreatePositionForwardStartingDeposits(t, filename):
   
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
    
    InstrumentXREF	=	'insaddr_' + str(t.insaddr.insaddr) + '_' + str(t.trdnbr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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
    
    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()
    
    return ''

def CreatePositionCombination(t, filename):
    
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
    PositionUnitsVAL	=	t.quantity/t.insaddr.index_factor
    
    InstrumentXREF	=	'insaddr_'+str(t.insaddr.insaddr)
    
    if t.prfnbr:
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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

    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype
 
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
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
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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

    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
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
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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

    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype
    
    #ExternalSystemRef           =       t.optional_key
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
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
        PortfolioXREF   =       'prfnbr_'+str(t.prfnbr.prfnbr)
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

    PortfolioNAME               = t.prfnbr.prfid
    InstrumentTYPE              = t.insaddr.instype
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()
    
    return ''

'''
def create_named_param(vector,Currency):
        param = acm.FNamedParameters();
        param.AddParameter('currency',Currency)
        vector.Add(param)

calc_space = acm.Calculations().CreateCalculationSpace( 'Standard','FPortfolioSheet' )
PortfolioL = []
'''
    
def CreatePositionCash(temp,FileDir,Filename,PositionName,Portfolio,curr,cash,*rest):

    port = acm.FPhysicalPortfolio[Portfolio].Oid() 
    filename    = FileDir + PositionName
    outfile     = open(filename, 'a')
    
    BASFLAG             =	'BAS'
    HeaderName          =	'Position'
    OBJECT	        =	'PositionSPEC'
    TYPE	        =	'Position'
    IDENTIFIER          =       str(curr) + '_Cash_' + str(Portfolio)
    InstrumentXREF      =       str(curr)+ '_Cash'
    PositionUnitsCAL	=	''
    PositionUnitsDAYC	=	''
    PositionUnitsFUNC	=	''
    PositionUnitsPERD	=	''
    PositionUnitsSTRG	=	''
    PositionUnitsVAL    =	cash
    PortfolioXREF       =       'prfnbr_' + str(port) #str(Portfolio)
    SettlmntAccntXREF	=	''
    SettlementProcFUNC	=	''
    CounterpartySTRG   	=       ''
    TraderNAME		=       ''
    PositionUnitsUNIT   =       ''

    PortfolioNAME               = Portfolio
    InstrumentTYPE              = 'Cash'

    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()

    return ''

    '''
    if Portfolio.prfid not in PortfolioL:
        PortfolioL.append(Portfolio.prfid)
    
        TradeCurrL  = []
        filename    = FileDir + PositionName
        outfile     = open(filename, 'a')
        TradeCurrL = acm.FCurrency.Select('')
        
        #set context, sheet type, column id, and portfolio
        context 	= acm.GetDefaultContext()
        sheet_type 	= 'FPortfolioSheet'
        ACMPortfolio= acm.FPhysicalPortfolio[Portfolio.prfid]

        #create CalculationSpace (virtual Trading Manager)
        #calc_space = acm.Calculations().CreateCalculationSpace( context,sheet_type )
        #add item to portfolio sheet
        top_node = calc_space.InsertItem(ACMPortfolio)
        calc_space.Refresh()
        #create named parameter
        
        #complex column example
        column_id 	= 'Portfolio Cash Vector'
        vector 		= acm.FArray()

        for Currency in TradeCurrL:
            TradeCurr = Currency.Name()
            if TradeCurr != 'ZAR':
                create_named_param(vector, Currency)

        column_config 	= acm.Sheet.Column().ConfigurationFromVector(vector)
        ins_node 		= top_node.Iterator().Find(Portfolio.prfid).Tree()
        
        calculation 	= calc_space.CreateCalculation(ins_node,column_id,column_config)
        
        for Value in calculation.Value():
                
            BASFLAG                 =	'BAS'
            HeaderName              =	'Position'
            OBJECT	                =	'PositionSPEC'
            TYPE	                =	'Position'
            IDENTIFIER              =       str(Value.Unit()) + '_Cash_' + str(Portfolio.prfid)
            InstrumentXREF          =       str(Value.Unit())+ '_Cash'
            PositionUnitsCAL	=	''
            PositionUnitsDAYC	=	''
            PositionUnitsFUNC	=	''
            PositionUnitsPERD	=	''
            PositionUnitsSTRG	=	''
            PositionUnitsVAL        =	Value.Number()
            PortfolioXREF           =       'prfnbr_' + str(Portfolio.prfid)
            SettlmntAccntXREF	=	''
            SettlementProcFUNC	=	''
            CounterpartySTRG   	=       ''
            TraderNAME		=       ''
            PositionUnitsUNIT       =       ''
            
            if PositionUnitsVAL != 0:
                outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG,HeaderName,OBJECT,TYPE,IDENTIFIER,PositionUnitsCAL,PositionUnitsDAYC,PositionUnitsFUNC,PositionUnitsPERD,PositionUnitsSTRG,PositionUnitsUNIT,PositionUnitsVAL,InstrumentXREF,PortfolioXREF,SettlmntAccntXREF,SettlementProcFUNC,CounterpartySTRG,TraderNAME))
        outfile.close()
        calc_space.Clear()
        '''


#CreatePositionCash(ael.Portfolio['LTFX'],'c:\\','Filename.csv','PositionName.csv')

def CreatePositionStock(temp,FileDir,Filename,PositionName,InsName,PortName,CounterParty,Position,*rest):

    port = acm.FPhysicalPortfolio[PortName].Oid()
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
    
    PortfolioXREF               =       'prfnbr_' + str(port)
    
    SettlmntAccntXREF	        =	''
    SettlementProcFUNC	        =	''
    
    CounterpartySTRG   	        =       str(CounterParty)
    TraderNAME		        =       ''
    PositionUnitsUNIT           =       ''
    
    PortfolioNAME               =       str(PortName)
    InstrumentTYPE              =       str(Instrument.instype)
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()

    return ''
    
def CreatePositionStockPremium(temp,FileDir,Filename,PositionName,InsName,PortName,CounterParty,AcquireDay,Position,*rest):

    port = acm.FPhysicalPortfolio[PortName].Oid()
    filename = FileDir + PositionName
    outfile = open(filename, 'a')
    
    Instrument = ael.Instrument[InsName]
    
    BASFLAG	                =	'BAS'
    HeaderName                  =	'Position'
    OBJECT	                =	'PositionSPEC'
    TYPE	                =	'Position'
    
    IDENTIFIER                  =       str(Instrument.insid) + '_' + str(PortName) + '_' + str(CounterParty) + '_' + str(AcquireDay)+'_P'
    
    InstrumentXREF              =       'Forward_ZAR' '_' + str(AcquireDay)
    
    PositionUnitsCAL	        =	''
    PositionUnitsDAYC	        =	''
    PositionUnitsFUNC	        =	''
    PositionUnitsPERD	        =	''
    PositionUnitsSTRG	        =	''
    
    PositionUnitsVAL            =	str(Position)
    
    PortfolioXREF               =       'prfnbr_' + str(port)
    
    SettlmntAccntXREF	        =	''
    SettlementProcFUNC	        =	''
    
    CounterpartySTRG   	        =       str(CounterParty)
    TraderNAME		        =       ''
    PositionUnitsUNIT           =       ''
    
    PortfolioNAME               =       str(PortName)
    InstrumentTYPE              =       str(Instrument.instype)
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE))
    outfile.close()

    return ''

def CreatePositionOnTrades(temp,FileDir,Filename,PositionName,FilterName,*rest):
    
    filename = FileDir + PositionName
    trades = acm.FTradeSelection[FilterName]
    for trade in trades.Trades():    
        ACM_ConvertionToAEL(trade, filename)

    return ''


def CreatePositionOnTrades_perTrade(temp,FileDir,Filename,PositionName,trd,*rest):
    
    filename = FileDir + PositionName
    CreatePositionIRSwap(trd, filename)
    '''
    trades = acm.FTradeSelection[FilterName]
    for trade in trades.Trades():    
        ACM_ConvertionToAEL(trade, filename)
    '''
    return ''

    
def ACM_ConvertionToAEL(t, filename):
    tr=ael.Trade[t.Oid()]
    CreatePositionIRSwap(tr, filename)
    return ''


