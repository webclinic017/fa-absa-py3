"""
Name      : SAMM_CALL_IT3B
Purpose   : Perorm IT3b functions - produce output files + produce xml for statements

Changes

Developer : Jaysen Naicker, Jaysen Naicker
Purpose   : Add in the function to produce output file in ABSA Group format
             Chabge ABSA file output format to be compatible with 2010 format
Date      : 08-03-2010
Department and Desk : OPS
Requester           : Karen Mortimer, Karen Mortimer
CR Number           : 247019, 576596


History
=======

2017-05-24 Vojtech Sidorin  FAU-938 Update dependency on elementtree.
"""

import ael, string, datetime, acm, random
from zak_funcs import formnum
from xml.etree.ElementTree import Element, SubElement, ElementTree

def trunc(fNumber,*rest):
    iNumber = (int) (fNumber)
    return (str) (iNumber)

def load_ClientInfo(filename,index,p_list,mc_index, *rest):
    ClientDictionary = {}
    mc_list = []
    fhandle = open(filename)
    fline = fhandle.readline()
    fline = fhandle.readline()

    while fline:
        line = string.split(fline, ',')
        id = line[index].strip()
        if id <> '':
            if int(id) in p_list:
                ClientDictionary[id] = line
                if line[mc_index].strip() not in mc_list:
                    mc_list.append(line[mc_index].strip())
        fline = fhandle.readline()

    return ClientDictionary, mc_list

def load_ClientAddress(filename, index, mc_list, *rest):

    ClientDictionary = {}
    fhandle = open(filename)
    fline = fhandle.readline()
    fline = fhandle.readline()
    while fline:
        line = string.split(fline, ',')
        id = line[index].strip()
        if id in mc_list:
            ClientDictionary[id] = line
        fline = fhandle.readline()
    return ClientDictionary
    												
def get_trade_detail(trds,FromDay, ToDay, Client_Dictionary, *rest):
    cd = Client_Dictionary
    details = {}

    for trd in trds:
        if ael.Party[trd.counterparty_ptynbr.ptynbr] and cd.has_key((str) (trd.counterparty_ptynbr.ptynbr)):
            skipentry = 0
            i = trd.insaddr
            l = i.legs()[0]
            
            #SEC_ID
            outstring =  'I'
            
            #ITS_PERS_ID
            
            if cd.has_key((str) (trd.counterparty_ptynbr.ptynbr)):
                outstring = outstring + string.ljust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2][0:25], 25)
            else:
                 outstring = outstring + string.ljust(((str)(trd.counterparty_ptynbr.ptynbr) + trd.counterparty_ptynbr.ptyid)[0:25], 25)
            
            #INCOME_NATURE
            outstring = outstring + '4201'
            
            #INCOME_PAID
            interest = 0
            int_set = trd.interest_settled(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1), 'ZAR')
            int_acc = trd.interest_accrued(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1), 'ZAR')
            #int_due = trd.interest_due(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1),'ZAR')
            int_due = 0
            interest = (int_set + int_acc + int_due)*trd.quantity 

            if interest < 0: 
                outstring = outstring + string.rjust(trunc(abs(interest)*100), 15)
                if trunc(abs(interest)*100) == '0' :
                    skipentry = 1
            else:
                outstring = outstring + string.rjust('0', 15)
                skipentry = 1

                
            #ACCOUNT_NO    
            outstring = outstring + string.ljust(trd.insaddr.insid[0:20], 20)
            
            #BRANCH_CODE
            outstring = outstring + string.rjust('0', 6)
            
            #ACCOUNT_TYPE
            outstring = outstring + string.rjust('12', 2)
            
            #START_DATE
            if trd.value_day > ael.date(FromDay.isoformat()):
                vdate=  ael.date(trd.value_day).to_string()
                outstring = outstring + string.split(vdate, '/')[2] + string.split(vdate, '/')[1] + string.split(vdate, '/')[0]
            else:    
                outstring = outstring + FromDay.strftime('%Y%m%d')

            #START_BAL
            balance = 0
            if trd.value_day > ael.date(FromDay.isoformat()):
                for cf in l.cash_flows():
                    if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                        if (cf.pay_day == trd.value_day) :
                            balance = balance + cf.projected_cf()*trd.quantity
            else:
                for cf in l.cash_flows():
                    if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                        if (cf.pay_day < ael.date(FromDay.isoformat())) :
                            balance = balance + cf.projected_cf()*trd.quantity
            outstring = outstring + string.rjust(trunc(abs(balance)*100), 15)
    
            #START_BAL_SIGN
            if balance < 0:
                outstring = outstring + 'C'
            else:
                outstring = outstring + 'D'
                
            #END_DATE
            outstring = outstring + ToDay.strftime('%Y%m%d')
            
            #END_BAL
            balance = 0
            for cf in l.cash_flows():
                if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                    if (cf.pay_day <= ael.date(ToDay.isoformat())) :
                        balance = balance + cf.projected_cf()*trd.quantity
            
            #END_BAL_SIGN           
            outstring = outstring + string.rjust(trunc(abs(balance)*100), 15)
            if balance < 0:
                outstring = outstring + 'C'
            else:
                outstring = outstring + 'D'
                
            #FOREIGN_TAX_PAID
            outstring = outstring + string.rjust('0', 15)
            

            if skipentry == 0:
                if trd.counterparty_ptynbr.ptynbr <> 32006:
           
                    if details.has_key(string.ljust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2], 25)):
                        entries = details[string.ljust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2], 25)]
                        entries.append(outstring)
                        details[string.ljust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2], 25)] = entries 
                    else:
                        details[string.ljust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2], 25)] = [outstring]

    return details      
    

