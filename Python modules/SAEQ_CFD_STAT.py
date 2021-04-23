"""
History
=======

2017-05-24 Vojtech Sidorin  FAU-938 Update dependency on elementtree.
"""

import ael, random
from zak_funcs import formnum
from xml.etree.ElementTree import Element, SubElement, ElementTree

def GenCFDStatementXML(t,t2,startd, endd, CPRINT,CFAX, CEMAIL, freq,con,*rest):
    print t.insaddr.insid, t2.insaddr.insid
    status = 'FAILED'
    newdate = ael.date_today().to_string('%Y%m%d')
    s =  str(freq) + '_' + str(t.insaddr.insid[0:18]) + '_' + newdate+ '_'+ str(int(random.random()*1000)) +'.xml'
    #name = 'C://' + s
    name = name = '//v036syb004001/MoneyMarketStatements/Input' + s
    #name = '//services/frontnt/BackOffice/Atlas-End-Of-Day/MoneyMarketStatements/Input' + s
    #t2= t.prfnbr.trades()[0]
    if CPRINT == 1:
        
        STAT = Element("STATEMENT")
        
    else:
        DOC = Element("DOC")
        STAT = SubElement(DOC, "STATEMENT")
        try: 
            
            xmloutFile=open(name, 'w')
            
        except: 
            status = 'FAIL'
            raise 'cant open'
            print 'cant open'
    
    if endd > ael.date_today():
        endd = ael.date_today()
    
    
        
# ========================================================================================
#       CONTACT DETAILS 
# ========================================================================================  
        
    CUST = SubElement(STAT, "CUSTLIN1") 
    SubElement(CUST, "BNAM").text ='PRODUCT CONTROL GROUP'
    SubElement(CUST, "BAD1").text ='P O BOX 1190'
    SubElement(CUST, "BAD2").text ='JOHANNESBURG'
    SubElement(CUST, "BAD3").text ='SOUTH AFRICA'
    SubElement(CUST, "BAD4").text ='2000'
    SubElement(CUST, "BTEL").text ='+2711 350 2890'
    SubElement(CUST, "BFAX").text ='PRODUCT CONTROL GROUP'
    SubElement(CUST, "BCON").text ='NICOLETTE BURGER'
    
    SubElement(STAT, "MSG").text = ''
    
    
# ========================================================================================
#       CUSTOMER CONTACT DETAILS 
# ======================================================================================== 
 
    p = t.counterparty_ptynbr
    CNAM = p.fullname
    PRINT = 'FAX'
    flag = 0
    check = 0
    l1 = []
    ctot=[]
    if CPRINT == 1:
        c1 = []
        c1.append('PRINT')
        c1.append('TMSCS')
        ctot.append(c1)
        #flag = 1

    if CFAX != 0:
        c1 = []
        c1.append('FAX')
        c1.append(CFAX.replace('+27', '0'))
        ctot.append(c1)
        CFAX = 0
        #flag =1                                   
    
    if CEMAIL != 0:
        c1 = []
        c1.append('EMAIL')
        c1.append(CEMAIL)
        ctot.append(c1)
        CFAX = 0
        #flag =1   

    
    cts = p.contacts()
    if cts:
        for c in cts:
            #print c.pp()
            rules = c.rules()
            #print rules
            for r in rules:
                #print 'rules', flag, r.instype, t.insaddr.instype
                if r.instype == t.insaddr.instype and flag == 0:
                    Fax = c.fax
                    Attention = c.attention
                    #print Attention, flag
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
                        
                    flag =1
                    break
                 
    if flag == 0:
        
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
       
        
        Attention =p.attention
     
  
    
    CACC = str(t.insaddr.insid[0:18])
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
        fielda = "CTYPE" + str(ind)
        fieldb = "CDEST" + str(ind)
        SubElement(COM, fielda).text = x[0]
        SubElement(COM, fieldb).text = x[1]
        ind = ind +1
    
   

   
# ========================================================================================
#       HEADER 2
# ======================================================================================== 
 
    month = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'Novenber',12:'December'}
    sy, sm, sd = startd.to_ymd()
    ey, em, ed = endd.to_ymd()
    
    

    if p.attention:
        ATT = 'Attention:' + Attention
    else:
        ATT = 'Attention: To whom it may concern'
    ins = t.add_info('Funding Instype')
    H1 = ins
    H2 = str(sd) + ' ' + month[sm] + ' ' + str(sy) + ' to ' + str(ed) + ' ' + month[em] + ' ' + str(ey)
    
    
    HEAD2 = SubElement(STAT, "header2") 
    SubElement(HEAD2, "ATT").text = str(ATT)
    SubElement(HEAD2, "H1").text = H1
    SubElement(HEAD2, "H2").text = H2
    SubElement(HEAD2, "CDATE").text = str(endd)
   
