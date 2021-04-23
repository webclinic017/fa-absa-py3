
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel / Henk Nel
CR Number               :329737, 707888

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-02-22     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-488
'''


import ael, string, acm, MR_MainFunctions

InsL = []
MemL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename        = FileDir + Filename

    outfile         =  open(filename, 'w')
    
    BASFLAG         = 'BAS'
    HeaderName      = 'Credit Process'
    OBJECT          = 'Credit ProcessSPEC'
    TYPE            = 'Credit Process'
           
    NAME            = str('MARKET RISK DUMMY')[0:35] + "_Credit Process"
    IDENTIFIER      = str(33549) + "_Credit Process"

    outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME))

    ro_FLAG          = 'rm_ro'
    ro_HeaderName    = 'Credit ProcessSPEC : Recovery Rate'
    ro_ATTRIBUTE     = 'Recovery Rate'
    OBJECT           = 'Credit ProcessSPEC'
    RecoveryRateVAL  = '0'
    
    outfile.write('%s,%s,%s,%s,%s\n'%(ro_FLAG, ro_HeaderName, ro_ATTRIBUTE, OBJECT, RecoveryRateVAL))    

    outfile.close()

    del InsL[:]
    InsL[:] = []  
    
    del MemL[:]
    MemL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(yc,FileDir,Filename,*rest):

    
    filename        = FileDir + Filename
    outfile         = open(filename, 'a')

    #yc = ael.YieldCurve['CDIssuerCurve_HR']
    if (yc.seqnbr) not in InsL:
        InsL.append(yc.seqnbr)
        
        BASFLAG         = 'BAS'
        HeaderName      = 'Credit Process'
        OBJECT          = 'Credit ProcessSPEC'
        TYPE            = 'Credit Process'
        
        for member in yc.attributes():
            if (member.seqnbr) not in MemL:
                MemL.append(member.seqnbr)
                
                NAME            = str(member.issuer_ptynbr.ptyid)[0:32] + str(member.curr.insid)+"_Credit Process"
                IDENTIFIER      = str(member.issuer_ptynbr.ptynbr) + str(member.curr.insid)+ "_Credit Process"

                outfile.write('%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME))
                
                ro_FLAG          = 'rm_ro'
                ro_HeaderName    = 'Credit ProcessSPEC : Recovery Rate'
                ro_ATTRIBUTE     = 'Recovery Rate'
                OBJECT           = 'Credit ProcessSPEC'
                RecoveryRateVAL  = member.recovery_rate / 100
                
                outfile.write('%s,%s,%s,%s,%s\n'%(ro_FLAG, ro_HeaderName, ro_ATTRIBUTE, OBJECT, RecoveryRateVAL))
                
    outfile.close()

    return str(yc.seqnbr)
    
# WRITE - FILE ######################################################################################################