def get_client_details(Client_Dictionary,Client_Address, FromDay, ToDay, *rest):
    cd = Client_Dictionary
    ca = Client_Address
    clients = {}
    for k in cd.keys():
        
        cparty = ael.Party[(int) (cd[k][1])]
        outstring = 'P'
        
        #IT3_PERS_ID
        outstring = outstring + string.ljust(cd[k][0][0:25], 25)
        
        #IT_REF_NO
        outstring = outstring + string.ljust('0000000000', 10)
        
        #PERIOD_START
        outstring = outstring + FromDay.strftime('%Y%m%d')
        
        #PERIOD_END
        outstring = outstring + ToDay.strftime('%Y%m%d')
        
        #TP-CATEGORY
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.rjust('1', 2)
        elif (cd[k][17] == 'Private trusts') or (cd[k][17] == 'Trust companies'):
            outstring = outstring + string.rjust('3', 2)
        else:
            outstring = outstring + string.rjust('2', 2)
            
        #TP_ID    
        if (cd[k][17] == 'Individuals') and (cd[k][9] == 'SOUTH AFRICA'):
            outstring = outstring + string.ljust(cd[k][3], 13)
        else:
            outstring = outstring + string.ljust('', 13)
            
        #TP_OTHER-ID    
        if (cd[k][17] == 'Individuals - Foreign') and (cd[k][9] != 'SOUTH AFRICA'):
            outstring = outstring + string.ljust(cd[k][3], 10)
        else:
            outstring = outstring + string.ljust('', 10)
        
        #CO-REG-NO
        if (cd[k][17] == 'Private trusts') or (cd[k][17] == 'Trust companies') or (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust('', 15)
        else:
            outstring = outstring + string.ljust(cd[k][4][0:15], 15)
        
        #TRUST-DEED-NO
        if (cd[k][17] == 'Private trusts') or (cd[k][17] == 'Trust companies'):
            outstring = outstring + string.ljust(cd[k][4][0:10], 10)
        else:
            outstring = outstring + string.ljust('', 10)
            
        #TP_NAME
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][20][0:120]), 120)
        else:
            outstring = outstring + string.ljust(cd[k][7][0:120], 120)
            
        #TP_INITS
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][22][0:5]), 5)
        else:
            outstring = outstring + string.ljust('', 5)
            
        #TP_FIRSTNAMES
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][21][0:90]), 90)
        else:
            outstring = outstring + string.ljust('', 90)
            
        #TP_DOB
        if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):            
            if len(cd[k][5])> 1:
                outstring = outstring + string.ljust(string.split(cd[k][5], '/')[0] + string.split(cd[k][5], '/')[1] + string.split(cd[k][5], '/')[2], 8)
            else:
                outstring = outstring + string.ljust('', 8)
        else:
            outstring = outstring + string.ljust('', 8)
    
        #TP_TRADE_NAME
        if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust('', 120)
        else:
            #outstring = outstring + string.ljust(cd[k][8][0:120],120)
            outstring = outstring + string.ljust('', 120)
        
        if cparty.address:
        
            #TP_POST_ADDR_1
            if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.address[0:35], 35)
            else:
                outstring = outstring + string.ljust(cparty.address[0:35], 35)   
                
            #TP_POST_ADDR_2
            if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.address2[0:35], 35)
            else:
                outstring = outstring + string.ljust(cparty.address2[0:35], 35)    
            
            #TP_POST_ADDR_3
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust('', 35)
            else:
                outstring = outstring + string.ljust('', 35)   
                
            #TP_POST_ADDR_4
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust('', 35)
            else:
                outstring = outstring + string.ljust('', 35) 
         
            #TP_POST_CODE
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.zipcode[0:10], 10)
            else:
                outstring = outstring + string.ljust(cparty.zipcode[0:10], 10)   
        else:
            #TP_POST_ADDR_1
            if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.address[0:35], 35)
            else:
                outstring = outstring + string.ljust(cparty.address[0:35], 35)   
                
            #TP_POST_ADDR_2
            if cd[k][17] == (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.address2[0:35], 35)
            else:
                outstring = outstring + string.ljust(cparty.address2[0:35], 35)    
            
            #TP_POST_ADDR_3
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust('', 35)
            else:
                outstring = outstring + string.ljust('', 35)   
                
            #TP_POST_ADDR_4
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust('', 35)
            else:
                outstring = outstring + string.ljust('', 35) 
         
            #TP_POST_CODE
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(cparty.zipcode[0:10], 10)
            else:
                outstring = outstring + string.ljust(cparty.zipcode[0:10], 10)  
                
                
        #TP_PHY_ADDR_1
        if ca.has_key(cd[k][0]):
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(ca[cd[k][0]][5][0:35], 35)
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][5][0:35], 35)
        else:
                outstring = outstring + string.ljust('', 35)
    
        #TP_PHY_ADDR_2
        if ca.has_key(cd[k][0]):
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(ca[cd[k][0]][6][0:35], 35)
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][6][0:35], 35)  
        else:
                outstring = outstring + string.ljust('', 35)
        
        #TP_PHY_ADDR_3
        if ca.has_key(cd[k][0]):
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(ca[cd[k][0]][7][0:35], 35)
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][7][0:35], 35)   
        else:
                outstring = outstring + string.ljust('', 35)

        #TP_PHY_ADDR_4
        if ca.has_key(cd[k][0]):
            if cd[k][17] == 'Individuals':
                outstring = outstring + string.ljust(ca[cd[k][0]][8][0:35], 35)
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][8][0:35], 35)
        else:
                outstring = outstring + string.ljust('', 35)
     
        #TP_PHY_CODE
        if ca.has_key(cd[k][0]):
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust( string.rstrip(ca[cd[k][0]][10][0:10]), 10)
            else:
                outstring = outstring + string.ljust(string.rstrip(ca[cd[k][0]][10][0:10]), 10)         
        else:
                outstring = outstring + string.ljust('', 10)
            
        #TP_SA_RES
        if (cd[k][9] != 'SOUTH AFRICA') and (cd[k][15] != 'Foreign Company'):
            outstring = outstring + 'N'
        else:
            outstring = outstring + 'Y'   
        
        #PARTNERSHIP
        outstring = outstring + 'N'
        clients[string.ljust(cd[k][0], 25)] = outstring
    return clients