# ========================================================================================
#                       SETUP 
# ========================================================================================
    legs = t.insaddr.legs()
    leg = legs[0]
    cashflows = legs[0].cash_flows()
    cf_list = []
    for cf in cashflows:
        cf_list.append([cf, t.quantity])
    
    leg2 = t2.insaddr.legs()[0]
    cfs2 = leg2.cash_flows()
    for cf in cfs2:
        cf_list.append([cf, t2.quantity])
    
    #print 'after', cf_list
    ins = t.insaddr
    daysx  = []
    daysy =[]
    dict_movement = {}
    movement = []
    OpeningBalance = 0.00
    total_interest = 0.00
    total_debits = 0.00
    total_credits = 0.00
    opening_int = 0.00
    today = ael.date_today()
    intbal =0
    ss = 'm'
    mx = 0
    dict_fixed= {}
    i1 = 0
    reinv = 0
    #All Movement and Interest Dates
    for cf in cashflows:
        if leg.reinvest == 0:
            if cf.type ==  'Interest Reinvestment' and cf.pay_day >= startd: 
                reinv = 1
                
    for cfs in cf_list:
        cf = cfs[0]
        if cf.type in ('Fixed Amount', 'Interest Reinvestment', 'Call Float Rate', 'Fixed Rate Adjustable'): 
            if cf.pay_day not in daysx:
                daysx.append(cf.pay_day)
            if cf.type == 'Fixed Amount' and cf.start_day:
                if cf.start_day not in daysx:
                    daysx.append(cf.start_day)
            
    daysx.sort()
    
       
    #MOVEMENTS
    for cfday in daysx:
        for cfs in cf_list:
            cf = cfs[0]
            if  cf.pay_day  == cfday :
                if cf.type in ('Fixed Amount', 'Interest Reinvestment') and abs(cf.projected_cf()*cfs[1]) > 0.005 :
                    if cf.type == 'Fixed Amount':
                            if cf.start_day:
                                cft = cf.start_day
                            else:
                                cft = cfday
                    else:
                        cft = cfday
                    if cf.type == 'Fixed Amount':
                        ss = 'm'
                    else:
                        ss = 'r'                
                
                    if (cf.pay_day >= startd and cf.pay_day <= endd) or (cf.start_day >= startd and cf.pay_day >= startd):
                        
                        if cf.type == 'Fixed Amount':
                            
                                s1 =[]
                                s1.append(str(cf.pay_day))
                                s1.append(ael.date_from_time(cf.creat_time))
                                s1.append(str(cf.cfwnbr))
                                val = cf.projected_cf() * cfs[1]
                                if val > 0:
                                    dstr = 'Transfer In  ' + cf.add_info('Account')
                                    s1.append(dstr)
                                else:
                                    dstr = 'Transfer Out  ' + cf.add_info('Account')
                                    s1.append(dstr)
                                s1.append(val)
                                s1.append(1)
                                movement.append(s1)
                                if cf.projected_cf()*cfs[1]< 0:
                                    total_debits = total_debits + cf.projected_cf()*cfs[1]
                                else:
                                    total_credits = total_credits + cf.projected_cf()*cfs[1]

                        else:
                            s1 =[]
                            s1.append(str(cf.pay_day))
                            s1.append(ael.date_from_time(cf.creat_time))
                            s1.append(str(cf.cfwnbr))
                            s1.append('Interest Reinvestment')
                            s1.append(cf.projected_cf() * cfs[1])
                            s1.append(1)
                            movement.append(s1)
                            
                            if cf.projected_cf()*t.quantity< 0:
                                total_debits = total_debits + cf.projected_cf()*cfs[1]
                            else:
                                total_credits = total_credits + cf.projected_cf()*cfs[1]
                    
                    if str(cft) in dict_movement.keys():
                        dict_movement[str(cft)].append([ss, cf.projected_cf()*cfs[1]])
                    else:
                        dict_movement[str(cft)] = [[ss, cf.projected_cf()*cfs[1]]]
            

                if cf.type == 'Call Float Rate' and (cf.pay_day >= startd and cf.pay_day <= endd): 
                    if cf.pay_day != ael.date_today():
                        
                        int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* cfs[1]
                        val = 0
                        if reinv ==1 or leg.reinvest == 1:
                            if cf.end_day != cf.pay_day:
                                val = get_cf(ins, cf.pay_day) + get_cf(ins, cf.end_day)
                                re_check = check_cf(ins, cf.pay_day) + check_cf(ins, cf.end_day)
                            else:
                                val = get_cf(ins, cf.pay_day)
                                re_check = check_cf(ins, cf.pay_day)
                        if cf.end_day <= startd and int_set!=0:
                            i1 = i1 + int_set
                        if int_set !=0 and (val == 0 and re_check == 0):
                            #print val, re_check
                            s1 =[]
                            s1.append(str(cf.pay_day))
                            s1.append(ael.date_from_time(cf.creat_time))
                            s1.append(str(cf.cfwnbr))
                            s1.append('Interest Settlement')
                            s1.append(int_set* t.quantity)
                                                              
                            
                            s1.append(0)
                            movement.append(s1)
                            
                            if int_set < 0:
                                total_debits = total_debits + int_set
                            else:
                                total_credits = total_credits + int_set
                                
                            if str(cfday) in dict_movement.keys():
                                dict_movement[str(cfday)].append(['i', int_set])
                            else:
                                dict_movement[str(cfday)] = [['i', int_set]]
                                
                          
                    
                if cf.type == 'Call Float Rate' and (leg.reinvest == 0):
                    
                    if cf.end_day <= startd and cf.pay_day > endd:
                        
                        int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* cfs[1]
                        mx =  mx + int_set
                            
            
    movement.sort(lambda x, y: cmp(ael.date(x[0]), ael.date(y[0])))
    
    
    #RESETS
    #======
    
    dict_reset = {}   
    for c in cashflows:
        if c.type == 'Call Float Rate':
            
            if (startd <= c.start_day and  endd >= c.start_day) or (c.end_day >= startd and c.end_day <= endd):
                               
                for r in c.resets():
                    
                    d1 = r.start_day
                    while d1 < r.end_day:
                    
                        if str(d1) in dict_reset.keys():
                            pass
                            #dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                        else:   
                            dict_reset[str(d1)] =  r.value + c.spread
                            #print 'forward', r.forward_rate(), 'spread', c.spread
                        d1 = d1.add_days(1)
                        
    dict_resetA = {}   
    for c in cfs2:
        if c.type == 'Call Float Rate':
            
            if (startd <= c.start_day and  endd >= c.start_day) or (c.end_day >= startd and c.end_day <= endd):
                               
                for r in c.resets():
                    d1 = r.start_day
                    while d1 < r.end_day:
                    
                        if str(d1) in dict_resetA.keys():
                            pass
                            #dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                        else:   
                            dict_resetA[str(d1)] =  r.value + c.spread
                        d1 = d1.add_days(1)
                           
    #print dict_reset 
    #print dict_resetA 
