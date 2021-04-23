
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :264536

 -- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003404656   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-444
'''


import ael, string, acm, MR_MainFunctions

InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    
    outfile             =  open(filename, 'w')
    
    outfile.close()
    
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename
    Instrument = acm.FInstrument[i.insaddr]
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)
        
        outfile = open(filename, 'a')
        #Base record
        
        BASFLAG             =       'BAS'
        HeaderName          =       'Synthetic'
        OBJECT              =       'Synthetic InstrumentSPEC'
        TYPE                =       'Synthetic InstrumentSPEC'
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''
        CurrencyUNIT        =       Instrument.Currency().Name()
        CostOfCarryCAL      =       ''
        CostOfCarryDAYC     =       ''
        CostOfCarryPERD     =       ''        
        CostOfCarryVAL      =   	''
        TheoModelXREF       =       'Basket Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, CostOfCarryCAL, CostOfCarryDAYC, CostOfCarryPERD, CostOfCarryVAL, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        Legs = i.legs()
        for l in Legs:
            #Rollover record            
                
            BASFLAG           =	'rm_ro'
            HeaderName	  =	'Synthetic : Component Weights'
            ATTRIBUTE	  =	'Component Weights'
            OBJECT            =	'Synthetic InstrumentSPEC'
            ComponentWghtVAL  =	1
                
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, ComponentWghtVAL))

            #Rollover record            
            BASFLAG            =	'rm_ro'
            HeaderName	   =	'Synthetic : Underlying Financial Entities'
            ATTRIBUTE	   =	'Underlying Financial Entities'
            OBJECT             =	'Synthetic InstrumentSPEC'           
            UndrFinEntitisXREF = 'insaddr_'+str(i.insaddr)+'_'+str(l.legnbr)
            outfile.write('%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, UndrFinEntitisXREF))
                                    
        outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################

