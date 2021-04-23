'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 701575

Description
Add two Payment Procedure on instrument type Price Index
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    
    ins = acm.FInstrument[i.insaddr]
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        #Base record
        outfile = open(filename, 'a')
        
        if i.instype == 'PriceIndex':
            BASFLAG             =       'BAS'
            HeaderName          =       'Payment Procedure'
            OBJECT              =       'Payment ProcedureSPEC'
            TYPE                =       'Payment Procedure'
            NAME                =       MR_MainFunctions.NameFix(str(i.insid))+'_Start_PP'
            IDENTIFIER          =       MR_MainFunctions.NameFix(str(i.insid))+'_Start_PP'    
            UndrNotnlIndexXREF  =       MR_MainFunctions.NameFix(str(i.insid))+'_NI'
            PrpymnPrcdrFUNC     =       '@notional index start date'

            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, UndrNotnlIndexXREF, PrpymnPrcdrFUNC))

            BASFLAG             =       'BAS'
            HeaderName          =       'Payment Procedure'
            OBJECT              =       'Payment ProcedureSPEC'
            TYPE                =       'Payment Procedure'
            NAME                =       MR_MainFunctions.NameFix(str(i.insid))+'_End_PP'
            IDENTIFIER          =       MR_MainFunctions.NameFix(str(i.insid))+'_End_PP'    
            UndrNotnlIndexXREF  =       MR_MainFunctions.NameFix(str(i.insid))+'_NI'  
            PrpymnPrcdrFUNC     =       '@notional index end date'
            
            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, UndrNotnlIndexXREF, PrpymnPrcdrFUNC))
            
        else:
        
            BASFLAG             =       'BAS'
            HeaderName          =       'Payment Procedure'
            OBJECT              =       'Payment ProcedureSPEC'
            TYPE                =       'Payment Procedure'
            NAME                =       MR_MainFunctions.NameFix(str(i.insid))+'_PP'
            IDENTIFIER          =       MR_MainFunctions.NameFix(str(i.insid))+'_PP'    
            UndrNotnlIndexXREF  =       MR_MainFunctions.NameFix(str(i.insid))+'_NI'
            PrpymnPrcdrFUNC     =       '@notional index start date'        
            
            if i.instype in ('Stock', 'EquityIndex', 'FX', 'Bond', 'IndexLinkedBond'): #removed PriceIndex
                PrpymnPrcdrFUNC                =       '@notional index start date'
            else:
                PrpymnPrcdrFUNC                =       '@notional index end date'

            outfile.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, UndrNotnlIndexXREF, PrpymnPrcdrFUNC))
        outfile.close()    

    return i.insid

# WRITE2 - FILE ######################################################################################################
def Write2(temp,FileDir,Filename,PositionName,currpair,*rest):
    
    filename            = FileDir + Filename
    
    #Base record
    outfile = open(filename, 'a')

    BASFLAG             =       'BAS'
    HeaderName          =       'Payment Procedure'
    OBJECT              =       'Payment ProcedureSPEC'
    TYPE                =       'Payment Procedure'
    NAME                =       currpair+'_PP'
    IDENTIFIER          =       currpair+'_PP'
    UndrNotnlIndexXREF  =       currpair+'_NI'
    PrpymnPrcdrFUNC     =       '@notional index start date'
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, UndrNotnlIndexXREF, PrpymnPrcdrFUNC))
    
    BASFLAG             =       'BAS'
    HeaderName          =       'Payment Procedure'
    OBJECT              =       'Payment ProcedureSPEC'
    TYPE                =       'Payment Procedure'
    NAME                =       currpair+'_PP_End'
    IDENTIFIER          =       currpair+'_PP_End'
    UndrNotnlIndexXREF  =       currpair+'_NI'
    PrpymnPrcdrFUNC     =       '@notional index end date'
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, UndrNotnlIndexXREF, PrpymnPrcdrFUNC))
    outfile.close()    

    return currpair
    
   # WRITE2 - FILE ###################################################################################################### 