#===========================================================================================
#                                       DAILY INTEREST
#===========================================================================================
    
    interest = []
    total = 0
    reset_rate = 0
    sd = startd
    if len(daysx) > 0:
        sd1 = daysx[0]
    else:
        sd1 = sd
    ed = endd
    mov1 = 0
    mov = 0
    bal =0
    total_interest = 0.00
    ClosingBalance = 0.00
    OpeningBalance = 0
    m1 = 0
   
    while sd1 < startd:
        if str(sd1) in  dict_movement.keys():
            for mov in  dict_movement[str(sd1)]:
                if mov[0] in ('m', 'r'):
                    m1 = mov[1] + m1
                
        sd1 = sd1.add_days(1)
    OpeningBalance = m1 
    bal = m1 
    set =0
    due = 0
    acc =0
    val = 0
    
    for days in  dict_fixed.keys():
       if ael.date(days).add_days(-1) <= startd:
            for mov in  dict_fixed[days]:
                val = mov[1] + val
                
    acc = leg.interest_accrued(leg.start_day, startd, 'ZAR')*t.quantity *(-1) + leg2.interest_accrued(leg2.start_day, startd, 'ZAR')*t2.quantity *(-1)
    total = -1*(i1 + val + mx) + acc
    
    while sd <= ed:
        intbal = 0
        day1 = sd
        day2 = sd.add_days(1)
        sd = day2
        l2 =[]
        intbal = 0        
        
        if str(day1) in  dict_movement.keys():
            mov1 = 0
            for mov in  dict_movement[str(day1)]:
                
                if mov[0] in ('m', 'r'):
                    mov1 = mov[1] + mov1
                if mov[0] =='i':
                    intbal = intbal + mov[1]
                if mov[0] =='r':
                    intbal = intbal + (mov[1])*(-1)
                                 
                   
        else:
            mov1 =   0
        int_set = 0
        int_acc = 0
        int_due = 0
        
        
        int_set = leg.interest_settled(day1, day2, 'ZAR') 
        int_acc = leg.interest_accrued(day1, day2, 'ZAR') 
        int_due = leg.interest_due(day1, day2, 'ZAR')
        
        int_set1 = leg2.interest_settled(day1, day2, 'ZAR')
        int_acc1 = leg2.interest_accrued(day1, day2, 'ZAR')
        int_due1 = leg2.interest_due(day1, day2, 'ZAR')
               
        tot = (int_set + int_acc + int_due)*t.quantity *-1
        tot1 = (int_set1 + int_acc1 + int_due1)*t2.quantity *-1
        
        if round(tot, 2) == 0 and round(tot1, 2) != 0:
            tot = tot1
            try:
                reset_rate = dict_resetA[str(day1)]
            except:
                pass
        elif round(tot1, 2) !=0 and round(tot, 2) !=0:
            tot = tot + tot1
            #reset_rate = '??'
        else:
            try:
                reset_rate = dict_reset[str(day1)]
            except:
                pass
        #print 'total A ', tot,'total B ', tot1, reset_rate
        total_interest = tot + total_interest
        bal = bal + mov1
        total = total + tot + intbal 
        intbal = 0
        
        if tot !=0 or total !=0:
            l2.append(day1.to_string('%Y/%m/%d'))
            l2.append(tot)
            #try:
            #    reset_rate = dict_reset[str(day1)]
            #except:
                
            #    pass
            l2.append(reset_rate)
            l2.append(total)
            l2.append(bal)
            
            interest.append(l2)
            acc =0
            
    
    ClosingBalance = bal
    
    
