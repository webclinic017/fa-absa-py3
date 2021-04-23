'''
Purpose                 :[Market Risk feed files],[A change to include prfnbr on PortfolioXREF]
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel, Tshepo Mabena
CR Number               :264536, 627760,CHNG0000048637

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-03-22     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-528
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''


import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    PositionFilename    = FileDir + PositionName
    outfileP            =  open(PositionFilename, 'w')
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    return PositionFilename

# OPENFILE ##########################################################################################################


def Write(t,FileDir,Filename,PositionName,*rest):
    
    PositionFilename    = FileDir + PositionName

    if MR_MainFunctions.ValidTradeNo(t) == 0:
        if MR_MainFunctions.IsExcludedPortfolio(t) == False:
            outfileP = open(PositionFilename, 'a')
            
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
            InstrumentXREF	=	'insaddr_'+str(t.insaddr.und_insaddr.insaddr)
            
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
            
            PortfolioNAME               =       t.prfnbr.prfid
            InstrumentTYPE              =       t.insaddr.instype
            TradeAggregationNAME        = 'trdnbr_'+str(t.trdnbr)
            
            outfileP.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, PositionUnitsCAL, PositionUnitsDAYC, PositionUnitsFUNC, PositionUnitsPERD, PositionUnitsSTRG, PositionUnitsUNIT, PositionUnitsVAL, InstrumentXREF, PortfolioXREF, SettlmntAccntXREF, SettlementProcFUNC, CounterpartySTRG, TraderNAME, PortfolioNAME, InstrumentTYPE, TradeAggregationNAME))
            outfileP.close()
    
    return t.insaddr.insid