def get_Details_Header(*rest):
    outstring = 'H'
        
    #INFO_TYPE
    outstring = outstring + 'IT3EXTRS'
        
    #INFO_SUBTYPE
    outstring = outstring + string.ljust('', 8)
        
    #TEST_DATA
    outstring = outstring + 'Y'
        
    #FILES_SERIES_CTL
    outstring = outstring + 'S'
        
    #EXT_SYS
    outstring = outstring + string.ljust('ABSA001', 8)
    
    #VER_NO
    outstring = outstring + string.rjust('1', 8)

    #OWN_FILE_ID
    outstring = outstring + string.ljust('', 14)    

    #OWN_FILE_ID
    outstring = outstring + string.ljust(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), 14)
    return outstring
    
    
def get_Details_Trailer(num, *rest):
    outstring = 'T'
        
    #REC_NO
    outstring = outstring + string.rjust((str) (num), 8)
    return outstring
    
def write_SARS_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address, SARS_file, *rest):    
	
    ExcludedClients = {}
    #ExcludedClients[string.ljust('19230',25)] = '19230'
    #ExcludedClients[string.ljust('60798',25)] = '60798'
    #ExcludedClients[string.ljust('7106',25)] = '7106'
    #ExcludedClients[string.ljust('7067',25)] = '7067'
    ExcludedClients[string.ljust('15036', 25)] = '15036'
    #ExcludedClients[string.ljust('6834',25)] = '6834'
    #ExcludedClients[string.ljust('23398',25)] = '23398'
    ExcludedClients[string.ljust('2335', 25)] = '2335'
    ExcludedClients[string.ljust('15043', 25)] = '15043'
    ExcludedClients[string.ljust('7032', 25)] = '7032'
    ExcludedClients[string.ljust('30574', 25)] = '30574'
    ExcludedClients[string.ljust('6781', 25)] = '6781'
    #ExcludedClients[string.ljust('30671',25)] = '30671'
    ExcludedClients[string.ljust('119175', 25)] = '119175'
    ExcludedClients[string.ljust('29580', 25)] = '29580'
    ExcludedClients[string.ljust('45023', 25)] = '45023'
    
    clients = get_client_details(cd, cd_address, FromDay, ToDay)
    trd_details = get_trade_detail(trdlist, FromDay, ToDay, cd_extra)

    tmpfile = file(SARS_file, 'w')
    tmpfile.write(get_Details_Header() + '\n')
    num = 0
    for ckey in clients:
        if trd_details.has_key(ckey):
            if not (ExcludedClients.has_key(ckey)):
                tmpfile.write(clients[ckey] + '\n')
                num = num + 1
                tentries = trd_details[ckey]
                for ent in tentries:
                    tmpfile.write(ent + '\n')
                    num = num + 1
                 
    tmpfile.write(get_Details_Trailer(num) + '\n')
    tmpfile.close()
    
    print 'done'

def GenStatementXML(trd,FromDay, ToDay, CPRINT,CFAX, CEMAIL, freq, con, cd, cd_address, cd_extra, path, PrinterName, *rest):
    status = 'FAIL'
    newdate = ael.date_today().to_string('%Y%m%d')
    s =  str(trd.insaddr.insid[0:18]).replace("/", "_") + '_' + newdate+ '_'+ str(int(random.random()*1000)) +'.xml'
    name =  path + s  
	    
    if CPRINT == 1:
        
        STAT = Element("STATEMENT")
        
    else:
        DOC = Element("DOC")
        STAT = SubElement(DOC, "STATEMENT")
    
    
        
# ========================================================================================
#       CONTACT DETAILS 
# ========================================================================================  
        
    CUST = SubElement(STAT, "PCG") 
    SubElement(CUST, "BNAM").text ='Secondary Markets Operations'
    SubElement(CUST, "BAD2").text ='Absa Capital'
    SubElement(CUST, "BAD3").text ='Private Bag X10056'
    SubElement(CUST, "BAD4").text ='Sandton'
    SubElement(CUST, "BAD5").text ='2146'
    SubElement(CUST, "BTEL").text ='+27 11 3502891'
    SubElement(CUST, "BFAX").text ='+27 11 3502899'
    SubElement(CUST, "BCON").text ='SHARON MAYNARD/BRIAN ALEXANDER'
    
    SubElement(STAT, "MSG").text = ''
    
    