#=========================================================================================        
#                       XML
#=========================================================================================    

    # SUMMARY
    # =========
    
    OB = formnum(OpeningBalance)
    TC =  formnum(total_credits)
    TD =  formnum(total_debits)
    TI = formnum(total_interest)
    CB =  formnum(ClosingBalance)
    
    ACCSUM = SubElement(STAT, "ACCSUM") 
    SubElement(ACCSUM, "OBAL").text = OB
    SubElement(ACCSUM, "TCRED").text = TC
    SubElement(ACCSUM, "TDEB").text = TD
    SubElement(ACCSUM, "TINT").text = TI
    SubElement(ACCSUM, "CBAL").text = CB
    
    
    
    SubElement(STAT, "YourTrans")
    sum1 = OpeningBalance

    # MOVEMENTS
    # =========
    
    TRANS = SubElement(STAT, "TRANLIN")
    SubElement(TRANS, "VDAT").text = startd.to_string('%Y/%m/%d')
    SubElement(TRANS, "PDAT").text = ""
    SubElement(TRANS, "DLNO").text = ""
    SubElement(TRANS, "CDES").text = "Balance Brought Forward"
    SubElement(TRANS, "TAMT").text = OB
    SubElement(TRANS, "TABAL").text = OB
    
    for x in movement:
        output=''
        if x[5] == 1:
            sum1 = sum1 + x[4]
        
        
        TA = formnum(x[4])
        S =  formnum(sum1)
        
        
        TRANS = SubElement(STAT, "TRANLIN")
        SubElement(TRANS, "VDAT").text = ael.date(x[0]).to_string('%Y/%m/%d')
        SubElement(TRANS, "PDAT").text = ael.date(x[1]).to_string('%Y/%m/%d')
        SubElement(TRANS, "DLNO").text = str(x[2])
        SubElement(TRANS, "CDES").text = str(x[3])
        SubElement(TRANS, "CREF").text = str(x[2])
        SubElement(TRANS, "TAMT").text = TA
        SubElement(TRANS, "TABAL").text = S

    # INTEREST
    # ========
    
     
    INTEREST = SubElement(STAT, "INTEREST")
    for x in interest:
        output=''
        
        IA = formnum(x[1]) #str(x[1])
        IB = formnum(x[3]) #str(x[3])
        AB = formnum(x[4]) #str(x[4])
        
        
        INTLIN = SubElement(STAT, "INTLIN")
        SubElement(INTLIN, "VDAT").text = str(x[0])
        SubElement(INTLIN, "IAMNT").text = IA
        SubElement(INTLIN, "IRATE").text = formnum(x[2])
        SubElement(INTLIN, "IBAL").text = IB
        SubElement(INTLIN, "ABAL").text = AB

    #Footer
    #======
    
    
    #if CPRINT == 1:
    #    return STAT
        
    #else:    
    ElementTree(DOC).write(xmloutFile, encoding='utf-8')
    return 'SUCCESS'


#================================================================================================================= 
#=================================================================================================================

def get_cf(ins, d):
    val = 0
    for cf in ins.legs()[0].cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day == d:
            val = val + cf.projected_cf()
    return val 
    
def check_cf(ins, d):
    
    for cf in ins.legs()[0].cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day == d:
            return 1
    return 0
    
