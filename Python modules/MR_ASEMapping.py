'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :586418,599672
'''

import ael, string, acm

# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,*rest):

    filename            = FileDir + Filename
    outfile             =  open(filename, 'w')
    outfile.close()

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,*rest):
    
    filename = FileDir + Filename
    
    if i.instype in ('EquityIndex', 'BondIndex', 'PriceIndex'):
        RiskFactor = i.insid + '_MarketIndex'
        Identifier = 'insaddr_' +str(i.insaddr) + '_MarketIndex'
    else:
        RiskFactor = i.insid
        Identifier = 'insaddr_' + str(i.insaddr)    
        
    outfile = open(filename, 'a')
    outfile.write('%s,%s\n'%(RiskFactor, Identifier))
    outfile.close()
        
    return RiskFactor

# WRITE - FILE ######################################################################################################