# ========================================================================================
#       CUSTOMER CONTACT DETAILS 
# ======================================================================================== 
 
    p = trd.counterparty_ptynbr
    CNAM = p.fullname + ' ' + p.fullname2
    PRINT = 'FAX'
    flag = 0
    check = 0
    l1 = []
    ctot=[]
    if CPRINT == 1:
        c1 = []
        c1.append('PRINT')
        c1.append(PrinterName)
        ctot.append(c1)
    
    if con != 0:
        c = ael.Contact[con]
        
        Fax = c.fax
        Attention = c.attention
        if c.address:
            l1.append(c.address.replace('&', '&amp;'))
            
        if c.address2:
            l1.append(c.address2.replace('&', '&amp;'))
            
        if c.city:
            l1.append(c.city.replace('&', '&amp;'))
            
        if c.zipcode:
            l1.append(c.zipcode)
            
        if c.country:
            l1.append(c.country.replace('&', '&amp;'))
            
        if CFAX ==1 and c.fax:
            c1 = []
            c1.append('FAX')
            c1.append(c.fax.replace('+27', '0'))
            ctot.append(c1)
            CFAX = 0
        if CEMAIL ==1 and c.email:
            c1 = []
            c1.append('EMAIL')
            c1.append(c.email)
            ctot.append(c1)
            CEMAIL = 0
    else:
         
        Fax = p.fax
        Attention = p.attention
        if p.address:
            l1.append(p.address.replace('&', '&amp;'))
            
        if p.address2:
            l1.append(p.address2.replace('&', '&amp;'))
            
        if p.city:
            l1.append(p.city.replace('&', '&amp;'))
            
        if p.zipcode:
            l1.append(p.zipcode)
            
        if p.country:
            l1.append(p.country.replace('&', '&amp;'))
    
        if CFAX ==1 and p.fax:
            c1 = []
            c1.append('FAX')
            c1.append(p.fax.replace('+27', '0'))
            ctot.append(c1)
            CFAX = 0
        if CEMAIL ==1 and p.email:
            c1 = []
            c1.append('EMAIL')
            c1.append(p.email)
            ctot.append(c1)
            CEMAIL = 0
    
    
    
    CACC = str(trd.insaddr.insid[0:18])
    CNAM = CNAM.replace('&', '&amp;') 
        
    CUST1 = SubElement(STAT, "CUSTLIN2") 
    SubElement(CUST1, "CNAM").text =CNAM
    SubElement(CUST1, "CACC").text =CACC
    
    ind = 1
    for x in l1:
        field = "CADD" + str(ind)
        SubElement(CUST1, field).text = x
        ind = ind +1
       
    
    ind = 1
    COM = SubElement(STAT, "COMM")
    for x in ctot:
        fielda = "CTYPE" 
        fieldb = "CDEST" 
        SubElement(COM, fielda).text = x[0]
        SubElement(COM, fieldb).text = x[1]
        ind = ind + 1


    ins = trd.add_info('Funding Instype')
    H1 = ins
    H2 = 'CERTIFICATE FOR INCOME TAX PURPOSES'
    
    
    HEAD2 = SubElement(STAT, "HEADER") 
    SubElement(HEAD2, "ATT").text = str(Attention)
    SubElement(HEAD2, "H1").text = H1
    SubElement(HEAD2, "H2").text = H2
    SubElement(HEAD2, "CDATE").text = ael.date_today().to_string("%d/%m/%Y")
    SubElement(HEAD2, "FROMDATE").text = FromDay.to_string("%d/%m/%Y")
    SubElement(HEAD2, "TODATE").text = ToDay.to_string("%d/%m/%Y")
    
    if cd.has_key(str(p.ptynbr)):
        if cd[str(p.ptynbr)][21] == '':
            SubElement(HEAD2, "CLIENTNAME").text = str(cd[str(p.ptynbr)][6][0:22] )
        else:
            SubElement(HEAD2, "CLIENTNAME").text = str(cd[str(p.ptynbr)][21][0:22] )
    else:
        SubElement(HEAD2, "CLIENTNAME").text = str(cd_extra[str(p.ptynbr)][4][0:22] )
        
    if cd.has_key(str(p.ptynbr)):    
        SubElement(HEAD2, "CLIENTCODE").text = str(cd[str(p.ptynbr)][0] )
    else:
        SubElement(HEAD2, "CLIENTCODE").text = str(cd_extra[str(p.ptynbr)][2] )
    
    if cd.has_key(str(p.ptynbr)):    
        if cd[str(p.ptynbr)][3] == '':
            if cd[str(p.ptynbr)][4] == '':
                SubElement(HEAD2, "IDNO").text = str("n/a")
            else:
                SubElement(HEAD2, "IDNO").text = str(cd[str(p.ptynbr)][4] )
        else:
            SubElement(HEAD2, "IDNO").text = str(cd[str(p.ptynbr)][3] )
    else:
        SubElement(HEAD2, "IDNO").text = str("n/a")
       

    if cd.has_key(str(p.ptynbr)): 
        if cd[str(p.ptynbr)][2] == '':
            SubElement(HEAD2, "TAXREF").text = str("n/a")
        else:
            SubElement(HEAD2, "TAXREF").text = str(cd[str(p.ptynbr)][2] )
    else:
        SubElement(HEAD2, "TAXREF").text = str("n/a")
    
    if cd.has_key(str(p.ptynbr)):
        if cd_address.has_key(cd[str(p.ptynbr)][0]):
            SubElement(HEAD2, "RESADD1").text = str(cd_address[cd[str(p.ptynbr)][0]][9])
            SubElement(HEAD2, "RESADD2").text = str(cd_address[cd[str(p.ptynbr)][0]][10])
            SubElement(HEAD2, "RESADD3").text = str(cd_address[cd[str(p.ptynbr)][0]][11]) 
        else:
            SubElement(HEAD2, "RESADD1").text =  ''
            SubElement(HEAD2, "RESADD2").text =  ''
            SubElement(HEAD2, "RESADD3").text =  ''
    else:
        SubElement(HEAD2, "RESADD1").text =  ''
        SubElement(HEAD2, "RESADD2").text =  ''
        SubElement(HEAD2, "RESADD3").text =  ''


    tot = 0.0
    
    int_set = trd.interest_settled(ael.date(FromDay), ael.date(ToDay).add_days(1), 'ZAR')
    int_acc = trd.interest_accrued(ael.date(FromDay), ael.date(ToDay).add_days(1), 'ZAR')
    #int_due = trd.interest_due(ael.date(FromDay), ael.date(ToDay).add_days(1),'ZAR')
    #tot = (int_set + int_acc + int_due)*trd.quantity 
    tot = (int_set + int_acc )*trd.quantity 
    if tot > -0.005: 
        tot = 0


    ins = trd.insaddr
    leg = ins.legs()[0]
    cashflows = leg.cash_flows()
    cap = 0
    #==========Interest========================
    for cf in cashflows:
        if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
            val = cf.projected_cf()*trd.quantity
            if abs(val) > 0.005:
                if cf.type == 'Fixed Amount':
                    if cf.start_day and cf.start_day <= ToDay:
                        cap += val
                        #print 'back dated', val
                    else:
                        if cf.pay_day <= ToDay:
                            cap += val
                            #print 'normal', ToDay, val
                else:
                    if cf.pay_day <= ToDay:
                        cap += val


    
    D = SubElement(STAT, "DETAIL")
    SubElement(D, "ACCTYPE").text = trd.add_info('Funding Instype').upper()
    SubElement(D, "ACCNUM").text = CACC
    SubElement(D, "DIVISION").text = 'ABS'
    SubElement(D, "CAPITAL").text = formnum(cap)
    SubElement(D, "INTEREST").text = formnum(tot*-1)

    if tot == 0 :
        
        status = 'FAIL'
        #print 'total interest is less than or equal to zero ', trd.insaddr.insid
        return status
        
    if CPRINT == 1:
        
        return STAT
        
    else:  
        #moved the file creation to end so that it will not create the file if the balances is zero
        try: 
            xmloutFile=open(name, 'w')
            ElementTree(DOC).write(xmloutFile, encoding='utf-8')
            
            status = 'SUCCESS'
        except: 
            status = 'FAIL'
            #raise 'cant open'
            print 'cant open ', name
        
        return status
    
