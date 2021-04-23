'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Ashley Kanter
Developer               :Christoffel Human
CR Number               :MINT-461

-- HISTORY --
Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2016-01-20     CHNG0003500355   Ashley Canter      Chris Human        http://abcap-jira/browse/MINT-461
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

def Write(temp,p,FileDir,Filename,*rest):
    
    filename            = FileDir + Filename

    ins = acm.FInstrument[p.insaddr.insaddr]
    currins = acm.FInstrument[p.curr.insaddr]



    if (p.insaddr.insid + p.curr.insid) not in InsL:
        InsL.append(p.insaddr.insid + p.curr.insid)
        outfile = open(filename, 'a')
        
        #Base record
        Curr1	                =       p.insaddr.insid
        Curr2                   =       p.curr.insid
        CurrencyPrice           =       p.last

        outfile.write('%s,%s,%s\n'%(Curr1, Curr2, CurrencyPrice))
   
        outfile.close()

    return str(p.prinbr)

# WRITE - FILE ######################################################################################################
