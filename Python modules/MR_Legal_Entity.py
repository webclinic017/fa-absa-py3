'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 707888

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-02-22     CHNG0003469409   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-488
'''

import ael, string, acm, MR_MainFunctions

InsL = []
MemL = []

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    #PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    #outfileP            =  open(PositionFilename, 'w')
    
    #Base record
    BASFLAG             =       'BAS'
    HeaderName          =       'Legal EntitySPEC'
    OBJECT              =       'Legal EntitySPEC'
    TYPE                =       'Legal Entity'
    NAME                =       str('MARKET RISK DUMMY')[0:50]
    IDENTIFIER          =       'ptynbr_'+str(33549)
    CreditProcessXREF   =       str(33549) + '_Credit Process'
    
    outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CreditProcessXREF))    
    
    outfile.close()
    #outfileP.close()

    del InsL[:]
    InsL[:] = []
    del MemL[:]
    MemL[:] = []
    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(yc,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    outfile = open(filename, 'a')
  
    
    if str(yc.seqnbr) not in InsL:
        InsL.append(yc.seqnbr)

        #Base record

        BASFLAG             =       'BAS'
        HeaderName          =       'Legal EntitySPEC'
        OBJECT              =       'Legal EntitySPEC'
        TYPE                =       'Legal Entity'
        IDENTIFIER          =       ''
        NAME                =       ''
        CreditProcessXREF   =       ''
        for member in yc.attributes():
            if (member.seqnbr) not in MemL:
                MemL.append(member.seqnbr)

                NAME            = str(member.issuer_ptynbr.fullname)[0:47]+str(member.curr.insid)
                IDENTIFIER      = 'ptynbr_'+str(member.issuer_ptynbr.ptynbr)+str(member.curr.insid)

                CreditProcessXREF   = str(member.issuer_ptynbr.ptynbr)+str(member.curr.insid) + '_Credit Process'

      
        
                outfile.write('%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, IDENTIFIER, NAME, CreditProcessXREF))
    outfile.close()
    
    return str(yc.seqnbr)

# WRITE - FILE ######################################################################################################