def write_XML_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address, path, PrinterName, *rest):
    global printflag
    printflag = 0
    DOC = Element("DOC")
    newdate = ael.date_today().to_string('%Y%m%d')
    s = "Print_Statements_" + newdate + ".xml"
    name =  path + s  
    
    Print = 0
    Fax = 0
    Email = 0
    
    for t in trdlist:
        if (t.value_day <= ToDay) and not (t.mirror_trdnbr):
            p = t.counterparty_ptynbr
            if cd_extra.has_key(str(p.ptynbr)) :
                cts = p.contacts()
                comm = ''
                if cts:
                    for c in cts:
                        rules = c.rules()
                        tag =  ''
                        for r in rules:
                            
                            if r.instype == t.insaddr.instype: # and r.event_chlnbr.entry == 'Money Market':
                                if  c.add_info('Comm Freq'):
                                    freq = c.add_info('Comm Freq')
                                    if freq.find('Monthly') >= 0 or freq.find('All') >= 0:
                                        
                                        comm = str(c.add_info('Comm Type - Monthly'))
                                        if (comm.find('Print') >= 0 or comm.find('All') >= 0): 
                                            tag = GenStatementXML(t, FromDay, ToDay, 1, 0, 0, '/MONTHLY', c.seqnbr, cd, cd_address, cd_extra, path, PrinterName)
                                            if tag != 'FAIL':
                                                Print = Print + 1
                                                DOC.append(tag)
                                                printflag = 1
                                                    
                                        if (comm.find('Fax') >= 0 or comm.find('All') >= 0):
                                            tag = GenStatementXML(t, FromDay, ToDay, 0, 1, 0, '/MONTHLY', c.seqnbr, cd, cd_address, cd_extra, path, PrinterName)
                                            if tag != 'FAIL':
                                                Fax = Fax + 1
                                                
                                        if (comm.find('Email') >= 0 or comm.find('All') >= 0):
                                            tag = GenStatementXML(t, FromDay, ToDay, 0, 0, 1, '/MONTHLY', c.seqnbr, cd, cd_address, cd_extra, path, PrinterName)
                                            if tag != 'FAIL':
                                                Email = Email + 1
    
                                        #if (tag != 'FAIL')  and (tag != ''):


                        if tag == '':
                            tag = GenStatementXML(t, FromDay, ToDay, 1, 0, 0, '/MONTHLY', c.seqnbr, cd, cd_address, cd_extra, path, PrinterName)
                            if tag != 'FAIL':
                                Print = Print + 1
                                DOC.append(tag)
                                printflag = 1                        
    
    if printflag == 1:
        xmloutFile = name
        ElementTree(DOC).write(xmloutFile, encoding='utf-8') 

    return 'success'
    
    
def Comp3(num, zlen, *rest):

    num_str = string.zfill(str (abs(int (num))), zlen*2)
    out_str = ''
    
    
    if len(num_str) % 2 == 0:
        num_str = '0' + num_str

    for i in range(len(num_str)/2):
        out_str = out_str +  chr(int (num_str[i*2:i*2+1]) * 16 + int (num_str[i*2+1:i*2+2]))
    
    if len(num_str) == 1:
        i=-1
    
    if num < 0:
        out_str = out_str + chr(int (num_str[i*2+2:i*2+3]) * 16 + 13)
    else:
        out_str = out_str +  chr(int (num_str[i*2+2:i*2+3]) * 16 + 12 )
    
    return out_str[len(out_str)-zlen:len(out_str)]

									
