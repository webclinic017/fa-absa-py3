
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536
'''

'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :278978
'''


import ael, string, acm, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    #PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    #outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    #outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    #PositionFilename    = FileDir + PositionName
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        #Base record
        outfile = open(filename, 'a')

        BASFLAG             =       'BAS'
        HeaderName          =       'Synthetic'
        OBJECT              =       'Synthetic InstrumentSPEC'
        TYPE                =       'Synthetic Instrument'

        NAME                =       MR_MainFunctions.NameFix(str(i.insid))+'_Synthetic'
        IDENTIFIER          =       MR_MainFunctions.NameFix(str(i.insid))+'_Synthetic'
      
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       i.curr.insid
        CostOfCarryCAL      =       '' 
        CostOfCarryDAYC     =       ''
        CostOfCarryPERD     =       ''
        
        #dividendYield       =       ins.AdditionalInfo().DividendYield()
        #if dividendYield == None:
        CostOfCarryVAL      =       ''
        #else:
        #    CostOfCarryVAL      =       dividendYield
        
        
        TheoModelXREF       =       'Basket Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
       
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
            
        #Roll Over Record:  Component Weights
        
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Synthetic : Component Weights'
        ATTRIBUTE           =       'Component Weights'
        OBJECT              =       'Synthetic InstrumentSPEC'
        ComponentWghtVAL    =       '1'    

        

        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))
                
       
        #Roll Over Record:  Underlying Financial Entities
                
        BASFLAG             =       'rm_ro'
        HeaderName          =       'Synthetic : Underlying Financial Entities'
        ATTRIBUTE           =       'Underlying Financial Entities'
        OBJECT              =       'Synthetic InstrumentSPEC'
        UndrFinEntitisXREF  =       'insaddr_'+str(i.insaddr)

        outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))
                
          
        return i.insid

# WRITE - FILE ######################################################################################################
