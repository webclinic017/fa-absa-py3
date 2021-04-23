'''
 -- HISTORY --
--------------------------------------------------------------------------------------------------------------------
Date           CR                    Requestor          Developer          Change
--------------------------------------------------------------------------------------------------------------------
2010-09-01     264536,290307         Natalie Austin     Douglas Finkel     Original
2020-09-11     CHG0128302	     Garth Saunders	Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
2021-03-11     CHG0158547            Thando Mpalala     Andile Biyana      https://absa.atlassian.net/browse/FAFO-41 
                                                                           
'''


import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
    
    outfile = open(filename, 'w')
    outfileP = open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()

    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename = FileDir + Filename
    PositionFilename = FileDir + PositionName
        
    ins = acm.FInstrument[i.insaddr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        BASFLAG = 'BAS'
        HeaderName = 'Synthetic'
        OBJECT = 'Synthetic InstrumentSPEC'
        TYPE = 'Synthetic Instrument'

        NAME = MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER = 'insaddr_'+str(i.insaddr)
        
        CurrencyCAL = ''
        CurrencyDAYC = ''
        CurrencyPERD = ''
        CurrencyUNIT = i.curr.insid
        
        CostOfCarryCAL = ''
        CostOfCarryDAYC = 'actual/365'
        CostOfCarryPERD = 'continuous'
        CostOfCarryVAL = ''
        
        TheoModelXREF = 'Basket Instrument'
        MarketModelXREF = ''
        FairValueModelXREF = ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        for Inst in ins.Instrument().InstrumentMaps():
            if Inst.Instrument().ExpiryDate() >= acm.Time().DateToday():
            
                # Roll Over Synthetic : Component
                BASFLAG = 'rm_ro'
                HeaderName = 'Synthetic : Component Weights'
                ATTRIBUTE = 'Component Weights'
                OBJECT = 'Synthetic InstrumentSPEC'
                
                if Inst.Instrument().InsType() in ('IndexLinkedBond'):
                    ComponentWghtVAL = 100 * Inst.Weight()/i.index_factor                
                else:
                    ComponentWghtVAL = Inst.Weight()/i.index_factor
                
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
                
                # Roll Over Synthetic : Underlying
                BASFLAG = 'rm_ro'
                HeaderName = 'Synthetic : Underlying Financial Entities'
                ATTRIBUTE = 'Underlying Financial Entities'
                OBJECT = 'Synthetic InstrumentSPEC'
                
                UndrFinEntitisXREF = ''
                
                try:
                    UndrFinEntitisXREF = 'insaddr_' + str(Inst.Instrument().Oid())
                except:
                    UndrFinEntitisXREF = ''
                    
                outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))
            
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePositionCombination(trades, PositionFilename)
    return i.insid

# WRITE - FILE ######################################################################################################