def get_trade_detail1(trds, FromDay, ToDay, cd, pc, *rest):
    details = {}

    for trd in trds:
        if ael.Party[trd.counterparty_ptynbr.ptynbr] and cd.has_key((str) (trd.counterparty_ptynbr.ptynbr)):
            skipentry = 0
            i = trd.insaddr
            l = i.legs()[0]

            #RECTP
            outstring =  '3'
            
            #SRT-PCODE
            if pc.has_key(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]):
                outstring = outstring + pc[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]]
            else:
                outstring = outstring + '00000'
                
            #SRT-CLNTCDE
            outstring = outstring + string.rjust(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2][0:10], 10)[:10]  
 
            #ACC-DESCR
            outstring = outstring + string.ljust('Investment account', 25)[:25] 
        
            #ACNO
            outstring = outstring + string.ljust('', 16)
            
            #ALPHA-ACNO    
            outstring = outstring + string.ljust(trd.insaddr.insid[0:19], 19)[:19]  
            
            #CORP
            outstring = outstring + 'ABS'
                
            #ABAL
            balance = 0
            for cf in l.cash_flows():
                if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                    if (cf.pay_day <= ael.date(ToDay.isoformat())) :
                        balance = balance + cf.projected_cf()*trd.quantity

            outstring = outstring + string.zfill(str(trunc(abs(balance)*100)), 15)[:15]
                        
            #PBAL
            balance = 0
            if trd.value_day > ael.date(FromDay.isoformat()):
                for cf in l.cash_flows():
                    if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                        if (cf.pay_day == trd.value_day) :
                            balance = balance + cf.projected_cf()*trd.quantity
            else:
                for cf in l.cash_flows():
                    if cf.type in ('Fixed Amount', 'Interest Reinvestment'):
                        if (cf.pay_day < ael.date(FromDay.isoformat())) :
                            balance = balance + cf.projected_cf()*trd.quantity
            outstring = outstring + string.zfill(str(trunc(abs(balance)*100)), 15)[:15]
            
            #AINT
            interest = 0
            int_set = trd.interest_settled(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1), 'ZAR')
            int_acc = trd.interest_accrued(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1), 'ZAR')
            #int_due = trd.interest_due(ael.date(FromDay.isoformat()), ael.date(ToDay.isoformat()).add_days(1),'ZAR')
            int_due = 0
            interest = (int_set + int_acc + int_due)*trd.quantity 

            if interest < 0: 
                outstring = outstring + string.zfill(str(trunc(abs(interest)*100)), 15)[:15]
                if trunc(abs(interest)*100) == 0 :
                    skipentry = 1
            else:
                outstring = outstring + '000000000000000'
                skipentry = 1

            #SPEC-DES
            outstring = outstring + string.ljust('', 50)   

            #INVSTMNT
            outstring = outstring + string.ljust('00', 2)  

            #BRCD
            outstring = outstring + string.rjust('000000', 6)
                        
            #FILLER
            #outstring = outstring + string.ljust('',253)   
            
            #AV-MON-BAL
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            outstring = outstring + string.rjust('000000000000000', 15)
            
            #ACC-OPEN-DT
            outstring = outstring + str(FromDay).replace("-", "")
            
            #ACC-CLOS-DT
            outstring = outstring + str(ToDay).replace("-", "")
            
            #ACCR-INT
            interest = int_acc *trd.quantity 
            if interest < 0: 
                outstring = outstring + string.zfill(str(trunc(abs(interest)*100)), 15)[:15]
            else:
                outstring = outstring + '000000000000000'
     
            #INT-PAID
            interest = int_set *trd.quantity 
            if interest < 0: 
                outstring = outstring + string.zfill(str(trunc(abs(interest)*100)), 15)[:15]
            else:
                outstring = outstring + '000000000000000'  
            
            
            if skipentry == 0:
                if details.has_key(cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]):
                    entries = details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][0]
                    entries.append(outstring)
                    details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][0]= entries 
                    details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][1] = details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][1] + 1
                    details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][2] = details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]][2] + abs(interest)
                else:
                    details[cd[(str) (trd.counterparty_ptynbr.ptynbr)][2]]= [[outstring], 1, abs(interest)]
    
    return details      


def get_postal_code(cd, *rest):
    pc = {}
    for k in cd.keys():
        if ael.Party[int (k)]:
            cparty = ael.Party[int (k)]

            if cparty.zipcode[0:5] == '' or not (cparty.zipcode[0:5]).isdigit():
                outstring = '00000'
            else:
                outstring = string.zfill(cparty.zipcode[0:5], 5)[:5]
            
            if pc.has_key(cd[k][0]):
                if int (pc[cd[k][0]]) == 0:
                    pc[cd[k][0]] = outstring
            else:
                pc[cd[k][0]] = outstring
    return pc


def get_client_details1(cd, td, pc, *rest):
    clients = {}
    for k in cd.keys():
        if td.has_key(cd[k][0]):

            #RECTP
            outstring = '1'
            
            #SRT-PCODE
            if pc[cd[k][0]]:
                outstring = outstring + pc[cd[k][0]]
            else:
                outstring = outstring + '00000'
                    
            #SRT-CLNTCDE
            outstring = outstring + string.rjust(cd[k][0][0:10], 10)[:10] 

            #LANGUAGE
            outstring = outstring + 'E'

            #RECEIVER-IND
            if td[cd[k][0]][2] < 700:
                outstring = outstring + 'N'
            else:
                outstring = outstring + 'Y'
                
            #FILLER
            #outstring = outstring + string.rjust('',378)   
            
            clients[cd[k][0]] = outstring
    return clients


def get_client_details2(cd, ca, pc, *rest):
    clients = {}
    for k in cd.keys():
        cparty = ael.Party[int (k)]

        ca_key_found = False
        RCODE = 0
        for ca_key in ca.keys():
            if cd[k][0] == ca_key:
                ca_key_found = True
                if (ca[ca_key][13]).isdigit():
                    RCODE = ca[ca_key][13]

        #RECTP
        outstring = '2'
        
        #SRT-PCODE
        if pc[cd[k][0]]:
            outstring = outstring + pc[cd[k][0]]
        else:
            outstring = outstring + '00000'
       
        #SRT-CLNTCDE
        outstring = outstring + string.rjust(cd[k][0][0:10], 10)[:10] 
       
        #TITLE
        outstring = outstring + string.ljust('', 8)
      
        #INITS
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][22][0:3]), 3)[:3] 
        else:
            outstring = outstring + string.ljust('', 3)[:3] 

        #SURNAME
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][20][0:60]), 60)[:60] 
        else:
            outstring = outstring + string.ljust(cd[k][7][0:60], 60)[:60] 

        #FIRSTNAME
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.ljust(string.rstrip(cd[k][21][0:40]), 40)[:40] 
        else:
            outstring = outstring + string.ljust('', 40)[:40] 
            
        #ADDR1
        outstring = outstring + string.ljust(cparty.address[0:30], 30)[:30]    
                
        #ADDR2
        outstring = outstring + string.ljust(cparty.address2[0:30], 30)[:30]             
    
        #SUBURB
        outstring = outstring + string.ljust('', 30)[:30]        
    
        #TOWN
        outstring = outstring + string.ljust(cparty.city[0:30], 30)[:30] 

        #RADDR1
        if ca_key_found:
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.rjust(ca[cd[k][0]][9][0:30], 30)[:30]
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][9][0:30], 30)[:30]
        else:
                outstring = outstring + string.ljust('', 30)[:30]
    
        #RADDR2
        if ca_key_found:
            if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
                outstring = outstring + string.ljust(ca[cd[k][0]][10][0:30], 30)[:30]
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][10][0:30], 30)[:30]  
        else:
                outstring = outstring + string.ljust('', 30)[:30]
        
        #RSUBURB
        outstring = outstring + string.ljust('', 30)[:30] 
            
        #RTOWN
        if ca_key_found:
            if cd[k][17] == 'Individuals':
                outstring = outstring + string.ljust(ca[cd[k][0]][11][0:30], 30)[:30]
            else:
                outstring = outstring + string.ljust(ca[cd[k][0]][11][0:30], 30)[:30]
        else:
                outstring = outstring + string.ljust('', 30)[:30]
     
        #RCODE
        if ca_key_found :
            if RCODE <> 0:
                outstring = outstring + string.zfill(ca[cd[k][0]][13][0:5], 5)[:5]
            else:
                outstring = outstring + '00000'        
        else:
                outstring = outstring + '00000'        

        #DOB
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):           
            if len(cd[k][5])> 1:
                if string.find(cd[k][5], '-') <> - 1:
                    outstring = outstring + (string.split(cd[k][5], '-')[0] + string.split(cd[k][5], '-')[1] + string.split(cd[k][5], '-')[2]) [:8]
                elif string.find(cd[k][5], '/') <> - 1:   
                    outstring = outstring + (string.split(cd[k][5], '/')[0] + string.split(cd[k][5], '/')[1] + string.split(cd[k][5], '/')[2]) [:8]
                else:
                    outstring = outstring + '00000000'
            else:
                outstring = outstring + '00000000'
        else:
            outstring = outstring + '00000000'
            
        #IDTP
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.rjust('01', 2)
        elif (cd[k][17] == 'Private trusts') or (cd[k][17] == 'Trust companies'):
            outstring = outstring + string.rjust('03', 2)
        else:
            outstring = outstring + string.rjust('03', 2)
        
        #IDNO    
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.rjust(cd[k][3], 15)[:15]
        else:
            outstring = outstring + string.rjust(cd[k][4][0:15], 15)[:15]
            
        #TXNO
        outstring = outstring + string.zfill(cd[k][3][0:10], 10)
        
        #TAX-CAT
        if (cd[k][17] == 'Individuals') or (cd[k][17] == 'Individuals - Foreign'):
            outstring = outstring + string.rjust('01', 2)
        elif (cd[k][17] == 'Private trusts') or (cd[k][17] == 'Trust companies'):
            outstring = outstring + string.rjust('03', 2)
        else:
            outstring = outstring + string.rjust('02', 2)  
 
        #SA-RES
        if (cd[k][9] != 'SOUTH AFRICA') and (cd[k][15] != 'Foreign Company'):
            outstring = outstring + 'N'
        else:
            outstring = outstring + 'Y'
        
        #TP
        outstring = outstring + 'N'
        
        clients[cd[k][0]] = outstring
    return clients


def write_ABSA_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address, SARS_file, *rest):    

    postal_code = get_postal_code(cd)
    trd_details = get_trade_detail1(trdlist, FromDay, ToDay, cd_extra, postal_code)
    clients1 = get_client_details1(cd, trd_details, postal_code)
    clients2 = get_client_details2(cd, cd_address, postal_code)

    
    tmpfile = file(SARS_file, 'w')

    for ckey in clients1:
        if trd_details.has_key(ckey):
            tmpfile.write(clients1[ckey] + '\n')
            tmpfile.write(clients2[ckey] + '\n')
            tentries = trd_details[ckey][0]
            for ent in tentries:
                tmpfile.write(ent + '\n')

    tmpfile.close()
  
    return 'done'
    


def ASQL(*rest):
    acm.RunModuleWithParameters( 'SAMM_CALL_IT3B', 'Standard' )
    return 'SUCCESS'

#       INSTRUMENTS
#       ===========

def get_ins():
    trds1 = ael.TradeFilter['Call_All_Trades'].trades()
    trds2 = ael.TradeFilter['SAMM_Primary_Trades'].trades()

    ins = []
    for trds in trds1:
        ins.append(trds.insaddr.insid)
    for trds in trds2:
        ins.append(trds.insaddr.insid)
    ins.sort()
    return ins

    
#       TAX YEARS
#       =========
     
start_dates = []
d = ael.date("2010-03-01")
start_dates.append(d)
d = d.add_years(1)
while d <= ael.date_today():
    start_dates.append(d)
    d = d.add_years(1)
    
ael_variables = [('Operation', 'Operation_Main', 'string', ['Create SARS file', 'Create ABSA file', 'Produce all client statements', 'Produce one statement']),
                ('Year', 'Tax Year Starting_Main', 'date', start_dates, start_dates[0]),
                ('Ins', 'Account_Main', 'string', get_ins(), None, 0, 0, '', ''),
                ('Midbase_Client_Data', 'Midbase Data?_Main', 'string', ['Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Counterparty.csv'], 'Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Counterparty.csv'),
                ('Front_Midbase_Mapping', 'Front Midbase Mapping?_Main', 'string', ['Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Front and Midbase Data.csv'], 'Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Front and Midbase Data.csv'),
                ('Client_Address_File', 'Client Address?_Main', 'string', ['Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Front Client Address Lists.csv'], 'Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/Front Client Address Lists.csv'),
                ('Output_File', 'Output File?_Main', 'string', ['Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/PCREP.MLIVE.GSAM.TAX.ACAP.FEB2011.txt'], 'Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/PCREP.MLIVE.GSAM.TAX.ACAP.FEB2011.txt'),
                ('Output_Folder', 'OutPut Folder?_Main', 'string', ['Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/'], 'Y:/Jhb/Operations Secondary Markets/Income Tax/IT3b_2010/'),
                ('Printer_Name', 'Printer Name?_Main', 'string', ['TMSCS'], 'TMSCS'),]

def ael_main(ael_dict):
    
    try:
        
        FromDay = ael.date(ael_dict['Year'])							
        ToDay = FromDay.add_years(1)
        ToDay = ToDay.add_days(-1)

        trds1 = ael.TradeFilter['Call_All_Trades'].trades()
        trds2 = ael.TradeFilter['SAMM_Primary_Trades'].trades()
        trdlist = []
        party_list = []
        
        for trds in trds1:
            trdlist.append(trds)
            if trds.counterparty_ptynbr.ptynbr not in party_list:
                party_list.append(trds.counterparty_ptynbr.ptynbr)

        for trds in trds2:
            if trds.insaddr.exp_day >= FromDay and trds.value_day <= ToDay and not (trds.mirror_trdnbr):
                trdlist.append(trds)
                if trds.counterparty_ptynbr.ptynbr not in party_list:
                    party_list.append(trds.counterparty_ptynbr.ptynbr)

        
        mc_list = []
        cd, mc_list1 = load_ClientInfo(ael_dict['Midbase_Client_Data'], 1, party_list, 0)
        cd_extra, mc_list2 = load_ClientInfo(ael_dict['Front_Midbase_Mapping'], 0, party_list, 2) 
       
        for mc in mc_list2:
            if mc in mc_list1:
                mc_list.append(mc)
        
        cd_address = load_ClientAddress(ael_dict['Client_Address_File'], 2, mc_list)
         
        path = ael_dict['Output_Folder']
        SARSfile = ael_dict['Output_File']
        PrinterName = ael_dict['Printer_Name']
        
        op = ael_dict['Operation']
        if op == '':
            func=acm.GetFunction('msgBox', 3)
            func("Fail", "Select a valid operation", 0)
            
        elif op == 'Create SARS file':
            FromDay = datetime.date(FromDay.to_ymd()[0], FromDay.to_ymd()[1], FromDay.to_ymd()[2])
            ToDay = datetime.date(ToDay.to_ymd()[0], ToDay.to_ymd()[1], ToDay.to_ymd()[2])
            print write_SARS_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address, SARSfile)
            
        elif op == 'Create ABSA file':
            FromDay = datetime.date(FromDay.to_ymd()[0], FromDay.to_ymd()[1], FromDay.to_ymd()[2])
            ToDay = datetime.date(ToDay.to_ymd()[0], ToDay.to_ymd()[1], ToDay.to_ymd()[2])
            print write_ABSA_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address, SARSfile)
            
        elif op == 'Produce one statement':
            if ael_dict['Ins'] == '':
                func=acm.GetFunction('msgBox', 3)
                func("Fail", "Select a valid instrument", 0)
            else:
                trade = ael.Instrument[ael_dict['Ins']].trades()[0]
                trdlist = [trade]
                print write_XML_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address,  path, PrinterName)
            
        elif op == 'Produce all client statements':
            FDay = datetime.date(FromDay.to_ymd()[0], FromDay.to_ymd()[1], FromDay.to_ymd()[2])
            TDay = datetime.date(ToDay.to_ymd()[0], ToDay.to_ymd()[1], ToDay.to_ymd()[2])
            print write_XML_file(trdlist, FromDay, ToDay, cd, cd_extra, cd_address,  path, PrinterName)
        print op
        
    except:
    
        return 'Invalid Operation'

